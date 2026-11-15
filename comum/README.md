# comum — o que os quatro robôs dividem

Cada robô mora na sua pasta em [`projetos/`](../projetos/). Aqui fica o que é de todos: o código que desenha e
confere as peças e as peças impressas iguais em mais de um robô.

| Pasta | O que tem |
|---|---|
| `cad/` | Todo o código (pacote Python `cad`): medidas, biblioteca de formas, gerador, verificador, renders, tabelas |
| `cad/parametros.py` | **Todas as medidas** num arquivo só |
| `cad/caminhos.py` | Registro único dos robôs: id do modelo → pasta em `projetos/` |
| `cad/comum/` | Biblioteca: geometria, componentes comprados, esqueleto e casca dos bichos, robôs quadrados, imprimibilidade |
| `cad/peles/` | Pele dos bichos (grade de distância que o gerador lê) |
| `pecas/stl/`, `pecas/3mf/` | Peças iguais em mais de um robô, já na posição de impressão |
| `legado/` | Peças comuns da versão 1.0.2 que nenhum robô usa mais (veja o [LEIA-ME](legado/LEIA-ME.md)) |

## Peças comuns e quem usa

| Arquivo (`pecas/stl/`) | Dinossauro | Capivara | Cubo | Cubo que roda |
|---|---|---|---|---|
| `comum-teste-encaixe.stl` (cupom de teste) | sim | sim | sim | sim |
| `comum-garfo-pescoco.stl` | sim | sim | | |
| `comum-berco-tilt.stl` | sim | sim | | |
| `comum-capa-esfera.stl` | sim | sim | | |

No `montagem.json` de cada robô, a peça comum aparece com o caminho relativo `../../comum/pecas/stl/comum-<peça>.stl`.

## O que tem em cada `projetos/<robô>/`

- `modelo.py`: o desenho do robô (`construir() -> Modelo`), lido pelo gerador.
- `stl/` e `3mf/`: uma peça por arquivo, **já na posição de impressão** (mm).
- `mesas/`: um 3MF por mesa de impressão (peças juntas por material e cor); `mesas.json` é a lista.
- `montagem.json`: onde cada peça vai no robô montado, juntas, poses e estimativas.
- `montagem.glb`: o robô montado num arquivo só (abre no Blender ou em qualquer visualizador glTF).
- `componentes/`: envelopes dos componentes comprados. **Não imprimir.**
- `verificacao.json` e `verificacao-saida.txt`: resultado do verificador.
- `imagens/`: renders do robô.

Pastas: `dino`, `capivara`, `cubo`, `cubo-rodas`. O id do cubo que roda no código e no nome dos STL é `cubo_rodas`.

## Comandos (na raiz do repo, com o venv)

```
.venv/bin/python comum/cad/gerar.py <id|todos>        # STL, 3MF, mesas, montagem.json   (id: dino, capivara, cubo, cubo_rodas)
.venv/bin/python comum/cad/verificar.py <id|todos>    # 11 testes; sai com 1 se algum falhar
.venv/bin/python comum/cad/depurar.py <id>            # volume, corpos e caixa de cada peça, sem exportar
.venv/bin/python comum/cad/onde.py <id> [pose]        # onde cada par de peças se sobrepõe
.venv/bin/python comum/cad/comum/imprimibilidade.py <id> [peça]   # áreas sem apoio de cada peça
.venv/bin/python comum/cad/comparar.py <id> --sem-gravar          # semelhança com a referência (IoU)
.venv/bin/python comum/cad/tabelas.py                 # tabelas de projetos/TABELAS.md e dos docs
comum/cad/vistas.sh <id> <saida.png> 600x600 40       # 4 vistas rápidas (Blender)
comum/cad/renders.sh <id>                             # renders finais em projetos/<robô>/imagens/
```

Robô novo: uma linha em `cad/caminhos.py`, uma seção em `cad/parametros.py` e `projetos/<pasta>/modelo.py`.

Peças com "esq" no nome são espelhadas. Tempo e filamento são **estimativas por volume** (sem fatiador).
