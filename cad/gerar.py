#!/usr/bin/env python3
"""Gera as peças de um modelo: STL (já na orientação de impressão), 3MF, montagem.json e mesas.json.

Uso:  .venv/bin/python cad/gerar.py dino|capivara|cubo|cubo_rodas|todos

Saída (por modelo):
  pecas/<modelo>/stl/<modelo>-<peca>.stl     peças só deste modelo
  pecas/comum/stl/comum-<peca>.stl           peças iguais em mais de um modelo
  pecas/<modelo>/3mf/…                        as mesmas peças em 3MF
  pecas/<modelo>/componentes/*.stl            envelopes dos componentes comprados (não imprimir)
  pecas/<modelo>/montagem.json                onde cada peça vai (matrizes), juntas, poses, estimativas
  pecas/<modelo>/montagem.glb                 montagem completa num arquivo só
  pecas/<modelo>/mesas.json                   disposição das peças nas mesas da impressora
"""
from __future__ import annotations

import importlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import trimesh

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from cad import parametros as P  # noqa: E402
from cad.comum.geo import desbeliscar, limites, limpar, para_numpy  # noqa: E402

MODELOS = ["dino", "capivara", "cubo", "cubo_rodas"]
I = P.IMPRESSORA


def malha(m) -> trimesh.Trimesh:
    v, f = para_numpy(m)
    return trimesh.Trimesh(v, f, process=False)


def orientar(peca):
    """Devolve (sólido na orientação de impressão, matriz impressão->montagem)."""
    R = np.asarray(peca.imprimir, float)
    s = desbeliscar(limpar(peca.solido)).transform(R[:3, :])
    lo, hi = limites(s)
    T = np.eye(4)
    T[:3, 3] = [-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]]
    s = s.translate(list(T[:3, 3]))
    return s, np.linalg.inv(T @ R)


def estimar(m, peca):
    """Estimativa SEM fatiador: volume de plástico, massa e tempo."""
    V = m.volume()
    A = m.surface_area()
    if peca.macica:
        casca = min(V, A * I.casca_solida_mm)
        Vp = casca + (V - casca) * I.preenchimento
    else:
        Vp = V
    dens = {"PLA": I.dens_pla, "PETG": I.dens_petg, "TPU": I.dens_tpu}[peca.material]
    massa = Vp / 1000.0 * dens
    tempo_h = Vp / I.vazao_media_mm3_s / 3600.0 + 0.08
    return round(Vp / 1000.0, 1), round(massa, 1), round(tempo_h, 2)


def empacotar(itens, lado=250.0, vao=6.0):
    """Prateleiras simples: itens = [(chave, w, d)]. Devolve [(chave, mesa, x, y)]."""
    itens = sorted(itens, key=lambda t: -t[2])
    res, mesa, x, y, linha = [], 0, 0.0, 0.0, 0.0
    for (k, w, d) in itens:
        if x + w > lado:
            x, y, linha = 0.0, y + linha + vao, 0.0
        if y + d > lado:
            mesa, x, y, linha = mesa + 1, 0.0, 0.0, 0.0
        res.append((k, mesa, x, y))
        x += w + vao
        linha = max(linha, d)
    return res, mesa + 1


