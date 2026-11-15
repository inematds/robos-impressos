#!/usr/bin/env python3
"""Esquema de ligação do robô quadrado que roda (id cubo_rodas), em dois desenhos empilhados:
1 · ENERGIA (pack 3S → proteção → chave → barra de emenda → conversores → placas) e 2 · SINAIS (shield ↔ driver ↔ motores
e encoders, servos, serial com o Raspberry Pi). As posições são fixas aqui; todo texto vem das chaves sv_* de
guia/src/robos/cubo-rodas.pt.json (traduzidas). Os fios seguem a lista `ligacoes` do cubo-rodas.dados.json: mudou um,
mude o outro. Chamado por pagina_robo.py › esquema (ROBOS["cubo-rodas"]["esquema"])."""
from esquema_base import (AVISO, B_AZUL, B_CEL, B_CTRL, B_MOTOR, B_PECA, B_PLACA, CINZA, COR, F_AZUL, F_CEL, F_CTRL, F_MOTOR, F_NEUTRO,
                          F_PECA, Desenho)

LARG, ALT = 760, 1825
Y1, Y2 = 26, 846          # deslocamento vertical de cada desenho


def borne(D, x, y, n):
    """Caixinha amarela numerada = um borne da barra de emenda (centro em x, topo em y)."""
    D.caixa(x - 12, y, 24, 20, fundo=F_PECA, borda=B_PECA, raio=4)
    D.txt(x, y + 14.5, str(n), 11, anc="middle", peso=700, cor="#6b4e00")


