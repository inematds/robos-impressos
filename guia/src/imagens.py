#!/usr/bin/env python3
"""Copia os renders de imagens/ para guia/assets/ em tamanho de página (1200 px de largura)."""
from pathlib import Path
from PIL import Image
RAIZ = Path(__file__).resolve().parents[2]
for f in sorted((RAIZ / "imagens").glob("*.jpg")):
    im = Image.open(f).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(RAIZ / "guia" / "assets" / f.name, quality=84, optimize=True)
    print(f.name, im.size)
