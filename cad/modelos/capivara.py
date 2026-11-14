"""Modelo 2: capivara filhote sentada (~32 cm). Mesmo esqueleto do dino (chassi, bandejas, garfo, berço).
Rodas dentro das coxas (aro ciano na lateral), esfera de apoio dentro do rabo redondo.
Movimentos preparados: pescoço pan + tilt e boca. Braços parados (fazem parte da casca)."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import bicho as BI
from cad.comum.base import B, CX, CY, CZ, F, N
from cad.comum.geo import caixa, casco, cil, elipsoide, esfera, espelho_x, limites, medir_parede, prisma, uniao
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot

K = P.CAPIVARA


def construir() -> Modelo:
    pecas, comps = [], []
    p_torso = BI.pele_torso(K.torso, h=K.passo)
    p_cab = BI.pele_blobs(K.cabeca, k=14, h=K.passo)
    p_perna = BI.pele_blobs(K.perna, k=14, h=K.passo)
    p_rabo = BI.pele_blobs(K.rabo, k=10, h=K.passo)
    t_gordo = BI.gordo(p_torso)

    # ------------------------------------------------------------ torso + painel da frente
    frente, costas, t_ext, t_int = BI.torso(p_torso)
    xs_pino = p_torso.ponto_na_pele((0, B.costura_y, 100.0), (1, 0, 0))[0] - F.parede - 1.0
    xg = N.gola_r - F.parede - 6.5
    frente, costas, mats_pino = BI.pinos_torso(frente, costas, t_ext, t_int, [(xs_pino - 3, 100.0), (-xs_pino + 3, 100.0), (xg, CZ - 2), (-xg, CZ - 2)])
    costas = BI.parafuso_costas_deck(costas, t_ext)
    frente, costas, barriga, c_fal = BI.frente_com_painel(p_torso, frente, costas, t_ext, t_int, K.barriga.c, K.barriga.r,
                                                          faixas=False, y_raio=-14.0, bracos=False, z_mic=K.barriga.c[1] + K.barriga.r[1] + 30)
    comps.append(c_fal)

    # mãos marrons (domos colados na ponta dos braços)
    mats_mao = []
    for s in (1, -1):
        p = p_torso.ponto_na_pele((s * 50, 14, 98), (0, 0.9, -0.3))
        frente, Mm = BI.bolso_unha(frente, t_ext, p, (0, 0.9, -0.3), r=10.0)
        mats_mao.append(Mm)

    # bandana verde: faixa em volta da esfera do pescoço (2 metades coladas) + triângulo na frente + laço atrás
    g2 = p_torso.deslocado(1.8)
    g0 = p_torso.deslocado(0.2)
    cascao = (g2 - g0) ^ esfera((CX, CY, CZ), N.gola_r + K.junta - 0.8, seg=96)
    faixa = caixa(-200, 200, -300, 300, CZ - 24, CZ - 3)
    tri = prisma([(-36, CZ - 10), (36, CZ - 10), (0, 135)], "y", 0, 200)
    band_f = ((g2 - g0) ^ tri) + (cascao ^ faixa ^ caixa(-200, 200, B.costura_y + 0.2, 300, 0, 400))
    for (dx, dz) in ((0, -5), (-7, 4), (0, 8), (7, 4)):      # patinha (4 covinhas para pintar de branco)
        pp = p_torso.ponto_na_pele((dx, -14, 150 + dz), (0, 1, 0))
        band_f = band_f - esfera(pp + np.array([0, 1.8, 0]), 3.4 if dz == -5 else 2.4, seg=20)
    band_t = cascao ^ faixa ^ caixa(-200, 200, -300, B.costura_y - 0.2, 0, 400)
    yb = p_torso.ponto_na_pele((0, -46, CZ - 14), (0, -1, 0))[1]
    laco = uniao(elipsoide((0, yb - 4, CZ - 14), (8, 6, 7), seg=32),
                 casco(esfera((-5, yb - 3, CZ - 16), 4, seg=16), elipsoide((-22, yb - 2, CZ - 34), (8, 4, 10), seg=24)),
                 casco(esfera((5, yb - 3, CZ - 16), 4, seg=16), elipsoide((22, yb - 2, CZ - 34), (8, 4, 10), seg=24)),
                 casco(esfera((-5, yb - 3, CZ - 12), 4, seg=16), elipsoide((-24, yb - 3, CZ - 4), (9, 4, 6), seg=24)),
                 casco(esfera((5, yb - 3, CZ - 12), 4, seg=16), elipsoide((24, yb - 3, CZ - 4), (9, 4, 6), seg=24)))
    band_t = band_t + (laco - g0)
    # o laço não pode entrar na zona varrida pela cabeça: corta tudo o que passa da esfera da junta acima do equador
    zona_cabeca = esfera((CX, CY, CZ), 400, seg=32) - esfera((CX, CY, CZ), N.gola_r + K.junta - 0.8, seg=96)
    band_t = band_t - (zona_cabeca ^ caixa(-200, 200, -300, 300, CZ - 12, 400))

    pecas += [
        Peca("torso-frente", frente, cor="laranja", imprimir=rot("x", 90), suporte="sim (árvore, por dentro)", explode=(0, 110, 0),
             obs="metade da frente; 1 M3 por baixo + 2 M3 cabeça chata nos postes (sob o painel)"),
        Peca("torso-costas", costas, cor="laranja", imprimir=rot("x", -90), suporte="sim (árvore, por dentro)", explode=(0, -130, 0),
             obs="metade de trás (tampa de acesso às bandejas); 2 M3 por baixo + 1 M3 no alto"),
        Peca("barriga", barriga, cor="laranja", imprimir=rot("x", -90), suporte="sim (árvore)", explode=(0, 185, 0),
             obs="painel da frente = grade do alto-falante e tampa; 2 M3"),
        Peca("bandana-frente", band_f, cor="verde-bandana", imprimir=rot("x", -90), suporte="sim (árvore)", explode=(0, 150, 30),
             obs="faixa da frente + triângulo; colar no torso-frente"),
        Peca("bandana-costas", band_t, cor="verde-bandana", imprimir=rot("x", 90), suporte="sim (árvore)", explode=(0, -170, 30),
             obs="faixa de trás + laço; colar no torso-costas"),
        Peca("mao", BI.domo_local(10.0, 9.0), cor="marrom", macica=True, copias=mats_mao, explode=(0, 70, 0), obs="2 mãos; cola ou pressão"),
        BS.pino_guia(mats_pino),
    ]

    # ------------------------------------------------------------ coxas (cobrem as rodas) + aro ciano + patas
    coxa_d, pe_ext = BI.perna(p_perna, t_gordo)
    px = p_perna.ponto_na_pele((60, 0, B.eixo_roda_z + 2), (1, 0, 0))
    xa = float(px[0]) - 4.5
    zc = B.eixo_roda_z + 2
    A = K.aro
    coxa_d = coxa_d + (cil((xa - F.parede, 0, zc), (xa + 0.01, 0, zc), A.r_fora + 3.0) ^ pe_ext)
    coxa_d = coxa_d - cil((xa, 0, zc), (xa + 40, 0, zc), A.r_fora + F.encaixe) - cil((xa - 10, 0, zc), (xa + 1, 0, zc), A.r_dentro)
    aro = cil((xa + 0.05, 0, zc), (xa + 3.0, 0, zc), A.r_fora) - cil((xa, 0, zc), (xa + 4, 0, zc), A.r_dentro + 0.4)
    c_pata, r_pata = K.pata
    pata = elipsoide(c_pata, r_pata, seg=48) - caixa(-300, 300, -300, 300, -50, BI.CHAO_Z) - BI.gordo(p_perna, 0.2) - t_gordo
    for dx in (-9, 0, 9):                                  # sulcos dos dedos
        pata = pata - caixa(c_pata[0] + dx - 0.8, c_pata[0] + dx + 0.8, c_pata[1] + 12, 200, BI.CHAO_Z + 4, 60)
    pecas += [
        Peca("coxa-dir", coxa_d, cor="laranja", suporte="sim (só sob as 2 orelhas)", explode=(95, 0, 0), obs="cobre a roda direita; 2 M3 por baixo"),
        Peca("coxa-esq", espelho_x(coxa_d), cor="laranja", suporte="sim (só sob as 2 orelhas)", explode=(-95, 0, 0), obs="cobre a roda esquerda; 2 M3 por baixo"),
        Peca("aro", aro, cor="ciano", imprimir=rot("y", -90), macica=True, copias=[np.eye(4), np.diag([-1.0, 1, 1, 1])],
             explode=(130, 0, 0), obs="aro das coxas (use filamento translúcido para o LED da fase 2); cola"),
        Peca("pata-dir", pata, cor="marrom", macica=True, explode=(95, 60, 0), obs="pata traseira; cola"),
        Peca("pata-esq", espelho_x(pata), cor="marrom", macica=True, explode=(-95, 60, 0), obs="pata traseira; cola"),
    ]

    # ------------------------------------------------------------ rabo (cobre a esfera de apoio e a chave)
    rabo, ra_ext = BI.traseiro(p_rabo, t_gordo)
    pecas.append(Peca("rabo", rabo, cor="marrom", suporte="sim (só sob as 2 orelhas)", explode=(0, -150, 0),
                      obs="cobre a esfera de apoio, a chave e o conector de carga; 2 M3 por baixo"))

    # ------------------------------------------------------------ cabeça
    boca = K.boca
    cran, mand, c_ext, c_int = BI.cabeca(p_cab, boca, junta=K.junta)
    yp, zp = boca["y_eixo"], boca["z_eixo"]
    o = K.olho
    olhos, iris, pups = [], [], []
    for s in (1, -1):
        cran, ol, ir, pu = BI.olho((s * o.c[0], o.c[1], o.c[2]), o.r, (s * o.dir[0], o.dir[1], o.dir[2]), o.iris_r, o.pupila_r, cran, c_ext)
        olhos.append(ol), iris.append(ir), pups.append(pu)
    # focinho marrom: painel encaixado (janela + rebaixo), com as 2 narinas
    fc = K.focinho
    c_m48 = p_cab.deslocado(-2 * F.parede)

    def jan(k, d=0.0):
        return BI.elipse_y(fc.c[0], fc.c[1], fc.r[0] * k + d, fc.r[1] * k + d, fc.y0, 300)

    cran, focinho = BI.painel(cran, c_ext, c_int, c_m48, jan)
    for s in (1, -1):
        pn = p_cab.ponto_na_pele((s * 13, 30, fc.c[1] + 8), (0, 1, 0.25))
        focinho = focinho - esfera(pn, 3.4, seg=24)
    # orelhas (domos marrons) e topete
    mats_orelha = []
    for s in (1, -1):
        d = np.array([s * 0.62, -0.12, 0.78])
        p = p_cab.ponto_na_pele(np.array(K.cabeca[0][0], float), d)
        cran, Mo = BI.bolso_unha(cran, c_ext, p, d, r=14.0)
        mats_orelha.append(Mo)
    top, bolso, nerv = BI.crista(p_cab, [(-18, 350), (-36, 350), (-54, 344)], 3, 12.0, 13.0, dentro=(0, -28, 254))
    cran = (cran + (nerv ^ c_ext)) - bolso
    cran, mand, mesa, comps_cab, M_bucha = BI.mecanica_cabeca(p_cab, cran, mand, c_ext, c_int, boca, zcam=fc.c[1] + fc.r[1] * 1.1 + 12.0)
    comps += comps_cab
    pecas += [
        Peca("cranio", cran, cor="laranja", grupo="cabeca", suporte="sim (árvore)", explode=(0, 0, 150),
             obs="3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto dão acesso aos parafusos da coluna"),
        Peca("mandibula", mand, cor="laranja", grupo="mandibula", suporte="sim (árvore, por fora)", explode=(0, 70, 85),
             obs="horn do servo na direita (parafuso central por fora); M3x16 + bucha na esquerda"),
        Peca("focinho", focinho, cor="marrom", grupo="cabeca", imprimir=rot("x", -90), suporte="sim (árvore)", explode=(0, 110, 160), obs="painel marrom do focinho; cola"),
        Peca("mesa-cabeca", mesa, material="PETG", cor="grafite", grupo="cabeca", imprimir=rot("x", 180), macica=True, explode=(0, 0, 95),
             obs="mesa da cabeça: 2 M3x10 na coluna do berço (por cima); segura o servo da boca"),
        Peca("orelha", BI.domo_local(14.0, 13.0), cor="marrom", grupo="cabeca", macica=True, copias=mats_orelha, explode=(0, 0, 200), obs="2 orelhas; cola ou pressão"),
        Peca("topete", top, cor="laranja", grupo="cabeca", imprimir=rot("y", 90), macica=True, explode=(0, -20, 215), obs="pressão ou cola"),
        Peca("olho", olhos[0], cor="branco", grupo="cabeca", macica=True, explode=(20, 60, 170), obs="direito"),
        Peca("olho-esq", olhos[1], cor="branco", grupo="cabeca", macica=True, explode=(-20, 60, 170), obs="esquerdo (espelhado)"),
        Peca("iris", iris[0], cor="marrom", grupo="cabeca", macica=True, explode=(24, 80, 176)),
        Peca("iris-esq", iris[1], cor="marrom", grupo="cabeca", macica=True, explode=(-24, 80, 176)),
        Peca("pupila", pups[0], cor="preto", grupo="cabeca", macica=True, explode=(28, 100, 182)),
        Peca("pupila-esq", pups[1], cor="preto", grupo="cabeca", macica=True, explode=(-28, 100, 182)),
    ]
    pecas.append(BS.bucha_eixo([M_bucha]))
    pecas[-1].grupo = "mandibula"

    # ------------------------------------------------------------ esqueleto comum
    pecas += [BS.chassi(), BS.capa_esfera(), BS.bandeja_uno(), BS.bandeja_pi(), BS.garfo(), BS.berco(), BS.teste_encaixe()]
    pecas[-1].copias = []
    comps += BS.comps_base(arms=False)

    juntas = BS.juntas_base()
    juntas["mandibula"] = Junta("cabeca", (0, yp, zp), (-1, 0, 0), N.boca)
    poses = [("neutra", {}),
             ("pan-esq", {"pan": N.pan[1]}), ("pan-dir", {"pan": N.pan[0]}),
             ("tilt-cima", {"cabeca": N.tilt[1]}), ("tilt-baixo", {"cabeca": N.tilt[0]}),
             ("boca-aberta", {"mandibula": N.boca[1]}),
             ("pan+tilt-baixo+boca", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": N.boca[1]}),
             ("pan+tilt-cima", {"pan": N.pan[0], "cabeca": N.tilt[1]})]
    apoios = [(BS.X_RODA + P.RODA.larg / 2, 0.0), (-BS.X_RODA - P.RODA.larg / 2, 0.0), (0.0, B.esfera_y)]
    parede = {"torso": medir_parede(t_ext, t_int), "cabeça": medir_parede(c_ext, c_int),
              "coxa": medir_parede(pe_ext, p_perna.deslocado(-F.parede)), "rabo": medir_parede(ra_ext, p_rabo.deslocado(-F.parede))}
    encaixes = [{"par": ["motor-tt-dir", "roda-dir"], "motivo": "eixo do motor entra no cubo da roda"},
                {"par": ["motor-tt-esq", "roda-esq"], "motivo": "eixo do motor entra no cubo da roda"}]
    cab = ["cranio", "mesa-cabeca", "mandibula", "bucha-eixo", "servo-boca MG90S", "camera (fase 2)", "focinho", "orelha", "topete",
           "olho", "olho-esq", "iris", "iris-esq", "pupila", "pupila-esq"]
    ordem = BS.ordem_bicho(traseira=["rabo"], pernas=("coxa-dir", "coxa-esq", ["aro#0", "pata-dir"], ["aro#1", "pata-esq"]), cabeca=cab,
                           extras_frente=["bandana-frente", "mao"], extras_costas=["bandana-costas"])
    return Modelo("capivara", "Capivara", pecas, comps, juntas, apoios, poses, ordem=ordem, obs={"parede_medida": parede, "explode_grupo": {"cabeca": (0, 0, 95), "pan": (0, 0, 30), "mandibula": (0, 70, 85)}}, encaixes=encaixes)
