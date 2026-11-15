#!/usr/bin/env bash
# Renderiza as 4 vistas de um modelo, AS MESMAS da régua de semelhança (comum/cad/vistas_regua.py: os ângulos
# nominais das folhas de referência), e junta numa imagem só (2 x 2, na ordem da folha).
# Uso: comum/cad/vistas.sh <modelo> <saida.png> [res] [amostras] [extra args do render]
# Variáveis opcionais:
#   VISTAS_JSON=<montagem.json>   renderiza outra montagem com as vistas de <modelo> (ex.: a da tag v1.0.2)
#   VISTAS_PASTA=<pasta>          guarda também cada vista separada: <pasta>/<nome-da-vista>.png
set -euo pipefail
CAD="$(cd "$(dirname "$0")" && pwd)"; RAIZ="$(cd "$CAD/../.." && pwd)"
PASTA="$("$RAIZ/.venv/bin/python" "$CAD/caminhos.py" "$1")"   # id → projetos/<robô> (registro único)
MOD="$1"; SAIDA="$2"; RES="${3:-700x700}"; AM="${4:-24}"; shift 4 || true
JSON="${VISTAS_JSON:-$PASTA/montagem.json}"
TMP="$(mktemp -d)"
FILA="$HOME/projetos/wifi/scripts/fila-vaga"
i=0
while read -r NOME AZ EL; do
  CMD=(blender -b --python "$CAD/render_blender.py" -- "$JSON" "$TMP/v$i.png" --az "$AZ" --el "$EL" --res "$RES" --amostras "$AM" "$@")
  if [ -x "$FILA" ]; then "$FILA" render "robos-$MOD" -- "${CMD[@]}" </dev/null >/dev/null 2>&1; else "${CMD[@]}" </dev/null >/dev/null 2>&1; fi
  if [ -n "${VISTAS_PASTA:-}" ]; then mkdir -p "$VISTAS_PASTA"; cp "$TMP/v$i.png" "$VISTAS_PASTA/$NOME.png"; fi
  i=$((i+1))
done < <("$RAIZ/.venv/bin/python" "$CAD/vistas_regua.py" "$MOD")
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
