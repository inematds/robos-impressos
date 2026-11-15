"""Esqueleto BAIXO E LARGO dos bichos cuja casca vem de malha (rodada 2). Diferente do esqueleto alto de base.py:
a junta do pescoço desce (capivara: Z=150 em vez de 185), o rack das placas fica ATRÁS (Pi no nível de baixo, Uno +
shield no de cima, bateria no piso; tudo sai por trás, pela porta da casca), a torre do servo de pan fica na FRENTE e
as esferas de apoio vão sob as patas da frente (o centro de gravidade cai à frente do eixo das rodas).

Tudo recebe `E` = esqueleto(K): os parâmetros `K.esq` do bicho (comum/cad/parametros.py) já no referencial do robô.
O que continua igual ao esqueleto alto e é reaproveitado de base.py sem mudança de geometria: garfo e berço do pescoço
(transladados para a junta nova), capa da esfera, envelopes dos componentes, matrizes dos motores.
"""
from __future__ import annotations

from types import SimpleNamespace as NS

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import casca as CA
from cad.comum import componentes as C
from cad.comum.base import F, furo, inserto, rasgo, sim
from cad.comum.geo import berco_modulo, caixa, cil, esfera, espelho_x, mat_trans, prisma, uniao
from cad.comum.modelo import Comp, Junta, Peca

N = P.PESCOCO


def esqueleto(K) -> NS:
    """Parâmetros do esqueleto no referencial do robô (soma `dy` aos valores dados no referencial da pele)."""
    e, dy = K.esq, K.dy
    E = NS(**vars(e))
    E.dy = dy
    E.centro = (0.0, K.pescoco[0] + dy, K.pescoco[1])
    par = lambda t: tuple(v + dy for v in t)
    E.parede_y, E.travessa_y, E.pi_y, E.uno_y = par(e.parede_y), par(e.travessa_y), par(e.pi_y), par(e.uno_y)
    E.bateria_y, E.pi_placa_y, E.uno_placa_y = e.bateria_y + dy, e.pi_placa_y + dy, e.uno_placa_y + dy
    E.esferas = tuple((x, y + dy) for (x, y) in e.esferas)
    E.z_gola = K.z_gola
    x0, x1, y0, y1, zt, zp = e.poste_porta
    E.poste_porta = (x0, x1, y0 + dy, y1 + dy, zt, zp)
    E.x0, E.x1 = e.parede_x0, e.parede_x0 + e.parede_esp
    E.stepdown, E.ubec = (e.stepdown[0] + dy, e.stepdown[1]), (e.ubec[0] + dy, e.ubec[1])
    E.bms, E.chave = (e.bms[0], e.bms[1] + dy), (e.chave[0], e.chave[1] + dy)
    assert abs(E.x1 - BS.X1) < 1e-9, "as matrizes dos motores de base.py valem para a parede em X=34"
    E.x_roda = E.x1 + P.TT.caixa[2] + P.RODA.folga_caixa
    E.eixo_roda_z = P.RODA.d / 2
    E.T = np.array(E.centro) - np.array(N.centro)          # do pescoço padrão (base.py) para o deste bicho
    assert abs(E.deck_z - (BS.B.deck_z + E.T[2])) < 1e-6, "deck_z tem de ficar 48 mm abaixo do centro da junta"
    return E


# ------------------------------------------------------------------ piso
def poligono_piso(E, pele):
    """Contorno do piso: a seção da PRÓPRIA pele em z do piso, recuada para dentro (parede + folga), limitada a
    |x| <= piso_x, mais um braço até cada esfera de apoio. Simétrico em X."""
    from shapely import affinity
    from shapely.geometry import Point, box
    from shapely.ops import unary_union

    sec = CA.contorno_secao(pele, E.piso_z[0], E.piso_nivel)
    partes = [sec.intersection(box(-E.piso_x, -1000, E.piso_x, 1000))]
    for (x, y) in E.esferas:
        for s in (1, -1):
            partes.append(Point(s * x, y).buffer(14.5).union(box(min(s * x, s * (E.piso_x - 3)), y - 10, max(s * x, s * (E.piso_x - 3)), y + 10)))
    pol = unary_union(partes).intersection(sec).buffer(-0.8).buffer(0.8)      # tira farpas
    x0p, _, ya = E.poste_porta[0], E.poste_porta[1], E.poste_porta[2]          # atrás dos postes o piso estreita: ali descem os blocos dos parafusos
    pol = pol.difference(box(x0p - 1.0, -1000, 200, ya - 0.3)).difference(box(-200, -1000, -x0p + 1.0, ya - 0.3))
    pol = pol.intersection(affinity.scale(pol, xfact=-1.0, origin=(0, 0)))
    return CA.maior_poligono(pol).simplify(0.3)


