"""Modelo 2: capivara filhote sentada (30 cm). Rodada 2: a casca é a malha de image-to-3D (cad/peles/capivara.npz)
cortada em "vasos" de base plana, sobre o esqueleto baixo de cad/comum/base_baixa.py.

Casca: bacia (corpo inteiro, entra por cima do chassi), porta traseira (bateria e bandejas saem por trás sem tirar a
cabeça), gola-bandana (esfera do pescoço), crânio + mandíbula. Rodas dentro das ancas, 2 esferas de apoio sob as
patas da frente. Movimentos: pescoço pan + tilt e boca. Braços parados (relevo da casca)."""
from __future__ import annotations

import numpy as np

from cad import parametros as P
from cad.comum import base as BS
from cad.comum import base_baixa as BB
from cad.comum import bicho as BI
from cad.comum import casca as CA
from cad.comum import componentes as C
from cad.comum.base import F, N
from cad.comum.geo import (caixa, cil, desbeliscar, esfera, espelho_x, limpar, mat_giro, mat_trans, maior_corpo, medir_parede, sdf_elipsoide, smin, uniao)
from cad.comum.modelo import Comp, Junta, Modelo, Peca, rot

K = P.CAPIVARA


def _boca(dy, dz):
    """Parâmetros da boca (dados na pele) levados a outro referencial."""
    b = dict(K.boca)
    for k in ("y_eixo", "y_corte", "y_ref"):
        b[k] += dy
    for k in ("z_eixo", "z0"):
        b[k] += dz
    return b


