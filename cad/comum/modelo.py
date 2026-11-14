"""Estruturas de dados de um modelo: peças impressas, componentes comprados, juntas e poses."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from manifold3d import Manifold

from cad.comum.geo import mat_giro

EYE = np.eye(4)


def rot(eixo: str, graus: float) -> np.ndarray:
    e = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[eixo]
    return mat_giro((0, 0, 0), e, graus)


@dataclass
class Peca:
    nome: str
    solido: Manifold                 # na posição de montagem (1ª cópia)
    material: str = "PLA"
    cor: str = "cinza"
    grupo: str = "corpo"             # grupo cinemático
    imprimir: np.ndarray = field(default_factory=lambda: EYE.copy())   # rotação montagem -> mesa
    suporte: str = "não"
    comum: bool = False              # peça igual em mais de um modelo (vai para pecas/comum)
    copias: list = field(default_factory=lambda: [EYE.copy()])         # 4x4 aplicadas ao sólido
    grupos: list | None = None       # grupo de cada cópia (se diferente)
    explode: tuple = (0.0, 0.0, 0.0)
    macica: bool = False             # peça maciça (estimativa usa casca + miolo)
    obs: str = ""
    liso: bool = True
    # impressão (teste 10 "imprimibilidade" e tabela por peça). `suporte` acima: "não" ou "sim (onde, tipo)"
    perimetros: int = 3              # nº de paredes; 4–5 nas peças estruturais
    infill: int = 15                 # % de preenchimento
    reforco: str = ""                # motivo dos reforços (nervura, ressalto do inserto, filete, camadas ao longo da carga…)
    orientacao: str = ""             # texto curto: qual face vai na mesa


@dataclass
class Comp:
    nome: str
    solido: Manifold
    grupo: str = "corpo"
    massa: float = 0.0
    cor: str = "grafite"
    copias: list = field(default_factory=lambda: [EYE.copy()])
    grupos: list | None = None
    fase2: bool = False              # componente só da fase 2 (espaço reservado)
    explode: tuple = (0.0, 0.0, 0.0)


@dataclass
class Junta:
    pai: str | None
    origem: tuple = (0, 0, 0)
    eixo: tuple = (0, 0, 1)
    lim: tuple = (0.0, 0.0)


@dataclass
class Modelo:
    nome: str
    titulo: str
    pecas: list
    comps: list
    juntas: dict                      # grupo -> Junta (grupo 'corpo' não tem junta)
    apoios: list                      # pontos (x, y) de contato com o chão
    poses: list                       # [(nome, {grupo: graus})]
    obs: dict = field(default_factory=dict)
    encaixes: list = field(default_factory=list)   # pares que se sobrepõem de propósito: [{'par': [a, b], 'motivo': ...}]
    ordem: list = field(default_factory=list)      # ordem de montagem: [{'passo': texto, 'move': [nomes], 'dir': (x,y,z) de onde vem, 'contra': [nomes] ou None}]

    def matriz_grupo(self, grupo: str, angulos: dict) -> np.ndarray:
        M = EYE.copy()
        g = grupo
        while g in self.juntas:
            j = self.juntas[g]
            M = mat_giro(j.origem, j.eixo, angulos.get(g, 0.0)) @ M
            g = j.pai
        return M
