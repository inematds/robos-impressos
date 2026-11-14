"""Esqueleto comum dos bichos que rodam: chassi (piso + rack + deck), bandejas das placas,
garfo e berço do pescoço (pan + tilt) e as peças pequenas iguais em todos os modelos.

Tudo na posição de montagem. Medidas em cad/parametros.py (BASE, PESCOCO, FOLGA, componentes).
"""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import componentes as C
from cad.comum.geo import caixa, casco, cil, esfera, espelho_x, prisma, uniao
from cad.comum.modelo import Comp, Junta, Peca, rot

B, F, N = P.BASE, P.FOLGA, P.PESCOCO
CX, CY, CZ = N.centro                      # centro da junta do pescoço
X0, X1 = B.parede_x0, B.parede_x0 + B.parede_esp
Z0, Z1 = B.piso_z


def sim(m):
    return m + espelho_x(m)


def furo(p, d, comp, diam):
    """Furo cilíndrico a partir de p na direção d."""
    p = np.asarray(p, float)
    d = np.asarray(d, float)
    return cil(p, p + d / np.linalg.norm(d) * comp, diam / 2, seg=24)


def inserto(p, d):
    """Furo para inserto M3 a quente, entrando em p na direção d."""
    return furo(np.asarray(p, float) - np.asarray(d, float) * 0.01, d, F.inserto_prof, F.inserto_d)


def rasgo(p0, p1, d, eixo, comp):
    """Rasgo oblongo de p0 a p1 (centros), diâmetro d, atravessando `comp` na direção `eixo`."""
    a = furo(p0, eixo, comp, d)
    b = furo(p1, eixo, comp, d)
    return casco(a, b)


def universal_z(x, y, z0, z1, ao_longo="x"):
    """Ponto universal: par de furos M3 passantes a 20 mm (suporte de sensor da fase 2)."""
    h = P.UNIVERSAL.passo / 2
    d = (h, 0) if ao_longo == "x" else (0, h)
    return furo((x - d[0], y - d[1], z0 - 0.5), (0, 0, 1), z1 - z0 + 1, F.m3_passante) + \
        furo((x + d[0], y + d[1], z0 - 0.5), (0, 0, 1), z1 - z0 + 1, F.m3_passante)


# posição dos servos (matrizes local -> montagem)
def M_pan():
    # eixo local z -> +Z; corpo (x local) para a frente (+Y)
    return C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (0, B.pescoco_y, B.deck_z))


def M_braco(lado):
    # eixo local z -> ±X (para fora); corpo (x local) para baixo
    y, z = B.ombro
    return C.M([(0, 0, -1), (0, lado, 0), (lado, 0, 0)], (lado * X1, y, z))


def M_tilt():
    # servo padrão em pé: eixo local z -> +X; corpo (x local) para cima (+Z); face de apoio da aba em X_ABA_TILT
    return C.M([(0, 0, 1), (0, -1, 0), (1, 0, 0)], (X_ABA_TILT, CY, CZ))


def M_motor(lado):
    # caixa encostada na face de fora da parede; motor para cima
    return C.M([(lado, 0, 0), (0, lado, 0), (0, 0, 1)], (lado * X1, 0, B.eixo_roda_z))


X_ABA_TILT = N.garfo_x - P.MG996R.aba_ate_topo_horn   # face de apoio da aba do servo de tilt (horn encostado no montante direito)
X_RODA = X1 + P.TT.caixa[2] + P.RODA.folga_caixa    # face interna da roda


# ------------------------------------------------------------------ chassi
def piso_solido(folga=0.0, z0=None, z1=None):
    """Piso do chassi (placa + faixas + asas + lança + pá). Com `folga` vira o envelope que as cascas contornam."""
    z0 = Z0 if z0 is None else z0
    z1 = Z1 if z1 is None else z1
    f = folga
    yf = B.piso_y[1]
    piso = prisma([(-B.piso_x - f, B.piso_y[0] - f), (B.piso_x + f, B.piso_y[0] - f), (B.piso_x + f, yf - 18 + f * 0.5), (24 + f * 0.5, yf + f),
                   (-24 - f * 0.5, yf + f), (-B.piso_x - f, yf - 18 + f * 0.5)], "z", z0, z1)
    ax0, ax1 = B.asa_x
    ay0, ay1 = B.asa_y
    lado = uniao(caixa(B.faixa_x[0] - f, B.faixa_x[1] + f, -ay1 - f, ay1 + f, z0, z1),
                 caixa(ax0 - f, ax1 + f, ay0 - f, ay1 + f, z0, z1), caixa(ax0 - f, ax1 + f, -ay1 - f, -ay0 + f, z0, z1))
    lanca = caixa(-B.lanca_x - f, B.lanca_x + f, B.lanca_y_fim - f, B.piso_y[0] + 1, z0, z1)
    pa = caixa(-B.pa_x - f, B.pa_x + f, B.pa_y[0] - f, B.pa_y[1] + f, z0, z1) + caixa(-B.pa_x - f, B.pa_x + f, B.pa_frente_y[0] - f, B.pa_frente_y[1] + f, z0, z1)
    return uniao(piso, sim(lado), lanca, pa)


