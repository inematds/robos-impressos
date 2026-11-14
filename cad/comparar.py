#!/usr/bin/env python3
"""Régua de semelhança: silhueta do NOSSO modelo × silhueta da imagem de referência (IoU por vista).

Uso (venv do repo):
  .venv/bin/python cad/comparar.py <modelo> [--pecas <pasta com montagem.json>] [--rotulo antes|depois|...]
  .venv/bin/python cad/comparar.py dino --malha referencia/malhas/dino-x.glb --cima +y --frente +z --rotulo malha-x
  .venv/bin/python cad/comparar.py --tabela            # só refaz comparacao/semelhanca.md a partir do JSON

<modelo> = dino | capivara | cubo | cubo_rodas (ou cubo-rodas) | qualquer nome novo com --referencia.
A referência é escolhida pelo começo do nome (cubo_rodas usa a do cubo) ou por --referencia.

O que faz, por vista da referência:
  1. lê a máscara de silhueta da referência (PNG em referencia/mascaras/, feita UMA vez: ver --mascaras);
  2. monta o modelo a partir de montagem.json + STL: peças impressas + rodas/esfera (sem os outros componentes,
     sem fase 2), na pose neutra;
  3. projeta (ortográfica) e procura o melhor azimute/elevação numa vizinhança do ângulo nominal da vista;
  4. alinha (mesma altura, base na mesma linha, centrado na horizontal) e calcula o IoU das duas máscaras.
Grava: comparacao/semelhanca.json + .md (números, entram no repo) e referencia/comparacao/<modelo>-<rotulo>.png
(referência | nosso modelo | sobreposição; contém a imagem do dono, NÃO entra no repo).

Ângulos (iguais aos do cad/render_blender.py): azimute 0 = câmera na frente (+Y) olhando o rosto; azimute
positivo = câmera indo para o lado +X (o bicho aparece olhando para a DIREITA da imagem); negativo = olhando para
a ESQUERDA. Elevação = câmera acima do horizonte.

As máscaras da referência (--mascaras) precisam de rembg, que NÃO está no venv do repo de propósito:
  .venv-i23d/bin/python cad/comparar.py --mascaras [dino|capivara|cubo]
Elas ficam em cache e a régua nunca as refaz sozinha (trocar a máscara muda todos os números).
"""
import argparse
import datetime
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_REF = os.path.join(RAIZ, "referencia")
DIR_MASC = os.path.join(DIR_REF, "mascaras")
DIR_REC = os.path.join(DIR_REF, "recortes")
DIR_LADO = os.path.join(DIR_REF, "comparacao")
DIR_TAB = os.path.join(RAIZ, "comparacao")
ARQ_JSON = os.path.join(DIR_TAB, "semelhanca.json")
ARQ_MD = os.path.join(DIR_TAB, "semelhanca.md")

# ---------------------------------------------------------------------------------------------------------------
# PROTOCOLO (congelado: mexer aqui muda todos os números; se mudar, suba "versao" e rode tudo de novo)
# ---------------------------------------------------------------------------------------------------------------
PROTOCOLO = {
    "versao": 1,
    "projecao": "ortografica",
    "altura_px": 400,                      # as duas silhuetas são levadas a esta altura
    "busca_az_graus": 25,                  # nominal ± isto
    "passo_az_graus": 5,
    "busca_el_graus": [-10, -5, 0, 5, 10],  # nominal + cada um (mínimo 0)
    "alinhamento": "caixa da silhueta: mesma altura, base na mesma linha, centro horizontal coincidente",
    "iou_ajustado": "secundario: melhor IoU com escala 0,88–1,12 e deslocamento de ate 12% (x) e 6% (y) da altura",
    "pecas": "pecas impressas (todas as copias de para_montagem) + componentes roda*/esfera*; sem fase 2; pose neutra",
}
COMPONENTES_VISIVEIS = re.compile(r"^(roda|esfera|pneu)", re.I)

