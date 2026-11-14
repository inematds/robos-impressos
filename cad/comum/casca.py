"""Casca de um bicho a partir da pele em grade (malha de image-to-3D convertida por cad/pele_malha.py).

Receita (genérica: recebe a pele e os parâmetros do bicho; foi feita para a capivara e serve para o dino):
  1. `carregar(nome, dy)`               pele do repo (cad/peles/<nome>) no referencial do robô (eixo das rodas em Y=0)
  2. `campo_cabeca` + `zona_varrida`    campo da cabeça (pele acima do plano de baixo, fora do soquete esférico) e o
                                        volume que ela varre em TODAS as poses do pescoço (pan x tilt) e da boca
  3. corpo = pele (+ blobs) menos a zona varrida com folga  → a esfera da gola nasce sozinha (raio = soquete - folga)
  4. `casca.py` corta o corpo em "vasos" por planos horizontais (bacia, gola), cada um com a base plana na mesa
  5. peças coloridas = `relevo()` (pedaço da própria pele além de um plano: base plana, imprime sem suporte) e
     `painel_plano()` (recorte raso com fundo plano)

Tudo o que é CSG exato (furos, orelhas, cortes) continua em Manifold; só a forma orgânica vem do campo.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from manifold3d import Manifold
from scipy import ndimage
from skimage import measure

from cad.comum.geo import PeleGrade, caixa, mat_giro, para_numpy, prisma, uniao

RAIZ = Path(__file__).resolve().parent.parent.parent
DIR_PELES = RAIZ / "cad" / "peles"
DIR_CACHE = RAIZ / ".preview" / "cache"      # só acelera builds repetidos; apagar não muda o resultado


def carregar(nome: str, dy=0.0, dz=0.0, reduzir=0.75) -> PeleGrade:
    return PeleGrade.de_arquivo(DIR_PELES / nome, dy=dy, dz=dz, reduzir=reduzir)


def _cache(chave: str, fn):
    """Guarda um array caro (zona varrida) em .preview/cache, pela chave dos parâmetros + data da pele."""
    h = hashlib.sha1(chave.encode()).hexdigest()[:16]
    arq = DIR_CACHE / f"{h}.npy"
    if arq.exists():
        return np.load(arq)
    v = fn()
    try:
        DIR_CACHE.mkdir(parents=True, exist_ok=True)
        np.save(arq, v)
    except OSError:
        pass
    return v


# ---------------------------------------------------------------- campos
def campo_cabeca(pele: PeleGrade, centro, r_soquete, z_baixo):
    """Cabeça = pele acima do plano z_baixo e fora da esfera oca (soquete) em volta da junta do pescoço."""
    c = np.asarray(centro, np.float32)
    return np.maximum(np.maximum(pele.F, z_baixo - pele.P[..., 2]), r_soquete - np.linalg.norm(pele.P - c, axis=-1))


def reamostrar(pele: PeleGrade, campo, M, fatia=None):
    """Campo levado por um movimento rígido M (4x4): devolve campo'(p) = campo(M⁻¹ p) nos nós da grade (ou de `fatia`)."""
    Mi = np.linalg.inv(np.asarray(M, float))
    Pp = pele.P if fatia is None else pele.P[fatia]
    forma = Pp.shape[:3]
    q = Pp.reshape(-1, 3) @ Mi[:3, :3].T.astype(np.float32) + Mi[:3, 3].astype(np.float32)
    idx = [(q[:, i] - pele.eixos[i][0]) / pele.h for i in range(3)]
    return ndimage.map_coordinates(campo, idx, order=1, mode="nearest").reshape(forma)


def zona_varrida(pele: PeleGrade, campo, centro, pans, tilts, caixa_lo, caixa_hi, chave=None):
    """Mínimo do campo da cabeça sobre todas as poses pan (em Z) x tilt (em X) em torno de `centro`: < 0 onde a
    cabeça passa em alguma pose. Fora da caixa devolve +99 (não foi calculado)."""
    def calc():
        sl = tuple(slice(max(int(np.searchsorted(pele.eixos[i], caixa_lo[i])) - 1, 0),
                         min(int(np.searchsorted(pele.eixos[i], caixa_hi[i])) + 1, len(pele.eixos[i]))) for i in range(3))
        S = np.full(pele.F.shape, 99.0, np.float32)
        sub = None
        for a in pans:
            for t in tilts:
                M = mat_giro(centro, (0, 0, 1), a) @ mat_giro(centro, (1, 0, 0), t)
                v = reamostrar(pele, campo, M, sl)
                sub = v if sub is None else np.minimum(sub, v)
        S[sl] = sub
        return S

    if chave is None:
        return calc()
    return _cache(f"varrida|{chave}|{pele.F.shape}|{list(pans)}|{list(tilts)}|{list(caixa_lo)}|{list(caixa_hi)}|{float(np.abs(campo).sum()):.3f}", calc)


