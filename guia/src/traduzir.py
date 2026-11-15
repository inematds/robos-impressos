#!/usr/bin/env python3
"""Traduz textos.pt.json (a entrada do guia) para EN e ES pelo tradutor central (inema-traduz, assinatura), com cache.
Também dá o pedido ao tradutor (`pedido`) e a conferência de tags (`tags`) às páginas de robô e à de evolução.
Uso: .venv/bin/python guia/src/traduzir.py [en|es] [--so chave1,chave2]   (sem argumento: os dois, só as chaves que faltam ou mudaram)"""
import json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
IDIOMA = {"en": ("inglês", "capybara", "(in Portuguese)"), "es": ("espanhol neutro da América Latina", "carpincho", "(en portugués)")}


def pedido(lg, bloco):
    nome, capi, nota = IDIOMA[lg]
    return f"""Traduza do português do Brasil para {nome} os VALORES do JSON abaixo (textos de uma página que ensina leigos a imprimir e montar robôs).
Regras:
- Devolva SOMENTE um JSON válido, com exatamente as mesmas chaves, sem comentário, sem cercas de código.
- Mantenha idênticas as tags HTML (<strong>, <code>, <li>, <span class="amb">) e tudo o que estiver dentro de <code>.
- Não traduza: robos-impressos, INEMA.CLUB, Arduino, Raspberry Pi, Bambu Lab A1, Bambu Studio, Blender, Python, git, PLANO.md, FOLGA, MG996R, SG90, MG90S, L298N, KCD11, LiDAR, IMU, PLA, PETG, STL, 3MF, GitHub, Roadmap.
- "capivara" = "{capi}" (em espanhol, nunca "capibara"). "robô quadrado de mesa" = square desktop robot / robot cuadrado de mesa. "robô quadrado que roda" = square robot on wheels / robot cuadrado con ruedas. Na medida de semelhança: "teto" = ceiling / techo; "alvo" = target / objetivo; "desenho de referência" = reference drawing / dibujo de referencia; "régua" = ruler / regla. "inserto" = threaded insert / inserto roscado. "fatiador" = slicer / laminador. "mesa" da impressora = build plate / cama. "casca" = shell / carcasa. "esqueleto" = skeleton / esqueleto.
- Onde aparecer "PLANO.md" seguido de "(em português)", troque a nota por "{nota}"; se aparecer "PLANO.md" sem nota, acrescente "{nota}" logo depois.
- Números, unidades, símbolos (±, °, ×, →, ↓, emojis) ficam iguais. Texto natural, frases curtas, tratando o leitor por "you" / "tú".

{json.dumps(bloco, ensure_ascii=False, indent=1)}"""


def tags(s):
    return sorted(re.findall(r"</?[a-z]+[^>]*>", s))


def cache_de(lg):
    """Marcas do português já traduzido (hash por chave). Fica no git, como as das páginas de robô: sem elas não dá para
    saber, num clone, se a tradução ainda corresponde ao português."""
    return AQUI / f"textos.cache.{lg}.json"


def traduz(lg, so=None):
    """Textos da ENTRADA do guia. Usa o mesmo tradutor com cache e as mesmas conferências das páginas de robô
    (pagina_robo._traduz: chaves, tags, marcadores [[ ]] e trechos entre crases iguais ao português)."""
    import pagina_robo as P          # aqui dentro: pagina_robo importa este módulo (pedido e tags)
    pt = json.loads((AQUI / "textos.pt.json").read_text())
    dest, cache = AQUI / f"textos.{lg}.json", cache_de(lg)
    if so and cache.exists():                                  # --so: força de novo as chaves pedidas
        marcas = json.loads(cache.read_text())
        cache.write_text(json.dumps({k: v for k, v in marcas.items() if k not in so}))
    P._traduz(pt, dest, cache, lg)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    so = None
    if "--so" in sys.argv:
        so = set(sys.argv[sys.argv.index("--so") + 1].split(","))
        args = [a for a in args if a not in so and "," not in a]
    for lg in (args or ["en", "es"]):
        traduz(lg, so)
