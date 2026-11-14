"""Renderiza o MAPA DE BALANÇOS de uma peça (PLY com cor por face gerado por cad/comum/imprimibilidade.py).

Uso (quem chama é `imprimibilidade.py --mapa`, pela fila de render):
  blender -b --python cad/render_balancos.py -- peca.ply saida [--vistas "35,-45;215,-45;35,28"] [--res 620x620] [--amostras 24]

Grava saida-0.png, saida-1.png, … (uma por vista "azimute,elevação"; elevação NEGATIVA = câmera por baixo da peça,
que é onde ficam as faces sem apoio). Sem chão e com luz ambiente por todos os lados, para o lado de baixo aparecer.
Cores: vermelho = sem apoio, amarelo = balanço tolerado, azul = face na mesa, cinza = resto.
"""
import math
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
ply, saida = argv[0], argv[1]


def opt(nome, padrao, tipo=str):
    return tipo(argv[argv.index(nome) + 1]) if nome in argv else padrao


VISTAS = [tuple(float(v) for v in par.split(",")) for par in opt("--vistas", "35,-45;215,-45;35,28").split(";")]
RES = opt("--res", "620x620")
AMOSTRAS = opt("--amostras", 24, int)
S = 0.001                                   # mm -> m

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = AMOSTRAS
sc.cycles.use_denoising = bool(getattr(bpy.app.build_options, "openimagedenoise", False))
w, h = (int(v) for v in RES.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.view_settings.view_transform = "Standard"

antes = set(bpy.data.objects)
if hasattr(bpy.ops.wm, "ply_import"):
    bpy.ops.wm.ply_import(filepath=ply)
else:
    bpy.ops.import_mesh.ply(filepath=ply)
ob = [o for o in bpy.data.objects if o not in antes][0]
ob.scale = (S, S, S)
bpy.context.view_layer.update()
for p in ob.data.polygons:
    p.use_smooth = False
atribs = [a.name for a in ob.data.color_attributes]
if not atribs:
    print("SEM_COR: o PLY chegou sem atributo de cor")
    sys.exit(3)

m = bpy.data.materials.new("mapa")
m.use_nodes = True
nt = m.node_tree
b = nt.nodes["Principled BSDF"]
cor = nt.nodes.new("ShaderNodeVertexColor")
cor.layer_name = atribs[0]
nt.links.new(cor.outputs["Color"], b.inputs["Base Color"])
b.inputs["Roughness"].default_value = 0.7
if "Emission Color" in b.inputs:            # um pouco de luz própria: a cor se lê mesmo na sombra
    nt.links.new(cor.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 0.6
ob.data.materials.clear()
ob.data.materials.append(m)

mundo = bpy.data.worlds.new("m")
sc.world = mundo
mundo.use_nodes = True
mundo.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.3

cantos = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
lo = Vector((min(c.x for c in cantos), min(c.y for c in cantos), min(c.z for c in cantos)))
hi = Vector((max(c.x for c in cantos), max(c.y for c in cantos), max(c.z for c in cantos)))
centro = (lo + hi) / 2
R = max(hi - lo)

cd = bpy.data.cameras.new("c")
cam = bpy.data.objects.new("c", cd)
bpy.context.collection.objects.link(cam)
sc.camera = cam
cd.lens, cd.sensor_width = 70, 36
cd.clip_start, cd.clip_end = 0.001, 100
sol_d = bpy.data.lights.new("sol", "SUN")
sol_d.energy = 1.3
sol_d.angle = 0.5
sol = bpy.data.objects.new("sol", sol_d)
bpy.context.collection.objects.link(sol)

for i, (az_g, el_g) in enumerate(VISTAS):
    az, el = math.radians(az_g), math.radians(el_g)
    dir_cam = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))   # +Y = frente
    cam.rotation_euler = (-dir_cam).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    rot = cam.rotation_euler.to_matrix()
    dir_r, dir_u = rot @ Vector((1, 0, 0)), rot @ Vector((0, 1, 0))
    meia_x = max(abs((c - centro).dot(dir_r)) for c in cantos)
    meia_y = max(abs((c - centro).dot(dir_u)) for c in cantos)
    prof = max(abs((c - centro).dot(dir_cam)) for c in cantos)
    fov_x = 2 * math.atan(18 / 70)
    fov_y = 2 * math.atan(18 / (w / h) / 70)
    dist = max(meia_x / math.tan(fov_x / 2), meia_y / math.tan(fov_y / 2)) * 1.12 + prof
    cam.location = centro + dir_cam * dist
    # luz principal do lado da câmera, um pouco para o lado e para "cima" da imagem
    d_luz = (dir_cam + 0.45 * dir_r + 0.35 * dir_u).normalized()
    sol.rotation_euler = (-d_luz).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"{saida}-{i}.png"
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    print("RENDER_OK", sc.render.filepath)
