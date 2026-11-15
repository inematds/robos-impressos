#!/usr/bin/env bash
# Renders finais de um modelo: montado, 4 vistas (as da régua de semelhança: vistas_regua.py), explodido, esqueleto e mesas. Saída em projetos/<robô>/imagens/ (JPG).
# Uso: comum/cad/renders.sh <modelo>     (usa a fila de render da máquina, se existir)
set -euo pipefail
CAD="$(cd "$(dirname "$0")" && pwd)"; RAIZ="$(cd "$CAD/../.." && pwd)"
M="$("$RAIZ/.venv/bin/python" "$CAD/caminhos.py" --id "$1")"          # aceita id ou pasta; os arquivos saem com o id (<id>-montado.jpg)
PASTA="$("$RAIZ/.venv/bin/python" "$CAD/caminhos.py" "$M")"           # id → projetos/<robô> (registro único)
OUT="$PASTA/imagens"; mkdir -p "$OUT"
FILA="$HOME/projetos/wifi/scripts/fila-vaga"
r() { # r <json> <saida.png> args...
  local J="$1" S="$2"; shift 2
  local CMD=(blender -b --python "$CAD/render_blender.py" -- "$J" "$S" "$@")
  if [ -x "$FILA" ]; then "$FILA" render "robos-$M" -- "${CMD[@]}" >/dev/null 2>&1; else "${CMD[@]}" >/dev/null 2>&1; fi
  "$RAIZ/.venv/bin/python" -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[1][:-4]+'.jpg', quality=88)" "$S" && rm -f "$S"
}
J="$PASTA/montagem.json"
# montado e 4 vistas = o robô da FASE 1 (--sem-fase2: sem câmera, ToF, microfones, LiDAR; a placa verde da câmera
# aparecia como um ponto verde dentro da pupila). O esqueleto também sai sem a fase 2 (sem a casca, a câmera e os
# microfones ficavam soltos no ar). Só o explodido mostra os componentes da fase 2, cada um no seu lugar.
r "$J" "$OUT/$M-montado.png"   --az 32 --el 13 --res 1400x1400 --amostras 96 --sem-fase2
r "$J" "$OUT/$M-explodido.png" --az 38 --el 16 --res 1600x1400 --amostras 96 --explodir 1.0
r "$J" "$OUT/$M-esqueleto.png" --az 32 --el 13 --res 1400x1400 --amostras 96 --so-material PETG --sem-fase2
# mesas: o render_blender enquadra pelas PLACAS (não pelas peças: com fileira incompleta a placa da ponta saía cortada)
# e numera cada uma; --az 180 = ordem de leitura (mesa 01 em cima, à esquerda)
r "$PASTA/mesas.json" "$OUT/$M-mesas.png" --az 180 --el 62 --res 1800x1200 --amostras 64 --mesa --sem-componentes --orto
"$CAD/vistas.sh" "$M" "$OUT/$M-vistas.png" 800x800 64 --sem-fase2 >/dev/null
"$RAIZ/.venv/bin/python" -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[1][:-4]+'.jpg', quality=88)" "$OUT/$M-vistas.png" && rm -f "$OUT/$M-vistas.png"
ls "$OUT" | grep "^$M-"
