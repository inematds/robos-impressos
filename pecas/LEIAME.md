# Peças

- `dino/`, `capivara/`, `cubo/`: peças de cada modelo. Dentro de cada um:
  - `stl/` e `3mf/`: uma peça por arquivo, **já na posição de impressão** (mm).
  - `mesas/`: um 3MF por mesa de impressão (peças juntas por material e cor); `mesas.json` é a lista.
  - `montagem.json`: onde cada peça vai no robô montado, juntas, poses e estimativas.
  - `montagem.glb`: o robô montado num arquivo só (abre no Blender ou em qualquer visualizador glTF).
  - `componentes/`: envelopes dos componentes comprados. **Não imprimir.**
  - `verificacao.json`: saída do `cad/verificar.py`.
- `comum/`: peças iguais no dinossauro e na capivara (chassi, bandejas, garfo, berço, capa da esfera, pino, bucha)
  e a peça de teste (`comum-teste-encaixe.stl`), que serve para os três.
- `TABELAS.md`: tabelas geradas por `cad/tabelas.py`.

Peças com "esq" no nome são espelhadas. Quantidades, material, cor e suporte: `TABELAS.md` ou `PLANO.md`.
Tempo e filamento são **estimativas por volume** (sem fatiador).