def piso_solido(E, pol, folga=0.0, z0=None, z1=None):
    z0 = E.piso_z[0] if z0 is None else z0
    z1 = E.piso_z[1] if z1 is None else z1
    return CA.prisma_poligono(pol.buffer(folga) if folga else pol, z0, z1)


# ------------------------------------------------------------------ chassi
def chassi(E, pol) -> Peca:
    Z0, Z1 = E.piso_z
    X0, X1 = E.x0, E.x1
    py0, py1 = E.parede_y
    ty0, ty1 = E.travessa_y
    dz0 = E.deck_z - E.deck_esp
    cy = E.centro[1]
    placa = piso_solido(E, pol)
    # paredes do rack (atrás, até rack_z) e da torre do pan (na frente, até o deck). A torre acaba onde o piso
    # acaba (a bacia desce por cima: nada do chassi pode ficar em balanço sobre a casca), por isso o servo de pan
    # vai DEITADO DE LADO (corpo para +X) e a parede direita da torre fica mais para fora (torre_x1).
    XT = E.torre_x1
    rack = caixa(X0, X1, py0, ty1, Z1 - 0.01, E.rack_z)
    torre_e = caixa(-X1, -X0, ty0, py1, Z1 - 0.01, E.deck_z)
    torre_d = caixa(XT, XT + E.parede_esp, ty0, py1, Z1 - 0.01, E.deck_z)
    quina = prisma([(py1 - 7.0, Z1 - 1.0), (py1 + 1.0, Z1 - 1.0), (py1 + 1.0, Z1 + 7.0)], "x", -200, 200)   # chanfro a 45° no pé da frente (a barriga da pele sobe ali)
    torre_e, torre_d = torre_e - quina, torre_d - quina
    # travessa (parede inteira do piso ao deck: o L298N vai na face da frente; a bateria encosta por trás)
    travessa = caixa(-X1, XT + E.parede_esp, ty0, ty1, Z1 - 0.01, dz0 + 0.01)
    # deck: placa entre as paredes da torre, apoiada na travessa (atrás), em 2 mísulas a 45° (lados) e num arco em
    # "V" a 45° (frente): nada de ponte no ar
    deck = caixa(-X0 - 0.01, XT + 0.01, ty0, py1, dz0, E.deck_z)
    s9 = P.MG996R
    jx0 = -s9.eixo_da_ponta - (s9.janela[0] - s9.corpo[0]) / 2                # janela do corpo do servo, em X
    jx1 = jx0 + s9.janela[0]
    le, ld = X0 + jx0 - 0.5, XT - jx1 - 0.5                                   # largura das mísulas (esquerda, direita)
    misula = prisma([(-X0 - 0.01, dz0 - le), (-X0 - 0.01, dz0 + 0.01), (-X0 + le, dz0 + 0.01)], "y", ty1 - 0.01, py1) \
        + prisma([(XT + 0.01, dz0 - ld), (XT + 0.01, dz0 + 0.01), (XT - ld, dz0 + 0.01)], "y", ty1 - 0.01, py1)
    xm, meia = (XT - X0) / 2, (XT + X0) / 2                                   # arco em "V" da frente
    arco = prisma([(-X0 - 0.01, dz0 - meia), (-X0 - 0.01, dz0 + 0.01), (xm, dz0 + 0.01)], "y", py1 - 3.0, py1) \
        + prisma([(XT + 0.01, dz0 - meia), (XT + 0.01, dz0 + 0.01), (xm, dz0 + 0.01)], "y", py1 - 3.0, py1)
    # postes da porta traseira (ponta de trás das paredes, engrossada para o inserto horizontal)
    px0, px1, pya, pyb, pzt, pzp = E.poste_porta
    poste = caixa(px0, X1, pya, pyb, Z1 - 0.01, pzt) + prisma([(X1 - 0.01, Z1), (px1, Z1 + (px1 - X1)), (px1, pzt), (X1 - 0.01, pzt)], "y", pya, pyb)
    # orelhas da gola: sobem da torre até a base da gola (2 M3 por cima); a da esquerda abre em mísula para fora do garfo
    ow, oe = E.orelha_gola
    ze = E.z_gola - 0.05
    orelha_d = caixa(XT, XT + E.parede_esp, cy - ow / 2, cy + ow / 2, E.deck_z - 0.01, ze)
    from cad.comum.geo import casco
    orelha_e = casco(caixa(-X1, -X0, cy - ow / 2, cy + ow / 2, E.deck_z - 14.0, E.deck_z), caixa(-37.5 - oe, -37.5, cy - ow / 2, cy + ow / 2, E.deck_z + 4.0, ze))
    reforco_deck = prisma([(ty1 - 0.01, dz0 - (cy - s9.janela[1] / 2 - ty1)), (ty1 - 0.01, dz0 + 0.01), (cy - s9.janela[1] / 2, dz0 + 0.01)], "x", jx0, jx1)
    # ressaltos das esferas de apoio
    ress = uniao(*[cil((s * x, y, Z0), (s * x, y, Z0 + 10.5), 14.5) for (x, y) in E.esferas for s in (1, -1)])
    corpo = uniao(placa, sim(rack), torre_e, torre_d, travessa, deck, misula, arco, sim(poste), ress, orelha_d, orelha_e, reforco_deck)

    cortes = []
    # --- paredes: motor TT (eixo interno, rasgos dos 2 furos de trás, furo da orelha), como em base.chassi
    ez, t = E.eixo_roda_z, P.TT
    d0, d1 = 12.3 / 2 - 0.4, t.furos_tras_dist / 2 + 0.4
    for s in (1, -1):
        cortes.append(furo((s * (X0 - 1), 0, ez), (s, 0, 0), E.parede_esp + 2, t.eixo_d + 3.0))
        for sy in (1, -1):
            cortes.append(rasgo((s * (X0 - 1), sy * d0, ez + t.furos_tras), (s * (X0 - 1), sy * d1, ez + t.furos_tras),
                                F.m3_passante, (s, 0, 0), E.parede_esp + 2))
        cortes.append(rasgo((s * (X0 - 1), 0, ez - t.furo_orelha - 1.2), (s * (X0 - 1), 0, ez - t.furo_orelha + 1.2),
                            F.m3_passante, (s, 0, 0), E.parede_esp + 2))
        # trilhos das bandejas (até a travessa)
        for tz in E.trilho_z:                          # rasgo + teto em chanfro de 45° (imprime sem suporte)
            tr = caixa(X0 - 0.1, X0 + E.trilho_prof, py0 - 1, ty0 + 0.01, tz, tz + E.trilho_alt) \
                + prisma([(X0 - 0.1, tz + E.trilho_alt - 0.01), (X0 + E.trilho_prof, tz + E.trilho_alt - 0.01), (X0 - 0.1, tz + E.trilho_alt + E.trilho_prof + 0.1)], "y", py0 - 1, ty0 + 0.01)
            cortes.append(tr if s > 0 else espelho_x(tr))
        # passagens de cabo nas paredes (rack -> motores) e na torre
        cortes.append(furo((s * (X0 - 1), ty0 - 14.0, 52.0), (s, 0, 0), E.parede_esp + 2, 6.0))
    # --- deck: janela do servo de pan (deitado, corpo para +X), rasgos das abas, passagem de cabos
    jw = s9.janela[1] / 2
    cortes.append(caixa(jx0, jx1, cy - jw, cy + jw, dz0 - 1, E.deck_z + 1))
    xcs = -s9.eixo_da_ponta + s9.corpo[0] / 2
    for sx in (1, -1):
        for sy in (1, -1):
            xx = xcs + sx * s9.furos_aba[0] / 2
            cortes.append(rasgo((xx - 1.5, cy + sy * s9.furos_aba[1] / 2, dz0 - 12), (xx + 1.5, cy + sy * s9.furos_aba[1] / 2, dz0 - 12),
                                F.m3_passante, (0, 0, 1), 18))
    cortes.append(caixa(jx0 - 12.0, jx0 - 6.0, cy - 8, cy + 8, dz0 - 1, E.deck_z + 1))          # cabos sobem ao lado do servo
    # --- travessa: L298N (4 furos piloto pela frente) + passagem de fios
    h = P.L298N.furos / 2
    for sx in (1, -1):
        for sz in (1, -1):
            cortes.append(furo((sx * h, ty1 + 1, E.driver_z + sz * h), (0, -1, 0), 5, F.m3_piloto))
    cortes.append(furo((0, ty1 + 1, E.driver_z), (0, -1, 0), 5, 6.0))
    cortes.append(furo((0, ty1 + 1, dz0 - 10.0), (0, -1, 0), 5, 6.0))
    # --- piso: furos das orelhas da bacia, esferas (soquete + insertos da capa)
    for (x, y) in E.esferas:
        for s in (1, -1):
            cortes.append(esfera((s * x, y, P.ESFERA.d / 2), P.ESFERA.d / 2 + 0.35))
            cortes.append(cil((s * x, y, P.ESFERA.d / 2 + 5.9), (s * x, y, Z0 + 9.3), 5.9, 1.5))     # teto do soquete em cone de 45° (sem suporte)
            for sx in (1, -1):
                cortes.append(inserto((s * x + sx * 10.5, y, Z0), (0, 0, 1)))
    # --- postes da porta: inserto horizontal, entrando por trás
    for sx in (1, -1):
        cortes.append(inserto((sx * E.poste_x[0], pya, pzp), (0, 1, 0)))
        cortes.append(inserto((sx * E.poste_x[1], pya, E.bacia_parafuso_z), (0, 1, 0)))
    cortes.append(inserto((XT + E.parede_esp / 2, cy, ze), (0, 0, -1)))
    cortes.append(inserto((-37.5 - oe / 2, cy, ze), (0, 0, -1)))
    # --- energia: berços (cantoneiras + abraçadeira) do step-down, do UBEC e do BMS; recorte da chave no piso
    somas = []
    for nome in ("stepdown", "ubec", "bms"):
        M, mod = mat_modulo(E, nome)
        so, co = berco_modulo(mod, alt=4.0 if nome == "bms" else 2.4, piso=(Z1 - Z0) if nome == "bms" else E.parede_esp, canal=1.2 if nome == "bms" else 0.0)   # na parede: cantoneira baixa (pouco balanço)
        somas.append(so.transform(M[:3, :]))
        cortes.append(co.transform(M[:3, :]))
    kx, ky = E.chave
    rw, rh = P.CHAVE.recorte
    cortes.append(caixa(kx - rw / 2, kx + rw / 2, ky - rh / 2, ky + rh / 2, Z0 - 1, Z1 + 1))
    cortes.append(caixa(kx - rw / 2 - 3, kx + rw / 2 + 3, ky - rh / 2 - 3, ky + rh / 2 + 3, Z0 + P.CHAVE.painel, Z1 + 1))
    corpo = uniao(corpo, *somas) - uniao(*cortes)
    return Peca("chassi", corpo, material="PETG", cor="grafite", grupo="corpo", macica=True, suporte="não", explode=(0, 0, 0),
                perimetros=4, infill=25, orientacao="piso na mesa (em pé)",
                reforco="mísulas e arco a 45° sob o deck do pan; travessa inteira do piso ao deck; postes de trás engrossados (10 mm de parede em volta dos insertos); orelhas da gola em mísula; trilhos com teto em chanfro",
                obs="piso recortado da seção da pele + rack das bandejas (atrás) + torre e deck do servo de pan (frente) + ressaltos das 2 esferas")


