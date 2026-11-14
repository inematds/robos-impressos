"""Modelo 3: robô quadrado de mesa (~20 cm). Cabeça-cubo com tela de 3,5" e Raspberry Pi dentro,
pan ±170° (servo comum de 180° + engrenagens 2:1 impressas, cabos pelo tubo oco do pescoço) e tilt.
Não roda: a base guarda Arduino Uno + shield, bateria, alto-falante e o servo de pan."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import componentes as C
from cad.comum.base import furo, inserto, rasgo
from cad.comum.geo import caixa, casco, cil, engrenagem, espelho_x, prisma, ret_arredondado, secao, uniao
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot

Q = P.CUBO
F = P.FOLGA
S9 = P.MG996R


def construir() -> Modelo:
    pecas, comps = [], []
    W, Dp, H = Q.base
    y0, y1 = Q.base_y
    yc = (y0 + y1) / 2
    t = Q.parede
    AY, SY = Q.eixo_y, Q.servo_y
    zt0 = H - Q.tampa_esp                       # face de baixo da tampa

    # ------------------------------------------------------------ base (cuba) + tampa + porta traseira
    perfil = ret_arredondado(W, Dp, Q.base_r).translate([0, yc])
    perfil_i = ret_arredondado(W - 2 * t, Dp - 2 * t, Q.base_r - t).translate([0, yc])
    base = secao(perfil, "z", 0, zt0) - secao(perfil_i, "z", t, zt0 + 1)
    base = base - caixa(-W / 2 + 6, W / 2 - 6, y0 - 1, y0 + t + 0.01, t - 0.01, zt0 + 1)         # abertura da porta (sem soleira: a bateria desliza)
    cx, cyf, cyt = W / 2 - t - 5, y1 - t - 5, y0 + t + 5
    cantos = [(cx, cyf), (-cx, cyf), (cx, cyt), (-cx, cyt)]
    for (px, py) in cantos:                                                                      # 4 postes da tampa
        base = base + (caixa(px - 5, px + 5, py - 5, py + 5, t - 0.01, zt0) ^ secao(perfil, "z", 0, zt0))
    for (px, py) in cantos:
        base = base - inserto((px, py, zt0), (0, 0, -1))
    # postes do servo de pan (aba apoiada em z = piso + base_ate_aba)
    za = t + S9.base_ate_aba
    xcs = -S9.eixo_da_ponta + S9.corpo[0] / 2
    for sx in (1, -1):
        xf = xcs + sx * S9.furos_aba[0] / 2
        base = base + caixa(xf - 3.6, xf + 3.6, SY - 10, SY + 10, t - 0.01, za)
        for sy in (1, -1):
            base = base - furo((xf, SY + sy * S9.furos_aba[1] / 2, za + 0.01), (0, 0, -1), 14, F.m3_piloto)
    # Arduino Uno: 4 pilares (USB para a porta de trás)
    ux, uy = Q.uno_xy
    pos_uno = [(ux + yd, uy + x) for (x, yd) in P.UNO.furos]
    for (x, y) in pos_uno:
        base = base + cil((x, y, t - 0.01), (x, y, t + 5), 3.5, seg=24)
    for (x, y) in pos_uno:
        base = base - furo((x, y, t + 5.01), (0, 0, -1), 7, F.m3_piloto)
    # berço da bateria (2 guias baixas) — sai pela porta de trás
    bx, by = Q.bateria_xy
    Lb, Wb, Hb = P.BATERIA.cx
    base = base + caixa(bx + Wb / 2 + 0.6, bx + Wb / 2 + 2.6, by - Lb / 2, by + Lb / 2, t - 0.01, t + 6)
    base = base + caixa(bx - Wb / 2, bx + Wb / 2, by + Lb / 2 + 0.6, by + Lb / 2 + 2.6, t - 0.01, t + 6)
    # alto-falante (fase 2) na parede da frente: anel + grade
    fx, fz = Q.falante_xz
    rf = P.FALANTE.d / 2
    yw = y1 - t
    base = base + (cil((fx, yw - 5, fz), (fx, yw + 0.01, fz), rf + 2.6) - cil((fx, yw - 6, fz), (fx, yw + 0.02, fz), rf + 0.3))
    for dz in (-12, -6, 0, 6, 12):
        meia = np.sqrt(17.0 ** 2 - dz ** 2) - 1
        base = base - caixa(fx - meia, fx + meia, yw - 1, y1 + 1, fz + dz - 1.0, fz + dz + 1.0)
    # fase 2: 2 pontos universais no piso (regulador de 5 V, IMU) e passagem de ar
    base = base - BS.universal_z(52, -52, 0, t) - BS.universal_z(-20, 52, 0, t)

    tampa = secao(perfil, "z", zt0, H)
    tampa = tampa - cil((0, AY, zt0 - 1), (0, AY, H + 2), Q.tubo[0] / 2 + F.deslizante / 2 + 0.05)
    for (px, py) in cantos:
        tampa = tampa - furo((px, py, zt0 - 1), (0, 0, 1), 6, F.m3_passante) - cil((px, py, H - 2.0), (px, py, H + 0.01), F.m3_passante / 2, 3.4, seg=24)
    for xm in (-18, -6, 6, 18):                                                                   # microfones (fase 2)
        tampa = tampa - furo((xm, y1 - 14, zt0 - 1), (0, 0, 1), 6, 2.0)
    tampa = tampa - BS.universal_z(0, y1 - 26, zt0, H)

    porta = caixa(-W / 2 + 6.3, W / 2 - 6.3, y0, y0 + t, t + 0.6, zt0 - 0.3)
    porta = porta + caixa(-56, 56, y0 + t - 0.01, y0 + t + 2.0, t + 0.6, t + 4.0)             # pé que encaixa por dentro
    rw, rh = P.CHAVE.recorte
    xch, zch = -40.0, 40.0
    porta = porta - caixa(xch - rw / 2, xch + rw / 2, y0 - 1, y0 + t + 1, zch - rh / 2, zch + rh / 2)
    porta = porta - caixa(xch - rw / 2 - 3, xch + rw / 2 + 3, y0 + P.CHAVE.painel, y0 + t + 1, zch - rh / 2 - 3, zch + rh / 2 + 3)
    porta = porta - furo((xch + 26, y0 - 1, zch), (0, 1, 0), 6, P.JACK.furo_d)
    porta = porta - furo((45, y0 - 1, zt0 - 8), (0, 1, 0), 6, F.m3_passante)
    tampa = tampa + caixa(39, 51, y0 + t + 0.2, y0 + t + 8, zt0 - 14, zt0 + 0.01)                              # orelha que prende a porta
    tampa = tampa - inserto((45, y0 + t + 0.2, zt0 - 8), (0, 1, 0))
    # a porta fica presa por 1 parafuso M3 na orelha da tampa; embaixo ela encaixa pelo pé

    # ------------------------------------------------------------ pescoço: tubo com engrenagem + engrenagem do servo
    z1, z2 = Q.dentes
    m = Q.modulo
    ez0, ez1 = Q.eng_z
    dist = m * (z1 + z2) / 2
    assert abs(dist - (AY - SY)) < 1e-6, "distância entre eixos ≠ m*(z1+z2)/2"
    gz = Q.garfo_z
    tubo = cil((0, AY, ez0 - 2.2), (0, AY, gz[0] + 4.0), Q.tubo[0] / 2)
    eng_p = engrenagem(z1, m, ez0, ez1, folga=Q.eng_folga, fase=-np.pi / 2).translate([0, AY, 0])
    tubo = tubo + eng_p - cil((0, AY, 0), (0, AY, 200), Q.tubo[1] / 2)
    pos_par = [(10.5 * np.cos(np.radians(a)), AY + 10.5 * np.sin(np.radians(a))) for a in (90, 210, 330)]
    for (px, py) in pos_par:
        tubo = tubo - furo((px, py, 0), (0, 0, 1), 200, F.m3_passante) - cil((px, py, ez0 - 3), (px, py, ez0 - 2.2 + F.porca_m3_esp + 0.3), F.bolso_porca / 2 / np.cos(np.pi / 6), seg=6)
    eng_s = engrenagem(z2, m, ez0, ez1, folga=Q.eng_folga, fase=np.pi / 2 + np.pi / z2).translate([0, SY, 0])
    z_horn = za + S9.aba_ate_topo_horn
    eng_s = eng_s - cil((0, SY, ez0 - 1), (0, SY, z_horn + 0.2), S9.horn_d / 2 + 0.3) - furo((0, SY, 0), (0, 0, 1), 200, 6.5)
    for a in (0, 90, 180, 270):
        c, s_ = np.cos(np.radians(a)), np.sin(np.radians(a))
        eng_s = eng_s - rasgo((5.5 * c, SY + 5.5 * s_, 0), (9.0 * c, SY + 9.0 * s_, 0), 2.2, (0, 0, 1), 200)

    # ------------------------------------------------------------ garfo (gira com o pescoço)
    gy = Q.garfo_y / 2
    bx_, be = Q.garfo_braco
    ZT = Q.tilt_z
    garfo = caixa(-22, 22, AY - gy, AY + gy, gz[0], gz[1]) + caixa(-bx_ - be, bx_ + be, AY - gy, AY + gy, gz[0] + 2.0, gz[1])   # só o cubo central apoia na tampa
    braco = caixa(bx_, bx_ + be, AY - gy, AY + gy, gz[1] - 0.01, ZT) + cil((bx_, AY, ZT), (bx_ + be, AY, ZT), gy)
    garfo = garfo + braco + espelho_x(braco)
    garfo = garfo - cil((0, AY, gz[0] - 1), (0, AY, gz[0] + 4.2), Q.tubo[0] / 2 + 0.2) - cil((0, AY, 0), (0, AY, 200), Q.tubo[1] / 2)
    for (px, py) in pos_par:
        garfo = garfo - furo((px, py, 0), (0, 0, 1), 200, F.m3_passante) - cil((px, py, gz[1] - 3.0), (px, py, gz[1] + 1), F.cabeca_m3_d / 2, seg=24)
    garfo = garfo - cil((bx_ - 0.01, AY, ZT), (bx_ + 1.0, AY, ZT), S9.horn_d / 2 + 0.3) - furo((bx_ - 1, AY, ZT), (1, 0, 0), be + 2, 9.0)
    for a in (45, 135, 225, 315):
        c, s_ = np.cos(np.radians(a)), np.sin(np.radians(a))
        garfo = garfo - rasgo((bx_ - 1, AY + 5.5 * c, ZT + 5.5 * s_), (bx_ - 1, AY + 8.6 * c, ZT + 8.6 * s_), 2.2, (1, 0, 0), be + 2)
    garfo = garfo - furo((-bx_ - be - 1, AY, ZT), (1, 0, 0), be + 2, F.m3_passante)

    # ------------------------------------------------------------ cabeça: quadro (esqueleto) + corpo + face
    Wc, Dc, Hc = Q.cabeca
    pc = Q.cabeca_parede
    yb, yfr = AY - Dc / 2, AY + Dc / 2
    sec = ret_arredondado(Wc, Hc, Q.cabeca_r).translate([0, ZT])
    sec_i = ret_arredondado(Wc - 2 * pc, Hc - 2 * pc, Q.cabeca_r - pc).translate([0, ZT])
    sec_l = ret_arredondado(Wc - 2 * pc - 0.5, Hc - 2 * pc - 0.5, Q.cabeca_r - pc - 0.25).translate([0, ZT])
    sec_l2 = ret_arredondado(Wc - 2 * pc - 4.5, Hc - 2 * pc - 4.5, max(Q.cabeca_r - pc - 2.25, 1)).translate([0, ZT])
    corpo = secao(sec, "y", yb, yfr - 3.0) - secao(sec_i, "y", yb + pc, yfr)
    face = secao(sec, "y", yfr - 3.0, yfr) + (secao(sec_l, "y", yfr - 8.0, yfr - 2.99) - secao(sec_l2, "y", yfr - 9, yfr - 2.9))
    zs = ZT + Q.tela_dz
    aw, ah = P.TELA35.ativa
    face = face - caixa(-aw / 2 - 0.5, aw / 2 + 0.5, yfr - 10, yfr + 1, zs - ah / 2 - 0.5, zs + ah / 2 + 0.5)
    # câmera (fase 2) acima da tela + furos piloto M2
    zcam = ZT + 34.5
    face = face - furo((0, yfr - 10, zcam), (0, 1, 0), 12, 8.5)
    cfx, cfz = P.CAMERA.furos
    for sx in (1, -1):
        for sz in (1, -1):
            face = face + cil((sx * cfx / 2, yfr - 3.0 - 11.0, zcam + sz * cfz / 2), (sx * cfx / 2, yfr - 2.99, zcam + sz * cfz / 2), 2.4, seg=16)
    for sx in (1, -1):
        for sz in (1, -1):
            face = face - furo((sx * cfx / 2, yfr - 3.0 - 11.5, zcam + sz * cfz / 2), (0, 1, 0), 7, F.m2_piloto)
    # 4 parafusos da face (cabeça chata) em ressaltos dos cantos do corpo
    cxf, czf = Wc / 2 - pc - 8.0, Hc / 2 - pc - 8.0
    for sx in (1, -1):
        for sz in (1, -1):
            px, pz = sx * cxf, ZT + sz * czf
            res = caixa(px - 4.5, px + 4.5, yfr - 18.0, yfr - 8.2, pz - 4.5, pz + 4.5) + caixa(min(px, px + sx * 12), max(px, px + sx * 12), yfr - 18.0, yfr - 8.2, min(pz, pz + sz * 12), max(pz, pz + sz * 12))
            corpo = corpo + (res ^ secao(sec, "y", yb, yfr))
            corpo = corpo - inserto((px, yfr - 8.2, pz), (0, -1, 0))
            face = face - furo((px, yfr - 10, pz), (0, 1, 0), 12, F.m3_passante) - cil((px, yfr - 1.9, pz), (px, yfr + 0.01, pz), F.m3_passante / 2, 3.4, seg=24)
    # furos laterais do eixo do tilt, passagem dos cabos embaixo, microfones e ponto do LiDAR em cima (fase 2)
    corpo = corpo - furo((Wc / 2 - pc - 1, AY, ZT), (1, 0, 0), pc + 2, 14.0) - furo((-Wc / 2 - 1, AY, ZT), (1, 0, 0), pc + 2, F.m3_passante + 0.6)
    # o corpo entra por trás com o servo de tilt já no quadro: o furo do eixo vira um rasgo aberto para a frente,
    # e a face traz uma lingueta que fecha esse rasgo
    corpo = corpo - caixa(Wc / 2 - pc - 1, Wc / 2 + 1, AY, yfr, ZT - 7.0, ZT + 7.0)
    lingueta = caixa(Wc / 2 - pc + 0.15, Wc / 2, AY, yfr - 2.99, ZT - 6.75, ZT + 6.75) - cil((Wc / 2 - pc - 1, AY, ZT), (Wc / 2 + 1, AY, ZT), 7.4)
    face = face + lingueta
    corpo = corpo - caixa(-10, 10, AY - 26, AY - 14, ZT - Hc / 2 - 1, ZT - Hc / 2 + pc + 1)
    for xm in (-18, -6, 6, 18):
        corpo = corpo - furo((xm, yfr - 14, ZT + Hc / 2 - pc - 1), (0, 0, 1), pc + 2, 2.0)
    corpo = corpo - BS.universal_z(0, AY - 6, ZT + Hc / 2 - pc, ZT + Hc / 2) - furo((0, AY - 24, ZT + Hc / 2 - pc - 1), (0, 0, 1), pc + 2, 10.0)

    # quadro: travessa (segura o Pi) + lateral direita (servo de tilt) + lateral esquerda (eixo livre)
    x_aba = bx_ - S9.aba_ate_topo_horn                 # face de apoio da aba do servo de tilt
    y_pi = yfr - 3.2 - P.TELA35.acima_do_pi - P.PI.esp  # face de trás da placa do Pi
    yt1 = y_pi - 5.0                                    # face da frente da travessa (espaçadores de 5 mm)
    yt0 = yt1 - 3.0
    xe = -Wc / 2 + pc + 0.6                             # lateral esquerda encosta na parede
    trav = caixa(xe, x_aba, yt0, yt1, zs - 28.5, zs + 32)
    lat_d = caixa(x_aba - 4, x_aba, yb + pc + 0.3, yt1, ZT - 16, ZT + 16)
    lat_e = caixa(xe, xe + 4, yb + pc + 0.3, yt1, ZT - 12, ZT + 12)
    quadro = uniao(trav, lat_d, lat_e)
    jl, jw = S9.janela
    ycs = AY + S9.eixo_da_ponta - S9.corpo[0] / 2      # centro do corpo (corpo para trás)
    quadro = quadro - caixa(x_aba - 5, x_aba + 1, ycs - jl / 2, ycs + jl / 2, ZT - jw / 2, ZT + jw / 2)
    for sy in (1, -1):
        for sz in (1, -1):
            yy = ycs + sy * S9.furos_aba[0] / 2
            quadro = quadro - rasgo((x_aba - 5, yy - 1.5, ZT + sz * S9.furos_aba[1] / 2), (x_aba - 5, yy + 1.5, ZT + sz * S9.furos_aba[1] / 2), F.m3_passante, (1, 0, 0), 6)
    quadro = quadro - caixa(-S9.eixo_da_ponta + x_aba - S9.base_ate_aba - 0.6, x_aba + 0.1, yt0 - 1, AY + S9.eixo_da_ponta + 0.6, ZT - jw / 2, ZT + jw / 2)   # o corpo do servo atravessa a travessa
    quadro = quadro + cil((xe + 3.99, AY, ZT), (xe + 7.0, AY, ZT), 6.0) - inserto((xe, AY, ZT), (1, 0, 0))
    # Pi: 4 furos M2,5 passantes na travessa (espaçadores soltos de 5 mm)
    pos_pi = [(P.PI.placa[0] / 2 - x, zs - P.PI.placa[1] / 2 + y) for (x, y) in P.PI.furos]
    for (px, pz) in pos_pi:
        quadro = quadro - furo((px, yt0 - 1, pz), (0, 1, 0), 5, 2.9)
    quadro = quadro - caixa(-22, 14, yt0 - 1, yt1 + 1, zs - 16, zs + 12)          # alívio / passagem de cabos atrás do Pi
    # fixação do quadro no fundo do corpo: 4 blocos com inserto (parafusos pela parede de trás)
    pos_fundo = [(x_aba - 4.0, ZT + 11.5), (x_aba - 4.0, ZT - 11.5), (xe + 4.0, ZT + 8.0), (xe + 4.0, ZT - 8.0)]
    for (px, pz) in pos_fundo:
        s = 1 if px > 0 else -1
        quadro = quadro + caixa(min(px, px - s * 8), max(px, px - s * 8), yb + pc + 0.3, yb + pc + 9, pz - 4.5, pz + 4.5)
    for (px, pz) in pos_fundo:
        s = 1 if px > 0 else -1
        quadro = quadro - inserto((px - s * 4, yb + pc + 0.3, pz), (0, 1, 0))
        corpo = corpo - furo((px - s * 4, yb - 1, pz), (0, 1, 0), pc + 2, F.m3_passante)
    esp_pi = cil((0, 0, 0), (0, 0, 5.0), 3.0, seg=24) - cil((0, 0, -1), (0, 0, 6), 1.5, seg=16)
    mats_esp = [C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (px, yt1, pz)) for (px, pz) in pos_pi]

    pecas += [
        Peca("base", base, material="PETG", cor="grafite", macica=True, explode=(0, 0, -60), obs="cuba: piso, 3 paredes, postes do servo, do Uno e da tampa"),
        Peca("tampa-base", tampa, material="PETG", cor="grafite", macica=True, imprimir=rot("x", 180), explode=(0, 0, 25), obs="4 M3 cabeça chata; o garfo apoia e gira sobre ela; furos dos microfones"),
        Peca("porta-traseira", porta, material="PETG", cor="grafite", macica=True, imprimir=rot("x", 90), explode=(0, -70, -30),
             obs="porta da bateria com a chave e o conector de carga; 1 M3"),
        Peca("tubo-pescoco", tubo, material="PETG", cor="prata", grupo="pan", macica=True, explode=(0, 0, 45), obs="tubo oco (cabos) com a engrenagem de 22 dentes; 3 M3x35 + porcas"),
        Peca("engrenagem-servo", eng_s, material="PETG", cor="amarelo", grupo="eng", macica=True, explode=(0, -60, 45), obs="44 dentes, presa no horn redondo do servo de pan"),
        Peca("garfo", garfo, material="PETG", cor="grafite", grupo="pan", macica=True, imprimir=rot("x", 90), explode=(0, 0, 70), obs="gira com o pescoço e segura o eixo do tilt"),
        Peca("quadro-cabeca", quadro, material="PETG", cor="amarelo", grupo="cabeca", macica=True, imprimir=rot("x", 90), explode=(0, -20, 140),
             obs="esqueleto da cabeça: Pi (4 M2,5), servo de tilt, eixo livre; 4 M3 pelo fundo do corpo"),
        Peca("cabeca-corpo", corpo, cor="branco", grupo="cabeca", imprimir=rot("x", -90), suporte="não", explode=(0, -110, 140), obs="casca da cabeça (5 lados)"),
        Peca("cabeca-face", face, cor="preto", grupo="cabeca", imprimir=rot("x", 90), explode=(0, 90, 140), obs="moldura da tela de 3,5 pol.; 4 M3 cabeça chata"),
        Peca("espacador-pi", esp_pi, cor="cinza", grupo="cabeca", macica=True, copias=mats_esp, explode=(0, 30, 140), obs="4 espaçadores de 5 mm do Raspberry Pi"),
        BS.teste_encaixe(),
    ]
    pecas[-1].copias = []
    for p_ in pecas:
        p_.liso = False            # peças de faces planas: sem sombreamento suave no render

    # ------------------------------------------------------------ componentes
    M_pan = C.M([(1, 0, 0), (0, 1, 0), (0, 0, 1)], (0, SY, za))
    M_tilt = C.M([(0, -1, 0), (0, 0, -1), (1, 0, 0)], (x_aba, AY, ZT))
    comps += [
        Comp("servo-pan MG996R", C.servo_padrao().transform(M_pan[:3, :]), "corpo", S9.massa, "preto"),
        Comp("servo-tilt MG996R", C.servo_padrao().transform(M_tilt[:3, :]), "cabeca", S9.massa, "preto"),
        Comp("Arduino Uno + shield", C.placa_eletronica(P.UNO).transform(C.M([(0, 1, 0), (-1, 0, 0), (0, 0, 1)], (ux + P.UNO.placa[1], uy, t + 5))[:3, :]), "corpo", P.UNO.massa + 20, "azul"),
        Comp("bateria 2x18650", C.bateria().translate([bx, by, t]), "corpo", P.BATERIA.massa_suporte + 2 * P.BATERIA.massa_celula, "prata"),
        Comp("Raspberry Pi 4/5", C.placa_eletronica(P.PI).transform(C.M([(-1, 0, 0), (0, 0, 1), (0, 1, 0)], (P.PI.placa[0] / 2, y_pi, zs - P.PI.placa[1] / 2))[:3, :]), "cabeca", P.PI.massa, "verde"),
        Comp("tela 3,5 pol.", C.tela35().translate([0, yfr - 3.2 - P.TELA35.esp_conjunto, zs]), "cabeca", P.TELA35.massa, "ciano"),
        Comp("alto-falante (fase 2)", C.falante().translate([fx, yw - 0.2, fz]), "corpo", P.FALANTE.massa, "preto", fase2=True),
        Comp("camera (fase 2)", C.camera().translate([0, yfr - 3.0 - 11.0 - 1.3, zcam]), "cabeca", 4.0, "verde", fase2=True),
        Comp("chave", C.chave().transform(C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (xch, y0, zch))[:3, :]), "corpo", 3.0, "preto"),
    ]
    juntas = {"pan": Junta("corpo", (0, AY, 0), (0, 0, 1), Q.pan),
              "cabeca": Junta("pan", (0, AY, ZT), (1, 0, 0), Q.tilt),
              "eng": Junta("corpo", (0, SY, 0), (0, 0, 1), (-Q.pan[1] / 2, -Q.pan[0] / 2))}

    def pose(nome, pan=0.0, tilt=0.0):
        return (nome, {"pan": pan, "eng": -pan * z1 / z2, "cabeca": tilt})

    poses = [pose("neutra"), pose("pan+170", Q.pan[1]), pose("pan-170", Q.pan[0]), pose("pan+90", 90.0), pose("pan+37", 37.0),
             pose("tilt-cima", 0.0, Q.tilt[1]), pose("tilt-baixo", 0.0, Q.tilt[0]),
             pose("pan+120+tilt-baixo", 120.0, Q.tilt[0]), pose("pan-75+tilt-cima", -75.0, Q.tilt[1])]
    apoios = [(W / 2 - Q.base_r, y1 - 2), (-W / 2 + Q.base_r, y1 - 2), (W / 2 - 2, y1 - Q.base_r), (-W / 2 + 2, y1 - Q.base_r),
              (W / 2 - Q.base_r, y0 + 2), (-W / 2 + Q.base_r, y0 + 2), (W / 2 - 2, y0 + Q.base_r), (-W / 2 + 2, y0 + Q.base_r)]
    encaixes = [{"par": ["engrenagem-servo", "servo-pan MG996R"], "motivo": "horn do servo fica no rebaixo da engrenagem"}]
    Zd, Yd, nY = (0, 0, 1), (0, 1, 0), (0, -1, 0)
    miolo = ["quadro-cabeca", "servo-tilt MG996R", "Raspberry Pi 4/5", "tela 3,5 pol.", "espacador-pi"]
    cab = miolo + ["cabeca-corpo", "cabeca-face", "camera (fase 2)"]
    ordem = [
        dict(passo="base", move=["base"], dir=Zd),
        dict(passo="servo de pan", move=["servo-pan MG996R"], dir=Zd),
        dict(passo="Arduino Uno", move=["Arduino Uno + shield"], dir=Zd),
        dict(passo="engrenagem do servo", move=["engrenagem-servo"], dir=Zd),
        dict(passo="alto-falante (por dentro, contra a grade)", move=["alto-falante (fase 2)"], dir=nY, curso=40),
        dict(passo="bateria (pela porta de trás)", move=["bateria 2x18650"], dir=nY, curso=160),
        dict(passo="tampa + tubo do pescoço", move=["tampa-base", "tubo-pescoco"], dir=Zd),
        dict(passo="garfo", move=["garfo"], dir=Zd),
        dict(passo="porta traseira + chave", move=["porta-traseira", "chave"], dir=nY, curso=60),
        dict(passo="corpo da cabeça por trás do quadro (na bancada)", move=["cabeca-corpo"], dir=nY, curso=140, contra=miolo),
        dict(passo="face da cabeça (na bancada)", move=["cabeca-face", "camera (fase 2)"], dir=Yd, curso=60, contra=miolo + ["cabeca-corpo"]),
        dict(passo="cabeça entre os braços do garfo", move=cab, dir=Zd, curso=140),
    ]
    return Modelo("cubo", "Robô quadrado de mesa", pecas, comps, juntas, apoios, poses, ordem=ordem,
                  obs={"peca_teste_negativo": "quadro-cabeca", "explode_grupo": {"cabeca": (0, 20, 140), "pan": (0, 0, 45), "eng": (0, -60, 45)}}, encaixes=encaixes)
