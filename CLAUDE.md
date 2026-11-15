# CLAUDE.md — robos-impressos

Robôs de ~30 cm para imprimir na **Bambu Lab A1** (mesa 256×256×256 mm), com Arduino Uno e/ou Raspberry Pi.
Quatro modelos no mesmo repo: **dino**, **capivara**, **cubo** (de mesa, cabeça-cubo com tela) e **cubo-rodas** (≥ 30 cm, roda).
Fase 1 = mecânica e encaixe. Fase 2 (voz, câmera, sensores, localização em casa, IA por `claude -p`) vem depois.

- Repo: `inematds/robos-impressos` (público). Autor dos commits: `inematds <inematds@gmail.com>`.
- Guia: https://inematds.github.io/robos-impressos/guia/ (PT, `/en/`, `/es/`). Portal: entrada id 10225.
- Referências visuais do Nei: `referencia/` (fora do repo público; não publicar sem o Nei decidir).
- Gerar peças: `.venv/bin/python cad/gerar.py todos`. Verificar: `.venv/bin/python cad/verificar.py todos`.
- Image-to-3D local (Hunyuan3D-2, GPU, sem API): `.venv-i23d` + `cad/imagem3d.py`; trabalho de GPU por `~/projetos/wifi/scripts/fila-vaga gpu robos -- <cmd>`.

## Ao começar uma sessão
1. Ler `handoffs/latest.md`.
2. Ler a execução longa em andamento: `longrun/2026-11-14-rodada2-separar-energia-design/` (goal → state → plan → canal → decisions → failures; briefs E3 e E5).
3. Modelo pedido pelo Nei para este projeto: **Fable 5.2, esforço high**.

## Regras do projeto
- Nenhuma API externa (Magnific, fal, Replicate, Tripo cloud...) sem autorização explícita. GitHub e Telegram liberados.
- Tradução só por `inema-traduz`. Imagem: Codex image_gen (assinatura); banner deve sair dos renders reais.
- Toda peça: cabe em 256 mm, parede ≥ 2 mm, imprimível sem suporte sempre que der, reforços nos pontos de carga.
- Commit a cada pacote verificado (a sessão já caiu uma vez e perdeu trabalho não commitado).
- No fim da rodada: avisar o Nei no v3 com `~/projetos/wifi/scripts/avisa-v3.sh "<msg>"` e citar o "msg N".

## Self-learning
Quando o Nei corrigir ou você notar um erro: antes de seguir, escreva a lição como uma linha no TOPO da seção Lessons abaixo.

## Lessons
- Casca recortada de malha: nenhum dos 11 testes vê buraco na casca nem peça abaixo do chão; depois de cada mudança de casca, render de 1200 px COM componentes + mapa em corte das juntas, e conferir no arquivo o parâmetro que a conta pediu (14/11/2026, E3b).
- Sessão longa com subagentes cai junto com a sessão: commit a cada pacote verificado e estado no state.md, senão o trabalho some (14/11/2026).
