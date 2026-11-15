#!/usr/bin/env python3
"""Mapas de balanços das peças PRINCIPAIS de cada robô, sem texto na imagem (servem para os 3 idiomas do guia).

  .venv/bin/python comum/cad/mapas_balancos.py <id|todos>

Saída: projetos/<robô>/imagens/balancos/<id>-<peça>.jpg (3 vistas lado a lado: por BAIXO pela frente/direita, por
BAIXO por trás/esquerda, por cima como sai da mesa) + `indice.json` (números de cada peça, para a legenda da página).
Cores: vermelho = sem apoio (balanço livre, teto, ponte longa), amarelo = balanço tolerado (furo, ponte curta,
beira), azul = face na mesa, cinza = sem balanço. A peça aparece NA ORIENTAÇÃO DE IMPRESSÃO.

Peça principal (regra, sem lista à mão): tem suporte declarado ("sim…") OU pesa >= 50 g OU é ponto de carga pelo
nome (garfo, berço, tubo do pescoço, chassi). O cálculo é o do teste 10 (comum/cad/comum/imprimibilidade.py); o PLY
com a cor por face fica em .preview/balancos/ (fora do git). Render: Blender pela fila de render da máquina.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "comum"))
from cad.caminhos import MODELOS, id_de, pasta  # noqa: E402
from cad.comum import imprimibilidade as IMP  # noqa: E402

from PIL import Image  # noqa: E402

MASSA_MIN_G = 50.0
CARGA = ("garfo", "berco", "tubo-pescoco", "chassi")
VISTAS = "35,-45;215,-45;35,28"
RES = 620
LARGURA = 1500                       # largura final do JPG (3 vistas)


def principais(mj: dict) -> list[dict]:
    fica = []
    for p in mj["pecas"]:
        sup = str(p.get("suporte", "não")).strip().lower()
        if sup.startswith("sim") or p.get("massa_g", 0) >= MASSA_MIN_G or any(p["nome"].startswith(c) for c in CARGA):
            fica.append(p)
    return sorted(fica, key=lambda p: -p.get("massa_g", 0))


def render(ply: Path, jpg: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "v"
        cmd = ["blender", "-b", "--python", str(RAIZ / "comum/cad/render_balancos.py"), "--", str(ply), str(base),
               "--vistas", VISTAS, "--res", f"{RES}x{RES}", "--amostras", "32"]
        fila = Path.home() / "projetos/wifi/scripts/fila-vaga"
        if fila.exists() and os.access(fila, os.X_OK):
            cmd = [str(fila), "render", "robos-balancos", "--"] + cmd
        for tentativa in (1, 2):
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            vs = sorted(Path(tmp).glob("v-*.png"))
            if r.returncode == 0 and len(vs) >= 3:
                break
            if tentativa == 1:
                # o importador de PLY do Blender 4.0 recusa alguns PLY binários válidos ("unknown error"; o trimesh
                # os lê): regrava em ASCII e tenta de novo
                import trimesh
                ascii_ = Path(tmp) / "ascii.ply"
                ascii_.write_bytes(trimesh.exchange.ply.export_ply(trimesh.load(ply, process=False), encoding="ascii"))
                cmd[cmd.index(str(ply))] = str(ascii_)
            else:
                print("   render falhou:", (r.stdout + r.stderr)[-300:].replace("\n", " | "))
                return False
        ims = [Image.open(v).convert("RGB") for v in vs]
        folha = Image.new("RGB", (RES * 3, RES), "white")
        for i, im in enumerate(ims):
            folha.paste(im, (i * RES, 0))
        folha = folha.resize((LARGURA, round(RES * LARGURA / (RES * 3))), Image.LANCZOS)
        jpg.parent.mkdir(parents=True, exist_ok=True)
        folha.save(jpg, quality=86, optimize=True)
    return True


def um(modelo: str) -> int:
    mid = id_de(modelo)
    base, mj = IMP.carregar_modelo(mid)
    lim = IMP.limites()
    dest = pasta(mid) / "imagens" / "balancos"
    indice, falhas = [], 0
    for p in principais(mj):
        nome = p["nome"]
        tm = IMP._carrega(base / p["arquivo"])
        d = IMP.exportar_mapa(tm, RAIZ / ".preview" / "balancos" / f"{mid}-{nome}.ply", lim)
        sup = p.get("suporte", "não")
        ok = render(RAIZ / ".preview" / "balancos" / f"{mid}-{nome}.ply", dest / f"{mid}-{nome}.jpg")
        falhas += 0 if ok else 1
        indice.append({
            "peca": nome, "imagem": f"{mid}-{nome}.jpg", "massa_g": p.get("massa_g"), "material": p.get("material"),
            "suporte": sup, "veredito": IMP.veredito(d, sup),
            "sem_apoio_mm2": round(d["sem_apoio_mm2"], 1), "sem_apoio_pct": round(d["sem_apoio_pct"], 2),
            "limite_mm2": round(d["limite_mm2"], 1), "maior_ponte_mm": round(d["maior_ponte_mm"], 1),
            "orientacao": p.get("orientacao", ""),
        })
        print(f"{mid:11s} {nome:18s} sem apoio {d['sem_apoio_mm2']:8.0f} mm² {d['sem_apoio_pct']:5.1f} %  {indice[-1]['veredito']}"
              + ("" if ok else "  (IMAGEM FALHOU)"))
    (dest / "indice.json").write_text(json.dumps({
        "modelo": mid,
        "vistas": ["por baixo, frente/direita", "por baixo, trás/esquerda", "por cima, como sai da mesa"],
        "cores": {"vermelho": "sem apoio (balanço livre, teto, ponte longa)", "amarelo": "balanço tolerado (furo, ponte curta, beira)",
                  "azul": "face na mesa", "cinza": "sem balanço"},
        "regra": f"peça com suporte declarado, ou >= {MASSA_MIN_G:.0f} g, ou ponto de carga ({', '.join(CARGA)})",
        "pecas": indice}, ensure_ascii=False, indent=1) + "\n")
    return falhas


if __name__ == "__main__":
    quais = list(MODELOS) if len(sys.argv) < 2 or sys.argv[1] == "todos" else sys.argv[1:]
    sys.exit(1 if sum(um(m) for m in quais) else 0)