def construir() -> Modelo:
    pecas, comps = [], []
    E = BB.esqueleto(K)
    C0 = np.array(E.centro)
    T = E.T                                            # pescoço padrão de base.py -> pescoço deste bicho
    r_gola = K.soquete_r - K.folga_junta
    z_top = float(C0[2] + r_gola * np.sin(np.radians(K.gola_elev)))
    zb = float(C0[2] + K.cabeca_z)

    # ------------------------------------------------------------ pele, cabeça e zona varrida
    base = CA.carregar(K.pele, dy=K.dy)
    Pg = base.P
    lo_l, hi_l = (np.array(v, float) + (0, K.dy, 0) for v in K.laco)
    H = np.maximum(CA.campo_cabeca(base, C0, K.soquete_r, zb), -CA.campo_caixa(Pg, lo_l, hi_l))      # cabeça sem o laço
    bo = _boca(K.dy, 0.0)
    # mandíbula aberta: a parte de baixo da boca, girada no eixo dela, também varre
    z_boca = bo["z0"] + bo["incl"] * (Pg[..., 1] - bo["y_ref"]) + 8.0
    recuo = max(bo["z_eixo"] - zb, 0.0) * np.sin(np.radians(abs(N.boca[1]))) + 1.5                     # o mesmo alívio esférico que bicho.cabeca dá à mandíbula
    Hj = np.maximum(np.maximum(H, bo["y_corte"] - Pg[..., 1]), Pg[..., 2] - z_boca)
    Hj = np.maximum(Hj, K.soquete_r + recuo - np.linalg.norm(Pg - C0.astype(np.float32), axis=-1))
    H = np.minimum(H, CA.reamostrar(base, Hj, mat_giro((0, bo["y_eixo"], bo["z_eixo"]), (-1, 0, 0), N.boca[1])))
    pans = np.arange(N.pan[0], N.pan[1] + 0.1, 7.5)
    tilts = np.unique(np.concatenate([np.linspace(N.tilt[0], 0, 3), np.linspace(0, N.tilt[1], 3)]))
    S = CA.zona_varrida(base, H, C0, pans, tilts, (-115, C0[1] - 120, 96), (115, C0[1] + 140, z_top + 14), chave=f"{K.pele}|{K.dy}")
    del H, Hj

    # ------------------------------------------------------------ peças em relevo do corpo (regiões no robô)
    dyv = np.array([0, K.dy, 0.0])
    R = CA.Regiao
    lo, hi = (np.array(v, float) + dyv for v in K.rabo.caixa)
    rel = {"rabo": CA.Relevo(R.caixa(lo, hi), (0, K.rabo.plano_y + K.dy, 70), (0, -1, 0))}
    for s, nm in ((1, "mao-dir"), (-1, "mao-esq")):
        rel[nm] = CA.Relevo(R.cil((s * K.mao.c[0], K.mao.plano_y + K.dy - 6, K.mao.c[1]), (s * K.mao.c[0], K.mao.plano_y + K.dy + 60, K.mao.c[1]), K.mao.r),
                            (0, K.mao.plano_y + K.dy, 65), (0, 1, 0))
    rel["avental"] = CA.Relevo(R.triangulo_xz(*K.avental.tri, 0.0, 300.0), (0, K.avental.plano_y + K.dy, 100), (0, 1, 0))
    A = K.aro
    # aro: a anca é cortada por um plano (face chata, sem rebaixo: nada fica em balanço) e o aro assenta nela
    aros = [CA.Relevo(R.caixa((min(s * (A.x - 1), s * 200), -45, 4), (max(s * (A.x - 1), s * 200), 45, 76)), (s * A.x, 0, A.z), (s, 0, 0)) for s in (1, -1)]

    # ------------------------------------------------------------ corpo = pele + ancas - zona varrida - relevos
    def campo_blobs(Pp, Fp):
        d = Fp
        for (c, r) in K.anca:
            for s in (1, -1):
                d = smin(d, sdf_elipsoide(Pp, (s * c[0], c[1] + K.dy, c[2]), r), 6.0)
        for (c, r) in K.rabo_blob:
            d = smin(d, sdf_elipsoide(Pp, (c[0], c[1] + K.dy, c[2]), r), 4.0)
        return d

    def campo_corpo(Pp, Fp):
        d = campo_blobs(Pp, Fp)
        d = np.maximum(np.maximum(d, K.folga_junta - S), Pp[..., 2] - (z_top + 6.0))
        d = CA.tirar_farelos(base, d, 2.5, K.z_gola - 14.0)
        # por baixo (não aparece): barriga da frente e fundo de trás sobem a 45° desde a mesa
        d = CA.autoportante(base, d, (-46, K.dy + 12, K.z_fundo), (46, K.dy + 62, 30.0))
        d = CA.autoportante(base, d, (-46, K.dy - 112, K.z_fundo), (46, K.dy - 70, 26.0))
        for r_ in list(rel.values()) + aros:
            d = r_.tirar(Pp, d)
        return d

    p_corpo = base.combinar(campo_corpo)
    del S
    p_orig = base.combinar(campo_blobs)                # pele original (+ blobs): é dela que saem as peças em relevo
    ext = p_corpo.solido()
    inte = p_corpo.deslocado(-F.parede)
    casca = ext - inte
    pol = BB.poligono_piso(E, p_corpo)
    chassi = BB.chassi(E, pol)
    v, pt = CA.sobra(p_corpo, chassi.solido)
    if v > -(F.parede + 0.5):
        print(f"  AVISO: o chassi chega a {v:+.1f} mm da pele em {np.round(pt, 0)} (tem de ser <= {-(F.parede + 0.5):.1f})")

    # ------------------------------------------------------------ bacia (corpo) + porta traseira
    comps_esq = BB.comps(E)
    obst = BB.obstaculos_bacia(E, chassi.solido, [c.solido for c in comps_esq if c.nome.startswith(("driver", "motor", "step", "ubec"))])
    bacia = maior_corpo(CA.fatia_z(casca, K.z_fundo, K.z_gola) - obst)
    px, yd = K.porta.x, K.porta.y_max + K.dy
    porta = maior_corpo(bacia ^ caixa(-px + F.encaixe, px - F.encaixe, -400, yd, -50, 400))
    bacia = maior_corpo(bacia - caixa(-px, px, -400, yd, -50, 400))
    # 4 M3 por trás, embaixo, nos 2 postes do chassi: 2 prendem a porta e 2 prendem a bacia. Cada parafuso atravessa
    # um bloco MACIÇO que nasce na mesa (nada em balanço) e vai da pele até o poste; a cabeça fica rebaixada na pele.
    # Em cima a bacia é presa pela gola (2 M3 nas orelhas da torre); na frente ela abraça os ressaltos das esferas.
    x0, x1, pya, pyb, pzt, pzp = E.poste_porta

    def bloco(xa, xb, xp, zp_):
        b = caixa(xa, xb, pya - 45, pya - 0.3, K.z_fundo, pzt + 1.0) ^ ext
        return b, cil((xp, pya - 4.0, zp_), (xp, pya - 90, zp_), F.cabeca_m3_d / 2 + 0.1, seg=24) + cil((xp, pya + 1, zp_), (xp, pya - 6, zp_), F.m3_passante / 2, seg=24)

    for sx in (1, -1):
        xa, xb = sorted((sx * (E.poste_x[0] - 4.5), sx * (E.poste_x[0] + 4.5)))
        b, c = bloco(xa, xb, sx * E.poste_x[0], pzp)
        porta = porta + b - c
        xa, xb = sorted((sx * (px + 0.3), sx * (E.poste_x[1] + 4.5)))
        b, c = bloco(xa, xb, sx * E.poste_x[1], E.bacia_parafuso_z)
        bacia = bacia + b - c
    # ------------------------------------------------------------ gola-bandana (esfera do pescoço)
    # A cavidade é só a esfera de dentro: entre a esfera e o rolo de fora a gola é MACIÇA (o teto da cavidade ficaria
    # em balanço). 2 abas na base (na mesa) recebem os M3 das orelhas da torre: é a gola que prende a bacia por cima.
    zg = K.z_gola + F.encaixe
    gola = maior_corpo(CA.fatia_z(ext, zg, z_top) - esfera(C0, r_gola - F.parede - 0.3, seg=128))
    ow, oe = E.orelha_gola
    for (xa, xb, xe) in ((E.torre_x1 - 2.0, 62.0, E.torre_x1 + E.parede_esp / 2), (-62.0, -35.5, -37.5 - oe / 2)):
        aba = caixa(xa, xb, C0[1] - ow / 2 - 1, C0[1] + ow / 2 + 1, zg, zg + 3.0) ^ esfera(C0, r_gola - 0.5, seg=64)
        gola = gola + aba - cil((xe, C0[1], zg - 1), (xe, C0[1], zg + 4), F.m3_passante / 2, seg=24)

    pc = {nm: r_.peca(p_orig) for nm, r_ in rel.items()}
    # carregador USB-C 2S DENTRO do rabo, em pé, com a boca para baixo (escondida); o rabo prende por 2 M3 por dentro da porta
    yb, z0c = K.rabo.plano_y + K.dy, K.carregador_z
    Lc, Wc, Hc = P.CARREGADOR2S.cx
    pc["rabo"] = pc["rabo"] - caixa(-Wc / 2 - 0.4, Wc / 2 + 0.4, yb - Hc - 0.8, yb + 0.5, z0c, z0c + Lc + 0.8) \
        - caixa(-6.5, 6.5, yb - 7.0, yb + 0.5, 20.0, z0c + 0.01)
    for sx in (1, -1):
        pc["rabo"] = pc["rabo"] - BS.inserto((sx * 15.5, yb, 62.0), (0, -1, 0))
        porta = porta - cil((sx * 15.5, yb + 8, 62.0), (sx * 15.5, yb - 0.5, 62.0), F.m3_passante / 2, seg=24)
    porta = porta - cil((0, yb + 8, z0c + 26), (0, yb - 0.5, z0c + 26), 3.5, seg=24)                        # fios do carregador
    comps.append(Comp("carregador USB-C 2S", C.modulo(P.CARREGADOR2S).transform(C.M([(0, 0, -1), (1, 0, 0), (0, -1, 0)], (0, yb - 0.4, z0c + 0.4 + Lc / 2))[:3, :]),
                      "corpo", P.CARREGADOR2S.massa, "azul"))
    # sensores de distância laterais (fase 2) atrás do miolo escuro do aro ciano
    xb = A.x - F.parede - 0.6
    for sx, nm in ((1, "dir"), (-1, "esq")):
        bacia = bacia - cil((sx * (A.x - 5), 0, A.z), (sx * (A.x + 1), 0, A.z), P.TOF.janela_d / 2, seg=24)
        cx_ = caixa(xb - P.TOF.esp, xb, -P.TOF.placa[0] / 2, P.TOF.placa[0] / 2, A.z - P.TOF.placa[1] / 2, A.z + P.TOF.placa[1] / 2)
        comps.append(Comp(f"tof-{nm} (fase 2)", cx_ if sx > 0 else espelho_x(cx_), "corpo", P.TOF.massa, "verde", fase2=True))
    miolo = cil((A.x + 0.05, 0, A.z), (A.x + A.esp - 0.6, 0, A.z), A.r_dentro) - cil((A.x - 1, 0, A.z), (A.x + A.esp + 1, 0, A.z), P.TOF.janela_d / 2 - 0.5)
    aro = cil((A.x + 0.05, 0, A.z), (A.x + A.esp, 0, A.z), A.r_fora) - cil((A.x, 0, A.z), (A.x + A.esp + 1, 0, A.z), A.r_dentro + 0.4)
    marrom = dict(cor="marrom", macica=True, suporte="não", orientacao="base plana (face de colar) na mesa")
    pecas += [
        Peca("rabo", pc["rabo"], imprimir=rel["rabo"].imprimir, explode=(0, -160, 0), obs="rabo; cola no assento plano da porta", **marrom),
        Peca("mao-dir", pc["mao-dir"], imprimir=rel["mao-dir"].imprimir, explode=(30, 90, 0), obs="mão direita; cola", **marrom),
        Peca("mao-esq", pc["mao-esq"], imprimir=rel["mao-esq"].imprimir, explode=(-30, 90, 0), obs="mão esquerda; cola", **marrom),
        Peca("avental", pc["avental"], cor="verde-bandana", macica=True, imprimir=rel["avental"].imprimir, explode=(0, 110, 20),
             orientacao="base plana (face de colar) na mesa", obs="ponta da bandana no peito; cola no rebaixo de fundo plano"),
        Peca("aro", aro, cor="ciano", imprimir=rot("y", -90), macica=True, copias=[np.eye(4), np.diag([-1.0, 1, 1, 1])], explode=(130, 0, 0),
             orientacao="face plana na mesa", obs="aro das ancas (filamento translúcido para o LED da fase 2); cola"),
        Peca("miolo", miolo, cor="preto", imprimir=rot("y", -90), macica=True, copias=[np.eye(4), np.diag([-1.0, 1, 1, 1])], explode=(140, 0, 0),
             orientacao="face plana na mesa", obs="disco escuro no centro do aro: janela do sensor de distância lateral (fase 2); cola"),
    ]
    # a base de cada vaso tem de sair PLANA: desfaz arestas beliscadas aqui (o gerar faria com cápsulas que passam
    # 0,5 mm da base e a peça deixaria de assentar na mesa) e refaz o corte da base
    bacia, porta, gola = (maior_corpo(CA.fatia_z(desbeliscar(limpar(m)), z0, 900.0)) for m, z0 in ((bacia, K.z_fundo), (porta, K.z_fundo), (gola, zg)))
    pecas += [
        Peca("corpo", bacia, cor="laranja", explode=(0, 0, 60), perimetros=4, infill=15,
             suporte="sim (pouco, árvore fina: teto de dentro das 2 patas, sobre os ressaltos das esferas, e quinas de baixo do relevo dos braços; ~0,9 % da área)",
             orientacao="borda de baixo (z=5) na mesa, em pé como um vaso; boca (z=124) para cima",
             reforco="2 blocos maciços atrás (um por parafuso M3, da mesa até o poste do chassi); barriga da frente e fundo de trás engrossados a 45° desde a mesa; 4 perímetros porque a bacia é aberta atrás (porta)",
             obs="bacia inteira do corpo; desce por cima do chassi; 2 M3 por trás (embaixo) + presa em cima pela gola; na frente abraça os ressaltos das esferas"),
        Peca("porta", porta, cor="laranja", explode=(0, -120, 0), perimetros=4, infill=15,
             suporte="sim (pouco: ~110 mm² na curva de baixo, por fora e por baixo; não aparece)",
             orientacao="borda de baixo na mesa, em pé", reforco="2 blocos maciços (um por parafuso M3, da mesa até o poste); assento plano do rabo com parede atrás",
             obs="porta traseira: bateria e bandejas saem por aqui sem tirar a cabeça; 2 M3 por trás (embaixo); leva o rabo e o carregador USB-C"),
        Peca("gola", gola, cor="verde-bandana", suporte="não", explode=(0, 0, 100), perimetros=4, infill=20,
             orientacao="base (z=124) na mesa; a esfera sobe até 45° e fica aberta em cima",
             reforco="maciça entre a esfera e o rolo de fora (sem teto em balanço); 2 abas na base para os M3 das orelhas da torre",
             obs="gola-bandana: esfera em que a cabeça gira; assenta na borda da bacia e a prende; 2 M3 por cima, nas orelhas da torre (por dentro, antes da cabeça)"),
    ]

    # ------------------------------------------------------------ cabeça (construída no referencial do pescoço padrão)
    p_cab = CA.carregar(K.pele, dy=K.dy - T[1], dz=-T[2])
    czs = BS.CZ
    p_cab = p_cab.recortar((-200, -400, czs - 8.0), (200, 400, 600))
    boca = _boca(K.dy - T[1], -T[2])
    p_cab0 = p_cab
    ds = np.array([0, K.dy - T[1], -T[2]])             # pele -> referencial padrão
    lo, hi = (np.array(v, float) + ds for v in K.focinho.caixa)
    relc = {"focinho": CA.Relevo(R.caixa(lo, hi), (0, K.focinho.plano_y + ds[1], 200 + ds[2]), (0, 1, 0))}
    lo, hi = (np.array(v, float) + ds for v in K.topete.caixa)
    relc["topete"] = CA.Relevo(R.caixa(lo, hi), (0, ds[1], K.topete.plano_z + ds[2]), (0, 0, 1))
    oc, on = np.array(K.orelha.c, float), np.array(K.orelha.n, float) / np.linalg.norm(K.orelha.n)
    for s, nm in ((1, "orelha-dir"), (-1, "orelha-esq")):
        e_ = np.array([s, 1, 1.0])
        relc[nm] = CA.Relevo(R.esfera(oc * e_ + ds, K.orelha.r), (oc + on * K.orelha.d) * e_ + ds, on * e_)
    lo_s, hi_s = (np.array(v, float) + ds for v in K.laco)

    def campo_cab(Pp, Fp):
        d = np.maximum(Fp, -CA.campo_caixa(Pp, lo_s, hi_s))          # sem o laço
        for r_ in relc.values():
            d = r_.tirar(Pp, d)
        return d

    p_cab = p_cab.combinar(campo_cab)
    pcc = {nm: r_.peca(p_cab0).translate(list(T)) for nm, r_ in relc.items()}
    cran, mand, c_ext, c_int = BI.cabeca(p_cab, boca, r_soquete=K.soquete_r, cabeca_z=K.cabeca_z)
    o = K.olho
    olhos, iris, pups = [], [], []
    ps = p_cab.ponto_na_pele((o.x, 300.0, o.z - T[2]), (0, -1, 0))
    nrm = CA.normal(p_cab, ps, 3.0)
    c_olho = ps - nrm * o.r * o.afunda
    # olho direito = câmera (Camera Module 3 Wide), olho esquerdo = ToF: decisão (b), ver decisions.md do longrun
    cam_furos = [(sx * P.CAMERA.furos[0] / 2, yy) for sx in (1, -1) for yy in (10.0, 10.0 - P.CAMERA.furos[1])]
    comps_olho, imp_olho = [], []
    for s, placa, furo_d, furos in ((1, P.CAMERA.placa, P.CAMERA.lente_d + 1.0, cam_furos), (-1, P.TOF.placa, P.TOF.janela_d, ())):
        esp = np.array([s, 1, 1.0])
        cran, ol, ir, pu, Mo = BI.olho_sensor(c_olho * esp, o.r, nrm * esp, o.iris_r, o.pupila_r, cran, c_ext, placa, furo_d, furos)
        olhos.append(ol), iris.append(ir), pups.append(pu)
        imp_olho.append(CA.mat_imprimir_base(nrm * esp))
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
                                                              eixo_oculto=True, sem_ponte=True)
    comps_cab += comps_olho
    for s_ in (1, -1):                                  # as orelhas crânio -> mesa nascem depois dos olhos: reabrir o lugar do olho
        cran = cran - esfera(c_olho * (s_, 1, 1), o.r + F.encaixe / 2, seg=64)
    # alto-falante (fase 2) em cima da mesa da cabeça, virado para baixo: o som sai pela boca e pelo vão do pescoço
    zmt = BS.CZ + N.mesa_z + N.mesa_esp
    ysf = K.falante_y + ds[1]
    rf = P.FALANTE.d / 2
    mesa = mesa - cil((0, ysf, zmt - 6), (0, ysf, zmt + 1), rf - 2.0) - cil((0, ysf, zmt - 2.5), (0, ysf, zmt + 0.01), rf - 2.0, rf + 0.6)
    comps_cab.append(Comp("alto-falante (fase 2)", C.falante().transform(C.M([(1, 0, 0), (0, 0, -1), (0, 1, 0)], (0, ysf, zmt - 0.55))[:3, :]),
                          "cabeca", P.FALANTE.massa, "preto", fase2=True))
    cran = maior_corpo(cran)
    mand = maior_corpo(mand - cran - cran.translate([0, 0, -0.6]))      # a almofada do eixo não passa do céu da boca
    Tl = list(T)
    for c in comps_cab:
        c.solido = c.solido.translate(Tl)
    comps += comps_cab
    g = lambda m: m.translate(Tl)
    yf, nx, nz = K.focinho.plano_y + K.dy, K.narina.x, K.narina.z
    cran_r = g(cran)
    for sx, nm in ((1, "dir"), (-1, "esq")):
        pcc["focinho"] = pcc["focinho"] - cil((sx * nx, yf - 1, nz), (sx * nx, yf + 60, nz), P.MIC.furo_som / 2, seg=16) \
            - cil((sx * nx, yf - 0.5, nz), (sx * nx, yf + P.MIC.esp + 1.0, nz), P.MIC.d / 2 + 0.3)
        cran_r = cran_r - cil((sx * nx, yf - 10, nz), (sx * nx, yf + 1, nz), 3.0, seg=24)                  # fio do microfone
        comps.append(Comp(f"microfone-{nm} (fase 2)", cil((sx * nx, yf + 0.2, nz), (sx * nx, yf + 0.2 + P.MIC.esp, nz), P.MIC.d / 2), "cabeca",
                          P.MIC.massa, "verde", fase2=True))
    pecas += [
        Peca("cranio", cran_r, cor="laranja", grupo="cabeca", explode=(0, 0, 150), perimetros=3, infill=15,
             suporte="sim (árvore POR DENTRO: teto do crânio e fundo dos copos dos olhos; e por baixo, fora do rosto: céu da boca e curva de baixo das bochechas)",
             orientacao="borda de baixo (z=152) na mesa, em pé", reforco="3 orelhas internas com inserto M3 para a mesa; copos dos olhos fechados por trás (só a janela do cabo)", obs="3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto dão acesso aos parafusos da coluna"),
        Peca("mandibula", g(mand), cor="laranja", grupo="mandibula", imprimir=rot("x", 90), explode=(0, 70, 85), perimetros=4, infill=20,
             suporte="sim (pouco: ~190 mm² no alívio esférico de trás, por dentro)", orientacao="face de trás (plano de corte) na mesa, ponta do queixo para cima",
             reforco="almofadas maciças nos 2 lados do eixo; 2 nervuras que abraçam o horn",
             obs="sem parafuso por fora: o horn encaixa entre 2 nervuras (direita) e o pino da mesa entra no soquete cego (esquerda); abre e encaixa por pressão"),
        Peca("mesa-cabeca", g(mesa), material="PETG", cor="grafite", grupo="cabeca", imprimir=rot("x", 180), macica=True, explode=(0, 0, 95),
             suporte="não", perimetros=4, infill=30, orientacao="de cabeça para baixo: face de cima na mesa",
             reforco="placa de 4 mm; janela do servo da boca com cantos em chanfro (ponte de 19,6 mm); assento cônico do alto-falante",
             obs="mesa da cabeça: 2 M3x10 na coluna do berço (por cima, pelos furos sob o topete); segura o servo da boca, o pino do eixo da mandíbula e o alto-falante"),
        Peca("olho", g(olhos[0]), cor="branco", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(20, 60, 170), orientacao="face de trás (plana) na mesa",
             obs="olho direito: bolso da câmera (Camera Module 3) aberto por trás; pressão ou cola no copo do crânio"),
        Peca("olho-esq", g(olhos[1]), cor="branco", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-20, 60, 170), orientacao="face de trás (plana) na mesa",
             obs="olho esquerdo: bolso do sensor ToF aberto por trás"),
        Peca("iris", g(iris[0]), cor="marrom", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(24, 80, 176), orientacao="face de trás na mesa",
             obs="anel da íris: a placa da câmera encosta atrás dele (4 furos piloto M2)"),
        Peca("iris-esq", g(iris[1]), cor="marrom", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-24, 80, 176), orientacao="face de trás na mesa"),
        Peca("pupila", g(pups[0]), cor="preto", grupo="cabeca", macica=True, imprimir=imp_olho[0], explode=(28, 100, 182), orientacao="face de trás na mesa",
             obs="pupila escura VAZADA no centro (a lente da câmera olha pelo furo); pressão, sem cola (dá acesso à lente)"),
        Peca("pupila-esq", g(pups[1]), cor="preto", grupo="cabeca", macica=True, imprimir=imp_olho[1], explode=(-28, 100, 182), orientacao="face de trás na mesa",
             obs="pupila escura vazada (janela do ToF)"),
    ]
    pecas += [
        Peca("focinho", pcc["focinho"], grupo="cabeca", imprimir=relc["focinho"].imprimir, explode=(0, 120, 160), obs="tampa marrom do focinho; cola", **marrom),
        Peca("orelha-dir", pcc["orelha-dir"], grupo="cabeca", imprimir=relc["orelha-dir"].imprimir, explode=(30, 0, 200), obs="orelha direita; cola", **marrom),
        Peca("orelha-esq", pcc["orelha-esq"], grupo="cabeca", imprimir=relc["orelha-esq"].imprimir, explode=(-30, 0, 200), obs="orelha esquerda; cola", **marrom),
        Peca("topete", pcc["topete"], cor="laranja", grupo="cabeca", macica=True, imprimir=relc["topete"].imprimir, explode=(0, 0, 215),
             orientacao="base plana na mesa", obs="topete; encaixe por pressão (sem cola): tampa os 2 furos de acesso aos parafusos da mesa"),
    ]

    # ------------------------------------------------------------ esqueleto baixo
    teste = BS.teste_encaixe()
    teste.copias = []
    pecas += [chassi, BB.capa_esfera(E), BB.bandeja_pi(E), BB.bandeja_uno(E), *BB.pescoco(E), teste]
    comps += comps_esq

    juntas = BB.juntas(E)
    yp, zp = bo["y_eixo"], bo["z_eixo"]
    juntas["mandibula"] = Junta("cabeca", (0, yp, zp), (-1, 0, 0), N.boca)
    poses = [("neutra", {}),
             ("pan-esq", {"pan": N.pan[1]}), ("pan-dir", {"pan": N.pan[0]}),
             ("tilt-cima", {"cabeca": N.tilt[1]}), ("tilt-baixo", {"cabeca": N.tilt[0]}),
             ("boca-aberta", {"mandibula": N.boca[1]}),
             ("pan+tilt-baixo+boca", {"pan": N.pan[1], "cabeca": N.tilt[0], "mandibula": N.boca[1]}),
             ("pan+tilt-cima", {"pan": N.pan[0], "cabeca": N.tilt[1]})]
    # parede medida longe das tampas (a pele é fechada no topo do corpo e na base da grade da cabeça só para o cálculo)
    parede = {"corpo": medir_parede(ext, CA.fatia_z(inte, K.z_fundo + 1.0, z_top - 1.0)),
              "cabeça": medir_parede(c_ext, CA.fatia_z(c_int, BS.CZ + K.cabeca_z + 4.0, 900.0))}
    encaixes = [{"par": ["motor-tt-dir", "roda-dir"], "motivo": "eixo do motor entra no cubo da roda"},
                {"par": ["motor-tt-esq", "roda-esq"], "motivo": "eixo do motor entra no cubo da roda"}]
    cab = ["cranio", "mesa-cabeca", "mandibula", "servo-boca MG90S", "olho", "olho-esq", "iris", "iris-esq", "pupila", "pupila-esq",
           "focinho", "orelha-dir", "orelha-esq", "topete", "camera olho direito (fase 2)", "tof-olho esquerdo (fase 2)",
           "microfone-dir (fase 2)", "microfone-esq (fase 2)", "alto-falante (fase 2)"]
    return Modelo("capivara", "Capivara", pecas, comps, juntas, BB.apoios(E), poses, ordem=_ordem(cab),
                  obs={"parede_medida": parede, "explode_grupo": {"cabeca": (0, 0, 95), "pan": (0, 0, 30), "mandibula": (0, 70, 85)}}, encaixes=encaixes)


