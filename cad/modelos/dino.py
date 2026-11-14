"""Modelo 1: dinossauro filhote (~30 cm). Roda com 2 motores TT escondidos nas pernas + esfera sob a cauda.
Movimentos preparados: pescoço pan + tilt, mandíbula, 2 braços."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import bicho as BI
from cad.comum import componentes as C
from cad.comum.base import B, CX, CY, CZ, F, N, X0, X1, Z0, Z1, furo, inserto, sim
from cad.comum.geo import caixa, casco, cil, elipsoide, esfera, espelho_x, girar, limites, mat_giro, mat_trans, prisma, uniao
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot

D = P.DINO


def construir() -> Modelo:
    pecas, comps = [], []
    # ------------------------------------------------------------ peles
    p_torso = BI.pele_torso(D.torso, h=D.passo)
    p_cab = BI.pele_blobs(D.cabeca, k=12, h=D.passo)
    p_perna = BI.pele_blobs(D.perna, k=14, h=D.passo)
    p_cauda = BI.pele_blobs(D.cauda, k=16, h=D.passo)
    t_gordo = BI.gordo(p_torso)

    # ------------------------------------------------------------ torso
    frente, costas, t_ext, t_int = BI.torso(p_torso)
    xs_pino = p_torso.ponto_na_pele((0, B.costura_y, 100.0), (1, 0, 0))[0] - F.parede - 1.0
    xg_pino = N.gola_r - F.parede - 6.5
    frente, costas, mats_pino = BI.pinos_torso(frente, costas, t_ext, t_int,
                                               [(xs_pino - 3, 100.0), (-xs_pino + 3, 100.0), (xg_pino, CZ - 2), (-xg_pino, CZ - 2)])
    costas = BI.parafuso_costas_deck(costas, t_ext)

    frente, costas, barriga, c_fal = BI.frente_com_painel(p_torso, frente, costas, t_ext, t_int, D.barriga.c, D.barriga.r)
    comps.append(c_fal)
    oy, oz = B.ombro

    # ------------------------------------------------------------ crista das costas (azul) — tampa o parafuso do alto
    cr_c, bolso, nerv = BI.crista(p_torso, [(-160, 160), (-170, 138), (-170, 114), (-164, 90)], 3, 20.0, 27.0,
                                  dentro=(0, -46, 118))
    costas = (costas + (nerv ^ t_ext)) - bolso

    pecas += [
        Peca("torso-frente", frente, cor="verde", imprimir=rot("x", 90), suporte="sim (árvore, por dentro)", explode=(0, 110, 0),
             obs="metade da frente; 1 M3 por baixo + 2 M3 cabeça chata nos postes (sob a barriga)"),
        Peca("torso-costas", costas, cor="verde", imprimir=rot("x", -90), suporte="sim (árvore, por dentro)", explode=(0, -130, 0),
             obs="metade de trás (tampa de acesso às bandejas); 2 M3 por baixo + 1 M3 no alto, sob a crista"),
        Peca("barriga", barriga, cor="creme", imprimir=rot("x", -90), suporte="sim (árvore)", explode=(0, 185, 0),
             obs="painel da barriga = grade do alto-falante e tampa da frente; 2 M3"),
        Peca("crista-costas", cr_c, cor="azul", imprimir=rot("y", 90), macica=True, explode=(0, -200, 0),
             obs="encaixe por pressão (sem cola: tampa o parafuso do alto das costas)"),
    ]
    pecas.append(BS.pino_guia(mats_pino))

    # ------------------------------------------------------------ pernas (com unhas creme)
    perna_d, pe_ext = BI.perna(p_perna, t_gordo)
    mats_unha = []
    cpe = np.array(D.perna[-1][0], float)
    for ang in (-34, 0, 34):
        a = np.radians(ang)
        d = np.array([np.sin(a) * 0.9, np.cos(a), 0.12])
        p = p_perna.ponto_na_pele(cpe + np.array([0, 0, -6.0]), d)
        perna_d, Mu = BI.bolso_unha(perna_d, pe_ext, p, d)
        mats_unha.append(Mu)
    perna_d = perna_d - t_gordo
    perna_e = espelho_x(perna_d)
    esp = np.diag([-1.0, 1, 1, 1])
    mats_unha_e = []
    for Mu in mats_unha:
        p = Mu[:3, 3] * np.array([-1, 1, 1])
        n = Mu[:3, 2] * np.array([-1, 1, 1])
        mats_unha_e.append(BI.mat_de_z_para(n, p))
    pecas += [
        Peca("perna-dir", perna_d, cor="verde", suporte="não", explode=(95, 0, 0), obs="cobre a roda direita; 2 M3 por baixo"),
        Peca("perna-esq", perna_e, cor="verde", suporte="não", explode=(-95, 0, 0), obs="cobre a roda esquerda; 2 M3 por baixo"),
        Peca("unha", BI.unha_local(), cor="creme", macica=True, copias=mats_unha + mats_unha_e,
             explode=(0, 60, 0), obs="6 unhas dos pés; cola ou pressão"),
    ]

    # ------------------------------------------------------------ cauda + crista
    cauda, ca_ext = BI.traseiro(p_cauda, t_gordo)
    cr_r, bolso, nerv = BI.crista(p_cauda, [(-121, 110), (-141, 90), (-161, 75), (-181, 65)], 3, 15.0, 20.0, dentro=(0, -151, 25))
    cauda = (cauda + ((nerv ^ ca_ext) - t_gordo)) - bolso
    pecas += [
        Peca("cauda", cauda, cor="verde", suporte="não", explode=(0, -150, 0), obs="cobre a esfera de apoio e a chave; 2 M3 por baixo"),
        Peca("crista-cauda", cr_r - t_gordo, cor="azul", imprimir=rot("y", 90), macica=True, explode=(0, -200, 40), obs="pressão ou cola"),
    ]

    # ------------------------------------------------------------ cabeça
    boca = D.boca
    cran, mand, c_ext, c_int = BI.cabeca(p_cab, boca)
    yp, zp = boca["y_eixo"], boca["z_eixo"]
    zm = CZ + N.mesa_z                    # face de baixo da mesa
    zmt = zm + N.mesa_esp

    def z_boca(x, y):
        return boca["z0"] + boca["incl"] * (y - boca["y_ref"]) + boca["raio_sorriso"] - np.sqrt(boca["raio_sorriso"] ** 2 - x * x)

    # olhos
    o = D.olho
    olhos, iris, pups = [], [], []
    for s in (1, -1):
        c = (s * o.c[0], o.c[1], o.c[2])
        d = (s * o.dir[0], o.dir[1], o.dir[2])
        cran, ol, ir, pu = BI.olho(c, o.r, d, o.iris_r, o.pupila_r, cran, c_ext)
        olhos.append(ol), iris.append(ir), pups.append(pu)
    # narinas
    for s in (1, -1):
        pn = p_cab.ponto_na_pele((s * 19, 20, 250), (0, 0.75, 0.66))
        cran = cran - esfera(pn, 3.6, seg=24)
    # crista da cabeça
    cr_h, bolso, nerv = BI.crista(p_cab, [(-20, 350), (-62, 338), (-98, 312), (-122, 275)], 3, 19.0, 27.0, dentro=(0, -30, 256))
    cran = (cran + (nerv ^ c_ext)) - bolso
    cran, mand, mesa, comps_cab, M_bucha = BI.mecanica_cabeca(p_cab, cran, mand, c_ext, c_int, boca, zcam=246.0)
    comps += comps_cab

    pecas += [
        Peca("cranio", cran, cor="verde", grupo="cabeca", suporte="sim (árvore)", explode=(0, 0, 150),
             obs="3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto dão acesso aos parafusos da coluna"),
        Peca("mandibula", mand, cor="verde", grupo="mandibula", suporte="sim (árvore, por fora)", explode=(0, 70, 85),
             obs="horn do servo na direita (parafuso central por fora); M3x16 + bucha na esquerda"),
        Peca("mesa-cabeca", mesa, material="PETG", cor="grafite", grupo="cabeca", imprimir=rot("x", 180), macica=True, explode=(0, 0, 95),
             obs="mesa da cabeça: 2 M3x10 na coluna do berço (por cima); segura o servo da boca"),
        Peca("crista-cabeca", cr_h, cor="azul", grupo="cabeca", imprimir=rot("y", 90), macica=True, explode=(0, -40, 200), obs="pressão ou cola"),
        Peca("olho", olhos[0], cor="branco", grupo="cabeca", macica=True, explode=(20, 60, 170), obs="direito"),
        Peca("olho-esq", olhos[1], cor="branco", grupo="cabeca", macica=True, explode=(-20, 60, 170), obs="esquerdo (espelhado)"),
        Peca("iris", iris[0], cor="azul", grupo="cabeca", macica=True, explode=(24, 80, 176)),
        Peca("iris-esq", iris[1], cor="azul", grupo="cabeca", macica=True, explode=(-24, 80, 176)),
        Peca("pupila", pups[0], cor="preto", grupo="cabeca", macica=True, explode=(28, 100, 182)),
        Peca("pupila-esq", pups[1], cor="preto", grupo="cabeca", macica=True, explode=(-28, 100, 182)),
    ]
    pecas.append(BS.bucha_eixo([M_bucha]))
    pecas[-1].grupo = "mandibula"

    # ------------------------------------------------------------ braços
    xsk = p_torso.ponto_na_pele((0, oy, oz), (1, 0, 0))[0]
    x_tip = X1 + P.MICRO.aba_ate_ponta
    bra = D.braco
    c1 = (xsk + bra.r_ombro[0] + 1.5, oy, oz)
    corpo_b = casco(elipsoide(c1, bra.r_ombro, seg=40), elipsoide(bra.mao, bra.r_mao, seg=40))
    for (dx, dz) in ((-6, 3), (0, -2), (6, 3)):
        corpo_b = corpo_b + esfera((bra.mao[0] + dx, bra.mao[1] + bra.r_mao[1] - 1, bra.mao[2] + dz - 2), 4.2, seg=24)
    corpo_b = corpo_b - BI.gordo(p_torso, 2.0)
    hl, hd, hp, he = P.MICRO.horn
    xh0 = x_tip - 3.0
    cubo = cil((xh0, oy, oz), (c1[0], oy, oz), 8.5)
    braco = corpo_b + cubo
    dirb = np.array([0, bra.mao[1] - oy, bra.mao[2] - oz], float)
    dirb /= np.linalg.norm(dirb)
    rec = casco(cil((xh0 - 0.1, oy, oz), (xh0 + he + 0.4, oy, oz), hd / 2 + 0.3, seg=24),
                cil((xh0 - 0.1, oy + dirb[1] * hl, oz + dirb[2] * hl), (xh0 + he + 0.4, oy + dirb[1] * hl, oz + dirb[2] * hl), hp / 2 + 0.3, seg=24))
    braco = braco - rec - cil((xh0 - 1, oy, oz), (x_tip + 1.0, oy, oz), hd / 2 + 0.3, seg=24)
    braco = braco - cil((xh0, oy, oz), (c1[0] + 40, oy, oz), 1.4, seg=12) - cil((x_tip + 3.0, oy, oz), (c1[0] + 40, oy, oz), 2.9, seg=16)
    pecas += [
        Peca("braco-dir", braco, cor="verde", grupo="braco_d", imprimir=rot("y", -90), macica=True, suporte="sim (pouco)", explode=(70, 20, 0),
             obs="encaixa no horn do servo; parafuso central pelo furo de fora"),
        Peca("braco-esq", espelho_x(braco), cor="verde", grupo="braco_e", imprimir=rot("y", 90), macica=True, suporte="sim (pouco)", explode=(-70, 20, 0)),
    ]

    # ------------------------------------------------------------ esqueleto comum
    pecas += [BS.chassi(), BS.capa_esfera(), BS.bandeja_uno(), BS.bandeja_pi(), BS.garfo(), BS.berco(), BS.teste_encaixe()]
    pecas[-1].copias = []            # o cupom de teste não entra na montagem
    comps += BS.comps_base(arms=True)

    juntas = BS.juntas_base()
    juntas["mandibula"] = Junta("cabeca", (0, yp, zp), (-1, 0, 0), N.boca)       # positivo = abre
    juntas["braco_d"] = Junta("corpo", (0, oy, oz), (1, 0, 0), D.braco.lim)      # positivo = mão sobe
    juntas["braco_e"] = Junta("corpo", (0, oy, oz), (1, 0, 0), D.braco.lim)
    poses = [("neutra", {}),
             ("pan-esq", {"pan": N.pan[1]}), ("pan-dir", {"pan": N.pan[0]}),
             ("tilt-cima", {"cabeca": N.tilt[1]}), ("tilt-baixo", {"cabeca": N.tilt[0]}),
             ("boca-aberta", {"mandibula": N.boca[1]}),
             ("pan+tilt-baixo+boca", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": N.boca[1]}),
             ("pan+tilt-cima", {"pan": N.pan[0], "cabeca": N.tilt[1]}),
             ("bracos-cima", {"braco_d": D.braco.lim[1], "braco_e": D.braco.lim[1]}),
             ("bracos-baixo", {"braco_d": D.braco.lim[0], "braco_e": D.braco.lim[0]}),
             ("tudo-1", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": N.boca[1], "braco_d": D.braco.lim[1], "braco_e": D.braco.lim[1]}),
             ("tudo-2", {"pan": N.pan[0], "cabeca": N.tilt[0], "mandibula": N.boca[1], "braco_d": D.braco.lim[1], "braco_e": D.braco.lim[0]})]
    apoios = [(BS.X_RODA + P.RODA.larg / 2, 0.0), (-BS.X_RODA - P.RODA.larg / 2, 0.0), (0.0, B.esfera_y)]
    from cad.comum.geo import medir_parede
    parede = {"torso": medir_parede(t_ext, t_int), "cabeça": medir_parede(c_ext, c_int),
              "perna": medir_parede(pe_ext, p_perna.deslocado(-F.parede)), "cauda": medir_parede(ca_ext, p_cauda.deslocado(-F.parede))}
    encaixes = [{"par": ["motor-tt-dir", "roda-dir"], "motivo": "eixo do motor entra no cubo da roda"},
                {"par": ["motor-tt-esq", "roda-esq"], "motivo": "eixo do motor entra no cubo da roda"}]
    cab = ["cranio", "mesa-cabeca", "mandibula", "bucha-eixo", "servo-boca MG90S", "camera (fase 2)", "crista-cabeca",
           "olho", "olho-esq", "iris", "iris-esq", "pupila", "pupila-esq"]
    ordem = BS.ordem_bicho(traseira=["cauda", "crista-cauda"], pernas=("perna-dir", "perna-esq", ["unha#0", "unha#1", "unha#2"], ["unha#3", "unha#4", "unha#5"]), cabeca=cab,
                           extras_costas=["crista-costas"], bracos=True)
    return Modelo("dino", "Dinossauro", pecas, comps, juntas, apoios, poses, ordem=ordem,
                  obs={"batente_frente_y": float(limites(perna_d)[1][1]), "parede_medida": parede, "explode_grupo": {"cabeca": (0, 0, 95), "pan": (0, 0, 30), "mandibula": (0, 70, 85), "braco_d": (70, 20, 0), "braco_e": (-70, 20, 0)}}, encaixes=encaixes)
