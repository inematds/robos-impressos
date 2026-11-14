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
from cad.comum.base import F, N
from cad.comum.geo import (caixa, cil, esfera, espelho_x, mat_giro, mat_trans, maior_corpo, medir_parede, sdf_elipsoide, smin, uniao)
from cad.comum.modelo import Junta, Modelo, Peca, rot

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
    H = CA.campo_cabeca(base, C0, K.soquete_r, zb)
    bo = _boca(K.dy, 0.0)
    # mandíbula aberta: a parte de baixo da boca, girada no eixo dela, também varre
    z_boca = bo["z0"] + bo["incl"] * (Pg[..., 1] - bo["y_ref"]) + 8.0
    Hj = np.maximum(np.maximum(H, bo["y_corte"] - Pg[..., 1]), Pg[..., 2] - z_boca)
    H = np.minimum(H, CA.reamostrar(base, Hj, mat_giro((0, bo["y_eixo"], bo["z_eixo"]), (-1, 0, 0), N.boca[1])))
    pans = np.arange(N.pan[0], N.pan[1] + 0.1, 15.0)
    tilts = np.unique(np.concatenate([np.linspace(N.tilt[0], 0, 3), np.linspace(0, N.tilt[1], 3)]))
    S = CA.zona_varrida(base, H, C0, pans, tilts, (-115, C0[1] - 120, 96), (115, C0[1] + 140, z_top + 14), chave=f"{K.pele}|{K.dy}")
    del H, Hj

    # ------------------------------------------------------------ corpo = pele + ancas - zona varrida
    def campo_corpo(Pp, Fp):
        d = Fp
        for (c, r) in K.anca:
            for s in (1, -1):
                d = smin(d, sdf_elipsoide(Pp, (s * c[0], c[1] + K.dy, c[2]), r), 6.0)
        return np.maximum(np.maximum(d, K.folga_junta - S), Pp[..., 2] - (z_top + 6.0))

    p_corpo = base.combinar(campo_corpo)
    del S
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
    obst = BB.obstaculos_bacia(E, chassi.solido, [c.solido for c in comps_esq if c.nome.startswith(("driver", "motor"))])
    bacia = maior_corpo(CA.fatia_z(casca, K.z_fundo, K.z_gola) - obst)
    for (x, y, s) in E.orelhas:                         # atrás: 2 orelhas no piso (M3 por baixo)
        for sx in (1, -1):
            o, fi = BI.orelha_piso(sx * x, y, ext, para=(0, s, 0))
            bacia = bacia + (o - obst) - fi
    o, fi = BB.orelhas_esfera(E, ext)                   # na frente: em cima dos ressaltos das esferas (os parafusos da capa)
    bacia = bacia + o - fi
    px, yd = K.porta.x, K.porta.y_max + K.dy
    porta = maior_corpo(bacia ^ caixa(-px + F.encaixe, px - F.encaixe, -400, yd, -50, 400))
    bacia = maior_corpo(bacia - caixa(-px, px, -400, yd, -50, 400))
    # porta: 2 M3 por trás, nos postes do chassi (tubo rebaixado da pele até o poste)
    x0, x1, pya, pyb, pzt, pzp = E.poste_porta
    for sx in (1, -1):
        xp = sx * (x0 + x1) / 2
        porta = porta + (cil((xp, pya - 0.3, pzp), (xp, pya - 80, pzp), 5.2) ^ ext)
        porta = porta - cil((xp, pya - 3.3, pzp), (xp, pya - 90, pzp), F.cabeca_m3_d / 2 + 0.1, seg=24) - cil((xp, pya + 1, pzp), (xp, pya - 5, pzp), F.m3_passante / 2, seg=24)
    # ------------------------------------------------------------ gola-bandana (esfera do pescoço)
    gola = maior_corpo(CA.fatia_z(casca, K.z_gola + F.encaixe, z_top))

    pecas += [
        Peca("corpo", bacia, cor="laranja", suporte="sim (provisório)", explode=(0, 0, 60),
             orientacao="borda de baixo (z=5) na mesa, como um vaso", obs="bacia inteira do corpo; entra por cima do chassi; 4 M3 por baixo"),
        Peca("porta", porta, cor="laranja", suporte="sim (provisório)", explode=(0, -120, 0),
             orientacao="borda de baixo na mesa, em pé", obs="porta traseira: bateria e bandejas saem por aqui; 2 M3 por trás"),
        Peca("gola", gola, cor="verde-bandana", suporte="sim (provisório)", explode=(0, 0, 100),
             orientacao="borda de baixo (z=124) na mesa", obs="gola-bandana: esfera em que a cabeça gira; assenta na borda da bacia"),
    ]

    # ------------------------------------------------------------ cabeça (construída no referencial do pescoço padrão)
    p_cab = CA.carregar(K.pele, dy=K.dy - T[1], dz=-T[2])
    czs = BS.CZ
    p_cab = p_cab.recortar((-200, -400, czs - 8.0), (200, 400, 600))
    boca = _boca(K.dy - T[1], -T[2])
    cran, mand, c_ext, c_int = BI.cabeca(p_cab, boca, r_soquete=K.soquete_r, cabeca_z=K.cabeca_z)
    o = K.olho
    olhos, iris, pups = [], [], []
    ps = p_cab.ponto_na_pele((o.x, 300.0, o.z - T[2]), (0, -1, 0))
    nrm = CA.normal(p_cab, ps, 3.0)
    c_olho = ps - nrm * o.r * o.afunda
    for s in (1, -1):
        esp = np.array([s, 1, 1.0])
        cran, ol, ir, pu = BI.olho(c_olho * esp, o.r, nrm * esp, o.iris_r, o.pupila_r, cran, c_ext)
        olhos.append(ol), iris.append(ir), pups.append(pu)
    cran, mand, mesa, comps_cab, M_bucha = BI.mecanica_cabeca(p_cab, cran, mand, c_ext, c_int, boca, zcam=0.0, camera=False, aparar_r=K.soquete_r)
    Tl = list(T)
    for c in comps_cab:
        c.solido = c.solido.translate(Tl)
    comps += comps_cab
    g = lambda m: m.translate(Tl)
    pecas += [
        Peca("cranio", g(cran), cor="laranja", grupo="cabeca", suporte="sim (provisório)", explode=(0, 0, 150),
             orientacao="borda de baixo (z=152) na mesa", obs="3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto dão acesso aos parafusos da coluna"),
        Peca("mandibula", g(mand), cor="laranja", grupo="mandibula", suporte="sim (provisório)", explode=(0, 70, 85),
             obs="horn do servo na direita (parafuso central por fora); M3x16 + bucha na esquerda"),
        Peca("mesa-cabeca", g(mesa), material="PETG", cor="grafite", grupo="cabeca", imprimir=rot("x", 180), macica=True, explode=(0, 0, 95),
             obs="mesa da cabeça: 2 M3x10 na coluna do berço (por cima); segura o servo da boca"),
        Peca("olho", g(olhos[0]), cor="branco", grupo="cabeca", macica=True, explode=(20, 60, 170), obs="direito"),
        Peca("olho-esq", g(olhos[1]), cor="branco", grupo="cabeca", macica=True, explode=(-20, 60, 170), obs="esquerdo (espelhado)"),
        Peca("iris", g(iris[0]), cor="marrom", grupo="cabeca", macica=True, explode=(24, 80, 176)),
        Peca("iris-esq", g(iris[1]), cor="marrom", grupo="cabeca", macica=True, explode=(-24, 80, 176)),
        Peca("pupila", g(pups[0]), cor="preto", grupo="cabeca", macica=True, explode=(28, 100, 182)),
        Peca("pupila-esq", g(pups[1]), cor="preto", grupo="cabeca", macica=True, explode=(-28, 100, 182)),
    ]
    bucha = BS.bucha_eixo([mat_trans(T) @ M_bucha])
    bucha.grupo = "mandibula"
    pecas.append(bucha)

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
    cab = ["cranio", "mesa-cabeca", "mandibula", "bucha-eixo", "servo-boca MG90S", "olho", "olho-esq", "iris", "iris-esq", "pupila", "pupila-esq"]
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
        dict(passo="roda direita", move=["roda-dir"], dir=X),
        dict(passo="roda esquerda", move=["roda-esq"], dir=nX),
        dict(passo="esferas de apoio + capas", move=["esfera-dir", "esfera-esq", "capa-esfera"], dir=nZ, curso=40),
        dict(passo="driver L298N (pela frente da torre)", move=["driver L298N"], dir=Y, curso=120),
        dict(passo="servo de pan", move=["servo-pan MG996R"], dir=Z),
        dict(passo="corpo (bacia) desce por cima do chassi", move=["corpo"], dir=Z, curso=240),
        dict(passo="garfo (por dentro da boca da bacia)", move=["garfo-pescoco"], dir=Z, curso=160),
        dict(passo="berço + servo de tilt", move=["berco-tilt", "servo-tilt MG996R"], dir=Z, curso=160),
        dict(passo="gola-bandana", move=["gola"], dir=Z, curso=160),
        *tras,
        dict(passo="porta traseira", move=["porta"], dir=nY, curso=170),
        dict(passo="mesa dentro do crânio (na bancada)", move=["mesa-cabeca", "servo-boca MG90S"], dir=nZ, curso=100, contra=["cranio"]),
        dict(passo="cabeça no pescoço", move=list(cab), dir=Z, curso=160),
        # abertura para manutenção SEM tirar a cabeça: porta, bandejas e bateria saem por trás
        dict(passo="ABRIR: porta traseira sai", move=["porta"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bandeja do Uno sai", move=["bandeja-uno", "Arduino Uno + shield"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bandeja do Pi sai", move=["bandeja-pi", "Raspberry Pi 4/5"], dir=nY, curso=170, sai=True),
        dict(passo="ABRIR: bateria sai", move=["bateria 2x18650"], dir=nY, curso=170, sai=True),
    ]
    return o
