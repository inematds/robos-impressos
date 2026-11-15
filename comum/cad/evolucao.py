#!/usr/bin/env python3
"""Imagens e números da página /guia/evolucao/ (capivara e dino: antes × depois, com a régua de semelhança).

  .venv/bin/python comum/cad/evolucao.py            # renders + lado a lado + dados.json
  .venv/bin/python comum/cad/evolucao.py --so-dados # só regrava guia/evolucao/assets/dados.json

Grava em guia/evolucao/assets/ (só o que a página usa; JPG reduzido):
  <bicho>-antes-<vista>.jpg / <bicho>-depois-<vista>.jpg   render nosso nas 4 vistas da régua (vistas_regua.py),
                                                            fase 1 (sem os componentes da fase 2), mesma câmera
  <bicho>-regua-antes.jpg / <bicho>-regua-depois.jpg       lado a lado da régua: referência | nosso | sobreposição
  <bicho>-referencia.jpg                                   a folha de referência do Nei (4 vistas)
  dados.json                                               IoU por vista: antes, depois, teto da malha, alvo

"Antes" = tag v1.0.2: precisa da cópia `git worktree add .preview/v102 v1.0.2` (STL e montagem.json vêm no repo).
As imagens que contêm a referência do Nei (régua e folha) entram no repo porque ele AUTORIZOU para esta página
(decisions.md, 14/11 noite). Malhas, máscaras e recortes de `referencia/` continuam fora do git.
Os lado a lado vêm de `comparar.py <bicho> --rotulo antes|depois` (referencia/comparacao/); este script não os refaz.
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
BICHOS = ("capivara", "dino")
TETO = {"capivara": "malha-capivara-hy2mv-flb-s2", "dino": "malha-dino-hy2mv-fl-s2"}     # a malha crua usada na casca
FOLHA = {"capivara": "capivara-4-vistas.png", "dino": "dino-4-angulos.png"}
# alvo da MÉDIA, fixado ANTES de existir o "depois" (canal.md, 14/11 17:00): metade do caminho entre o antes e o teto
ALVO_OFICIAL = {"capivara": 0.852, "dino": 0.856}
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


def imagens():
    DEST.mkdir(parents=True, exist_ok=True)
    for b in BICHOS:
        antes = V102 / "pecas" / b / "montagem.json"
        if not antes.exists():
            sys.exit(f"falta {antes}: rode `git worktree add .preview/v102 v1.0.2`")
        for estado, mj in (("antes", antes), ("depois", pasta(b) / "montagem.json")):
            for nome, az, el in vistas(b):
                render(mj, DEST / f"{b}-{estado}-{nome}.jpg", az, el)
        for estado in ("antes", "depois"):
            reduz(RAIZ / "referencia" / "comparacao" / f"{b}-{estado}.png", DEST / f"{b}-regua-{estado}.jpg", LARG_REGUA)
        reduz(RAIZ / "referencia" / FOLHA[b], DEST / f"{b}-referencia.jpg", LARG_REGUA)


def dados():
    DEST.mkdir(parents=True, exist_ok=True)
    sem = json.loads((RAIZ / "comparacao" / "semelhanca.json").read_text())
    saida = {
        "fonte": "comparacao/semelhanca.json (comum/cad/comparar.py, protocolo v%s)" % sem["protocolo"]["versao"],
        "como_ler": "IoU = área comum ÷ área total das duas silhuetas (0 a 1). Mede só o contorno em cada vista, não cor nem detalhe.",
        "regra_do_alvo": "alvo = metade do caminho entre o 'antes' e o teto (a malha crua medida contra a mesma referência); "
                         "a regra vale para a MÉDIA do bicho; o alvo por vista é a mesma conta aplicada à vista (derivado)",
        "antes": "tag v1.0.2", "depois": "v1.1.2", "bichos": {},
    }
    for b in BICHOS:
        r = sem["resultados"][b]
        a, d, t = r["antes"], r["depois"], r[TETO[b]]
        vs = []
        for (nome, az, el), va, vd, vt in zip(vistas(b), a["vistas"], d["vistas"], t["vistas"]):
            assert va["vista"] == vd["vista"] == vt["vista"] == nome, (nome, va["vista"])
            vs.append({
                "vista": nome, "az_nominal": az, "el_nominal": el,
                "antes": round(va["iou"], 3), "depois": round(vd["iou"], 3), "teto": round(vt["iou"], 3),
                "alvo_derivado": round((va["iou"] + vt["iou"]) / 2, 3), "ganho": round(round(vd["iou"], 3) - round(va["iou"], 3), 3),
                "az_el_escolhidos": {"antes": [va["az"], va["el"]], "depois": [vd["az"], vd["el"]]},
                "imagem_antes": f"{b}-antes-{nome}.jpg", "imagem_depois": f"{b}-depois-{nome}.jpg",
            })
        alvo = ALVO_OFICIAL[b]
        assert abs(alvo - (a["media"] + t["media"]) / 2) < 0.001, "o alvo gravado não bate com antes/teto do JSON"
        saida["bichos"][b] = {
            "vistas": vs,
            "media": {"antes": round(a["media"], 3), "depois": round(d["media"], 3), "teto": round(t["media"], 3),
                      "alvo": round(alvo, 3), "ganho": round(round(d["media"], 3) - round(a["media"], 3), 3),
                      "atingiu_o_alvo": bool(d["media"] >= alvo),
                      "caminho_percorrido_pct": round(100 * (d["media"] - a["media"]) / (t["media"] - a["media"]))},
            "teto_e": f"malha crua do image-to-3D local ({TETO[b]}), medida contra a mesma referência",
            "regua_antes": f"{b}-regua-antes.jpg", "regua_depois": f"{b}-regua-depois.jpg", "referencia": f"{b}-referencia.jpg",
            "colunas_da_regua": ["referência", "nosso modelo (mesma câmera)", "silhuetas sobrepostas: vermelho = só na referência; azul = só no nosso; verde = nos dois"],
            "aviso_da_regua": "o texto dentro das imagens da régua está em português; no desenho do nosso modelo a régua pinta as rodas por cima da casca (no robô elas ficam escondidas)",
        }
    (DEST / "dados.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1) + "\n")
    for b in BICHOS:
        m = saida["bichos"][b]["media"]
        print(f"{b}: antes {m['antes']:.3f} · depois {m['depois']:.3f} · teto {m['teto']:.3f} · alvo {m['alvo']:.3f} · "
              f"{m['caminho_percorrido_pct']} % do caminho até o teto")


if __name__ == "__main__":
    if "--so-dados" not in sys.argv:
        imagens()
    dados()
