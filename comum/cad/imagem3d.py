#!/usr/bin/env python3
"""Imagem de referência → malha 3D, LOCAL na GPU (Hunyuan3D-2, só a FORMA; sem textura, sem API, sem nuvem).

Serve para ter uma malha do personagem parecida com a referência, que a etapa de CAD usa como casca externa.
NÃO faz parte do build (comum/cad/gerar.py não depende disto) e precisa de coisas que não estão no repo:
  - as imagens de referência do dono e os recortes sem fundo (referencia/recortes/*-rgba.png, feitos por
    `comum/cad/comparar.py --mascaras`);
  - um venv próprio com torch+CUDA, diffusers, transformers, torchvision, einops, omegaconf, opencv, pymeshlab:
    `.venv-i23d/` (fora do git);
  - o código oficial: `git clone --depth 1 https://github.com/Tencent-Hunyuan/Hunyuan3D-2 .preview/i23d/Hunyuan3D-2`
    (ou aponte HY3D_REPO) e, para o modelo 2.1, `.../Tencent-Hunyuan/Hunyuan3D-2.1 .preview/i23d/Hunyuan3D-2.1`
    (ou HY3D21_REPO = pasta hy3dshape; pede também pytorch-lightning e timm); os pesos vêm do Hugging Face na primeira vez (tencent/Hunyuan3D-2mv, -2, -2.1; ~5–7 GB cada).

Uso (sempre pela vaga de GPU da máquina, com tempo e memória limitados):
  ~/projetos/wifi/scripts/fila-vaga gpu dinobot -- timeout 1500 .venv-i23d/bin/python comum/cad/imagem3d.py capivara \
      --modelo 2mv --vistas front=frente,left=lado,back=costas --sementes 1,2
  ... comum/cad/imagem3d.py dino --modelo 2.1 --imagem tres-quartos-b --sementes 1

Modelos: 2mv = multi-vista (front/left/back/right; "left" = personagem olhando para a ESQUERDA da imagem);
         2.0 e 2.1 = uma imagem só.
Saída: referencia/malhas/<personagem>-hy<modelo>-<vistas>-s<semente>.glb (eixos do gerador: Y para cima, +Z frente).
Medir contra a referência: .venv/bin/python comum/cad/comparar.py <personagem> --malha <glb> --cima +y --frente +z --rotulo malha-...
"""
import argparse
import os
import sys
import threading
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # raiz do repo (este arquivo: comum/cad/)
DIR_REC = os.path.join(RAIZ, "referencia", "recortes")
DIR_MALHAS = os.path.join(RAIZ, "referencia", "malhas")
MODELOS = {
    "2mv": ("tencent/Hunyuan3D-2mv", "hunyuan3d-dit-v2-mv"),
    "2.0": ("tencent/Hunyuan3D-2", "hunyuan3d-dit-v2-0"),
    "2.1": ("tencent/Hunyuan3D-2.1", "hunyuan3d-dit-v2-1"),
}


def guarda_memoria(minimo_gb):
    """No GB10 a memória é uma só para CPU e GPU e o cgroup não segura o CUDA: se faltar, mata o processo."""
    def laco():
        while True:
            for linha in open("/proc/meminfo"):
                if linha.startswith("MemAvailable"):
                    livre = int(linha.split()[1]) / 1e6
                    if livre < minimo_gb:
                        print(f"GUARDA: só {livre:.1f} GB livres (< {minimo_gb}); abortando.", flush=True)
                        os._exit(3)
            time.sleep(2)
    threading.Thread(target=laco, daemon=True).start()


def main():
    ap = argparse.ArgumentParser(description="Imagem → malha 3D local (Hunyuan3D-2, só forma).")
    ap.add_argument("personagem", help="dino | capivara | cubo (prefixo dos recortes)")
    ap.add_argument("--modelo", choices=list(MODELOS), default="2mv")
    ap.add_argument("--vistas", help="multi-vista: front=frente,left=lado,back=costas (nomes das vistas da régua)")
    ap.add_argument("--imagem", help="imagem única: nome da vista (ex.: tres-quartos)")
    ap.add_argument("--sementes", default="1")
    ap.add_argument("--passos", type=int, default=50)
    ap.add_argument("--octree", type=int, default=384)
    ap.add_argument("--guia", type=float, default=5.0)
    ap.add_argument("--memoria-minima-gb", type=float, default=14.0)
    a = ap.parse_args()

    guarda_memoria(a.memoria_minima_gb)
    previa = os.path.join(RAIZ, ".preview", "i23d")
    import torch
    from PIL import Image
    if a.modelo == "2.1":       # o 2.1 tem pacote próprio (hy3dshape) e checkpoint .ckpt
        sys.path.insert(0, os.environ.get("HY3D21_REPO", os.path.join(previa, "Hunyuan3D-2.1", "hy3dshape")))
        from hy3dshape.pipelines import Hunyuan3DDiTFlowMatchingPipeline
        from hy3dshape.postprocessors import FloaterRemover
    else:
        sys.path.insert(0, os.environ.get("HY3D_REPO", os.path.join(previa, "Hunyuan3D-2")))
        from hy3dgen.shapegen import FloaterRemover, Hunyuan3DDiTFlowMatchingPipeline

    assert torch.cuda.is_available(), "torch sem CUDA neste venv"

    def recorte(vista):
        return Image.open(os.path.join(DIR_REC, f"{a.personagem}-{vista}-rgba.png")).convert("RGBA")

    if a.modelo == "2mv":
        pares = dict(p.split("=") for p in (a.vistas or "front=frente").split(","))
        imagem = {k: recorte(v) for k, v in pares.items()}
        etiqueta = "".join(k[0] for k in pares)        # ex.: flb = front+left+back
    else:
        imagem = recorte(a.imagem or "frente")
        etiqueta = a.imagem or "frente"

    repo, sub = MODELOS[a.modelo]
    t0 = time.time()
    pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(repo, subfolder=sub, variant="fp16",
                                                            use_safetensors=a.modelo != "2.1")
    print(f"modelo {a.modelo} carregado em {time.time() - t0:.0f} s", flush=True)
    os.makedirs(DIR_MALHAS, exist_ok=True)
    for s in [int(x) for x in a.sementes.split(",")]:
        t0 = time.time()
        malha = pipe(image=imagem, num_inference_steps=a.passos, octree_resolution=a.octree, num_chunks=20000,
                     guidance_scale=a.guia, generator=torch.manual_seed(s), output_type="trimesh")[0]
        try:
            malha = FloaterRemover()(malha)
        except Exception as e:      # sem pymeshlab: segue com a malha crua
            print("sem FloaterRemover:", type(e).__name__, e)
        arq = os.path.join(DIR_MALHAS, f"{a.personagem}-hy{a.modelo}-{etiqueta}-s{s}.glb")
        malha.export(arq)
        print(f"ok {arq}  {len(malha.faces)} faces  {time.time() - t0:.0f} s  "
              f"pico GPU {torch.cuda.max_memory_allocated() / 1e9:.1f} GB", flush=True)


if __name__ == "__main__":
    main()