# Recortes em pixels (x0, y0, x1, y1) na folha original; az/el nominais de cada vista (ver docstring).
# Os nominais foram estimados A OLHO nas folhas (fotos em perspectiva, de cima); a busca acha o melhor em volta.
# As 4 vistas do dino NÃO incluem costas; a cabeça muda de pose entre as vistas (a régua usa sempre a pose neutra).
# "apaga": retângulos (x0, y0, x1, y1) no recorte, apagados da máscara à mão (sombra/mesa), se preciso.
REFERENCIAS = {
    "dino": {
        "arquivo": "dino-4-angulos.png",
        "metodo": "rembg",
        "vistas": [
            {"nome": "frente", "recorte": [0, 0, 622, 622], "az": 0, "el": 15},
            {"nome": "tres-quartos-a", "recorte": [632, 0, 1254, 622], "az": -45, "el": 15},
            {"nome": "tres-quartos-b", "recorte": [0, 632, 622, 1254], "az": -40, "el": 15},
            {"nome": "lado", "recorte": [632, 632, 1254, 1254], "az": -75, "el": 15},
        ],
    },
    "capivara": {
        "arquivo": "capivara-4-vistas.png",
        "metodo": "rembg",
        "vistas": [
            {"nome": "frente", "recorte": [0, 0, 651, 598], "az": 0, "el": 15},
            {"nome": "tres-quartos", "recorte": [661, 0, 1312, 598], "az": -45, "el": 15},
            {"nome": "lado", "recorte": [0, 606, 651, 1199], "az": -80, "el": 15},
            {"nome": "costas", "recorte": [661, 606, 1312, 1199], "az": 180, "el": 15},
        ],
    },
    "cubo": {
        "arquivo": "robo-quadrado.png",
        "metodo": "fundo-branco",
        "vistas": [
            {"nome": "tres-quartos", "recorte": [0, 0, 220, 220], "az": 35, "el": 22},
        ],
    },
}


def referencia_de(modelo, forcada=None):
    if forcada:
        if forcada not in REFERENCIAS:
            sys.exit(f"referência desconhecida: {forcada} (tenho {', '.join(REFERENCIAS)})")
        return forcada
    for nome in sorted(REFERENCIAS, key=len, reverse=True):
        if modelo.lower().startswith(nome):
            return nome
    sys.exit(f"não sei qual referência usar para '{modelo}': passe --referencia {'|'.join(REFERENCIAS)}")


def pasta_pecas(modelo, dada=None):
    if dada:
        p = dada if os.path.isabs(dada) else os.path.join(os.getcwd(), dada)
        if os.path.isfile(os.path.join(p, "montagem.json")):
            return p
        sys.exit(f"não achei montagem.json em {p}")
    for nome in dict.fromkeys([modelo, modelo.replace("_", "-"), modelo.replace("-", "_")]):
        for base in ("pecas", "projetos"):
            for p in (os.path.join(RAIZ, base, nome), os.path.join(RAIZ, base, nome, "pecas")):
                if os.path.isfile(os.path.join(p, "montagem.json")):
                    return p
    sys.exit(f"não achei montagem.json do modelo '{modelo}': passe --pecas <pasta>")


