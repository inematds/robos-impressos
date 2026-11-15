#!/usr/bin/env python3
"""Regenera o GUIA INTEIRO com um comando: entrada + página de cada robô + evolução, em PT, EN e ES, e confere tudo.

  .venv/bin/python guia/src/tudo.py                  tudo (traduz só o texto que falta ou mudou, pelo inema-traduz)
  .venv/bin/python guia/src/tudo.py --sem-traduzir   não chama o tradutor (para se houver texto sem tradução)
  .venv/bin/python guia/src/tudo.py --so-conferir    só as conferências

Ordem:
  1. imagens.py                       cópias de 1200 px dos renders em guia/assets/ (entrada)
  2. por robô (dino, capivara, cubo, cubo-rodas): pagina_robo.py imagens → traduzir → pagina
  3. traduzir.py → montar.py          entrada
  4. evolucao.py traduzir → pagina    evolução (as imagens de guia/evolucao/assets/ vêm de comum/cad/evolucao.py)
  5. pagina_robo.py conferir <robô>   (página, docs e zip de cada robô) e conferir_guia.py (todas as páginas)

O que este comando NÃO faz (é de quem mexe no modelo): gerar peças, verificar, renderizar, `comum/cad/evolucao.py`,
`comum/cad/tabelas.py`, e `pagina_robo.py docs|zip <robô>` (documentos e zip em projetos/<robô>/). A única coisa que ele
escreve fora de guia/ é projetos/<robô>/ligacao.<idioma>.svg, regravado igual pelo passo `pagina`.
Se o modelo de um robô mudou, rode antes `pagina_robo.py docs <robô> pt`, `traduzir`, `docs`, `zip` (ver README, passos 15–17).
"""
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
import montar  # noqa: E402

PY = sys.executable


def roda(*args):
    print("\n$ " + " ".join(["python", *[str(a).replace(str(RAIZ) + "/", "") for a in args]]), flush=True)
    r = subprocess.run([PY, *map(str, args)], cwd=RAIZ)
    if r.returncode:
        print(f"\nFalhou: guia/src/tudo.py — o passo acima saiu com código {r.returncode}")
        sys.exit(r.returncode)


def main():
    t0 = time.time()
    traduz = "--sem-traduzir" not in sys.argv
    if "--so-conferir" not in sys.argv:
        roda(AQUI / "imagens.py")
        for m in montar.MODELOS:
            roda(AQUI / "pagina_robo.py", "imagens", m)
            if traduz:
                roda(AQUI / "pagina_robo.py", "traduzir", m)
            roda(AQUI / "pagina_robo.py", "pagina", m)
        if traduz:
            roda(AQUI / "traduzir.py")
        roda(AQUI / "montar.py")
        if traduz:
            roda(AQUI / "evolucao.py", "traduzir")
        roda(AQUI / "evolucao.py", "pagina")
    for m in montar.MODELOS:
        roda(AQUI / "pagina_robo.py", "conferir", m)
    roda(AQUI / "conferir_guia.py")
    print(f"\nTerminei: guia regenerado e conferido ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
