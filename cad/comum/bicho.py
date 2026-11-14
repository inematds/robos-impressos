"""Ferramentas para vestir o esqueleto comum com a casca de um bicho (dinossauro, capivara, ...).

A casca é sempre: torso em duas metades (frente/costas, costura no plano Y=BASE.costura_y, que passa
pelo eixo do pescoço), "gola" esférica no topo do torso (a cabeça gira e inclina em volta dela),
pernas/coxas que cobrem as rodas, uma peça traseira que cobre a esfera de apoio, crânio + mandíbula.
"""
from __future__ import annotations

import numpy as np
from manifold3d import Manifold

from cad import parametros as P
from cad.comum import base as BS
from cad.comum.base import B, CX, CY, CZ, F, N, Z0, Z1, furo, inserto, sim
from cad.comum.geo import (Pele, arrastar, caixa, campo_blobs, casco, cil, elipsoide, esfera, espelho_x, girar, limites, maior_corpo,
                           mat_giro, mat_trans, prisma, sdf_elipsoide, smin, uniao)

RIM_Z = Z1 + 0.2          # as orelhas das cascas assentam 0,2 acima do piso
SAIA_Z = Z0 - 2.0         # a parede do torso desce 2 mm abaixo do piso e esconde a placa
CHAO_Z = 3.0              # borda de baixo de pernas e cauda (3 mm acima do chão)
LUG_Z = (RIM_Z, RIM_Z + 7.5)


def limites_blobs(blobs):
    lo = np.min([np.asarray(b[0]) - np.asarray(b[1]) for b in blobs], axis=0)
    hi = np.max([np.asarray(b[0]) + np.asarray(b[1]) for b in blobs], axis=0)
    return lo, hi


def pele_blobs(blobs, k=12.0, h=1.25, extra=None, margem=8.0):
    """Pele de uma lista de blobs; `extra(P, d)` pode combinar outro campo."""
    f0 = campo_blobs(blobs, k)
    f = (lambda Pp: extra(Pp, f0(Pp))) if extra else f0
    lo, hi = limites_blobs(blobs)
    return Pele(f, lo, hi, h=h, margem=margem)


def pele_torso(blobs, k=14.0, h=1.25):
    """Torso + gola esférica do pescoço."""
    c = np.array(N.centro, np.float32)

    def extra(Pp, d):
        e = np.linalg.norm(Pp - c, axis=-1) - N.gola_r
        return smin(d, e, 8.0)

    f0 = campo_blobs(blobs, k)
    lo, hi = limites_blobs(blobs)
    hi = np.maximum(hi, c + N.gola_r)
    lo = np.minimum(lo, c - N.gola_r)
    return Pele(lambda Pp: extra(Pp, f0(Pp)), lo, hi, h=h)


def espelhar_blobs(blobs):
    return [((-b[0][0], b[0][1], b[0][2]), b[1]) + tuple(b[2:]) for b in blobs]


# ---------------------------------------------------------------- orelhas de fixação (insertos M3)
def orelha_piso(x, y, ext: Manifold, para=(1, 0, 0), rampa=None, larg=9.0, comp=10.0):
    """Orelha com inserto M3 vertical (parafuso vem de baixo, pelo piso do chassi).
    `para` = direção em que a orelha se estende até encontrar a parede da casca.
    `rampa` = direção (na impressão) de onde vem a mesa: cria a rampa autoportante."""
    z0, z1 = LUG_Z
    para = np.asarray(para, float)
    ex = 60.0
    hx, hy = (comp / 2, larg / 2) if abs(para[0]) > 0 else (larg / 2, comp / 2)
    bl = caixa(x - hx, x + hx, y - hy, y + hy, z0, z1)
    far = bl.translate(list(para * ex))
    corpo = casco(bl, far)
    if rampa is not None:
        r = np.asarray(rampa, float)
        base = caixa(x - hx, x + hx, y - hy, y + hy, z0, z0 + 0.6).translate(list(para * 14.0 + r * (z1 - z0 + 6)))
        corpo = corpo + casco(bl, base, far)
    corpo = corpo ^ ext
    return corpo, inserto((x, y, z0), (0, 0, 1))


def gordo(pele: Pele, folga=None) -> Manifold:
    return pele.deslocado(F.casca if folga is None else folga)