def mat_modulo(E, nome):
    """Matriz 4x4 que leva o módulo de energia do referencial de componentes.modulo()/geo.berco_modulo() (centrado em
    XY, comprimento em X, z=0 = assento) para o lugar dele no chassi. Devolve (matriz, parâmetros do módulo)."""
    if nome == "stepdown":                       # em pé, na face de fora (x = -X1) da parede esquerda da torre
        y, z = E.stepdown
        return C.M([(0, 0, 1), (0, 1, 0), (-1, 0, 0)], (-E.x1, y, z)), P.STEPDOWN5V
    if nome == "ubec":                           # em pé, na face de fora da parede direita da torre
        y, z = E.ubec
        return C.M([(0, 0, 1), (0, -1, 0), (1, 0, 0)], (E.torre_x1 + E.parede_esp, y, z)), P.UBEC6V
    if nome == "bms":                            # deitado no piso, sob o L298N
        x, y = E.bms
        return C.M(None, (x, y, E.piso_z[1])), P.BMS2S
    raise ValueError(nome)


def capa_esfera(E) -> Peca:
    """A mesma capa da esfera de base.py (peça comum), uma em cada esfera de apoio."""
    base = BS.capa_esfera()
    s = base.solido.translate([0, -BS.B.esfera_y, 0])
    base.solido = s
    base.copias = [mat_trans((sx * x, y, 0.0)) for (x, y) in E.esferas for sx in (1, -1)]
    base.explode = (0, 0, -30)
    return base


