#!/usr/bin/env python3
"""Depuração: lista volume, nº de corpos e caixa de cada peça de um modelo (sem exportar)."""
import sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # comum/ = raiz de import do pacote `cad`
from cad.caminhos import construir
from cad.comum.geo import limites

t = time.time()
mod = construir(sys.argv[1])
print("construído em", round(time.time() - t, 1), "s")
for p in mod.pecas:
    if p.solido.is_empty():
        print(f"{p.nome:16s} VAZIA"); continue
    lo, hi = limites(p.solido)
    cs = p.solido.decompose()
    vols = sorted([round(c.volume(), 1) for c in cs], reverse=True)
    print(f"{p.nome:16s} vol {p.solido.volume():9.0f} tris {p.solido.num_tri():6d} corpos {len(cs)} {vols[1:4] if len(cs)>1 else ''} lo {np.round(lo,0)} hi {np.round(hi,0)}")