def chassi() -> Peca:
    placa = piso_solido()
    py0, py1 = B.parede_y
    parede = caixa(X0, X1, py0, B.travessa_y[1], Z1 - 0.01, B.deck_z) + caixa(X0, X1, B.travessa_y[1] - 0.01, py1, Z1 - 0.01, B.lobo_motor_z) \
        + prisma([(B.travessa_y[1] - 0.01, B.lobo_motor_z - 0.01), (py1, B.lobo_motor_z - 0.01), (B.travessa_y[1] - 0.01, B.lobo_motor_z + (py1 - B.travessa_y[1]))], "x", X0, X1)
    orelha = caixa(X0, X1, B.ombro[0] - 12, B.ombro[0] + 12, B.deck_z - 0.01, B.orelha_ombro_z)
    # deck (apoia o servo de pan) + mísulas a 45° para imprimir sem suporte
    dz0 = B.deck_z - B.deck_esp
    deck = caixa(-X0 - 0.01, X0 + 0.01, py0, B.deck_y1, dz0, B.deck_z)
    misula = prisma([(X0 + 0.01, dz0 - 12), (X0 + 0.01, dz0 + 0.01), (X0 - 12, dz0 + 0.01)], "y", py0, B.ombro[0] - 7.5)
    travessa = caixa(-X0 - 0.01, X0 + 0.01, B.travessa_y[0], B.travessa_y[1], B.travessa_z[0], dz0 + 0.01) \
        - caixa(-B.travessa_recorte[0], B.travessa_recorte[0], B.travessa_y[0] - 1, B.travessa_y[1] + 1, B.travessa_recorte[1], dz0 + 1)
    # esfera de apoio: ressalto com soquete
    ey = B.esfera_y
    ressalto = cil((0, ey, Z0), (0, ey, Z0 + 10.5), 14.5)
    # batente da frente da bateria (atrás ela fica livre para sair; prenda com fita dupla-face ou velcro)
    by = B.bateria_y
    Lb = P.BATERIA.cx[0]
    bat_f = caixa(-12, 12, by + Lb / 2 + 0.6, by + Lb / 2 + 2.6, Z1 - 0.01, Z1 + 6)

    # ressalto traseiro do deck (parafuso do alto do torso-costas) e 2 postes da frente (parafusos do torso-frente)
    zr = B.deck_z - B.deck_esp / 2
    res_t = caixa(-5, 5, py0 - 6, py0 + 0.01, zr - 4.5, zr + 4.5) + prisma([(py0 - 6, zr - 4.3), (py0 + 0.01, zr - 4.3), (py0 + 0.01, zr - 10.5)], "x", -4.9, 4.9)
    ty1 = B.travessa_y[1]
    postes = []
    for (px, pz, pyt) in B.postes_frente:
        postes.append(cil((px, ty1 - 0.01, pz), (px, pyt, pz), 4.6) + prisma([(ty1 - 0.01, pz - 4.0), (pyt, pz - 4.0), (ty1 - 0.01, pz - 4.0 - (pyt - ty1))], "x", px - 1.6, px + 1.6))
    poste = uniao(*postes)

    corpo = uniao(placa, sim(parede), sim(orelha), deck, sim(misula), travessa, ressalto, bat_f, res_t, sim(poste))

    cortes = []
    # --- paredes: motor TT (eixo interno, rasgos dos 2 furos de trás, furo da orelha)
    ez = B.eixo_roda_z
    t = P.TT
    d0, d1 = 12.3 / 2 - 0.4, t.furos_tras_dist / 2 + 0.4
    for s in (1, -1):
        cortes.append(furo((s * (X0 - 1), 0, ez), (s, 0, 0), B.parede_esp + 2, t.eixo_d + 3.0))
        for sy in (1, -1):
            cortes.append(rasgo((s * (X0 - 1), sy * d0, ez + t.furos_tras), (s * (X0 - 1), sy * d1, ez + t.furos_tras),
                                F.m3_passante, (s, 0, 0), B.parede_esp + 2))
        cortes.append(rasgo((s * (X0 - 1), 0, ez - t.furo_orelha - 1.2), (s * (X0 - 1), 0, ez - t.furo_orelha + 1.2),
                            F.m3_passante, (s, 0, 0), B.parede_esp + 2))
        # trilhos das bandejas
        for tz in B.trilho_z:
            cortes.append(caixa(X0 - 0.1, X0 + B.trilho_prof, py0 - 1, B.trilho_y_fim, tz, tz + B.trilho_alt) if s > 0 else
                          caixa(-X0 - B.trilho_prof, -X0 + 0.1, py0 - 1, B.trilho_y_fim, tz, tz + B.trilho_alt))
        # janela do servo do braço (SG90/MG90S) + furos piloto das abas
        oy, oz = B.ombro
        jl, jw = P.MICRO.janela
        zc = oz + P.MICRO.eixo_da_ponta - P.MICRO.corpo[0] / 2       # centro do corpo
        cortes.append(caixa(min(s * (X0 - 1), s * (X1 + 1)), max(s * (X0 - 1), s * (X1 + 1)), oy - jw / 2, oy + jw / 2, zc - jl / 2, zc + jl / 2))
        for dz in (-P.MICRO.furos_aba / 2, P.MICRO.furos_aba / 2):
            cortes.append(furo((s * (X1 + 0.5), oy, zc + dz), (-s, 0, 0), B.parede_esp + 1, F.m2_piloto))
        # passagens de cabo
        for (cy_, cz_) in ((B.pescoco_y - 23.0, 58.0), (B.pescoco_y - 23.0, 110.0)):
            cortes.append(furo((s * (X0 - 1), cy_, cz_), (s, 0, 0), B.parede_esp + 2, 10.0))
    # trava das bandejas (parede direita)
    for tz in B.trilho_z:
        cortes.append(furo((X0 - 1, B.trava_y, tz + 0.3 - 4.1), (1, 0, 0), B.parede_esp + 2, F.m3_passante))
    # --- deck: janela do servo de pan, rasgos das abas, passagem de cabos, recorte dos servos dos braços, ponto do IMU
    s9 = P.MG996R
    jy0 = B.pescoco_y - s9.eixo_da_ponta - (s9.janela[0] - s9.corpo[0]) / 2
    cortes.append(caixa(-s9.janela[1] / 2, s9.janela[1] / 2, jy0, jy0 + s9.janela[0], dz0 - 1, B.deck_z + 1))
    ycs = B.pescoco_y - s9.eixo_da_ponta + s9.corpo[0] / 2
    for sx in (1, -1):
        for sy in (1, -1):
            yy = ycs + sy * s9.furos_aba[0] / 2
            cortes.append(rasgo((sx * s9.furos_aba[1] / 2, yy - 1.5, dz0 - 12), (sx * s9.furos_aba[1] / 2, yy + 1.5, dz0 - 12),
                                F.m3_passante, (0, 0, 1), 18))
    cortes.append(caixa(-10, 10, B.pescoco_y - 33, B.pescoco_y - 24, dz0 - 1, B.deck_z + 1))                       # cabos (flat da câmera + servos)
    cortes.append(sim(caixa(15, X0 + 0.5, B.ombro[0] - 7.2, B.ombro[0] + 7.2, dz0 - 13, B.deck_z + 1)))   # corpo dos servos dos braços
    cortes.append(furo((-10, B.pescoco_y - 37, dz0 - 1), (0, 0, 1), 6, F.m3_piloto) + furo((10, B.pescoco_y - 37, dz0 - 1), (0, 0, 1), 6, F.m3_piloto))   # IMU
    # --- travessa: L298N (4 furos piloto) + passagem de fios + ponto universal
    h = P.L298N.furos / 2
    for sx in (1, -1):
        for sz in (1, -1):
            cortes.append(furo((sx * h, B.travessa_y[0] - 1, B.driver_z + sz * h), (0, 1, 0), 5, F.m3_piloto))
        cortes.append(furo((sx * 10, B.travessa_y[0] - 1, 104), (0, 1, 0), 5, F.m3_piloto))
    cortes.append(furo((0, B.travessa_y[0] - 1, B.driver_z), (0, 1, 0), 5, 16.0))
    # --- piso: furos das cascas, pontos universais (queda/laterais), chave, conector de carga, esfera
    for (x, y) in B.furos_torso_frente + B.furos_torso_costas + B.furos_perna + B.furos_cauda:
        for sx in ((1, -1) if x else (1,)):
            cortes.append(furo((sx * x, y, Z0 - 1), (0, 0, 1), 6, F.m3_passante))
    for sx in (1, -1):
        cortes.append(universal_z(sx * 46.5, 30.0, Z0, Z1, "y"))
        cortes.append(universal_z(sx * 46.5, -30.0, Z0, Z1, "y"))
    rw, rh = P.CHAVE.recorte
    cortes.append(caixa(-rw / 2, rw / 2, B.chave_y - rh / 2, B.chave_y + rh / 2, Z0 - 1, Z1 + 1))
    cortes.append(caixa(-rw / 2 - 3, rw / 2 + 3, B.chave_y - rh / 2 - 3, B.chave_y + rh / 2 + 3, Z0 + P.CHAVE.painel, Z1 + 1))
    cortes.append(furo((0, B.jack_y, Z0 - 1), (0, 0, 1), 6, P.JACK.furo_d))
    cortes.append(furo((0, B.jack_y, Z0 + 2.5), (0, 0, 1), 3, 15.0))
    cortes.append(esfera((0, ey, P.ESFERA.d / 2), P.ESFERA.d / 2 + 0.35))
    for sx in (1, -1):
        cortes.append(inserto((sx * 10.5, ey, Z0), (0, 0, 1)))
    cortes.append(inserto((0, py0 - 6, zr), (0, 1, 0)))
    for (px, pz, pyt) in B.postes_frente:
        for sx in (1, -1):
            cortes.append(inserto((sx * px, pyt, pz), (0, -1, 0)))
    corpo = corpo - uniao(*cortes)
    return Peca("chassi", corpo, material="PETG", cor="grafite", grupo="corpo", comum=True, macica=True,
                suporte="não", explode=(0, 0, 0),
                obs="piso + rack das bandejas + deck do servo de pan; imprime em pé, piso na mesa")