# ------------------------------------------------------------------ bandejas
def _bandeja(E, nivel, y0, y1, furos, r_pilar, d_piloto, vazado):
    w, e = E.bandeja_larg, E.bandeja_esp
    zt = E.trilho_z[nivel] + 0.3
    m = caixa(-w / 2, w / 2, y0, y1, zt, zt + e) + caixa(-10, 10, y0 - 4, y0 + 0.01, zt, zt + e)       # placa + puxador atrás
    cx, cyv, lx, ly = vazado
    m = m - caixa(cx - lx / 2, cx + lx / 2, cyv - ly / 2, cyv + ly / 2, zt - 1, zt + e + 1)
    for (x, y) in furos:
        m = m + cil((x, y, zt + e - 0.01), (x, y, zt + e + E.espacador), r_pilar, seg=24)
    for (x, y) in furos:
        m = m - furo((x, y, zt + 0.6), (0, 0, 1), E.espacador + e, d_piloto)
    return m, zt + e + E.espacador


def pos_pi(E):
    """Furos do Pi (x, y) no robô. Blocos USB/Ethernet para trás."""
    return [(-P.PI.placa[1] / 2 + y, E.pi_placa_y - x) for (x, y) in P.PI.furos]


def pos_uno(E):
    """Furos do Uno (x, y) no robô. USB para trás."""
    return [(yd - P.UNO.placa[1] / 2, E.uno_placa_y + x) for (x, yd) in P.UNO.furos]


