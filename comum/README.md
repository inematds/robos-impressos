# comum — o que os quatro robôs dividem

Cada robô mora na sua pasta em [`projetos/`](../projetos/). Aqui fica o que é de todos: o código que desenha e
confere as peças e as peças impressas iguais em mais de um robô. As decisões que valem para os quatro estão no
[PLANO.md da raiz](../PLANO.md).

| Pasta | O que tem |
|---|---|
| `cad/` | Todo o código (pacote Python `cad`): medidas, biblioteca de formas, gerador, verificador, renders, tabelas |
| `cad/parametros.py` | **Todas as medidas** num arquivo só |
| `cad/caminhos.py` | Registro único dos robôs: id do modelo → pasta em `projetos/` |
| `cad/comum/` | Biblioteca: geometria, componentes comprados, esqueleto e casca dos bichos, robôs quadrados, imprimibilidade |
| `cad/peles/` | Pele dos bichos (grade de distância que o gerador lê) |
| `pecas/stl/`, `pecas/3mf/` | Peças iguais em mais de um robô, já na posição de impressão |

## Peças comuns e quem usa

| Arquivo (`pecas/stl/`) | Dinossauro | Capivara | Cubo | Cubo que roda |
|---|---|---|---|---|
| `comum-teste-encaixe.stl` (cupom de teste) | sim | sim | sim | sim |
| `comum-garfo-pescoco.stl` | sim | sim | | |
| `comum-berco-tilt.stl` | sim | sim | | |
| `comum-capa-esfera.stl` | sim | sim | | |

No `montagem.json` de cada robô, a peça comum aparece com o caminho relativo `../../comum/pecas/stl/comum-<peça>.stl`.
O zip de cada robô (`projetos/<robô>/<robô>-stl.zip`) já leva as peças comuns que ele usa.

## O que mais é comum, além das peças

| O quê | Onde | Quem usa |
|---|---|---|
| Medidas dos componentes comprados, com a fonte | `cad/parametros.py` | os 4 |
| Cabeça dos bichos: crânio, mandíbula, olhos com bolso de sensor, mesa da cabeça | `cad/comum/bicho.py` | dinossauro e capivara |
| Casca a partir da pele (malha da imagem), cortes em vasos, peças em relevo | `cad/comum/casca.py`, `cad/peles/` | dinossauro e capivara |
| Esqueleto baixo (chassi, bandejas) | `cad/comum/base_baixa.py` | capivara (o dinossauro tem o dele, em `projetos/dino/modelo.py`, e reaproveita a bandeja do Raspberry Pi) |
| Garfo do pescoço, berço do tilt, capa da esfera, cupom de teste | `cad/comum/base.py` | dinossauro e capivara (o cupom, os 4) |
| Cabeça-cubo, pescoço com engrenagens 2:1 e tubo oco, servo de pan | `cad/comum/quadrado.py` | os 2 robôs quadrados |
| Berço dos módulos de energia (4 cantoneiras + abraçadeira) | `cad/comum/geo.py › berco_modulo` | os 4 |
| Teste de imprimibilidade (área sem apoio de cada peça) | `cad/comum/imprimibilidade.py` | os 4 |
| Eletrônica de base: Raspberry Pi, Arduino Uno + Sensor Shield, servos MG996R, baterias 18650 com placa de proteção, carga USB-C, UBEC de 6 V, serial de 3 fios entre as placas | `projetos/<robô>/LIGACAO.md` | os 4 (os 3 que rodam somam o driver L298N) |

## O que tem em cada `projetos/<robô>/`

- `modelo.py`: o desenho do robô (`construir() -> Modelo`), lido pelo gerador.
- `stl/` e `3mf/`: uma peça por arquivo, **já na posição de impressão** (mm).
- `mesas/`: um 3MF por mesa de impressão (peças juntas por material e cor); `mesas.json` é a lista.
- `montagem.json`: onde cada peça vai no robô montado, juntas, poses e estimativas.
- `montagem.glb`: o robô montado num arquivo só (abre no Blender ou em qualquer visualizador glTF).
- `componentes/`: envelopes dos componentes comprados. **Não imprimir.**
- `verificacao.json` e `verificacao-saida.txt`: resultado do verificador.
- `imagens/`: renders do robô.
- `README.md`, `PLANO.md`, `LISTA-DE-COMPRAS.md`, `IMPRIMIR.md`, `LIGACAO.md` (+ `.en.md` e `.es.md` dos três últimos),
  `ligacao.<idioma>.svg`, `firmware/` e `<robô>-stl.zip`: os documentos e o pacote de cada robô. Os blocos entre
  `<!-- GERADO:... -->` são preenchidos por `guia/src/pagina_robo.py` a partir de `guia/src/robos/<robô>.dados.json`.

Pastas: `dino`, `capivara`, `cubo`, `cubo-rodas`. O id do cubo que roda no código e no nome dos STL é `cubo_rodas`.

## Comandos (na raiz do repo, com o venv)

```
.venv/bin/python comum/cad/gerar.py <id|todos>        # STL, 3MF, mesas, montagem.json   (id: dino, capivara, cubo, cubo_rodas)
.venv/bin/python comum/cad/verificar.py <id|todos>    # 11 testes; sai com 1 se algum falhar
.venv/bin/python comum/cad/depurar.py <id>            # volume, corpos e caixa de cada peça, sem exportar
.venv/bin/python comum/cad/onde.py <id> [pose]        # onde cada par de peças se sobrepõe
.venv/bin/python comum/cad/comum/imprimibilidade.py <id> [peça]   # áreas sem apoio de cada peça
.venv/bin/python comum/cad/comparar.py <id> --sem-gravar          # semelhança com a referência (IoU)
.venv/bin/python comum/cad/tabelas.py --docs          # tabelas de projetos/TABELAS.md, do PLANO.md e dos README da raiz (sem --docs, também as do guia)
.venv/bin/python guia/src/pagina_robo.py docs <robô> pt        # blocos gerados dos documentos de um robô (robô = pasta: dino, capivara, cubo, cubo-rodas)
.venv/bin/python guia/src/pagina_robo.py traduzir <robô>       # inglês e espanhol pelo inema-traduz (só o que mudou)
.venv/bin/python guia/src/pagina_robo.py docs <robô>           # documentos .en.md e .es.md
.venv/bin/python guia/src/pagina_robo.py esquema <robô>        # esquema de ligação (SVG) nos 3 idiomas
.venv/bin/python guia/src/pagina_robo.py zip <robô>            # <robô>-stl.zip
.venv/bin/python guia/src/pagina_robo.py conferir <robô>       # links, idiomas e zip
.venv/bin/python guia/src/tudo.py                         # o guia inteiro (entrada, página de cada robô, evolução) e as conferências
comum/cad/vistas.sh <id> <saida.png> 600x600 40       # 4 vistas rápidas (Blender)
comum/cad/renders.sh <id>                             # renders finais em projetos/<robô>/imagens/
```

Robô novo: uma linha em `cad/caminhos.py`, uma seção em `cad/parametros.py` e `projetos/<pasta>/modelo.py`.

Peças com "esq" no nome são espelhadas. Tempo e filamento são **estimativas por volume** (sem fatiador).