# ---------------------------------------------------------------- torso
def torso(pele: Pele, rodas=True):
    """Devolve (frente, costas, ext, int) já com: borda de baixo, abertura da gola, poços das rodas,
    orelhas de fixação no piso e pinos-guia. Recortes do modelo (barriga, cristas...) vêm depois."""
    ext = pele.solido()
    inte = pele.deslocado(-F.parede)
    casca = ext - inte
    lo, hi = limites(ext)
    casca = casca - caixa(lo[0] - 5, hi[0] + 5, lo[1] - 5, hi[1] + 5, lo[2] - 5, SAIA_Z) - BS.piso_solido(0.6, -5, RIM_Z)
    # abertura do topo da gola (por onde sobe a coluna do berço)
    casca = casca - cil((CX, CY, CZ + 8), (CX, CY, CZ + N.gola_r + 5), N.gola_abertura_r, seg=64)
    if rodas:
        r = P.RODA.d / 2 + 3.5
        poco = cil((BS.X_RODA - 3.5, 0, B.eixo_roda_z), (BS.X_RODA + P.RODA.larg + 40, 0, B.eixo_roda_z), r, seg=64)
        casca = casca - sim(poco)
    ys = B.costura_y
    if rodas:
        ez = B.eixo_roda_z
        casca = casca - sim(caixa(BS.X1 + P.TT.caixa[2] - 1, 200, ys - 0.1, 0, ez - P.TT.eixo_d / 2 - 2, ez + P.TT.eixo_d / 2 + 2))
    frente = casca ^ caixa(lo[0] - 5, hi[0] + 5, ys, hi[1] + 5, lo[2] - 5, hi[2] + 5)
    costas = casca ^ caixa(lo[0] - 5, hi[0] + 5, lo[1] - 5, ys, lo[2] - 5, hi[2] + 5)
    # caminho de montagem: a frente entra deslizando para trás e as costas para a frente, por cima do piso.
    # Tira da saia tudo o que o piso varreria nesse movimento, e fica só com o corpo principal.
    env = BS.piso_solido(0.6, -5, RIM_Z)
    frente = maior_corpo(frente - arrastar(env, (0, -1, 0)))        # do ponto de vista da casca, o piso "anda" para trás
    costas = maior_corpo(costas - arrastar(env + BS.obstaculos_tras(), (0, 1, 0)))
    # orelha traseira no piso (parafuso M3 por baixo, na lança do chassi)
    for (x, y) in B.furos_torso_costas:
        for s in ((1, -1) if x else (1,)):
            o, fi = orelha_piso(s * x, y, ext, para=(0, -1, 0))
            costas = costas + o - fi
    for (x, y) in B.furos_torso_frente:
        o, fi = orelha_piso(x, y, ext, para=(0, 1, 0), larg=9.0, comp=8.0)
        frente = frente + o - fi
    return frente, costas, ext, inte


def pinos_torso(frente, costas, ext, inte, pontos):
    """Pinos-guia na costura: bloco em cada metade + furo. pontos = [(x, z)]. Devolve também as matrizes dos pinos."""
    ys = B.costura_y
    mats = []
    for (x, z) in pontos:
        s = 1 if x >= 0 else -1
        bl = caixa(min(x - s * 4, x + s * 30), max(x - s * 4, x + s * 30), ys - 6, ys + 6, z - 4, z + 4) ^ ext
        bl = bl - cil((CX, CY, CZ + 8), (CX, CY, CZ + N.gola_r + 5), N.gola_abertura_r, seg=64)
        fu = cil((x, ys - 4.7, z), (x, ys + 4.7, z), F.pino_d / 2 + F.encaixe / 2, seg=24)
        frente = frente + (bl ^ caixa(-999, 999, ys, 999, -999, 999)) - fu
        costas = costas + (bl ^ caixa(-999, 999, -999, ys, -999, 999)) - fu
        mats.append(mat_trans((x, ys + 4.5, z)) @ mat_giro((0, 0, 0), (1, 0, 0), 90))
    return frente, costas, mats


def parafuso_costas_deck(costas, ext):
    """Parafuso do alto das costas: tubo rebaixado da pele até o ressalto traseiro do deck (fica sob a crista/laço)."""
    z = B.deck_z - B.deck_esp / 2
    y_res = B.parede_y[0] - 6.0          # face de trás do ressalto do deck
    tubo = cil((0, y_res - 0.3, z), (0, y_res - 60, z), 5.2) ^ ext
    costas = costas + tubo
    costas = costas - cil((0, y_res - 3.3, z), (0, y_res - 70, z), F.cabeca_m3_d / 2 + 0.1, seg=24) - cil((0, y_res + 1, z), (0, y_res - 5, z), F.m3_passante / 2, seg=24)
    return costas


