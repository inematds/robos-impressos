#!/usr/bin/env python3
"""Esquema de ligação (SVG) dos bichos que rodam: dino e capivara. Um desenho só; o que muda entre eles vem de
<robô>.dados.json › "servos" (lista [chave sv_ do nome, pino do shield]) e dos textos sv_* do <robô>.pt.json.
As posições são fixas aqui. Os fios seguem a lista `ligacoes` do dados.json: mudou um, mude o outro.
Chamado por pagina_robo.py (comandos `esquema` e `pagina`)."""
from esquema_base import (AVISO, B_AZUL, B_CEL, B_CTRL, B_MOTOR, B_PECA, CINZA, COR, F_AZUL, F_CEL, F_CTRL, F_MOTOR,
                          F_NEUTRO, F_PECA, Desenho)

# pinos de sinal do driver L298N, da esquerda para a direita, e o conector do shield em que cada um entra
DRIVER = (("ENA", "D5"), ("IN1", "D4"), ("IN2", "D7"), ("IN3", "D8"), ("IN4", "D12"), ("ENB", "D6"))


def svg(X, R):
    t = X.t
    servos = R.d["servos"]                       # do pan (o último a ser desenhado) para os da cabeça e dos braços
    n = len(servos)
    y_pi = 756 + 34 * n + 22                     # o Raspberry Pi fica abaixo da coluna dos servos
    alt = y_pi + 80 + 216
    D = Desenho(760, alt, t("sv_titulo"), t("sv_aviso"))
    D.zona(10, 58, 740, y_pi + 80 + 14 - 58, t("sv_corpo"))

    # ---- fios (antes das caixas: as pontas ficam por baixo da borda)
    D.fio([(214, 106), (236, 106)], "v")
    D.fio([(314, 106), (340, 106)], "v")                                     # suporte + → fusível → B+
    D.fio([(214, 174), (340, 174)], "p")                                     # suporte − → B−
    D.fio([(214, 140), (340, 140)], "a")                                     # ponto do meio → BM
    D.fio([(326, 140), (326, 82), (548, 82), (548, 140), (570, 140)], "a")   # BM → carregador (meio)
    D.fio([(500, 174), (570, 174)], "p")                                     # P− → carregador −
    D.fio([(500, 106), (570, 106)], "v")                                     # P+ → carregador +
    D.fio([(555, 174), (555, 300), (160, 300), (160, 330)], "p")             # P− → GND geral → LM2596 IN−
    D.fio([(555, 300), (650, 300), (650, 330)], "p")                         # GND → UBEC IN−
    D.fio([(420, 300), (420, 330)], "p")                                     # GND → driver
    D.fio([(505, 106), (505, 222)], "v")                                     # P+ → chave
    D.fio([(505, 252), (505, 280), (110, 280), (110, 330)], "v")             # chave → LM2596 IN+
    D.fio([(505, 280), (600, 280), (600, 330)], "v")                         # → UBEC IN+
    D.fio([(370, 280), (370, 330)], "v")                                     # → driver (motores)
    D.fio([(160, 406), (160, 590)], "p")                                     # LM2596 OUT− → − do COM
    D.fio([(160, 448), (48, 448), (48, y_pi + 54), (110, y_pi + 54)], "p")   # OUT− → Raspberry Pi (pinos 6 e 9)
    D.fio([(110, 406), (110, 590)], "v")                                     # LM2596 OUT+ → + do COM
    D.fio([(110, 430), (34, 430), (34, y_pi + 26), (110, y_pi + 26)], "v")   # OUT+ → Raspberry Pi (pinos 2 e 4)
    D.fio([(110, 439), (330, 439)], "v")                                     # 5,1 V → +5V do driver
    D.fio([(640, 406), (640, 590)], "v")                                     # UBEC + → borne VCC
    D.fio([(716, 406), (716, 590)], "p")                                     # UBEC − → borne GND
    D.fio([(640, 540), (652, 540)], "v", 2.4)
    D.fio([(704, 540), (716, 540)], "p", 2.4)                                # capacitor nos 6 V
    D.fio([(510, 435), (536, 435)], "m", 5.0)                                # driver → motor direito (2 fios)
    D.fio([(510, 467), (536, 467)], "m", 5.0)                                # driver → motor esquerdo (2 fios)
    for i in range(6):
        D.fio([(350 + 30 * i, 500), (350 + 30 * i, 590)], "r", 2.6)          # 6 sinais do driver
    for i in range(n):                                                       # servos: o pino mais à direita liga na caixa de cima
        x, yc = 440 + 30 * (n - 1 - i), 769 + 34 * i
        D.fio([(x, 740), (x, yc), (576, yc)], "l", 4.4)
    D.fio([(200, 740), (200, y_pi)], "g")                                    # D0 (RX) ← pino 32 (TX)
    D.fio([(300, 740), (300, 772)], "z")
    D.fio([(300, 794), (300, y_pi)], "z")                                    # D1 (TX) → 1 kΩ → pino 33 (RX)
    D.fio([(300, 822), (326, 822)], "p", 2.4)
    D.fio([(388, 822), (400, 822)], "p", 2.4)                                # divisor: nó → 2 × 1 kΩ → GND
    D.fio([(400, 740), (400, y_pi)], "p")                                    # G ↔ pino 34 (GND)
    for x, y, c in ((326, 140, "a"), (505, 106, "v"), (555, 174, "p"), (555, 300, "p"), (420, 300, "p"), (505, 280, "v"),
                    (370, 280, "v"), (110, 439, "v"), (640, 540, "v"), (716, 540, "p"), (400, 822, "p")):
        D.no(x, y, c)

    # ---- bateria, proteção e carga
    D.caixa(24, 92, 190, 96)
    D.txt(34, 110, t("sv_suporte"), 12, peso=700)
    for y, k in ((120, "sv_cel1"), (152, "sv_cel2")):
        D.caixa(34, y, 92, 26, fundo=F_CEL, borda=B_CEL, raio=12)
        D.txt(80, y + 17, t(k), 11, anc="middle")
    D.txt(206, 110, "+", 14, anc="end", peso=700, cor=COR["v"])
    D.txt(206, 144, t("sv_meio"), 11, anc="end", cor="#8a6500", peso=700)
    D.txt(206, 179, "−", 14, anc="end", peso=700)
    D.caixa(236, 94, 78, 24, fundo=F_PECA, borda=B_PECA, raio=5)
    D.txt(275, 110, t("sv_fusivel"), 11, anc="middle", peso=600)
    D.caixa(340, 92, 160, 96)
    for y, a, b in ((110, "B+", "P+"), (144, "BM/B1", ""), (179, "B−", "P−/C−")):
        D.pino(347, y, a, anc="start")
        D.pino(493, y, b, anc="end")
    D.txt(440, 129, t("sv_bms"), 12, anc="middle", peso=700)
    D.txt(440, 158, t("sv_bms2"), 11, anc="middle", cor=CINZA)
    D.caixa(570, 92, 176, 96)
    for y, a, c in ((110, "B+", COR["v"]), (144, "BM", "#8a6500"), (179, "B−", "#1a1a22")):
        D.pino(577, y, a, anc="start", cor=c)
    D.txt(672, 129, t("sv_carregador"), 12, anc="middle", peso=700)
    D.txt(740, 162, t("sv_carregador2"), 9.5, anc="end", cor=CINZA)
    D.caixa(460, 222, 90, 30, fundo=F_NEUTRO)
    D.txt(505, 242, t("sv_chave"), 12, anc="middle", peso=700)
    D.txt(250, 273, t("sv_bat"), 11, anc="middle", cor=COR["v"], peso=600)

    # ---- conversores e driver
    D.caixa(60, 330, 240, 76)
    for x, a, b in ((110, "IN+", "OUT+"), (160, "IN−", "OUT−")):
        D.pino(x, 347, a)
        D.pino(x, 399, b)
    D.txt(240, 366, t("sv_lm"), 13, anc="middle", peso=700)
    D.txt(240, 383, t("sv_lm2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.caixa(330, 330, 180, 170)
    D.pino(370, 347, t("sv_l298_vs"))
    D.pino(420, 347, "GND")
    D.pino(336, 443, "+5V", anc="start")
    D.txt(425, 392, t("sv_l298"), 13, anc="middle", peso=700)
    D.txt(425, 409, t("sv_l298b"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.pino(503, 439, "OUT1/2", anc="end", tam=10)
    D.pino(503, 471, "OUT3/4", anc="end", tam=10)
    for i, (a, _) in enumerate(DRIVER):
        D.pino(350 + 30 * i, 494, a, tam=9.5)
    D.caixa(536, 421, 96, 28, fundo=F_MOTOR, borda=B_MOTOR)
    D.txt(584, 439, t("sv_mot_d"), 10.5, anc="middle", peso=700)
    D.caixa(536, 453, 96, 28, fundo=F_MOTOR, borda=B_MOTOR)
    D.txt(584, 471, t("sv_mot_e"), 10.5, anc="middle", peso=700)
    D.caixa(560, 330, 186, 76)
    D.pino(600, 347, "IN+")
    D.pino(650, 347, "IN−")
    D.pino(640, 399, "+", cor=COR["v"], tam=13)
    D.pino(716, 399, "−", tam=13)
    D.txt(700, 362, t("sv_ubec"), 13, anc="middle", peso=700)
    D.txt(700, 379, t("sv_ubec2"), 10.5, anc="middle", cor=AVISO, peso=600)
    D.txt(102, 416, t("sv_51"), 11, anc="end", cor=COR["v"], peso=600)
    D.txt(648, 500, t("sv_6"), 11, cor=COR["v"], peso=600)
    D.caixa(652, 529, 52, 22, fundo=F_AZUL, borda=B_AZUL, raio=5)
    D.txt(678, 544, t("sv_cap"), 10, anc="middle", peso=600)
    D.txt(678, 523, t("sv_capn"), 10.5, anc="middle", cor=B_AZUL, peso=600)
    D.caixa(98, 421, 76, 36, fundo=F_PECA, borda=B_PECA, raio=4)
    D.txt(326, 475, t("sv_emenda"), 9, anc="end", cor="#6b4e00", peso=600)

    # ---- Arduino + shield
    D.caixa(60, 590, 686, 150, fundo=F_CTRL, borda=B_CTRL)
    D.pino(110, 608, t("sv_5v"))
    D.pino(166, 608, "− (COM)")
    for i, (_, d) in enumerate(DRIVER):
        D.pino(350 + 30 * i, 608, d, tam=10)
    D.pino(640, 608, "VCC")
    D.pino(716, 608, "GND")
    D.txt(678, 624, t("sv_borne"), 10.5, anc="middle", cor=B_AZUL, peso=600)
    D.txt(345, 662, t("sv_shield"), 15, anc="middle", peso=700)
    D.txt(345, 682, t("sv_shield2"), 12, anc="middle", cor=AVISO, peso=600)
    D.pino(200, 731, "D0 (RX)")
    D.pino(300, 731, "D1 (TX)")
    D.pino(400, 731, "G")
    for i, (chave, pino) in enumerate(servos):
        x, yc = 440 + 30 * (n - 1 - i), 769 + 34 * i
        D.pino(x, 731, pino, tam=10)
        D.caixa(576, yc - 13, 170, 26, fundo=F_MOTOR, borda=B_MOTOR)
        D.txt(661, yc + 4, t(chave), 10, anc="middle", peso=700)
    # divisor da serial
    D.caixa(279, 772, 42, 22, fundo="#fff", raio=3)
    D.txt(300, 787, t("sv_r1"), 10.5, anc="middle", peso=600)
    D.caixa(288, 812, 24, 20, fundo=F_PECA, borda=B_PECA, raio=4)
    D.txt(282, 826, t("sv_b3"), 10.5, anc="end", cor="#6b4e00", peso=600)
    D.caixa(326, 811, 62, 22, fundo="#fff", raio=3)
    D.txt(357, 826, t("sv_r2"), 10.5, anc="middle", peso=600)

    # ---- Raspberry Pi
    D.caixa(110, y_pi, 420, 80, fundo="#e9f6ea", borda=B_CTRL)
    D.pino(200, y_pi + 17, "32 (TX)")
    D.pino(300, y_pi + 17, "33 (RX)")
    D.pino(400, y_pi + 17, "34 (GND)")
    D.pino(118, y_pi + 30, "+", anc="start", cor=COR["v"], tam=14)
    D.pino(118, y_pi + 59, "−", anc="start", tam=14)
    D.txt(134, y_pi + 30, t("sv_pi_mais"), 11, cor=CINZA)
    D.txt(134, y_pi + 59, t("sv_pi_menos"), 11, cor=CINZA)
    D.txt(450, y_pi + 52, t("sv_pi"), 14, anc="middle", peso=700)

    # ---- legenda
    D.legenda(y_pi + 80 + 36, [("v", t("sv_leg1")), ("p", t("sv_leg2")), ("a", t("sv_leg3")), ("gz", t("sv_leg4")), ("l", t("sv_leg5")),
                               ("r", t("sv_leg_r")), ("m", t("sv_leg_m")), ("", t("sv_leg6"))],
              [t("sv_leg7"), t("sv_leg8"), t("sv_leg9"), t("sv_leg9b"), t("sv_leg10"), t("sv_leg10b")])
    return D.svg()