# ---------------------------------------------------------------------------------------------------------------
# geometria
# ---------------------------------------------------------------------------------------------------------------
def carrega_modelo(pasta):
    """Devolve (tris (N,3,3) em mm, cores (N,3) 0..1, tris simplificados para a busca, nomes que entraram)."""
    import trimesh

    cena = json.load(open(os.path.join(pasta, "montagem.json")))
    itens = [(it, False) for it in cena.get("pecas", [])]
    itens += [(it, True) for it in cena.get("componentes", [])
              if COMPONENTES_VISIVEIS.search(it.get("nome", "")) and not it.get("fase2")]
    tris, cores, leves, nomes = [], [], [], []
    for it, eh_comp in itens:
        if not it.get("para_montagem"):
            continue
        m = trimesh.load(os.path.join(pasta, it["arquivo"]), force="mesh", process=False)
        v, f = np.asarray(m.vertices, float), np.asarray(m.faces)
        vl, fl = _simplifica(v, f)
        for M in it["para_montagem"]:
            M = np.asarray(M, float)
            tris.append((v @ M[:3, :3].T + M[:3, 3])[f])
            leves.append((vl @ M[:3, :3].T + M[:3, 3])[fl])
            cores.append(np.tile(np.asarray(it.get("rgb", [0.6, 0.6, 0.6]), float)[:3], (len(f), 1)))
        nomes.append(("componente " if eh_comp else "") + it["nome"] + f" x{len(it['para_montagem'])}")
    if not tris:
        sys.exit(f"nenhuma peça em {pasta}")
    return np.concatenate(tris), np.concatenate(cores), np.concatenate(leves), nomes


def carrega_malha(arquivo, cima, frente):
    """Malha avulsa (glb/obj/stl) → nossos eixos (X lados, +Y frente, Z cima, chão em Z=0)."""
    import trimesh

    m = trimesh.load(arquivo, force="mesh", process=False)
    v, f = np.asarray(m.vertices, float), np.asarray(m.faces)
    R = np.array([np.cross(_eixo(frente), _eixo(cima)), _eixo(frente), _eixo(cima)])
    v = v @ R.T
    v[:, 2] -= v[:, 2].min()
    v[:, :2] -= (v[:, :2].min(0) + v[:, :2].max(0)) / 2
    vl, fl = _simplifica(v, f)
    cores = np.tile(np.array([0.55, 0.57, 0.6]), (len(f), 1))
    return v[f], cores, vl[fl], [os.path.basename(arquivo) + f" ({len(f)} triângulos, cima {cima}, frente {frente})"]


def _eixo(txt):
    t = txt.strip().lower()
    s = -1.0 if t.startswith("-") else 1.0
    e = np.zeros(3)
    e["xyz".index(t.lstrip("+-"))] = s
    return e


def _simplifica(v, f, alvo=6000):
    if len(f) <= alvo:
        return v, f
    try:
        import fast_simplification

        vl, fl = fast_simplification.simplify(v.astype(np.float32), f.astype(np.int32), target_count=alvo)
        if len(fl) > 100:
            return np.asarray(vl, float), np.asarray(fl)
    except Exception:
        pass
    return v, f


def camera(az, el):
    a, e = math.radians(az), math.radians(el)
    olho = np.array([math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)])   # do centro para a câmera
    direita = np.array([-math.cos(a), math.sin(a), 0.0])
    cima = np.array([-math.sin(a) * math.sin(e), -math.cos(a) * math.sin(e), math.cos(e)])
    return olho, direita, cima


def silhueta(tris, az, el, altura):
    """Máscara booleana da projeção ortográfica, recortada na própria caixa, com `altura` pixels de altura."""
    _, direita, cima = camera(az, el)
    x, y = tris @ direita, tris @ cima
    esc = (altura - 1) / max(y.max() - y.min(), 1e-9)
    px, py = (x - x.min()) * esc + 1.0, (y.max() - y) * esc + 1.0
    im = Image.new("L", (int(math.ceil(px.max())) + 3, altura + 2), 0)
    d = ImageDraw.Draw(im)
    for t in np.stack([px, py], -1).reshape(-1, 6).tolist():
        d.polygon(t, fill=255, outline=255)
    return normaliza(np.asarray(im) > 0, altura)


