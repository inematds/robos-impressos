"""Partes comuns dos dois robôs quadrados (cubo de mesa e cubo que roda): cabeça-cubo com tela, garfo INTERNO do
tilt, pescoço (tubo oco + engrenagens 2:1) e suporte do servo de pan.

Ideias que valem para os dois (rodada 2, etapa E1):
- A cabeça é um COPO (casca de 5 lados) impresso com o fundo (as costas) na mesa e a boca para cima: nenhuma ponte,
  nenhum teto. Arestas compridas com raio grande (são verticais na impressão), aresta de trás com chanfro de 45°
  (é a que encosta na mesa), borda da frente arredondada (fica virada para cima).
- O rosto é um PAINEL escuro de cantos arredondados, encaixado 1 mm para dentro da borda do copo (fresta de sombra).
  Nenhum parafuso na frente: o painel tem 4 pilares para trás e é preso por trás do quadro; o copo entra por trás e
  é preso por 4 M3 na parede de trás. Câmera atrás do painel (furo de 8 mm acima da tela); microfones por baixo.
- O tilt fica DENTRO da cabeça: um garfo pequeno no topo do tubo do pescoço abraça o eixo do servo de tilt; o tubo
  entra por um rasgo no fundo da cabeça (invisível de frente e de 3/4). De fora só se vê o pescoço estreito.
- Pescoço: engrenagem de 22 dentes + tubo com flange cônica + garfo, apertados por 3 tirantes M3x45 que entram por
  baixo (as camadas do tubo trabalham em compressão). A flange (por cima) e a engrenagem (por baixo) abraçam a tampa.

Tudo em mm, na posição de montagem. As funções recebem um namespace de parâmetros (comum/cad/parametros.py › CUBO, CUBO_RODAS).
"""
from __future__ import annotations

from types import SimpleNamespace as NS

import numpy as np

from cad import parametros as P
from cad.comum import componentes as C
from cad.comum.geo import caixa, casco, cil, engrenagem, prisma, ressalto_nervurado, ret_arredondado, secao, uniao
from cad.comum.modelo import Comp, Peca, rot

F = P.FOLGA
S9 = P.MG996R
PINO_TILT = (5.4, 4.4)      # pino do tilt M5: furo passante na lateral do quadro, piloto no braço do garfo (rosca no plástico)


# ------------------------------------------------------------------ utilitários
def furo(p, d, comp, diam, seg=24):
    p = np.asarray(p, float)
    d = np.asarray(d, float)
    return cil(p, p + d / np.linalg.norm(d) * comp, diam / 2, seg=seg)


def inserto(p, d, prof=None):
    """Furo para inserto M3 a quente, entrando em p na direção d."""
    return furo(np.asarray(p, float) - np.asarray(d, float) * 0.01, d, prof or F.inserto_prof, F.inserto_d)


def gota(p, d, comp, diam, cima):
    """Furo horizontal em GOTA: cilindro + telhado a 45° apontado para `cima` (o lado que fica para cima na impressão).
    Imprime sem suporte em qualquer diâmetro."""
    p = np.asarray(p, float)
    d = np.asarray(d, float) / np.linalg.norm(d)
    c = np.asarray(cima, float) / np.linalg.norm(cima)
    r = diam / 2
    lado = np.cross(d, c)
    a = cil(p, p + d * comp, r, seg=32)
    k = r / np.sqrt(2.0)
    pts = [p + lado * k + c * k, p - lado * k + c * k, p + c * (r * np.sqrt(2.0))]
    cunha = casco(*[cil(q, q + d * comp, 0.02, seg=8) for q in pts])
    return a + cunha


def prato(perfil_de, z0, z1, chanfro_baixo=0.0, chanfro_cima=0.0):
    """Sólido CONVEXO extrudado em Z a partir de `perfil_de(recuo)` (seção com as bordas recuadas `recuo` mm), com
    chanfro de 45° na aresta de baixo e/ou de cima."""
    fatias = []
    if chanfro_baixo > 0:
        fatias.append(secao(perfil_de(chanfro_baixo), "z", z0, z0 + 0.01))
    fatias.append(secao(perfil_de(0.0), "z", z0 + chanfro_baixo, z1 - chanfro_cima))
    if chanfro_cima > 0:
        fatias.append(secao(perfil_de(chanfro_cima), "z", z1 - 0.01, z1))
    return casco(*fatias) if len(fatias) > 1 else fatias[0]


def nervura(p, ao_longo, para, cateto, esp=2.4):
    """Mão-francesa triangular (45°): nasce em p, corre `cateto` na direção `ao_longo` (parede) e `cateto` na direção
    `para` (peça reforçada). Espessura centrada em p."""
    p = np.asarray(p, float)
    a = np.asarray(ao_longo, float) / np.linalg.norm(ao_longo)
    b = np.asarray(para, float) / np.linalg.norm(para)
    n = np.cross(a, b)
    pts = [p, p + a * cateto, p + b * cateto]
    return casco(*[cil(q - n * esp / 2, q + n * esp / 2, 0.02, seg=8) for q in pts])


