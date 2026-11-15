"""Cena do banner: os 4 robôs REAIS (STL do repo, cores do montagem.json) sobre uma mesa de madeira, com luz quente
e fundo desfocado. É a base do banner do guia, do hero e da capa (comum/cad/banners.py põe o texto por cima).

Uso (pela fila de render):
  blender -b --python comum/cad/render_cena.py -- saida.png [--res 2800x1576] [--amostras 256] [--lente 70]
          [--largura 1.9] [--dx 0.0] [--dy 0.0] [--el 9] [--fstop 3.2] [--fundo fundo.png] [--robos dino,capivara,cubo,cubo_rodas]
          [--sem-fase2]

--largura = largura da cena (m) que cabe no quadro na distância dos robôs; --dx/--dy deslocam o grupo no quadro
(fração da largura/altura: dx > 0 leva os robôs para a DIREITA, deixando a esquerda livre para o título; dy > 0 leva
para CIMA).
--fundo = imagem já desfocada da sala (gerada por banners.py); sem ela, o fundo é um degradê quente.
Nada aqui é gerado por IA: são as peças do repo, na pose neutra, cada robô só girado em torno do eixo vertical.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
saida = argv[0]


def opt(nome, padrao=None, tipo=str):
    return tipo(argv[argv.index(nome) + 1]) if nome in argv else padrao


RES = opt("--res", "2800x1576")
AMOSTRAS = opt("--amostras", 256, int)
LENTE = opt("--lente", 70.0, float)
LARGURA = opt("--largura", 1.9, float)
DX = opt("--dx", 0.0, float)
DY = opt("--dy", 0.0, float)
EL = opt("--el", 9.0, float)
FSTOP = opt("--fstop", 3.2, float)
FUNDO = opt("--fundo", None)
ROBOS = opt("--robos", "dino,capivara,cubo,cubo_rodas").split(",")
SEM_FASE2 = "--sem-fase2" in argv

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTAS = {"dino": "dino", "capivara": "capivara", "cubo": "cubo", "cubo_rodas": "cubo-rodas"}   # = comum/cad/caminhos.py
S = 0.001

# Lugar de cada robô na mesa (mm) e giro em torno do eixo vertical (graus; + = vira o rosto para a ESQUERDA da imagem).
# A câmera fica na frente (+Y) olhando para -Y: na imagem, a DIREITA é -X. Ordem na imagem, da esquerda para a direita:
# dinossauro, capivara, cubo, cubo com rodas (a mesma ordem do texto do banner).
LUGAR = {
    "dino": (300, 45, -32),           # à esquerda, virado para o centro: aparecem a cauda, os 2 braços e os 2 pés
    "capivara": (85, -55, -10),       # meio passo atrás
    "cubo": (-100, 85, 10),           # o menor, na frente
    "cubo_rodas": (-335, -40, 22),    # o mais alto; afastado do cubo para as 2 rodas aparecerem
}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = AMOSTRAS
sc.cycles.use_denoising = bool(getattr(bpy.app.build_options, "openimagedenoise", False))
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.005
sc.cycles.sample_clamp_indirect = 4.0
sc.cycles.max_bounces = 6
w, h = (int(v) for v in RES.split("x"))
sc.render.resolution_x, sc.render.resolution_y = w, h
sc.view_settings.view_transform = "Standard"      # o mesmo dos outros renders: as cores do modelo saem como são

mats = {}


def material(rgb, rug=0.42, emissao=0.0):
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


lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))


def poe_robo(mid):
    global lo, hi
    base = os.path.join(RAIZ, "projetos", PASTAS[mid])
    cena = json.load(open(os.path.join(base, "montagem.json")))
    x, y, giro = LUGAR[mid]
    lugar = Matrix.Translation((x, y, 0)) @ Matrix.Rotation(math.radians(giro), 4, "Z")
    cache = {}
    for eh_comp, itens in ((False, cena.get("pecas", [])), (True, cena.get("componentes", []))):
        for it in itens:
            if eh_comp and SEM_FASE2 and it.get("fase2"):
                continue
            arq = os.path.join(base, it["arquivo"])
            for k, M in enumerate(it["para_montagem"]):
                if arq in cache:
                    ob = cache[arq].copy()
                    ob.data = ob.data.copy()
                    bpy.context.collection.objects.link(ob)
                else:
                    ob = importa(arq)
                    cache[arq] = ob
                    for p in ob.data.polygons:
                        p.use_smooth = bool(it.get("liso", not eh_comp))
                ob.matrix_world = Matrix.Diagonal((S, S, S, 1)) @ lugar @ Matrix(M)
                ob.data.materials.clear()
                ob.data.materials.append(material(it.get("rgb", [0.6, 0.6, 0.6]), it.get("rug", 0.42 if not eh_comp else 0.6),
                                                  it.get("emissao", 0.0)))
                for c in ob.bound_box:
                    pw = ob.matrix_world @ Vector(c)
                    lo = Vector((min(lo.x, pw.x), min(lo.y, pw.y), min(lo.z, pw.z)))
                    hi = Vector((max(hi.x, pw.x), max(hi.y, pw.y), max(hi.z, pw.z)))


for r in ROBOS:
    poe_robo(r)
centro = Vector(((lo.x + hi.x) / 2, 0.0, (lo.z + hi.z) / 2))
zmesa = lo.z - 0.0003

# ---------------------------------------------------------------------------------------------- mesa de madeira
bpy.ops.mesh.primitive_plane_add(size=1, location=(centro.x, 0.5, zmesa))
mesa = bpy.context.object
mesa.scale = (9.0, 5.0, 1)                      # 9 m de largura; a borda de trás fica 2 m atrás dos robôs
mm = bpy.data.materials.new("madeira")
mm.use_nodes = True
nt = mm.node_tree
bsdf = nt.nodes["Principled BSDF"]
geo = nt.nodes.new("ShaderNodeNewGeometry")                 # posição no MUNDO (m): a textura não depende da escala do plano
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])


def conta(op, a, b=None, v=None):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    nt.links.new(a, n.inputs[0])
    if b is not None:
        nt.links.new(b, n.inputs[1])
    if v is not None:
        n.inputs[1].default_value = v
    return n.outputs[0]


# tábuas de 16 cm ao longo de X: cada uma com um tom e um deslocamento do veio próprios
tabua = conta("FLOOR", conta("DIVIDE", sep.outputs["Y"], v=0.16))
ruido_tabua = nt.nodes.new("ShaderNodeTexWhiteNoise")
ruido_tabua.noise_dimensions = "1D"
nt.links.new(tabua, ruido_tabua.inputs["W"])
# veio: ruído muito esticado ao longo de X (riscas finas) + ondas largas
junta = nt.nodes.new("ShaderNodeCombineXYZ")
nt.links.new(conta("ADD", sep.outputs["X"], conta("MULTIPLY", ruido_tabua.outputs["Value"], v=7.0)), junta.inputs["X"])
nt.links.new(sep.outputs["Y"], junta.inputs["Y"])
mp = nt.nodes.new("ShaderNodeMapping")
mp.inputs["Scale"].default_value = (1.6, 55.0, 1.0)
nt.links.new(junta.outputs["Vector"], mp.inputs["Vector"])
veio = nt.nodes.new("ShaderNodeTexNoise")
veio.inputs["Scale"].default_value = 2.2
veio.inputs["Detail"].default_value = 7.0
veio.inputs["Roughness"].default_value = 0.62
veio.inputs["Distortion"].default_value = 0.7
nt.links.new(mp.outputs["Vector"], veio.inputs["Vector"])
mp2 = nt.nodes.new("ShaderNodeMapping")
mp2.inputs["Scale"].default_value = (0.5, 9.0, 1.0)
nt.links.new(junta.outputs["Vector"], mp2.inputs["Vector"])
onda = nt.nodes.new("ShaderNodeTexNoise")
onda.inputs["Scale"].default_value = 1.5
onda.inputs["Detail"].default_value = 2.0
nt.links.new(mp2.outputs["Vector"], onda.inputs["Vector"])
mist = nt.nodes.new("ShaderNodeMixRGB")
mist.inputs["Fac"].default_value = 0.45
nt.links.new(veio.outputs["Fac"], mist.inputs["Color1"])
nt.links.new(onda.outputs["Fac"], mist.inputs["Color2"])
tom = conta("ADD", mist.outputs["Color"], conta("MULTIPLY", conta("SUBTRACT", ruido_tabua.outputs["Value"], v=0.5), v=0.16))
rampa = nt.nodes.new("ShaderNodeValToRGB")
rampa.color_ramp.elements[0].position = 0.30
rampa.color_ramp.elements[0].color = (0.115, 0.042, 0.012, 1)    # veio escuro
rampa.color_ramp.elements[1].position = 0.74
rampa.color_ramp.elements[1].color = (0.33, 0.145, 0.045, 1)     # mel
nt.links.new(tom, rampa.inputs["Fac"])
# fresta escura e fina entre as tábuas
frac = conta("FRACT", conta("DIVIDE", sep.outputs["Y"], v=0.16))
borda2 = conta("MAXIMUM", conta("LESS_THAN", frac, v=0.012), conta("GREATER_THAN", frac, v=0.988))   # 1 na fresta
cor = nt.nodes.new("ShaderNodeMixRGB")
nt.links.new(borda2, cor.inputs["Fac"])
nt.links.new(rampa.outputs["Color"], cor.inputs["Color1"])
cor.inputs["Color2"].default_value = (0.03, 0.012, 0.004, 1)
nt.links.new(cor.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.40
for nome in ("Coat Weight", "Clearcoat"):
    if nome in bsdf.inputs:
        bsdf.inputs[nome].default_value = 0.10
rel = nt.nodes.new("ShaderNodeBump")
rel.inputs["Strength"].default_value = 0.05
rel.inputs["Distance"].default_value = 0.002
nt.links.new(conta("SUBTRACT", mist.outputs["Color"], borda2), rel.inputs["Height"])
nt.links.new(rel.outputs["Normal"], bsdf.inputs["Normal"])
mesa.data.materials.append(mm)

# --------------------------------------------------------------------------------------------------- câmera
el = math.radians(EL)
dir_cam = Vector((0.0, math.cos(el), math.sin(el)))                 # câmera na frente (+Y), um pouco acima
cd = bpy.data.cameras.new("c")
cam = bpy.data.objects.new("c", cd)
bpy.context.collection.objects.link(cam)
sc.camera = cam
cd.lens = LENTE
cd.sensor_width = 36
dist = LARGURA / (2 * math.tan(math.atan(18 / LENTE)))
alvo = Vector((centro.x, 0.0, centro.z))
cam.location = alvo + dir_cam * dist
cam.rotation_euler = (-dir_cam).to_track_quat("-Z", "Y").to_euler()
cd.shift_x = -DX                                                    # desloca o quadro sem mudar a perspectiva
cd.shift_y = -DY * h / w
cd.clip_start, cd.clip_end = 0.01, 200
cd.dof.use_dof = FSTOP > 0
cd.dof.focus_distance = dist - 0.02
cd.dof.aperture_fstop = max(FSTOP, 0.1)
cd.dof.aperture_blades = 0

# ---------------------------------------------------------------------------------------------------- fundo
# plano emissor atrás da mesa: a "sala" já desfocada (imagem) ou um degradê quente
bpy.ops.mesh.primitive_plane_add(size=1, location=(centro.x, -6.0, 0.35))
tela = bpy.context.object
tela.rotation_euler = (math.radians(90), 0, math.radians(180))     # de frente para a câmera, sem espelhar a imagem
tela.scale = (8.0, 2.4, 1)                                          # 8 x 2,4 m = a proporção de fundo.png (3200 x 960)
mf = bpy.data.materials.new("fundo")
mf.use_nodes = True
nf = mf.node_tree
for n in list(nf.nodes):
    nf.nodes.remove(n)
out = nf.nodes.new("ShaderNodeOutputMaterial")
em = nf.nodes.new("ShaderNodeEmission")
em.inputs["Strength"].default_value = 0.8
if FUNDO and os.path.exists(FUNDO):
    tx = nf.nodes.new("ShaderNodeTexImage")
    tx.image = bpy.data.images.load(FUNDO)
    tx.extension = "EXTEND"
    nf.links.new(tx.outputs["Color"], em.inputs["Color"])
else:
    em.inputs["Color"].default_value = (0.10, 0.045, 0.02, 1)
nf.links.new(em.outputs["Emission"], out.inputs["Surface"])
tela.data.materials.append(mf)

mundo = bpy.data.worlds.new("m")
sc.world = mundo
mundo.use_nodes = True
mundo.node_tree.nodes["Background"].inputs[0].default_value = (0.20, 0.11, 0.06, 1)
mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.12

# ---------------------------------------------------------------------------------------------------- luzes


def luz(loc, energia, tamanho, cor, alvo_=None):
    d = bpy.data.lights.new("l", "AREA")
    d.energy, d.size, d.color = energia, tamanho, cor
    o = bpy.data.objects.new("l", d)
    o.location = loc
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (Vector(alvo_ if alvo_ is not None else alvo) - Vector(loc)).normalized().to_track_quat("-Z", "Y").to_euler()
    return o


luz(alvo + Vector((0.9, 1.5, 1.25)), 54, 1.6, (1.0, 0.87, 0.72))            # principal: quente, da frente/esquerda da imagem
luz(alvo + Vector((-1.4, 1.2, 0.5)), 8, 2.0, (1.0, 0.93, 0.86))            # preenchimento, do outro lado
luz(alvo + Vector((-1.1, -1.5, 1.1)), 48, 0.9, (1.0, 0.60, 0.25))           # contraluz âmbar (recorta a silhueta)
luz(alvo + Vector((1.3, -1.4, 0.9)), 32, 0.9, (1.0, 0.66, 0.32))            # contraluz âmbar do outro lado
luz(alvo + Vector((0.0, 0.3, 1.9)), 15, 2.4, (1.0, 0.88, 0.74))             # de cima, suave

sc.render.filepath = saida
sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
print("CENA_OK", saida, "dist %.2f m" % dist)
