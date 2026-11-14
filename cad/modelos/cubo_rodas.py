"""Modelo 4: o cubo que RODA (≥ 30 cm). Mesma cabeça-cubo do robô de mesa, maior (tela de 5" HDMI), pescoço estreito
com pan ±170° (engrenagens 2:1 + tubo oco) e tilt por dentro. Embaixo, uma base móvel de tração diferencial:
2 motores JGB37-520 com encoder + rodas de 85 mm NA FRENTE e uma bola de 40 mm atrás. Pack 3S (12 V).

Pilha (de baixo para cima): base-rodas (cuba com motores, bateria num alçapão por baixo, carregador USB-C, BMS, chave)
→ deck (servo de pan, Arduino, L298N, step-down do Pi, UBEC) → tronco (casca de cima, com o alto-falante atrás)
→ pescoço → cabeça. Parafusos só por baixo e por trás; cada motor sai pela lateral, atrás da roda, sem abrir o robô."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import componentes as C
from cad.comum import quadrado as QD
from cad.comum.geo import berco_modulo, caixa, casco, cil, mat_giro, ressalto_nervurado, ret_arredondado, secao, uniao
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot
from cad.comum.quadrado import furo, gota, inserto

Q = P.CUBO_RODAS
K = Q.cab
F = P.FOLGA
MT, RD = P.JGB37, P.RODA85


def construir() -> Modelo:
    pecas, comps = [], []
    W = Q.larg
    y0, y1 = Q.y
    yc, Ly = (y0 + y1) / 2, y1 - y0
    t = Q.parede
    zc = Q.chao                                  # face de baixo do piso
    zf = zc + t                                  # face de cima do piso
    zd0, zd1 = Q.z_deck, Q.z_deck + Q.deck_esp   # deck
    ztop = Q.z_topo
    zt0 = ztop - Q.tampa_esp
    AY, ZT = Q.eixo_y, Q.tilt_z
    ze = RD.d / 2                                # altura do eixo das rodas
    zm = ze + MT.eixo_desloc                     # centro da caixa de redução (o eixo fica embaixo)
    xi = W / 2 - t

    def perfil(d=0.0):
        return ret_arredondado(W - 2 * d, Ly - 2 * d, Q.raio - d).translate([0, yc])

    postes = [(sx * px, py) for (px, py) in Q.postes for sx in (1, -1)]

    # ------------------------------------------------------------ base-rodas (cuba): piso na mesa
    fora = QD.prato(perfil, zc, zd0, chanfro_baixo=Q.chanfro)
    base = fora - secao(perfil(t), "z", zf, zd0 + 1)
    cortes = []
    for (px, py) in postes:                                                                  # 4 postes: parafuso por baixo → deck → tronco
        base = base + (cil((px, py, zf - 0.01), (px, py, zd0), 6.0, seg=32) ^ fora)
        cortes.append(furo((px, py, zc - 1), (0, 0, 1), zd0 - zc + 2, F.m3_passante) + cil((px, py, zc - 0.01), (px, py, zd0 - 4.0), 3.25, seg=24))
    fd, fe, fc = Q.flange_motor
    for s in (1, -1):                                                                        # parede do motor: reforço + furo em gota + 4 insertos da flange
        xa, xb = sorted((s * (xi - 4.0), s * (xi + 0.01)))
        base = base + caixa(xa, xb, -fd / 2, fd / 2, zf - 0.01, zm + fd / 2 + 1.0)
        cortes.append(gota((s * (xi - 5.0), 0, zm), (s, 0, 0), t + 6.0, Q.furo_motor, (0, 0, 1)))
        for a in (45, 135, 225, 315):
            cortes.append(inserto((s * W / 2, fc / 2 * np.cos(np.radians(a)), zm + fc / 2 * np.sin(np.radians(a))), (-s, 0, 0)))
    # alçapão da bateria (por baixo): abertura no piso + 4 ressaltos com inserto
    by = Q.bateria_y
    Lb, Wb, Hb = P.BATERIA3S.cx
    ax_, ay_ = Lb / 2 + 2.5, Wb / 2 + 2.5
    cortes.append(caixa(-ax_, ax_, by - ay_, by + ay_, zc - 1, zf + 1))
    hx_, hy_ = Q.alcapao[0] / 2, Q.alcapao[1] / 2
    pos_alc = [(sx * (hx_ - 7.0), by + sy * (hy_ - 5.5)) for sx in (1, -1) for sy in (1, -1)]
    # apoio de trás: poço da bola (cilindro + assento cônico a 45°) e 4 ressaltos da capa
    bx_, byb = 0.0, Q.bola_y
    rb = P.BOLA40.d / 2
    rw = rb + 0.6
    cz = zc + rb * np.sqrt(2.0) + 0.2                      # o cone r = cz - z tangencia a bola a 45°
    z1, z2 = cz - rw, cz - 3.0
    base = base + cil((bx_, byb, zf - 0.01), (bx_, byb, z1 + 4.0), rw + 3.0) + cil((bx_, byb, z1 + 4.0), (bx_, byb, z2 + 3.0), rw + 3.0, 5.5)
    cortes.append(cil((bx_, byb, zc - 1), (bx_, byb, z1), rw) + cil((bx_, byb, z1 - 0.01), (bx_, byb, z2), rw, 3.0))
    pos_capa = [(bx_ + 28.0 * np.cos(np.radians(a)), byb + 28.0 * np.sin(np.radians(a))) for a in (35, 145, 215, 325)]
    for (px, py) in pos_alc + pos_capa:
        base = base + ressalto_nervurado((px, py, zf + 5.5), (0, 0, -1), 5.51, d_ext=10.0, angulos=[90, 270], nervura_alt=4.0)
        cortes.append(inserto((px, py, zc), (0, 0, 1)))
    # carregador USB-C (boca na parede de trás, rente ao piso), BMS (fita dupla-face), chave atrás
    ycg = y0 + t + 0.3 + P.CARREGADOR2S.cx[0] / 2
    baixo = [("carregador USB-C 3S", P.CARREGADOR2S, (Q.carregador_x, ycg), 90.0, "verde", dict(piso=t)),
             ("bms 3S 10A", P.BMS3S, Q.bms_xy, 90.0, "rosa", dict(piso=t, fita=None))]
    for (nm, comp, (ex, ey), ang, cor, opc) in baixo:
        soma, corte = berco_modulo(comp, alt=min(4.0, comp.cx[2]), **opc)
        base = base + soma.rotate([0, 0, ang]).translate([ex, ey, zf])
        if corte is not None:
            cortes.append(corte.rotate([0, 0, ang]).translate([ex, ey, zf]))
        comps.append(Comp(nm, C.modulo(comp).rotate([0, 0, ang]).translate([ex, ey, zf]), "corpo", comp.massa, cor))
    uw, uh = P.CARREGADOR2S.usb_c
    cortes.append(caixa(Q.carregador_x - uw / 2 - 0.4, Q.carregador_x + uw / 2 + 0.4, y0 - 1, y0 + t + 1, zf + 0.4, zf + 0.4 + uh + 1.0))
    rw_, rh_ = P.CHAVE.recorte
    xch, zch = Q.chave_xz
    cortes.append(caixa(xch - rw_ / 2, xch + rw_ / 2, y0 - 1, y0 + t + 1, zch - rh_ / 2, zch + rh_ / 2))
    cortes.append(caixa(xch - rw_ / 2 - 2.5, xch + rw_ / 2 + 2.5, y0 + P.CHAVE.painel, y0 + t + 1, zch - rh_ / 2 - 2.5, zch + rh_ / 2 + 2.5))
    # fase 2: sensor de queda (janela no piso, na frente) e 3 ToF (entalhe na borda, escondido na fresta do deck)
    cortes.append(caixa(-7, 7, y1 - t - 9, y1 - t - 3, zc - 1, zf + 1) + BS.universal_z(0, y1 - t - 6, zc, zf))
    cortes.append(caixa(-7, 7, y1 - t - 1, y1 + 1, zd0 - 4.0, zd0 + 1))
    for sx in (1, -1):
        cortes.append(furo((sx * 10.0, y1 - t - 0.01, zd0 - 10.0), (0, 1, 0), 2.0, F.m25_piloto))
        xa, xb = sorted((sx * (xi - 1), sx * (W / 2 + 1)))
        cortes.append(caixa(xa, xb, yc - 7, yc + 7, zd0 - 4.0, zd0 + 1))
        for sy in (1, -1):
            cortes.append(furo((sx * (xi - 0.01), yc + sy * 10.0, zd0 - 10.0), (sx, 0, 0), 2.0, F.m25_piloto))
    for c in cortes:
        base = base - c

    # ------------------------------------------------------------ tampa-bateria (alçapão): bateria presa nela, sai por baixo
    alc = caixa(-hx_, hx_, by - hy_, by + hy_, zc - 3.0, zc)
    soma, corte = berco_modulo(P.BATERIA3S, alt=4.0, piso=3.0)
    alc = alc + soma.translate([0, by, zc]) - corte.translate([0, by, zc])
    for (px, py) in pos_alc:
        alc = alc - furo((px, py, zc - 4), (0, 0, 1), 5, F.m3_passante)

    # ------------------------------------------------------------ capa da bola (por baixo)
    capa = cil((bx_, byb, zc - 12.0), (bx_, byb, zc), rw + 3.0)
    for (px, py) in pos_capa:
        capa = capa + casco(cil((px, py, zc - 3.0), (px, py, zc), 5.5, seg=24), cil((bx_, byb, zc - 3.0), (bx_, byb, zc), 12.0))
    rl = np.sqrt(rb ** 2 - 12.0 ** 2) + 0.3                # boca de baixo: menor que a bola, ela não cai
    capa = capa - cil((bx_, byb, zc - 13.0), (bx_, byb, zc - 12.0 + 0.01), rl) - cil((bx_, byb, zc - 12.0), (bx_, byb, zc - 12.0 + (rw - rl)), rl, rw) \
        - cil((bx_, byb, zc - 12.0 + (rw - rl) - 0.01), (bx_, byb, zc + 1), rw)
    for (px, py) in pos_capa:
        capa = capa - furo((px, py, zc - 4), (0, 0, 1), 5, F.m3_passante)

    # ------------------------------------------------------------ flange dos motores (2 cópias; fica atrás da roda)
    fl = cil((W / 2, 0, zm), (W / 2 + fe, 0, zm), fd / 2)
    fl = fl - furo((W / 2 - 1, 0, ze), (1, 0, 0), fe + 2, MT.ressalto[0] + 1.0)
    for k in range(MT.n_furos):
        a = np.radians(60.0 * k)
        py, pz = MT.furos_circ / 2 * np.cos(a), zm + MT.furos_circ / 2 * np.sin(a)
        fl = fl - furo((W / 2 - 1, py, pz), (1, 0, 0), fe + 2, F.m3_passante) - furo((W / 2 + fe - 1.5, py, pz), (1, 0, 0), 2.0, F.cabeca_m3_d)
    for a in (45, 135, 225, 315):
        fl = fl - furo((W / 2 - 1, fc / 2 * np.cos(np.radians(a)), zm + fc / 2 * np.sin(np.radians(a))), (1, 0, 0), fe + 2, F.m3_passante)
    M_esq = mat_giro((0, 0, 0), (0, 0, 1), 180.0)

    # ------------------------------------------------------------ deck: bandeja de eletrônica entre a base e o tronco
    rec = Q.deck_recuo
    deck = QD.prato(lambda d=0.0: perfil(d + rec), zd0, zd1)
    sp = QD.servo_pan(Q, (0.0, AY), Q.ang_servo, Q.ang_corpo, zd1)
    deck = deck + sp.soma
    cd = [sp.corte]
    ux, uy = Q.uno_xy
    pos_uno = [(ux + x, uy + P.UNO.placa[1] - yd) for (x, yd) in P.UNO.furos]
    lx, ly = Q.l298_xy
    pos_l298 = [(lx + sx * P.L298N.furos / 2, ly + sy * P.L298N.furos / 2) for sx in (1, -1) for sy in (1, -1)]
    for (x, y) in pos_uno + pos_l298:
        deck = deck + ressalto_nervurado((x, y, zd1 + 5.0), (0, 0, -1), 5.01, d_inserto=F.m3_piloto, d_ext=7.0, n_nervuras=3, ang0=90.0, nervura_alt=4.0)
        cd.append(furo((x, y, zd1 + 5.01), (0, 0, -1), 7.5, F.m3_piloto))
    cima = [("step-down 5V (XL4015)", P.STEPDOWN5V, Q.stepdown_xy, 0.0, "azul", dict(pontas=True)),
            ("ubec 6V 3A dos servos", P.UBEC6V, Q.ubec_xy, 90.0, "laranja", {})]
    for (nm, comp, (ex, ey), ang, cor, opc) in cima:
        soma, corte = berco_modulo(comp, alt=4.0, piso=Q.deck_esp, canal=0.0, **opc)
        deck = deck + soma.rotate([0, 0, ang]).translate([ex, ey, zd1])
        cd.append(corte.rotate([0, 0, ang]).translate([ex, ey, zd1]))
        comps.append(Comp(nm, C.modulo(comp).rotate([0, 0, ang]).translate([ex, ey, zd1]), "corpo", comp.massa, cor))
    for (px, py) in postes:
        cd.append(furo((px, py, zd0 - 1), (0, 0, 1), Q.deck_esp + 2, F.m3_passante))
    for sx in (1, -1):
        cd.append(caixa(sx * 50 - 6, sx * 50 + 6, 3, 15, zd0 - 1, zd1 + 1))                    # fios dos motores e encoders
    cd.append(caixa(-56, -40, -141, -129, zd0 - 1, zd1 + 1))                                  # fios da bateria, chave e carregador
    cd.append(BS.universal_z(0, -38, zd0, zd1))                                               # fase 2: IMU no centro, perto do eixo das rodas
    for c in cd:
        deck = deck - c

    # ------------------------------------------------------------ cabeça + pescoço (comuns aos dois robôs quadrados)
    ld = P.LD19
    lid = dict(furos=[(fx_, -30.0 + fy_) for (fx_, fy_) in ld.furos], piloto=F.m25_piloto, comp="lidar LD19 (fase 2)",
               solido=C.lidar_ld19(), xy=(0.0, -19.0), massa=ld.massa, cabo=(12.0, -12.0))
    hd = QD.cabeca(K, P.TELA5, (0.0, AY, ZT), nome_tela="tela 5 pol. HDMI", lidar=lid)
    p_tubo, p_eng, furo_tampa = QD.pescoco(Q, K, (0.0, AY), (zt0, ztop), hd.zg0, hd.pos_tir, Q.ang_servo)

    # ------------------------------------------------------------ tronco (casca de cima): imprime de cabeça para baixo
    tr_fora = QD.prato(perfil, zd1, ztop, chanfro_cima=Q.chanfro_topo)
    tronco = tr_fora - QD.prato(lambda d=0.0: perfil(d + t), zd1 - 1, zt0, chanfro_cima=Q.chanfro_topo - 2.5) - furo_tampa
    for (px, py) in postes:                                                                   # 4 colunas até a borda, com inserto
        tronco = tronco + (cil((px, py, zd1), (px, py, zt0 + 0.01), 6.0, seg=32) ^ tr_fora)
    for (px, py) in postes:
        tronco = tronco - inserto((px, py, zd1), (0, 0, 1))
    fz = Q.falante_z                                                                          # alto-falante (fase 2) atrás: trilhos + grade de fendas verticais
    rf = P.FALANTE.d / 2
    yw = y0 + t
    for s in (1, -1):
        xa, xb = sorted((s * (rf + 0.4), s * (rf + 2.4)))
        tronco = tronco + caixa(xa, xb, yw - 0.01, yw + 6.2, fz - 12, zt0 + 0.01)
        xa, xb = sorted((s * (rf - 2.1), s * (rf + 2.4)))
        tronco = tronco + caixa(xa, xb, yw + 4.6, yw + 6.2, fz - 12, zt0 + 0.01)
    tronco = tronco + caixa(-6, 6, yw - 0.01, yw + 4.4, fz + rf + 0.2, zt0 + 0.01)
    for k in range(-3, 4):
        h = np.sqrt(17.0 ** 2 - (5.0 * k) ** 2) - 1.0
        tronco = tronco - caixa(5.0 * k - 1.1, 5.0 * k + 1.1, y0 - 1, yw + 1, fz - h, fz + h)

    pecas += [
        Peca("base-rodas", base, material="PETG", cor="grafite", macica=True, explode=(0, 0, -70), perimetros=5, infill=25,
             orientacao="piso na mesa", reforco="paredes dos motores com reforço de 4 mm e furo em gota; 4 postes Ø12 nos cantos; ressaltos nervurados do alçapão e da capa; assento cônico da bola a 45°; chanfro de 45° embaixo",
             obs="cuba da base móvel: motores entram pela lateral (flange atrás da roda), bateria num alçapão por baixo, carregador USB-C e chave atrás, janela do sensor de queda e entalhes dos ToF"),
        Peca("tampa-bateria", alc, material="PETG", cor="grafite", macica=True, explode=(0, 0, -110), perimetros=4, infill=25,
             orientacao="face de baixo na mesa, cantoneiras para cima", reforco="4 cantoneiras + abraçadeira seguram o suporte 3x18650",
             obs="alçapão da bateria: 4 M3x8 por baixo; a bateria desce junto com ele"),
        Peca("capa-esfera", capa, material="PETG", cor="grafite", macica=True, imprimir=rot("x", 180), explode=(0, 0, -100), perimetros=4, infill=40,
             orientacao="de cabeça para baixo: a face que encosta no piso na mesa; a boca fecha a 45°", reforco="4 orelhas; boca cônica a 45°",
             obs="segura a bola de 40 mm no poço; 4 M3x8 por baixo; a 8 mm do chão"),
        Peca("flange-motor", fl, material="PETG", cor="grafite", macica=True, imprimir=rot("y", -90), copias=[np.eye(4), M_esq], explode=(60, 0, 0),
             perimetros=5, infill=60, orientacao="deitada, a face que encosta na parede na mesa", reforco="disco quase maciço (5 perímetros, 60 %): leva o peso e o torque do motor",
             obs="prende o motor JGB37 (6 M3x6) e fecha o furo lateral da base (4 M3x10); fica escondida atrás da roda"),
        Peca("deck", deck, material="PETG", cor="grafite", macica=True, explode=(0, 0, 20), perimetros=4, infill=25,
             orientacao="face de baixo na mesa", reforco="postes do servo de pan com mãos-francesas; ressaltos nervurados do Uno e do L298N; berços com abraçadeira",
             obs="bandeja de eletrônica: servo de pan, Arduino Uno, L298N, step-down do Pi e UBEC; 1,5 mm para dentro (fresta de sombra entre base e tronco)"),
        Peca("tronco", tronco, material="PETG", cor="branco", macica=True, imprimir=rot("x", 180), explode=(0, 0, 60), perimetros=4, infill=15,
             orientacao="de cabeça para baixo: o topo na mesa", reforco="4 colunas Ø12 fundidas nas paredes (inserto na ponta); chanfro de 45° de 6 mm no topo; trilhos do alto-falante nascem do topo",
             obs="casca de cima: 4 M3x12 entram POR BAIXO da base, atravessam o deck e rosqueiam aqui; grade do alto-falante atrás"),
        p_tubo, p_eng, sp.eng, hd.garfo,
    ] + hd.pecas + [BS.teste_encaixe()]
    pecas[-1].copias = []
    for p_ in pecas:
        p_.liso = False

    # ------------------------------------------------------------ componentes
    mot = C.motor_jgb37()
    Mz = M_esq[:3, :]
    xr = W / 2 + fe + Q.roda_folga                       # face de dentro da roda
    M_chave = C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (xch, y0, zch))
    M_drv = C.M([(1, 0, 0), (0, 0, 1), (0, -1, 0)], (lx, ly, zd1 + 5.0))
    comps += [
        Comp("motor-dir JGB37-520 + encoder", mot.translate([W / 2, 0, ze]), "corpo", MT.massa, "prata"),
        Comp("motor-esq JGB37-520 + encoder", mot.translate([W / 2, 0, ze]).transform(Mz), "corpo", MT.massa, "prata"),
        Comp("adaptador-dir sextavado 12 mm", C.adaptador_hex().translate([xr, 0, ze]), "corpo", P.HEX12.massa, "prata"),
        Comp("adaptador-esq sextavado 12 mm", C.adaptador_hex().translate([xr, 0, ze]).transform(Mz), "corpo", P.HEX12.massa, "prata"),
        Comp("roda-dir 85 mm", C.roda_sextavada().translate([xr, 0, ze]), "corpo", RD.massa, "preto"),
        Comp("roda-esq 85 mm", C.roda_sextavada().translate([xr, 0, ze]).transform(Mz), "corpo", RD.massa, "preto"),
        Comp("bola 40 mm (apoio de trás)", C.bola().translate([bx_, byb, rb]), "corpo", P.BOLA40.massa, "branco"),
        Comp("bateria 3x18650 (3S)", C.modulo(P.BATERIA3S).translate([0, by, zc]), "corpo", P.BATERIA3S.massa_suporte + 3 * P.BATERIA3S.massa_celula, "prata"),
        Comp("chave", C.chave().transform(M_chave[:3, :]), "corpo", 3.0, "preto"),
        sp.comp,
        Comp("Arduino Uno + shield", C.placa_eletronica(P.UNO).translate([ux, uy, zd1 + 5]), "corpo", P.UNO.massa + 20, "azul"),
        Comp("driver L298N", C.driver().transform(M_drv[:3, :]), "corpo", P.L298N.massa, "azul"),
        Comp("alto-falante (fase 2)", C.falante().rotate([0, 0, 180]).translate([0, yw + 0.2, fz]), "corpo", P.FALANTE.massa, "preto", fase2=True),
    ] + hd.comps
    sx_, sy_ = sp.xy
    z1_, z2_ = Q.dentes
    juntas = {"pan": Junta("corpo", (0, AY, 0), (0, 0, 1), Q.pan),
              "cabeca": Junta("pan", (0, AY, ZT), (1, 0, 0), Q.tilt),
              "eng": Junta("corpo", (sx_, sy_, 0), (0, 0, 1), (-Q.pan[1] / 2, -Q.pan[0] / 2))}

    def pose(nome, pan=0.0, tilt=0.0):
        return (nome, {"pan": pan, "eng": -pan * z1_ / z2_, "cabeca": tilt})

    poses = [pose("neutra"), pose("pan+170", Q.pan[1]), pose("pan-170", Q.pan[0]), pose("pan+90", 90.0), pose("pan-90", -90.0),
             pose("tilt-cima", 0.0, Q.tilt[1]), pose("tilt-baixo", 0.0, Q.tilt[0]),
             pose("pan+90+tilt-baixo", 90.0, Q.tilt[0]), pose("pan-90+tilt-cima", -90.0, Q.tilt[1]),
             pose("pan+170+tilt-baixo", Q.pan[1], Q.tilt[0]), pose("pan+170+tilt-cima", Q.pan[1], Q.tilt[1])]
    xa_ = xr + RD.larg / 2
    apoios = [(xa_, 0.0), (-xa_, 0.0), (bx_, byb)]
    encaixes = [{"par": ["engrenagem-servo", "servo-pan MG996R"], "motivo": "horn do servo fica no rebaixo da engrenagem"}]
    Zd, nZ, nY, Xd, nX = (0, 0, 1), (0, 0, -1), (0, -1, 0), (1, 0, 0), (-1, 0, 0)
    n_lid = "lidar LD19 (fase 2)"
    cab = hd.nomes + ["garfo", n_lid]
    topo = ["tronco", "alto-falante (fase 2)", "tubo-pescoco", "engrenagem-pescoco"] + cab
    no_deck = ["servo-pan MG996R", "Arduino Uno + shield", "driver L298N", "step-down 5V (XL4015)", "ubec 6V 3A dos servos"]
    ordem = [
        dict(passo="base-rodas", move=["base-rodas"], dir=Zd),
        dict(passo="motor direito com a flange, pela lateral (6 M3x6 + 4 M3x10)", move=["motor-dir JGB37-520 + encoder", "flange-motor#0"], dir=Xd, curso=90),
        dict(passo="motor esquerdo com a flange, pela lateral", move=["motor-esq JGB37-520 + encoder", "flange-motor#1"], dir=nX, curso=90),
        dict(passo="roda direita com o adaptador sextavado", move=["adaptador-dir sextavado 12 mm", "roda-dir 85 mm"], dir=Xd, curso=60),
        dict(passo="roda esquerda com o adaptador sextavado", move=["adaptador-esq sextavado 12 mm", "roda-esq 85 mm"], dir=nX, curso=60),
        dict(passo="bola e capa, por baixo (4 M3x8)", move=["bola 40 mm (apoio de trás)", "capa-esfera"], dir=nZ, curso=60),
        dict(passo="carregador USB-C e BMS no piso", move=["carregador USB-C 3S", "bms 3S 10A"], dir=Zd, curso=90),
        dict(passo="chave (por fora, atrás)", move=["chave"], dir=nY, curso=40),
        dict(passo="bateria no alçapão, por baixo (4 M3x8)", move=["tampa-bateria", "bateria 3x18650 (3S)"], dir=nZ, curso=60),
        dict(passo="servo de pan, Uno, L298N, step-down e UBEC no deck (bancada)", move=no_deck, dir=Zd, curso=80, contra=["deck"]),
        dict(passo="engrenagem do servo no horn (bancada)", move=["engrenagem-servo"], dir=Zd, curso=60, contra=["deck"] + no_deck),
        dict(passo="deck montado sobre a base", move=["deck", "engrenagem-servo"] + no_deck, dir=Zd, curso=120),
    ] + hd.bancada + [
        dict(passo="alto-falante nos trilhos do tronco, por baixo (bancada)", move=["alto-falante (fase 2)"], dir=nZ, curso=80, contra=["tronco"]),
        dict(passo="tubo do pescoço no tronco, por cima (bancada)", move=["tubo-pescoco"], dir=Zd, contra=["tronco"]),
        dict(passo="engrenagem do pescoço por dentro do tronco (bancada)", move=["engrenagem-pescoco"], dir=nZ, contra=["tronco", "tubo-pescoco"]),
        dict(passo="cabeça sobre o tubo; 3 tirantes M3 por dentro do tronco (bancada)", move=hd.nomes + ["garfo"], dir=Zd, curso=160, contra=["tronco", "tubo-pescoco", "engrenagem-pescoco"]),
        dict(passo="LiDAR no topo da cabeça (fase 2)", move=[n_lid], dir=Zd, curso=60, contra=hd.nomes),
        dict(passo="tronco + pescoço + cabeça sobre o deck; 4 M3x12 por baixo da base", move=topo, dir=Zd, curso=180),
        dict(passo="abrir: alçapão com a bateria sai por baixo", move=["tampa-bateria", "bateria 3x18650 (3S)"], dir=nZ, curso=60, sai=True),
        dict(passo="abrir: motor direito sai pela lateral (roda, depois flange + motor)", move=["adaptador-dir sextavado 12 mm", "roda-dir 85 mm", "motor-dir JGB37-520 + encoder", "flange-motor#0"], dir=Xd, curso=90, sai=True),
        dict(passo="abrir: tronco + pescoço + cabeça saem por cima (placas do deck à mostra)", move=topo, dir=Zd, curso=180, sai=True),
    ]
    obs = {"peca_teste_negativo": "quadro-cabeca",
           "explode_grupo": {"cabeca": (0, 20, 170), "pan": (0, 0, 90), "eng": (0, 60, 40)},
           "altura_mm": round(hd.topo_z, 1), "altura_com_lidar_mm": round(hd.topo_z + ld.cx[2], 1),
           "largura_total_mm": round(2 * (xr + RD.larg), 1), "bitola_mm": round(2 * xa_, 1), "entre_eixos_mm": round(-byb, 1),
           "vao_livre_mm": {"piso": zc, "capa_da_bola": zc - 12.0},
           "energia": "pack 3S (12 V): XL4015 → 5 V do Pi; UBEC → 6 V dos 2 MG996R; L298N → 2 motores JGB37 12 V; carregador USB-C 3S com balanceamento + BMS 3S"}
    mod = Modelo("cubo_rodas", "Robô quadrado que roda", pecas, comps, juntas, apoios, poses, ordem=ordem, obs=obs, encaixes=encaixes)
    # ------------------------------------------------------------ estabilidade: CG, margem e aceleração máxima sem tombar
    est, pior = QD.estabilidade(mod)
    v_max = MT.rpm / 60.0 * np.pi * RD.d / 1000.0
    n0 = est["neutra"]
    mod.obs["estabilidade"] = {
        "por_pose": est, "pior_a_max_m_s2": pior, "v_max_m_s": round(float(v_max), 2),
        "parada_min_m": round(float(v_max ** 2 / (2 * pior["frente"])), 3) if pior["frente"] > 0 else None,
        "texto": ("CG neutro em y=%.1f z=%.1f mm (massa %d g). Sem tombar, no pior caso de pose da cabeça: frear andando para a frente até %.2f m/s² (%.2f g), "
                  "arrancar para a frente / frear de ré até %.2f m/s² (%.2f g), curva até %.2f m/s² (%.2f g). A %.2f m/s (motor sem carga) a parada mais curta "
                  "sem tombar leva %.0f mm. Estimativa de corpo rígido (a = g·alcance/altura do CG): limite a rampa do firmware à metade disso."
                  % (n0["cg"][1], n0["cg"][2], n0["massa_g"], pior["frente"], pior["frente"] / 9.81, pior["tras"], pior["tras"] / 9.81,
                     min(pior["esq"], pior["dir"]), min(pior["esq"], pior["dir"]) / 9.81, v_max, 1000 * v_max ** 2 / (2 * max(pior["frente"], 1e-6)))),
    }
    return mod
