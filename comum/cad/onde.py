#!/usr/bin/env python3
"""Depuração: mostra ONDE (caixa em mm, montagem) cada par de sólidos se sobrepõe numa pose.
Uso: .venv/bin/python comum/cad/onde.py <modelo> [pose]"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # comum/ = raiz de import do pacote `cad`
from cad.caminhos import id_de, pasta
from cad.verificar import carrega, para_manifold, interferencias, matriz_grupo

nome = id_de(sys.argv[1]); pose_n = sys.argv[2] if len(sys.argv) > 2 else "neutra"
base = pasta(nome)
mj = json.loads((base / "montagem.json").read_text())
itens = []
for grupo_lista, chave in ((mj["pecas"], True), (mj["componentes"], False)):
    for p in grupo_lista:
        m0 = para_manifold(carrega(base / p["arquivo"]))
        for k, M in enumerate(p["para_montagem"]):
            nm = f"{p['nome']}#{k}" if len(p["para_montagem"]) > 1 else p["nome"]
            itens.append((nm, p["grupos"][k], m0.transform(np.asarray(M)[:3, :]), None, None))
ang = next(p["angulos"] for p in mj["poses"] if p["nome"] == pose_n)
res, pos = interferencias(itens, mj["juntas"], ang, so_moveis=(pose_n != "neutra"))
d = {p[0]: p[2] for p in pos}
prev = {tuple(sorted(e["par"])) for e in mj.get("encaixes_previstos", [])}
for (a, b, v) in res:
    if tuple(sorted((a.split("#")[0], b.split("#")[0]))) in prev: continue
    bb = (d[a] ^ d[b]).bounding_box()
    print(f"{a:18s} x {b:22s} {v:8.1f}  x[{bb[0]:6.1f},{bb[3]:6.1f}] y[{bb[1]:6.1f},{bb[4]:6.1f}] z[{bb[2]:6.1f},{bb[5]:6.1f}]")