def T_(m, pos):
    return m.translate(list(pos))


# ------------------------------------------------------------------ cabeça
def cabeca(K, tela, pos, nome_tela="tela 3,5 pol.", lidar=None):
    """Cabeça-cubo completa. Referencial LOCAL: origem no cruzamento do eixo do pan com o eixo do tilt; X = lados,
    +Y = frente (rosto), Z = cima. `pos` = (x, y, z) desse ponto no robô. `K` = parâmetros da cabeça (CUBO.cab).
    Devolve NS(pecas, comps, garfo (Peca do grupo 'pan'), bancada (passos de `ordem` da montagem na bancada),
    nomes (tudo o que gira com a cabeça), fundo_z, tubo_topo_z, massa_aprox)."""
    Wc = K.larg
    yb, yf = K.y
    zb, zt = K.z
    pc, r = K.parede, K.raio
    Hc, zc = zt - zb, (zb + zt) / 2

    def sec(d=0.0):
        return ret_arredondado(Wc - 2 * d, Hc - 2 * d, max(r - d, 0.6)).translate([0, zc])

    # ---------------- copo (cabeca-corpo): 5 lados, imprime com as costas na mesa
    ct, rf = K.chanfro_tras, K.raio_frente
    fatias = [secao(sec(ct), "y", yb, yb + 0.01), secao(sec(0), "y", yb + ct, yf - rf)]
    for a in np.radians([22.5, 45.0, 67.5, 90.0]):
        y = yf - rf + rf * np.sin(a)
        fatias.append(secao(sec(rf * (1 - np.cos(a))), "y", y - 0.01, y))
    corpo = casco(*fatias) - secao(sec(pc), "y", yb + pc, yf + 1)
    xi, zi0, zi1 = Wc / 2 - pc, zb + pc, zt - pc          # faces internas

    # ---------------- cotas ao longo de Y (da frente para trás)
    yp1 = yf - K.painel_recuo                 # face da frente do painel (1 mm para dentro: fresta de sombra)
    yp0 = yp1 - K.painel_esp                  # face de trás do painel
    yg = yp0 - 0.2                            # vidro da tela
    zs = K.zs
    aw, ah = tela.ativa
    gpio = hasattr(tela, "acima_do_pi")       # tela de 3,5" espetada no GPIO do Pi; senão, tela HDMI presa no painel
    if gpio:
        y_pi = yg - tela.acima_do_pi - P.PI.esp
    else:
        y_pi = yg - tela.esp_conjunto - K.vao_tela_pi - P.PI.altura_pilha - P.PI.esp
    yt1 = y_pi - K.espacador                  # face da frente da travessa do quadro
    yt0 = yt1 - K.travessa_esp
    yq = yb + pc + 0.3                        # fim (atrás) das laterais do quadro

    # ---------------- painel do rosto (cabeca-face): placa escura + 4 pilares + postes da câmera
    face = secao(sec(pc + F.encaixe), "y", yp0, yp1)
    face = face - caixa(-aw / 2 - 0.5, aw / 2 + 0.5, yp0 - 1, yp1 + 1, zs - ah / 2 - 0.5, zs + ah / 2 + 0.5)
    zcam = K.zcam
    face = face - furo((0, yp0 - 1, zcam), (0, 1, 0), K.painel_esp + 2, 8.0)
    y_cam = yp0 - P.CAMERA.lente_alt - 0.3                 # face de trás da placa da câmera
    cfx, cfz = P.CAMERA.furos
    for sx in (1, -1):
        for sz in (1, -1):
            pf = (sx * cfx / 2, y_cam + 1.2, zcam + sz * cfz / 2)
            face = face + cil(pf, (pf[0], yp0 + 0.01, pf[2]), 2.4, seg=16)
    for sx in (1, -1):
        for sz in (1, -1):
            face = face - furo((sx * cfx / 2, y_cam + 1.19, zcam + sz * cfz / 2), (0, 1, 0), 6.0, F.m2_piloto)
    pil = [(sx * K.pilar_x, zs + sz * K.pilar_dz) for sx in (1, -1) for sz in (1, -1)]
    for (px, pz) in pil:
        face = face + ressalto_nervurado((px, yt1 + 0.01, pz), (0, 1, 0), yp0 - yt1, d_ext=10.0, angulos=[90, 270], nervura_alt=9.0)
    for (px, pz) in pil:
        face = face - inserto((px, yt1 + 0.01, pz), (0, 1, 0))
    pos_tela = []
    if not gpio:                                          # tela HDMI: 4 pilares com furo piloto M2,5 no padrão da placa
        fx_, fz_ = tela.furos
        y_pcb = yg - tela.esp_conjunto + tela.pcb_esp       # face da frente da placa da tela
        pos_tela = [(sx * fx_ / 2, zs + sz * fz_ / 2) for sx in (1, -1) for sz in (1, -1)]
        for (px, pz) in pos_tela:
            face = face + cil((px, y_pcb, pz), (px, yp0 + 0.01, pz), 3.2, seg=20)
        for (px, pz) in pos_tela:
            face = face - furo((px, y_pcb - 0.01, pz), (0, 1, 0), 7.0, F.m25_piloto)

    t_baixo_ = np.radians(-K.tilt[0])
    by_ = K.bloco_y / 2
    # ---------------- quadro (quadro-cabeca): travessa + 2 laterais; imprime com a frente da travessa na mesa
    xq = xi - 0.6
    hx = K.horn_x                                 # face do braço do garfo que recebe o horn do servo de tilt
    x_aba = hx + S9.aba_ate_topo_horn             # face de apoio da aba do servo (o eixo aponta para -X)
    ld0, ld1 = x_aba, x_aba + K.lateral_esp       # lateral direita (segura o servo)
    le1 = -K.braco_x - 0.6                        # lateral esquerda (mancal do pino do tilt): face de dentro
    le0 = le1 - K.lateral_esp
    zq0, zq1 = zs - tela.placa[1] / 2 - 1.7, zs + tela.placa[1] / 2 + 2.2
    trav = caixa(-xq, xq, yt0, yt1, zq0, zq1)
    # a travessa (que vai na mesa) cobre o pé das duas laterais e das colunas: nada nasce no ar
    trav_pes = lambda: caixa(ld0 - 3.0, min(xq, ld1 + 7.0), yt0, yt1, max(zd0 - 2.0, zi0 + 0.6), zd1 + 2.0) + \
        caixa(max(-xq, le0 - 7.0), le1 + 1.0, yt0, yt1, K.lat_e_z[0] - 1.0, K.lat_e_z[1] + 1.0)
    jl, jw = S9.janela
    zcs = -S9.eixo_da_ponta + S9.corpo[0] / 2     # centro do corpo do servo (em pé: 31 para cima, 10 para baixo do eixo)
    zd0, zd1 = zcs - S9.comp_abas / 2 - 3.0, zcs + S9.comp_abas / 2 + 3.5
    lat_d = caixa(ld0, ld1, yq, yt0 + 0.01, zd0, zd1)
    lat_d = lat_d - caixa(ld0 - 1, ld1 + 1, yq - 1, jw / 2, zcs - jl / 2, zcs + jl / 2)        # rasgo em U aberto para trás: o servo entra por trás
    lat_e = caixa(le0, le1, yq, yt0 + 0.01, K.lat_e_z[0], K.lat_e_z[1])
    col_d = [(ld1 + 1.5, zcs - jl / 2 - 5.6), (ld1 + 1.5, zcs + jl / 2 + 5.6)]                 # colunas dos insertos de trás
    col_e = [(le0 - 1.5, K.lat_e_z[0] + 21.0), (le0 - 1.5, K.lat_e_z[1] - 6.0)]
    quadro = uniao(trav, trav_pes(), lat_d, lat_e, *[cil((cx_, yq, cz_), (cx_, yt0 + 0.01, cz_), 5.0, seg=32) for (cx_, cz_) in col_d + col_e])
    quadro = quadro ^ secao(sec(pc + 0.6), "y", yq - 1, yt1 + 1)                               # cabe nos cantos arredondados do copo
    quadro = quadro - caixa(ld1 - 0.01, xq + 1, yq - 1, jw / 2, zcs - jl / 2, zcs + jl / 2)    # as colunas não invadem o corpo do servo
    for sy in (1, -1):
        for sz in (1, -1):                                                                 # 4 furos piloto das abas do servo
            quadro = quadro - furo((ld0 - 0.01, sy * S9.furos_aba[1] / 2, zcs + sz * S9.furos_aba[0] / 2), (1, 0, 0), K.lateral_esp + 5.0, F.m3_piloto)
    quadro = quadro - furo((le0 - 1, 0, 0), (1, 0, 0), K.lateral_esp + 2, PINO_TILT[0])        # pino do tilt (M5 que gira no furo)
    for sy in (1, -1):                                                                     # passagem da chave até os 2 parafusos de CIMA da aba do servo
        quadro = quadro - furo((le0 - 7, sy * S9.furos_aba[1] / 2, zcs + S9.furos_aba[0] / 2), (1, 0, 0), K.lateral_esp + 8, 5.0)
    for (cx_, cz_) in col_d + col_e:
        quadro = quadro - inserto((cx_, yq, cz_), (0, 1, 0))
        corpo = corpo - furo((cx_, yb - 1, cz_), (0, 1, 0), pc + 2, F.m3_passante)
    for (px, pz) in pil:
        quadro = quadro - furo((px, yt0 - 1, pz), (0, 1, 0), K.travessa_esp + 2, F.m3_passante)
    pos_pi = [(-P.PI.placa[0] / 2 + x, zs + P.PI.placa[1] / 2 - y) for (x, y) in P.PI.furos]
    for (px, pz) in pos_pi:
        quadro = quadro - furo((px, yt0 - 1, pz), (0, 1, 0), K.travessa_esp + 2, 2.9)
    quadro = quadro - caixa(-22, 14, yt0 - 1, yt1 + 1, zs - 16, zs + 12)                       # passagem de cabos atrás do Pi
    # com a cabeça baixa, a quina de baixo da travessa varre o bloco do garfo: recorte nessa faixa de X
    z_rec = (by_ + 1.5 - yt0 * np.cos(t_baixo_)) / np.sin(t_baixo_)
    if z_rec > zq0:
        quadro = quadro - caixa(-K.braco_x - 0.3, hx + 3.0 + 1.5, yt0 - 1, yt1 + 1, zq0 - 1, z_rec)
    # mãos-francesas das laterais (45°, nascem na travessa)
    quadro = quadro + nervura((le0 + 0.01, yt0, K.lat_e_z[1] - 16), (0, -1, 0), (-1, 0, 0), 9.0) + nervura((le0 + 0.01, yt0, K.lat_e_z[0] + 4), (0, -1, 0), (-1, 0, 0), 9.0)
    esp_pi = cil((0, 0, 0), (0, 0, K.espacador), 3.0, seg=24) - cil((0, 0, -1), (0, 0, K.espacador + 1), 1.5, seg=16)
    mats_esp = [C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (px + pos[0], yt1 + pos[1], pz + pos[2])) for (px, pz) in pos_pi]

    # ---------------- garfo interno (gira com o pescoço): bloco + 2 braços; imprime deitado (costas na mesa)
    gy = K.garfo_y / 2
    zg0, zg1 = K.garfo_z                          # fundo (assenta no tubo) e topo do bloco
    bx = K.braco_x
    bloco = caixa(-bx, hx + 3.0, -by_, by_, zg0, zg1)
    zt_b, cb = gy * 0.95, gy * 0.62                # topo dos braços: chanfros de 45° (o de trás encosta na mesa na impressão)
    perfil_b = [(-gy, zg1 - 0.01), (gy, zg1 - 0.01), (gy, zt_b - cb), (gy - cb, zt_b), (-gy + cb, zt_b), (-gy, zt_b - cb)]
    br_d = prisma(perfil_b, "x", hx - K.braco_esp, hx)
    br_e = prisma(perfil_b, "x", -bx, -bx + K.braco_esp_e)
    garfo = uniao(bloco, br_d, br_e)
    garfo = garfo - gota((hx - K.braco_esp - 1, 0, 0), (1, 0, 0), K.braco_esp + 2, 7.0, (0, 1, 0))
    for a in (45, 135, 225, 315):                                                             # parafusos do horn
        c, s_ = np.cos(np.radians(a)), np.sin(np.radians(a))
        garfo = garfo - casco(furo((hx - K.braco_esp - 1, 6.3 * c, 6.3 * s_), (1, 0, 0), K.braco_esp + 2, 2.2),
                              furo((hx - K.braco_esp - 1, 8.8 * c, 8.8 * s_), (1, 0, 0), K.braco_esp + 2, 2.2))
    # pino do tilt = M5 rosqueado direto no braço (piloto 4,4). Antes de pôr o pino, o furo é a passagem da chave até o
    # parafuso central do horn; os 4 furos em volta dão acesso aos 4 parafusos do horn (aperte com o garfo ainda solto)
    garfo = garfo - furo((-bx - 1, 0, 0), (1, 0, 0), K.braco_esp_e + 2, PINO_TILT[1])
    for a in (45, 135, 225, 315):
        garfo = garfo - furo((-bx - 1, 7.5 * np.cos(np.radians(a)), 7.5 * np.sin(np.radians(a))), (1, 0, 0), K.braco_esp_e + 2, 4.2)
    garfo = garfo - gota((0, 0, zg0 - 1), (0, 0, 1), zg1 - zg0 + 2, K.furo_cabos, (0, 1, 0))  # cabos sobem pelo meio
    pos_tir = [(K.tirante_r * np.cos(np.radians(a)), K.tirante_r * np.sin(np.radians(a))) for a in K.tirante_ang]
    for (px, py) in pos_tir:
        garfo = garfo - inserto((px, py, zg0), (0, 0, 1)) - furo((px, py, zg0), (0, 0, 1), zg1 - zg0 - 2.0, F.m3_passante)

    # ---------------- copo: rasgo do pescoço (em gota para a frente = para cima na impressão), microfones, fase 2
    rt = K.tubo_d / 2 + 1.5
    t_cima, t_baixo = np.radians(K.tilt[1]), np.radians(-K.tilt[0])
    # o tubo é um cilindro inclinado em relação à cabeça: na parede do fundo a seção é uma elipse (rt / cos)
    ys0 = zb * np.tan(t_cima) - rt / np.cos(t_cima)     # cabeça para cima → o tubo vai para trás (zb é negativo)
    ys1 = -zb * np.tan(t_baixo) + rt / np.cos(t_baixo) * np.sqrt(2.0)
    pts = [(rt * np.cos(a), ys0 + rt + rt * np.sin(a)) for a in np.linspace(np.pi, 2 * np.pi, 17)] + [(rt, ys1 - rt), (0.0, ys1), (-rt, ys1 - rt)]
    corpo = corpo - prisma(pts, "z", zb - 1, zb + pc + 1)
    for sx in (1, -1):                                                                        # microfones (fase 2): por baixo
        corpo = corpo - furo((sx * K.mic_x, yf - 12.0, zb - 1), (0, 0, 1), pc + 2, 2.0)
    comps_extra = []
    if lidar is not None and "comp" in lidar:
        comps_extra.append(Comp(lidar["comp"], T_(lidar["solido"].translate([lidar["xy"][0], lidar["xy"][1], zt]), pos), "cabeca", lidar["massa"], "preto", fase2=True))
    if lidar is not None:
        # trilho por dentro do teto (vertical na impressão) com furos CEGOS: por fora não aparece nada. Na fase 2,
        # fura-se a pele de 0,8 mm por dentro com o próprio parafuso.
        for (lx, ly) in lidar["furos"]:
            corpo = corpo + caixa(lx - 4.0, lx + 4.0, yb + pc - 0.01, ly + 5.0, zi1 - 3.2, zi1 + 0.01)
        for (lx, ly) in lidar["furos"]:
            corpo = corpo - furo((lx, ly, zi1 - 3.3), (0, 0, 1), 3.2 + pc - 0.8 + 0.1, lidar["piloto"])
        if "cabo" in lidar:                                # passagem do cabo: rebaixo cego Ø8 por dentro (pele de 0,8 mm a romper)
            corpo = corpo - furo((lidar["cabo"][0], lidar["cabo"][1], zi1 - 0.01), (0, 0, 1), pc - 0.8, 8.0)

    # ---------------- peças
    def T(m):
        return m.translate(list(pos))

    pecas = [
        Peca("quadro-cabeca", T(quadro), material="PETG", cor="amarelo", grupo="cabeca", macica=True, imprimir=rot("x", -90), explode=(0, -20, 140),
             perimetros=4, infill=30, orientacao="frente da travessa na mesa, laterais para cima",
             reforco="laterais inteiras até o fundo com colunas Ø10 nos 4 insertos e mãos-francesas a 45° na travessa; servo de tilt em rasgo em U (sem ponte), 4 parafusos",
             obs="esqueleto da cabeça: Raspberry Pi (4 M2,5), servo de tilt, mancal do pino; recebe o painel (4 M3 por trás) e o copo (4 M3 pela parede de trás)"),
        Peca("cabeca-corpo", T(corpo), cor="branco", grupo="cabeca", imprimir=rot("x", 90), suporte="não", explode=(0, -110, 140),
             perimetros=3, infill=15, orientacao="costas na mesa, boca (frente) para cima, como um copo",
             reforco="arestas compridas com raio de %.0f mm (verticais na impressão) e chanfro de 45° na aresta de trás; rasgo do pescoço em gota; sem ponte nem teto" % r,
             obs="casca da cabeça (5 lados); entra por trás, 4 M3 na parede de trás; rasgo do pescoço e furos de microfone por baixo"),
        Peca("cabeca-face", T(face), cor="preto", grupo="cabeca", imprimir=rot("x", -90), explode=(0, 90, 140),
             perimetros=3, infill=20, orientacao="face da frente (a que aparece) na mesa, pilares para cima",
             reforco="4 pilares Ø10 com 2 nervuras a 45° cada (insertos M3 na ponta); postes da câmera",
             obs="painel escuro do rosto: janela da tela, furo de 8 mm da câmera acima dela; nenhum parafuso na frente"),
        Peca("espacador-pi", esp_pi, cor="cinza", grupo="cabeca", macica=True, copias=mats_esp, explode=(0, 30, 140),
             orientacao="em pé", obs="4 espaçadores de %.0f mm do Raspberry Pi" % K.espacador),
    ]
    garfo_p = Peca("garfo", T(garfo), material="PETG", cor="grafite", grupo="pan", macica=True, imprimir=rot("x", 90), explode=(0, 0, 70),
                   perimetros=5, infill=40, orientacao="deitado, costas na mesa: as camadas correm do bloco para os braços",
                   reforco="camadas ao longo dos braços (flexão); bloco maciço com 3 insertos dos tirantes; furos em gota",
                   obs="garfo interno do tilt: fica dentro da cabeça, no topo do tubo; horn do servo num braço, pino M5 (rosca no plástico) no outro; furos de passagem da chave no braço esquerdo")

    # ---------------- componentes
    M_tilt = C.M([(0, 0, 1), (0, 1, 0), (-1, 0, 0)], (x_aba, 0, 0))
    M_pi = C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (-P.PI.placa[0] / 2, y_pi, zs + P.PI.placa[1] / 2))   # USB à direita
    tw, th = tela.placa
    if gpio:
        tela_s = caixa(-tw / 2, tw / 2, yg - tela.esp_conjunto, yg, zs - th / 2, zs + th / 2)
    else:                                     # tela HDMI: placa com orelhas atrás + painel LCD (mais baixo) na frente
        lw, lh = tela.lcd
        tela_s = caixa(-tw / 2, tw / 2, yg - tela.esp_conjunto, yg - tela.esp_conjunto + tela.pcb_esp, zs - th / 2, zs + th / 2) + \
            caixa(-lw / 2, lw / 2, yg - tela.esp_conjunto + tela.pcb_esp - 0.01, yg, zs - lh / 2, zs + lh / 2)
    # o que a tela mostra (olhos e boca, como na referência): lâminas de 0,2 mm sobre o vidro, só para o render
    ex, er = aw * 0.21, ah * 0.11
    rosto = uniao(*[casco(cil((sx * ex, yg + 0.05, zs + ah * 0.10), (sx * ex, yg + 0.25, zs + ah * 0.10), er, seg=24),
                          cil((sx * ex, yg + 0.05, zs + ah * 0.16), (sx * ex, yg + 0.25, zs + ah * 0.16), er, seg=24)) for sx in (1, -1)],
                  caixa(-aw * 0.09, aw * 0.09, yg + 0.05, yg + 0.25, zs - ah * 0.20, zs - ah * 0.20 + er * 0.7))
    comps = [
        Comp("servo-tilt MG996R", T(C.servo_padrao().transform(M_tilt[:3, :])), "cabeca", S9.massa, "preto"),
        Comp("Raspberry Pi 4/5", T(C.placa_eletronica(P.PI).transform(M_pi[:3, :])), "cabeca", P.PI.massa, "verde"),
        Comp(nome_tela, T(tela_s), "cabeca", tela.massa, "preto"),
        Comp("rosto-na-tela (imagem, não é peça)", T(rosto), "cabeca", 0.0, "ciano"),
        Comp("camera (fase 2)", T(C.camera().translate([0, y_cam, zcam])), "cabeca", 4.0, "preto", fase2=True),
    ] + comps_extra
    n_tela = nome_tela
    miolo = ["quadro-cabeca", "Raspberry Pi 4/5", "espacador-pi", n_tela, "rosto-na-tela (imagem, não é peça)", "servo-tilt MG996R"]
    n_face = [n_tela, "rosto-na-tela (imagem, não é peça)", "cabeca-face", "camera (fase 2)"]
    bancada = [
        dict(passo="Raspberry Pi e espaçadores no quadro (bancada)", move=["Raspberry Pi 4/5", "espacador-pi"], dir=(0, 1, 0), curso=60, contra=["quadro-cabeca"]),
        dict(passo="tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada)", move=n_face, dir=(0, 1, 0), curso=80,
             contra=["quadro-cabeca", "Raspberry Pi 4/5", "espacador-pi"]),
        dict(passo="servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada)", move=["servo-tilt MG996R"], dir=(0, -1, 0), curso=80,
             contra=["quadro-cabeca", "Raspberry Pi 4/5", "espacador-pi"] + n_face),
        dict(passo="garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada)", move=["garfo"], dir=(0, 0, -1), curso=80,
             contra=["quadro-cabeca", "servo-tilt MG996R", "Raspberry Pi 4/5"] + n_face),
        dict(passo="copo da cabeça por trás; 4 M3 na parede de trás (bancada)", move=["cabeca-corpo"], dir=(0, -1, 0), curso=160,
             contra=miolo + ["cabeca-face", "camera (fase 2)", "garfo"]),
    ]
    nomes = miolo + ["cabeca-face", "camera (fase 2)", "cabeca-corpo"]
    return NS(pecas=pecas, comps=comps, garfo=garfo_p, bancada=bancada, nomes=nomes, pos_tir=pos_tir, zg0=zg0 + pos[2],
              fundo_z=zb + pos[2], topo_z=zt + pos[2], yt0=yt0, y_frente=yf, y_tras=yb, zi1=zi1)


