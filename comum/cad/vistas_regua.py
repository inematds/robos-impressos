#!/usr/bin/env python3
"""As 4 vistas de cada robô, tiradas da régua de semelhança (`REFERENCIAS` de comum/cad/comparar.py, ângulos nominais).

Uma lista só para tudo o que mostra "as mesmas vistas da referência": `vistas.sh` (folha `<id>-vistas.jpg`) e
`evolucao.py` (antes × depois da página /guia/evolucao/). Não muda nem lê nada do protocolo da régua.

  .venv/bin/python comum/cad/vistas_regua.py dino      → uma linha "nome az el" por vista

Bicho com folha de 4 vistas (dino, capivara): as 4 da régua, na ordem da folha.
Cubos: a referência tem UMA vista (três-quartos, az +35 / el 22); a folha leva essa e mais três na mesma elevação
(frente, três-quartos pelo outro lado, costas), para o robô aparecer por todos os lados.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # raiz de import: comum/
from cad.caminhos import id_de  # noqa: E402
from cad.comparar import REFERENCIAS, referencia_de  # noqa: E402


def vistas(modelo: str) -> list[tuple[str, float, float]]:
    """[(nome, azimute, elevação)] — azimute 0 = frente; negativo = o robô olha para a ESQUERDA da imagem."""
    vs = REFERENCIAS[referencia_de(id_de(modelo))]["vistas"]
    if len(vs) >= 4:
        return [(v["nome"], float(v["az"]), float(v["el"])) for v in vs[:4]]
    v = vs[0]
    az, el = float(v["az"]), float(v["el"])
    return [("frente", 0.0, el), (v["nome"], az, el), (v["nome"] + "-outro-lado", -az, el), ("costas", 180.0, el)]


if __name__ == "__main__":
    for nome, az, el in vistas(sys.argv[1]):
        print(nome, f"{az:g}", f"{el:g}")
