#!/usr/bin/env python3
"""Converte a malha crua de image-to-3D (referencia/malhas/*.glb, FORA do git) na PELE PROCESSADA do repo:
uma grade de distância com sinal (mm; negativa dentro), já escalada, orientada e simétrica, em comum/cad/peles/<bicho>.npz.

O build (comum/cad/gerar.py) lê só o .npz, por `cad.comum.geo.PeleGrade.de_arquivo()`: não precisa da malha crua.

Uso (venv do repo):
  .venv/bin/python comum/cad/pele_malha.py capivara referencia/malhas/capivara-hy2mv-flb-s2.glb --altura 300
  .venv/bin/python comum/cad/pele_malha.py dino referencia/malhas/dino-hy2mv-fl-s2.glb --altura 300 [--sem-simetria]
  .venv/bin/python comum/cad/pele_malha.py capivara --cortes .preview/e3a/cortes.png      # só desenha cortes da pele gravada

O que faz:
  1. lê o GLB (eixos do Hunyuan3D: Y para cima, +Z frente) e leva para os eixos do projeto (X lados, +Y frente,
     Z cima), chão em Z=0, centro da caixa em X=0 e Y=0, altura = --altura (mm);
  2. fatia a malha (Manifold.slice) camada a camada na grade de passo --passo (1,25 mm) → dentro/fora;
  3. distância REAL até a superfície numa faixa de ±12 mm (árvore k-d nos vértices, centros e meios de aresta);
  4. simetria em X (média do campo com o espelho), suavização leve (tira a textura de degrau do gerador);
  5. grava int8 (0,1 mm por unidade, faixa ±12,7 mm) compactado: ~2–3 MB.
A posição do bicho em relação ao eixo das rodas (deslocamento em Y) NÃO é gravada: é parâmetro do modelo
(`PeleGrade.de_arquivo(caminho, dy=...)`).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # comum/ = raiz de import do pacote `cad`
from cad.caminhos import DIR_PELES, RAIZ  # noqa: E402,F401
ESCALA_INT8 = 0.1      # mm por unidade
FAIXA = 12.0           # mm de distância real guardada em volta da superfície


def converter(nome: str, glb: Path, altura: float, passo: float, simetria: bool, suave: float, cima="+y", frente="+z"):
    import trimesh
    from manifold3d import Manifold, Mesh
    from PIL import Image, ImageDraw
    from scipy import ndimage
    from scipy.spatial import cKDTree

    tm = trimesh.load(glb, force="mesh", process=True)
    if not tm.is_watertight:
        raise SystemExit("a malha não é fechada")
    v = np.asarray(tm.vertices, float)
    eixo = {"x": 0, "y": 1, "z": 2}
    ic, sc = eixo[cima[1]], (1 if cima[0] == "+" else -1)
    ifr, sf = eixo[frente[1]], (1 if frente[0] == "+" else -1)
    il = 3 - ic - ifr
    v2 = np.stack([v[:, il], sf * v[:, ifr], sc * v[:, ic]], axis=1)
    f = np.asarray(tm.faces)
    if np.linalg.det(np.eye(3)[[il, ifr, ic]] * np.array([[1], [sf], [sc]])) < 0:   # mudança de eixos espelhou: inverte as faces
        f = f[:, ::-1]
    lo, hi = v2.min(0), v2.max(0)
    esc = altura / (hi[2] - lo[2])
    v2 = (v2 - [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]]) * esc
    f = np.ascontiguousarray(f)
    man = Manifold(Mesh(vert_properties=v2.astype(np.float32), tri_verts=f.astype(np.uint32)))
    if man.status().name != "NoError":
        raise SystemExit(f"malha não vira sólido: {man.status()}")
    if man.volume() < 0:
        f = np.ascontiguousarray(f[:, ::-1])
        man = Manifold(Mesh(vert_properties=v2.astype(np.float32), tri_verts=f.astype(np.uint32)))
    lo, hi = v2.min(0), v2.max(0)
    print(f"malha: {len(f)} faces, {hi[0] - lo[0]:.1f} x {hi[1] - lo[1]:.1f} x {hi[2] - lo[2]:.1f} mm, volume {man.volume() / 1000:.0f} cm³")

    # grade simétrica em X (x=0 cai num nó), com margem
    mg = FAIXA + 2 * passo
    nx = int(np.ceil((max(-lo[0], hi[0]) + mg) / passo))
    xs = (np.arange(-nx, nx + 1) * passo).astype(np.float32)
    ys = np.arange(lo[1] - mg, hi[1] + mg + passo, passo, dtype=np.float32)
    zs = np.arange(-mg, hi[2] + mg + passo, passo, dtype=np.float32)
    dentro = np.zeros((len(xs), len(ys), len(zs)), bool)
    for k, z in enumerate(zs):
        if z <= lo[2] or z >= hi[2]:
            continue
        cs = man.slice(float(z))
        if cs.is_empty():
            continue
        im = Image.new("1", (len(xs), len(ys)), 0)
        dr = ImageDraw.Draw(im)
        polys = cs.to_polygons()
        # contornos externos (área > 0) pintam, furos (área < 0) apagam; do maior para o menor
        ars = [0.5 * float(np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1])) for p in polys]
        for i in np.argsort([-abs(a) for a in ars]):
            p = polys[i]
            px = (p[:, 0] - xs[0]) / passo
            py = (p[:, 1] - ys[0]) / passo
            dr.polygon(list(zip(px.tolist(), py.tolist())), fill=1 if ars[i] > 0 else 0)
        dentro[:, :, k] = np.asarray(im, bool).T
    aprox = (ndimage.distance_transform_edt(~dentro) - ndimage.distance_transform_edt(dentro)) * passo
    tri = v2[f]
    pts = np.vstack([v2, tri.mean(axis=1), (tri[:, 0] + tri[:, 1]) / 2, (tri[:, 1] + tri[:, 2]) / 2, (tri[:, 2] + tri[:, 0]) / 2])
    arv = cKDTree(pts)
    sel = np.abs(aprox) < FAIXA + 2 * passo
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    d, _ = arv.query(np.stack([X[sel], Y[sel], Z[sel]], axis=1), workers=-1)
    D = aprox.astype(np.float32)
    D[sel] = np.where(dentro[sel], -d, d)
    if simetria:
        D = 0.5 * (D + D[::-1])
    if suave > 0:
        D = ndimage.gaussian_filter(D, suave / passo)
    D = np.clip(D, -FAIXA - 0.7, FAIXA + 0.7)
    q = np.round(D / ESCALA_INT8).astype(np.int8)
    DIR_PELES.mkdir(exist_ok=True)
    arq = DIR_PELES / f"{nome}.npz"
    np.savez_compressed(arq, d=q, origem=np.array([xs[0], ys[0], zs[0]], np.float32), passo=np.float32(passo),
                        escala=np.float32(ESCALA_INT8), altura=np.float32(altura), fonte=str(glb.name), simetria=bool(simetria))
    print(f"gravado {arq} ({arq.stat().st_size / 1e6:.2f} MB), grade {D.shape}, passo {passo} mm")
    return arq


def cortes(nome: str, saida: Path, dy=0.0):
    """Desenha cortes da pele gravada (para conferir e para planejar o esqueleto): silhuetas de lado e de frente,
    corte no plano de simetria e cortes horizontais."""
    from PIL import Image, ImageDraw
    from cad.comum.geo import PeleGrade

    p = PeleGrade.de_arquivo(DIR_PELES / f"{nome}.npz", dy=dy)
    F = p.F
    xs, ys, zs = p.eixos
    esc = 2.0   # px por mm

    def img(masc, ex, ey, titulo):
        w, h = int((ex[-1] - ex[0]) * esc), int((ey[-1] - ey[0]) * esc)
        im = Image.fromarray((~masc.T[::-1]).astype(np.uint8) * 255).resize((w, h)).convert("RGB")
        d = ImageDraw.Draw(im)
        for t in np.arange(np.ceil(ex[0] / 50) * 50, ex[-1], 50):
            xx = (t - ex[0]) * esc
            d.line([(xx, 0), (xx, h)], fill=(200, 60, 60) if t == 0 else (160, 190, 255))
            d.text((xx + 2, 2), f"{t:.0f}", fill=(0, 0, 160))
        for t in np.arange(np.ceil(ey[0] / 50) * 50, ey[-1], 50):
            yy = h - (t - ey[0]) * esc
            d.line([(0, yy), (w, yy)], fill=(200, 60, 60) if t == 0 else (160, 190, 255))
            d.text((2, yy + 2), f"{t:.0f}", fill=(0, 0, 160))
        d.text((w // 2 - 60, h - 14), titulo, fill=(0, 0, 0))
        return im

    ix0 = int(np.argmin(np.abs(xs)))
    ims = [img((F < 0).any(axis=0), ys, zs, "silhueta de lado (y, z)"), img((F < 0).any(axis=1), xs, zs, "silhueta de frente (x, z)"),
           img(F[ix0] < 0, ys, zs, "corte x=0 (y, z)")]
    for z in (33, 70, 100, 130, 150, 200):
        ims.append(img(F[:, :, int(np.argmin(np.abs(zs - z)))] < 0, xs, ys, f"corte z={z} (x, y)"))
    W = sum(i.size[0] for i in ims[:3]) + 20
    H = max(i.size[1] for i in ims[:3]) + max(i.size[1] for i in ims[3:]) * 2 + 30
    g = Image.new("RGB", (max(W, sum(i.size[0] for i in ims[3:6]) + 20), H), "white")
    x = 0
    for i in ims[:3]:
        g.paste(i, (x, 0))
        x += i.size[0] + 10
    y = max(i.size[1] for i in ims[:3]) + 10
    for linha in (ims[3:6], ims[6:9]):
        x = 0
        for i in linha:
            g.paste(i, (x, y))
            x += i.size[0] + 10
        y += max(i.size[1] for i in linha) + 10
    saida.parent.mkdir(parents=True, exist_ok=True)
    g.save(saida)
    print("ok", saida)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("glb", nargs="?")
    ap.add_argument("--altura", type=float, default=300.0)
    ap.add_argument("--passo", type=float, default=1.25)
    ap.add_argument("--suave", type=float, default=0.8, help="sigma da suavização em mm (0 desliga)")
    ap.add_argument("--sem-simetria", action="store_true")
    ap.add_argument("--cima", default="+y")
    ap.add_argument("--frente", default="+z")
    ap.add_argument("--cortes")
    ap.add_argument("--dy", type=float, default=0.0)
    a = ap.parse_args()
    if a.glb:
        converter(a.nome, Path(a.glb), a.altura, a.passo, not a.sem_simetria, a.suave, a.cima, a.frente)
    if a.cortes:
        cortes(a.nome, Path(a.cortes), a.dy)
