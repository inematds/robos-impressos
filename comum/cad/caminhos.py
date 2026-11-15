#!/usr/bin/env python3
"""Registro ÚNICO dos robôs e dos caminhos do repo. Todo script pergunta aqui onde ficam as coisas.

Estrutura:
  comum/cad/                 todo o código (este pacote `cad`; a raiz de import é `comum/`)
  comum/pecas/{stl,3mf}/     peças iguais em mais de um robô (gravadas pelo gerar.py)
  projetos/<pasta>/          um robô: modelo.py + stl/ 3mf/ mesas/ componentes/ imagens/ + montagem.json,
                             montagem.glb, mesas.json, verificacao.json, verificacao-saida.txt e os docs

O id do modelo (usado no código, em `parametros.py` e no nome dos STL) não muda; só a PASTA do cubo que roda
tem hífen. Robô novo = uma linha em MODELOS + `projetos/<pasta>/modelo.py` com `construir() -> Modelo`.

Uso em shell (os .sh pegam a pasta por aqui):
  .venv/bin/python comum/cad/caminhos.py cubo_rodas      → /…/projetos/cubo-rodas
  .venv/bin/python comum/cad/caminhos.py --id cubo-rodas → cubo_rodas (o id, venha o id ou o nome da pasta)
  .venv/bin/python comum/cad/caminhos.py                 → uma linha "id pasta" por robô
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]            # raiz do repo
DIR_CODIGO = RAIZ / "comum"                            # raiz de import do pacote `cad`
DIR_PROJETOS = RAIZ / "projetos"
DIR_PECAS_COMUNS = RAIZ / "comum" / "pecas"
DIR_PELES = RAIZ / "comum" / "cad" / "peles"
DIR_PREVIA = RAIZ / ".preview"                         # temporários, fora do git

# id do modelo → pasta em projetos/ (a ordem é a do `todos`)
MODELOS = {"dino": "dino", "capivara": "capivara", "cubo": "cubo", "cubo_rodas": "cubo-rodas"}


def id_de(nome: str) -> str:
    """Aceita o id (`cubo_rodas`) ou o nome da pasta (`cubo-rodas`) e devolve o id."""
    if nome in MODELOS:
        return nome
    for i, p in MODELOS.items():
        if p == nome:
            return i
    raise SystemExit(f"modelo desconhecido: '{nome}' (há: {', '.join(MODELOS)})")


def pasta(modelo: str) -> Path:
    """Pasta do robô: projetos/<pasta>/."""
    return DIR_PROJETOS / MODELOS[id_de(modelo)]


def rel_comum(modelo: str, sub: str, arquivo: str) -> str:
    """Caminho de uma peça comum RELATIVO à pasta do robô (é o que vai no campo `arquivo` do montagem.json)."""
    return os.path.relpath(DIR_PECAS_COMUNS / sub / arquivo, pasta(modelo)).replace(os.sep, "/")


def construir(modelo: str):
    """Carrega projetos/<pasta>/modelo.py pelo caminho e devolve o `Modelo` de `construir()`."""
    modelo = id_de(modelo)
    if str(DIR_CODIGO) not in sys.path:
        sys.path.insert(0, str(DIR_CODIGO))
    arq = pasta(modelo) / "modelo.py"
    spec = importlib.util.spec_from_file_location(f"modelo_{modelo}", arq)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.construir()


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--id":
        print(id_de(sys.argv[2]))
    elif len(sys.argv) > 1:
        print(pasta(sys.argv[1]))
    else:
        for i, p in MODELOS.items():
            print(i, p)
