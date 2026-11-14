#!/usr/bin/env python3
"""Monta o guia nos 3 idiomas a partir de corpo.html (estrutura única) + textos.<idioma>.json.
A estrutura é a mesma por construção; só os textos mudam. Depois rode cad/tabelas.py para preencher as tabelas.

Uso: python3 guia/src/montar.py
"""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GUIA = AQUI.parent
RAIZ = GUIA.parent
TEMPLATE = Path.home() / ".claude/skills/projetos-landing-guia/assets/template.html"
MODELOS = ["dino", "capivara", "cubo"]
NOME = {"pt": {"dino": "Dinossauro", "capivara": "Capivara", "cubo": "Robô quadrado"},
        "en": {"dino": "Dinosaur", "capivara": "Capybara", "cubo": "Square robot"},
        "es": {"dino": "Dinosaurio", "capivara": "Carpincho", "cubo": "Robot cuadrado"}}
CSS_EXTRA = """
  .techhead{background:var(--bg2);border-top:3px solid var(--amb);padding:58px 0 8px}
  .techhead h2{font-family:Sora;margin:.3em 0 0}
  .techzone{background:var(--bg2)}
  .nota{font-size:.88rem;color:var(--mut);margin-top:14px;max-width:80ch}
  .mini{font-size:.82rem;color:var(--mut);margin:.4em 0 0}
  .shot{display:block;width:100%;border-radius:12px;border:1px solid var(--line);margin:0 0 14px;background:#e9e9ee}
  .g2{grid-template-columns:repeat(2,1fr)} .g4{grid-template-columns:repeat(4,1fr)}
  .numero{text-align:center} .numero b{display:block;font-family:Sora;font-size:2.1rem;color:var(--amb);line-height:1.15} .numero span{display:block;font-size:.9rem;color:var(--mut);margin-top:6px}
  .arraste{display:none;font-size:.8rem;color:var(--mut);margin:18px 0 -14px}
  .sep4{font-family:Sora;margin:22px 0 10px}
  #pecas,#compras,section{scroll-margin-top:76px} .hero figcaption.mini{padding:8px 12px 10px}
  .glossario{margin:18px 0 0;display:grid;grid-template-columns:max-content 1fr;gap:8px 18px} .glossario dt{font-weight:700;color:var(--amb)} .glossario dd{margin:0}
  .tabela-wrap{overflow-x:auto;margin:22px 0 6px;border:1px solid var(--line);border-radius:12px}
  .tabela{border-collapse:collapse;width:100%;font-size:.9rem;min-width:560px}
  .tabela th,.tabela td{padding:8px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
  .tabela th{font-family:Sora;font-size:.82rem;color:var(--mut);background:var(--bg2)}
  .tabela tr:last-child td{border-bottom:0}
  .barras{margin-top:22px} .barra{display:grid;grid-template-columns:150px 1fr 60px;gap:10px;align-items:center;margin:8px 0;font-size:.92rem}
  .barra i{display:block;height:16px;border-radius:8px;background:var(--amb)}
  .lista{margin:.4em 0 0 1.2em;padding:0} .lista li{margin:.3em 0}
  .sep3{font-family:Sora;margin:34px 0 0}
  pre.saida{white-space:pre-wrap;font-size:.8rem;line-height:1.5}
  .card ul{margin:.5em 0 0 1.1em;padding:0} .card li{margin:.35em 0}
  @media(max-width:1180px){nav .links .sec{display:none}}
  @media(max-width:860px){.g2,.g4{grid-template-columns:1fr}.barra{grid-template-columns:110px 1fr 50px}.arraste{display:block}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.74rem}figcaption.mini{padding:8px 4px 0}.glossario{grid-template-columns:1fr;gap:2px 0}.glossario dd{margin:0 0 10px}}
"""


