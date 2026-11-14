"""Renderiza uma cena descrita em JSON (peças STL + matriz + cor) com o Blender (Cycles, CPU).

Uso:
  blender -b --python cad/render_blender.py -- cena.json saida.png [--az 35] [--el 18] [--res 1400x1400]
          [--amostras 48] [--explodir 1.0] [--sem-componentes] [--so-componentes] [--orto] [--mesa]

cena.json = montagem.json gerado por cad/gerar.py (ou o mesas.json, com --mesa).
Unidades do JSON: mm. A cena do Blender fica em metros (escala 0,001).
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
cena_json, saida = argv[0], argv[1]


def opt(nome, padrao=None, tipo=str):
    if nome in argv:
        return tipo(argv[argv.index(nome) + 1])
    return padrao


AZ = opt("--az", 35.0, float)
EL = opt("--el", 16.0, float)
RES = opt("--res", "1400x1400")
AMOSTRAS = opt("--amostras", 48, int)
EXPLODIR = opt("--explodir", 0.0, float)
ZOOM = opt("--zoom", 1.0, float)
SEM_COMP = "--sem-componentes" in argv
SO_COMP = "--so-componentes" in argv
ORTO = "--orto" in argv
MESA = "--mesa" in argv
FUNDO = opt("--fundo", "0.93,0.93,0.95")
SO_MATERIAL = opt("--so-material", None)      # ex.: PETG = mostra só o esqueleto

S = 0.001
base = os.path.dirname(os.path.abspath(cena_json))
cena = json.load(open(cena_json))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = AMOSTRAS
sc.cycles.use_denoising = bool(getattr(bpy.app.build_options, "openimagedenoise", False))
sc.cycles.use_adaptive_sampling = True
w, h = (int(v) for v in RES.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.render.film_transparent = False
sc.view_settings.view_transform = "Standard"

mats = {}


def material(rgb, rug=0.45, emissao=0.0):
    k = (tuple(round(c, 3) for c in rgb), rug, emissao)
    if k in mats:
        return mats[k]
    m = bpy.data.materials.new("m%d" % len(mats))
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rug
    if emissao:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emissao
    mats[k] = m
    return m


def importa(arquivo):
    antes = set(bpy.data.objects)
    bpy.ops.wm.stl_import(filepath=arquivo) if hasattr(bpy.ops.wm, "stl_import") else bpy.ops.import_mesh.stl(filepath=arquivo)
    return [o for o in bpy.data.objects if o not in antes][0]


cache = {}
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))


def poe(item, eh_comp):
    global lo, hi
    arq = os.path.join(base, item["arquivo"])
    for k, M in enumerate(item["para_montagem"]):
        if arq in cache:
            ob = cache[arq].copy()
            bpy.context.collection.objects.link(ob)
        else:
            ob = importa(arq)
            cache[arq] = ob
            for p in ob.data.polygons:
                p.use_smooth = bool(item.get("liso", not eh_comp))
        Mm = Matrix(M)
        ex = Vector(item.get("explode", [0, 0, 0])) * EXPLODIR
        if "explode_inst" in item:
            ex = Vector(item["explode_inst"][k]) * EXPLODIR
        T = Matrix.Translation(ex) @ Mm
        # mm -> m
        Sm = Matrix.Diagonal((S, S, S, 1))
        ob.matrix_world = Sm @ T
        rgb = item.get("rgb", [0.6, 0.6, 0.6])
        ob.data = ob.data.copy() if k else ob.data
        ob.data.materials.clear()
        ob.data.materials.append(material(rgb, item.get("rug", 0.45 if not eh_comp else 0.6), item.get("emissao", 0.0)))
        for c in ob.bound_box:
            pw = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo.x, pw.x), min(lo.y, pw.y), min(lo.z, pw.z)))
            hi = Vector((max(hi.x, pw.x), max(hi.y, pw.y), max(hi.z, pw.z)))


if not SO_COMP:
    for it in cena.get("pecas", []):
        if SO_MATERIAL and it.get("material") != SO_MATERIAL:
            continue
        poe(it, False)
if not SEM_COMP:
    for it in cena.get("componentes", []):
        poe(it, True)

centro = (lo + hi) / 2
tam = hi - lo

# chão
bpy.ops.mesh.primitive_plane_add(size=20, location=(centro.x, centro.y, lo.z - 0.0002))
chao = bpy.context.object
fr, fg, fb = (float(v) for v in FUNDO.split(","))
chao.data.materials.append(material((fr, fg, fb), 0.9))

# placas da mesa (256 x 256) no modo --mesa
for pl in cena.get("mesas", []) if MESA else []:
    x0, y0, lado = pl["x0"] * S, pl["y0"] * S, pl["lado"] * S
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x0 + lado / 2, y0 + lado / 2, lo.z - 0.0001))
    p = bpy.context.object
    p.scale = (lado, lado, 1)
    p.data.materials.append(material((0.16, 0.17, 0.19), 0.7))

# mundo e luzes
mundo = bpy.data.worlds.new("m")
sc.world = mundo
mundo.use_nodes = True
mundo.node_tree.nodes["Background"].inputs[0].default_value = (fr, fg, fb, 1)
mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.55


def luz(tipo, loc, energia, tamanho=1.0, alvo=centro):
    d = bpy.data.lights.new("l", tipo)
    d.energy = energia
    if tipo == "AREA":
        d.size = tamanho
    if tipo == "SUN":
        d.angle = 0.3
    o = bpy.data.objects.new("l", d)
    o.location = loc
    bpy.context.collection.objects.link(o)
    dirv = (Vector(alvo) - Vector(loc)).normalized()
    o.rotation_euler = dirv.to_track_quat("-Z", "Y").to_euler()
    return o


R = max(tam.x, tam.y, tam.z)
az = math.radians(AZ)
el = math.radians(EL)
dir_cam = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))  # +Y = frente
luz("AREA", centro + Vector((math.sin(az + 0.7), math.cos(az + 0.7), 1.1)) * R * 2.2, 4.2 * R * R / 0.09, R * 1.6)
luz("AREA", centro + Vector((math.sin(az - 1.0), math.cos(az - 1.0), 0.5)) * R * 2.2, 1.6 * R * R / 0.09, R * 2.0)
luz("AREA", centro + Vector((-math.sin(az), -math.cos(az), 0.9)) * R * 2.2, 1.4 * R * R / 0.09, R * 2.0)

cd = bpy.data.cameras.new("c")
cam = bpy.data.objects.new("c", cd)
bpy.context.collection.objects.link(cam)
sc.camera = cam
cam.rotation_euler = (-dir_cam).to_track_quat("-Z", "Y").to_euler()
# enquadra pelos 8 cantos
cantos = [Vector((x, y, z)) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)]
dir_r = cam.rotation_euler.to_matrix() @ Vector((1, 0, 0))
dir_u = cam.rotation_euler.to_matrix() @ Vector((0, 1, 0))
meia_x = max(abs((c - centro).dot(dir_r)) for c in cantos)
meia_y = max(abs((c - centro).dot(dir_u)) for c in cantos)
prof = max(abs((c - centro).dot(dir_cam)) for c in cantos)
asp = w / h
if ORTO:
    cd.type = "ORTHO"
    cd.ortho_scale = 2.16 * max(meia_x, meia_y * asp) / ZOOM
    cam.location = centro + dir_cam * (prof + R * 3)
else:
    cd.lens = 70
    cd.sensor_width = 36
    fov_x = 2 * math.atan(18 / 70)
    fov_y = 2 * math.atan(18 / asp / 70)
    dist = max(meia_x / math.tan(fov_x / 2), meia_y / math.tan(fov_y / 2)) * 1.1 / ZOOM + prof
    cam.location = centro + dir_cam * dist
cd.clip_start = 0.001
cd.clip_end = 100

sc.render.filepath = saida
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("RENDER_OK", saida)