# ---------------------------------------------------------------- pernas e traseiro
def varredura_costas(torso_gordo: Manifold) -> Manifold:
    """Volume que o torso-costas varre ao sair para trás (-Y): silhueta da metade de trás, extrudada."""
    tras = torso_gordo ^ caixa(-400, 400, -400, B.costura_y, -50, 500)
    sil = tras.transform([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0]]).project()        # (x, z) no plano; y vira altura
    sil = sil.offset(1.2, __import__("manifold3d").JoinType.Round)                       # folga para as costas passarem sem raspar
    return Manifold.extrude(sil, 300).transform([[1, 0, 0, 0], [0, 0, -1, B.costura_y], [0, 1, 0, 0]])


def perna(pele: Pele, torso_gordo: Manifold, furos=None, lado=1):
    """Casca da perna direita (lado=1): cobre a roda, aberta embaixo e do lado do torso."""
    ext = pele.solido()
    casca = ext - pele.deslocado(-F.parede)
    lo, hi = limites(ext)
    casca = casca - torso_gordo - caixa(lo[0] - 5, hi[0] + 5, lo[1] - 5, hi[1] + 5, lo[2] - 5, CHAO_Z) - varredura_costas(torso_gordo)
    # nada da casca pode ficar para dentro do plano da face da caixa do motor
    casca = casca - caixa(-5, BS.X1 + P.TT.caixa[2] + 1.0, -400, 400, -50, 400)
    for (x, y) in (furos if furos is not None else B.furos_perna):
        o, fi = orelha_piso(x, y, ext, para=(0, 1 if y > 0 else -1, 0), larg=9.0, comp=9.0)
        casca = casca + (o - torso_gordo - varredura_costas(torso_gordo)) - fi
    return casca, ext


def traseiro(pele: Pele, torso_gordo: Manifold):
    """Casca traseira (cauda ou rabo): cobre a esfera de apoio; presa por 2 orelhas na pá da lança."""
    ext = pele.solido()
    casca = ext - pele.deslocado(-F.parede)
    lo, hi = limites(ext)
    casca = casca - torso_gordo - caixa(lo[0] - 5, hi[0] + 5, lo[1] - 5, hi[1] + 5, lo[2] - 5, CHAO_Z)
    casca = maior_corpo(casca - arrastar(BS.piso_solido(0.6, -5, RIM_Z), (0, 1, 0)))      # a traseira sai deslizando para trás
    for (x, y) in B.furos_cauda:
        for s in (1, -1):
            o, fi = orelha_piso(s * x, y, ext, para=(s, 0, 0), larg=9.0, comp=9.0)
            casca = casca + (o - torso_gordo) - fi
    return casca, ext


# ---------------------------------------------------------------- cabeça
def cabeca(pele: Pele, boca: dict, junta=None, r_soquete=None, cabeca_z=None):
    """Crânio e mandíbula a partir da pele da cabeça.
    boca = {y_eixo, z_eixo, y_corte, z0, incl (dz/dy), raio_sorriso, folga}.
    Por bicho (padrão = PESCOCO): `r_soquete` = raio da esfera oca em volta da junta (padrão gola_r + junta);
    `cabeca_z` = altura do plano de baixo da cabeça acima do centro da junta."""
    ext = pele.solido()
    inte = pele.deslocado(-F.parede)
    casca = ext - inte
    lo, hi = limites(ext)
    zb = CZ + (N.cabeca_z if cabeca_z is None else cabeca_z)
    casca = casca - caixa(lo[0] - 5, hi[0] + 5, lo[1] - 5, hi[1] + 5, lo[2] - 5, zb)
    junta = F.junta_esfera if junta is None else junta
    if r_soquete is not None:
        junta = r_soquete - N.gola_r
    casca = casca - esfera((CX, CY, CZ), N.gola_r + junta, seg=96)
    g = boca.get("folga", 1.2)

    def inferior(dz):
        """Região abaixo da superfície da boca (cilindro de raio grande = sorriso), deslocada dz."""
        R = boca["raio_sorriso"]
        z0 = boca["z0"] + dz
        ang = np.degrees(np.arctan(boca["incl"]))
        cilg = cil((0, -300, z0 + R), (0, 300, z0 + R), R, seg=180)
        cilg = girar(cilg, (0, boca["y_ref"], z0), (1, 0, 0), ang)
        bloco = girar(caixa(-200, 200, -300, 300, z0 - 200, z0 + R), (0, boca["y_ref"], z0), (1, 0, 0), ang)
        return bloco - cilg

    yc, yp, zp = boca["y_corte"], boca["y_eixo"], boca["z_eixo"]
    mand = casca ^ inferior(-g / 2) ^ caixa(-200, 200, yc, 400, 0, 500)
    # a parte de baixo/atrás da mandíbula recua ao abrir: afasta da esfera da gola o tanto desse recuo
    recuo = max(zp - zb, 0.0) * np.sin(np.radians(abs(N.boca[1]))) + 1.5
    mand = mand - esfera((CX, CY, CZ), N.gola_r + junta + recuo, seg=96)
    # crânio: tira a região da mandíbula + cunha atrás/abaixo do eixo (onde a mandíbula recua ao abrir)
    t = np.tan(np.radians(abs(N.boca[1]) + 3))
    cunha = prisma([(yc - g - (zp - (zb - 5)) * t, zb - 5), (yc - g, zp), (yc - g, 500), (400, 500), (400, zb - 5)], "x", -200, 200)
    cran = casca - (inferior(+g / 2) ^ cunha)
    return cran, mand, ext, inte


