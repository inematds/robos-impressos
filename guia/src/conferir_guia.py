#!/usr/bin/env python3
"""Confere TODAS as páginas do guia, sem servidor: entrada, página de cada robô e evolução, em PT, EN e ES.

Em cada página: todo src/href relativo existe em disco (e a âncora, quando há, existe na página de destino); toda âncora
interna tem destino; todo link do GitHub (raw, blob, tree em main) aponta para arquivo que existe e não é ignorado pelo
git; nenhum [[ ]] nem {{ }} sobrando; hreflang dos 3 idiomas apontando para a própria página; troca de idioma com os 3
links válidos; nav com INEMA.CLUB; toda imagem com alt; mesma contagem de tags nos 3 idiomas; inglês sem vírgula decimal;
nenhuma nota interna no texto; EN/ES sem português sobrando fora de <pre> e <code>.
Na entrada: as âncoras da página publicada antes (origin/main) continuam existindo e a versão aparece.

Uso: .venv/bin/python guia/src/conferir_guia.py      (sai com 1 se algo falhar)
"""
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import montar            # noqa: E402
import pagina_robo as P  # noqa: E402

GUIA, RAIZ = P.GUIA, P.RAIZ
SITE = "https://inematds.github.io/robos-impressos/guia/"
PAGINAS = [""] + [m + "/" for m in montar.MODELOS] + ["evolucao/"]          # caminho dentro de guia/ (ou guia/<lg>/)
HREFLANG = {"pt": "pt-BR", "en": "en", "es": "es"}
TAGS = ("section", "div", "tr", "td", "li", "img", "a", "h2", "h3", "h4", "dt", "figure", "details")
PORTUGUES = r"\w+ção\b|\w+ções\b|\bvocê\b|\bnão\b|\bpeças?\b|\brobôs?\b|\bimpressão\b"
# palavras que ficam em português de propósito nas páginas traduzidas (hoje nenhuma)
PT_PERMITIDO = set()
MARCADOR_PT = "&lt;robô&gt;"                # o marcador de pasta dos caminhos (projetos/<robô>/), igual nos 3 idiomas


def arq(pag, lg):
    return GUIA / ("" if lg == "pt" else lg) / pag / "index.html"


def visivel(h):
    return re.sub(r"<pre.*?</pre>|<code.*?</code>|<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<[^>]+>", " ", h[h.index("<body"):], flags=re.S)


