#!/usr/bin/env python3
"""Banners do guia (live e grade, PT/EN/ES), hero e capa, feitos dos MODELOS REAIS: a cena é renderizada no Blender
(comum/cad/render_cena.py: os 4 robôs do repo sobre mesa de madeira, luz quente, fundo desfocado) e o texto entra
por composição (PIL), nunca por IA.

  .venv/bin/python comum/cad/banners.py fundo     # a "sala" desfocada que vai atrás da mesa (.preview/banner/fundo.png)
  .venv/bin/python comum/cad/banners.py cenas     # 3 renders pela fila de render (live, grade, hero) em .preview/banner/
  .venv/bin/python comum/cad/banners.py montar    # guia/assets/banner[-grade][-en|-es].jpg, guia/assets/hero.png, capa/capa.png
  .venv/bin/python comum/cad/banners.py tudo
  opções: --rascunho (cenas em 1/2 da resolução e poucas amostras, para conferir o enquadramento)

Textos: comum/cad/banners.textos.json (PT original; EN/ES pelo inema-traduz). Fontes: Sora (variável) e Montserrat
Black, procuradas em ~/.claude/skills/projetos-landing-guia/assets/fontes e ~/.local/share/fonts (se faltarem, cai
na DejaVu e avisa). Padrão INEMA (~/projetos/inema-design/DESIGN.md, linha Banner): fundo escuro com luz âmbar, letras
brancas + UMA palavra grande em dourado, 1400 px, um banner por idioma.
"""
import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
CAD = Path(__file__).resolve().parent
TMP = RAIZ / ".preview" / "banner"
ASSETS = RAIZ / "guia" / "assets"
TEXTOS = json.loads((CAD / "banners.textos.json").read_text())
W, H = 1400, 788
OURO = (250, 204, 21)                # #FACC15
BRANCO = (255, 255, 255)

# cena de cada saída: resolução do render (2x a final: sem denoiser, a redução limpa o ruído), largura da cena (m)
# na distância dos robôs e deslocamento do grupo no quadro
CENAS = {
    "live": dict(res=(2800, 1576), amostras=256, largura=1.62, dx=0.222, dy=-0.03, el=9, fstop=3.2),
    "grade": dict(res=(2800, 1576), amostras=256, largura=1.66, dx=0.0, dy=0.04, el=8, fstop=3.2),
    "hero": dict(res=(2700, 1800), amostras=384, largura=1.05, dx=0.0, dy=0.02, el=9, fstop=3.2),
}

# ------------------------------------------------------------------------------------------------------- fontes
_DIRS = [Path.home() / ".claude/skills/projetos-landing-guia/assets/fontes", Path.home() / ".local/share/fonts",
         Path("/usr/share/fonts/truetype/dejavu")]
_avisou = set()


def _arquivo(nome):
    for d in _DIRS:
        if (d / nome).exists():
            return str(d / nome)
    return None


def fonte(tam, peso="Bold"):
    """Sora no peso pedido (Thin, ExtraLight, Light, Regular, SemiBold, Bold, ExtraBold); 'Black' = Montserrat Black."""
    if peso == "Black":
        f = _arquivo("Montserrat-Black.ttf")
        if f:
            return ImageFont.truetype(f, tam)
    f = _arquivo("Sora.ttf")
    if f:
        ft = ImageFont.truetype(f, tam)
        try:
            ft.set_variation_by_name("ExtraBold" if peso == "Black" else peso)
        except Exception:                                    # noqa: BLE001
            pass
        return ft
    if "f" not in _avisou:
        _avisou.add("f")
        print("AVISO: fontes Sora/Montserrat não encontradas; usando DejaVu")
    return ImageFont.truetype(_arquivo("DejaVuSans-Bold.ttf") or "DejaVuSans-Bold.ttf", tam)


def largura(txt, ft, esp=0):
    return ft.getlength(txt) + esp * max(len(txt) - 1, 0)


def escreve(d, xy, txt, ft, cor, esp=0, anchor="ls"):
    """Texto com espaçamento entre letras opcional (esp em px). xy = ponto da linha de base, à esquerda."""
    if not esp:
        d.text(xy, txt, font=ft, fill=cor, anchor=anchor)
        return
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=ft, fill=cor, anchor=anchor)
        x += ft.getlength(ch) + esp


