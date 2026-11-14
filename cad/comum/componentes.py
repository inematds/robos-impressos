"""Envelopes dos componentes comprados (caixas e cilindros com as medidas de cad/parametros.py).

Servem para duas coisas: (1) o verificador testa interferência entre peças impressas e componentes,
(2) os renders mostram onde cada componente vai. Cada função devolve o sólido num sistema LOCAL
documentado; quem monta aplica a matriz 4x4.
"""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum.geo import caixa, cil, uniao


def micro_servo(s=P.MICRO):
    """Local: eixo de saída em +Z, origem no eixo sobre a face de BAIXO da aba (face de apoio).
    Corpo comprido para +X (eixo a `eixo_da_ponta` da extremidade -X)."""
    L, W = s.corpo
    x0 = -s.eixo_da_ponta
    corpo = caixa(x0, x0 + L, -W / 2, W / 2, -s.base_ate_aba, 4.3 + s.aba_esp)
    cx = x0 + L / 2
    aba = caixa(cx - s.comp_abas / 2, cx + s.comp_abas / 2, -W / 2, W / 2, 0, s.aba_esp)
    ressalto = cil((0, 0, 4.3 + s.aba_esp), (0, 0, s.aba_ate_ponta - 3.2), 5.9)
    eixo = cil((0, 0, s.aba_ate_ponta - 3.2), (0, 0, s.aba_ate_ponta), 2.4)
    return uniao(corpo, aba, ressalto, eixo)


def servo_padrao(s=P.MG996R):
    """MG996R. Local: eixo em +Z, origem no eixo sobre a face de baixo da aba; corpo para +X."""
    L, W = s.corpo
    x0 = -s.eixo_da_ponta
    corpo = caixa(x0, x0 + L, -W / 2, W / 2, -s.base_ate_aba, s.topo_caixa - s.base_ate_aba)
    cx = x0 + L / 2
    aba = caixa(cx - s.comp_abas / 2, cx + s.comp_abas / 2, -W / 2, W / 2, 0, s.aba_esp)
    topo = s.aba_ate_topo_horn
    eixo = cil((0, 0, s.topo_caixa - s.base_ate_aba), (0, 0, topo - s.horn_esp), 3.0)
    horn = cil((0, 0, topo - s.horn_esp), (0, 0, topo), s.horn_d / 2)
    return uniao(corpo, aba, eixo, horn)


def motor_tt(t=P.TT, encoder=0.0):
    """Motor TT. Local: eixo de saída ao longo de X; origem no eixo sobre a face de apoio da caixa
    (x=0 encosta na parede; a caixa vai de x=0 a x=espessura; a roda fica em +X).
    O corpo cresce para +Z (motor para cima); a orelha fica em -Z."""
    Lc, W, E = t.caixa
    zf = -t.eixo_da_frente
    cx = caixa(0, E, -W / 2, W / 2, zf, zf + Lc)
    orelha = caixa(E / 2 - 2.5, E / 2 + 2.5, -5, 5, zf - t.orelha_alem, zf)
    ztopo = zf - t.orelha_alem + t.comp_total
    lata = cil((E / 2, 0, zf + Lc), (E / 2, 0, ztopo + encoder), t.lata_d / 2) ^ caixa(0, E, -W, W, zf, ztopo + encoder + 1)   # lata achatada: não passa da espessura da caixa
    eixo = cil((-t.eixo_saliente, 0, 0), (E + t.eixo_saliente, 0, 0), t.eixo_d / 2)
    return uniao(cx, orelha, lata, eixo)


def roda(r=P.RODA):
    """Roda. Local: eixo ao longo de X, face interna em x=0, face externa em x=largura."""
    return cil((0, 0, 0), (r.larg, 0, 0), r.d / 2, seg=64)


def placa_eletronica(b, pilha=None):
    """Uno ou Pi. Local: placa no plano XY, canto (0,0), componentes para +Z até a altura da pilha.
    O Pi tem envelope em degrau: baixo na maior parte e alto só nos blocos USB/Ethernet (x perto de 85)."""
    w, h = b.placa
    if hasattr(b, "bloco_usb"):
        return uniao(caixa(0, w, 0, h, 0, b.esp + b.altura_baixa), caixa(w - b.bloco_usb, w + 2.5, 0, h, 0, b.esp + b.altura_pilha))
    return caixa(0, w, 0, h, 0, b.esp + (pilha if pilha is not None else b.altura_pilha))


def bateria(b=P.BATERIA):
    """Suporte 2x18650. Local: centrado em XY, base em z=0; comprimento ao longo de Y."""
    L, W, H = b.cx
    return caixa(-W / 2, W / 2, -L / 2, L / 2, 0, H)


def driver(d=P.L298N):
    """L298N. Local: placa no plano XZ centrada, face de trás em y=0, componentes para +Y."""
    w, h = d.placa
    return caixa(-w / 2, w / 2, 0, d.altura, -h / 2, h / 2)


def esfera_apoio(e=P.ESFERA):
    from cad.comum.geo import esfera

    return esfera((0, 0, 0), e.d / 2, seg=48)


def chave(c=P.CHAVE):
    """Chave gangorra. Local: moldura em z<=0 (para fora do painel), corpo em +Z."""
    w, h = c.corpo
    rw, rh = c.recorte
    return uniao(caixa(-w / 2, w / 2, -h / 2, h / 2, -2.0, 0), caixa(-rw / 2 + 0.1, rw / 2 - 0.1, -rh / 2 + 0.1, rh / 2 - 0.1, 0, c.prof - 2.0))


def falante(f=P.FALANTE):
    """Alto-falante. Local: face da frente em y=0, corpo para -Y."""
    return uniao(cil((0, 0, 0), (0, -4, 0), f.d / 2), cil((0, -4, 0), (0, -f.prof, 0), f.d / 2 - 7))


def camera(c=P.CAMERA):
    """Câmera. Local: placa no plano XZ centrada, face de trás em y=0, lente para +Y."""
    w, h = c.placa
    return uniao(caixa(-w / 2, w / 2, 0, 1.2, -h / 2, h / 2), cil((0, 1.2, 0), (0, c.lente_alt, 0), c.lente_d / 2))


def tela35(t=P.TELA35):
    """Tela 3,5". Local: placa no plano XZ centrada, vidro em y=esp (frente = +Y)."""
    w, h = t.placa
    return caixa(-w / 2, w / 2, 0, t.esp_conjunto, -h / 2, h / 2)


def modulo(c):
    """Módulo eletrônico sem furo confiável (step-down, UBEC, carregador, BMS…): caixa `c.cx` = (comprimento, largura,
    altura). Local: centrado em XY, base em z=0, comprimento ao longo de X. Fixação: geo.berco_modulo (cantoneiras +
    abraçadeira). Ex.: Comp("step-down 5V", C.modulo(P.STEPDOWN5V).translate([x, y, z_do_piso]), "corpo", P.STEPDOWN5V.massa)."""
    L, W, H = c.cx
    return caixa(-L / 2, L / 2, -W / 2, W / 2, 0, H)


def M(R=None, t=(0, 0, 0)):
    """Matriz 4x4 a partir de colunas (para onde vão os eixos locais x, y, z) e translação."""
    m = np.eye(4)
    if R is not None:
        m[:3, :3] = np.array(R, float).T
    m[:3, 3] = t
    return m
