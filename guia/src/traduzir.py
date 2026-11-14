#!/usr/bin/env python3
"""Traduz textos.pt.json para EN e ES pelo tradutor central (inema-traduz, assinatura). Confere chaves e tags.
Uso: python3 guia/src/traduzir.py [en|es] [--so chave1,chave2]   (sem argumento: os dois, só as chaves que faltam ou mudaram)"""
import json, re, subprocess, sys, hashlib
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
- "capivara" = "{capi}". "inserto" = threaded insert / inserto roscado. "fatiador" = slicer / laminador. "mesa" da impressora = build plate / cama. "casca" = shell / carcasa. "esqueleto" = skeleton / esqueleto.
- Onde aparecer "PLANO.md" seguido de "(em português)", troque a nota por "{nota}"; se aparecer "PLANO.md" sem nota, acrescente "{nota}" logo depois.
- Números, unidades, símbolos (±, °, ×, →, ↓, emojis) ficam iguais. Texto natural, frases curtas, tratando o leitor por "you" / "tú".

{json.dumps(bloco, ensure_ascii=False, indent=1)}"""


def tags(s):
    return sorted(re.findall(r"</?[a-z]+[^>]*>", s))


def traduz(lg, so=None):
    pt = json.loads((AQUI / "textos.pt.json").read_text())
    dest = AQUI / f"textos.{lg}.json"
    cache = AQUI / f".cache.{lg}.json"
    feito = json.loads(dest.read_text()) if dest.exists() else {}
    marcas = json.loads(cache.read_text()) if cache.exists() else {}
    h = lambda t: hashlib.sha1(t.encode()).hexdigest()[:12]
    pend = [k for k in pt if (so and k in so) or (not so and (k not in feito or marcas.get(k) != h(pt[k])))]
    for i in range(0, len(pend), 45):
        chaves = pend[i:i + 45]
        bloco = {k: pt[k] for k in chaves}
        for tentativa in range(3):
            r = subprocess.run(["inema-traduz"], input=pedido(lg, bloco), capture_output=True, text=True, timeout=900)
            txt = r.stdout.strip()
            mo = re.search(r"\{.*\}", txt, re.S)
            try:
                out = json.loads(mo.group(0))
                assert set(out) == set(bloco), "chaves diferentes"
                ruins = [k for k in bloco if tags(out[k]) != tags(bloco[k])]
                assert not ruins, f"tags diferentes em {ruins}"
                break
            except Exception as e:
                print(f"  {lg} bloco {i}: tentativa {tentativa + 1} falhou ({e})", flush=True)
                out = None
        if out is None:
            raise SystemExit(f"Falhou: tradução {lg} bloco {i}")
        feito.update(out)
        for k in chaves:
            marcas[k] = h(pt[k])
        dest.write_text(json.dumps({k: feito[k] for k in pt if k in feito}, ensure_ascii=False, indent=1))
        cache.write_text(json.dumps(marcas))
        print(f"  {lg}: {min(i + 45, len(pend))}/{len(pend)}", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    so = None
    if "--so" in sys.argv:
        so = set(sys.argv[sys.argv.index("--so") + 1].split(","))
        args = [a for a in args if a not in so and "," not in a]
    for lg in (args or ["en", "es"]):
        traduz(lg, so)