def olho(c, r, direcao, iris_r, pupila_r, cran, cab_ext, lado_plano=0.30):
    """Copo do olho no crânio + olho (calota), íris e pupila como peças de encaixe.
    Devolve (cranio, olho, iris, pupila) na posição de montagem."""
    c = np.asarray(c, float)
    d = np.asarray(direcao, float)
    d = d / np.linalg.norm(d)
    fol = F.encaixe / 2
    copo = (esfera(c, r + fol + F.parede, seg=64) - esfera(c, r + fol, seg=64)) ^ cab_ext
    cran = (cran - esfera(c, r + fol, seg=64)) + copo
    meio = cil(c - d * r * lado_plano, c + d * (r + 5), r + 5)          # meia-esfera da frente (fundo plano)
    ol = esfera(c, r, seg=64) ^ meio
    cil_i = cil(c + d * r * 0.45, c + d * (r + 5), iris_r)
    iris = esfera(c, r, seg=64) ^ cil_i
    ol = ol - cil(c + d * (r * 0.45 - fol), c + d * (r + 5), iris_r + fol)
    cil_p = cil(c + d * r * 0.62, c + d * (r + 5), pupila_r)
    pup = esfera(c, r, seg=64) ^ cil_p
    iris = iris - cil(c + d * (r * 0.62 - fol), c + d * (r + 5), pupila_r + fol)
    return cran, ol, iris, pup


def crista(pele: Pele, pontos_yz, n_esp, alt, larg_base, esp=6.0, fundo=4.0, inclina=0.25, dentro=(0, 0, 0)):
    """Crista no plano de simetria (X=0): lâmina de `esp` mm com `n_esp` espinhos em folha.
    pontos_yz = lista de (y, z) FORA da pele, na ordem; cada ponto é projetado na pele na direção de `dentro`.
    Devolve (crista, bolso, nervura): bolso = recorte na casca; nervura = reforço por dentro."""
    from shapely.geometry import LineString, Polygon
    from shapely.ops import unary_union

    alvo = np.asarray(dentro, float)
    pele_pts = []
    for (y, z) in pontos_yz:
        o = np.array([0.0, y, z])
        dvec = alvo - o
        p = pele.ponto_na_pele(o, dvec)
        pele_pts.append((float(p[1]), float(p[2])))
    linha = LineString(pele_pts)
    # faixa de base: 1 mm para fora da pele, `fundo` para dentro
    faixa = linha.buffer(fundo, cap_style=2, single_sided=True)
    faixa2 = linha.buffer(-fundo, cap_style=2, single_sided=True)
    centro2d = (alvo[1], alvo[2])
    from shapely.geometry import Point

    base = faixa if faixa.centroid.distance(Point(centro2d)) < faixa2.centroid.distance(Point(centro2d)) else faixa2
    fora = faixa2 if base is faixa else faixa
    espinhos = []
    Ltot = linha.length
    for i in range(n_esp):
        s = Ltot * (i + 0.5) / n_esp
        p = np.array(linha.interpolate(s).coords[0])
        q = np.array(linha.interpolate(min(s + 1.0, Ltot)).coords[0])
        tg = (q - p) / (np.linalg.norm(q - p) + 1e-9)
        nrm = np.array([-tg[1], tg[0]])
        if np.dot(nrm, p - np.array(centro2d)) < 0:
            nrm = -nrm
        k = 1.0 - 0.25 * abs((i + 0.5) / n_esp - 0.5) * 2          # espinhos do meio maiores
        a = p - tg * larg_base / 2 * k - nrm * 1.0
        b = p + tg * larg_base / 2 * k - nrm * 1.0
        ap = p + nrm * alt * k + tg * inclina * alt * k
        tri = Polygon([tuple(a), tuple(ap), tuple(b)]).buffer(-2.0).buffer(3.2)
        espinhos.append(tri)
    forma = unary_union([base] + espinhos).buffer(0.01)
    forma = forma.simplify(0.05)

    def extr(poly, meia):
        ps = poly.geoms if hasattr(poly, "geoms") else [poly]
        return uniao(*[prisma(list(g.exterior.coords)[:-1], "x", -meia, meia) for g in ps])

    cr = extr(forma, esp / 2)
    bolso = extr(forma.buffer(F.encaixe, join_style=2), esp / 2 + F.encaixe)      # a crista inteira, com folga
    nerv = extr(base.buffer(0).buffer(F.parede, join_style=2), esp / 2 + F.parede)
    return cr, bolso, nerv