def capa_esfera() -> Peca:
    ey = B.esfera_y
    z0, z1 = 3.2, Z0 - 0.2
    anel = cil((0, ey, z0), (0, ey, z1), 14.5)
    r = P.ESFERA.d / 2
    cone = cil((0, ey, z0 - 0.01), (0, ey, z1 + 0.01), r - 0.8, r + 0.4)
    m = anel - cone
    for sx in (1, -1):
        m = m - furo((sx * 10.5, ey, z0 - 1), (0, 0, 1), 8, F.m3_passante) - furo((sx * 10.5, ey, z0 - 1), (0, 0, 1), 1 + 2.4, F.cabeca_m3_d)
    return Peca("capa-esfera", m, material="PETG", cor="grafite", comum=True, macica=True, imprimir=rot("x", 180),
                explode=(0, 0, -30), obs="anel que segura a esfera de apoio; 2 M3x8")


# ------------------------------------------------------------------ bandejas
def _bandeja_base(nivel=0):
    w, L, e = B.bandeja
    zt = B.trilho_z[nivel] + 0.3
    y0 = B.bandeja_y0
    m = caixa(-w / 2, w / 2, y0, y0 + L, zt, zt + e)
    # bloco da trava (inserto M3 pela lateral direita)
    m = m - prisma([(w / 2 + 1, y0 - 1), (w / 2 + 1, y0 + 8), (w / 2 - 14, y0 - 1)], "z", zt - 1, zt + e + 1) - prisma([(-w / 2 - 1, y0 - 1), (-w / 2 - 1, y0 + 8), (-w / 2 + 14, y0 - 1)], "z", zt - 1, zt + e + 1)
    bl = caixa(20.5, X0 - 0.4, B.trava_y - 4, B.trava_y + 4, zt - 8, zt + 0.01)
    m = m + bl - inserto((X0 - 0.4, B.trava_y, zt - 4.1), (-1, 0, 0))
    # puxador atrás
    m = m + caixa(-10, 10, y0 - 4, y0 + 0.01, zt, zt + e)
    return m, zt + e


