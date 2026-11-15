"""Modelo 3: robô quadrado de mesa (~19 cm). Cabeça-cubo com tela de 3,5" e Raspberry Pi dentro, pan ±170°
(servo comum de 180° + engrenagens 2:1 impressas, cabos pelo tubo oco do pescoço) e tilt por DENTRO da cabeça.
Não roda: a base baixa e larga guarda Arduino Uno + shield, bateria 2S, step-down do Pi, UBEC dos servos,
carregador USB-C + BMS, alto-falante (fase 2) e o servo de pan. Nenhum parafuso nem furo técnico de frente ou de 3/4:
a tampa é presa por baixo, a cabeça por trás, a grade do alto-falante, a chave e o USB-C ficam atrás."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import componentes as C
from cad.comum import quadrado as QD
from cad.comum.geo import berco_modulo, caixa, cil, ressalto_nervurado, ret_arredondado, secao
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot
from cad.comum.quadrado import furo, inserto

Q = P.CUBO
K = Q.cab
F = P.FOLGA


def construir() -> Modelo:
    pecas, comps = [], []
    W, Dp, H = Q.base
    y0, y1 = -Dp / 2, Dp / 2
    t = Q.parede
    AY = Q.eixo_y
    zt0 = H - Q.tampa_esp                       # face de baixo da tampa
    ZT = Q.tilt_z

    def perfil(d=0.0):
        return ret_arredondado(W - 2 * d, Dp - 2 * d, Q.base_r - d)

    # ------------------------------------------------------------ base (cuba): piso na mesa, chanfro de 45° embaixo
    base = QD.prato(perfil, 0, zt0, chanfro_baixo=Q.chanfro) - secao(perfil(t), "z", t, zt0 + 1)
    px0, px1 = Q.porta_x
    base = base - caixa(px0, px1, y0 - 1, y0 + t + 0.01, t - 0.01, zt0 + 1)                    # abertura da porta (sem soleira: a bateria desliza)
    cxp, cyp = W / 2 - Q.base_r + 7.5, Dp / 2 - Q.base_r + 7.5
    cantos = [(sx * cxp, sy * cyp) for sx in (1, -1) for sy in (1, -1)]
    zp1 = zt0 - 8.2                                                                           # topo dos postes da tampa
    for (px, py) in cantos:
        base = base + cil((px, py, t - 0.01), (px, py, zp1), 6.0, seg=32)
    for (px, py) in cantos:                                                                   # parafuso da tampa entra POR BAIXO (chave Allen longa)
        base = base - furo((px, py, -1), (0, 0, 1), zp1 + 2, F.m3_passante) - cil((px, py, -0.01), (px, py, zp1 - 4.0), 3.25, seg=24)
    sp = QD.servo_pan(Q, (0, AY), Q.ang_servo, Q.ang_corpo, t)
    base = base + sp.soma
    # Arduino Uno: 4 ressaltos nervurados com furo piloto
    ux, uy = Q.uno_xy
    pos_uno = [(ux + x, uy + P.UNO.placa[1] - yd) for (x, yd) in P.UNO.furos]
    for (x, y) in pos_uno:
        base = base + ressalto_nervurado((x, y, t + 5.0), (0, 0, -1), 5.01, d_inserto=F.m3_piloto, d_ext=7.0, n_nervuras=3, ang0=90.0, nervura_alt=4.0)
    # berço da bateria (guias baixas) e batentes da porta
    bx, by = Q.bateria_xy
    Lb, Wb, Hb = P.BATERIA.cx
    base = base + caixa(bx + Wb / 2 + 0.6, bx + Wb / 2 + 2.6, by - Lb / 2 + 8, by + Lb / 2, t - 0.01, t + 6)
    base = base + caixa(bx - Wb / 2 - 2.6, bx - Wb / 2 - 0.6, by - Lb / 2 + 8, by + Lb / 2, t - 0.01, t + 6)
    base = base + caixa(bx - Wb / 2, bx + Wb / 2, by + Lb / 2 + 0.6, by + Lb / 2 + 2.6, t - 0.01, t + 6)
    for (xa, xb) in ((px0 + 0.5, px0 + 2.3), (px1 - 2.3, px1 - 0.5)):
        base = base + caixa(xa, xb, y0 + t + 2.3, y0 + t + 5.3, t - 0.01, t + 4)
    # módulos de energia: berço de cantoneiras + abraçadeira (comum/cad/comum/geo.py › berco_modulo)
    ycg = y0 + t + 0.3 + P.CARREGADOR2S.cx[0] / 2
    energia = [("step-down 5V (LM2596)", P.STEPDOWN5V, Q.stepdown_xy, 90.0, "azul", dict(pontas=True)),      # encostado na parede: abraçadeira ao comprido
               ("ubec 6V 3A dos servos", P.UBEC6V, Q.ubec_xy, 90.0, "laranja", {}),
               ("carregador USB-C 2S", P.CARREGADOR2S, (Q.carregador_x, ycg), 90.0, "verde", {}),
               ("bms 2S 10A", P.BMS2S, Q.bms_xy, 90.0, "rosa", dict(fita=None))]                             # bolso raso + fita dupla-face
    cortes = [sp.corte]
    for (nm, comp, (ex, ey), ang, cor, opc) in energia:
        soma, corte = berco_modulo(comp, alt=min(4.0, comp.cx[2]), piso=t, **opc)
        base = base + soma.rotate([0, 0, ang]).translate([ex, ey, t])
        if corte is not None:
            cortes.append(corte.rotate([0, 0, ang]).translate([ex, ey, t]))
        comps.append(Comp(nm, C.modulo(comp).rotate([0, 0, ang]).translate([ex, ey, t]), "corpo", comp.massa, cor))
    uw, uh = P.CARREGADOR2S.usb_c
    cortes.append(caixa(Q.carregador_x - uw / 2 - 0.4, Q.carregador_x + uw / 2 + 0.4, y0 - 1, y0 + t + 1, t + 0.4, t + 0.4 + uh + 1.0))   # janela do USB-C (atrás)
    # alto-falante (fase 2) na parede de TRÁS: 2 trilhos em L + apoio; grade de fendas VERTICAIS (pontes de 2,2 mm)
    fx, fz = Q.falante_xz
    rf = P.FALANTE.d / 2
    yw = y0 + t
    for s in (1, -1):
        xa, xb = sorted((fx + s * (rf + 0.4), fx + s * (rf + 2.4)))
        base = base + caixa(xa, xb, yw - 0.01, yw + 6.2, t - 0.01, fz + 12)
        xa, xb = sorted((fx + s * (rf - 2.1), fx + s * (rf + 2.4)))
        base = base + caixa(xa, xb, yw + 4.6, yw + 6.2, t - 0.01, fz + 12)
    base = base + caixa(fx - 6, fx + 6, yw - 0.01, yw + 4.4, t - 0.01, fz - rf - 0.2)
    for k in range(-3, 4):
        h = np.sqrt(17.0 ** 2 - (5.0 * k) ** 2) - 1.0
        cortes.append(caixa(fx + 5.0 * k - 1.1, fx + 5.0 * k + 1.1, y0 - 1, yw + 1, fz - h, fz + h))
    # chave na parede de trás (acima do carregador)
    rw, rh = P.CHAVE.recorte
    xch, zch = Q.chave_xz
    cortes.append(caixa(xch - rw / 2, xch + rw / 2, y0 - 1, yw + 1, zch - rh / 2, zch + rh / 2))
    cortes.append(caixa(xch - rw / 2 - 2.5, xch + rw / 2 + 2.5, y0 + P.CHAVE.painel, yw + 1, zch - rh / 2 - 2.5, zch + rh / 2 + 2.5))
    for (x, y) in pos_uno:
        cortes.append(furo((x, y, t + 5.01), (0, 0, -1), 7, F.m3_piloto))
    cortes.append(BS.universal_z(12, 0, 0, t))                                               # fase 2: ponto universal (IMU) no piso
    for c in cortes:
        base = base - c

    # ------------------------------------------------------------ cabeça + pescoço (comuns aos dois robôs quadrados)
    hd = QD.cabeca(K, P.TELA35, (0.0, AY, ZT), lidar=dict(furos=[(-10.0, -12.0), (10.0, -12.0)], piloto=F.m3_piloto))
    p_tubo, p_eng, furo_tampa = QD.pescoco(Q, K, (0.0, AY), (zt0, H), hd.zg0, hd.pos_tir, Q.ang_servo)

    # ------------------------------------------------------------ tampa (imprime de cabeça para baixo; chanfro de 45° em cima)
    tampa = QD.prato(perfil, zt0, H, chanfro_cima=2.5) - furo_tampa
    for (px, py) in cantos:
        w = np.degrees(np.arctan2(-py, -px))
        tampa = tampa + ressalto_nervurado((px, py, zt0 - 8.0), (0, 0, 1), 8.01, n_nervuras=3, angulos=[-(w - 50), -w, -(w + 50)], nervura_alt=6.0)
    for (px, py) in cantos:
        tampa = tampa - inserto((px, py, zt0 - 8.0), (0, 0, 1))
    xe = (px0 + px1) / 2
    tampa = tampa + caixa(xe - 6, xe + 6, yw + 0.2, yw + 8, zt0 - 14, zt0 + 0.01)                 # orelha que prende a porta
    tampa = tampa - inserto((xe, yw + 0.2, zt0 - 8), (0, 1, 0))

    porta = caixa(px0 + 0.3, px1 - 0.3, y0, yw, t + 0.6, zt0 - 0.3)
    porta = porta + caixa(px0 + 6, px1 - 6, yw - 0.01, yw + 2.0, t + 0.6, t + 4.0)                # pé: encosta nos 2 batentes do piso
    porta = porta - furo((xe, y0 - 1, zt0 - 8), (0, 1, 0), t + 2, F.m3_passante)

    pecas += [
        Peca("base", base, material="PETG", cor="grafite", macica=True, explode=(0, 0, -60), perimetros=4, infill=20,
             orientacao="piso na mesa", reforco="chanfro de 45° na aresta de baixo; postes da tampa Ø12 fundidos nos cantos; postes do servo com mãos-francesas; ressaltos nervurados do Uno; fendas verticais na grade",
             obs="cuba: piso, paredes, postes do servo de pan, do Uno e da tampa, berços dos módulos de energia (abraçadeira), trilhos do alto-falante; chave, USB-C e grade atrás"),
        Peca("tampa-base", tampa, material="PETG", cor="grafite", macica=True, imprimir=rot("x", 180), explode=(0, 0, 25), perimetros=4, infill=25,
             orientacao="de cabeça para baixo: a face de cima na mesa", reforco="4 ressaltos de inserto com 3 nervuras a 45°; chanfro de 45° na aresta que encosta na mesa",
             obs="presa por 4 M3x10 que entram POR BAIXO da base; a flange do pescoço gira sobre ela; orelha do parafuso da porta"),
        Peca("porta-traseira", porta, material="PETG", cor="grafite", macica=True, imprimir=rot("x", 90), explode=(0, -70, -30), perimetros=3, infill=20,
             orientacao="face de fora na mesa", obs="porta da bateria (atrás); 1 M3 na orelha da tampa, pé contra 2 batentes do piso"),
        p_tubo, p_eng, sp.eng, hd.garfo,
    ] + hd.pecas + [BS.teste_encaixe()]
    pecas[-1].copias = []
    for p_ in pecas:
        p_.liso = False            # peças de faces planas: sem sombreamento suave no render

    # ------------------------------------------------------------ componentes
    M_chave = C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (xch, y0, zch))
    comps += [
        sp.comp,
        Comp("Arduino Uno + shield", C.placa_eletronica(P.UNO).translate([ux, uy, t + 5]), "corpo", P.UNO.massa + 20, "azul"),
        Comp("bateria 2x18650", C.bateria().translate([bx, by, t]), "corpo", P.BATERIA.massa_suporte + 2 * P.BATERIA.massa_celula, "prata"),
        Comp("alto-falante (fase 2)", C.falante().rotate([0, 0, 180]).translate([fx, yw + 0.2, fz]), "corpo", P.FALANTE.massa, "preto", fase2=True),
        Comp("chave", C.chave().transform(M_chave[:3, :]), "corpo", 3.0, "preto"),
    ] + hd.comps
    sx_, sy_ = sp.xy
    z1, z2 = Q.dentes
    juntas = {"pan": Junta("corpo", (0, AY, 0), (0, 0, 1), Q.pan),
              "cabeca": Junta("pan", (0, AY, ZT), (1, 0, 0), Q.tilt),
              "eng": Junta("corpo", (sx_, sy_, 0), (0, 0, 1), (-Q.pan[1] / 2, -Q.pan[0] / 2))}

    def pose(nome, pan=0.0, tilt=0.0):
        return (nome, {"pan": pan, "eng": -pan * z1 / z2, "cabeca": tilt})

    poses = [pose("neutra"), pose("pan+170", Q.pan[1]), pose("pan-170", Q.pan[0]), pose("pan+90", 90.0), pose("pan+37", 37.0),
             pose("tilt-cima", 0.0, Q.tilt[1]), pose("tilt-baixo", 0.0, Q.tilt[0]),
             pose("pan+120+tilt-baixo", 120.0, Q.tilt[0]), pose("pan-75+tilt-cima", -75.0, Q.tilt[1]), pose("pan+170+tilt-baixo", Q.pan[1], Q.tilt[0])]
    c, r = Q.chanfro, Q.base_r
    apoios = [(sx * (W / 2 - r), sy * (Dp / 2 - c)) for sx in (1, -1) for sy in (1, -1)] + [(sx * (W / 2 - c), sy * (Dp / 2 - r)) for sx in (1, -1) for sy in (1, -1)]
    encaixes = [{"par": ["engrenagem-servo", "servo-pan MG996R"], "motivo": "horn do servo fica no rebaixo da engrenagem"}]
    Zd, nZ, nY = (0, 0, 1), (0, 0, -1), (0, -1, 0)
    cab = hd.nomes + ["garfo"]
    topo = ["tampa-base", "tubo-pescoco", "engrenagem-pescoco"] + cab
    ordem = [
        dict(passo="base", move=["base"], dir=Zd),
        dict(passo="servo de pan nos 2 postes", move=["servo-pan MG996R"], dir=Zd),
        dict(passo="Arduino Uno nos 4 ressaltos", move=["Arduino Uno + shield"], dir=Zd),
        dict(passo="módulos de energia nos berços (1 abraçadeira cada)", move=[e[0] for e in energia], dir=Zd, curso=60),
        dict(passo="chave (por fora, atrás)", move=["chave"], dir=nY, curso=40),
        dict(passo="alto-falante nos trilhos da parede de trás", move=["alto-falante (fase 2)"], dir=Zd, curso=60),
        dict(passo="engrenagem do servo no horn", move=["engrenagem-servo"], dir=Zd),
        dict(passo="bateria (pela porta de trás)", move=["bateria 2x18650"], dir=nY, curso=160),
    ] + hd.bancada + [
        dict(passo="tubo do pescoço na tampa, por cima (bancada)", move=["tubo-pescoco"], dir=Zd, contra=["tampa-base"]),
        dict(passo="engrenagem do pescoço por baixo da tampa (bancada)", move=["engrenagem-pescoco"], dir=nZ, contra=["tampa-base", "tubo-pescoco"]),
        dict(passo="cabeça sobre o tubo; 3 tirantes M3 por baixo (bancada)", move=cab, dir=Zd, curso=140, contra=["tampa-base", "tubo-pescoco", "engrenagem-pescoco"]),
        dict(passo="tampa + pescoço + cabeça sobre a base; 4 M3 por baixo", move=topo, dir=Zd, curso=140),
        dict(passo="porta traseira (1 M3)", move=["porta-traseira"], dir=nY, curso=60),
        dict(passo="abrir: porta traseira", move=["porta-traseira"], dir=nY, curso=60, sai=True),
        dict(passo="abrir: bateria sai por trás", move=["bateria 2x18650"], dir=nY, curso=160, sai=True),
        dict(passo="abrir: tampa + pescoço + cabeça saem por cima (placas à mostra)", move=topo, dir=Zd, curso=140, sai=True),
    ]
    obs = {"peca_teste_negativo": "quadro-cabeca", "explode_grupo": {"cabeca": (0, 20, 140), "pan": (0, 0, 45), "eng": (0, -60, 45)},
           "energia": "pack 2S → LM2596 (5 V do Pi, até ~6,5 V de pack), UBEC 6 V 3 A (2 MG996R), carregador USB-C 2S com balanceamento + BMS 2S",
           "altura_mm": round(hd.topo_z, 1)}
    return Modelo("cubo", "Robô quadrado de mesa", pecas, comps, juntas, apoios, poses, ordem=ordem, obs=obs, encaixes=encaixes)