# ------------------------------------------------------------------ pescoço
def pescoco(Q, K, pan_xy, z_tampa, z_garfo, pos_tir, ang_servo):
    """Tubo oco com flange cônica + engrenagem do pescoço (22 dentes), no eixo `pan_xy`.
    z_tampa = (face de baixo, face de cima) da tampa que o pescoço atravessa; z_garfo = fundo do garfo (topo do tubo).
    Devolve (Peca tubo, Peca engrenagem, sólido do furo da tampa)."""
    ax, ay = pan_xy
    z1, z2 = Q.dentes
    ez0, ez1 = Q.eng_z
    rt, rc = K.tubo_d / 2, K.furo_cabos / 2
    rfl, hfl = Q.flange
    zt0, zt1 = z_tampa
    tubo = cil((ax, ay, ez1), (ax, ay, z_garfo), rt)
    tubo = tubo + cil((ax, ay, zt1), (ax, ay, zt1 + hfl), rfl) + cil((ax, ay, zt1 + hfl), (ax, ay, zt1 + hfl + (rfl - rt)), rfl, rt)   # flange + cone a 45°
    eng = engrenagem(z1, Q.modulo, ez0, ez1, folga=Q.eng_folga, fase=np.radians(ang_servo)).translate([ax, ay, 0])
    oco = cil((ax, ay, ez0 - 1), (ax, ay, z_garfo + 1), rc, seg=32)
    tubo, eng = tubo - oco, eng - oco
    for (px, py) in pos_tir:
        f = furo((ax + px, ay + py, ez0 - 1), (0, 0, 1), z_garfo - ez0 + 2, F.m3_passante)
        tubo, eng = tubo - f, eng - f
    furo_tampa = cil((ax, ay, zt0 - 1), (ax, ay, zt1 + 1), rt + F.deslizante / 2 + 0.05)
    comp = z_garfo - ez0 + F.inserto_prof - 1.0
    p_tubo = Peca("tubo-pescoco", tubo, material="PETG", cor="prata", grupo="pan", macica=True, imprimir=rot("x", 180), explode=(0, 0, 45),
                  perimetros=5, infill=40, orientacao="de cabeça para baixo: o topo (lado do garfo) na mesa, a flange cônica abre a 45°",
                  reforco="3 tirantes M3 de aço atravessam o tubo inteiro: as camadas trabalham só em compressão; flange cônica a 45°",
                  obs="pescoço oco (cabos por dentro); 3 M3x%d entram por baixo, pela engrenagem, e rosqueiam nos insertos do garfo" % (5 * round(comp / 5)))
    p_eng = Peca("engrenagem-pescoco", eng, material="PETG", cor="prata", grupo="pan", macica=True, explode=(0, 0, 20),
                 perimetros=5, infill=60, orientacao="deitada", reforco="dentes módulo %.1f com 5 perímetros (dente quase maciço); presa pelos 3 tirantes" % Q.modulo,
                 obs="%d dentes; fica por baixo da tampa e, com a flange do tubo por cima, impede o pescoço de bambear" % z1)
    return p_tubo, p_eng, furo_tampa