def _vazados(m, zt, furos_xy):
    # rasgos de ventilação/alívio, longe dos pilares
    for (x, y, lx, ly) in furos_xy:
        m = m - caixa(x - lx / 2, x + lx / 2, y - ly / 2, y + ly / 2, zt - 4, zt + 1)
    return m


def pos_uno(nivel=0):
    """Posição dos furos do Uno na bandeja: (x, y) em montagem. USB para trás."""
    return [(yd - P.UNO.placa[1] / 2, B.bandeja_y0 + 16.5 + x) for (x, yd) in P.UNO.furos]


def pos_pi():
    """Furos do Pi na bandeja. Blocos USB/Ethernet para trás."""
    return [(-P.PI.placa[1] / 2 + y, B.bandeja_y0 + 85.0 - x) for (x, y) in P.PI.furos]


def bandeja_uno() -> Peca:
    m, zt = _bandeja_base(0)
    m = _vazados(m, zt, [(0, B.bandeja_y0 + 50, 22, 30)])
    for (x, y) in pos_uno():
        m = m + cil((x, y, zt - 0.01), (x, y, zt + B.espacador), 3.5, seg=24)
    for (x, y) in pos_uno():
        m = m - furo((x, y, zt - 2.5), (0, 0, 1), B.espacador + 3, F.m3_piloto)
    return Peca("bandeja-uno", m, material="PETG", cor="amarelo", comum=True, macica=True, explode=(0, -120, 0),
                obs="bandeja deslizante do Arduino Uno (+ shield); 4 parafusos M3x8 auto-atarraxantes")