def pinta(tris, cores, az, el, altura, ss=2):
    """Render simples (sombreado plano, ordem de profundidade) na MESMA câmera da silhueta. Devolve imagem RGB."""
    olho, direita, cima = camera(az, el)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    vis = n @ olho > 0
    x, y = tris @ direita, tris @ cima
    H = altura * ss
    esc = (H - 1) / max(y.max() - y.min(), 1e-9)
    x0, y1 = x.min(), y.max()
    luz = olho + 0.55 * cima + 0.45 * direita
    luz /= np.linalg.norm(luz)
    tom = 0.42 + 0.58 * np.clip(n @ luz, 0, 1)
    rgb = (np.clip(cores, 0, 1) ** (1 / 2.2)) * tom[:, None]
    ordem = np.argsort((tris @ olho).mean(1))
    ordem = ordem[vis[ordem]]
    px, py = (x - x0) * esc + ss, (y1 - y) * esc + ss
    im = Image.new("RGB", (int(math.ceil(px.max())) + 2 * ss, H + 2 * ss), (255, 255, 255))
    d = ImageDraw.Draw(im)
    pts = np.stack([px, py], -1).reshape(-1, 6)
    c8 = (rgb * 255).astype(np.uint8)
    for i in ordem.tolist():
        cor = tuple(c8[i].tolist())
        d.polygon(pts[i].tolist(), fill=cor, outline=cor)
    return im.resize((max(1, im.width // ss), max(1, im.height // ss)), Image.LANCZOS)


# ---------------------------------------------------------------------------------------------------------------
# máscaras e IoU
# ---------------------------------------------------------------------------------------------------------------
def normaliza(m, altura):
    """Recorta na caixa da silhueta e leva para `altura` pixels de altura (largura proporcional)."""
    ys, xs = np.where(m)
    if len(ys) == 0:
        return np.zeros((altura, 1), bool)
    m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    w = max(1, int(round(m.shape[1] * altura / m.shape[0])))
    return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((w, altura), Image.BILINEAR)) > 127


def _no_quadro(m, W, H, dx=0, dy=0):
    """Põe a máscara num quadro W×H: centro horizontal no meio (+dx), base na base (+dy)."""
    q = np.zeros((H, W), bool)
    h, w = m.shape
    x0, y0 = (W - w) // 2 + dx, H - h + dy
    ax0, ay0, ax1, ay1 = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if ax1 > ax0 and ay1 > ay0:
        q[ay0:ay1, ax0:ax1] = m[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0]
    return q


def iou_fixo(ref, nos):
    """IoU principal: as duas na mesma altura, base na mesma linha, centro horizontal da caixa coincidente."""
    W, H = max(ref.shape[1], nos.shape[1]), max(ref.shape[0], nos.shape[0])
    a, b = _no_quadro(ref, W, H), _no_quadro(nos, W, H)
    return float((a & b).sum() / max((a | b).sum(), 1)), a, b


def iou_ajustado(ref, nos):
    """IoU secundário: deixa escala e posição do nosso modelo variarem um pouco (ver PROTOCOLO)."""
    H0 = ref.shape[0]
    W, H = int(max(ref.shape[1], nos.shape[1]) * 1.5) + 8, int(H0 * 1.25)
    a = _no_quadro(ref, W, H, dy=-int(H0 * 0.1))
    melhor = (0.0, 1.0, 0, 0)
    dxs = [int(round(H0 * k / 100)) for k in range(-12, 13, 2)]
    dys = [int(round(H0 * k / 100)) for k in range(-6, 7, 2)]
    for s in np.linspace(0.88, 1.12, 9):
        h = max(2, int(round(H0 * s)))
        w = max(1, int(round(nos.shape[1] * s)))
        b0 = np.asarray(Image.fromarray((nos * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)) > 127
        for dx in dxs:
            for dy in dys:
                b = _no_quadro(b0, W, H, dx=dx, dy=dy - int(H0 * 0.1))
                v = (a & b).sum() / max((a | b).sum(), 1)
                if v > melhor[0]:
                    melhor = (float(v), float(s), dx, dy)
    return melhor


def le_mascara(ref, vista):
    arq = os.path.join(DIR_MASC, f"{ref}-{vista['nome']}.png")
    if not os.path.isfile(arq):
        sys.exit(f"falta a máscara {arq}\n  gere uma vez: .venv-i23d/bin/python cad/comparar.py --mascaras {ref}")
    m = np.asarray(Image.open(arq).convert("L")) > 127
    ys, xs = np.where(m)
    borda = bool(ys.min() <= 1 or xs.min() <= 1 or ys.max() >= m.shape[0] - 2 or xs.max() >= m.shape[1] - 2)
    return m, borda


def gera_mascaras(quais, modelo_rembg, forcar):
    """Recorta as vistas e tira o fundo LOCALMENTE (rembg). Roda com .venv-i23d (tem rembg); cache para sempre."""
    from scipy import ndimage

    sessao = None
    for d in (DIR_MASC, DIR_REC):
        os.makedirs(d, exist_ok=True)
    for ref in quais:
        cfg = REFERENCIAS[ref]
        folha = Image.open(os.path.join(DIR_REF, cfg["arquivo"])).convert("RGB")
        for v in cfg["vistas"]:
            arq = os.path.join(DIR_MASC, f"{ref}-{v['nome']}.png")
            if os.path.isfile(arq) and not forcar:
                print(f"já existe (não refaço sem --forcar): {arq}")
                continue
            rec = folha.crop(tuple(v["recorte"]))
            rec.save(os.path.join(DIR_REC, f"{ref}-{v['nome']}.png"))
            if cfg["metodo"] == "fundo-branco":
                a = np.asarray(rec).astype(int)
                m = (a.max(2) < 232) | ((a.max(2) - a.min(2)) > 30)
                m = ndimage.binary_opening(m, np.ones((3, 3), bool))      # some com as linhas de cota (1 px)
            else:
                from rembg import new_session, remove

                sessao = sessao or new_session(modelo_rembg)
                m = np.asarray(remove(rec, session=sessao, only_mask=True).convert("L")) > 127
            for x0, y0, x1, y1 in v.get("apaga", []):
                m[y0:y1, x0:x1] = False
            rot, n = ndimage.label(m)
            if n > 1:
                m = rot == (1 + int(np.argmax(ndimage.sum(m, rot, range(1, n + 1)))))
            if cfg["metodo"] == "fundo-branco":
                m = ndimage.binary_fill_holes(m)
            Image.fromarray((m * 255).astype(np.uint8)).save(arq)
            rgba = np.dstack([np.asarray(rec), (m * 255).astype(np.uint8)])
            Image.fromarray(rgba, "RGBA").save(os.path.join(DIR_REC, f"{ref}-{v['nome']}-rgba.png"))
            # conferência a olho: recorte com o que NÃO é máscara escurecido e o contorno em magenta
            a = np.asarray(rec).astype(float)
            a[~m] = a[~m] * 0.35 + 40
            a[m ^ ndimage.binary_erosion(m, iterations=2)] = (255, 0, 255)
            Image.fromarray(a.astype(np.uint8)).save(os.path.join(DIR_MASC, f"{ref}-{v['nome']}-confere.jpg"))
            print(f"ok {arq}  ({int(m.sum())} px)")


# ---------------------------------------------------------------------------------------------------------------
# medição
# ---------------------------------------------------------------------------------------------------------------
def mede(ref, tris, tris_leves, espelha=False, busca_az=None):
    H = PROTOCOLO["altura_px"]
    baz = PROTOCOLO["busca_az_graus"] if busca_az is None else busca_az
    passo = PROTOCOLO["passo_az_graus"]
    saida = []
    for v in REFERENCIAS[ref]["vistas"]:
        bruta, borda = le_mascara(ref, v)
        mref = normaliza(bruta, H)
        az0 = -v["az"] if espelha else v["az"]
        melhor = (-1.0, az0, v["el"])
        for daz in range(-baz, baz + 1, passo):
            for d_el in PROTOCOLO["busca_el_graus"]:
                az, el = az0 + daz, max(0, v["el"] + d_el)
                val = iou_fixo(mref, silhueta(tris_leves, az, el, H))[0]
                if val > melhor[0]:
                    melhor = (val, az, el)
        _, az, el = melhor
        nos = silhueta(tris, az, el, H)
        val, a, b = iou_fixo(mref, nos)
        aj = iou_ajustado(mref, nos)
        if aj[0] < val:                     # a grade do ajuste não contém exatamente o alinhamento fixo
            aj = (val, 1.0, 0, 0)
        saida.append({
            "vista": v["nome"], "az_nominal": az0, "el_nominal": v["el"], "az": az, "el": el,
            "iou": round(val, 4), "iou_ajustado": round(aj[0], 4), "ajuste_escala": round(aj[1], 3),
            "mascara_toca_borda": borda, "az_no_limite_da_busca": abs(az - az0) >= baz,
            "el_no_limite_da_busca": abs(el - v["el"]) >= max(PROTOCOLO["busca_el_graus"]),
            "_a": a, "_b": b,
        })
        print(f"  {v['nome']:<16} az {az:>5}°  el {el:>3}°  IoU {val:.3f}  (ajustado {aj[0]:.3f})"
              + ("  [máscara toca a borda]" if borda else "") + ("  [az no limite da busca]" if abs(az - az0) >= baz else "")
              + ("  [el no limite da busca]" if abs(el - v["el"]) >= max(PROTOCOLO["busca_el_graus"]) else ""))
    return saida


def _fonte(tam):
    for arq in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"):
        if os.path.isfile(arq):
            return ImageFont.truetype(arq, tam)
    return ImageFont.load_default()


def _cabe(im, lado):
    k = min(lado / im.width, lado / im.height)
    im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    q = Image.new("RGB", (lado, lado), (255, 255, 255))
    q.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return q


def lado_a_lado(ref, modelo, rotulo, vistas, tris, cores, arquivo, eh_malha=False):
    C, M, T = 400, 14, 46
    f1, f2 = _fonte(20), _fonte(15)
    folha_ref = Image.open(os.path.join(DIR_REF, REFERENCIAS[ref]["arquivo"])).convert("RGB")
    n = len(vistas)
    W, Ht = 3 * C + 4 * M, 64 + n * (C + T) + 40
    g = Image.new("RGB", (W, Ht), (255, 255, 255))
    d = ImageDraw.Draw(g)
    media = sum(v["iou"] for v in vistas) / n
    d.text((M, 10), f"{modelo} · {rotulo} · IoU médio {media:.3f}".replace(".", ","), fill=(0, 0, 0), font=f1)
    meio = "malha do image-to-3D (mesma câmera)" if eh_malha else "nosso modelo (mesma câmera)"
    for k, t in enumerate(("referência", meio, "silhuetas sobrepostas")):
        d.text((M + k * (C + M), 40), t, fill=(90, 90, 90), font=f2)
    for i, (cfg, v) in enumerate(zip(REFERENCIAS[ref]["vistas"], vistas)):
        y = 64 + i * (C + T)
        g.paste(_cabe(folha_ref.crop(tuple(cfg["recorte"])), C), (M, y))
        g.paste(_cabe(pinta(tris, cores, v["az"], v["el"], C), C), (2 * M + C, y))
        a, b = v["_a"], v["_b"]
        s = np.full(a.shape + (3,), 255, np.uint8)
        s[a & ~b] = (226, 74, 74)       # só a referência
        s[b & ~a] = (66, 112, 232)      # só o nosso
        s[a & b] = (150, 205, 150)      # os dois
        g.paste(_cabe(Image.fromarray(s), C), (3 * M + 2 * C, y))
        txt = (f"{v['vista']} · az {v['az']}° el {v['el']}° (nominal {v['az_nominal']}°/{v['el_nominal']}°) · "
               f"IoU {v['iou']:.3f} · ajustado {v['iou_ajustado']:.3f}").replace(".", ",")
        d.text((M, y + C + 8), txt, fill=(0, 0, 0), font=f2)
    yl = Ht - 30
    for k, (cor, t) in enumerate((((226, 74, 74), "só na referência"), ((66, 112, 232), "só na malha" if eh_malha else "só no nosso"),
                                  ((150, 205, 150), "nos dois"))):
        d.rectangle((M + k * 230, yl, M + k * 230 + 18, yl + 18), fill=cor)
        d.text((M + k * 230 + 26, yl), t, fill=(0, 0, 0), font=f2)
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    g.save(arquivo)


# ---------------------------------------------------------------------------------------------------------------
# tabela (JSON com merge + Markdown)
# ---------------------------------------------------------------------------------------------------------------
def grava_tabela(modelo=None, rotulo=None, registro=None):
    os.makedirs(DIR_TAB, exist_ok=True)
    dados = json.load(open(ARQ_JSON)) if os.path.isfile(ARQ_JSON) else {}
    dados["protocolo"] = PROTOCOLO
    dados["angulos_nominais"] = {r: [{k: v[k] for k in ("nome", "recorte", "az", "el")} for v in c["vistas"]]
                                 for r, c in REFERENCIAS.items()}
    dados.setdefault("resultados", {})
    if registro:
        dados["resultados"].setdefault(modelo, {})[rotulo] = registro
    json.dump(dados, open(ARQ_JSON, "w"), ensure_ascii=False, indent=1)
    L = ["# Semelhança com as imagens de referência (IoU de silhueta)", "",
         "Gerado por `cad/comparar.py` (não edite à mão). IoU = área comum ÷ área total das duas silhuetas, "
         "de 0 a 1: quanto maior, mais parecido o contorno. Mede só o CONTORNO em cada vista, não cor nem detalhe.",
         "",
         f"Protocolo v{PROTOCOLO['versao']}: projeção ortográfica, silhuetas com {PROTOCOLO['altura_px']} px de "
         f"altura, base na mesma linha e centro horizontal coincidente; melhor azimute em nominal ± "
         f"{PROTOCOLO['busca_az_graus']}° (passo {PROTOCOLO['passo_az_graus']}°) e elevação em nominal ± 10° "
         "(passo 5°). Entram as peças impressas + rodas/esfera, pose neutra. \"Ajustado\" = número secundário, "
         "deixando escala (±12%) e posição variarem.", ""]
    fmt = lambda x: f"{x:.3f}".replace(".", ",")
    for mod in sorted(dados["resultados"]):
        rots = dados["resultados"][mod]
        nomes = list(rots)
        L += [f"## {mod}", ""]
        vistas = [v["vista"] for v in rots[nomes[0]]["vistas"]]
        L.append("| vista | " + " | ".join(f"{r}: IoU | {r}: ajustado | {r}: az/el" for r in nomes) + " |")
        L.append("|---|" + "---:|---:|---|" * len(nomes))
        for i, vn in enumerate(vistas):
            cel = []
            for r in nomes:
                v = rots[r]["vistas"][i]
                cel.append(f"{fmt(v['iou'])} | {fmt(v['iou_ajustado'])} | {v['az']}°/{v['el']}°")
            L.append(f"| {vn} | " + " | ".join(cel) + " |")
        L.append("| **média** | " + " | ".join(
            f"**{fmt(rots[r]['media'])}** | **{fmt(rots[r]['media_ajustado'])}** | " for r in nomes) + " |")
        L.append("")
        for r in nomes:
            L.append(f"- `{r}`: {rots[r]['origem']} · {rots[r]['data']}"
                     + (f" · {rots[r]['nota']}" if rots[r].get("nota") else ""))
        L.append("")
    open(ARQ_MD, "w").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser(description="Régua de semelhança (IoU de silhueta) contra as imagens de referência.")
    ap.add_argument("modelo", nargs="?")
    ap.add_argument("--pecas", help="pasta com montagem.json (padrão: pecas/<modelo>)")
    ap.add_argument("--rotulo", default="antes", help="antes | depois | qualquer nome (chave na tabela)")
    ap.add_argument("--referencia", help="dino | capivara | cubo (padrão: pelo começo do nome do modelo)")
    ap.add_argument("--malha", help="mede uma malha avulsa (glb/obj/stl) em vez do modelo montado")
    ap.add_argument("--cima", default="+z", help="eixo da malha que aponta para cima (ex.: +y)")
    ap.add_argument("--frente", default="+y", help="eixo da malha que aponta para a frente (ex.: +z)")
    ap.add_argument("--nota", default="", help="observação gravada na tabela")
    ap.add_argument("--busca-az", type=int, help="só para explorar: muda a vizinhança do azimute (fica registrado)")
    ap.add_argument("--espelha", action="store_true", help="teste de sinal: troca o sinal dos azimutes nominais")
    ap.add_argument("--sem-gravar", action="store_true", help="não mexe na tabela nem na imagem lado a lado")
    ap.add_argument("--saida", help="caminho da imagem lado a lado (padrão: referencia/comparacao/<modelo>-<rotulo>.png)")
    ap.add_argument("--mascaras", nargs="*", metavar="REF", help="gera as máscaras da referência (precisa de rembg)")
    ap.add_argument("--rembg", default="birefnet-general", help="modelo do rembg para --mascaras")
    ap.add_argument("--forcar", action="store_true", help="com --mascaras: refaz as que já existem")
    ap.add_argument("--tabela", action="store_true", help="só refaz o Markdown a partir do JSON")
    a = ap.parse_args()

    if a.mascaras is not None:
        gera_mascaras(a.mascaras or list(REFERENCIAS), a.rembg, a.forcar)
        return
    if a.tabela:
        grava_tabela()
        print("ok", ARQ_MD)
        return
    if not a.modelo:
        ap.error("diga o modelo (dino, capivara, cubo, cubo_rodas...)")

    ref = referencia_de(a.modelo, a.referencia)
    if a.malha:
        origem = os.path.relpath(os.path.abspath(a.malha), RAIZ)
        tris, cores, leves, nomes = carrega_malha(a.malha, a.cima, a.frente)
    else:
        pasta = pasta_pecas(a.modelo, a.pecas)
        origem = os.path.relpath(pasta, RAIZ)
        tris, cores, leves, nomes = carrega_modelo(pasta)
    print(f"{a.modelo} [{a.rotulo}] · referência {ref} · {origem} · {len(tris)} triângulos")
    print("  entram: " + ", ".join(nomes))
    vistas = mede(ref, tris, leves, espelha=a.espelha, busca_az=a.busca_az)
    media = sum(v["iou"] for v in vistas) / len(vistas)
    media_aj = sum(v["iou_ajustado"] for v in vistas) / len(vistas)
    print(f"  => {a.modelo} [{a.rotulo}]: IoU médio {media:.3f} (ajustado {media_aj:.3f})")
    if a.sem_gravar:
        return
    arq = a.saida or os.path.join(DIR_LADO, f"{a.modelo}-{a.rotulo}.png")
    lado_a_lado(ref, a.modelo, a.rotulo, vistas, tris, cores, arq, eh_malha=bool(a.malha))
    nota = a.nota
    if a.espelha:
        nota = (nota + " · azimutes espelhados (teste)").strip(" ·")
    if a.busca_az is not None:
        nota = (nota + f" · busca de azimute ±{a.busca_az}° (fora do protocolo)").strip(" ·")
    grava_tabela(a.modelo, a.rotulo, {
        "referencia": ref, "origem": origem, "data": datetime.date.today().isoformat(), "nota": nota,
        "triangulos": int(len(tris)), "entram": nomes,
        "vistas": [{k: v[k] for k in v if not k.startswith("_")} for v in vistas],
        "media": round(media, 4), "media_ajustado": round(media_aj, 4),
    })
    print(f"  lado a lado: {arq}\n  tabela: {ARQ_MD}")


if __name__ == "__main__":
    main()