def bandeja_pi(E) -> Peca:
    m, _ = _bandeja(E, 0, E.pi_y[0], E.pi_y[1], pos_pi(E), 3.0, F.m25_piloto, (0, (E.pi_y[0] + E.pi_y[1]) / 2, 30, 40))
    return Peca("bandeja-pi", m, material="PETG", cor="amarelo", macica=True, explode=(0, -150, 0), perimetros=4, infill=25,
                orientacao="placa na mesa, pilares para cima", reforco="placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack",
                obs="bandeja deslizante do Raspberry Pi 4/5 (nível de baixo); sai por trás, pela porta; 4 M2,5x8 auto-atarraxantes")


def bandeja_uno(E) -> Peca:
    m, _ = _bandeja(E, 1, E.uno_y[0], E.uno_y[1], pos_uno(E), 3.5, F.m3_piloto, (0, (E.uno_y[0] + E.uno_y[1]) / 2, 22, 30))
    return Peca("bandeja-uno", m, material="PETG", cor="amarelo", macica=True, explode=(0, -150, 0), perimetros=4, infill=25,
                orientacao="placa na mesa, pilares para cima", reforco="placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack",
                obs="bandeja deslizante do Arduino Uno + shield (nível de cima); sai por trás, pela porta; 4 M3x8 Allen direto no plástico")


# ------------------------------------------------------------------ pescoço (peças comuns de base.py, transladadas)
def pescoco(E):
    g, b = BS.garfo(), BS.berco()
    for p in (g, b):
        p.solido = p.solido.translate(list(E.T))
    return [g, b]


def juntas(E):
    return {"pan": Junta("corpo", E.centro, (0, 0, 1), N.pan), "cabeca": Junta("pan", E.centro, (1, 0, 0), N.tilt)}