def bandeja_pi() -> Peca:
    m, zt = _bandeja_base(1)
    m = _vazados(m, zt, [(0, B.bandeja_y0 + 52, 30, 40)])
    for (x, y) in pos_pi():
        m = m + cil((x, y, zt - 0.01), (x, y, zt + B.espacador), 3.0, seg=24)
    for (x, y) in pos_pi():
        m = m - furo((x, y, zt - 2.5), (0, 0, 1), B.espacador + 3, F.m25_piloto)
    return Peca("bandeja-pi", m, material="PETG", cor="amarelo", comum=True, macica=True, explode=(0, -120, 0),
                obs="bandeja deslizante do Raspberry Pi 4/5; 4 parafusos M2,5x8 auto-atarraxantes")


# ------------------------------------------------------------------ pescoço
POS_MESA = [(0.0, CY - 8.0), (0.0, CY - 0.5)]     # parafusos mesa -> coluna, no plano de simetria (acesso por cima, sob a crista)


def garfo() -> Peca:
    zb = B.deck_z + P.MG996R.aba_ate_topo_horn       # topo do horn do pan = base do garfo
    zt = zb + N.garfo_base_esp
    hd = P.MG996R.horn_d
    gx, ge = N.garfo_x, N.garfo_esp
    base = cil((CX, CY, zb), (CX, CY, zt), N.garfo_base_r) + caixa(-gx - ge, gx + ge, CY - 9, CY + 9, zb, zt)
    anel = cil((CX, CY, zb - 1.8), (CX, CY, zb + 0.01), hd / 2 + 3.0) - cil((CX, CY, zb - 2), (CX, CY, zb + 0.02), hd / 2 + 0.4)
    gx, ge = N.garfo_x, N.garfo_esp
    ztopo = CZ + 13
    mont = caixa(gx, gx + ge, CY - 9, CY + 9, zt - 0.01, ztopo) + cil((gx, CY, ztopo), (gx + ge, CY, ztopo), 9.0)
    m = uniao(base, anel, mont, espelho_x(mont))
    # montante esquerdo: parafuso M3x10 com inserto vira o pino do berço
    m = m + cil((-gx - ge + 0.01, CY, CZ), (-gx - ge - 3.0, CY, CZ), 5.5)
    m = m - inserto((-gx - ge - 3.0, CY, CZ), (1, 0, 0)) - furo((-gx - ge - 3.5, CY, CZ), (1, 0, 0), ge + 5, 3.3)
    # montante direito: horn redondo do servo de tilt (rebaixo de centragem, furo central, 4 rasgos dos parafusinhos)
    m = m - cil((gx - 0.01, CY, CZ), (gx + 1.0, CY, CZ), hd / 2 + 0.3)
    m = m - furo((gx - 1, CY, CZ), (1, 0, 0), ge + 2, 9.0)
    for a in (45, 135, 225, 315):
        c, s_ = np.cos(np.radians(a)), np.sin(np.radians(a))
        m = m - rasgo((gx - 1, CY + 5.5 * c, CZ + 5.5 * s_), (gx - 1, CY + 8.6 * c, CZ + 8.6 * s_), 2.2, (1, 0, 0), ge + 2)
    # horn do servo de pan: furo central + 4 rasgos radiais
    m = m - furo((CX, CY, zb - 3), (0, 0, 1), 10, 6.5)
    for a in (0, 90, 180, 270):
        c, s_ = np.cos(np.radians(a)), np.sin(np.radians(a))
        m = m - rasgo((CX + 5.5 * c, CY + 5.5 * s_, zb - 3), (CX + 9.0 * c, CY + 9.0 * s_, zb - 3), 2.2, (0, 0, 1), 10)
    # passagem de cabos (flat da câmera e fios dos servos da cabeça), à frente do eixo
    m = m - caixa(-9, 9, CY + 14.0, CY + 20.0, zb - 3, zt + 1)
    return Peca("garfo-pescoco", m, material="PETG", cor="grafite", grupo="pan", comum=True, macica=True,
                explode=(0, 0, 30), obs="gira com o servo de pan (horn redondo) e segura o eixo do tilt")