def cabeca_rodape():
    t = TEMPLATE.read_text().split("\n")
    i_body = next(i for i, l in enumerate(t) if l.strip() == "<body>")
    i_script = next(i for i, l in enumerate(t) if l.strip().startswith("<script>"))
    head = "\n".join(t[:i_body + 1])
    script = "\n".join(t[i_script:])
    head = head.replace("</style>", CSS_EXTRA + "</style>", 1)
    head = re.sub(r"<!-- TEMPLATE.*?-->\n?", "", head, flags=re.S)
    return head, script


def numeros():
    tot, parede, maior, horas = 0, 9.9, 0.0, {}
    for m in MODELOS:
        mj = json.loads((RAIZ / "pecas" / m / "montagem.json").read_text())
        tot += sum(p["qtd"] for p in mj["pecas"])
        for v in mj.get("parede_medida", {}).values():
            parede = min(parede, v["min"])
        maior = max(maior, max(max(p["dim"]) for p in mj["pecas"]))
        horas[m] = sum(p["tempo_h"] * p["qtd"] for p in mj["pecas"])
    return tot, parede, maior, horas


def saida_verif():
    o = []
    for m in MODELOS:
        v = json.loads((RAIZ / "pecas" / m / "verificacao.json").read_text())
        o.append(f"== {m}")
        for k, x in v["testes"].items():
            o.append(f"  [{'PASSOU' if x['ok'] else 'FALHOU'}] {k}: {x['texto']}")
    return "\n".join(o).replace("&", "&amp;").replace("<", "&lt;")


def montar(lg):
    tx = json.loads((AQUI / f"textos.{lg}.json").read_text())
    head, script = cabeca_rodape()
    corpo = (AQUI / "corpo.html").read_text()
    tot, parede, maior, horas = numeros()
    hmax = max(horas.values())
    barras = "\n    ".join(f'<div class="barra"><span>{NOME[lg][m]}</span><i style="width:{horas[m] / hmax * 100:.0f}%"></i><b>~{horas[m]:.0f} h</b></div>' for m in MODELOS)
    A = "assets/" if lg == "pt" else "../assets/"
    lang = {"pt": '<span class="lang"><a class="on" href="./">PT</a><a href="en/">EN</a><a href="es/">ES</a></span>',
            "en": '<span class="lang"><a href="../">PT</a><a class="on" href="./">EN</a><a href="../es/">ES</a></span>',
            "es": '<span class="lang"><a href="../">PT</a><a href="../en/">EN</a><a class="on" href="./">ES</a></span>'}[lg]
    fixos = {"LANG": lang, "A": A, "SUF": "" if lg == "pt" else f"-{lg}", "N_PECAS": str(tot), "N_PAREDE": f"{parede:.2f}".replace(".", "," if lg != "en" else "."),
             "N_MAIOR": f"{maior:.0f}", "BARRAS": barras, "SAIDA_VERIF": saida_verif()}
    faltam = set()

    def troca(mo):
        k = mo.group(1)
        if k in fixos:
            return fixos[k]
        if k not in tx:
            faltam.add(k)
            return mo.group(0)
        return tx[k]

    corpo = re.sub(r"\[\[([A-Za-z0-9_]+)\]\]", troca, corpo)
    assert not faltam, f"{lg}: textos faltando {sorted(faltam)}"
    head = (head.replace("{{PROJETO}} — {{TAGLINE}}", tx["titulo"]).replace("{{META_DESCRICAO}}", tx["meta"]).replace("{{SLUG}}", "robos-impressos"))
    head = head.replace('<html lang="pt-BR">', {"pt": '<html lang="pt-BR">', "en": '<html lang="en">', "es": '<html lang="es">'}[lg])
    script = script.replace("{{SLUG}}", "robos-impressos")
    pagina = head + "\n\n" + corpo + "\n" + script
    assert "{{" not in pagina.replace("${{", ""), "placeholder do template sobrando"
    destino = GUIA / ("index.html" if lg == "pt" else f"{lg}/index.html")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pagina)
    print(destino.relative_to(RAIZ), len(pagina))


if __name__ == "__main__":
    for lg in ("pt", "en", "es"):
        if (AQUI / f"textos.{lg}.json").exists():
            montar(lg)