# ------------------------------------------------------------------ componentes
def comps(E):
    Z0, Z1 = E.piso_z
    T = list(E.T)
    cs = [Comp("servo-pan MG996R", C.servo_padrao().translate([0, E.centro[1], E.deck_z]), "corpo", P.MG996R.massa, "preto"),   # deitado: corpo para +X
          Comp("servo-tilt MG996R", C.servo_padrao().transform(BS.M_tilt()[:3, :]).translate(T), "cabeca", P.MG996R.massa, "preto")]
    for lado, nm in ((1, "dir"), (-1, "esq")):
        cs.append(Comp(f"motor-tt-{nm}", C.motor_tt(encoder=E.encoder_extra).transform(BS.M_motor(lado)[:3, :]), "corpo", P.TT.massa, "amarelo"))
        r = C.roda().translate([E.x_roda, 0, E.eixo_roda_z])
        cs.append(Comp(f"roda-{nm}", r if lado > 0 else espelho_x(r), "corpo", P.RODA.massa, "preto"))
        for (x, y) in E.esferas:
            cs.append(Comp(f"esfera-{nm}", C.esfera_apoio().translate([lado * x, y, P.ESFERA.d / 2]), "corpo", P.ESFERA.massa, "prata"))
    cs.append(Comp("bateria 2x18650", C.bateria().translate([0, E.bateria_y, Z1]), "corpo", P.BATERIA.massa_suporte + 2 * P.BATERIA.massa_celula, "prata"))
    cs.append(Comp("driver L298N", C.driver().translate([0, E.travessa_y[1] + 3.0, E.driver_z]), "corpo", P.L298N.massa, "prata"))
    e = E.bandeja_esp + E.espacador
    zP, zU = E.trilho_z[0] + 0.3 + e, E.trilho_z[1] + 0.3 + e
    pi = C.placa_eletronica(P.PI).transform(C.M([(0, -1, 0), (1, 0, 0), (0, 0, 1)], (-P.PI.placa[1] / 2, E.pi_placa_y, zP))[:3, :])
    uno = C.placa_eletronica(P.UNO).transform(C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (P.UNO.placa[1] / 2, E.uno_placa_y, zU))[:3, :])
    for nome, rot_ in (("stepdown", "step-down 5V (LM2596)"), ("ubec", "ubec 6V 3A"), ("bms", "bms 2S")):
        M, mod = mat_modulo(E, nome)
        cs.append(Comp(rot_, C.modulo(mod).transform(M[:3, :]), "corpo", mod.massa, "azul"))
    cs.append(Comp("chave", C.chave().translate([E.chave[0], E.chave[1], Z0]), "corpo", 3.0, "preto"))
    cs.append(Comp("Raspberry Pi 4/5", pi, "corpo", P.PI.massa, "verde"))
    cs.append(Comp("Arduino Uno + shield", uno, "corpo", P.UNO.massa + 20, "azul"))
    return cs


def apoios(E):
    xr = E.x_roda + P.RODA.larg / 2
    return [(xr, 0.0), (-xr, 0.0)] + [(s * x, y) for (x, y) in E.esferas for s in (1, -1)]


def sombra_abaixo(solido, niveis, folga=0.6):
    """Tudo o que fica ABAIXO de um sólido (a "sombra" vertical dele, com folga), em fatias: entre niveis[i] e
    niveis[i+1] vale a projeção do que o sólido tem acima de niveis[i]. É o que uma casca que DESCE por cima do
    sólido tem de deixar livre."""
    from manifold3d import JoinType, Manifold

    partes = []
    for a, b in zip(niveis[:-1], niveis[1:]):
        cima = solido ^ caixa(-900, 900, -900, 900, a, 900)
        if cima.is_empty():
            continue
        cs = cima.project().offset(folga, JoinType.Round, circular_segments=32)
        partes.append(Manifold.extrude(cs, b - a).translate([0, 0, a]))
    return uniao(*partes)


def obstaculos_bacia(E, chassi_solido, outros=(), folga=0.6):
    """O que a bacia tem de contornar ao DESCER por cima do chassi já com rodas e esferas: a sombra do chassi
    (piso; ressaltos; paredes, torre e deck), os poços das rodas e o conjunto esfera + capa."""
    Z0, Z1 = E.piso_z
    partes = [sombra_abaixo(chassi_solido, [-5.0, Z1 + 0.2, Z0 + 10.5 + 0.2, 400.0], folga)]
    partes += [sombra_abaixo(m, [-5.0, 400.0], folga + 0.4) for m in outros]      # componentes montados antes da bacia
    r = P.RODA.d / 2 + 2.5
    xa, xb = E.x_roda - 2.5, E.x_roda + P.RODA.larg + 2.5
    poco = cil((xa, 0, E.eixo_roda_z), (xb, 0, E.eixo_roda_z), r, seg=64) + caixa(xa, xb, -r, r, -5.0, E.eixo_roda_z)
    partes.append(sim(poco))
    for (x, y) in E.esferas:
        partes.append(sim(cil((x, y, -5.0), (x, y, Z0 + 10.5 + folga), 14.5 + folga)))
    return uniao(*partes)