def berco() -> Peca:
    s9 = P.MG996R
    xa = X_ABA_TILT
    zc = CZ - s9.eixo_da_ponta + s9.corpo[0] / 2      # centro do corpo do servo de tilt (em pé)
    z_topo = zc + s9.comp_abas / 2 + 2.5              # acima da aba de cima
    pA = caixa(xa - 4, xa, CY - 11, CY + 11, CZ - 18.5, z_topo)
    xb = -N.garfo_x + 0.5
    pB = caixa(xb, xb + 4, CY - 10, CY + 10, CZ - 8, z_topo)
    ponte = caixa(xb, xa, CY - 11, CY + 11, z_topo - 0.01, z_topo + 4)
    zt = CZ + N.mesa_z
    col = cil((CX, CY, z_topo + 3.99), (CX, CY, zt), N.coluna_r) - caixa(-20, 20, CY + N.coluna_chato, CY + 20, z_topo, zt + 1)
    m = uniao(pA, pB, ponte, col)
    jl, jw = s9.janela
    m = m - caixa(xa - 5, xa + 1, CY - jw / 2, CY + jw / 2, zc - jl / 2, zc + jl / 2)
    for sy in (1, -1):
        for sz in (1, -1):
            zz = zc + sz * s9.furos_aba[0] / 2
            m = m - rasgo((xa - 5, CY + sy * s9.furos_aba[1] / 2, zz - 1.5), (xa - 5, CY + sy * s9.furos_aba[1] / 2, zz + 1.5), F.m3_passante, (1, 0, 0), 6)
    m = m - furo((xb - 0.5, CY, CZ), (1, 0, 0), 5, 3.3)
    for (mx, my) in POS_MESA:
        m = m - inserto((mx, my, zt), (0, 0, -1))
    return Peca("berco-tilt", m, material="PETG", cor="grafite", grupo="cabeca", comum=True, macica=True,
                imprimir=rot("x", 180), suporte="sim (pouco, sob a ponte)", explode=(0, 0, 60),
                obs="segura o servo de tilt (MG996R em pé) e sobe pela abertura da gola até a mesa da cabeça; cabos pela face chata da coluna")





# ------------------------------------------------------------------ peças pequenas
def pino_guia(copias) -> Peca:
    m = cil((0, 0, 0), (0, 0, 9.0), F.pino_d / 2 - 0.1, seg=24)
    return Peca("pino-guia", m, cor="cinza", comum=True, macica=True, copias=copias, obs="pino Ø4 x 9 entre as metades do torso")


def bucha_eixo(copias) -> Peca:
    m = cil((0, 0, 0), (0, 0, 3.4), 3.6, seg=24) - cil((0, 0, -1), (0, 0, 5), 1.75, seg=24)
    return Peca("bucha-eixo", m, cor="cinza", comum=True, macica=True, copias=copias, obs="bucha do eixo livre da mandíbula")


