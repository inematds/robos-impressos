#!/usr/bin/env python3
"""Imprimibilidade (FDM) de uma peça, medida no STL JÁ na orientação de impressão (Z para cima, mesa em Z=0).

Responde: esta peça imprime SEM suporte? Quanto de área fica sem apoio, e ONDE?

Uso:
  .venv/bin/python cad/comum/imprimibilidade.py --autoteste           # sólidos de gabarito (resposta conhecida)
  .venv/bin/python cad/comum/imprimibilidade.py dino                  # tabela de todas as peças do modelo
  .venv/bin/python cad/comum/imprimibilidade.py dino cranio           # uma peça só, com a lista de regiões
  .venv/bin/python cad/comum/imprimibilidade.py caminho/peca.stl      # STL avulso (já na orientação de impressão)
      --girar x,180        gira a peça antes (experimentar outra orientação); reassenta em Z=0
      --mapa [PASTA]       grava o mapa de balanços: <peça>.ply (cor por face) + <peça>.png (Blender, pela fila-vaga)
      --md ARQUIVO         grava o diagnóstico em markdown (tabela por peça + onde está o problema)
      --json               despeja os números em JSON

Como o cálculo funciona (tudo em mm, limites em cad/parametros.py › IMPRESSAO_LIMITES):

1. BALANÇO = face virada para baixo cujo ângulo com a VERTICAL passa de `angulo_max` (45°; parede vertical = 0°,
   teto horizontal = 90°). Há 1° de tolerância (`tol_angulo`) para um chanfro de 45° exato não ser acusado por
   arredondamento do STL (float32).
2. MESA = face virada para baixo com os 3 vértices em |z| < `z_mesa` (0,3 mm): é a 1ª camada, não é balanço.
3. As faces em balanço são agrupadas em REGIÕES (faces vizinhas por aresta). Região com menos de `fragmento_mm2`
   (4 mm² ≈ um quadrado de 2 x 2 mm, 5 filetes de 0,42) é FRAGMENTO: o próprio filete atravessa, não conta.
4. Em cada região, a borda é classificada aresta por aresta:
     APOIO  = do outro lado da aresta a superfície DESCE (parede, arco) ou é a mesa: a camada nasce em cima de
              material já impresso;
     LIVRE  = do outro lado a superfície sobe ou segue de lado (ponta do balanço).
   A região é amostrada por área (subdivisão determinística dos triângulos, sem sorteio) e, de cada amostra, saem
   raios horizontais em 12 direções + os 2 eixos principais da região. Para cada amostra:
     vão    = menor corda que termina em APOIO nas DUAS pontas (se existir);
     fundo  = distância até a aresta de apoio mais próxima.
5. Classe de cada amostra (a área é somada pelo peso da amostra):
     furo         vão ≤ `furo_max` (6 mm): teto de furo horizontal até ~Ø8 mm, rasgo estreito → imprime sem suporte;
     beira        fundo ≤ `balanco_curto` (1 mm ≈ 2 filetes): a borda do balanço ainda se apoia no vizinho;
     ponte        região PLANA (horizontal), apoiada nas duas pontas, vão ≤ `ponte_max` (20 mm) → imprime;
     ponte longa  idem com vão > `ponte_max`                                   → SEM APOIO
     teto         região curva/inclinada apoiada dos dois lados, vão > 6 mm (cúpula, arco, furo grande) → SEM APOIO
     balanço livre  sem apoio nas duas pontas em nenhuma direção (aba, prateleira, rampa > 45°)        → SEM APOIO
   "Plana" é decidido pela MAIORIA da área da região (um filete na ponta de uma ponte não a transforma em teto).
6. INÍCIO NO AR: o ângulo sozinho não vê uma ponta de paredes íngremes que nasce no ar (cone de bico para baixo).
   Mínimos locais de Z acima da mesa, com normal para baixo e saliência ≥ `inicio_no_ar_mm`, são contados à parte.
7. VEREDITO: precisa de suporte se  área sem apoio > max(`area_max_mm2`, `area_max_pct` % da área total)
   ou se houver início no ar. Peça declarada "não" em `Peca.suporte` que precisa de suporte = REPROVADA.

Limitações conhecidas: é geometria, não fatiador (não vê refrigeração, material, velocidade); regiões são
projetadas no plano XY (teto muito dobrado sobre si mesmo é raro, mas mediria errado); a "saliência" do início no ar
é medida ao longo da superfície.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
if __name__ == "__main__" and sys.path and Path(sys.path[0] or ".").resolve() == Path(__file__).resolve().parent:
    sys.path.pop(0)                       # rodando como script: cad/comum não deve virar raiz de import
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import time  # noqa: E402
from types import SimpleNamespace as NS  # noqa: E402

import numpy as np  # noqa: E402
import trimesh  # noqa: E402
from scipy.sparse import coo_matrix  # noqa: E402
from scipy.sparse.csgraph import connected_components  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

from cad import parametros as P  # noqa: E402

# Valores de reserva (os que valem ficam em cad/parametros.py › IMPRESSAO_LIMITES, com a justificativa).
_PADRAO = dict(angulo_max=45.0, tol_angulo=1.0, z_mesa=0.3, ponte_max=20.0, furo_max=6.0, balanco_curto=1.0,
               fragmento_mm2=4.0, area_max_mm2=30.0, area_max_pct=0.2, inicio_no_ar_mm=0.6)

NORMAL, MESA, FRAG, FURO, PONTE, BEIRA, PONTE_LONGA, BALANCO, TETO = range(9)
SEM_APOIO = (PONTE_LONGA, BALANCO, TETO)
NOME_CLASSE = {NORMAL: "normal", MESA: "mesa", FRAG: "fragmento", FURO: "furo", PONTE: "ponte", BEIRA: "beira",
               PONTE_LONGA: "ponte longa", BALANCO: "balanço livre", TETO: "teto"}
# cores do mapa de balanços: vermelho = sem apoio; amarelo = balanço tolerado (furo, ponte curta, beira, fragmento);
# azul = face na mesa; cinza = resto
COR = {NORMAL: (176, 178, 186), MESA: (60, 110, 215), FRAG: (245, 205, 40), FURO: (245, 205, 40),
       PONTE: (245, 205, 40), BEIRA: (245, 205, 40), PONTE_LONGA: (225, 30, 30), BALANCO: (225, 30, 30),
       TETO: (225, 30, 30)}

PASSO_AMOSTRA = 2.0     # mm: lado alvo da subdivisão dos triângulos grandes
N_SUB_MAX = 24          # subdivisão máxima por aresta de um triângulo
N_AMOSTRAS_MAX = 2500   # por região
N_DIRECOES = 12         # raios de 15 em 15 graus
COS_PLANO = math.cos(math.radians(10.0))   # face "plana" = até 10° da horizontal


def limites() -> NS:
    """Limites em vigor: cad/parametros.py › IMPRESSAO_LIMITES por cima dos valores de reserva."""
    d = dict(_PADRAO)
    d.update(vars(getattr(P, "IMPRESSAO_LIMITES", NS())))
    return NS(**d)


# ---------------------------------------------------------------------------------------------- geometria auxiliar
_BARY = {}


def _bary(k: int) -> np.ndarray:
    """Baricêntricas dos centros dos k² triângulos iguais em que um triângulo é dividido."""
    if k not in _BARY:
        pts = []
        for i in range(k):
            for j in range(k - i):
                pts.append(((i + 1 / 3) / k, (j + 1 / 3) / k))
                if i + j <= k - 2:
                    pts.append(((i + 2 / 3) / k, (j + 2 / 3) / k))
        uv = np.array(pts, float)
        _BARY[k] = np.column_stack([1 - uv.sum(axis=1), uv[:, 0], uv[:, 1]])
    return _BARY[k]


def _amostrar(tri: np.ndarray, area: np.ndarray, nz: np.ndarray):
    """tri (n,3,3) → pontos (m,3), pesos (m,) em mm², nz (m,). Determinístico; no máximo N_AMOSTRAS_MAX."""
    lados = np.linalg.norm(tri - np.roll(tri, 1, axis=1), axis=2).max(axis=1)
    n = np.clip(np.ceil(lados / PASSO_AMOSTRA).astype(int), 1, N_SUB_MAX)
    pts, pesos, nzs = [], [], []
    for k in np.unique(n):
        sel = np.nonzero(n == k)[0]
        B = _bary(int(k))
        pts.append(np.einsum("bj,njd->nbd", B, tri[sel]).reshape(-1, 3))
        pesos.append(np.repeat(area[sel] / (k * k), k * k))
        nzs.append(np.repeat(nz[sel], k * k))
    pts, pesos, nzs = np.concatenate(pts), np.concatenate(pesos), np.concatenate(nzs)
    if len(pts) > N_AMOSTRAS_MAX:           # amostragem sistemática pela área acumulada (sem sorteio)
        acum = np.cumsum(pesos)
        alvo = (np.arange(N_AMOSTRAS_MAX) + 0.5) * acum[-1] / N_AMOSTRAS_MAX
        idx, cont = np.unique(np.minimum(np.searchsorted(acum, alvo), len(pts) - 1), return_counts=True)
        pts, nzs, pesos = pts[idx], nzs[idx], cont * acum[-1] / N_AMOSTRAS_MAX
    return pts, pesos, nzs


def _raios(p2, a2, b2, apoio, dirs):
    """De cada ponto p2 (S,2), raios nas direções dirs (K,2), nos dois sentidos, contra os segmentos a2-b2 (E,2).
    Devolve vão (S,) = menor corda com APOIO nas duas pontas (inf se não há)."""
    S, E = len(p2), len(a2)
    vao = np.full(S, np.inf)
    if E == 0 or S == 0:
        return vao
    e = b2 - a2
    bloco = max(1, int(2_000_000 // max(E, 1)))
    for i0 in range(0, S, bloco):
        ap = a2[None, :, :] - p2[i0:i0 + bloco, None, :]            # (s,E,2)
        for d in dirs:
            den = d[0] * e[:, 1] - d[1] * e[:, 0]                   # (E,)
            ok = np.abs(den) > 1e-12
            dens = np.where(ok, den, 1.0)
            t = (ap[:, :, 0] * e[None, :, 1] - ap[:, :, 1] * e[None, :, 0]) / dens
            s = (ap[:, :, 0] * d[1] - ap[:, :, 1] * d[0]) / dens
            val = ok[None, :] & (s >= -1e-9) & (s <= 1 + 1e-9)
            tp = np.where(val & (t > 1e-9), t, np.inf)
            tn = np.where(val & (t < -1e-9), -t, np.inf)
            ip, im = tp.argmin(axis=1), tn.argmin(axis=1)
            lin = np.arange(len(ip))
            dp, dm = tp[lin, ip], tn[lin, im]
            corda = np.where(apoio[ip] & apoio[im] & np.isfinite(dp) & np.isfinite(dm), dp + dm, np.inf)
            vao[i0:i0 + bloco] = np.minimum(vao[i0:i0 + bloco], corda)
    return vao


def _dist_segmentos(p2, a2, b2):
    """Distância de cada ponto (S,2) ao segmento mais próximo (E,2); inf se não há segmentos."""
    if len(a2) == 0:
        return np.full(len(p2), np.inf)
    e = b2 - a2
    l2 = np.maximum((e * e).sum(axis=1), 1e-18)
    res = np.empty(len(p2))
    bloco = max(1, int(2_000_000 // len(a2)))
    for i0 in range(0, len(p2), bloco):
        ap = p2[i0:i0 + bloco, None, :] - a2[None, :, :]
        u = np.clip((ap * e[None]).sum(axis=2) / l2[None], 0.0, 1.0)
        d = ap - u[:, :, None] * e[None]
        res[i0:i0 + bloco] = np.sqrt((d * d).sum(axis=2)).min(axis=1)
    return res


def _inicios_no_ar(tm: trimesh.Trimesh, lim: NS):
    """Pontos onde o material NASCE no ar: mínimos locais de Z acima da mesa, com a normal para baixo e saliência
    (quanto se sobe pela superfície até encontrar material que vem de mais baixo) ≥ lim.inicio_no_ar_mm."""
    V = np.asarray(tm.vertices)
    z = V[:, 2]
    ar = np.asarray(tm.edges_unique)
    if len(ar) == 0:
        return []
    zmin_viz = np.full(len(V), np.inf)
    np.minimum.at(zmin_viz, ar[:, 0], z[ar[:, 1]])
    np.minimum.at(zmin_viz, ar[:, 1], z[ar[:, 0]])
    vn = np.asarray(tm.vertex_normals)
    cand = (z <= zmin_viz + 1e-6) & (z > lim.z_mesa + 0.2) & (vn[:, 2] < -0.1)
    if not cand.any():
        return []
    viz = tm.vertex_neighbors
    ordem = np.argsort(z, kind="stable")
    pai = -np.ones(len(V), int)
    minimo = {}
    achados = []

    def acha(x):
        r = x
        while pai[r] != r:
            r = pai[r]
        while pai[x] != r:
            pai[x], x = r, pai[x]
        return r

    for v in ordem:
        v = int(v)
        pai[v] = v
        raizes = {acha(u) for u in viz[v] if pai[u] >= 0}
        if not raizes:
            minimo[v] = v
            continue
        rs = sorted(raizes, key=lambda r: (z[minimo[r]], minimo[r]))
        pai[v] = rs[0]
        for r in rs[1:]:
            m = minimo.pop(r)
            sal = float(z[v] - z[m])
            if cand[m] and sal >= lim.inicio_no_ar_mm:
                achados.append((m, sal))
            pai[r] = rs[0]
    return [{"ponto": [round(float(c), 1) for c in V[m]], "saliencia_mm": round(s, 1), "_v": int(m)} for (m, s) in achados]


# ---------------------------------------------------------------------------------------------------------- análise
def _calcular(tm: trimesh.Trimesh, lim: NS):
    """Núcleo: devolve (dados, interno). `interno` guarda máscaras e amostras para o mapa de balanços."""
    if len(tm.vertices) == 3 * len(tm.faces):           # STL sem soldar: solda (cópia) para ter vizinhança
        tm = tm.copy()
        tm.merge_vertices()
    V = np.asarray(tm.vertices, float)
    F = np.asarray(tm.faces)
    N = np.asarray(tm.face_normals, float)
    A = np.asarray(tm.area_faces, float)
    zf = V[F][:, :, 2]
    area_total = float(A.sum())
    sen_lim = math.sin(math.radians(lim.angulo_max + lim.tol_angulo))
    mesa = (zf.max(axis=1) < lim.z_mesa) & (N[:, 2] < -0.5)
    bal = (N[:, 2] < -sen_lim) & (A > 1e-9) & ~mesa

    soma = {c: 0.0 for c in NOME_CLASSE}
    soma[MESA] = float(A[mesa].sum())
    regioes, pontes_longas = [], []
    am_p, am_c = [], []                                  # amostras (posição 3D, classe) para o mapa
    maior_ponte = 0.0
    maior_balanco = 0.0
    classe_face = np.zeros(len(F), np.int8)
    classe_face[mesa] = MESA

    if bal.any():
        adj = np.asarray(tm.face_adjacency)
        ar = np.asarray(tm.face_adjacency_edges)
        nao_comum = np.asarray(tm.face_adjacency_unshared)
        convexa = np.asarray(tm.face_adjacency_convex)
        angulo = np.asarray(tm.face_adjacency_angles)
        b0, b1 = bal[adj[:, 0]], bal[adj[:, 1]]
        dentro = b0 & b1
        nf = len(F)
        g = coo_matrix((np.ones(dentro.sum(), bool), (adj[dentro, 0], adj[dentro, 1])), shape=(nf, nf))
        _, rot = connected_components(g, directed=False)
        rot = np.where(bal, rot, -1)

        # ---- borda de todas as regiões de uma vez: aresta entre face em balanço e face fora
        bd = b0 ^ b1
        f_in = np.where(b0[bd], adj[bd, 0], adj[bd, 1])
        f_out = np.where(b0[bd], adj[bd, 1], adj[bd, 0])
        va, vb = V[ar[bd, 0]], V[ar[bd, 1]]
        vc = V[np.where(b0[bd], nao_comum[bd, 1], nao_comum[bd, 0])]      # 3º vértice da face de fora
        ed = vb - va
        ed /= np.maximum(np.linalg.norm(ed, axis=1, keepdims=True), 1e-12)
        t = vc - (va + vb) / 2
        u = t - (t * ed).sum(axis=1, keepdims=True) * ed                    # para onde a face de fora se afasta da aresta
        desce = u[:, 2] < -0.2 * np.maximum(np.linalg.norm(u, axis=1), 1e-12)
        cunha = convexa[bd] & (angulo[bd] > 0.35)                           # quina convexa viva: é ponta, não parede
        apoio_bd = mesa[f_out] | (desce & ~cunha)
        rot_bd = rot[f_in]
        ordem_bd = np.argsort(rot_bd, kind="stable")
        rot_bd_o = rot_bd[ordem_bd]

        faces_bal = np.nonzero(bal)[0]
        ordem_f = np.argsort(rot[faces_bal], kind="stable")
        faces_o = faces_bal[ordem_f]
        rot_o = rot[faces_o]
        cortes = np.nonzero(np.diff(rot_o))[0] + 1
        ang_dir = np.arange(N_DIRECOES) * math.pi / N_DIRECOES
        dirs_base = np.column_stack([np.cos(ang_dir), np.sin(ang_dir)])

        for fi in np.split(faces_o, cortes):
            a_reg = float(A[fi].sum())
            r = rot[fi[0]]
            if a_reg < lim.fragmento_mm2:
                soma[FRAG] += a_reg
                classe_face[fi] = FRAG
                am_p.append(V[F[fi]].mean(axis=1))
                am_c.append(np.full(len(fi), FRAG, np.int8))
                continue
            i0, i1 = np.searchsorted(rot_bd_o, r), np.searchsorted(rot_bd_o, r, side="right")
            ib = ordem_bd[i0:i1]
            a2, b2, ap = va[ib][:, :2], vb[ib][:, :2], apoio_bd[ib]
            pts, pesos, nzs = _amostrar(V[F[fi]], A[fi], N[fi, 2])
            p2 = pts[:, :2]
            # direções: 12 fixas + eixos principais da região (ponte estreita em diagonal)
            c = p2 - np.average(p2, axis=0, weights=pesos)
            cov = (c * pesos[:, None]).T @ c
            _, vec = np.linalg.eigh(cov)
            dirs = np.vstack([dirs_base, vec.T])
            vao = _raios(p2, a2, b2, ap, dirs)
            fundo = _dist_segmentos(p2, a2[ap], b2[ap])
            frac_plana = float(pesos[nzs < -COS_PLANO].sum() / pesos.sum())
            if frac_plana >= 0.6:
                plano = np.ones(len(pts), bool)
            elif frac_plana <= 0.3:
                plano = np.zeros(len(pts), bool)
            else:
                plano = nzs < -COS_PLANO
            tem_vao = np.isfinite(vao)
            cls = np.full(len(pts), BALANCO, np.int8)
            cls[tem_vao & ~plano] = TETO
            cls[tem_vao & plano & (vao > lim.ponte_max)] = PONTE_LONGA
            cls[tem_vao & plano & (vao <= lim.ponte_max)] = PONTE
            cls[fundo <= lim.balanco_curto] = BEIRA
            cls[tem_vao & (vao <= lim.furo_max)] = FURO
            for k in np.unique(cls):
                soma[int(k)] += float(pesos[cls == k].sum())
            am_p.append(pts)
            am_c.append(cls)
            # classe por face (maioria simples pela amostra mais próxima do centro) — serve ao relatório de regiões
            classe_face[fi] = cls[cKDTree(pts).query(V[F[fi]].mean(axis=1))[1]]
            m_ponte = (cls == PONTE) | (cls == PONTE_LONGA)
            if m_ponte.any():
                maior_ponte = max(maior_ponte, float(vao[m_ponte].max()))
            m_bal = cls == BALANCO
            if m_bal.any() and np.isfinite(fundo[m_bal]).any():
                maior_balanco = max(maior_balanco, float(fundo[m_bal][np.isfinite(fundo[m_bal])].max()))
            sem = np.isin(cls, SEM_APOIO)
            if sem.any():
                a_sem = float(pesos[sem].sum())
                tipos = {k: float(pesos[cls == k].sum()) for k in SEM_APOIO}
                tipo = max(tipos, key=tipos.get)
                lo, hi = pts[sem].min(axis=0), pts[sem].max(axis=0)
                reg = {"tipo": NOME_CLASSE[tipo], "area_mm2": round(a_sem, 1),
                       "caixa": [[round(float(x), 1) for x in lo], [round(float(x), 1) for x in hi]]}
                mv = sem & tem_vao
                if mv.any():
                    reg["vao_mm"] = round(float(vao[mv].max()), 1)
                mf = sem & ~tem_vao & np.isfinite(fundo)
                if mf.any():
                    reg["fundo_mm"] = round(float(fundo[mf].max()), 1)
                if not ap.any():
                    reg["sem_ancora"] = True         # nenhuma aresta de apoio: a região inteira nasce no ar
                regioes.append(reg)
                ml = cls == PONTE_LONGA
                if ml.any() and float(pesos[ml].sum()) >= 1.0:
                    pl, ph = pts[ml].min(axis=0), pts[ml].max(axis=0)
                    pontes_longas.append({"vao_mm": round(float(vao[ml].max()), 1), "area_mm2": round(float(pesos[ml].sum()), 1),
                                          "caixa": [[round(float(x), 1) for x in pl], [round(float(x), 1) for x in ph]]})

    # ---- inícios no ar que o ângulo não pegou (ponta de paredes íngremes)
    inicios = []
    for ini in _inicios_no_ar(tm, lim):
        v = ini.pop("_v")
        faces_v = tm.vertex_faces[v]
        faces_v = faces_v[faces_v >= 0]
        if not np.isin(classe_face[faces_v], SEM_APOIO).any():
            inicios.append(ini)

    sem_apoio = sum(soma[k] for k in SEM_APOIO)
    regioes.sort(key=lambda r_: -r_["area_mm2"])
    pontes_longas.sort(key=lambda r_: -r_["vao_mm"])
    lim_area = max(lim.area_max_mm2, lim.area_max_pct / 100.0 * area_total)
    motivos = []
    if sem_apoio > lim_area:
        motivos.append(f"{sem_apoio:.0f} mm² sem apoio (limite {lim_area:.0f})")
    if inicios:
        motivos.append(f"{len(inicios)} ponto(s) que nascem no ar")
    dados = {
        "area_total_mm2": round(area_total, 1),
        "mesa_mm2": round(soma[MESA], 1),
        "balanco_bruto_mm2": round(float(A[bal].sum()), 1),          # tudo o que passa de 45° fora da mesa
        "sem_apoio_mm2": round(sem_apoio, 1),
        "sem_apoio_pct": round(100.0 * sem_apoio / area_total, 2) if area_total else 0.0,
        "limite_mm2": round(lim_area, 1),
        "tolerado_mm2": {"fragmentos": round(soma[FRAG], 1), "furos": round(soma[FURO], 1),
                         "pontes": round(soma[PONTE], 1), "beiras": round(soma[BEIRA], 1)},
        "por_tipo_mm2": {NOME_CLASSE[k]: round(soma[k], 1) for k in SEM_APOIO},
        "maior_ponte_mm": round(maior_ponte, 1),
        "maior_balanco_mm": round(maior_balanco, 1),
        "pontes_longas": pontes_longas[:8],
        "inicios_no_ar": inicios[:8],
        "n_inicios_no_ar": len(inicios),
        "n_regioes": len(regioes),
        "regioes": regioes[:8],
        "precisa_suporte": bool(motivos),
        "motivos": motivos,
    }
    interno = NS(tm=tm, bal=bal, mesa=mesa,
                 am_p=np.concatenate(am_p) if am_p else np.zeros((0, 3)),
                 am_c=np.concatenate(am_c) if am_c else np.zeros(0, np.int8))
    return dados, interno


def analisar(tm: trimesh.Trimesh, lim: NS | None = None) -> dict:
    """Números de imprimibilidade de UMA peça (malha na orientação de impressão, mesa em Z=0)."""
    return _calcular(tm, lim or limites())[0]


def girar(tm: trimesh.Trimesh, eixo: str, graus: float) -> trimesh.Trimesh:
    """Cópia da peça girada em torno de X, Y ou Z e REASSENTADA na mesa (Z mínimo = 0, centrada em XY)."""
    e = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[eixo.lower()]
    g = tm.copy()
    g.apply_transform(trimesh.transformations.rotation_matrix(math.radians(graus), e))
    lo, hi = g.bounds
    g.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
    return g


def declarada_sem_suporte(suporte: str) -> bool:
    return str(suporte).strip().lower().startswith(("não", "nao"))


def veredito(dados: dict, suporte: str) -> str:
    if declarada_sem_suporte(suporte):
        return "REPROVADA" if dados["precisa_suporte"] else "ok sem suporte"
    return "precisa de suporte (declarado)" if dados["precisa_suporte"] else "ok (declarou suporte; o cálculo não vê necessidade)"


def onde(dados: dict, n: int = 3) -> str:
    """Texto curto: onde está a área sem apoio (caixas na orientação de impressão)."""
    partes = []
    for r in dados["regioes"][:n]:
        (x0, y0, z0), (x1, y1, z1) = r["caixa"]
        extra = f", vão {r['vao_mm']:.0f}" if "vao_mm" in r else (f", fundo {r['fundo_mm']:.0f}" if "fundo_mm" in r else "")
        if r.get("sem_ancora"):
            extra += ", nasce no ar"
        partes.append(f"{r['tipo']} {r['area_mm2']:.0f} mm² em x {x0:.0f}..{x1:.0f}, y {y0:.0f}..{y1:.0f}, z {z0:.0f}..{z1:.0f}{extra}")
    if dados["n_regioes"] > n:
        partes.append(f"+{dados['n_regioes'] - n} regiões")
    for i in dados["inicios_no_ar"][:2]:
        partes.append(f"nasce no ar em {tuple(i['ponto'])} (saliência {i['saliencia_mm']} mm)")
    return "; ".join(partes)


def caixa_na_montagem(caixa, matriz) -> list:
    """Caixa (orientação de impressão) → caixa envolvente na posição de MONTAGEM (matriz = para_montagem[0])."""
    (x0, y0, z0), (x1, y1, z1) = caixa
    cantos = np.array([[x, y, z, 1.0] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)])
    q = (np.asarray(matriz, float) @ cantos.T).T[:, :3]
    return [[round(float(v), 1) for v in q.min(axis=0)], [round(float(v), 1) for v in q.max(axis=0)]]


# ------------------------------------------------------------------------------------------------- mapa de balanços
def exportar_mapa(tm: trimesh.Trimesh, caminho, lim: NS | None = None) -> dict:
    """Grava a malha com COR POR FACE (PLY; .glb também funciona): vermelho = sem apoio, amarelo = balanço
    tolerado (furo, ponte curta, beira, fragmento), azul = na mesa, cinza = resto. Devolve os números da peça.
    Faces grandes em balanço são subdivididas (3 mm) para a cor acompanhar a classe de cada trecho."""
    dados, it = _calcular(tm, lim or limites())
    tm = it.tm
    V, F = np.asarray(tm.vertices, float), np.asarray(tm.faces)
    cor = np.zeros((len(F), 3), np.uint8)
    cor[:] = COR[NORMAL]
    cor[it.mesa] = COR[MESA]
    fora = ~it.bal
    tri = [V[F[fora]]]
    cores = [cor[fora]]
    if it.bal.any():
        vb, fb = trimesh.remesh.subdivide_to_size(V, F[it.bal], max_edge=3.0, max_iter=12)
        tb = vb[fb]
        cls = it.am_c[cKDTree(it.am_p).query(tb.mean(axis=1))[1]]
        tri.append(tb)
        cores.append(np.array([COR[int(k)] for k in cls], np.uint8))
    tri = np.concatenate(tri)
    cores = np.concatenate(cores)
    m = trimesh.Trimesh(vertices=tri.reshape(-1, 3), faces=np.arange(len(tri) * 3).reshape(-1, 3), process=False)
    rgba = np.column_stack([cores, np.full(len(cores), 255, np.uint8)])
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if caminho.suffix.lower() == ".ply":                 # cor por vértice com vértices não compartilhados = cor por face
        m.visual.vertex_colors = np.repeat(rgba, 3, axis=0)
    else:
        m.visual.face_colors = rgba
    m.export(caminho)
    return dados


def render_mapa(ply, png, titulo: str = "", linhas: list | None = None, res: int = 620, amostras: int = 24) -> bool:
    """Renderiza o PLY do mapa em 3 vistas (2 por BAIXO, onde estão as faces sem apoio, + 1 por cima) e monta um PNG
    com título e legenda. Usa o Blender pela fila de render (~/projetos/wifi/scripts/fila-vaga), se ela existir."""
    from PIL import Image, ImageDraw, ImageFont

    ply, png = Path(ply), Path(png)
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "v"
        cmd = ["blender", "-b", "--python", str(RAIZ / "cad" / "render_balancos.py"), "--", str(ply), str(base),
               "--vistas", "35,-45;215,-45;35,28", "--res", f"{res}x{res}", "--amostras", str(amostras)]
        fila = Path.home() / "projetos/wifi/scripts/fila-vaga"
        if fila.exists() and os.access(fila, os.X_OK):
            cmd = [str(fila), "render", "robos-balancos", "--"] + cmd
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        except (OSError, subprocess.TimeoutExpired) as ex:
            print("render do mapa falhou:", ex)
            return False
        vistas = sorted(Path(tmp).glob("v-*.png"))
        if r.returncode != 0 or len(vistas) < 3:
            print("render do mapa falhou:", (r.stdout + r.stderr)[-600:])
            return False
        ims = [Image.open(v).convert("RGB") for v in vistas]

        def fonte(t):
            for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
                if Path(f).exists():
                    return ImageFont.truetype(f, t)
            return ImageFont.load_default()

        linhas = linhas or []
        topo = 46 + 22 * len(linhas)
        pe = 40
        W = res * 3
        folha = Image.new("RGB", (W, topo + res + pe), "white")
        d = ImageDraw.Draw(folha)
        d.text((14, 8), titulo, fill=(20, 20, 24), font=fonte(26))
        for i, l in enumerate(linhas):
            d.text((14, 42 + 22 * i), l, fill=(60, 60, 66), font=fonte(16))
        rot = ["visto por BAIXO (frente/direita)", "visto por BAIXO (trás/esquerda)", "visto por cima (como sai da mesa)"]
        for i, im in enumerate(ims):
            folha.paste(im, (i * res, topo))
            d.text((i * res + 10, topo + 6), rot[i], fill=(60, 60, 66), font=fonte(15))
        x = 14
        for (c, txt) in ((COR[BALANCO], "sem apoio (balanço livre, teto, ponte longa)"), (COR[PONTE], "balanço tolerado (furo, ponte curta, beira)"),
                         (COR[MESA], "face na mesa"), (COR[NORMAL], "sem balanço")):
            d.rectangle([x, topo + res + 10, x + 20, topo + res + 30], fill=c, outline=(40, 40, 40))
            d.text((x + 28, topo + res + 11), txt, fill=(40, 40, 44), font=fonte(16))
            x += 60 + int(d.textlength(txt, font=fonte(16)))
        png.parent.mkdir(parents=True, exist_ok=True)
        folha.save(png)
    return True


# ------------------------------------------------------------------------------------- uso pelo verificador (teste 10)
def _carrega(caminho: Path) -> trimesh.Trimesh:
    """Lê o STL soldando os vértices. Tenta 2 vezes (outra etapa pode estar regravando o arquivo)."""
    erro = None
    for _ in range(2):
        try:
            tm = trimesh.load(caminho, process=True)
            if len(tm.faces):
                return tm
            erro = "malha vazia"
        except Exception as ex:                            # noqa: BLE001
            erro = ex
        time.sleep(1.0)
    raise RuntimeError(f"não consegui ler {caminho}: {erro}")


def analisar_pecas(pecas_json: list, malhas: dict | None = None, base: Path | None = None, lim: NS | None = None) -> dict:
    """Roda a análise em todas as peças de um montagem.json. `malhas` = {nome: trimesh} já carregadas (opcional).
    Devolve {nome: dados}, com `suporte`, `veredito`, `onde` e os campos de impressão declarados na peça."""
    lim = lim or limites()
    res = {}
    for p in pecas_json:
        nome = p["nome"]
        try:
            tm = (malhas or {}).get(nome)
            if tm is None:
                tm = _carrega(Path(base) / p["arquivo"])
            d = analisar(tm, lim)
        except Exception as ex:                            # noqa: BLE001
            res[nome] = {"erro": f"{type(ex).__name__}: {ex}", "suporte": p.get("suporte", "não"), "veredito": "ERRO",
                         "precisa_suporte": True, "sem_apoio_mm2": 0.0, "sem_apoio_pct": 0.0, "maior_ponte_mm": 0.0}
            continue
        mats = p.get("para_montagem") or []
        if mats:
            for r in d["regioes"]:
                r["caixa_montagem"] = caixa_na_montagem(r["caixa"], mats[0])
        d["suporte"] = p.get("suporte", "não")
        d["veredito"] = veredito(d, d["suporte"])
        d["onde"] = onde(d)
        d["material"] = p.get("material", "")
        d["perimetros"] = p.get("perimetros", 3)
        d["infill"] = p.get("infill", 15)
        d["reforco"] = p.get("reforco", "")
        d["orientacao"] = p.get("orientacao", "")
        res[nome] = d
    return res


def teste_imprimibilidade(pecas_json: list, malhas: dict | None = None, base: Path | None = None):
    """Teste 10 do verificador. Devolve (ok, texto, dados_por_peça).
    FALHA se alguma peça declarada SEM suporte (`suporte` começa com "não") precisa de suporte pelo cálculo."""
    lim = limites()
    dados = analisar_pecas(pecas_json, malhas, base, lim)
    reprov = sorted((n for n, d in dados.items() if d["veredito"] in ("REPROVADA", "ERRO")), key=lambda n: -dados[n]["sem_apoio_mm2"])
    com_sup = sorted((n for n, d in dados.items() if not declarada_sem_suporte(d["suporte"])), key=lambda n: -dados[n]["sem_apoio_mm2"])
    sem = [n for n, d in dados.items() if d["veredito"] == "ok sem suporte"]

    def item(n):
        d = dados[n]
        if "erro" in d:
            return f"{n} (ERRO: {d['erro']})"
        extra = f", ponte de {d['maior_ponte_mm']:.0f} mm" if d["maior_ponte_mm"] > lim.ponte_max else ""
        extra += f", {d['n_inicios_no_ar']} ponto(s) no ar" if d.get("n_inicios_no_ar") else ""
        return f"{n} ({d['sem_apoio_mm2']:.0f} mm² = {d['sem_apoio_pct']:.1f} %{extra})"

    txt = (f"{len(dados)} peças distintas: {len(sem)} saem sem suporte; {len(com_sup)} com suporte declarado"
           + (": " + ", ".join(item(n) for n in com_sup) if com_sup else "")
           + f"; {len(reprov)} REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max({lim.area_max_mm2:.0f} mm², "
             f"{lim.area_max_pct} % da área) a mais de {lim.angulo_max:.0f}° ou ponto que nasce no ar)"
           + (": " + ", ".join(item(n) for n in reprov) if reprov else ""))
    return (not reprov), txt, dados


def teste_negativo(pecas_json: list, malhas: dict | None, dados: dict, base: Path | None = None):
    """Teste 11: prova que o cálculo ENXERGA. Pega a peça aprovada sem suporte com a maior face na mesa, gira de
    propósito (180° em X; se a peça for simétrica, 90° em X e depois 90° em Y) e exige que a área sem apoio passe do
    limite. Devolve (ok, texto, info)."""
    lim = limites()
    cand = sorted((n for n, d in dados.items() if d.get("veredito") == "ok sem suporte"),
                  key=lambda n: (-dados[n]["mesa_mm2"], n))
    if not cand:
        cand = sorted((n for n, d in dados.items() if "erro" not in d), key=lambda n: (dados[n]["sem_apoio_mm2"], n))
        if not cand:
            return False, "nenhuma peça analisável para girar", {}
    nome = cand[0]
    p = next(q for q in pecas_json if q["nome"] == nome)
    tm = (malhas or {}).get(nome)
    if tm is None:
        tm = _carrega(Path(base) / p["arquivo"])
    antes = dados[nome]
    tent = []
    for (eixo, graus) in (("x", 180.0), ("x", 90.0), ("y", 90.0)):
        d = analisar(girar(tm, eixo, graus), lim)
        tent.append({"giro": f"{graus:.0f}° em {eixo.upper()}", "sem_apoio_mm2": d["sem_apoio_mm2"], "sem_apoio_pct": d["sem_apoio_pct"],
                     "limite_mm2": d["limite_mm2"], "acusou": d["precisa_suporte"]})
        if d["precisa_suporte"]:
            break
    ok = tent[-1]["acusou"]
    u = tent[-1]
    txt = (f"'{nome}' na orientação declarada: {antes['sem_apoio_mm2']:.0f} mm² sem apoio (limite {antes['limite_mm2']:.0f}); girada {u['giro']} → "
           f"{u['sem_apoio_mm2']:.0f} mm² = {u['sem_apoio_pct']:.1f} % " + ("(acusou; tem que acusar)" if ok else "(NÃO acusou)")
           + (f"; giros tentados antes sem acusar: {', '.join(t['giro'] for t in tent[:-1])}" if len(tent) > 1 else ""))
    return ok, txt, {"peca": nome, "antes_mm2": antes["sem_apoio_mm2"], "tentativas": tent}


# --------------------------------------------------------------------------------------------------------- autoteste
def _via_stl(m) -> trimesh.Trimesh:
    """Manifold → STL binário (float32) → trimesh soldado, como o verificador lê do disco."""
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)
    lo = tm.bounds[0]
    tm.apply_translation([0, 0, -lo[2]])
    dados = tm.export(file_type="stl")
    return trimesh.load(io.BytesIO(dados), file_type="stl", process=True)


def _gabaritos():
    """Sólidos com resposta conhecida: (nome, malha, precisa_suporte esperado, checagem extra ou None)."""
    from manifold3d import CrossSection, Manifold

    def cx(x, y, z, pos=(0, 0, 0)):
        return Manifold.cube([x, y, z]).translate(list(pos))

    def cil_y(d, comp, pos, n=48):       # cilindro com eixo em Y
        return Manifold.cylinder(comp, d / 2, d / 2, n).rotate([-90, 0, 0]).translate(list(pos))

    def perfil_y(pts, comp, y0=0.0):     # extrusão ao longo de Y de um polígono (x, z)
        sinal = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))
        pts = pts if sinal > 0 else pts[::-1]            # CrossSection descarta polígono em sentido horário
        return CrossSection([[(x, z) for (x, z) in pts]]).extrude(comp).rotate([90, 0, 0]).translate([0, y0 + comp, 0])

    def ponte(vao, extra=None):
        s = cx(10, 20, 15) + cx(10, 20, 15, (10 + vao, 0, 0)) + cx(20 + vao, 20, 3, (0, 0, 15))
        return s + extra if extra is not None else s

    g = []
    g.append(("caixa na mesa", cx(20, 20, 10), False, None))
    t_pe = cx(10, 20, 20, (15, 0, 0)) + cx(40, 20, 4, (0, 0, 20))
    g.append(("T em pé (haste na mesa, aba de 15 mm de cada lado)", t_pe, True, lambda d: 500 < d["sem_apoio_mm2"] < 620))
    g.append(("T deitado (aba na mesa)", cx(40, 20, 4) + cx(10, 20, 20, (15, 0, 4)), False, None))
    g.append(("ponte de 10 mm", ponte(10), False, lambda d: abs(d["maior_ponte_mm"] - 10) < 0.6))
    g.append(("ponte de 30 mm", ponte(30), True, lambda d: abs(d["maior_ponte_mm"] - 30) < 1.0 and d["pontes_longas"]))
    # ponte de 16 mm com filete R3 nas duas pontas (canto entre pilar e tabuleiro)
    fil = (cx(3, 20, 3, (10, 0, 12)) - cil_y(6, 20, (13, 0, 12))) + (cx(3, 20, 3, (23, 0, 12)) - cil_y(6, 20, (23, 0, 12)))
    g.append(("ponte de 16 mm com filete R3 nas pontas", ponte(16, fil), False, None))
    # ponte de 30 mm com mão-francesa de 45° exatos de 6 mm em cada ponta → teto plano de 18 mm
    ch = perfil_y([(10, 15), (16, 15), (10, 9)], 20) + perfil_y([(40, 15), (40, 9), (34, 15)], 20)
    g.append(("ponte de 30 mm com chanfro de 45° (teto de 18 mm)", ponte(30, ch), False, lambda d: 17 < d["maior_ponte_mm"] < 19.5))
    bloco = cx(24, 10, 24)
    g.append(("furo horizontal Ø3,4", bloco - cil_y(3.4, 10, (12, 0, 12)), False, None))
    g.append(("furo horizontal Ø12", bloco - cil_y(12, 10, (12, 0, 12)), True, None))
    gota = cil_y(12, 10, (12, 0, 12)) + perfil_y([(12 - 6 * math.sin(math.pi / 4), 12 + 6 * math.cos(math.pi / 4)),
                                                 (12 + 6 * math.sin(math.pi / 4), 12 + 6 * math.cos(math.pi / 4)),
                                                 (12, 12 + 6 * math.sqrt(2))], 10)
    g.append(("furo em gota Ø12 (teto a 45°)", cx(24, 10, 26) - gota, False, lambda d: d["sem_apoio_mm2"] < 1.0))
    g.append(("chanfro de 45° exatos na borda de baixo", perfil_y([(5, 0), (25, 0), (30, 5), (30, 15), (0, 15), (0, 5)], 20), False,
              lambda d: d["balanco_bruto_mm2"] < 0.5))
    t50 = math.tan(math.radians(50))
    g.append(("rampa de 50° (5° além do limite)", perfil_y([(0, 0), (10, 0), (10 + 20 * t50, 20), (20 * t50, 20)], 20), True, None))
    g.append(("beira de 1 mm", cx(20, 20, 10) + cx(21, 20, 3, (0, 0, 10)), False, None))
    g.append(("beira de 5 mm", cx(20, 20, 10) + cx(25, 20, 3, (0, 0, 10)), True, lambda d: 60 < d["sem_apoio_mm2"] < 90))
    cup = (Manifold.sphere(30, 96) - Manifold.sphere(27.6, 96)) - cx(80, 80, 40, (-40, -40, -40))
    g.append(("cúpula R30 com a boca para baixo", cup, True, lambda d: 1100 < d["sem_apoio_mm2"] < 1400))
    cone = Manifold.cylinder(8, 0.05, 3, 32).translate([18, 10, 7])
    g.append(("ponte de 16 mm com cone de bico para baixo pendurado", ponte(16, cone), True, lambda d: d["n_inicios_no_ar"] >= 1))
    return [(n, _via_stl(m), esp, chk) for (n, m, esp, chk) in g]


def autoteste(verboso=True) -> bool:
    lim = limites()
    ok_geral = True
    for (nome, tm, esperado, chk) in _gabaritos():
        d = analisar(tm, lim)
        ok = d["precisa_suporte"] == esperado and (chk is None or bool(chk(d)))
        ok_geral &= ok
        if verboso:
            print(f"  [{'ok' if ok else 'ERRADO'}] {nome}: sem apoio {d['sem_apoio_mm2']:.1f} mm² ({d['sem_apoio_pct']:.1f} %), "
                  f"bruto {d['balanco_bruto_mm2']:.1f}, maior ponte {d['maior_ponte_mm']:.1f}, no ar {d['n_inicios_no_ar']} → "
                  f"{'precisa de suporte' if d['precisa_suporte'] else 'sem suporte'} (esperado: {'precisa' if esperado else 'sem suporte'})")
    if verboso:
        print("  => autoteste:", "TUDO CERTO" if ok_geral else "HÁ ERROS")
    return ok_geral


# ------------------------------------------------------------------------------------------------- linha de comando
def _linha_tabela(nome, d):
    if "erro" in d:
        return f"| {nome} | {d['suporte']} | – | – | – | ERRO | {d['erro']} |"
    return (f"| {nome} | {d['suporte']} | {d['sem_apoio_mm2']:.0f} | {d['sem_apoio_pct']:.1f} | "
            f"{d['maior_ponte_mm']:.0f} | {d['veredito']} | {d['onde'] or '–'} |")


def carregar_modelo(modelo: str, raiz_pecas: Path | None = None):
    base = (raiz_pecas or RAIZ / "pecas") / modelo
    mj = json.loads((base / "montagem.json").read_text())
    return base, mj


def diagnostico_md(modelos: list, saida: Path, raiz_pecas: Path | None = None) -> dict:
    """Grava a tabela de diagnóstico (peça, suporte declarado, área sem apoio, maior ponte, veredito, onde)."""
    lim = limites()
    blocos, comuns, resumo = [], {}, {}
    for m in modelos:
        base, mj = carregar_modelo(m, raiz_pecas)
        dados = analisar_pecas(mj["pecas"], None, base, lim)
        proprias = [p["nome"] for p in mj["pecas"] if not p.get("comum")]
        for p in mj["pecas"]:
            if p.get("comum"):
                comuns.setdefault(p["nome"], (dados[p["nome"]], []))[1].append(m)
        blocos.append((m, mj["titulo"], [(n, dados[n]) for n in proprias], time.strftime("%H:%M:%S")))
        resumo[m] = dados
    L = ["# Imprimibilidade — estado ANTES das correções", "",
         f"Gerado em {time.strftime('%d/%m/%Y %H:%M')} por `cad/comum/imprimibilidade.py --md` sobre os STL de `pecas/` "
         "(orientação de impressão declarada em cada peça).", "",
         f"Limites (`cad/parametros.py › IMPRESSAO_LIMITES`): balanço > {lim.angulo_max:.0f}° da vertical (+{lim.tol_angulo:.0f}° de tolerância); "
         f"mesa = |z| < {lim.z_mesa} mm; ponte plana até {lim.ponte_max:.0f} mm; teto de furo/rasgo até {lim.furo_max:.0f} mm de vão; "
         f"beira até {lim.balanco_curto:.0f} mm; região < {lim.fragmento_mm2:.0f} mm² ignorada; "
         f"**precisa de suporte se a área sem apoio > max({lim.area_max_mm2:.0f} mm², {lim.area_max_pct} % da área da peça) ou se algo nasce no ar**.", "",
         "Veredito: **REPROVADA** = declarada sem suporte, mas o cálculo diz que precisa (é a lista de trabalho); "
         "*precisa de suporte (declarado)* = coerente, mas a ordem 9 pede reduzir; *ok sem suporte* = passa.", "",
         "Coluna \"onde\": caixas em mm na ORIENTAÇÃO DE IMPRESSÃO (X, Y da mesa; Z = altura na mesa). "
         "A caixa na posição de montagem está em `pecas/<modelo>/verificacao.json › imprimibilidade › <peça> › regioes › caixa_montagem`.", ""]
    todas = []
    for (m, titulo, linhas, hora) in blocos:
        L += [f"## {m} — {titulo} (peças só deste modelo; STL lidos às {hora})", "",
              "| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |",
              "|---|---|---:|---:|---:|---|---|"]
        for (n, d) in sorted(linhas, key=lambda t: -t[1].get("sem_apoio_mm2", 0)):
            L.append(_linha_tabela(n, d))
            todas.append((f"{m}/{n}", d))
        L.append("")
    if comuns:
        L += ["## comum — peças iguais em mais de um modelo (`pecas/comum`)", "",
              "| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |",
              "|---|---|---:|---:|---:|---|---|"]
        for n, (d, ms) in sorted(comuns.items(), key=lambda t: -t[1][0].get("sem_apoio_mm2", 0)):
            L.append(_linha_tabela(f"{n} ({', '.join(ms)})", d))
            todas.append((f"comum/{n}", d))
        L.append("")
    n_ok = sum(1 for _, d in todas if d["veredito"] == "ok sem suporte")
    n_rep = sum(1 for _, d in todas if d["veredito"] in ("REPROVADA", "ERRO"))
    n_sup = sum(1 for _, d in todas if d["veredito"].startswith("precisa"))
    n_fol = len(todas) - n_ok - n_rep - n_sup
    L += ["## Resumo", "",
          f"- {len(todas)} peças distintas analisadas: **{n_ok} passam sem suporte**, **{n_rep} REPROVADAS**, "
          f"{n_sup} com suporte declarado e necessário, {n_fol} com suporte declarado sem necessidade pelo cálculo.", "",
          "### As 10 piores (área sem apoio)", "",
          "| # | peça | suporte declarado | sem apoio (mm²) | % | veredito |", "|---:|---|---|---:|---:|---|"]
    for i, (n, d) in enumerate(sorted(todas, key=lambda t: -t[1].get("sem_apoio_mm2", 0))[:10], 1):
        L.append(f"| {i} | {n} | {d['suporte']} | {d['sem_apoio_mm2']:.0f} | {d['sem_apoio_pct']:.1f} | {d['veredito']} |")
    L.append("")
    Path(saida).write_text("\n".join(L))
    return {"todas": todas, "ok": n_ok, "reprovadas": n_rep, "com_suporte": n_sup, "folga": n_fol}


def _principal(argv):
    if "--autoteste" in argv:
        return 0 if autoteste() else 1
    opc = {"--girar": None, "--mapa": None, "--md": None}
    args, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a in ("--girar", "--md"):
            opc[a] = argv[i + 1]
            i += 2
        elif a == "--mapa":
            if i + 1 < len(argv) and not argv[i + 1].startswith("--") and ("/" in argv[i + 1] or argv[i + 1].startswith(".")):
                opc[a] = argv[i + 1]
                i += 2
            else:
                opc[a] = str(RAIZ / ".preview" / "balancos")
                i += 1
        elif a.startswith("--"):
            i += 1
        else:
            args.append(a)
            i += 1
    if not args:
        print(__doc__)
        return 2
    lim = limites()
    if opc["--md"]:
        r = diagnostico_md(args, Path(opc["--md"]))
        print(f"gravado {opc['--md']}: {len(r['todas'])} peças, {r['ok']} ok sem suporte, {r['reprovadas']} reprovadas, "
              f"{r['com_suporte']} com suporte declarado e necessário, {r['folga']} com suporte declarado sem necessidade")
        return 0
    if args[0].lower().endswith(".stl"):
        itens = [(Path(args[0]).stem, _carrega(Path(args[0])), "não")]
    else:
        base, mj = carregar_modelo(args[0])
        quais = args[1:] or [p["nome"] for p in mj["pecas"]]
        itens = []
        for n in quais:
            p = next((q for q in mj["pecas"] if q["nome"] == n), None)
            if p is None:
                print(f"peça '{n}' não existe em {args[0]}; há: {', '.join(q['nome'] for q in mj['pecas'])}")
                return 2
            itens.append((f"{args[0]}-{n}", _carrega(base / p["arquivo"]), p.get("suporte", "não")))
    saida_json = {}
    detalhe = len(itens) <= 3
    if not detalhe:
        print(f"{'peça':28s} {'suporte declarado':28s} {'sem apoio mm²':>13s} {'%':>6s} {'ponte':>6s}  veredito")
    for (nome, tm, sup) in itens:
        if opc["--girar"]:
            eixo, graus = opc["--girar"].split(",")
            tm = girar(tm, eixo, float(graus))
            nome += f"-girada-{eixo}{graus}"
        if opc["--mapa"]:
            pasta = Path(opc["--mapa"])
            d = exportar_mapa(tm, pasta / f"{nome}.ply", lim)
        else:
            d = analisar(tm, lim)
        d["suporte"], d["veredito"], d["onde"] = sup, veredito(d, sup), onde(d, 6)
        saida_json[nome] = d
        if detalhe:
            print(f"== {nome}  (suporte declarado: {sup})")
            print(f"   área total {d['area_total_mm2']:.0f} mm²; na mesa {d['mesa_mm2']:.0f}; balanço bruto (> {lim.angulo_max:.0f}°) {d['balanco_bruto_mm2']:.0f}")
            print(f"   tolerado: {d['tolerado_mm2']}")
            print(f"   SEM APOIO: {d['sem_apoio_mm2']:.0f} mm² = {d['sem_apoio_pct']:.2f} % (limite {d['limite_mm2']:.0f} mm²)  por tipo: {d['por_tipo_mm2']}")
            print(f"   maior ponte {d['maior_ponte_mm']:.1f} mm; maior balanço livre {d['maior_balanco_mm']:.1f} mm; pontos que nascem no ar: {d['n_inicios_no_ar']}")
            for r in d["regioes"]:
                print(f"     região: {r}")
            for r in d["pontes_longas"]:
                print(f"     ponte longa: {r}")
            for r in d["inicios_no_ar"]:
                print(f"     nasce no ar: {r}")
            print(f"   => {d['veredito']}" + (f"  ({'; '.join(d['motivos'])})" if d["motivos"] else ""))
        else:
            print(f"{nome:28s} {sup[:28]:28s} {d['sem_apoio_mm2']:13.0f} {d['sem_apoio_pct']:6.1f} {d['maior_ponte_mm']:6.0f}  {d['veredito']}")
        if opc["--mapa"]:
            pasta = Path(opc["--mapa"])
            linhas = [f"sem apoio: {d['sem_apoio_mm2']:.0f} mm² = {d['sem_apoio_pct']:.1f} % da área (limite {d['limite_mm2']:.0f} mm²)  ·  "
                      f"maior ponte {d['maior_ponte_mm']:.0f} mm  ·  suporte declarado: {sup}  ·  {d['veredito']}"]
            ok = render_mapa(pasta / f"{nome}.ply", pasta / f"{nome}.png", f"mapa de balanços — {nome}", linhas)
            print(f"   mapa: {pasta / (nome + '.ply')}" + (f"  +  {pasta / (nome + '.png')}" if ok else "  (PNG falhou)"))
    if "--json" in argv:
        print(json.dumps(saida_json, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(_principal(sys.argv[1:]))