def servo_pan(Q, pan_xy, ang_servo, ang_corpo, z_piso):
    """Suporte do servo de pan sobre um piso em z=z_piso: 2 postes com mãos-francesas + engrenagem de 44 dentes no horn.
    ang_servo = direção (graus, a partir de +X) do eixo do pan para o eixo do servo; ang_corpo = para onde aponta o
    corpo do servo. Devolve NS(soma, corte, eng (Peca), comp (Comp), xy)."""
    z1, z2 = Q.dentes
    m = Q.modulo
    dist = m * (z1 + z2) / 2
    a = np.radians(ang_servo)
    sx, sy = pan_xy[0] + dist * np.cos(a), pan_xy[1] + dist * np.sin(a)
    b = np.radians(ang_corpo)
    u = np.array([np.cos(b), np.sin(b), 0.0])            # ao longo do corpo
    v = np.array([-np.sin(b), np.cos(b), 0.0])
    za = z_piso + S9.base_ate_aba
    cc = -S9.eixo_da_ponta + S9.corpo[0] / 2
    o = np.array([sx, sy, 0.0])
    soma, corte = [], []
    for s in (1, -1):
        c = o + u * (cc + s * S9.furos_aba[0] / 2)
        pts = [c + u * dx + v * dy for dx in (-3.6, 3.6) for dy in (-10.0, 10.0)]
        soma.append(casco(*[cil((q[0], q[1], z_piso - 0.01), (q[0], q[1], za), 0.02, seg=8) for q in pts]))
        for sv in (1, -1):                                 # mão-francesa de cada lado do poste, para fora do corpo
            soma.append(nervura((c + u * s * 3.5 + v * sv * 6.0)[:2].tolist() + [z_piso], (0, 0, 1), u * s, min(12.0, S9.base_ate_aba - 4)))
            q = c + v * sv * S9.furos_aba[1] / 2
            corte.append(furo((q[0], q[1], za + 0.01), (0, 0, -1), 14, F.m3_piloto))
    ez0, ez1 = Q.eng_z
    assert abs(ez0 - (za + S9.aba_ate_topo_horn - S9.horn_esp)) < 0.6, "eng_z não bate com a altura do horn do servo de pan"
    eng = engrenagem(z2, m, ez0, ez1, folga=Q.eng_folga, fase=a + np.pi + np.pi / z2).translate([sx, sy, 0])
    z_horn = za + S9.aba_ate_topo_horn
    eng = eng - cil((sx, sy, ez0 - 1), (sx, sy, z_horn + 0.2), S9.horn_d / 2 + 0.3) - furo((sx, sy, 0), (0, 0, 1), 400, 6.0)
    for g in (0, 90, 180, 270):
        c, s_ = np.cos(np.radians(g)), np.sin(np.radians(g))
        eng = eng - casco(furo((sx + 5.5 * c, sy + 5.5 * s_, 0), (0, 0, 1), 400, 2.2), furo((sx + 9.0 * c, sy + 9.0 * s_, 0), (0, 0, 1), 400, 2.2))
    p_eng = Peca("engrenagem-servo", eng, material="PETG", cor="amarelo", grupo="eng", macica=True, imprimir=rot("x", 180), explode=(0, -60, 45),
                 perimetros=5, infill=60, orientacao="de cabeça para baixo: a face de cima na mesa, o rebaixo do horn para cima",
                 reforco="dentes módulo %.1f com 5 perímetros; 4 parafusos no horn redondo" % m,
                 obs="%d dentes, presa no horn redondo do servo de pan (o pescoço gira 2x o servo)" % z2)
    Mp = C.M([(u[0], u[1], 0), (v[0], v[1], 0), (0, 0, 1)], (sx, sy, za))
    comp = Comp("servo-pan MG996R", C.servo_padrao().transform(Mp[:3, :]), "corpo", S9.massa, "preto")
    return NS(soma=uniao(*soma), corte=uniao(*corte), eng=p_eng, comp=comp, xy=(sx, sy), za=za)


