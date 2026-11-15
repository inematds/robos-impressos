"""Modelo 1: dinossauro filhote (30 cm). Rodada 2: a casca é a malha de image-to-3D (cad/peles/dino.npz), com a
mesma receita da capivara (cad/comum/casca.py), sobre um esqueleto próprio.

Casca: corpo (pernas, barriga e peito; desce por cima do chassi), traseira (anca + cauda; sai para trás e dá acesso
à bateria e às bandejas sem tirar a cabeça), gola (esfera do pescoço), crânio + mandíbula. Rodas dentro das coxas,
1 esfera de apoio atrás, sob a raiz da cauda. Movimentos: pescoço pan + tilt, boca e os 2 braços (micro servo)."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import base_baixa as BB
from cad.comum import bicho as BI
from cad.comum import casca as CA
from cad.comum import componentes as C
from cad.comum.base import F, N, furo, inserto, rasgo, sim
from cad.comum.geo import (berco_modulo, caixa, campo_blobs, casco, cil, desbeliscar, esfera, espelho_x, girar, limpar, mat_giro, mat_trans,
                           maior_corpo, medir_parede, prisma, smin, uniao)
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot

K = P.DINO
ESP = np.diag([-1.0, 1, 1, 1])


def _boca(dy, dz):
    """Parâmetros da boca (dados na pele) levados a outro referencial."""
    b = dict(K.boca)
    for k in ("y_eixo", "y_corte", "y_ref"):
        b[k] += dy
    for k in ("z_eixo", "z0"):
        b[k] += dz
    return b


def _v(p, o):
    return np.asarray(p, float) + o


# ====================================================================== esqueleto próprio do dino
def _chassi(E, p_corpo, dentro) -> Peca:
    """Piso recortado da seção da pele + rack (atrás, com alargamento a 45° onde a anca é estreita) + torre e deck
    do servo de pan (sobre o eixo das rodas) + orelhas dos servos dos braços + postes da gola e do corpo + ressalto
    da esfera de trás. `dentro` = pele do corpo recuada (parede + folga): as paredes são aparadas por ela."""
    from shapely import affinity
    from shapely.geometry import Point, box
    from shapely.ops import unary_union

    e, DY = K.esq, K.dy
    Z0, Z1 = E.piso_z
    X0, X1 = E.x0, E.x1
    py0, py1 = E.parede_y
    ty0, ty1 = E.travessa_y
    dz0 = E.deck_z - E.deck_esp
    cy = E.centro[1]
    ype, dky0, yd = e.rack_y_pe + DY, e.deck_y0 + DY, K.costura_y + DY
    ye = E.esferas[0][1]
    s9, mi = P.MG996R, P.MICRO
    zr_e, zr_d = e.rack_z
    a = e.alarga_x
    pp = e.poste

    # --- piso: seção da pele em z do piso, recuada; lança até a esfera de trás; sem a faixa das abas do corpo
    sec = CA.contorno_secao(p_corpo, Z0, E.piso_nivel)
    pol = sec.intersection(box(-E.piso_x, -1000, E.piso_x, 1000))
    pol = unary_union([pol, box(-11, ye, 11, ype), Point(0, ye).buffer(14.5)])
    for s in (1, -1):
        pol = pol.difference(box(min(s * (pp.x[0] + 0.1), s * 200), -1000, max(s * (pp.x[0] + 0.1), s * 200), pp.y[0] + DY - 0.01))
    pol = pol.intersection(affinity.scale(pol, xfact=-1.0, origin=(0, 0)))
    pol = CA.maior_poligono(pol.buffer(-0.8).buffer(0.8)).simplify(0.3)
    placa = CA.prisma_poligono(pol, Z0, Z1)

    # --- rack: paredes X0..X1. Na anca (atrás de ype) o fundo é estreito: a parede nasce de um alargamento a 45° do piso
    def perfil(zr):
        ai = a + 0.7                                    # face de dentro (a bateria, de ±20,5, passa)
        return [(a - 2.5, Z0), (a, Z0), (X1, Z0 + X1 - a), (X1, zr), (X0, zr), (X0, Z1 + X0 - ai), (ai, Z1), (a - 2.5, Z1)]

    rack = uniao(prisma(perfil(zr_d), "y", py0, ype), caixa(X0, X1, ype - 0.01, ty0 + 0.01, Z1 - 0.01, zr_d),
                 espelho_x(prisma(perfil(zr_e), "y", py0, ype)), caixa(-X1, -X0, ype - 0.01, ty0 + 0.01, Z1 - 0.01, zr_e))
    torre = sim(caixa(X0, X1, ty0, py1, Z1 - 0.01, E.deck_z))
    paredes = (rack + torre) ^ dentro
    travessa = caixa(-X0 - 0.01, X0 + 0.01, ty0, ty1, Z1 - 0.01, dz0 + 0.01)
    # --- deck (corpo do servo de pan para a FRENTE): placa entre as paredes; atrás apoia na travessa e avança num
    # lábio com chanfro de 45°; dos lados, mísulas até a janela; na frente, parede em "V" sob a aba do servo
    jw = s9.janela[1] / 2
    wy0 = cy - s9.eixo_da_ponta - (s9.janela[0] - s9.corpo[0]) / 2
    wy1 = wy0 + s9.janela[0]
    fy1, xl = e.deck_y1 + DY, e.deck_lingua
    deck = caixa(-X0 - 0.01, X0 + 0.01, dky0, py1, dz0, E.deck_z) + caixa(-xl, xl, py1 - 0.01, fy1, dz0, E.deck_z) \
        + prisma([(ty0 + 0.01, dz0 - (ty0 - dky0)), (ty0 + 0.01, dz0 + 0.01), (dky0, dz0 + 0.01)], "x", -X1, X1)
    L = X0 - jw - 0.25
    misula = sim(prisma([(X0 + 0.01, dz0 - L), (X0 + 0.01, dz0 + 0.01), (X0 - L, dz0 + 0.01)], "y", ty1 - 0.01, py1))
    # língua da frente (em balanço, livre por baixo: o L298N e o BMS entram pela frente): 2 mísulas ao lado da janela +
    # cunha sob a aba da frente do servo; a face de baixo sobe a 45° a partir da frente das mísulas das paredes
    # arco em "V" invertido entre as paredes (z >= deck - |x|), que apoia a cunha a 45° sob a língua
    lam = prisma([(-X0 - 0.01, dz0 - X0), (0.0, dz0), (X0 + 0.01, dz0 - X0), (X0 + 0.01, dz0 + 0.01), (-X0 - 0.01, dz0 + 0.01)], "y", py1 - 3.0, fy1)
    cunha_ = prisma([(py1 - 3.0, dz0 - (fy1 - py1)), (py1, dz0 - (fy1 - py1)), (fy1, dz0), (fy1, dz0 + 0.01), (py1 - 3.0, dz0 + 0.01)], "x", -X0 - 0.01, X0 + 0.01)
    arco = (lam ^ cunha_) ^ (caixa(-X0 - 0.01, X0 + 0.01, py1 - 3.0, py1, 0, 400) + caixa(-xl, xl, py1 - 0.01, fy1, 0, 400))
    # --- orelhas dos micro servos dos braços (em "U" aberto em cima: o corpo do servo entra por fora, sem ponte)
    oy, oz = K.braco.eixo[0] + DY, K.braco.eixo[1]
    xo0, xo1 = e.ombro_x
    ycs = oy + mi.eixo_da_ponta - mi.corpo[0] / 2          # centro do corpo do servo (corpo para TRÁS)
    jl, jwm = mi.janela
    orelha = caixa(xo0, xo1, ycs - 18.5, ycs + 18.5, E.deck_z - 0.01, oz + 7.5) - caixa(xo0 - 1, xo1 + 1, ycs - jl / 2, ycs + jl / 2, oz - jwm / 2, 400)
    for sy in (1, -1):
        orelha = orelha - furo((xo1 + 0.5, ycs + sy * mi.furos_aba / 2, oz), (-1, 0, 0), 6, F.m2_piloto)
    # --- postes do corpo (atrás das coxas): inserto horizontal, entrando por trás
    poste_c = sim(caixa(pp.x[0] - 0.01, pp.x[1], pp.y[0] + DY, pp.y[1] + DY, Z1 - 0.01, pp.z_topo))
    # --- ressalto da esfera de apoio (atrás)
    ress = cil((0, ye, Z0), (0, ye, Z0 + 10.5), 14.5)
    # mesinha do carregador USB-C sobre o ressalto da esfera (nasce na mesa de impressão)
    ycg, zcg = e.carregador[0] + DY, e.carregador[1]
    Lc, Wc, _ = P.CARREGADOR2S.cx
    mesinha = caixa(-Wc / 2 - 2.2, Wc / 2 + 2.2, ycg - Lc / 2 - 2.2, ycg + Lc / 2 + 2.2, Z0, zcg) \
        - prisma([(ye - 10.0, Z0 - 1.0), (ye - 40.0, Z0 - 1.0), (ye - 40.0, Z0 + 29.0)], "x", -50, 50)      # atrás do ressalto a face de baixo sobe a 45° (fica dentro da cauda)
    so_c, _ = berco_modulo(P.CARREGADOR2S, alt=3.0, canto=4.0, fita=None)
    corpo = uniao(placa, paredes, travessa, deck, misula, arco, sim(orelha), poste_c, ress, mesinha, so_c.transform(_m_carregador(E)[:3, :]))

    cortes = []
    ez, t = E.eixo_roda_z, P.TT
    d0, d1 = 12.3 / 2 - 0.4, t.furos_tras_dist / 2 + 0.4
    for s in (1, -1):
        # motor TT (eixo interno, rasgos dos 2 furos de trás, furo da orelha), como em base.chassi
        cortes.append(furo((s * (X0 - 1), 0, ez), (s, 0, 0), E.parede_esp + 2, t.eixo_d + 3.0))
        for sy in (1, -1):
            cortes.append(rasgo((s * (X0 - 1), sy * d0, ez + t.furos_tras), (s * (X0 - 1), sy * d1, ez + t.furos_tras),
                                F.m3_passante, (s, 0, 0), E.parede_esp + 2))
        cortes.append(rasgo((s * (X0 - 1), 0, ez - t.furo_orelha - 1.2), (s * (X0 - 1), 0, ez - t.furo_orelha + 1.2),
                            F.m3_passante, (s, 0, 0), E.parede_esp + 2))
        # trilhos das bandejas: os 2 na parede esquerda; na direita só o de baixo (a bandeja de cima apoia no topo)
        for tz in (E.trilho_z if s < 0 else E.trilho_z[:1]):
            tr = caixa(X0 - 0.1, X0 + E.trilho_prof, py0 - 1, ty0 + 0.01, tz, tz + E.trilho_alt) \
                + prisma([(X0 - 0.1, tz + E.trilho_alt - 0.01), (X0 + E.trilho_prof, tz + E.trilho_alt - 0.01), (X0 - 0.1, tz + E.trilho_alt + E.trilho_prof + 0.1)], "y", py0 - 1, ty0 + 0.01)
            cortes.append(tr if s > 0 else espelho_x(tr))
        cortes.append(furo((s * (X0 - 1), py1 - 4.0, 40.0), (s, 0, 0), E.parede_esp + 2, 6.0))          # fios dos motores -> L298N (à frente do motor)
        cortes.append(inserto((s * (pp.x[0] + pp.x[1]) / 2, pp.y[0] + DY, pp.z_parafuso), (0, 1, 0)))
        cortes.append(furo((s * e.traseira_parafuso[0], e.traseira_parafuso[1] + DY, Z0 - 0.01), (0, 0, 1), 3.8, F.m3_piloto))
    # deck: janela do servo de pan, rasgos das abas, passagem de cabos (flat da câmera e fios da cabeça)
    cortes.append(caixa(-jw, jw, wy0, wy1, dz0 - 45, E.deck_z + 1))
    ycp = cy - s9.eixo_da_ponta + s9.corpo[0] / 2
    for sx in (1, -1):
        for sy in (1, -1):
            yy = ycp + sy * s9.furos_aba[0] / 2
            cortes.append(rasgo((sx * s9.furos_aba[1] / 2, yy - 1.5, dz0 - 12), (sx * s9.furos_aba[1] / 2, yy + 1.5, dz0 - 12), F.m3_passante, (0, 0, 1), 18))
    cortes.append(caixa(11.0, 29.0, cy + 17.5, cy + 20.0, dz0 - 25, E.deck_z + 1))          # rasgo do flat da câmera e dos fios da cabeça (18 x 2,5), à direita do servo
    # travessa: L298N (4 furos piloto pela frente) + passagens de fios
    h = P.L298N.furos / 2
    for sx in (1, -1):
        for sz in (1, -1):
            cortes.append(furo((sx * h, ty1 + 1, E.driver_z + sz * h), (0, -1, 0), 5, F.m3_piloto))
    cortes.append(furo((0, ty1 + 1, E.driver_z), (0, -1, 0), 5, 6.0))
    cortes.append(furo((0, ty1 + 1, 80.0), (0, -1, 0), 5, 8.0))
    # esfera de apoio: soquete com teto em cone + insertos da capa
    cortes.append(esfera((0, ye, P.ESFERA.d / 2), P.ESFERA.d / 2 + 0.35))
    cortes.append(cil((0, ye, P.ESFERA.d / 2 + 5.9), (0, ye, Z0 + 9.3), 5.9, 1.5))
    for sx in (1, -1):
        cortes.append(inserto((sx * 10.5, ye, Z0), (0, 0, 1)))
    # energia: berços (cantoneiras + abraçadeira) do step-down, do UBEC e do BMS; recorte da chave no piso
    somas = []
    for nome in ("stepdown", "ubec", "bms"):
        M, mod = BB.mat_modulo(E, nome)
        so, co = berco_modulo(mod, alt=4.0 if nome == "bms" else 2.4, piso=(Z1 - Z0) if nome == "bms" else E.parede_esp, canal=1.2 if nome == "bms" else 0.0)
        somas.append(so.transform(M[:3, :]))
        cortes.append(co.transform(M[:3, :]))
    kx, ky = E.chave
    rw, rh = P.CHAVE.recorte
    cortes.append(caixa(kx - rw / 2, kx + rw / 2, ky - rh / 2, ky + rh / 2, Z0 - 1, Z1 + 1))
    cortes.append(caixa(kx - rw / 2 - 3, kx + rw / 2 + 3, ky - rh / 2 - 3, ky + rh / 2 + 3, Z0 + P.CHAVE.painel, Z1 + 1))
    corpo = maior_corpo(uniao(corpo, *somas) - uniao(*cortes))
    return Peca("chassi", corpo, material="PETG", cor="grafite", grupo="corpo", macica=True, suporte="não", explode=(0, 0, 0),
                perimetros=4, infill=25, orientacao="piso na mesa (em pé)",
                reforco="mísulas a 45° e parede em V sob o deck do pan; travessa inteira do piso ao deck; paredes do rack alargadas a 45° desde o piso; postes maciços nos insertos",
                obs="piso recortado da seção da pele + rack das bandejas (atrás) + torre e deck do servo de pan + orelhas dos servos dos braços + ressalto da esfera de trás")


def _bandeja_uno(E) -> Peca:
    """Bandeja de cima: Arduino Uno + shield ATRAVESSADO (lado maior em X). Corre no trilho da parede esquerda e
    apoia no topo da parede direita, por cima da qual avança até os 2 pilares dos furos de x = +31,7."""
    w, e = E.bandeja_larg, E.bandeja_esp
    zt = E.trilho_z[1] + 0.3
    y0, y1 = E.uno_y
    m = caixa(-w / 2, K.esq.uno_x, y0, y1, zt, zt + e) + caixa(-10, 10, y0 - 4, y0 + 0.01, zt, zt + e)
    m = m - caixa(-12, 14, (y0 + y1) / 2 - 15, (y0 + y1) / 2 + 15, zt - 1, zt + e + 1)
    fs = _pos_uno(E)
    for (x, y) in fs:
        m = m + cil((x, y, zt + e - 0.01), (x, y, zt + e + K.esq.uno_espacador), 3.5, seg=24)
    for (x, y) in fs:
        m = m - furo((x, y, zt + 0.6), (0, 0, 1), K.esq.uno_espacador + e, F.m3_piloto)
    return Peca("bandeja-uno", m, material="PETG", cor="amarelo", macica=True, explode=(0, -150, 0), perimetros=4, infill=25,
                orientacao="placa na mesa, pilares para cima", reforco="placa de 3 mm; trilho na parede esquerda e apoio no topo da parede direita",
                obs="bandeja do Arduino Uno + shield, atravessado (nível de cima); sai por trás, sem a traseira; 4 M3x8 auto-atarraxantes")


def _pos_uno(E):
    return [(x - P.UNO.placa[0] / 2 + K.esq.uno_dx, E.uno_placa_y + yd) for (x, yd) in P.UNO.furos]


def _m_braco(E, lado):
    """Micro servo do braço: eixo para fora (±X), corpo para TRÁS; aba apoiada na face de fora da orelha."""
    oy, oz = K.braco.eixo[0] + K.dy, K.braco.eixo[1]
    return C.M([(0, -1, 0), (0, 0, -lado), (lado, 0, 0)], (lado * K.esq.ombro_x[1], oy, oz))


def _m_carregador(E):
    """Carregador USB-C: deitado na mesinha de trás, comprimento ao longo de Y, boca para trás."""
    return C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (0.0, K.esq.carregador[0] + K.dy, K.esq.carregador[1]))


def _comps(E):
    Z0, Z1 = E.piso_z
    T = list(E.T)
    cy = E.centro[1]
    cs = [Comp("servo-pan MG996R", C.servo_padrao().transform(C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (0, cy, E.deck_z))[:3, :]), "corpo", P.MG996R.massa, "preto"),
          Comp("servo-tilt MG996R", C.servo_padrao().transform(BS.M_tilt()[:3, :]).translate(T), "cabeca", P.MG996R.massa, "preto"),
          Comp("servo-braco-dir", C.micro_servo().transform(_m_braco(E, 1)[:3, :]), "corpo", P.MICRO.massa, "azul"),
          Comp("servo-braco-esq", C.micro_servo().transform(_m_braco(E, -1)[:3, :]), "corpo", P.MICRO.massa, "azul")]
    for lado, nm in ((1, "dir"), (-1, "esq")):
        cs.append(Comp(f"motor-tt-{nm}", C.motor_tt(encoder=E.encoder_extra).transform(BS.M_motor(lado)[:3, :]), "corpo", P.TT.massa, "amarelo"))
        r = C.roda().translate([E.x_roda, 0, E.eixo_roda_z])
        cs.append(Comp(f"roda-{nm}", r if lado > 0 else espelho_x(r), "corpo", P.RODA.massa, "preto"))
    cs.append(Comp("esfera-apoio", C.esfera_apoio().translate([0, E.esferas[0][1], P.ESFERA.d / 2]), "corpo", P.ESFERA.massa, "prata"))
    cs.append(Comp("bateria 2x18650", C.bateria().translate([0, E.bateria_y, Z1]), "corpo", P.BATERIA.massa_suporte + 2 * P.BATERIA.massa_celula, "prata"))
    cs.append(Comp("driver L298N", C.driver().translate([0, E.travessa_y[1] + 3.0, E.driver_z]), "corpo", P.L298N.massa, "prata"))
    for nome, rot_ in (("stepdown", "step-down 5V (LM2596)"), ("ubec", "ubec 6V 3A"), ("bms", "bms 2S")):
        M, mod = BB.mat_modulo(E, nome)
        cs.append(Comp(rot_, C.modulo(mod).transform(M[:3, :]), "corpo", mod.massa, "azul"))
    cs.append(Comp("carregador USB-C 2S", C.modulo(P.CARREGADOR2S).transform(_m_carregador(E)[:3, :]), "corpo", P.CARREGADOR2S.massa, "azul"))
    cs.append(Comp("chave", C.chave().translate([E.chave[0], E.chave[1], Z0]), "corpo", 3.0, "preto"))
    e = E.bandeja_esp + E.espacador
    zP, zU = E.trilho_z[0] + 0.3 + e, E.trilho_z[1] + 0.3 + E.bandeja_esp + K.esq.uno_espacador
    pi = C.placa_eletronica(P.PI).transform(C.M([(0, -1, 0), (1, 0, 0), (0, 0, 1)], (-P.PI.placa[1] / 2, E.pi_placa_y, zP))[:3, :])
    uno = C.placa_eletronica(P.UNO).translate([-P.UNO.placa[0] / 2 + K.esq.uno_dx, E.uno_placa_y, zU])
    cs.append(Comp("Raspberry Pi 4/5", pi, "corpo", P.PI.massa, "verde"))
    cs.append(Comp("Arduino Uno + shield", uno, "corpo", P.UNO.massa + 20, "azul"))
    return cs


def _obstaculos(E, chassi_solido, outros, folga=0.6):
    """O que o corpo tem de contornar ao DESCER por cima do chassi já com rodas, motores e servos. O corpo do dino
    estreita para cima: a sombra é calculada em fatias finas (cada fatia só vê o que o chassi tem ACIMA dela), senão
    a casca seria cortada também acima das paredes."""
    Z0, Z1 = E.piso_z
    niv = [-5.0, Z1 + 0.2, Z0 + 10.5 + 0.2] + [float(z) for z in np.arange(24.0, E.z_gola + 12.0, 5.0)]
    partes = [BB.sombra_abaixo(chassi_solido, niv, folga)]
    for m in outros:                                    # componentes montados antes do corpo
        topo = m.bounding_box()[5]
        partes.append(BB.sombra_abaixo(m, [-5.0] + [float(z) for z in np.arange(20.0, topo, 8.0)] + [topo + 0.3], folga + 0.4))
    r = P.RODA.d / 2 + 2.5
    xa, xb = E.x_roda - 2.5, E.x_roda + P.RODA.larg + 2.5
    partes.append(sim(cil((xa, 0, E.eixo_roda_z), (xb, 0, E.eixo_roda_z), r, seg=64) + caixa(xa, xb, -r, r, -5.0, E.eixo_roda_z)))
    return uniao(*partes)


# ====================================================================== modelo
def construir() -> Modelo:
    pecas, comps = [], []
    E = BB.esqueleto(K)
    C0 = np.array(E.centro)
    T = E.T                                            # pescoço padrão de base.py -> pescoço deste bicho
    DY = K.dy
    dyv = np.array([0.0, DY, 0.0])
    r_gola = K.soquete_r - K.folga_junta
    r_gola_in = r_gola - F.parede - 1.0
    z_top = float(C0[2] + np.sqrt(r_gola_in ** 2 - K.gola_boca_r ** 2))     # a boca de cima da gola tem gola_boca_r de raio
    zb = float(C0[2] + K.cabeca_z)
    yd = K.costura_y + DY
    cr, br = K.crista, K.braco
    R = CA.Regiao

    # ------------------------------------------------------------ pele: boca fechada, coxas que cobrem as rodas, cortina
    base = CA.carregar(K.pele, dy=DY)
    Pg = base.P
    eixo_roda = (0.0, P.RODA.d / 2)
    lo_c, hi_c = (_v(v, dyv) for v in K.cortina)
    lo_b, hi_b = (_v(v, dyv) for v in K.boca_vao)

    def campo_cheia(Pp, Fp):
        d = CA.fechar_vao_z(base, Fp, lo_b, hi_b)
        Pa = Pp.copy()
        Pa[..., 0] = np.abs(Pa[..., 0])
        d = smin(d, CA.cil_x_redondo(Pa, eixo_roda, K.coxa.r, K.coxa.x[0], K.coxa.x[1], K.coxa.arred), 6.0)
        return CA.autoportante(base, d, lo_c, hi_c, cos45=0.0)

    cheia = base.combinar(campo_cheia)                 # pele "cheia": com os espinhos da crista

    def caixas_crista(o):
        return [((lo[0] + o[1], lo[1] + o[2]), (hi[0] + o[1], hi[1] + o[2])) for (lo, hi) in (cr.cabeca, cr.costas, cr.nuca)]

    def campo_lisa(Pp, Fp):
        d = Fp
        for lo, hi in caixas_crista(dyv):
            d = CA.sem_crista(base, d, cr.xc, lo, hi)
        return d

    lisa = cheia.combinar(campo_lisa)                  # sem os espinhos (viram lâminas azuis)

    # ------------------------------------------------------------ cabeça e zona varrida (pan x tilt x boca)
    H = CA.campo_cabeca(cheia, C0, K.soquete_r, zb)
    bo = _boca(DY, 0.0)
    z_boca = bo["z0"] + bo["incl"] * (Pg[..., 1] - bo["y_ref"]) + 8.0
    eixo_boca = (0.0, bo["y_eixo"], bo["z_eixo"])
    angs_boca = np.linspace(0.0, K.boca_abre, 5)
    Hj = np.maximum(np.maximum(H, bo["y_corte"] - Pg[..., 1]), Pg[..., 2] - z_boca)
    for th in angs_boca:
        Cth = (mat_giro(eixo_boca, (-1, 0, 0), -th) @ np.array([*C0, 1.0]))[:3].astype(np.float32)
        Hj = np.maximum(Hj, K.soquete_r + 0.5 - np.linalg.norm(Pg - Cth, axis=-1))
    H = np.minimum(H, CA.reamostrar(base, Hj, mat_giro(eixo_boca, (-1, 0, 0), K.boca_abre)))
    pans = np.arange(N.pan[0], N.pan[1] + 0.1, 7.5)
    tilts = np.unique(np.concatenate([np.linspace(N.tilt[0], 0, 3), np.linspace(0, N.tilt[1], 3)]))
    S = CA.zona_varrida(base, H, C0, pans, tilts, (-95, C0[1] - 115, 100), (95, C0[1] + 70, z_top + 14), chave=f"{K.pele}|{DY}|{K.soquete_r}|{zb}")
    del H, Hj
    p_livre = cheia.combinar(lambda Pp, Fp: np.maximum(Fp, K.folga_junta - S))      # pele fora da zona varrida (a barriga sobe até onde a cabeça não passa)

    # ------------------------------------------------------------ peças em relevo e assentos (regiões no robô)
    lo, hi = (_v(v, dyv) for v in K.barriga.caixa)
    rel = {"barriga": CA.Relevo(R.caixa(lo, hi), (0, K.barriga.plano_y + DY, 95), (0, 1, 0))}
    for s, lado in ((1, "dir"), (-1, "esq")):
        for i, (c, n) in enumerate(K.dedos):
            c_, n_ = _v(c, dyv) * (s, 1, 1), np.asarray(n, float) * (s, 1, 1)
            rel[f"dedo-{lado}-{i + 1}"] = CA.Relevo(R.cil(c_ - n_ * 4.0, c_ + n_ * 30.0, K.dedo_r), c_, n_)
        mc = K.mancha
        cm = np.array([s * mc.x, mc.c[0] + DY, mc.c[1]])
        rel[f"mancha-{lado}"] = CA.Relevo(R.cil(cm - (s * 8.0, 0, 0), cm + (s * 25.0, 0, 0), mc.r), cm, (s, 0, 0))
    assentos = []                                      # o relevo dos braços da malha sai (entram os braços que giram)
    for s in (1, -1):
        lo, hi = (_v(v, dyv) * (s, 1, 1) for v in br.ombro)
        assentos.append(CA.Relevo(R.caixa(np.minimum(lo, hi), np.maximum(lo, hi)), (s * (br.x_base - 0.5), 0, 0), (s, 0, 0), folga=0.0))
        lo, hi = (_v(v, dyv) * (s, 1, 1) for v in br.mao)
        n_ = np.asarray(br.mao_n, float) * (s, 1, 1)
        assentos.append(CA.Relevo(R.caixa(np.minimum(lo, hi), np.maximum(lo, hi)), _v(np.asarray(br.mao_n, float) * br.mao_d, dyv) * (s, 1, 1), n_, folga=0.0))

    # braços que giram: blobs (no robô), face de dentro plana em x_base; o corpo se afasta 2 mm do que eles varrem
    oy, oz = br.eixo[0] + DY, br.eixo[1]
    blobs = [(tuple(_v(c, dyv)), r) for (c, r) in br.blobs]
    f_braco = campo_blobs(blobs, 8.0)
    sl_b = CA._fatia(base, (br.x_base - 14, oy - 50, oz - 50), (br.x_base + 30, oy + 60, oz + 50))
    Pb = base.P[sl_b]
    varre = np.full(Pb.shape[:3], 99.0, np.float32)
    for th in np.radians(np.linspace(br.lim[0], br.lim[1], 12)):
        c_, s_ = np.cos(th), np.sin(th)
        Q = np.stack([Pb[..., 0], oy + (Pb[..., 1] - oy) * c_ + (Pb[..., 2] - oz) * s_, oz - (Pb[..., 1] - oy) * s_ + (Pb[..., 2] - oz) * c_], axis=-1)
        varre = np.minimum(varre, f_braco(Q.astype(np.float32)))
    varre = np.maximum(varre, (br.x_base - 1.0) - Pb[..., 0])      # o braço de verdade só existe de x_base para fora (o blob inteiro abriria um bolso no ombro)
    nx = len(base.eixos[0])
    sl_e = (slice(nx - sl_b[0].stop, nx - sl_b[0].start), sl_b[1], sl_b[2])          # o mesmo bloco, espelhado em X

    # ------------------------------------------------------------ corpo = pele lisa + esfera da gola - zona varrida - assentos
    def campo_corpo(Pp, Fp):
        d = np.minimum(Fp, np.linalg.norm(Pp - C0.astype(np.float32), axis=-1) - r_gola)
        d = np.maximum(np.maximum(d, K.folga_junta - S), Pp[..., 2] - (z_top + 6.0))
        d = CA.tirar_farelos(base, d, 2.5, K.z_gola - 14.0)
        for r_ in list(rel.values()) + assentos:
            d = r_.tirar(Pp, d)
        d[sl_b] = np.maximum(d[sl_b], 2.0 - varre)
        d[sl_e] = np.maximum(d[sl_e], 2.0 - varre[::-1])
        return d

    p_corpo = lisa.combinar(campo_corpo)
    ext = p_corpo.solido()
    inte = p_corpo.deslocado(-F.parede)
    casca = ext - inte
    chassi = _chassi(E, p_corpo, p_corpo.deslocado(-(F.parede + 0.7)))
    v, pt = CA.sobra(p_corpo, chassi.solido ^ caixa(-200, 200, -400, 400, E.piso_z[1] + 8.0, 400))
    if v > -(F.parede + 0.5):
        print(f"  AVISO: o chassi chega a {v:+.1f} mm da pele em {np.round(pt, 0)} (tem de ser <= {-(F.parede + 0.5):.1f})")

    # ------------------------------------------------------------ corpo (frente) + traseira (anca e cauda)
    comps_esq = _comps(E)
    antes = ("driver", "motor", "step", "ubec", "servo-pan", "servo-braco", "chave")
    obst = _obstaculos(E, chassi.solido, [c.solido for c in comps_esq if c.nome.startswith(antes)])
    corpo = maior_corpo((CA.fatia_z(casca, K.z_fundo, K.z_gola) - obst) ^ caixa(-400, 400, yd, 400, -50, 400))
    tras = maior_corpo(casca ^ caixa(-400, 400, -400, yd - F.encaixe, -50, K.z_gola))
    ye = E.esferas[0][1]
    c_car = [c.solido for c in comps_esq if c.nome.startswith("carregador")][0]
    obst_t = (chassi.solido ^ caixa(-400, 400, -400, yd + 3.0, -50, 400)) + cil((0, ye, -5.0), (0, ye, E.piso_z[0] + 10.5 + 0.6), 14.5) + c_car
    tras = maior_corpo(tras - CA.sombra_frente(obst_t, list(np.arange(yd - 140.0, yd + 2.6, 2.5)), 0.6))
    tras = tras + (ext ^ cil((0.0, yd - 104.0, 58.0), (0.0, yd - 164.0, 58.0), 0.05, 60.0))          # ponta da cauda maciça, em cone de 45° (sem teto na impressão em pé)
    # carregador USB-C: o plugue entra por trás, por um rasgo sob a raiz da cauda
    ycg, zcg = K.esq.carregador[0] + DY, K.esq.carregador[1]
    tras = tras - caixa(-6.5, 6.5, yd - 160.0, ycg - P.CARREGADOR2S.cx[0] / 2 + 1.0, zcg + 0.2, zcg + 7.5)
    # lábio do corpo: faixa por dentro da borda de trás que entra 5 mm na traseira e a alinha
    labio = (p_corpo.deslocado(-(F.parede + F.encaixe)) - p_corpo.deslocado(-(F.parede + F.encaixe + 1.6))) ^ caixa(-400, 400, yd - 5.0, yd + 6.0, 30.0, K.z_gola - 6.0)
    corpo = corpo + (labio - obst - caixa(-cr.esp / 2 - F.parede - 1.0, cr.esp / 2 + F.parede + 1.0, yd - 6.0, yd, 60.0, 400.0))
    # 2 M3 horizontais, por trás, prendem o corpo nos postes do chassi (as abas ficam cobertas pela traseira)
    pp = K.esq.poste
    xp = (pp.x[0] + pp.x[1]) / 2
    for sx in (1, -1):
        xa, xb = sorted((sx * (pp.x[0] + 0.7), sx * 200.0))
        aba = caixa(xa, xb, yd, pp.y[0] + DY - 0.3, K.z_fundo, pp.z_topo - 2.0) ^ ext
        corpo = corpo + aba - cil((sx * xp, yd - 5, pp.z_parafuso), (sx * xp, yd + 12, pp.z_parafuso), F.m3_passante / 2, seg=24)
        # ombro: furo por onde o cubo do braço chega ao horn do micro servo
        corpo = corpo - cil((sx * 30.0, oy, oz), (sx * 90.0, oy, oz), br.r_furo)
    # colarinho maciço por dentro da borda de cima, na metade de trás (onde as costas fecham para o pescoço): a face de baixo
    # é um cone a 45° que nasce na parede; sem teto em balanço
    zc_ = K.z_gola - 0.05
    colar = (cil((C0[0], C0[1], zc_ - 54.0), (C0[0], C0[1], zc_), 95.0) - cil((C0[0], C0[1], zc_ - 54.01), (C0[0], C0[1], zc_ + 0.01), K.gola_boca_r + 54.5, K.gola_boca_r + 0.5)) \
        ^ ext ^ caixa(-400, 400, yd + 0.4, C0[1] - 15.0, -50, 400)
    corpo = corpo + colar
    # gola: 3 ressaltos por dentro da borda de cima do corpo, com inserto vertical; a face de baixo sobe a 45° até a parede
    rg_, angs_g = K.esq.gola_ressalto
    zt_ = K.z_gola - 0.05
    pos_g = []
    for ang in angs_g:
        res = prisma([(C0[1] + rg_ - 4.0, zt_), (C0[1] + rg_ + 30.0, zt_), (C0[1] + rg_ + 30.0, zt_ - 42.0), (C0[1] + rg_ - 4.0, zt_ - 8.0)], "x", -4.5, 4.5)
        res = girar(res, (0.0, C0[1], 0.0), (0, 0, 1), ang) ^ ext ^ caixa(-400, 400, yd + 0.4, 400, -50, 400)
        pg_ = (-rg_ * np.sin(np.radians(ang)), C0[1] + rg_ * np.cos(np.radians(ang)))
        pos_g.append(pg_)
        corpo = corpo + res - inserto((pg_[0], pg_[1], zt_), (0, 0, -1))
    # traseira: 2 M3 auto-atarraxantes POR BAIXO (cabeça abaulada para fora, 2 mm abaixo do fundo), no piso do chassi
    tx, ty = K.esq.traseira_parafuso[0], K.esq.traseira_parafuso[1] + DY
    for sx in (1, -1):
        zs_ = float(p_corpo.ponto_na_pele((sx * tx, ty, -30.0), (0, 0, 1))[2])
        tras = tras + (cil((sx * tx, ty, zs_ - 1.0), (sx * tx, ty, E.piso_z[0] - 0.2), 4.6) ^ ext) - cil((sx * tx, ty, -5), (sx * tx, ty, E.piso_z[0]), F.m3_passante / 2, seg=24)

    # ------------------------------------------------------------ crista das costas (lâmina azul na traseira)
    def crista(caixa_yz, livre, corte_ext):
        lo_, hi_ = caixa_yz
        pol = CA.lamina_crista(cheia, lisa.F, lo_, hi_, cr.fundo, livre=livre)
        pol = CA.maior_poligono(pol)
        faixa = CA.lamina_crista(lisa, lisa.F, (lo_[0] - 2, lo_[1] - 2), (hi_[0] + 2, hi_[1] + 2), cr.fundo + F.parede + 0.6)
        lam = CA.extrudar_x(pol, cr.esp / 2)
        rasgo_ = CA.extrudar_x(pol.buffer(F.encaixe, join_style=2), cr.esp / 2 + F.encaixe)
        nerv = CA.extrudar_x(faixa.intersection(pol.buffer(F.parede + 0.6, join_style=2)), cr.esp / 2 + F.encaixe + F.parede) ^ corte_ext
        return lam, rasgo_, nerv

    cx_cab, cx_cos, _ = caixas_crista(dyv)
    lam_c, rg, nv = crista(cx_cos, S - K.folga_junta, ext ^ caixa(-400, 400, -400, yd - F.encaixe, -50, K.z_gola))
    tras = maior_corpo(tras + nv - rg)
    del S

    # ------------------------------------------------------------ gola (esfera do pescoço)
    zg = K.z_gola + F.encaixe
    gola = CA.fatia_z(ext, zg, z_top) - esfera(C0, r_gola_in, seg=128)
    gola = gola - cil((C0[0], C0[1], zg - 1.0), tuple(C0), K.gola_boca_r - 0.5, seg=128)      # por baixo a boca tem o mesmo raio da de cima: a gola desce por cima do garfo
    for sx in (1, -1):                                  # acima dos ombros a face de baixo da gola sobe a 45° (o corpo foi afastado do que o braço varre)
        gola = gola - (prisma([(sx * (br.x_base - 0.4), zg - 1.0), (sx * (br.x_base + 40.0), zg - 1.0), (sx * (br.x_base + 40.0), zg + 40.4)], "y", br.ombro[0][1] + DY, br.ombro[1][1] + DY))      # só na faixa do assento plano do ombro (fora dela a borda do corpo ficaria descoberta)
    for sx in (1, -1):                                  # tampa sobre o ombro: o corte z_gola passa pelo alto da saliência do ombro, que é oca; sem ela ficava uma fresta aberta para dentro
        xa, xb = sorted((sx * (K.gola_boca_r + 2.0), sx * (br.x_base - 0.5)))
        gola = gola + caixa(xa, xb, br.ombro[0][1] + DY, br.ombro[1][1] + DY, zg, zg + 2.4)
    gola = maior_corpo(gola)
    for (gx, gy) in pos_g:                               # 3 M3 por cima: furo passante + rebaixo fundo (a chave entra pela boca da gola)
        gola = gola - cil((gx, gy, zg - 1), (gx, gy, zg + 4), F.m3_passante / 2, seg=24) - cil((gx, gy, zg + 3.0), (gx, gy, zg + 32.0), F.cabeca_m3_d / 2 + 0.2, seg=24)

    # ------------------------------------------------------------ peças em relevo (barriga e dedos creme) e braços
    pc = {nm: r_.peca(p_livre if nm == "barriga" else cheia) for nm, r_ in rel.items()}
    creme = dict(cor="creme", macica=True, suporte="não", orientacao="base plana (face de colar) na mesa")
    pecas.append(Peca("barriga", pc["barriga"], imprimir=rel["barriga"].imprimir, explode=(0, 110, 0), obs="barriga creme; cola no assento plano do corpo", **creme))
    for nm in rel:
        if nm.startswith("dedo"):
            d_ = maior_corpo(pc[nm] - caixa(-400, 400, -400, 400, -50, 2.0) - obst)
            pecas.append(Peca(nm, d_, imprimir=rel[nm].imprimir, explode=(40 if "dir" in nm else -40, 70, 0), obs="dedo do pé; cola", **creme))
    # sensores de distância laterais (fase 2) atrás das 2 manchas verde-escuras dos flancos
    mc = K.mancha
    xb_ = mc.x - 0.25 - F.parede - 0.6
    for sx, lado in ((1, "dir"), (-1, "esq")):
        ym, zm_ = mc.c[0] + DY, mc.c[1]
        jan = cil((sx * (mc.x - 8.0), ym, zm_), (sx * (mc.x + 30.0), ym, zm_), P.TOF.janela_d / 2, seg=24)
        corpo = corpo - jan
        pecas.append(Peca(f"mancha-{lado}", maior_corpo(pc[f"mancha-{lado}"] - jan), cor="verde-escuro", macica=True, suporte="não", imprimir=rel[f"mancha-{lado}"].imprimir,
                          explode=(sx * 110, 0, 0), orientacao="base plana (face de colar) na mesa",
                          obs="mancha do flanco: janela do sensor de distância lateral (fase 2); cola no assento plano do corpo"))
        cx_ = caixa(xb_ - P.TOF.esp, xb_, ym - P.TOF.placa[0] / 2, ym + P.TOF.placa[0] / 2, zm_ - P.TOF.placa[1] / 2, zm_ + P.TOF.placa[1] / 2)
        comps.append(Comp(f"tof-{lado} (fase 2)", cx_ if sx > 0 else espelho_x(cx_), "corpo", P.TOF.massa, "verde", fase2=True))

    p_br = BI.pele_blobs(blobs, k=8.0, h=1.0)
    hl, hd, hp, he = P.MICRO.horn
    xh0 = br.x_ponta - he - 0.2                          # face de dentro do horn
    xs1 = br.x_base + br.encaixe                         # fundo do encaixe do cubo dentro do braço
    chato = lambda fol: caixa(-200, 200, oy - 50, oy + 50, oz - 6.5 - fol, oz + 6.5 + fol)        # o cubo tem 2 faces chatas (não gira dentro do braço)
    braco = maior_corpo(p_br.solido() ^ caixa(br.x_base, 300, -400, 400, -50, 400))
    braco = braco - (cil((br.x_base - 1, oy, oz), (xs1 + 0.3, oy, oz), br.r_cubo + 0.15) ^ chato(0.15))
    cubo = cil((xh0, oy, oz), (br.x_base - 0.3, oy, oz), br.r_cubo) + (cil((br.x_base - 0.31, oy, oz), (xs1, oy, oz), br.r_cubo) ^ chato(0.0))
    cubo = cubo - casco(cil((xh0 - 0.1, oy, oz), (br.x_ponta + 0.4, oy, oz), hd / 2 + 0.3, seg=24),
                        cil((xh0 - 0.1, oy + hl, oz), (br.x_ponta + 0.4, oy + hl, oz), hp / 2 + 0.3, seg=24))
    cubo = cubo - cil((xh0, oy, oz), (xs1 + 1, oy, oz), 1.4, seg=12) - cil((br.x_ponta + 3.0, oy, oz), (xs1 + 1, oy, oz), 2.9, seg=16)
    verde = dict(cor="verde", macica=True, suporte="não", perimetros=3, infill=20, orientacao="face de dentro (plana) na mesa")
    pecas += [
        Peca("braco-dir", braco, grupo="braco_d", imprimir=rot("y", -90), explode=(70, 20, 0),
             obs="braço direito; encaixa por pressão no cubo (2 faces chatas), sem parafuso por fora", **verde),
        Peca("braco-esq", espelho_x(braco), grupo="braco_e", imprimir=rot("y", 90), explode=(-70, 20, 0), obs="braço esquerdo", **verde),
        Peca("cubo-braco", cubo, material="PETG", cor="grafite", macica=True, imprimir=rot("y", 90), copias=[np.eye(4), ESP.copy()], grupos=["braco_d", "braco_e"],
             explode=(55, 20, 0), suporte="não", perimetros=4, infill=60, orientacao="ponta de fora (2 faces chatas) na mesa, rebaixo do horn para cima",
             reforco="maciço em volta do rebaixo do horn",
             obs="cubo do braço: entra pelo furo do ombro, abraça o horn do micro servo e é preso pelo parafuso central do servo (fica escondido pelo braço)"),
    ]

    # a base de cada vaso tem de sair PLANA: desfaz arestas beliscadas aqui e refaz o corte da base
    corpo, gola = (maior_corpo(CA.fatia_z(desbeliscar(limpar(m)), z0, 900.0)) for m, z0 in ((corpo, K.z_fundo), (gola, zg)))
    tras = maior_corpo(desbeliscar(limpar(tras)) ^ caixa(-400, 400, -400, yd - F.encaixe, 3.0, 400))      # nada abaixo de z=3 (o fundo da pele fica em z=4; a cortina do corpo deixava uma lasca na costura)
    pecas += [
        Peca("corpo", corpo, cor="verde", explode=(0, 0, 60), perimetros=4, infill=15, suporte="sim (árvore POR DENTRO: teto das 2 coxas, sobre as rodas; degraus de dentro dos assentos planos (barriga, braços, manchas); por fora nada)",
             orientacao="borda de baixo (z=5) na mesa, em pé como um vaso; boca (z=134) para cima",
             reforco="2 abas maciças atrás (M3 horizontal nos postes do chassi); lábio por dentro da borda de trás; colarinho maciço atrás e 3 ressaltos com inserto na borda de cima; 4 perímetros porque o corpo é aberto atrás",
             obs="pernas, barriga e peito; desce por cima do chassi; 2 M3 por trás (cobertos pela traseira); a borda de trás encaixa na traseira"),
        Peca("traseira", tras, cor="verde", imprimir=rot("x", -90), explode=(0, -140, 0), perimetros=4, infill=15,
             suporte="sim (árvore POR DENTRO: teto de cima da anca (53° da vertical) e nervura do rasgo da crista; por fora nada)",
             orientacao="borda da frente (plano da costura) na mesa, cauda para cima",
             reforco="nervura por dentro ao longo do rasgo da crista; 2 almofadas nos parafusos de baixo; ponta da cauda maciça em cone",
             obs="anca + cauda: sai para trás e dá acesso à bateria e às bandejas sem tirar a cabeça; 2 M3 auto-atarraxantes por baixo"),
        Peca("gola", gola, cor="verde", suporte="não", explode=(0, 0, 100), perimetros=4, infill=20,
             orientacao="base (z=134) na mesa; a esfera sobe e fica aberta em cima",
             reforco="maciça entre a esfera e a pele de fora (sem teto em balanço); 3 furos M3 com rebaixo fundo",
             obs="gola: esfera em que a cabeça gira; assenta na borda do corpo; 3 M3 por cima, nos ressaltos do corpo (por dentro, antes da cabeça)"),
        Peca("crista-costas", lam_c, cor="azul", imprimir=rot("y", 90), macica=True, explode=(0, -190, 30), suporte="não",
             orientacao="deitada (lâmina de 6 mm)", obs="crista das costas e da raiz da cauda; pressão ou cola no rasgo da traseira"),
    ]

    # ------------------------------------------------------------ cabeça (construída no referencial do pescoço padrão)
    ds = np.array([0.0, DY - T[1], -T[2]])             # pele -> referencial padrão
    p_cab0 = CA.carregar(K.pele, dy=ds[1], dz=ds[2]).recortar((-200, -400, BS.CZ + K.cabeca_z - 12.0), (200, 400, 600))
    lo_b, hi_b = (_v(v, ds) for v in K.boca_vao)
    p_cab_cheia = p_cab0.combinar(lambda Pp, Fp: CA.fechar_vao_z(p_cab0, Fp, lo_b, hi_b))
    (lo_k, hi_k), _, (lo_n, hi_n) = caixas_crista(ds)
    p_cab = p_cab_cheia.combinar(lambda Pp, Fp: CA.sem_crista(p_cab0, CA.sem_crista(p_cab0, Fp, cr.xc, lo_k, hi_k), cr.xc, lo_n, hi_n))
    boca = _boca(ds[1], ds[2])
    cran, mand, c_ext, c_int = BI.cabeca(p_cab, boca, r_soquete=K.soquete_r, cabeca_z=K.cabeca_z, recuo=0.5)
    # ponta do queixo maciça à frente de um plano a 45°: a mandíbula imprime de pé (plano de trás na mesa) e a cavidade fecha sem teto
    zpl_ = boca["z0"] - boca["folga"] / 2
    acima = girar(caixa(-200, 200, -300, 300, zpl_, zpl_ + 200), (0, boca["y_ref"], zpl_), (1, 0, 0), float(np.degrees(np.arctan(boca["incl"]))))
    ym_, zm0_ = K.boca_macico[0] + ds[1], K.boca_macico[1] + ds[2]
    cunha_q = prisma([(ym_, zm0_ - 60.0), (ym_, zm0_), (ym_ + 90.0, zm0_ + 90.0), (ym_ + 300.0, zm0_ + 90.0), (ym_ + 300.0, zm0_ - 60.0)], "x", -200, 200)
    mand = mand + (((c_ext - acima) ^ caixa(-200, 200, boca["y_corte"], 400, 0, 500)) ^ cunha_q)
    for th in angs_boca:                                # alívio da mandíbula: a esfera do soquete vista por ela em cada ângulo de abertura
        mand = mand - esfera((BS.CX, BS.CY, BS.CZ), K.soquete_r + 0.5, seg=96).transform(mat_giro((0.0, boca["y_eixo"], boca["z_eixo"]), (-1, 0, 0), -th)[:3, :])
    # canto de trás da mandíbula, acima do eixo: ao abrir ele recua; chanfro que acompanha a abertura máxima (+3°)
    tb = np.tan(np.radians(K.boca_abre + 3.0))
    mand = mand - prisma([(boca["y_corte"] - 8.0, boca["z_eixo"]), (boca["y_corte"], boca["z_eixo"]), (boca["y_corte"] + 40.0 * tb, boca["z_eixo"] + 40.0), (boca["y_corte"] - 8.0, boca["z_eixo"] + 40.0)], "x", -200, 200)
    mand = maior_corpo(mand)
    o = K.olho
    olhos, iris, pups = [], [], []
    # olho direito = câmera (Camera Module 3 Wide), olho esquerdo = ToF: decisão (b), a mesma da capivara (decisions.md)
    cam_furos = [(sx * P.CAMERA.furos[0] / 2, yy) for sx in (1, -1) for yy in (10.0, 10.0 - P.CAMERA.furos[1])]
    comps_olho, imp_olho, c_olhos = [], [], []
    for s, placa, furo_d, furos in ((1, P.CAMERA.placa, P.CAMERA.lente_d + 1.0, cam_furos), (-1, P.TOF.placa, P.TOF.janela_d, ())):
        c_o, d_o = _v(o.c, ds) * (s, 1, 1), np.asarray(o.dir, float) * (s, 1, 1)
        c_olhos.append(c_o)
        cran, ol, ir, pu, Mo = BI.olho_sensor(c_o, o.r, d_o, o.iris_r, o.pupila_r, cran, c_ext, placa, furo_d, furos)
        olhos.append(ol), iris.append(ir), pups.append(pu)
        imp_olho.append(CA.mat_imprimir_base(d_o))
        if s > 0:
            Mk = Mo.copy()
            Mk[:3, 1], Mk[:3, 2] = Mo[:3, 2], Mo[:3, 1]                      # câmera: placa em XZ local, lente em +Y
            Mk[:3, 3] = Mo[:3, 3] - Mo[:3, 2] * 1.2
            comps_olho.append(Comp("camera olho direito (fase 2)", C.camera().transform(Mk[:3, :]), "cabeca", 4.0, "verde", fase2=True))
        else:
            w_, h_ = P.TOF.placa
            comps_olho.append(Comp("tof-olho esquerdo (fase 2)", caixa(-w_ / 2, w_ / 2, -h_ / 2, h_ / 2, -P.TOF.esp, 0).transform(Mo[:3, :]),
                                   "cabeca", P.TOF.massa, "verde", fase2=True))
    cran = maior_corpo(cran)
    cran, mand, mesa, comps_cab, M_bucha = BI.mecanica_cabeca(p_cab, cran, mand, c_ext, c_int, boca, zcam=0.0, camera=False, aparar_r=K.soquete_r,
                                                              eixo_oculto=True, sem_ponte=True, sondas=K.boca_sondas, servo_em_pe=True)
    comps_cab += comps_olho
    # microfones (fase 2) atrás das 2 narinas: furo de som Ø2 + anel por dentro da casca, onde a plaquinha redonda encaixa
    for s, lado in ((1, "dir"), (-1, "esq")):
        ps = np.asarray(p_cab.ponto_na_pele((s * K.narina.x, K.narina.y + ds[1], BS.CZ + 250.0), (0, 0, -1)), float)
        n_ = CA.normal(p_cab, ps, 3.0)
        a0, a1 = ps - n_ * (F.parede - 0.3), ps - n_ * (F.parede + P.MIC.esp + 1.6)
        cran = cran + (cil(a0, a1, P.MIC.d / 2 + 2.0) - cil(a0 + n_ * 5.0, a1 - n_, P.MIC.d / 2 + 0.3))
        cran = cran - cil(ps + n_ * 3.0, ps - n_ * 10.0, P.MIC.furo_som / 2, seg=16)
        comps_cab.append(Comp(f"microfone-{lado} (fase 2)", cil(ps - n_ * (F.parede + 1.3), ps - n_ * (F.parede + 1.3 + P.MIC.esp), P.MIC.d / 2), "cabeca", P.MIC.massa, "verde", fase2=True))
    # alto-falante (fase 2) em cima da mesa da cabeça, virado para baixo: o som sai pela boca e pelo vão do pescoço
    zmt = BS.CZ + N.mesa_z + N.mesa_esp
    xsf, ysf, rf = K.falante[0], K.falante[1] + ds[1], P.FALANTE.d / 2
    mesa = mesa + (cil((xsf, ysf, zmt - N.mesa_esp), (xsf, ysf, zmt), rf + 2.6) ^ p_cab.deslocado(-F.parede - 1.2))
    mesa = mesa - cil((xsf, ysf, zmt - N.mesa_esp - 0.01), (xsf, ysf, zmt + 1), rf - 2.0) - cil((xsf, ysf, zmt - 2.5), (xsf, ysf, zmt + 0.01), rf - 2.0, rf + 0.6)
    mesa = mesa - caixa(-29.0, -11.0, BS.CY + 4.0, BS.CY + 10.0, zmt - N.mesa_esp - 1, zmt + 1)      # os cabos sobem aqui (o alto-falante cobre o rasgo do meio)
    comps_cab.append(Comp("alto-falante (fase 2)", C.falante().transform(C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (xsf, ysf, zmt - 0.55))[:3, :]),
                          "cabeca", P.FALANTE.massa, "preto", fase2=True))
    for c_o in c_olhos:                                 # as orelhas crânio -> mesa nascem depois dos olhos: reabrir o lugar do olho
        cran = cran - esfera(c_o, o.r + F.encaixe / 2, seg=64)
    cran = maior_corpo(cran)
    # nada da mandíbula (almofadas do eixo incluídas) passa do plano da boca
    mand = maior_corpo(mand - acima - cran - cran.translate([0, 0, -0.6]))
    Tl = list(T)
    for c in comps_cab:
        c.solido = c.solido.translate(Tl)
    comps += comps_cab
    g = lambda m: m.translate(Tl)
    # crista da cabeça (lâmina azul): rasgo + nervura no crânio, já no robô
    lam_h, rg, nv = crista(cx_cab, None, g(c_ext) - esfera(C0, K.soquete_r + 0.3, seg=96))
    lam_h = lam_h - esfera(C0, K.soquete_r + 1.0, seg=96)
    cran_r = maior_corpo(g(cran) + nv - rg)
    pecas += [
        Peca("cranio", cran_r, cor="verde", grupo="cabeca", explode=(0, 0, 150), perimetros=3, infill=15,
             suporte="sim (árvore POR DENTRO: teto do crânio, fundo dos copos dos olhos e nervura da crista; e por baixo, fora do rosto: borda do céu da boca, que fica 40 mm acima da mesa)",
             orientacao="borda de baixo na mesa, em pé", reforco="3 orelhas internas com inserto M3 para a mesa; copos dos olhos fechados por trás (só a janela do cabo)",
             obs="3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto, sob a crista, dão acesso aos parafusos da coluna"),
        Peca("mandibula", g(mand), cor="verde", grupo="mandibula", imprimir=rot("x", 90), explode=(0, 70, 85), perimetros=4, infill=20,
             suporte="sim (pouco: sob o recorte esférico de trás, que nasce 2 a 10 mm acima da mesa; face escondida, virada para o pescoço)", orientacao="face de trás (plano de corte) na mesa, ponta do queixo para cima",
             reforco="almofadas maciças nos 2 lados do eixo; 2 nervuras que abraçam o horn; ponta do queixo maciça à frente de um plano a 45°",
             obs="sem parafuso por fora: o horn encaixa entre 2 nervuras (direita) e o pino da mesa entra no soquete cego (esquerda)"),
        Peca("mesa-cabeca", g(mesa), material="PETG", cor="grafite", grupo="cabeca", imprimir=rot("x", 180), macica=True, explode=(0, 0, 95),
             suporte="não", perimetros=4, infill=30, orientacao="de cabeça para baixo: face de cima na mesa",
             reforco="placa de 4 mm; janela do servo da boca com cantos em chanfro",
             obs="mesa da cabeça: 2 M3x10 na coluna do berço (por cima, pelos furos sob a crista); segura o servo da boca e o pino do eixo da mandíbula"),
        Peca("crista-cabeca", lam_h, cor="azul", grupo="cabeca", imprimir=rot("y", 90), macica=True, explode=(0, -40, 215), suporte="não",
             orientacao="deitada (lâmina de 6 mm)", obs="crista da cabeça; encaixe por pressão (sem cola): tampa os 2 furos de acesso aos parafusos da mesa"),
        Peca("olho", g(olhos[0]), cor="branco", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(20, 60, 170), orientacao="face de trás (plana) na mesa",
             obs="olho direito: bolso da câmera (Camera Module 3) aberto por trás; pressão ou cola no copo do crânio"),
        Peca("olho-esq", g(olhos[1]), cor="branco", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-20, 60, 170), orientacao="face de trás (plana) na mesa",
             obs="olho esquerdo: bolso do sensor ToF aberto por trás"),
        Peca("iris", g(iris[0]), cor="azul", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(24, 80, 176), orientacao="face de trás na mesa",
             obs="anel da íris: a placa da câmera encosta atrás dele (4 furos piloto M2)"),
        Peca("iris-esq", g(iris[1]), cor="azul", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-24, 80, 176), orientacao="face de trás na mesa"),
        Peca("pupila", g(pups[0]), cor="preto", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(28, 100, 182), orientacao="face de trás na mesa",
             obs="pupila escura VAZADA no centro (a lente da câmera olha pelo furo); pressão, sem cola (dá acesso à lente)"),
        Peca("pupila-esq", g(pups[1]), cor="preto", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-28, 100, 182), orientacao="face de trás na mesa",
             obs="pupila escura vazada (janela do ToF)"),
    ]

    # ------------------------------------------------------------ esqueleto
    teste = BS.teste_encaixe()
    teste.copias = []
    capa = BS.capa_esfera()
    capa.solido = capa.solido.translate([0, -BS.B.esfera_y, 0])
    capa.copias = [mat_trans((0.0, ye, 0.0))]
    capa.explode = (0, 0, -30)
    pecas += [chassi, capa, BB.bandeja_pi(E), _bandeja_uno(E), *BB.pescoco(E), teste]
    comps += comps_esq

    juntas = BB.juntas(E)
    juntas["mandibula"] = Junta("cabeca", (0, bo["y_eixo"], bo["z_eixo"]), (-1, 0, 0), (0.0, K.boca_abre))
    juntas["braco_d"] = Junta("corpo", (0, oy, oz), (1, 0, 0), br.lim)          # positivo = mão sobe
    juntas["braco_e"] = Junta("corpo", (0, oy, oz), (1, 0, 0), br.lim)
    poses = [("neutra", {}),
             ("pan-esq", {"pan": N.pan[1]}), ("pan-dir", {"pan": N.pan[0]}),
             ("tilt-cima", {"cabeca": N.tilt[1]}), ("tilt-baixo", {"cabeca": N.tilt[0]}),
             ("boca-aberta", {"mandibula": K.boca_abre}),
             ("pan+tilt-baixo+boca", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": K.boca_abre}),
             ("pan+tilt-cima", {"pan": N.pan[0], "cabeca": N.tilt[1]}),
             ("bracos-cima", {"braco_d": br.lim[1], "braco_e": br.lim[1]}),
             ("bracos-baixo", {"braco_d": br.lim[0], "braco_e": br.lim[0]}),
             ("tudo-1", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": K.boca_abre, "braco_d": br.lim[1], "braco_e": br.lim[1]}),
             ("tudo-2", {"pan": N.pan[0], "cabeca": N.tilt[0], "mandibula": K.boca_abre, "braco_d": br.lim[1], "braco_e": br.lim[0]})]
    xr = E.x_roda + P.RODA.larg / 2
    apoios = [(xr, 0.0), (-xr, 0.0), (0.0, ye)]
    parede = {"corpo": medir_parede(ext, CA.fatia_z(inte, K.z_fundo + 1.0, K.z_gola - 1.0)),
              "gola": medir_parede(ext, CA.fatia_z(esfera(C0, r_gola_in, seg=128), zg + 4.0, z_top - 1.0)),
              "cabeça": medir_parede(c_ext, CA.fatia_z(c_int, BS.CZ + K.cabeca_z + 4.0, 900.0))}
    encaixes = [{"par": ["motor-tt-dir", "roda-dir"], "motivo": "eixo do motor entra no cubo da roda"},
                {"par": ["motor-tt-esq", "roda-esq"], "motivo": "eixo do motor entra no cubo da roda"}]
    cab = ["cranio", "mesa-cabeca", "mandibula", "servo-boca MG90S", "crista-cabeca", "olho", "olho-esq", "iris", "iris-esq", "pupila", "pupila-esq",
           "camera olho direito (fase 2)", "tof-olho esquerdo (fase 2)", "microfone-dir (fase 2)", "microfone-esq (fase 2)", "alto-falante (fase 2)"]
    dedos = [nm for nm in rel if nm.startswith("dedo")]
    return Modelo("dino", "Dinossauro", pecas, comps, juntas, apoios, poses, ordem=_ordem(cab, dedos),
                  obs={"parede_medida": parede, "explode_grupo": {"cabeca": (0, 0, 95), "pan": (0, 0, 30), "mandibula": (0, 70, 85), "braco_d": (70, 20, 0), "braco_e": (-70, 20, 0)}},
                  encaixes=encaixes)


def _ordem(cab, dedos):
    """Ordem de montagem e de abertura (teste 9). `dir` = de onde a peça vem."""
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    nX, nY, nZ = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
    tras = [dict(passo="bateria (entra por trás, por cima do carregador, e desce no piso)", move=["bateria 2x18650"], dir=(0, -0.12, 0.99), curso=15, depois=[(0, -1, 0), 180]),
            dict(passo="bandeja do Pi", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=190),
            dict(passo="bandeja do Uno", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=190)]
    traseira = ["traseira", "crista-costas"]
    return [
        dict(passo="chassi", move=["chassi"], dir=Z),
        dict(passo="motor direito", move=["motor-tt-dir"], dir=X),
        dict(passo="motor esquerdo", move=["motor-tt-esq"], dir=nX),
        dict(passo="step-down 5 V (parede esquerda, abraçadeira)", move=["step-down 5V (LM2596)"], dir=nX, curso=60),
        dict(passo="UBEC 6 V (parede direita, abraçadeira)", move=["ubec 6V 3A"], dir=X, curso=60),
        dict(passo="BMS 2S (no piso, sob o lugar do L298N)", move=["bms 2S"], dir=Z, curso=6, depois=[(0, 1, 0), 90]),
        dict(passo="chave (por baixo do piso)", move=["chave"], dir=nZ, curso=40),
        dict(passo="roda direita", move=["roda-dir"], dir=X),
        dict(passo="roda esquerda", move=["roda-esq"], dir=nX),
        dict(passo="esfera de apoio + capa", move=["esfera-apoio", "capa-esfera"], dir=nZ, curso=40),
        dict(passo="driver L298N (pela frente da torre)", move=["driver L298N"], dir=Y, curso=120),
        dict(passo="servo de pan", move=["servo-pan MG996R"], dir=Z),
        dict(passo="servo do braço direito", move=["servo-braco-dir"], dir=X, curso=60),
        dict(passo="servo do braço esquerdo", move=["servo-braco-esq"], dir=nX, curso=60),
        dict(passo="carregador USB-C (na mesinha de trás, fita dupla-face)", move=["carregador USB-C 2S"], dir=Z, curso=30),
        dict(passo="corpo desce por cima do chassi", move=["corpo", "barriga", *dedos, "mancha-dir", "mancha-esq", "tof-dir (fase 2)", "tof-esq (fase 2)"], dir=Z, curso=260),
        dict(passo="garfo (por dentro da boca do corpo)", move=["garfo-pescoco"], dir=Z, curso=160),
        dict(passo="berço + servo de tilt", move=["berco-tilt", "servo-tilt MG996R"], dir=Z, curso=160),
        dict(passo="gola", move=["gola"], dir=Z, curso=160),
        dict(passo="cubo + braço direito", move=["cubo-braco#0", "braco-dir"], dir=X, curso=60),
        dict(passo="cubo + braço esquerdo", move=["cubo-braco#1", "braco-esq"], dir=nX, curso=60),
        *tras,
        dict(passo="traseira (com a crista das costas)", move=list(traseira), dir=nY, curso=190),
        dict(passo="mesa dentro do crânio (na bancada)", move=["mesa-cabeca", "servo-boca MG90S", "alto-falante (fase 2)"], dir=nZ, curso=100, contra=["cranio"]),
        dict(passo="cabeça no pescoço", move=list(cab), dir=Z, curso=160),
        # abertura para manutenção SEM tirar a cabeça: traseira, bandejas e bateria saem por trás
        dict(passo="ABRIR: traseira sai", move=list(traseira), dir=nY, curso=190, sai=True),
        dict(passo="ABRIR: bandeja do Uno sai", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=190, sai=True),
        dict(passo="ABRIR: bandeja do Pi sai", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=190, sai=True),
        dict(passo="ABRIR: bateria sai", move=["bateria 2x18650"], dir=(0, -0.12, 0.99), curso=15, depois=[(0, -1, 0), 180], sai=True),
    ]