def elipse_y(cx, cz, rx, rz, y0, y1):
    """Cilindro elíptico ao longo de Y (janela da barriga)."""
    return cil((0, y0, 0), (0, y1, 0), 1.0, seg=96).scale([rx, 1, rz]).translate([cx, 0, cz])


def unha_local(r=9.0, alt=11.0, assento=2.4):
    """Unha: disco de assento + domo. Local: eixo +Z, fundo plano em z=0."""
    domo = elipsoide((0, 0, assento), (r, r, alt), seg=48) ^ caixa(-r - 1, r + 1, -r - 1, r + 1, assento, assento + alt + 1)
    return cil((0, 0, 0), (0, 0, assento + 0.01), r) + domo


def mat_de_z_para(n, p):
    """Matriz que leva o eixo +Z local para a direção n, com origem em p."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    z = np.array([0, 0, 1.0])
    v = np.cross(z, n)
    s = np.linalg.norm(v)
    M = np.eye(4)
    if s > 1e-9:
        v = v / s
        ang = np.degrees(np.arctan2(s, float(np.dot(z, n))))
        M = mat_giro((0, 0, 0), v, ang)
    elif n[2] < 0:
        M = mat_giro((0, 0, 0), (1, 0, 0), 180)
    M[:3, 3] = p
    return M


def bolso_unha(casca, ext, p, n, r=9.0, assento=2.4, prof=1.6):
    """Abre na casca o assento plano da unha (com reforço por dentro). Devolve (casca, matriz da unha)."""
    p = np.asarray(p, float)
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    base = p - n * prof
    reforco = cil(base - n * F.parede, base + n * 0.01, r + 2.0) ^ ext
    casca = casca + reforco - cil(base, base + n * 30, r + F.encaixe)
    return casca, mat_de_z_para(n, base + n * 0.02)


def mecanica_cabeca(p_cab: Pele, cran, mand, c_ext, c_int, boca, zcam, camera=True, aparar_r=None):
    """Tudo o que prende e move a cabeça, igual nos bichos: pilares da câmera (fase 2), orelhas crânio->mesa,
    almofadas do eixo da mandíbula, mesa da cabeça (com o servo da boca) e os componentes.
    `camera=False` deixa de fora o furo e os pilares da câmera na testa/focinho (bicho com os sensores nos olhos).
    `aparar_r` (raio do soquete): apara o que pende da mesa (placa do servo, orelha do eixo) contra a parede de
    dentro da cabeça e contra a esfera da junta (cabeça baixa e de queixo raso, como a da capivara).
    Devolve (cranio, mandibula, mesa, componentes, matriz_da_bucha)."""
    from cad.comum import componentes as C
    from cad.comum.modelo import Comp

    yp, zp = boca["y_eixo"], boca["z_eixo"]
    zm = CZ + N.mesa_z                    # face de baixo da mesa
    zmt = zm + N.mesa_esp
    # câmera (fase 2): furo da lente no focinho + 4 pilares M2 por dentro
    fx, fz = P.CAMERA.furos
    cw, ch = P.CAMERA.placa
    # a testa/focinho é inclinada: usa o ponto mais recuado da pele sobre a área da câmera
    if camera:
        ycam = min(p_cab.ponto_na_pele((sx * cw / 2, CY, zcam + sz * ch / 2), (0, 1, 0))[1] for sx in (1, -1) for sz in (1, -1))
        y_placa = ycam - F.parede - P.CAMERA.lente_alt - 1.5          # face de trás da placa da câmera
        pil = uniao(*[cil((sx * fx / 2, y_placa + 1.2, zcam + sz * fz / 2), (sx * fx / 2, ycam + 40, zcam + sz * fz / 2), 2.6, seg=20) for sx in (1, -1) for sz in (1, -1)]) ^ c_int
        cran = cran + pil
        for sx in (1, -1):
            for sz in (1, -1):
                cran = cran - cil((sx * fx / 2, y_placa, zcam + sz * fz / 2), (sx * fx / 2, y_placa + 7, zcam + sz * fz / 2), F.m2_piloto / 2, seg=12)
        cran = cran - cil((0, y_placa + 1.3, zcam), (0, ycam + 40, zcam), 7.0, seg=32)
    # fixação crânio -> mesa (feita na BANCADA, antes de a cabeça ir para o pescoço): 2 orelhas na frente,
    # junto aos cantos da boca, + 1 atrás; os 3 parafusos M3 entram por baixo, pela mesa.
    fix = [(46.0, yp + 8.0), (-46.0, yp + 8.0), (0.0, CY - 46.0)]
    for (fx_, fy_) in fix:
        if fx_:
            s_ = 1 if fx_ > 0 else -1
            orl = caixa(min(fx_ - s_ * 5, fx_ + s_ * 40), max(fx_ - s_ * 5, fx_ + s_ * 40), fy_ - 5, fy_ + 5, zmt + 0.2, zmt + 9.0) ^ c_ext
        else:
            orl = caixa(-6, 6, fy_ - 60, fy_ + 5, zmt + 0.2, zmt + 9.0) ^ c_ext
        cran = cran + orl
        cran = cran - inserto((fx_, fy_, zmt + 0.2), (0, 0, 1))
    # acesso da chave aos 2 parafusos mesa -> coluna: 2 furos no alto do crânio, no plano de simetria (a crista tampa)
    for (mx, my) in BS.POS_MESA:
        cran = cran - cil((mx, my, zmt + 2), (mx, my, zmt + 200), 3.3, seg=20)

    # mandíbula: almofada do horn (direita), furo do eixo livre (esquerda)
    xw = [p_cab.ponto_na_pele((0, yy, zp), (1, 0, 0))[0] for yy in (yp - 5, yp, yp + 10, yp + 22)]
    xflat = min(xw) - F.parede - 1.0
    almof = caixa(xflat, xflat + 30, yp - 5.5, yp + 23, zp - 5.5, zp + 5.5) ^ c_ext
    mand = mand + almof
    mand = mand - cil((xflat - 1, yp, zp), (xflat + 40, yp, zp), 1.6, seg=16)
    for dy in (10.0, 15.0):
        mand = mand - cil((xflat - 0.5, yp + dy, zp), (xflat + 3.0, yp + dy, zp), 0.75, seg=10)
    xwe = [p_cab.ponto_na_pele((0, yy, zp), (-1, 0, 0))[0] for yy in (yp - 5, yp, yp + 5)]
    xi_e = max(xwe) + F.parede + 1.0                  # face plana da almofada esquerda (negativo)
    mand = mand + (caixa(xi_e - 30, xi_e, yp - 5.5, yp + 5.5, zp - 5.5, zp + 5.5) ^ c_ext)
    mand = mand - cil((xi_e + 2, yp, zp), (xi_e - 40, yp, zp), F.m3_passante / 2, seg=16)
    mand = mand - cil((xi_e + 0.01, yp, zp), (xi_e + 14, yp, zp), 4.3, seg=24)      # assento plano da bucha

    # mesa da cabeça (fica de cabeça para baixo na impressão: o que pende, sobe)
    x_ponta = xflat - P.MICRO.horn[3]
    x_aba = x_ponta - P.MICRO.aba_ate_ponta
    mesa = uniao(caixa(-30, 30, CY - 18, yp + 23.5, zm, zmt), caixa(-8, 8, CY - 52, CY - 17.9, zm, zmt),
                 caixa(-52, 52, yp + 2.5, yp + 13.5, zm, zmt))
    mesa = mesa ^ p_cab.deslocado(-F.parede - 1.2)
    jl, jw = P.MICRO.janela
    ycs = yp - P.MICRO.eixo_da_ponta + P.MICRO.corpo[0] / 2
    placa_s = caixa(x_aba - 3, x_aba, ycs - P.MICRO.comp_abas / 2 - 1.5, ycs + P.MICRO.comp_abas / 2 + 1.5, zp - 8.5, zm + 0.01)
    placa_s = placa_s - caixa(x_aba - 4, x_aba + 1, ycs - jl / 2, ycs + jl / 2, zp - jw / 2, zp + jw / 2)
    for dy in (-P.MICRO.furos_aba / 2, P.MICRO.furos_aba / 2):
        placa_s = placa_s - furo((x_aba + 0.5, ycs + dy, zp), (-1, 0, 0), 4, F.m2_piloto)
    xl = xi_e + 4.1                      # face de fora da orelha do eixo livre (bucha de 3,4 no vão)
    orelha_e = caixa(xl, xl + 7.0, yp - 5.5, yp + 5.5, zp, zm + 0.01) + cil((xl, yp, zp), (xl + 7.0, yp, zp), 5.5) - inserto((xl, yp, zp), (1, 0, 0))
    mand = mand - cil((xl - 0.4, yp, zp), (xl + 8.0, yp, zp), 6.6)                 # alívio em volta da orelha do eixo
    mesa = mesa + (caixa(xl, 30, yp - 7, yp + 7, zm, zmt) ^ p_cab.deslocado(-F.parede - 1.2))
    if aparar_r is not None:
        dentro = p_cab.deslocado(-F.parede - 1.5) - esfera((CX, CY, CZ), aparar_r + 0.5, seg=96)
        placa_s, orelha_e = placa_s ^ dentro, orelha_e ^ dentro
    mesa = mesa + placa_s + orelha_e
    for (mx, my) in BS.POS_MESA:
        mesa = mesa - furo((mx, my, zm - 1), (0, 0, 1), 6, F.m3_passante) - furo((mx, my, zmt - 2.2), (0, 0, 1), 3, F.cabeca_m3_d)
    for (fx_, fy_) in fix:
        mesa = mesa - furo((fx_, fy_, zm - 1), (0, 0, 1), 6, F.m3_passante)
    # a mesa (com o que pende dela) tem que subir por baixo para dentro do crânio: tira dela a "sombra" de tudo
    # o que o crânio tem abaixo do topo da mesa
    baixo = cran ^ caixa(-400, 400, -400, 400, 0, zmt + 0.1)
    sombra = baixo.project().offset(1.0, __import__("manifold3d").JoinType.Round)
    mesa = mesa - Manifold.extrude(sombra, 120).translate([0, 0, zm - 70])
    mesa = mesa - caixa(-9, 9, CY + N.coluna_chato + 0.5, CY + N.coluna_chato + 7.5, zm - 1, zmt + 1)      # cabos sobem aqui

    M_boca = C.M([(0, 1, 0), (0, 0, 1), (1, 0, 0)], (x_aba, yp, zp))
    comps = []
    comps.append(Comp("servo-boca MG90S", C.micro_servo().transform(M_boca[:3, :]), "cabeca", P.MICRO.massa, "azul"))
    if camera:
        comps.append(Comp("camera (fase 2)", C.camera().translate([0, y_placa, zcam]), "cabeca", 4.0, "verde", fase2=True))

    Mb = mat_trans((xi_e + 0.35, yp, zp)) @ mat_giro((0, 0, 0), (0, 1, 0), 90)
    return cran, mand, mesa, comps, Mb


def frente_com_painel(p_torso: Pele, frente, costas, t_ext, t_int, bc, br, faixas=True, y_raio=-16.0, bracos=True, z_mic=None):
    """Painel da frente (barriga): janela + rebaixo no torso-frente, painel separado com a grade e o anel do
    alto-falante (fase 2), 2 parafusos do painel, 2 parafusos do torso-frente nos postes do chassi (escondidos
    sob o painel), furos do cubo dos braços, furos de microfone, janela do sensor da frente e ventilação do Pi.
    Devolve (frente, costas, painel, componente_alto_falante)."""
    from cad.comum import componentes as C
    from cad.comum.modelo import Comp

    # barriga creme: janela + rebaixo no torso-frente, painel separado (grade do alto-falante)
    t_m48 = p_torso.deslocado(-2 * F.parede)
    jan = elipse_y(bc[0], bc[1], br[0], br[1], -11, 200)
    frente = frente - jan
    reb = (t_int - t_m48) ^ (elipse_y(bc[0], bc[1], br[0] * 1.10, br[1] * 1.10, -11, 200) - elipse_y(bc[0], bc[1], br[0] * 0.87, br[1] * 0.87, -12, 201))
    frente = frente + reb
    barriga = (t_ext - t_int) ^ elipse_y(bc[0], bc[1], br[0] - 0.3, br[1] - 0.3, -11, 200)
    # faixas da barriga (sulcos de 0,8 mm)
    t_m08 = p_torso.deslocado(-0.8)
    for zf in ((bc[1] - 26, bc[1] - 13, bc[1] + 13, bc[1] + 26) if faixas else ()):
        barriga = barriga - (caixa(-60, 60, y_raio, 200, zf - 0.7, zf + 0.7) - t_m08)
    # alto-falante (fase 2): anel por dentro do painel + grade
    zfal = max(bc[1] + 15, B.driver_z + P.L298N.placa[1] / 2 + P.FALANTE.d / 2 + 4.5)   # acima do L298N
    rf = P.FALANTE.d / 2
    yrim = min(p_torso.ponto_na_pele((rf * np.cos(a), y_raio, zfal + rf * np.sin(a)), (0, 1, 0))[1] for a in np.linspace(0, 2 * np.pi, 12, endpoint=False))
    yfal = yrim - F.parede - 0.4                      # face da frente do alto-falante (plana), atrás da curva do painel
    anel = (cil((0, yfal - 6, zfal), (0, yfal + 30, zfal), rf + 2.6) - cil((0, yfal - 7, zfal), (0, yfal + 0.01, zfal), rf + 0.3)
            - cil((0, yfal, zfal), (0, yfal + 31, zfal), rf - 2.0)) ^ t_int
    barriga = barriga + anel
    for dz in (-12, -6, 0, 6, 12):
        meia = np.sqrt(max(17.0 ** 2 - dz ** 2, 1)) - 1
        barriga = barriga - caixa(-meia, meia, yfal - 1, yfal + 40, zfal + dz - 1.0, zfal + dz + 1.0)
    # 2 parafusos do painel (um de cada lado) com ressalto + inserto no rebaixo
    for sx in (1, -1):
        xx, zz = sx * (br[0] - 3.5), bc[1]
        yo = p_torso.ponto_na_pele((xx, y_raio, zz), (0, 1, 0))[1]
        res = cil((xx, yo - 10.4, zz), (xx, yo, zz), 4.6) ^ t_int ^ elipse_y(bc[0], bc[1], br[0] * 1.2, br[1] * 1.2, -11, 200)
        frente = frente + res
        frente = frente - cil((xx, yo - 2.0 - F.inserto_prof - 2.4, zz), (xx, yo + 1, zz), F.inserto_d / 2, seg=24)
        barriga = barriga - cil((xx, yo - 6, zz), (xx, yo + 3, zz), F.m3_passante / 2, seg=24) - cil((xx, yo - 1.2, zz), (xx, yo + 3, zz), F.cabeca_m3_d / 2, seg=24)
    # 2 parafusos de cabeça chata do torso-frente nos postes do chassi (ficam sob o painel da barriga)
    for (px, pz, pyt) in B.postes_frente:
        for s in (1, -1):
            yo = p_torso.ponto_na_pele((s * px, y_raio, pz), (0, 1, 0))[1]
            assert yo - 2 * F.parede > pyt + 1.0, f"poste ({px},{pz}) passa da casca: pele em y={yo:.1f}"
            res = cil((s * px, pyt + 0.3, pz), (s * px, yo, pz), 5.0) ^ t_int
            frente = frente + res
            frente = frente - cil((s * px, pyt - 1, pz), (s * px, yo + 1, pz), F.m3_passante / 2, seg=24)
            frente = frente - cil((s * px, yo - 2 * F.parede - 2.0, pz), (s * px, yo - F.parede + 0.8, pz), F.m3_passante / 2, 3.6, seg=24)
            barriga = barriga - cil((s * px, yo - F.parede - 0.6, pz), (s * px, yo - F.parede + 1.2, pz), 3.8, seg=24)
    # ombros: furo no torso para o cubo do braço
    oy, oz = B.ombro
    for s in ((1, -1) if bracos else ()):
        frente = frente - cil((s * 30, oy, oz), (s * 90, oy, oz), 10.5)
    # fase 2: furos do microfone (4 x Ø2) e janela do sensor de distância da frente, acima da barriga
    zmic = bc[1] + br[1] + 12 if z_mic is None else z_mic
    for xm in (-18, -6, 6, 18):
        frente = frente - cil((xm, y_raio, zmic), (xm, 120, zmic), 1.0, seg=12)
    frente = frente - cil((0, y_raio, bc[1] - br[1] - 9), (0, 120, bc[1] - br[1] - 9), 5.0, seg=24)
    # fase 2: ventilação do Pi nas costas (rasgos na altura da bandeja B)
    zv = B.trilho_z[1] + 14
    for i in range(5):
        costas = costas - caixa(-22 + i * 10, -22 + i * 10 + 4, -200, -76, zv - 12, zv + 12)

    falante = Comp("alto-falante (fase 2)", C.falante().translate([0, yfal - 0.2, zfal]), "corpo", P.FALANTE.massa, "preto", fase2=True)
    return frente, costas, barriga, falante


def painel(casca, ext, inte, m48, prisma_escala, folga=0.3, aba=(0.86, 1.10)):
    """Painel de outra cor encaixado na casca: abre a janela, cria o rebaixo por dentro e devolve o painel.
    prisma_escala(k) = sólido da janela escalado por k. Devolve (casca, painel)."""
    casca = casca - prisma_escala(1.0)
    reb = (inte - m48) ^ (prisma_escala(aba[1]) - prisma_escala(aba[0]))
    casca = casca + reb
    pn = (ext - inte) ^ prisma_escala(1.0, -folga)
    return casca, pn


def domo_local(r=14.0, alt=16.0, assento=2.4):
    return unha_local(r, alt, assento)