def energia(D, t):
    f, no = D.fio, D.no
    D.txt(20, 46, t("sv_p1"), 12, peso=700, cor=B_PLACA, extra=' letter-spacing="1"')
    D.zona(10, 58, 740, 228, t("sv_base"))
    D.zona(10, 296, 740, 330, t("sv_deck"))
    D.faixa(10, 634, 740, 28, "")
    D._faixas = [(610, 652, t("sv_pescoco"))]
    D.zona(10, 670, 740, 96, t("sv_cabeca"))
    # ---- fios da base
    f([(402, 106), (420, 106)], "v")
    f([(490, 106), (524, 106)], "v")                                      # suporte + → fusível → B+
    f([(402, 202), (524, 202)], "p")                                      # suporte − → B−
    f([(402, 138), (524, 138)], "a")
    f([(402, 170), (524, 170)], "a")                                      # 2 emendas → placa de proteção
    f([(232, 138), (174, 138)], "a")
    f([(232, 170), (174, 170)], "a")                                      # 2 emendas → carregador
    f([(674, 106), (708, 106), (708, 78), (200, 78), (200, 106), (174, 106)], "v")     # P+ → carregador B+
    f([(674, 202), (690, 202), (690, 236), (200, 236), (200, 202), (174, 202)], "p")   # P− → carregador B−
    f([(708, 106), (708, 246)], "v")                                      # P+ → chave
    f([(708, 274), (708, 310)], "v")                                      # chave → borne 4
    f([(640, 236), (640, 310)], "p")                                      # P− → borne 5
    # ---- fios do deck
    f([(640, 330), (640, 346), (185, 346)], "p")                          # borne 5 → barra do negativo
    f([(185, 346), (185, 376)], "p")                                      # → UBEC IN−
    f([(335, 346), (335, 376)], "p")                                      # → XL4015 IN−
    f([(585, 346), (585, 376)], "p")                                      # → driver GND
    f([(708, 330), (708, 376)], "v")                                      # borne 4 → driver +12V
    f([(708, 362), (95, 362), (95, 376)], "v")                            # → UBEC IN+
    f([(385, 362), (385, 376)], "v")                                      # → XL4015 IN+
    f([(335, 452), (335, 470)], "p")                                      # XL4015 OUT− → borne 2
    f([(385, 452), (385, 470)], "v")                                      # XL4015 OUT+ → borne 1
    f([(397, 480), (585, 480), (585, 452)], "v", 2.6)                     # borne 1 → +5V do driver
    f([(95, 452), (95, 540)], "v")
    f([(185, 452), (185, 540)], "p")                                      # UBEC → borne azul do shield
    f([(95, 501), (107, 501)], "v", 2.4)
    f([(173, 501), (185, 501)], "p", 2.4)                                 # capacitor nos 6 V
    f([(335, 490), (335, 540)], "p")
    f([(385, 490), (385, 540)], "v")                                      # bornes 2 e 1 → COM do shield
    f([(385, 520), (470, 520), (470, 694)], "v")                          # borne 1 → pescoço → pinos 2 e 4
    f([(323, 480), (266, 480), (266, 694)], "p")                          # borne 2 → pescoço → pinos 6 e 9
    f([(530, 724), (560, 724)], "c", 9)                                   # tela ligada ao Pi por cabos
    for x, y, c in ((708, 106, "v"), (640, 236, "p"), (335, 346, "p"), (585, 346, "p"), (708, 362, "v"), (385, 362, "v"),
                    (95, 501, "v"), (185, 501, "p"), (385, 520, "v")):
        no(x, y, c)
    D.rotulos_das_faixas()
    # ---- caixas da base
    D.caixa(24, 92, 150, 124)
    D.txt(92, 144, t("sv_carregador"), 12, anc="middle", peso=700)
    D.txt(92, 160, t("sv_carregador2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.pino(167, 110, "B+", "end", COR["v"])
    D.pino(167, 206, "B−", "end")
    D.caixa(232, 92, 170, 124)
    D.txt(317, 108, t("sv_suporte"), 12, anc="middle", peso=700)
    for y, k in ((116, "sv_cel1"), (148, "sv_cel2"), (180, "sv_cel3")):
        D.caixa(272, y, 90, 24, fundo=F_CEL, borda=B_CEL, raio=12)
        D.txt(317, y + 16, t(k), 11, anc="middle")
    D.pino(395, 110, "+", "end", COR["v"], 14)
    D.pino(395, 206, "−", "end", tam=14)
    D.caixa(420, 94, 70, 24, fundo=F_PECA, borda=B_PECA, raio=5)
    D.txt(455, 110, t("sv_fusivel"), 10.5, anc="middle", peso=600)
    D.caixa(524, 92, 150, 124)
    for y, a in ((110, "B+"), (206, "B−")):
        D.pino(531, y, a, "start")
    D.txt(516, 131, "≈ 8 V", 10.5, anc="end", cor="#8a6500", peso=700)       # sobre o fio de cada emenda
    D.txt(516, 163, "≈ 4 V", 10.5, anc="end", cor="#8a6500", peso=700)
    D.pino(667, 110, "P+", "end")
    D.pino(667, 206, "P−", "end")
    D.txt(599, 152, t("sv_bms"), 12, anc="middle", peso=700)
    D.txt(599, 168, t("sv_bms2"), 11, anc="middle", cor=CINZA)
    D.caixa(670, 246, 76, 28, fundo=F_NEUTRO)
    D.txt(708, 265, t("sv_chave"), 12, anc="middle", peso=700)
    D.txt(238, 133, "≈ 8 V", 10.5, anc="start", cor="#8a6500", peso=700)       # dentro do suporte, lado do carregador
    D.txt(238, 165, "≈ 4 V", 10.5, anc="start", cor="#8a6500", peso=700)
    # ---- caixas do deck
    borne(D, 708, 310, 4)
    borne(D, 640, 310, 5)
    D.caixa(60, 376, 200, 76)
    D.pino(95, 393, "IN+")
    D.pino(185, 393, "IN−")
    D.pino(95, 445, "+", cor=COR["v"], tam=13)
    D.pino(185, 445, "−", tam=13)
    D.txt(140, 414, t("sv_ubec"), 13, anc="middle", peso=700)
    D.txt(140, 430, t("sv_ubec2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.caixa(300, 376, 230, 76)
    D.pino(335, 393, "IN−")
    D.pino(385, 393, "IN+")
    D.pino(335, 445, "OUT−")
    D.pino(385, 445, "OUT+")
    D.txt(462, 414, t("sv_xl"), 13, anc="middle", peso=700)
    D.txt(462, 430, t("sv_xl2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.caixa(550, 376, 200, 76)
    D.pino(585, 393, "GND")
    D.pino(708, 393, "+12V")
    D.pino(585, 445, "+5V")
    D.txt(668, 420, t("sv_l298"), 13, anc="middle", peso=700)
    D.txt(668, 436, t("sv_l2982"), 10.5, anc="middle", cor=AVISO, peso=600)
    borne(D, 335, 470, 2)
    borne(D, 385, 470, 1)
    D.txt(410, 474, t("sv_51"), 11, cor=COR["v"], peso=600)
    D.txt(87, 472, t("sv_6"), 11, anc="end", cor=COR["v"], peso=600)
    D.caixa(107, 490, 66, 22, fundo=F_AZUL, borda=B_AZUL, raio=5)
    D.txt(140, 505, t("sv_cap"), 10.5, anc="middle", peso=600)
    D.txt(140, 485, t("sv_capn"), 10.5, anc="middle", cor=B_AZUL, peso=600)
    D.caixa(40, 540, 210, 62, fundo=F_CTRL, borda=B_CTRL)
    D.pino(95, 557, "VCC")
    D.pino(185, 557, "GND")
    D.txt(145, 578, t("sv_azul"), 11.5, anc="middle", peso=700)
    D.txt(145, 593, t("sv_azul2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.caixa(276, 540, 188, 62, fundo=F_CTRL, borda=B_CTRL)
    D.pino(335, 557, "−", tam=13)
    D.pino(385, 557, "+", cor=COR["v"], tam=13)
    D.txt(370, 578, t("sv_com"), 11.5, anc="middle", peso=700)
    D.txt(370, 593, t("sv_com2"), 10.5, anc="middle", cor=CINZA)
    # ---- cabeça
    D.caixa(200, 694, 330, 60, fundo="#e9f6ea", borda=B_CTRL)
    D.pino(266, 711, t("sv_pignd"))
    D.pino(470, 711, t("sv_pi5v"))
    D.txt(365, 741, t("sv_pi"), 14, anc="middle", peso=700)
    D.caixa(560, 694, 180, 60, fundo=F_NEUTRO)
    D.txt(650, 720, t("sv_tela"), 11.5, anc="middle", peso=700)
    D.txt(650, 737, t("sv_tela2"), 10.5, anc="middle", cor=CINZA)


def sinais(D, t):
    f, no = D.fio, D.no
    D.txt(20, 14, t("sv_p2"), 12, peso=700, cor=B_PLACA, extra=' letter-spacing="1"')
    D.zona(10, 24, 740, 108, t("sv_base"))
    D.zona(10, 140, 740, 470, "")
    D.txt(232, 158, t("sv_deck"), 11, cor="#6b7080", peso=700, extra=' letter-spacing="1.5"')
    D.faixa(10, 618, 740, 28, "")
    D._faixas = [(495, 636, t("sv_pescoco"))]
    D.zona(10, 654, 740, 108, t("sv_cabeca"))
    # pinos do cabo de 6 fios: (x no motor direito, x no motor esquerdo, cor do fio, chave do nome)
    cabo = ((46, 714, "a", "sv_am"), (80, 680, "g", "sv_vd"), (114, 646, "z", "sv_az"), (148, 612, "p", "sv_pt"), (182, 578, "c", "sv_br"), (214, 546, "v", "sv_vm"))
    # ---- motores → driver (energia do motor e do encoder) e encoders → shield
    for (xd, xe, c, _), y in zip(cabo[2:], (275, 245, 215, 190)):
        f([(xd, 120), (xd, y), (270, y)], c)
        f([(xe, 120), (xe, y), (490, y)], c)
    for xd, xe, c, _ in cabo[:2]:
        f([(xd, 120), (xd, 400)], c)
        f([(xe, 120), (xe, 400)], c)
    pinos_drv = ((300, "ENA", "D5"), (332, "IN1", "D4"), (364, "IN2", "D7"), (396, "IN3", "D8"), (428, "IN4", "D12"), (460, "ENB", "D6"))
    for x, _, _ in pinos_drv:
        f([(x, 320), (x, 400)], "r")                                     # 6 sinais do driver
    # ---- shield → pescoço → cabeça
    f([(150, 510), (150, 686)], "g")                                      # D0 (RX) ← pino 32 (TX)
    f([(250, 510), (250, 532)], "z")
    f([(250, 554), (250, 686)], "z")                                      # D1 (TX) → 1 kΩ → pino 33 (RX)
    f([(250, 582), (276, 582)], "p", 2.4)
    f([(338, 582), (350, 582)], "p", 2.4)                                 # divisor: nó → 2 × 1 kΩ → GND
    f([(350, 510), (350, 686)], "p")                                      # G ↔ pino 34 (GND)
    f([(640, 510), (640, 690)], "l", 4.4)                                 # D10 → pescoço → servo de tilt
    f([(700, 510), (700, 540)], "l", 4.4)                                 # D9 → servo de pan
    no(350, 582, "p")
    D.rotulos_das_faixas()
    # ---- motores
    for x0, k, lado in ((24, "sv_motd", 0), (516, "sv_mote", 1)):
        D.caixa(x0, 44, 220, 76, fundo=F_MOTOR, borda=B_MOTOR)
        D.txt(x0 + 110, 62, t(k), 12, anc="middle", peso=700)
        D.txt(x0 + 110, 76, t("sv_cabo6"), 10.5, anc="middle", cor=CINZA)
        for i, p in enumerate(cabo):
            D.txt(p[lado], 100 if i % 2 == 0 else 113, t(p[3]), 10, anc="middle", peso=600)
    # ---- driver
    D.caixa(270, 170, 220, 150)
    for y, a, b in ((194, "OUT1", "OUT3"), (219, "OUT2", "OUT4"), (249, "GND", "GND"), (279, "+5V", "+5V")):
        D.pino(277, y, a, "start")
        D.pino(483, y, b, "end")
    D.txt(380, 226, t("sv_l298"), 12.5, anc="middle", peso=700)
    D.txt(380, 243, t("sv_l298b2"), 10.5, anc="middle", cor=AVISO, peso=600)
    for x, a, _ in pinos_drv:
        D.pino(x, 312, a, tam=10.5)
    # ---- shield
    D.caixa(24, 400, 712, 110, fundo=F_CTRL, borda=B_CTRL)
    for x, a in ((46, "D2"), (80, "A0"), (680, "A1"), (714, "D3")):
        D.pino(x, 417, a)
    for x, _, a in pinos_drv:
        D.pino(x, 417, a, tam=10.5)
    D.txt(380, 452, t("sv_shield"), 15, anc="middle", peso=700)
    D.txt(380, 471, t("sv_shield2"), 11.5, anc="middle", cor=AVISO, peso=600)
    for x, a in ((150, "D0 (RX)"), (250, "D1 (TX)"), (350, "G"), (640, "D10"), (700, "D9")):
        D.pino(x, 502, a)
    D.caixa(229, 532, 42, 22, fundo="#fff", raio=3)
    D.txt(250, 547, t("sv_r1"), 10.5, anc="middle", peso=600)
    D.caixa(238, 572, 24, 20, fundo=F_PECA, borda=B_PECA, raio=4)
    D.txt(250, 586.5, "3", 11, anc="middle", peso=700, cor="#6b4e00")
    D.caixa(276, 571, 62, 22, fundo="#fff", raio=3)
    D.txt(307, 586, t("sv_r2"), 10.5, anc="middle", peso=600)
    D.caixa(652, 540, 94, 44, fundo=F_MOTOR, borda=B_MOTOR)
    D.txt(699, 566, t("sv_pan"), 11, anc="middle", peso=700)
    D.txt(632, 604, t("sv_ext"), 11, anc="end", cor=B_MOTOR, peso=600)
    # ---- cabeça
    D.caixa(90, 686, 330, 64, fundo="#e9f6ea", borda=B_CTRL)
    for x, a in ((150, "32 (TX)"), (250, "33 (RX)"), (350, "34 (GND)")):
        D.pino(x, 703, a)
    D.txt(255, 736, t("sv_pi"), 14, anc="middle", peso=700)
    D.caixa(573, 690, 134, 44, fundo=F_MOTOR, borda=B_MOTOR)
    D.txt(640, 716, t("sv_tilt"), 10.5, anc="middle", peso=700)


def svg(X, R=None):
    t = X.t
    D = Desenho(LARG, ALT, t("sv_titulo"), t("sv_aviso"))
    for dy, desenho in ((Y1, energia), (Y2, sinais)):
        D.o.append(f'<g transform="translate(0,{dy})">')
        D._faixas = []
        desenho(D, t)
        D.o.append("</g>")
    D.legenda(Y2 + 790, [("v", t("sv_leg1")), ("p", t("sv_leg2")), ("a", t("sv_leg3")), ("gz", t("sv_leg4")), ("l", t("sv_leg5")), ("r", t("sv_leg6")),
                         ("", t("sv_leg7"))],
              [t("sv_leg8"), t("sv_leg8b"), t("sv_leg9"), t("sv_leg10"), t("sv_leg11"), t("sv_leg12")])
    return D.svg()