def gerar(nome: str):
    t0 = time.time()
    mod = importlib.import_module(f"cad.modelos.{nome}").construir()
    base = RAIZ / "pecas" / nome
    for sub in ("stl", "3mf", "componentes"):
        (base / sub).mkdir(parents=True, exist_ok=True)
        for f in (base / sub).glob("*"):
            f.unlink()
    comum = RAIZ / "pecas" / "comum"
    (comum / "stl").mkdir(parents=True, exist_ok=True)
    (comum / "3mf").mkdir(parents=True, exist_ok=True)

    mj = {"modelo": nome, "titulo": mod.titulo, "pecas": [], "componentes": [], "juntas": {}, "poses": [],
          "apoios": mod.apoios, "obs": mod.obs, "encaixes_previstos": getattr(mod, "encaixes", [])}
    cena = trimesh.Scene()
    linhas = []
    malhas_imp = {}
    for p in mod.pecas:
        if p.solido.is_empty():
            raise SystemExit(f"peça vazia: {p.nome} (status {p.solido.status()})")
        s, inv = orientar(p)
        tm = malha(s)
        if p.comum:
            arq = f"../comum/stl/comum-{p.nome}.stl"
            tm.export(comum / "stl" / f"comum-{p.nome}.stl")
            tm.export(comum / "3mf" / f"comum-{p.nome}.3mf")
        else:
            arq = f"stl/{nome}-{p.nome}.stl"
            tm.export(base / "stl" / f"{nome}-{p.nome}.stl")
            tm.export(base / "3mf" / f"{nome}-{p.nome}.3mf")
        malhas_imp[p.nome] = tm
        lo, hi = limites(s)
        dim = [round(float(v), 1) for v in (hi - lo)]
        vol, massa, tempo = estimar(s, p)
        mats = [(np.asarray(c, float) @ inv).tolist() for c in p.copias]
        grupos = p.grupos or [p.grupo] * len(p.copias)
        rgb = list(P.CORES[p.cor])
        mj["pecas"].append({"nome": p.nome, "arquivo": arq, "material": p.material, "cor": p.cor, "rgb": rgb,
                            "grupo": p.grupo, "grupos": grupos, "qtd": max(len(p.copias), 1), "na_montagem": len(p.copias),
                            "para_montagem": mats, "explode": list(p.explode), "suporte": p.suporte, "comum": p.comum,
                            "macica": p.macica, "dim": dim, "tris": int(s.num_tri()), "plastico_cm3": vol, "massa_g": massa,
                            "tempo_h": tempo, "obs": p.obs, "liso": p.liso, "perimetros": p.perimetros,
                            "infill": p.infill, "reforco": p.reforco, "orientacao": p.orientacao})
        for k, M in enumerate(mats):
            g = tm.copy()
            g.visual.face_colors = [int(c * 255) for c in rgb] + [255]
            cena.add_geometry(g, node_name=f"{p.nome}-{k}", geom_name=f"{p.nome}-{k}", transform=np.asarray(M))
        linhas.append((p.nome, dim, max(len(p.copias), 1), p.material, p.cor, massa, tempo, p.suporte))
    exp_g = mod.obs.get("explode_grupo", {})
    for c in mod.comps:
        if not any(c.explode):
            c.explode = tuple(exp_g.get(c.grupo, (0.0, 0.0, 0.0)))
        arq = f"componentes/{c.nome.split(' ')[0]}.stl"
        tm = malha(c.solido)
        tm.export(base / arq)
        grupos = c.grupos or [c.grupo] * len(c.copias)
        mj["componentes"].append({"nome": c.nome, "arquivo": arq, "grupo": c.grupo, "grupos": grupos, "massa_g": c.massa,
                                  "rgb": list(P.CORES[c.cor]), "para_montagem": [np.asarray(m, float).tolist() for m in c.copias],
                                  "fase2": c.fase2, "explode": list(c.explode), "liso": False})
    for g, j in mod.juntas.items():
        mj["juntas"][g] = {"pai": j.pai, "origem": list(map(float, j.origem)), "eixo": list(map(float, j.eixo)), "lim": list(j.lim)}
    mj["poses"] = [{"nome": n, "angulos": a} for (n, a) in mod.poses]
    mj["parede_medida"] = mod.obs.get("parede_medida", {})
    mj["ordem_montagem"] = [{**o, "dir": [float(v) for v in o["dir"]],
                             **({"depois": [[float(v) for v in o["depois"][0]], float(o["depois"][1])]} if "depois" in o else {})} for o in mod.ordem]
    (base / "montagem.json").write_text(json.dumps(mj, ensure_ascii=False, indent=1))
    cena.export(base / "montagem.glb")

    # mesas: agrupa por material+cor
    grupos = {}
    for pj in mj["pecas"]:
        for k in range(pj["qtd"]):
            grupos.setdefault((pj["material"], pj["cor"]), []).append((f'{pj["nome"]}#{k}', pj["dim"][0], pj["dim"][1], pj))
    mesas, cena_m, n_mesa = [], {"pecas": [], "mesas": []}, 0
    (base / "mesas").mkdir(exist_ok=True)
    for f in (base / "mesas").glob("*"):
        f.unlink()
    cenas_mesa = {}
    for (mat, cor), its in sorted(grupos.items()):
        res, n = empacotar([(k, w, d) for (k, w, d, _) in its])
        info = {k: pj for (k, _, _, pj) in its}
        for i in range(n):
            col, lin = (n_mesa + i) % 4, (n_mesa + i) // 4
            cena_m["mesas"].append({"x0": col * 290.0, "y0": -lin * 290.0, "lado": 256.0, "material": mat, "cor": cor})
            mesas.append({"mesa": n_mesa + i + 1, "material": mat, "cor": cor, "itens": []})
        for (k, m_i, x, y) in res:
            pj = info[k]
            col, lin = (n_mesa + m_i) % 4, (n_mesa + m_i) // 4
            px = col * 290.0 + 3 + x + pj["dim"][0] / 2
            py = -lin * 290.0 + 3 + y + pj["dim"][1] / 2
            T = np.eye(4)
            T[:3, 3] = [px, py, 0]
            cena_m["pecas"].append({"arquivo": pj["arquivo"], "rgb": pj["rgb"], "para_montagem": [T.tolist()], "liso": pj["liso"]})
            mesas[n_mesa + m_i]["itens"].append(pj["nome"])
            Tl = np.eye(4)
            Tl[:3, 3] = [3 + x + pj["dim"][0] / 2, 3 + y + pj["dim"][1] / 2, 0]
            cenas_mesa.setdefault(n_mesa + m_i, trimesh.Scene()).add_geometry(malhas_imp[pj["nome"]].copy(), node_name=k, geom_name=k, transform=Tl)
        n_mesa += n
    for i, c in cenas_mesa.items():
        mesas[i]["arquivo"] = f"mesas/{nome}-mesa-{i + 1:02d}-{mesas[i]['material'].lower()}-{mesas[i]['cor']}.3mf"
        c.export(base / mesas[i]["arquivo"])
    (base / "mesas.json").write_text(json.dumps({"mesas_lista": mesas, **cena_m}, ensure_ascii=False, indent=1))

    print(f"== {nome}: {len(mj['pecas'])} peças distintas, {sum(p['qtd'] for p in mj['pecas'])} no total, {n_mesa} mesas, {time.time() - t0:.1f} s")
    for (n, dim, q, mat, cor, massa, tempo, sup) in linhas:
        print(f"  {n:16s} {dim[0]:6.1f} x {dim[1]:6.1f} x {dim[2]:6.1f}  x{q}  {mat:4s} {cor:8s} ~{massa:6.1f} g ~{tempo:5.2f} h  suporte: {sup}")


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    for n in (MODELOS if alvo == "todos" else [alvo]):
        gerar(n)
