#!/usr/bin/env python3
"""Imagens e números da página /guia/evolucao/ e da seção "Evolução do desenho" da entrada do guia
(capivara, dino e cubo: referência × antes × depois, com a régua de semelhança; banner antigo × novo).

  .venv/bin/python comum/cad/evolucao.py                 # tudo: renders dos 3 + apoio + dados.json
  .venv/bin/python comum/cad/evolucao.py cubo            # renders só do cubo (os outros JPG de render ficam como estão)
  .venv/bin/python comum/cad/evolucao.py --sem-render    # só o apoio (referências, réguas, banner antigo) + dados.json
  .venv/bin/python comum/cad/evolucao.py --so-dados      # só regrava guia/evolucao/assets/dados.json

Grava em guia/evolucao/assets/ (só o que as páginas usam; JPG reduzido):
  <robô>-antes-<vista>.jpg / <robô>-depois-<vista>.jpg   render nosso nas vistas da régua (vistas_regua.py),
                                                          fase 1 (sem os componentes da fase 2), mesma câmera
  <robô>-ref-<vista>.jpg                                 o desenho de referência do Nei NAQUELA vista (recorte quadrado)
  <robô>-regua-antes.jpg / <robô>-regua-depois.jpg       lado a lado da régua: referência | nosso | sobreposição
  <robô>-referencia.jpg                                  a folha de referência inteira (só os bichos: 4 vistas)
  banner-antes[-en|-es].jpg                              o banner da v1.0.2 (ilustração de IA), para o antes × depois
  dados.json                                             IoU por vista: antes, depois, teto da malha, alvo; nomes das imagens

Bichos (capivara, dino): as 4 vistas da folha. Cubo: a referência tem UMA vista (três-quartos), e é só ela que entra;
não tem malha (teto = null) e o alvo é antes + 0,10.
"Antes" = tag v1.0.2: precisa da cópia `git worktree add .preview/v102 v1.0.2` (STL e montagem.json vêm no repo).
As imagens que contêm a referência do Nei (recortes, régua e folha) entram no repo porque ele AUTORIZOU
(decisions.md, 14/11 noite e 15/11: vale também para a do cubo). Malhas e máscaras de `referencia/` continuam fora do git.
Os lado a lado vêm de `comparar.py <robô> --rotulo antes|depois` (referencia/comparacao/); este script não os refaz.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "comum"))
from cad.caminhos import pasta  # noqa: E402
from cad.vistas_regua import vistas  # noqa: E402

DEST = RAIZ / "guia" / "evolucao" / "assets"
V102 = RAIZ / ".preview" / "v102"
BICHOS = ("capivara", "dino", "cubo")                 # a chave do dados.json continua "bichos" (lida por 3 scripts do guia)
TETO = {"capivara": "malha-capivara-hy2mv-flb-s2", "dino": "malha-dino-hy2mv-fl-s2"}     # a malha crua usada na casca
FOLHA = {"capivara": "capivara-4-vistas.png", "dino": "dino-4-angulos.png"}
# alvo da MÉDIA, fixado ANTES de existir o "depois" (canal.md, 14/11 17:00): metade do caminho entre o antes e o teto
ALVO_OFICIAL = {"capivara": 0.852, "dino": 0.856}
SEM_MALHA = 0.10      # robô sem malha (cubo): alvo = antes + 0,10
CAPA = {"capivara": "frente", "dino": "frente", "cubo": "tres-quartos"}   # a vista do bloco compacto da entrada
LADO_REF_MAX = 2.0    # o recorte da referência nunca é ampliado mais que isto (o do cubo tem 220 px)
FUNDO_REF = (233, 233, 238)
BANNERS = {"pt": "banner.jpg", "en": "banner-en.jpg", "es": "banner-es.jpg"}   # guia/assets/ na tag v1.0.2
LARG_BANNER = 1100
LADO = 720            # lado de cada vista (px)
LARG_REGUA = 1100     # largura dos lado a lado e da folha (px)


def render(montagem: Path, saida_jpg: Path, az: float, el: float):
    fila = Path.home() / "projetos/wifi/scripts/fila-vaga"
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "v.png"
        cmd = ["blender", "-b", "--python", str(RAIZ / "comum/cad/render_blender.py"), "--", str(montagem), str(png),
               "--az", f"{az:g}", "--el", f"{el:g}", "--res", f"{LADO * 2}x{LADO * 2}", "--amostras", "48", "--sem-fase2"]
        if fila.exists() and os.access(fila, os.X_OK):
            cmd = [str(fila), "render", "robos-evolucao", "--"] + cmd
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not png.exists():
            sys.exit(f"render falhou ({montagem}, az {az}): {(r.stdout + r.stderr)[-500:]}")
        Image.open(png).convert("RGB").resize((LADO, LADO), Image.LANCZOS).save(saida_jpg, quality=86, optimize=True)
    print("ok", saida_jpg.relative_to(RAIZ))


def reduz(origem: Path, destino: Path, larg: int):
    im = Image.open(origem).convert("RGB")
    if im.width > larg:
        im = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    im.save(destino, quality=85, optimize=True)
    print("ok", destino.relative_to(RAIZ), im.size)


def vistas_medidas(b):
    """As vistas de `vistas_regua` que a régua mede de verdade (têm referência): as 4 dos bichos; no cubo, só a três-quartos."""
    sem = json.loads((RAIZ / "comparacao" / "semelhanca.json").read_text())["resultados"][b]["depois"]["vistas"]
    medidas = [v["vista"] for v in sem]
    vs = [v for v in vistas(b) if v[0] in medidas]
    assert [v[0] for v in vs] == medidas, (b, medidas, [v[0] for v in vistas(b)])
    return vs


def ref_vista(b, nome):
    """Recorte da referência naquela vista → quadrado (sem cortar o desenho: completa com faixa neutra), no máximo LADO px
    e nunca ampliado mais que LADO_REF_MAX."""
    im = Image.open(RAIZ / "referencia" / "recortes" / f"{b}-{nome}.png").convert("RGB")
    q = max(im.size)
    quadro = Image.new("RGB", (q, q), FUNDO_REF)
    quadro.paste(im, ((q - im.width) // 2, (q - im.height) // 2))
    lado = min(LADO, round(q * LADO_REF_MAX))
    destino = DEST / f"{b}-ref-{nome}.jpg"
    quadro.resize((lado, lado), Image.LANCZOS).save(destino, quality=86, optimize=True)
    print("ok", destino.relative_to(RAIZ), (lado, lado))


def banner_antigo():
    """O banner da v1.0.2 (feito por IA), nos 3 idiomas, lido da tag."""
    import io
    for lg, arq in BANNERS.items():
        r = subprocess.run(["git", "-C", str(RAIZ), "show", f"v1.0.2:guia/assets/{arq}"], capture_output=True)
        if r.returncode != 0:
            sys.exit(f"não achei guia/assets/{arq} na tag v1.0.2")
        im = Image.open(io.BytesIO(r.stdout)).convert("RGB")
        im = im.resize((LARG_BANNER, round(im.height * LARG_BANNER / im.width)), Image.LANCZOS)
        destino = DEST / ("banner-antes.jpg" if lg == "pt" else f"banner-antes-{lg}.jpg")
        im.save(destino, quality=85, optimize=True)
        print("ok", destino.relative_to(RAIZ), im.size)


def renders(quais):
    for b in quais:
        antes = V102 / "pecas" / b / "montagem.json"
        if not antes.exists():
            sys.exit(f"falta {antes}: rode `git worktree add .preview/v102 v1.0.2`")
        for estado, mj in (("antes", antes), ("depois", pasta(b) / "montagem.json")):
            for nome, az, el in vistas_medidas(b):
                render(mj, DEST / f"{b}-{estado}-{nome}.jpg", az, el)


def apoio():
    """Referências, réguas e banner antigo: cópias reduzidas (não renderiza nada)."""
    DEST.mkdir(parents=True, exist_ok=True)
    for b in BICHOS:
        for nome, _, _ in vistas_medidas(b):
            ref_vista(b, nome)
        for estado in ("antes", "depois"):
            reduz(RAIZ / "referencia" / "comparacao" / f"{b}-{estado}.png", DEST / f"{b}-regua-{estado}.jpg", LARG_REGUA)
        if b in FOLHA:
            reduz(RAIZ / "referencia" / FOLHA[b], DEST / f"{b}-referencia.jpg", LARG_REGUA)
    banner_antigo()


def dados():
    DEST.mkdir(parents=True, exist_ok=True)
    sem = json.loads((RAIZ / "comparacao" / "semelhanca.json").read_text())
    saida = {
        "fonte": "comparacao/semelhanca.json (comum/cad/comparar.py, protocolo v%s)" % sem["protocolo"]["versao"],
        "como_ler": "IoU = área comum ÷ área total das duas silhuetas (0 a 1). Mede só o contorno em cada vista, não cor nem detalhe.",
        "regra_do_alvo": "alvo = metade do caminho entre o 'antes' e o teto (a malha crua medida contra a mesma referência); "
                         "a regra vale para a MÉDIA do bicho; o alvo por vista é a mesma conta aplicada à vista (derivado)",
        "antes": "tag v1.0.2", "depois": "v1.1.2",
        "banner": {"antes": {lg: ("banner-antes.jpg" if lg == "pt" else f"banner-antes-{lg}.jpg") for lg in BANNERS},
                   "depois": dict(BANNERS),
                   "nota": "antes = banner da tag v1.0.2 (ilustração feita por IA), em guia/evolucao/assets/; depois = o banner de guia/assets/ (render dos modelos do repo)"},
        "bichos": {},
    }
    for b in BICHOS:
        r = sem["resultados"][b]
        a, d, t = r["antes"], r["depois"], (r[TETO[b]] if b in TETO else None)
        tv = t["vistas"] if t else [None] * len(a["vistas"])
        vs = []
        for (nome, az, el), va, vd, vt in zip(vistas_medidas(b), a["vistas"], d["vistas"], tv):
            assert va["vista"] == vd["vista"] == nome and (vt is None or vt["vista"] == nome), (nome, va["vista"])
            vs.append({
                "vista": nome, "az_nominal": az, "el_nominal": el,
                "antes": round(va["iou"], 3), "depois": round(vd["iou"], 3), "teto": round(vt["iou"], 3) if vt else None,
                "alvo_derivado": round((va["iou"] + vt["iou"]) / 2 if vt else va["iou"] + SEM_MALHA, 3),
                "ganho": round(round(vd["iou"], 3) - round(va["iou"], 3), 3),
                "az_el_escolhidos": {"antes": [va["az"], va["el"]], "depois": [vd["az"], vd["el"]]},
                "imagem_ref": f"{b}-ref-{nome}.jpg", "imagem_antes": f"{b}-antes-{nome}.jpg", "imagem_depois": f"{b}-depois-{nome}.jpg",
            })
        if t:
            alvo = ALVO_OFICIAL[b]
            assert abs(alvo - (a["media"] + t["media"]) / 2) < 0.001, "o alvo gravado não bate com antes/teto do JSON"
        else:
            alvo = a["media"] + SEM_MALHA
        assert CAPA[b] in [v["vista"] for v in vs], f"{b}: a vista da capa não está entre as medidas"
        saida["bichos"][b] = {
            "vistas": vs,
            "vista_da_entrada": CAPA[b],
            "media": {"antes": round(a["media"], 3), "depois": round(d["media"], 3), "teto": round(t["media"], 3) if t else None,
                      "alvo": round(alvo, 3), "ganho": round(round(d["media"], 3) - round(a["media"], 3), 3),
                      "atingiu_o_alvo": bool(d["media"] >= alvo),
                      "caminho_percorrido_pct": round(100 * (d["media"] - a["media"]) / (t["media"] - a["media"])) if t else None},
            "teto_e": (f"malha crua do image-to-3D local ({TETO[b]}), medida contra a mesma referência" if t else
                       "não há: este robô não teve malha; o alvo é o antes + 0,10"),
            "regua_antes": f"{b}-regua-antes.jpg", "regua_depois": f"{b}-regua-depois.jpg",
            "referencia": f"{b}-referencia.jpg" if b in FOLHA else None,
            "colunas_da_regua": ["referência", "nosso modelo (mesma câmera)", "silhuetas sobrepostas: vermelho = só na referência; azul = só no nosso; verde = nos dois"],
            "aviso_da_regua": "o texto dentro das imagens da régua está em português; no desenho do nosso modelo a régua pinta as rodas por cima da casca (no robô elas ficam escondidas)",
        }
    (DEST / "dados.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1) + "\n")
    for b in BICHOS:
        m = saida["bichos"][b]["media"]
        print(f"{b}: antes {m['antes']:.3f} · depois {m['depois']:.3f} · alvo {m['alvo']:.3f} · " +
              (f"teto {m['teto']:.3f} · {m['caminho_percorrido_pct']} % do caminho até o teto" if m["teto"] else "sem malha (sem teto)"))


if __name__ == "__main__":
    quais = [a for a in sys.argv[1:] if not a.startswith("--")]
    assert set(quais) <= set(BICHOS), f"robô desconhecido: {quais} (use {BICHOS})"
    if "--so-dados" not in sys.argv:
        if "--sem-render" not in sys.argv:
            renders(quais or BICHOS)
        apoio()
    dados()
