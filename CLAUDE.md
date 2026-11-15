# CLAUDE.md — robos-impressos

Robôs de ~30 cm para imprimir na **Bambu Lab A1** (mesa 256×256×256 mm), com Arduino Uno e/ou Raspberry Pi.
Quatro modelos no mesmo repo: **dino**, **capivara**, **cubo** (de mesa, cabeça-cubo com tela) e **cubo-rodas** (≥ 30 cm, roda).
Fase 1 = mecânica e encaixe. Fase 2 (voz, câmera, sensores, localização em casa, IA por `claude -p`) vem depois.

- Repo: `inematds/robos-impressos` (público). Autor dos commits: `inematds <inematds@gmail.com>`.
- Guia: https://inematds.github.io/robos-impressos/guia/ (PT, `/en/`, `/es/`). Portal: entrada id 10225.
- Referências visuais do Nei: `referencia/` (fora do repo público; não publicar sem o Nei decidir).
- Estrutura (desde 14/11/2026): `projetos/<robô>/` = um robô inteiro (`modelo.py`, `stl/`, `3mf/`, `mesas/`, `componentes/`, `imagens/`, `montagem.json`, `verificacao.json`, `verificacao-saida.txt`, docs); `comum/cad/` = todo o código; `comum/pecas/` = peças iguais em mais de um robô; `comum/legado/` = peças da v1.0.2 que nenhum robô usa. Pastas: `dino`, `capivara`, `cubo`, `cubo-rodas` (id no código: `cubo_rodas`). Registro único id → pasta: `comum/cad/caminhos.py`.
- Gerar peças: `.venv/bin/python comum/cad/gerar.py <id|todos>`. Verificar: `.venv/bin/python comum/cad/verificar.py <id|todos>` (11 testes; 4 × `TUDO PASSOU`).
- Outros: `comum/cad/depurar.py <id>`, `comum/cad/onde.py <id> [pose]`, `comum/cad/comum/imprimibilidade.py <id> [peça]`, `comum/cad/comparar.py <id> --sem-gravar` (sem a opção, regrava `comparacao/`), `comum/cad/tabelas.py`, `comum/cad/vistas.sh <id> <saida.png>`, `comum/cad/renders.sh <id>` (saída em `projetos/<robô>/imagens/`).
- Página de um robô no guia: `.venv/bin/python guia/src/pagina_robo.py docs|pagina|zip|conferir <robô>` (não rodar `traduzir` sem necessidade: retraduz texto aprovado).
- Depois de `gerar.py`: os 3MF saem com bytes diferentes a cada rodada mesmo sem mudar a geometria, e os STL comuns do berço e da capa (`comum/pecas/stl/`) mudam em ruído de 1e-6 conforme o robô que os grava. Antes do commit: se NENHUM STL de `projetos/*/stl` mudou (`git status`), `git restore -- ':(glob)**/*.3mf'`; os 2 STL comuns só voltam (`git restore comum/pecas/stl`) se nada da geometria comum (garfo, berço, capa, cupom: `comum/cad/comum/base*.py`, `parametros.py`) foi tocado. Se a geometria mudou, commit de tudo (STL + 3MF + `montagem.json` + `verificacao.json`) junto.
- Image-to-3D local (Hunyuan3D-2, GPU, sem API): `.venv-i23d` + `comum/cad/imagem3d.py`; trabalho de GPU por `~/projetos/wifi/scripts/fila-vaga gpu robos -- <cmd>`.

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
- Texto de montagem ou medida herdado de outro robô: conferir no modelo DESTE robô o furo, o caminho e o número (ex.: carregador da capivara fica fora da porta e não passa no furo de 7 mm; a folga sobre o Pi muda de 17 para 19 mm) antes de escrever "já vem soldado" ou "medida do modelo" (14/11/2026).
- Casca recortada de malha: nenhum dos 11 testes vê buraco na casca nem peça abaixo do chão; depois de cada mudança de casca, render de 1200 px COM componentes + mapa em corte das juntas, e conferir no arquivo o parâmetro que a conta pediu (14/11/2026, E3b).
- Sessão longa com subagentes cai junto com a sessão: commit a cada pacote verificado e estado no state.md, senão o trabalho some (14/11/2026).
