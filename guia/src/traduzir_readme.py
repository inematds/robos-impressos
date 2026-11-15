#!/usr/bin/env python3
"""Traduz o README.md para README.en.md e README.es.md pelo tradutor central (inema-traduz, assinatura)."""
import re, subprocess, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
PT = (RAIZ / "README.md").read_text()
# tabelas geradas saem do texto (comum/cad/tabelas.py as recoloca já traduzidas)
PT = re.sub(r"(<!-- TABELA:[a-z_:]+ -->).*?(<!-- /TABELA -->)", r"\1\n\2", PT, flags=re.S)
CFG = {"en": ("inglês", "capybara", "What it is", "(in Portuguese)"), "es": ("espanhol neutro da América Latina", "carpincho", "Qué es", "(en portugués)")}
for lg in (sys.argv[1:] or ["en", "es"]):
    nome, capi, oque, nota = CFG[lg]
    pedido = f"""Traduza este README (Markdown) do português do Brasil para {nome}. Devolva SOMENTE o Markdown traduzido, sem cercas de código em volta.
Regras:
- Mantenha idênticos: a estrutura Markdown, as tabelas, os comandos e caminhos dentro de crases, os nomes de arquivo, os emojis, os marcadores <!-- TABELA:... --> e <!-- /TABELA -->, e a linha do seletor de idioma (a que começa com **🇧🇷).
- Troque a URL do guia `https://inematds.github.io/robos-impressos/guia/` por `https://inematds.github.io/robos-impressos/guia/{lg}/` e `guia/assets/banner.jpg` por `guia/assets/banner-{lg}.jpg`.
- O título da seção "## O que é" vira "## {oque}".
- Mantenha idêntico o destino de cada link (o que fica entre parênteses depois de `]`); as únicas trocas são as pedidas acima.
- Os links para o PLANO.md da raiz (`](PLANO.md)`) e para `comum/README.md` ganham a nota "{nota}" depois do link. Os links da tabela dos robôs ficam como estão, sem nota.
- "robô quadrado de mesa" = square desktop robot / robot cuadrado de mesa; "robô quadrado que roda" = square robot on wheels / robot cuadrado con ruedas; "cupom de teste" = test coupon / cupón de prueba; "plano" (o arquivo) = plan / plan.
- Não traduza: robos-impressos, INEMA.CLUB, Arduino, Raspberry Pi, Bambu Lab A1, PLANO.md, nomes de servos e motores, PLA, PETG, STL, 3MF, GitHub Pages, `claude -p`.
- "capivara" = "{capi}"; "fatiador" = slicer / laminador; "mesa" da impressora = build plate / cama; "inserto" = threaded insert / inserto roscado.

{PT}"""
    r = subprocess.run(["inema-traduz"], input=pedido, capture_output=True, text=True, timeout=1200)
    out = r.stdout.strip()
    out = re.sub(r"^```(?:markdown)?\n|\n```$", "", out)
    # os 3 guias de cada robô têm versão no idioma: o link passa a apontar para ela
    out = re.sub(r"\]\((projetos/[a-z-]+/(?:LISTA-DE-COMPRAS|IMPRIMIR|LIGACAO))\.md\)", rf"](\1.{lg}.md)", out)
    assert out.count("](") == PT.count("]("), f"tradução {lg}: número de links diferente"
    assert out.count("<!-- TABELA:") == PT.count("<!-- TABELA:") and "🇧🇷" in out and f"/guia/{lg}/" in out, f"tradução {lg} incompleta"
    (RAIZ / f"README.{lg}.md").write_text(out + "\n")
    print(lg, len(out))