def teste_encaixe() -> Peca:
    """Cupom de teste: imprima ANTES das peças grandes para acertar as folgas em cad/parametros.py."""
    m = caixa(0, 70, 0, 34, 0, 8)
    jl, jw = P.MICRO.janela
    m = m - caixa(4, 4 + jl, 4, 4 + jw, -1, 9)                       # janela do micro servo
    for i, d in enumerate((3.9, 4.0, 4.1)):                          # furos de inserto
        m = m - furo((34 + i * 9, 8, 8.01), (0, 0, -1), F.inserto_prof, d)
    m = m - furo((34, 22, -1), (0, 0, 1), 10, F.m3_passante)         # M3 passante
    m = m - furo((43, 22, -1), (0, 0, 1), 10, F.m3_piloto)           # M3 piloto
    m = m - furo((52, 22, -1), (0, 0, 1), 10, F.m25_piloto)          # M2,5 piloto
    m = m - furo((61, 22, -1), (0, 0, 1), 10, F.m2_piloto)           # M2 piloto
    for i, f in enumerate((0.2, 0.25, 0.3)):                         # soquetes do pino-guia
        m = m - furo((6 + i * 8, 26, 8.01), (0, 0, -1), 5, F.pino_d + 2 * f - 0.2)
    m = m - furo((62, 8, -1), (0, 0, 1), 10, P.TT.eixo_d + 0.2)      # eixo do motor TT (gira livre)
    m = m - furo((43, 14.2, 8.01), (0, 0, -1), 0.8, 1.8) - furo((14, 32.0, 8.01), (0, 0, -1), 0.8, 1.8)   # covinhas: marcam o furo de 4,0 e o soquete de 0,25 (os do projeto)
    return Peca("teste-encaixe", m, cor="cinza", comum=True, macica=True,
                obs="cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto")


# ------------------------------------------------------------------ componentes comuns
def comps_base(arms=True):
    cs = []
    cs.append(Comp("servo-pan MG996R", C.servo_padrao().transform(M_pan()[:3, :]), "corpo", P.MG996R.massa, "preto"))
    cs.append(Comp("servo-tilt MG996R", C.servo_padrao().transform(M_tilt()[:3, :]), "cabeca", P.MG996R.massa, "preto"))
    if arms:
        cs.append(Comp("servo-braco-dir", C.micro_servo().transform(M_braco(1)[:3, :]), "corpo", P.MICRO.massa, "azul"))
        cs.append(Comp("servo-braco-esq", C.micro_servo().transform(M_braco(-1)[:3, :]), "corpo", P.MICRO.massa, "azul"))
    for lado, nm in ((1, "dir"), (-1, "esq")):
        cs.append(Comp(f"motor-tt-{nm}", C.motor_tt(encoder=B.encoder_extra).transform(M_motor(lado)[:3, :]), "corpo", P.TT.massa, "amarelo"))
        r = C.roda()
        r = r.translate([X_RODA, 0, B.eixo_roda_z]) if lado > 0 else espelho_x(r.translate([X_RODA, 0, B.eixo_roda_z]))
        cs.append(Comp(f"roda-{nm}", r, "corpo", P.RODA.massa, "preto"))
    cs.append(Comp("bateria 2x18650", C.bateria().translate([0, B.bateria_y, Z1]), "corpo", P.BATERIA.massa_suporte + 2 * P.BATERIA.massa_celula, "prata"))
    cs.append(Comp("esfera-apoio", C.esfera_apoio().translate([0, B.esfera_y, P.ESFERA.d / 2]), "corpo", P.ESFERA.massa, "prata"))
    cs.append(Comp("chave", C.chave().translate([0, B.chave_y, Z0]), "corpo", 3.0, "preto"))
    cs.append(Comp("driver L298N", C.driver().translate([0, B.travessa_y[1] + 3.0, B.driver_z]), "corpo", P.L298N.massa, "prata"))
    # placas nas bandejas: Uno (nível A) e Pi (nível B)
    zA = B.trilho_z[0] + 0.3 + B.bandeja[2] + B.espacador
    zB = B.trilho_z[1] + 0.3 + B.bandeja[2] + B.espacador
    uno = C.placa_eletronica(P.UNO).transform(C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (P.UNO.placa[1] / 2, B.bandeja_y0 + 16.5, zA))[:3, :])
    pi = C.placa_eletronica(P.PI).transform(C.M([(0, -1, 0), (1, 0, 0), (0, 0, 1)], (-P.PI.placa[1] / 2, B.bandeja_y0 + 85.0, zB))[:3, :])
    cs.append(Comp("Arduino Uno + shield", uno, "corpo", P.UNO.massa + 20, "azul"))
    cs.append(Comp("Raspberry Pi 4/5", pi, "corpo", P.PI.massa, "verde", fase2=False))
    return cs