# ------------------------------------------------------------------ estabilidade (robô que roda)
def _centroide(m):
    me = m.to_mesh()
    v = np.asarray(me.vert_properties)[:, :3].astype(float)
    t = np.asarray(me.tri_verts)
    v0, v1, v2 = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    vt = np.einsum("ij,ij->i", v0, np.cross(v1, v2)) / 6.0
    return ((v0 + v1 + v2) / 4.0 * vt[:, None]).sum(axis=0) / vt.sum()


def _alcance(apoios, p, d):
    """Distância de p até a borda do polígono convexo de apoio andando na direção d (0 se p está fora)."""
    from scipy.spatial import ConvexHull

    h = ConvexHull(np.asarray(apoios, float))
    d = np.asarray(d, float) / np.linalg.norm(d)
    melhor = np.inf
    for (a, b, c) in h.equations:                      # a*x + b*y + c <= 0 dentro
        f = a * p[0] + b * p[1] + c
        if f > 0:
            return 0.0
        den = a * d[0] + b * d[1]
        if den > 1e-12:
            melhor = min(melhor, -f / den)
    return float(melhor)


def estabilidade(mod, g=9.81):
    """CG (mesma estimativa de massa do gerar.py), margem de tombamento e aceleração máxima sem tombar em cada pose:
    a = g * alcance / altura do CG, onde alcance = distância horizontal do CG até a borda do polígono de apoio NA
    DIREÇÃO da força de inércia. Frear andando para a frente joga o robô para a FRENTE (alcance até a linha das rodas);
    arrancar para a frente (ou frear de ré) joga para TRÁS (alcance até a bola); curva joga para o LADO.
    Devolve {pose: {...}} e o resumo do pior caso. Estimativa de corpo rígido: não conta folga, pneu nem piso inclinado."""
    from cad.gerar import estimar   # import tardio (gerar.py importa os modelos)

    itens = []
    for p in mod.pecas:
        _, massa, _ = estimar(p.solido, p)
        c0 = _centroide(p.solido)
        grupos = p.grupos or [p.grupo] * len(p.copias)
        for M, gr in zip(p.copias, grupos):
            itens.append((massa, (np.asarray(M) @ np.append(c0, 1.0))[:3], gr))
    for c in mod.comps:
        if c.massa > 0:
            itens.append((c.massa, _centroide(c.solido), c.grupo))
    res = {}
    for (nome, ang) in mod.poses:
        mt, soma = 0.0, np.zeros(3)
        for (m, c, gr) in itens:
            Mg = mod.matriz_grupo(gr, ang)
            soma += m * (Mg @ np.append(c, 1.0))[:3]
            mt += m
        cg = soma / mt
        al = {k: _alcance(mod.apoios, cg[:2], d) for k, d in (("frente", (0, 1)), ("tras", (0, -1)), ("esq", (-1, 0)), ("dir", (1, 0)))}
        res[nome] = {"cg": [round(float(v), 1) for v in cg], "massa_g": round(mt), "alcance_mm": {k: round(v, 1) for k, v in al.items()},
                     "a_max_m_s2": {k: round(g * v / cg[2], 2) for k, v in al.items()}}
    pior = {k: min(res[n]["a_max_m_s2"][k] for n in res) for k in ("frente", "tras", "esq", "dir")}
    return res, pior