def _ordem(cab):
    """Ordem de montagem e de abertura (teste 9). `dir` = de onde a peça vem."""
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    nX, nY, nZ = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
    tras = [dict(passo="bateria (entra por trás, pelo piso)", move=["bateria 2x18650"], dir=nY, curso=170),
            dict(passo="bandeja do Pi", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=170),
            dict(passo="bandeja do Uno", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=170)]
    o = [
        dict(passo="chassi", move=["chassi"], dir=Z),
        dict(passo="motor direito", move=["motor-tt-dir"], dir=X),
        dict(passo="motor esquerdo", move=["motor-tt-esq"], dir=nX),
        dict(passo="step-down 5 V (parede esquerda da torre, abraçadeira)", move=["step-down 5V (LM2596)"], dir=nX, curso=60),
        dict(passo="UBEC 6 V (parede direita da torre, abraçadeira)", move=["ubec 6V 3A"], dir=X, curso=60),
        dict(passo="BMS 2S (no piso, sob o lugar do L298N)", move=["bms 2S"], dir=Z, curso=6, depois=[(0, 1, 0), 90]),
        dict(passo="chave (por baixo do piso)", move=["chave"], dir=nZ, curso=40),
        dict(passo="roda direita", move=["roda-dir"], dir=X),
        dict(passo="roda esquerda", move=["roda-esq"], dir=nX),
        dict(passo="esferas de apoio + capas", move=["esfera-dir", "esfera-esq", "capa-esfera"], dir=nZ, curso=40),
        dict(passo="driver L298N (pela frente da torre)", move=["driver L298N"], dir=Y, curso=120),
        dict(passo="servo de pan", move=["servo-pan MG996R"], dir=Z),
        dict(passo="corpo (bacia) desce por cima do chassi", move=["corpo", "mao-dir", "mao-esq", "avental", "aro", "miolo", "tof-dir (fase 2)", "tof-esq (fase 2)"], dir=Z, curso=240),
        dict(passo="garfo (por dentro da boca da bacia)", move=["garfo-pescoco"], dir=Z, curso=160),
        dict(passo="berço + servo de tilt", move=["berco-tilt", "servo-tilt MG996R"], dir=Z, curso=160),
        dict(passo="gola-bandana", move=["gola"], dir=Z, curso=160),
        *tras,
        dict(passo="porta traseira (com o rabo e o carregador USB-C)", move=["porta", "rabo", "carregador USB-C 2S"], dir=nY, curso=170),
        dict(passo="mesa dentro do crânio (na bancada)", move=["mesa-cabeca", "servo-boca MG90S", "alto-falante (fase 2)"], dir=nZ, curso=100, contra=["cranio"]),
        dict(passo="cabeça no pescoço", move=list(cab), dir=Z, curso=160),
        # abertura para manutenção SEM tirar a cabeça: porta, bandejas e bateria saem por trás
        dict(passo="ABRIR: porta traseira sai", move=["porta", "rabo", "carregador USB-C 2S"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bandeja do Uno sai", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bandeja do Pi sai", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bateria sai", move=["bateria 2x18650"], dir=nY, curso=170, sai=True),
    ]
    return o