def juntas_base():
    return {
        "pan": Junta("corpo", (CX, CY, CZ), (0, 0, 1), N.pan),
        "cabeca": Junta("pan", (CX, CY, CZ), (1, 0, 0), N.tilt),
    }


def ordem_bicho(traseira, pernas, cabeca, extras_frente=(), extras_costas=(), bracos=False, painel=("barriga",), enfeites=()):
    """Ordem de montagem dos bichos (usada no PLANO e conferida pelo teste 9 do verificador)."""
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    nX, nY, nZ = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
    o = [
        dict(passo="chassi", move=["chassi"], dir=Z),
        dict(passo="motor direito", move=["motor-tt-dir"], dir=X),
        dict(passo="motor esquerdo", move=["motor-tt-esq"], dir=nX),
        dict(passo="esfera + capa", move=["esfera-apoio", "capa-esfera"], dir=nZ, curso=40),
        dict(passo="chave", move=["chave"], dir=nZ, curso=40),
        dict(passo="servo de pan", move=["servo-pan MG996R"], dir=Z),
        dict(passo="garfo", move=["garfo-pescoco"], dir=Z),
        dict(passo="berço + servo de tilt", move=["berco-tilt", "servo-tilt MG996R"], dir=Z),
    ]
    if bracos:
        o += [dict(passo="servo do braço direito", move=["servo-braco-dir"], dir=X), dict(passo="servo do braço esquerdo", move=["servo-braco-esq"], dir=nX)]
    o += [
        dict(passo="bateria (entra por trás, inclinada por cima da chave)", move=["bateria 2x18650"], dir=(0, -1, 0), curso=15, depois=[(0, -0.6, 0.8), 120]),
        dict(passo="driver L298N", move=["driver L298N"], dir=Y, curso=80),
        dict(passo="bandeja do Uno", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=160),
        dict(passo="bandeja do Pi", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=160),
        dict(passo="torso-frente", move=["torso-frente", *extras_frente], dir=Y, curso=160),
        dict(passo="roda direita", move=["roda-dir"], dir=X),
        dict(passo="roda esquerda", move=["roda-esq"], dir=nX),
        dict(passo="painel da frente", move=[*painel, "alto-falante (fase 2)"], dir=Y, curso=80),
        dict(passo="torso-costas", move=["torso-costas", "pino-guia", *extras_costas], dir=nY, curso=160),
        dict(passo="perna direita", move=[pernas[0], *pernas[2]], dir=X),
        dict(passo="perna esquerda", move=[pernas[1], *pernas[3]], dir=nX),
        dict(passo="traseira", move=list(traseira), dir=nY, curso=160),
        dict(passo="mesa dentro do crânio (na bancada)", move=["mesa-cabeca", "servo-boca MG90S"], dir=nZ, curso=100, contra=["cranio"]),
        dict(passo="cabeça no pescoço", move=list(cabeca), dir=Z, curso=140),
    ]
    if bracos:
        o += [dict(passo="braço direito", move=["braco-dir"], dir=X, curso=60), dict(passo="braço esquerdo", move=["braco-esq"], dir=nX, curso=60)]
    # abertura para manutenção (teste de saída): cabeça, traseira, costas e bandejas.
    # A cabeça sai antes porque a metade de trás da esfera do pescoço fica dentro dela.
    o += [
        dict(passo="ABRIR: cabeça sai para cima", move=list(cabeca), dir=Z, curso=140, sai=True),
        dict(passo="ABRIR: traseira sai", move=list(traseira), dir=nY, curso=160, sai=True),
        dict(passo="ABRIR: torso-costas sai", move=["torso-costas", "pino-guia", *extras_costas], dir=nY, curso=160, sai=True),
        dict(passo="ABRIR: bandeja do Pi sai", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=160, sai=True),
        dict(passo="ABRIR: bandeja do Uno sai", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=160, sai=True),
    ]
    return o


def obstaculos_tras(folga=0.8):
    """O que fica acima do piso atrás do rack e que as costas têm de contornar ao sair: ressalto da esfera e chave."""
    ey = B.esfera_y
    rw, rh = P.CHAVE.corpo
    return uniao(cil((0, ey, 0), (0, ey, Z0 + 10.5 + folga), 14.5 + folga),
                 caixa(-rw / 2 - folga, rw / 2 + folga, B.chave_y - rh / 2 - folga, B.chave_y + rh / 2 + folga, 0, Z0 + P.CHAVE.prof + folga))