def cabe(txt, peso, tam, larg_max, esp=0, minimo=12):
    """Maior fonte <= tam em que o texto cabe em larg_max."""
    while tam > minimo and largura(txt, fonte(tam, peso), esp) > larg_max:
        tam -= 1
    return fonte(tam, peso)


def dourado(im, xy, txt, ft, brilho=18, forca=0.9):
    """Palavra grande em dourado: degradê vertical + brilho âmbar atrás. xy = linha de base à esquerda. Devolve a largura."""
    x, y = xy
    bb = ft.getbbox(txt, anchor="ls")
    w, h = bb[2] - bb[0] + 8, bb[3] - bb[1] + 8
    ox, oy = bb[0] - 4, bb[1] - 4
    masc = Image.new("L", (w, h), 0)
    ImageDraw.Draw(masc).text((-ox, -oy), txt, font=ft, fill=255, anchor="ls")
    grad = Image.new("RGB", (w, h))
    gd = ImageDraw.Draw(grad)
    paradas = [(0.0, (255, 236, 150)), (0.45, (252, 205, 40)), (0.56, (238, 160, 12)), (1.0, (255, 196, 46))]
    for j in range(h):
        t = j / max(h - 1, 1)
        for (a, ca), (b, cb) in zip(paradas, paradas[1:]):
            if a <= t <= b:
                k = (t - a) / (b - a)
                gd.line([(0, j), (w, j)], fill=tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
                break
    pad = brilho * 3
    halo = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    halo.paste(masc, (pad, pad))
    halo = halo.filter(ImageFilter.GaussianBlur(brilho)).point(lambda v: min(255, int(v * forca)))
    cor_halo = Image.new("RGB", halo.size, (255, 140, 10))
    im.paste(cor_halo, (round(x + ox - pad), round(y + oy - pad)), halo)
    im.paste(grad, (round(x + ox), round(y + oy)), masc)
    return bb[2]


def sombra_texto(im, desenha, raio=6, forca=0.75):
    """Desenha o texto (função que recebe um ImageDraw) com uma sombra escura suave por baixo, para ler sobre a cena."""
    cam = Image.new("L", im.size, 0)
    desenha(ImageDraw.Draw(cam), 255)
    sb = cam.filter(ImageFilter.GaussianBlur(raio)).point(lambda v: min(255, int(v * forca * 1.6)))
    im.paste(Image.new("RGB", im.size, (0, 0, 0)), (0, 0), sb)
    desenha(ImageDraw.Draw(im), None)


# -------------------------------------------------------------------------------------------- fundo desfocado
def fundo():
    """A sala atrás da mesa, já desfocada: parede de tijolo quente, painel de madeira, estante com objetos, luzes.
    Desenho procedural (nenhuma foto, nenhuma IA). 3200 x 960 = o plano de 8 x 2,4 m do render_cena.py; a câmera
    só enxerga o miolo (x de ~250 a ~2550, y de ~280 a ~670): o resto é margem."""
    rnd = random.Random(7)
    w, h = 3200, 960
    im = Image.new("RGB", (w, h), (30, 17, 10))
    d = ImageDraw.Draw(im)

    def claro(j):                                             # parede mais clara na faixa visível
        return max(0.0, 1 - abs(j / h - 0.47) * 2.1)

    for j in range(h):
        t = claro(j)
        d.line([(0, j), (w, j)], fill=(round(30 + 62 * t), round(16 + 30 * t), round(10 + 14 * t)))
    for j in range(0, h, 26):                                 # tijolos (viram textura depois do desfoque)
        for i in range(-60, w, 78):
            x0 = i + (39 if (j // 26) % 2 else 0)
            v = rnd.randint(-16, 16)
            t = claro(j)
            d.rectangle([x0, j, x0 + 72, j + 21], fill=(round((108 + v) * t + 20), round((52 + v // 2) * t + 11), round((32 + v // 3) * t + 7)))
    # painel de madeira escura (porta) à esquerda
    d.rectangle([0, 0, 620, h], fill=(24, 13, 8))
    d.rectangle([640, 120, 1010, h], fill=(70, 33, 13))
    for x in range(660, 1010, 60):
        d.line([(x, 120), (x, h)], fill=(42, 19, 7), width=6)
    d.rectangle([1010, 100, 1050, h], fill=(26, 13, 7))
    # estante escura com objetos à direita
    d.rectangle([1980, 0, 3200, h], fill=(27, 15, 9))
    for y in (430, 640):
        d.rectangle([2010, y, 3150, y + 18], fill=(11, 6, 4))
    for (x, y1, lw, lh, cor) in [(2040, 430, 74, 120, (156, 72, 20)), (2140, 430, 48, 92, (26, 88, 100)), (2230, 430, 96, 128, (62, 36, 19)),
                                 (2380, 430, 62, 74, (214, 122, 26)), (2480, 430, 54, 104, (100, 38, 20)), (2580, 430, 104, 88, (30, 64, 74)),
                                 (2050, 640, 112, 96, (74, 46, 25)), (2210, 640, 58, 116, (194, 98, 20)), (2310, 640, 134, 84, (24, 74, 86)),
                                 (2500, 640, 72, 104, (124, 54, 22)), (2620, 640, 84, 78, (62, 31, 14))]:
        d.rounded_rectangle([x, y1 - lh, x + lw, y1], 8, fill=cor)
    # poltrona azul-petróleo (fica quase toda atrás da mesa)
    d.rounded_rectangle([1380, 610, 1900, 960], 60, fill=(20, 66, 80))
    im = im.filter(ImageFilter.GaussianBlur(26))
    # luzes quentes (bokeh): discos de borda suave somados por cima, tamanhos e brilhos variados
    luz = Image.new("RGB", (w, h), (0, 0, 0))
    ld = ImageDraw.Draw(luz)
    for (x, y, r, cor) in [(1180, 330, 118, (255, 150, 40)), (1470, 300, 44, (255, 172, 72)), (1600, 420, 30, (255, 190, 104)),
                           (1790, 340, 58, (255, 160, 52)), (1930, 470, 34, (250, 176, 80)), (2290, 300, 46, (255, 170, 60)),
                           (1330, 500, 24, (255, 200, 124)), (820, 360, 40, (255, 150, 52)), (2460, 520, 28, (255, 190, 104)),
                           (1700, 250, 20, (255, 210, 144)), (1060, 520, 22, (255, 190, 112)), (2120, 380, 24, (255, 200, 124)),
                           (560, 420, 56, (255, 140, 36)), (380, 320, 30, (255, 170, 80)), (2650, 360, 38, (255, 176, 76))]:
        ld.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(c * rnd.uniform(0.62, 1.0)) for c in cor))
    halo = luz.filter(ImageFilter.GaussianBlur(80))
    luz = luz.filter(ImageFilter.GaussianBlur(7))
    im = ImageChops.add(im, luz.point(lambda v: int(v * 0.66)))
    im = ImageChops.add(im, halo.point(lambda v: int(v * 0.60)))
    TMP.mkdir(parents=True, exist_ok=True)
    im.save(TMP / "fundo.png")
    print("fundo:", TMP / "fundo.png")


# --------------------------------------------------------------------------------------------------- renders
def cenas(rascunho=False, quais=None):
    if not (TMP / "fundo.png").exists():
        fundo()
    fila = Path.home() / "projetos/wifi/scripts/fila-vaga"
    for nome, c in CENAS.items():
        if quais and nome not in quais:
            continue
        rw, rh = c["res"]
        am = c["amostras"]
        if rascunho:
            rw, rh, am = rw // 4 * 2, rh // 4 * 2, 24
        saida = TMP / (f"cena-{nome}" + ("-rascunho" if rascunho else "") + ".png")
        cmd = ["blender", "-b", "--python", str(CAD / "render_cena.py"), "--", str(saida), "--res", f"{rw}x{rh}",
               "--amostras", str(am), "--largura", str(c["largura"]), "--dx", str(c["dx"]), "--dy", str(c["dy"]),
               "--el", str(c["el"]), "--fstop", str(c["fstop"]), "--fundo", str(TMP / "fundo.png"), "--sem-fase2"]
        if fila.exists() and os.access(fila, os.X_OK):
            cmd = [str(fila), "render", "robos-banner", "--"] + cmd
        r = subprocess.run(cmd, capture_output=True, text=True)
        ok = r.returncode == 0 and saida.exists()
        print(("cena: " if ok else "FALHOU: ") + str(saida))
        if not ok:
            print((r.stdout + r.stderr)[-800:])
            sys.exit(1)


def cena(nome, rascunho=False):
    p = TMP / (f"cena-{nome}" + ("-rascunho" if rascunho else "") + ".png")
    return Image.open(p).convert("RGB")


def acabamento(im):
    """Vinheta leve (escurece as bordas); nada que mude a forma dos robôs."""
    w, h = im.size
    v = Image.new("L", (w, h), 0)
    ImageDraw.Draw(v).ellipse([-w * 0.18, -h * 0.30, w * 1.18, h * 1.30], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(w // 9))
    return Image.composite(im, im.point(lambda p: int(p * 0.62)), v)


def degrade_h(tam, x0, x1, a0, a1):
    """Máscara L com alfa a0 até x0, caindo linearmente até a1 em x1."""
    w, h = tam
    m = Image.new("L", (w, 1), 0)
    px = m.load()
    for x in range(w):
        t = min(1.0, max(0.0, (x - x0) / max(x1 - x0, 1)))
        t = t * t * (3 - 2 * t)
        px[x, 0] = round(255 * (a0 + (a1 - a0) * t))
    return m.resize((w, h))


def degrade_v(tam, y0, y1, a0, a1):
    w, h = tam
    m = Image.new("L", (1, h), 0)
    px = m.load()
    for y in range(h):
        t = min(1.0, max(0.0, (y - y0) / max(y1 - y0, 1)))
        t = t * t * (3 - 2 * t)
        px[0, y] = round(255 * (a0 + (a1 - a0) * t))
    return m.resize((w, h))


# ------------------------------------------------------------------------------------------------ banner live
def live(lg, rascunho=False):
    T = TEXTOS[lg]
    im = acabamento(cena("live", rascunho).resize((W, H), Image.LANCZOS))
    preto = Image.new("RGB", (W, H), (6, 5, 6))
    im.paste(preto, (0, 0), degrade_h((W, H), 330, 800, 0.93, 0.0))          # esquerda escura para o título
    im.paste(preto, (0, 0), degrade_v((W, H), 560, 788, 0.0, 0.80))          # faixa de baixo para a linha de passos
    d = ImageDraw.Draw(im)
    x0, larg = 44, 556
    # linha 1: palavra forte + palavra fina
    ft_a = fonte(92, "ExtraBold")
    ft_b = fonte(92, "Light")
    la = ft_a.getlength(T["t1a"])
    tot = la + 24 + ft_b.getlength(T["t1b"])
    if tot > larg:
        k = larg / tot
        ft_a, ft_b = fonte(int(92 * k), "ExtraBold"), fonte(int(92 * k), "Light")
        la = ft_a.getlength(T["t1a"])
    d.text((x0, 212), T["t1a"], font=ft_a, fill=BRANCO, anchor="ls")
    d.text((x0 + la + 24, 212), T["t1b"], font=ft_b, fill=BRANCO, anchor="ls")
    # linha 2: a palavra grande em dourado
    ft2 = cabe(T["t2"], "Black", 190, larg + 6)
    alt2 = -ft2.getbbox(T["t2"], anchor="ls")[1]
    y2 = 236 + alt2
    dourado(im, (x0 - 4, y2), T["t2"], ft2)
    d = ImageDraw.Draw(im)
    y = y2 + 74
    d.text((x0, y), T["sub_live"], font=cabe(T["sub_live"], "Bold", 34, larg), fill=BRANCO, anchor="ls")
    y += 46
    d.text((x0, y), T["linha"], font=cabe(T["linha"], "Light", 25, larg), fill=(236, 232, 226), anchor="ls")
    y += 34
    fio = Image.new("L", (larg, 4), 0)
    fp = fio.load()
    for x in range(larg):
        for j in range(4):
            fp[x, j] = round(255 * min(1.0, (larg - x) / (larg * 0.35)))
    im.paste(Image.new("RGB", (larg, 4), OURO), (x0, y), fio)
    d = ImageDraw.Draw(im)
    passos = "  ·  ".join(T["passos"])
    d.text((x0, 668), passos, font=cabe(passos, "Regular", 22, W - 2 * x0), fill=(240, 236, 230), anchor="ls")
    d.text((x0, 742), T["pe"], font=fonte(21, "Regular"), fill=(232, 228, 222), anchor="ls")
    return im


# ----------------------------------------------------------------------------------------------- ícones (grade)
def icone(n, tam=64, cor=OURO):
    """Ícones de traço dourado, desenhados à mão (4x e reduzidos): 0 escolher, 1 imprimir, 2 servo, 3 casca,
    4 cabeça que vira, 5 pronto."""
    s = 4
    t = tam * s
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    e = max(3 * s, round(tam * s * 0.042))        # traço ~4 % do tamanho

    def L(pts, fecha=False):
        pts = [(x * t, y * t) for x, y in pts]
        d.line(pts + ([pts[0]] if fecha else []), fill=cor, width=e, joint="curve")
        for p in pts:
            d.ellipse([p[0] - e / 2, p[1] - e / 2, p[0] + e / 2, p[1] + e / 2], fill=cor)

    def R(x0, y0, x1, y1, r=0.06):
        d.rounded_rectangle([x0 * t, y0 * t, x1 * t, y1 * t], r * t, outline=cor, width=e)

    def C(cx, cy, r, cheio=False):
        d.ellipse([(cx - r) * t, (cy - r) * t, (cx + r) * t, (cy + r) * t], outline=cor, width=e, fill=cor if cheio else None)

    if n == 0:                                   # escolher: um bicho (cabeça com orelhas) e um cubo com tela
        C(0.28, 0.44, 0.20)
        C(0.13, 0.22, 0.07)
        C(0.43, 0.22, 0.07)
        C(0.22, 0.42, 0.022, True)
        C(0.34, 0.42, 0.022, True)
        R(0.56, 0.44, 0.94, 0.82, 0.07)
        R(0.64, 0.52, 0.86, 0.68, 0.03)
        L([(0.10, 0.92), (0.46, 0.92)])
    elif n == 1:                                 # impressora: pórtico, bico e a peça nascendo em camadas
        L([(0.12, 0.88), (0.12, 0.12), (0.88, 0.12), (0.88, 0.88)])
        L([(0.40, 0.12), (0.40, 0.30), (0.50, 0.42), (0.60, 0.30), (0.60, 0.12)])
        L([(0.34, 0.58), (0.66, 0.58)])
        L([(0.30, 0.68), (0.70, 0.68)])
        L([(0.26, 0.78), (0.74, 0.78)])
        L([(0.04, 0.90), (0.96, 0.90)])
    elif n == 2:                                 # servo: corpo com as duas orelhas de fixação, eixo e braço
        R(0.22, 0.34, 0.78, 0.90, 0.05)
        L([(0.06, 0.48), (0.22, 0.48)])
        L([(0.78, 0.48), (0.94, 0.48)])
        C(0.50, 0.34, 0.11)
        L([(0.50, 0.34), (0.78, 0.10)])
        C(0.78, 0.10, 0.03, True)
    elif n == 3:                                 # casca: as duas metades fechando sobre o miolo
        d.arc([0.12 * t, 0.10 * t, 0.88 * t, 0.86 * t], 180, 360, fill=cor, width=e)
        L([(0.12, 0.48), (0.12, 0.40)])
        L([(0.88, 0.48), (0.88, 0.40)])
        d.arc([0.12 * t, 0.26 * t, 0.88 * t, 1.02 * t], 20, 160, fill=cor, width=e)
        L([(0.50, 0.30), (0.50, 0.60)])
        L([(0.40, 0.50), (0.50, 0.60), (0.60, 0.50)])
    elif n == 4:                                 # cabeça-cubo com dois olhos e setas de giro para os dois lados
        R(0.28, 0.30, 0.72, 0.74, 0.09)
        C(0.41, 0.50, 0.035, True)
        C(0.59, 0.50, 0.035, True)
        L([(0.22, 0.40), (0.08, 0.52), (0.22, 0.64)])
        L([(0.78, 0.40), (0.92, 0.52), (0.78, 0.64)])
        L([(0.40, 0.86), (0.60, 0.86)])
    else:                                        # pronto: círculo com visto
        C(0.50, 0.50, 0.40)
        L([(0.30, 0.52), (0.45, 0.66), (0.72, 0.36)])
    return im.resize((tam, tam), Image.LANCZOS)


def quebra2(txt, ft, larg):
    """Quebra em até 2 linhas equilibradas, se não couber em uma."""
    if ft.getlength(txt) <= larg:
        return [txt]
    ps = txt.split(" ")
    melhor = None
    for i in range(1, len(ps)):
        a, b = " ".join(ps[:i]), " ".join(ps[i:])
        pior = max(ft.getlength(a), ft.getlength(b))
        if melhor is None or pior < melhor[0]:
            melhor = (pior, [a, b])
    return melhor[1]


# ----------------------------------------------------------------------------------------------- banner grade
def grade(lg, rascunho=False):
    T = TEXTOS[lg]
    im = acabamento(cena("grade", rascunho).resize((W, H), Image.LANCZOS))
    preto = Image.new("RGB", (W, H), (6, 5, 6))
    im.paste(preto, (0, 0), degrade_v((W, H), 0, 215, 0.86, 0.0))            # topo escuro para o título
    im.paste(preto, (0, 0), degrade_v((W, H), 492, 566, 0.0, 0.90))          # base escura para os cartões
    # título numa linha: parte branca + palavra dourada
    branca = f'{T["t1a"]} {T["t1b"]}'
    tam = 92
    while True:
        fa, fb = fonte(tam, "ExtraBold"), fonte(tam, "Black")
        tot = fa.getlength(branca) + tam * 0.30 + fb.getlength(T["t2"])
        if tot <= W - 240 or tam <= 40:
            break
        tam -= 2
    x = (W - tot) / 2
    yb = 108
    ImageDraw.Draw(im).text((x, yb), branca, font=fa, fill=BRANCO, anchor="ls")
    dourado(im, (x + fa.getlength(branca) + tam * 0.30, yb), T["t2"], fb, brilho=14, forca=0.8)
    d = ImageDraw.Draw(im)
    fs = cabe(T["sub_grade"], "Bold", 30, W - 120)
    d.text((W / 2, 152), T["sub_grade"], font=fs, fill=BRANCO, anchor="ms")
    fl = cabe(T["linha"], "Light", 23, W - 300)
    d.text((W / 2, 186), T["linha"], font=fl, fill=(236, 232, 226), anchor="ms")
    lw = fl.getlength(T["linha"])
    for (xa, xb) in ((W / 2 - lw / 2 - 190, W / 2 - lw / 2 - 22), (W / 2 + lw / 2 + 22, W / 2 + lw / 2 + 190)):
        d.line([(xa, 178), (xb, 178)], fill=OURO, width=2)
    # 6 cartões
    n, mx, vao = 6, 56, 14
    cw = (W - 2 * mx - (n - 1) * vao) / n
    y0, y1 = 512, 674
    ft_c = fonte(23, "Bold")
    for i, txt in enumerate(T["passos"]):
        xa = mx + i * (cw + vao)
        cart = Image.new("RGBA", (round(cw), y1 - y0), (0, 0, 0, 0))
        cd = ImageDraw.Draw(cart)
        cd.rounded_rectangle([0, 0, round(cw) - 1, y1 - y0 - 1], 14, fill=(14, 11, 9, 205), outline=(250, 204, 21, 235), width=2)
        im.paste(cart, (round(xa), y0), cart)
        ic = icone(i, 76)
        im.paste(ic, (round(xa + cw / 2 - 38), y0 + 12), ic)
        linhas = quebra2(txt, ft_c, cw - 22)
        f = ft_c
        if max(ft_c.getlength(l) for l in linhas) > cw - 16:
            f = cabe(max(linhas, key=len), "Bold", 23, cw - 16)
        d = ImageDraw.Draw(im)
        yy = y0 + 117 if len(linhas) == 2 else y0 + 131
        for l in linhas:
            d.text((xa + cw / 2, yy), l, font=f, fill=BRANCO, anchor="ms")
            yy += 27
    # faixa do rodapé
    fx = Image.new("RGBA", (W - 2 * mx, 58), (0, 0, 0, 0))
    ImageDraw.Draw(fx).rounded_rectangle([0, 0, W - 2 * mx - 1, 57], 14, fill=(10, 8, 7, 225), outline=(250, 204, 21, 235), width=2)
    im.paste(fx, (mx, 704), fx)
    fp_ = fonte(30, "Bold")
    partes = [p.strip() for p in T["pe"].split("·")]
    vao_p = 34
    tot = sum(fp_.getlength(p) for p in partes) + vao_p * (len(partes) - 1)
    d = ImageDraw.Draw(im)
    xx = (W - tot) / 2
    for i, p in enumerate(partes):
        d.text((xx, 733), p, font=fp_, fill=BRANCO, anchor="lm")
        xx += fp_.getlength(p)
        if i < len(partes) - 1:
            d.ellipse([xx + vao_p / 2 - 5, 733 - 4, xx + vao_p / 2 + 5, 733 + 6], fill=OURO)
            xx += vao_p
    return im


# ------------------------------------------------------------------------------------------------ hero e capa
def hero(rascunho=False):
    return acabamento(cena("hero", rascunho).resize((1800, 1200), Image.LANCZOS))


def capa(rascunho=False):
    """Capa 1280 x 720 no desenho da anterior: marca + selo + título à esquerda, cartão com a cena real à direita."""
    T = TEXTOS["capa"]
    cw, ch = 1280, 720
    im = Image.new("RGB", (cw, ch), (12, 12, 16))                     # #0c0c10
    brilho = Image.new("RGB", (cw, ch), (0, 0, 0))
    ImageDraw.Draw(brilho).ellipse([760, -200, 1500, 420], fill=(64, 44, 16))
    ImageDraw.Draw(brilho).ellipse([-300, 480, 420, 1000], fill=(16, 26, 36))
    im = ImageChops.add(im, brilho.filter(ImageFilter.GaussianBlur(170)))
    # cartão com a cena (recorte 4:3 do hero, centrado nos robôs)
    h_ = hero(rascunho)
    rw, rh = 1500, 1125
    rec = h_.crop(((1800 - rw) // 2, 1200 - rh - 30, (1800 - rw) // 2 + rw, 1200 - 30)).resize((600, 450), Image.LANCZOS)
    masc = Image.new("L", (600, 450), 0)
    ImageDraw.Draw(masc).rounded_rectangle([0, 0, 599, 449], 22, fill=255)
    sb = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(sb).rounded_rectangle([628, 148, 1228, 598], 22, fill=150)
    im.paste(Image.new("RGB", (cw, ch), (0, 0, 0)), (0, 0), sb.filter(ImageFilter.GaussianBlur(26)))
    im.paste(rec, (624, 135), masc)
    ImageDraw.Draw(im).rounded_rectangle([624, 135, 1223, 584], 22, outline=(52, 46, 38), width=2)
    d = ImageDraw.Draw(im)
    fm = fonte(22, "ExtraBold")
    escreve(d, (60, 307), T["marca"], fm, BRANCO, esp=3)
    xm = 60 + largura(T["marca"], fm, 3) + 3
    escreve(d, (xm, 307), T["marca2"], fm, OURO, esp=3)
    xs = xm + largura(T["marca2"], fm, 3) + 16
    fsel = fonte(15, "ExtraBold")
    ls = largura(T["selo"], fsel, 1.5)
    d.rounded_rectangle([xs, 283, xs + ls + 28, 314], 15.5, fill=OURO)
    escreve(d, (xs + 14, 304), T["selo"], fsel, (26, 18, 6), esp=1.5)
    d.text((58, 392), T["titulo"], font=cabe(T["titulo"], "ExtraBold", 62, 540), fill=BRANCO, anchor="ls")
    d.rounded_rectangle([60, 430, 140, 436], 3, fill=OURO)
    return im


def montar(rascunho=False):
    destino = TMP / "rascunho" if rascunho else None
    if destino:
        destino.mkdir(parents=True, exist_ok=True)
    for lg in ("pt", "en", "es"):
        suf = "" if lg == "pt" else f"-{lg}"
        for nome, f in ((f"banner{suf}.jpg", live), (f"banner-grade{suf}.jpg", grade)):
            p = (destino or ASSETS) / nome
            f(lg, rascunho).save(p, quality=90, optimize=True, progressive=True)
            print(p, os.path.getsize(p) // 1024, "KB")
    p = (destino or ASSETS) / "hero.png"
    hero(rascunho).save(p, optimize=True)
    print(p, os.path.getsize(p) // 1024, "KB")
    p = (destino or (RAIZ / "capa")) / "capa.png"
    capa(rascunho).save(p, optimize=True)
    print(p, os.path.getsize(p) // 1024, "KB")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    rasc = "--rascunho" in sys.argv
    cmd = a[0] if a else "tudo"
    if cmd in ("fundo", "tudo"):
        fundo()
    if cmd in ("cenas", "tudo"):
        cenas(rasc, a[1:] or None)
    if cmd in ("montar", "tudo"):
        montar(rasc)