def main():
    falhas = []
    ignorados = lambda cs: set(subprocess.run(["git", "-C", str(RAIZ), "check-ignore", *cs], capture_output=True, text=True).stdout.split()) if cs else set()
    textos = {}
    for pag in PAGINAS:
        conta = {}
        for lg in P.IDIOMAS:
            f = arq(pag, lg)
            rel = str(f.relative_to(RAIZ))
            bad = lambda msg: falhas.append(f"{rel}: {msg}")
            if not f.exists():
                bad("página não existe")
                continue
            h = textos[f] = f.read_text()
            ids = set(re.findall(r'\bid="([^"]+)"', h))
            # --- links relativos e âncoras
            for u, frag in re.findall(r'(?:src|href)="([^"#]*)(#[^"]*)?"', h):
                if re.match(r"(https?:|mailto:|data:)", u):
                    continue
                if not u:
                    if frag and frag[1:] not in ids:
                        bad(f"âncora {frag} sem destino")
                    continue
                alvo = f.parent / u
                alvo = alvo / "index.html" if u.endswith("/") else alvo
                if not alvo.exists():
                    bad(f"link relativo quebrado: {u}")
                elif frag and alvo.suffix == ".html" and f'id="{frag[1:]}"' not in alvo.read_text():
                    bad(f"âncora {frag} não existe em {u}")
            # --- links para o repositório no GitHub
            gh = sorted(set(re.findall(re.escape(P.REPO) + r'/(?:raw|blob|tree)/main/([^"#?]+)', h)))
            for u in gh:
                if not (RAIZ / u).exists():
                    bad(f"link do GitHub para arquivo que não existe no repo: {u}")
            for u in ignorados(gh):
                bad(f"link do GitHub para arquivo ignorado pelo git: {u}")
            # --- marcadores, hreflang, idioma, nav
            if "[[" in h or "{{" in h.replace("${{", ""):
                bad("[[ ]] ou {{ }} sobrando")
            for k, cod in HREFLANG.items():
                esperado = f'<link rel="alternate" hreflang="{cod}" href="{SITE}{"" if k == "pt" else k + "/"}{pag}">'
                if esperado not in h:
                    bad(f"falta {esperado}")
            if f'<html lang="{HREFLANG[lg]}">' not in h:
                bad("atributo lang do <html> errado")
            mo = re.search(r'<span class="lang">(.*?)</span>', h, re.S)
            troca = re.findall(r'<a( class="on")? href="([^"]+)">(PT|EN|ES)</a>', mo.group(1)) if mo else []
            if [x[2] for x in troca] != ["PT", "EN", "ES"]:
                bad("troca de idioma sem os 3 links PT/EN/ES")
            for on, u, rot in troca:
                k = rot.lower()
                if bool(on) != (k == lg):
                    bad(f"troca de idioma: marca 'on' errada em {rot}")
                if (f.parent / u / "index.html").resolve() != arq(pag, k).resolve():
                    bad(f"troca de idioma: {rot} aponta para {u}, não para a mesma página em {k}")
            if '<a class="inema" href="https://inema.club"' not in h:
                bad("nav sem o link INEMA.CLUB")
            for img in re.findall(r"<img\b[^>]*>", h):
                if not re.search(r'\balt="[^"]+"', img):
                    bad(f"imagem sem alt: {img[:80]}")
            # --- texto
            v = visivel(h.replace(MARCADOR_PT, " "))
            if lg == "en":
                for m in sorted(set(re.findall(r"\S*\d,\d\S*", v))):
                    bad(f"vírgula decimal ou de milhar no inglês: '{m}'")
            for pad in P.INTERNAS:
                for m in sorted(set(re.findall(pad, v))):
                    bad(f"nota interna no texto: '{m}'")
            if lg != "pt":
                pt = sorted({m.lower() for m in re.findall(PORTUGUES, v, flags=re.I)} - PT_PERMITIDO)
                if pt:
                    bad(f"português sobrando no texto: {pt[:12]}")
            conta[lg] = {tg: len(re.findall(f"<{tg}[ >]", h)) for tg in TAGS}
        for lg in ("en", "es"):
            if lg in conta and "pt" in conta and conta[lg] != conta["pt"]:
                dif = {k: (conta["pt"][k], conta[lg][k]) for k in TAGS if conta["pt"][k] != conta[lg][k]}
                falhas.append(f"guia/{lg}/{pag}: contagem de tags diferente do PT (pt, {lg}): {dif}")
        if "pt" in conta:
            print(f"guia/{pag or '(entrada)'}: {conta['pt']['section']} seções, {conta['pt']['img']} imagens, {conta['pt']['a']} links por idioma")
    # --- entrada: âncoras antigas e versão
    antiga = subprocess.run(["git", "-C", str(RAIZ), "show", "origin/main:guia/index.html"], capture_output=True, text=True)
    if antiga.returncode == 0:
        velhas = set(re.findall(r'\bid="([^"]+)"', antiga.stdout))
        for lg in P.IDIOMAS:
            h = textos.get(arq("", lg), "")
            sumiram = sorted(velhas - set(re.findall(r'\bid="([^"]+)"', h)))
            if sumiram:
                falhas.append(f"entrada {lg}: âncoras da página publicada que sumiram: {sumiram}")
        print(f"entrada: {len(velhas)} âncoras da página publicada (origin/main) conferidas")
    else:
        falhas.append("não consegui ler origin/main:guia/index.html para conferir as âncoras antigas")
    for lg in P.IDIOMAS:
        if montar.VERSAO not in visivel(textos.get(arq("", lg), "<body")):
            falhas.append(f"entrada {lg}: versão {montar.VERSAO} não aparece")
    for x in falhas:
        print("  FALHA", x)
    print("conferir_guia:", "OK" if not falhas else f"FALHOU ({len(falhas)})", f"· {len(textos)} páginas")
    return not falhas


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
