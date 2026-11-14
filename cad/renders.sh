#!/usr/bin/env bash
# Renders finais de um modelo: montado, 4 vistas, explodido, esqueleto e mesas. Saída em imagens/ (JPG).
# Uso: cad/renders.sh <modelo>     (usa a fila de render da máquina, se existir)
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
M="$1"; OUT="$RAIZ/imagens"; mkdir -p "$OUT"
FILA="$HOME/projetos/wifi/scripts/fila-vaga"
r() { # r <json> <saida.png> args...
  local J="$1" S="$2"; shift 2
  local CMD=(blender -b --python "$RAIZ/cad/render_blender.py" -- "$J" "$S" "$@")
  if [ -x "$FILA" ]; then "$FILA" render "robos-$M" -- "${CMD[@]}" >/dev/null 2>&1; else "${CMD[@]}" >/dev/null 2>&1; fi
  "$RAIZ/.venv/bin/python" -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[1][:-4]+'.jpg', quality=88)" "$S" && rm -f "$S"
}
J="$RAIZ/pecas/$M/montagem.json"
r "$J" "$OUT/$M-montado.png"   --az 32 --el 13 --res 1400x1400 --amostras 96
r "$J" "$OUT/$M-explodido.png" --az 38 --el 16 --res 1600x1400 --amostras 96 --explodir 1.0 --zoom 1.35
r "$J" "$OUT/$M-esqueleto.png" --az 32 --el 13 --res 1400x1400 --amostras 96 --so-material PETG
r "$RAIZ/pecas/$M/mesas.json" "$OUT/$M-mesas.png" --az 0 --el 62 --res 1800x1200 --amostras 64 --mesa --sem-componentes --orto
"$RAIZ/cad/vistas.sh" "$M" "$OUT/$M-vistas.png" 800x800 64 >/dev/null
"$RAIZ/.venv/bin/python" -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[1][:-4]+'.jpg', quality=88)" "$OUT/$M-vistas.png" && rm -f "$OUT/$M-vistas.png"
ls "$OUT" | grep "^$M-"