def normal(pele: PeleGrade, p, e=1.0):
    """Normal para fora da pele num ponto (gradiente do campo por diferenças centrais)."""
    p = np.asarray(p, np.float32)
    g = [float(pele.f_pontos(np.array([p + d]))[0] - pele.f_pontos(np.array([p - d]))[0]) for d in np.eye(3, dtype=np.float32) * e]
    g = np.array(g)
    return g / (np.linalg.norm(g) + 1e-9)


def sobra(pele: PeleGrade, solido: Manifold, margem=0.0):
    """Quanto um sólido sai da pele: maior valor do campo nos vértices (negativo = dentro; compare com -parede-folga).
    Devolve (valor, ponto)."""
    v, f = para_numpy(solido)
    pts = np.vstack([v, v[f].mean(axis=1)])
    val = pele.f_pontos(pts.astype(np.float32)) + margem
    i = int(np.argmax(val))
    return float(val[i]), pts[i]


# ---------------------------------------------------------------- seções
def contorno_secao(pele: PeleGrade, z, nivel=0.0, simplificar=0.3):
    """Seção horizontal da pele em z, no nível `nivel` do campo (negativo = recuada para dentro): polígono shapely."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    xs, ys, zs = pele.eixos
    k = int(np.argmin(np.abs(zs - z)))
    pols = []
    for c in measure.find_contours(pele.F[:, :, k], nivel):
        if len(c) < 4:
            continue
        pg = Polygon(np.c_[xs[0] + c[:, 0] * pele.h, ys[0] + c[:, 1] * pele.h]).buffer(0)
        if pg.area > 20:
            pols.append(pg)
    return unary_union(pols).simplify(simplificar)


def maior_poligono(g):
    return max(g.geoms, key=lambda q: q.area) if hasattr(g, "geoms") else g


def prisma_poligono(pol, z0, z1) -> Manifold:
    """Prisma vertical de um polígono shapely (sem furos) ou de vários."""
    ps = pol.geoms if hasattr(pol, "geoms") else [pol]
    return uniao(*[prisma(list(g.exterior.coords)[:-1], "z", z0, z1) for g in ps if g.area > 1])


# ---------------------------------------------------------------- peças recortadas da pele
def fatia_z(m: Manifold, z0, z1) -> Manifold:
    return m ^ caixa(-500, 500, -500, 500, z0, z1)


def meio_espaco(p0, n, lado=600.0) -> Manifold:
    """Meio-espaço {q: n·(q - p0) >= 0} como caixa grande (para interseção)."""
    from cad.comum.geo import _mat_z_para

    cx = Manifold.cube([lado, lado, lado], True).translate([0, 0, lado / 2])
    return cx.transform(_mat_z_para(n, p0))


def relevo(ext: Manifold, regiao: Manifold, p0, n, folga=0.25):
    """Peça colorida em RELEVO recortada da própria pele: tudo o que a pele tem dentro de `regiao` além do plano
    (p0, n). A base é plana (imprime com ela na mesa, sem suporte). Devolve (peça, corte): `corte` é o que se tira do
    campo/da casca do corpo (a região além do plano, com folga) para o corpo ficar com um assento plano."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    p0 = np.asarray(p0, float)
    peca = ext ^ regiao ^ meio_espaco(p0, n)
    corte = regiao ^ meio_espaco(p0 - n * folga, n)
    return peca, corte


def campo_meio_espaco(P, p0, n):
    """Distância com sinal ao plano (positiva do lado de n)."""
    n = np.asarray(n, np.float32)
    n = n / np.linalg.norm(n)
    return (P - np.asarray(p0, np.float32)) @ n


def mat_imprimir_base(n):
    """Rotação montagem -> mesa que põe o plano de normal n (a base da peça fica do lado -n) virado para baixo."""
    from cad.comum.geo import _mat_z_para

    R = _mat_z_para(n, (0, 0, 0))[:, :3]      # leva +Z para n
    M = np.eye(4)
    M[:3, :3] = R.T                            # leva n para +Z: a base (lado -n) fica na mesa
    return M
