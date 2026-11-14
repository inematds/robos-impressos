#!/usr/bin/env python3
"""Traduz o README.md para README.en.md e README.es.md pelo tradutor central (inema-traduz, assinatura)."""
import re, subprocess, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
PT = (RAIZ / "README.md").read_text()
# tabelas geradas saem do texto (cad/tabelas.py as recoloca já traduzidas)
PT = re.sub(r"(<!-- TABELA:[a-z:]+ -->).*?(<!-- /TABELA -->)", r"\1\n\2", PT, flags=re.S)
CFG = {"en": ("inglês", "capybara", "What it is", "(in Portuguese)"), "es": ("espanhol neutro da América Latina", "carpincho", "Qué es", "(en portugués)")}
for lg in (sys.argv[1:] or ["en", "es"]):
    nome, capi, oque, nota = CFG[lg]
    pedido = f"""Traduza este README (Markdown) do português do Brasil para {nome}. Devolva SOMENTE o Markdown traduzido, sem cercas de código em volta.
Regras:
- Mantenha idênticos: a estrutura Markdown, as tabelas, os comandos e caminhos dentro de crases, os nomes de arquivo, os emojis, os marcadores <!-- TABELA:... --> e <!-- /TABELA -->, e a linha do seletor de idioma (a que começa com **🇧🇷).
- Troque a URL do guia `https://inematds.github.io/robos-impressos/guia/` por `https://inematds.github.io/robos-impressos/guia/{lg}/` e `guia/assets/banner.jpg` por `guia/assets/banner-{lg}.jpg`.
- O título da seção "## O que é" vira "## {oque}".
- Links para PLANO.md continuam apontando para PLANO.md (com as mesmas âncoras em português) e ganham a nota "{nota}" depois do link.
- Não traduza: robos-impressos, INEMA.CLUB, Arduino, Raspberry Pi, Bambu Lab A1, PLANO.md, nomes de servos e motores, PLA, PETG, STL, 3MF, GitHub Pages, `claude -p`.
- "capivara" = "{capi}"; "fatiador" = slicer / laminador; "mesa" da impressora = build plate / cama; "inserto" = threaded insert / inserto roscado.

{PT}"""
    r = subprocess.run(["inema-traduz"], input=pedido, capture_output=True, text=True, timeout=1200)
    out = r.stdout.strip()
    out = re.sub(r"^```(?:markdown)?\n|\n```$", "", out)
    assert out.count("<!-- TABELA:") == PT.count("<!-- TABELA:") and "🇧🇷" in out and f"/guia/{lg}/" in out, f"tradução {lg} incompleta"
    (RAIZ / f"README.{lg}.md").write_text(out + "\n")
    print(lg, len(out))
