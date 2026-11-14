#!/usr/bin/env python3
"""Gera as tabelas de peças e de verificação a partir de pecas/<modelo>/montagem.json e verificacao.json
(fonte única dos números) e as injeta nos documentos, entre marcadores:

    <!-- TABELA:pecas:dino -->   ...   <!-- /TABELA -->        (peças impressas de um modelo)
    <!-- TABELA:verif:dino -->   ...   <!-- /TABELA -->        (saída do verificador)
    <!-- TABELA:resumo -->       ...   <!-- /TABELA -->        (resumo dos 3 modelos)

Uso:  .venv/bin/python cad/tabelas.py            (reescreve pecas/TABELAS.md e injeta em PLANO.md, README*.md, guia/**/index.html)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = ["dino", "capivara", "cubo"]
T = {
    "pt": dict(peca="Peça", dim="Tamanho deitada (mm)", qtd="Qtd", mat="Material", cor="Cor", sup="Suporte", massa="Filamento (g)*", tempo="Tempo (h)*",
               comum="comum", total="Total", teste="Teste", res="Resultado", passou="PASSOU", falhou="FALHOU", modelo="Modelo", altura="Altura (mm)",
               pecas="Peças", mesas="Mesa", massa_t="Filamento total (g)*", tempo_t="Impressão total (h)*", massa_robo="Robô montado (g)*",
               nao="não", sim="sim", est="* estimativa por volume, sem fatiador"),
    "en": dict(peca="Part", dim="Size on the bed (mm)", qtd="Qty", mat="Material", cor="Colour", sup="Supports", massa="Filament (g)*", tempo="Time (h)*",
               comum="shared", total="Total", teste="Test", res="Result", passou="PASSED", falhou="FAILED", modelo="Model", altura="Height (mm)",
               pecas="Parts", mesas="Plate", massa_t="Total filament (g)*", tempo_t="Total print time (h)*", massa_robo="Assembled robot (g)*",
               nao="no", sim="yes", est="* estimate from volume, no slicer"),
    "es": dict(peca="Pieza", dim="Tamaño en la cama (mm)", qtd="Cant.", mat="Material", cor="Color", sup="Soportes", massa="Filamento (g)*", tempo="Tiempo (h)*",
               comum="común", total="Total", teste="Prueba", res="Resultado", passou="PASÓ", falhou="FALLÓ", modelo="Modelo", altura="Altura (mm)",
               pecas="Piezas", mesas="Cama", massa_t="Filamento total (g)*", tempo_t="Impresión total (h)*", massa_robo="Robot armado (g)*",
               nao="no", sim="sí", est="* estimación por volumen, sin laminador"),
}
NOMES = {"pt": {"dino": "Dinossauro", "capivara": "Capivara", "cubo": "Robô quadrado"},
         "en": {"dino": "Dinosaur", "capivara": "Capybara", "cubo": "Square robot"},
         "es": {"dino": "Dinosaurio", "capivara": "Carpincho", "cubo": "Robot cuadrado"}}
CORES = {"en": {"verde": "green", "creme": "cream", "azul": "blue", "branco": "white", "preto": "black", "cinza": "grey", "laranja": "orange",
                "marrom": "brown", "verde-bandana": "green", "ciano": "cyan", "grafite": "graphite", "prata": "silver", "amarelo": "yellow"},
         "es": {"verde": "verde", "creme": "crema", "azul": "azul", "branco": "blanco", "preto": "negro", "cinza": "gris", "laranja": "naranja",
                "marrom": "marrón", "verde-bandana": "verde", "ciano": "cian", "grafite": "grafito", "prata": "plata", "amarelo": "amarillo"}}


def carrega(m):
    b = RAIZ / "pecas" / m
    return json.loads((b / "montagem.json").read_text()), json.loads((b / "verificacao.json").read_text()), json.loads((b / "mesas.json").read_text())


def sup(txt, lg):
    t = T[lg]
    return t["nao"] if txt.startswith("não") else t["sim"]


def linhas_pecas(m, lg):
    mj, _, _ = carrega(m)
    t = T[lg]
    cab = [t["peca"], t["dim"], t["qtd"], t["mat"], t["cor"], t["sup"], t["massa"], t["tempo"]]
    ls = []
    for p in mj["pecas"]:
        cor = CORES.get(lg, {}).get(p["cor"], p["cor"])
        nome = p["nome"] + (f" ({t['comum']})" if p["comum"] else "")
        ls.append([nome, f'{p["dim"][0]:.0f} × {p["dim"][1]:.0f} × {p["dim"][2]:.0f}', str(p["qtd"]), p["material"], cor, sup(p["suporte"], lg),
                   f'{p["massa_g"] * p["qtd"]:.0f}', f'{p["tempo_h"] * p["qtd"]:.1f}'])
    tot_m = sum(p["massa_g"] * p["qtd"] for p in mj["pecas"])
    tot_t = sum(p["tempo_h"] * p["qtd"] for p in mj["pecas"])
    ls.append([f'**{t["total"]}**', "", str(sum(p["qtd"] for p in mj["pecas"])), "", "", "", f"**{tot_m:.0f}**", f"**{tot_t:.0f}**"])
    return cab, ls


def linhas_verif(m, lg):
    _, v, _ = carrega(m)
    t = T[lg]
    return [t["teste"], t["res"], ""], [[k, t["passou"] if x["ok"] else t["falhou"], x["texto"]] for k, x in v["testes"].items()]


def altura(m):
    import numpy as np

    mj, _, _ = carrega(m)
    z = 0.0
    for p in mj["pecas"]:
        for M in p["para_montagem"]:
            M = np.array(M)
            d = p["dim"]
            cantos = np.array([[sx * d[0] / 2, sy * d[1] / 2, sz * d[2], 1] for sx in (-1, 1) for sy in (-1, 1) for sz in (0, 1)])
            z = max(z, float((cantos @ M.T)[:, 2].max()))
    return z


def linhas_mesas(m, lg):
    _, _, ms = carrega(m)
    t = T[lg]
    cab = [t["mesas"], t["mat"], t["cor"], t["peca"]]
    ls = []
    for x in ms["mesas_lista"]:
        from collections import Counter
        c = Counter(x["itens"])
        itens = ", ".join(f"{n} ×{q}" if q > 1 else n for n, q in c.items())
        ls.append([str(x["mesa"]), x["material"], CORES.get(lg, {}).get(x["cor"], x["cor"]), itens])
    return cab, ls


def linhas_resumo(lg):
    t = T[lg]
    cab = [t["modelo"], t["altura"], t["pecas"], t["mesas"] + {"pt": "s (impressões)", "en": "s (print jobs)", "es": "s (impresiones)"}[lg], t["massa_t"], t["tempo_t"], t["massa_robo"]]
    ls = []
    for m in MODELOS:
        mj, v, ms = carrega(m)
        ls.append([NOMES[lg][m], f"{altura(m):.0f}", str(sum(p["qtd"] for p in mj["pecas"])), str(len(ms["mesas"])),
                   f'{sum(p["massa_g"] * p["qtd"] for p in mj["pecas"]):.0f}', f'{sum(p["tempo_h"] * p["qtd"] for p in mj["pecas"]):.0f}',
                   f'{v["cg"][0]["massa_g"]:.0f}'])
    return cab, ls


ARRASTE = {"pt": "↔ no celular, arraste a tabela para o lado", "en": "↔ on a phone, swipe the table sideways", "es": "↔ en el celular, desliza la tabla hacia un lado"}
LG_ATUAL = ["pt"]


def md(cab, ls):
    o = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    o += ["| " + " | ".join(l) + " |" for l in ls]
    return "\n".join(o)


def html(cab, ls):
    f = lambda s: re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    o = ['<p class="arraste">' + ARRASTE[LG_ATUAL[0]] + '</p><div class="tabela-wrap"><table class="tabela"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cab) + "</tr></thead><tbody>"]
    o += ["<tr>" + "".join(f"<td>{f(c)}</td>" for c in l) + "</tr>" for l in ls]
    o.append("</tbody></table></div>")
    return "\n".join(o)


def tabela(chave, lg, fmt):
    LG_ATUAL[0] = lg
    partes = chave.split(":")
    if partes[0] == "pecas":
        cab, ls = linhas_pecas(partes[1], lg)
    elif partes[0] == "verif":
        cab, ls = linhas_verif(partes[1], "pt" if fmt == "md" and lg == "pt" else lg)
    elif partes[0] == "resumo":
        cab, ls = linhas_resumo(lg)
    elif partes[0] == "mesas":
        cab, ls = linhas_mesas(partes[1], lg)
        if fmt == "md":
            ls = [[c.replace("<code>", "`").replace("</code>", "`") for c in l] for l in ls]
    else:
        raise ValueError(chave)
    corpo = md(cab, ls) if fmt == "md" else html(cab, ls)
    if partes[0] in ("pecas", "resumo"):
        corpo += ("\n\n" + T[lg]["est"]) if fmt == "md" else f'\n<p class="nota">{T[lg]["est"]}</p>'
    return corpo


def injeta(arquivo: Path, lg, fmt):
    if not arquivo.exists():
        return 0
    s = arquivo.read_text()
    n = 0

    def troca(mo):
        nonlocal n
        n += 1
        return f"<!-- TABELA:{mo.group(1)} -->\n{tabela(mo.group(1), lg, fmt)}\n<!-- /TABELA -->"

    s2 = re.sub(r"<!-- TABELA:([a-z:]+) -->.*?<!-- /TABELA -->", troca, s, flags=re.S)
    if s2 != s:
        arquivo.write_text(s2)
    return n


if __name__ == "__main__":
    o = ["# Tabelas geradas (não edite: rode `cad/tabelas.py`)\n", "## Resumo\n", tabela("resumo", "pt", "md"), ""]
    for m in MODELOS:
        o += [f"\n## {NOMES['pt'][m]} — peças impressas\n", tabela(f"pecas:{m}", "pt", "md"), f"\n### {NOMES['pt'][m]} — verificação\n", tabela(f"verif:{m}", "pt", "md")]
    (RAIZ / "pecas" / "TABELAS.md").write_text("\n".join(o) + "\n")
    alvos = [("PLANO.md", "pt", "md"), ("README.md", "pt", "md"), ("README.en.md", "en", "md"), ("README.es.md", "es", "md"),
             ("guia/index.html", "pt", "html"), ("guia/en/index.html", "en", "html"), ("guia/es/index.html", "es", "html")]
    for (a, lg, fmt) in alvos:
        n = injeta(RAIZ / a, lg, fmt)
        if n:
            print(f"{a}: {n} tabela(s)")
    print("pecas/TABELAS.md ok")
