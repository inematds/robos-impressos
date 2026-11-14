#!/usr/bin/env bash
# Renderiza 4 vistas de um modelo (como a folha de referência) e junta numa imagem só.
# Uso: cad/vistas.sh <modelo> <saida.png> [res] [amostras] [extra args do render]
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
MOD="$1"; SAIDA="$2"; RES="${3:-700x700}"; AM="${4:-24}"; shift 4 || true
TMP="$(mktemp -d)"
FILA="$HOME/projetos/wifi/scripts/fila-vaga"
i=0
for AZ in 0 35 -35 90; do
  CMD=(blender -b --python "$RAIZ/cad/render_blender.py" -- "$RAIZ/pecas/$MOD/montagem.json" "$TMP/v$i.png" --az "$AZ" --el 12 --res "$RES" --amostras "$AM" "$@")
  if [ -x "$FILA" ]; then "$FILA" render "robos-$MOD" -- "${CMD[@]}" >/dev/null 2>&1; else "${CMD[@]}" >/dev/null 2>&1; fi
  i=$((i+1))
done
"$RAIZ/.venv/bin/python" - "$TMP" "$SAIDA" <<'PY'
import sys
from PIL import Image
t, s = sys.argv[1], sys.argv[2]
ims = [Image.open(f"{t}/v{i}.png") for i in range(4)]
w, h = ims[0].size
g = Image.new("RGB", (2 * w, 2 * h), "white")
for i, im in enumerate(ims):
    g.paste(im, ((i % 2) * w, (i // 2) * h))
g.save(s)
print("ok", s)
PY
rm -rf "$TMP"
