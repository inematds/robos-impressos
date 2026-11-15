# Como imprimir o dinossauro

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impressora de referência: Bambu Lab A1 (mesa de 256 × 256 × 256 mm), bico de 0,4 mm, camada de 0,2 mm.

Sugestão de ajuste, ainda não testada com estas peças:

- Placa PEI texturizada para os dois materiais.
- No Bambu Studio, perfil Generic PLA para o PLA e Generic PETG para o PETG, com as temperaturas que o perfil traz.
- Valores usuais, para você conferir: PLA com bico a 220 °C e mesa a 55–65 °C; PETG com bico a 250–255 °C e mesa a 70–80 °C. O [guia de filamentos da Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) dá de 240 a 270 °C para o bico no PETG.

Página com as mesmas tabelas: https://inematds.github.io/robos-impressos/guia/dino/#imprimir

## Os arquivos já estão na posição de impressão

- Cada STL de `projetos/dino/stl/` está na posição em que deve ser impresso: a face de apoio em Z = 0. Abra no fatiador e
  imprima sem girar.
- Cada 3MF de `projetos/dino/mesas/` traz as peças de uma cor já arrumadas numa mesa de 256 mm.
- Tudo de uma vez: [dino-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/dino-stl.zip)
  (os STL, os 3MF das mesas, o programa do Arduino e os guias).
- Como foi conferido (14/11/2026): em cada STL, a caixa da peça é igual ao tamanho "na mesa" da tabela abaixo e o
  ponto mais baixo está em Z = 0.
- Os 3MF são genéricos: só geometria e posição, sem perfil nem cor. Foram relidos por script, mas ainda não foram
  abertos no Bambu Studio. Se algum não abrir, use os STL.

## Seis peças pedem suporte

As outras saem sem suporte. Nestas seis, ligue o suporte no fatiador (em árvore, onde a tabela não diz outra coisa).
Em nenhuma o suporte encosta no rosto nem num encaixe.

| Peça | Onde vai o suporte | Aparece? |
|---|---|---|
| Crânio | Por dentro: teto do crânio, fundo dos copos dos olhos e nervura da crista. Por baixo: borda do céu da boca. | Não. Nada no rosto. |
| Corpo | Por dentro: teto das 2 coxas, sobre as rodas, e degraus dos assentos planos (2,3 % da área). | Não. |
| Traseira | Por dentro: teto de cima da anca e nervura do rasgo da crista (2,4 % da área). | Não. |
| Mandíbula | Sob o recorte redondo de trás, virado para o pescoço. | Não. |
| Garfo do pescoço | 1,8 mm sob a base, em volta do anel do horn. Suporte normal. | Não: fica dentro da gola. |
| Berço do tilt | Pouco, sob a ponte entre as 2 paredes do servo. | Não: fica dentro da gola. |

O verificador do projeto mede a área sem apoio de cada peça e reprova a que foi declarada sem suporte e precisaria
dele. Ninguém tirou ainda o suporte de uma destas peças impressas: comece por uma peça pequena, como a mandíbula.

## 1. Imprima primeiro o cupom de teste

**Nada deste projeto foi impresso ainda.** O cupom de teste (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está na mesa 05. Teste nele:

- um inserto M3 em cada um dos 3 furos (3,9, 4,0 e 4,1 mm);
- um parafuso M3 no furo passante (3,4 mm) e outro no furo de rosquear direto no plástico (2,7 mm);
- o micro servo na janela e o eixo do motor das rodas no furo dele;
- os furos M2,5 (Raspberry Pi) e M2 (parafusos dos micro servos), de rosquear direto no plástico.

A covinha marca a medida que o projeto usa. Se outro furo ficar melhor na sua impressora, você não precisa refazer as
peças: no Bambu Studio, a opção X-Y hole compensation (compensação de furo X-Y; aba Qualidade, grupo Precisão, com o
modo avançado ligado) abre ou fecha todos os furos da peça: valor positivo abre, negativo fecha
([fonte: código do Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
A fonte não diz se o valor conta por lado ou no diâmetro: comece com 0,05 mm e imprima o cupom de novo. O cupom decide.

Quem mexe no código pode mudar o valor no bloco `FOLGA` de `comum/cad/parametros.py` e gerar as peças de novo
(`.venv/bin/python comum/cad/gerar.py dino`).

Três avisos:

- O cupom é comum aos outros robôs do projeto. Os 3 soquetes de pino dele não são usados neste robô.
- O encaixe do servo MG996R não está no cupom. Confira o servo no berço do tilt (mesa 02, a terceira da ordem abaixo),
  antes das impressões longas.
- O cupom sai em PLA, mas 7 dos 13 insertos ficam em peças de PETG (chassi, berço e garfo). Imprima um segundo cupom em PETG. Ele não está em nenhuma mesa nem nos totais: carregue o arquivo `comum-teste-encaixe.stl` à parte, com PETG, e conte cerca de 15 g e 38 minutos a mais.

## 2. Ordem sugerida das mesas

Primeiro as peças pequenas e o esqueleto; por último as impressões longas: o crânio, a traseira e o corpo.

<!-- GERADO:mesas -->
| Ordem | Arquivo da mesa | Material e cor | Peças | Filamento (g) | Tempo (h) | Por que nesta ordem |
|---|---|---|---|---|---|---|
| 1 | [dino-mesa-05-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-05-pla-cinza.3mf) | PLA cinza | Cupom de teste (teste-encaixe) | 15 | 0,6 | Comece por aqui. O cupom de teste mostra se os insertos, os parafusos M3, o micro servo e o eixo do motor entram com a folga certa na SUA impressora. Menos de 1 hora. |
| 2 | [dino-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-01-petg-amarelo.3mf) | PETG amarelo | Bandeja do Raspberry Pi (bandeja-pi), Bandeja do Arduino (bandeja-uno) | 28 | 1,2 | As 2 bandejas: peças pequenas que já testam os furos do Raspberry Pi e do Arduino. |
| 3 | [dino-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-02-petg-grafite.3mf) | PETG grafite | Chassi (chassi), Mesa da cabeça (mesa-cabeca), Garfo do pescoço (garfo-pescoco), Capa da esfera (capa-esfera), Berço do tilt (berco-tilt), 2 × Cubo do braço (cubo-braco) | 243 | 9,4 | O esqueleto inteiro em PETG: chassi, mesa da cabeça, garfo, berço, capa da esfera e os 2 cubos dos braços. Garfo e berço pedem suporte. Confira no berço se o servo MG996R entra, antes das impressões longas. |
| 4 | [dino-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-04-pla-branco.3mf) | PLA branco | Olho direito (olho), Olho esquerdo (olho-esq) | 28 | 1,2 | Os 2 olhos. |
| 5 | [dino-mesa-03-pla-azul.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-03-pla-azul.3mf) | PLA azul | Crista da cabeça (crista-cabeca), Crista das costas (crista-costas), Íris direita (iris), Íris esquerda (iris-esq) | 42 | 1,9 | Cristas e íris, em azul. |
| 6 | [dino-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-07-pla-preto.3mf) | PLA preto | Pupila direita (pupila), Pupila esquerda (pupila-esq) | 4 | 0,3 | As 2 pupilas. |
| 7 | [dino-mesa-12-pla-verde-escuro.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-12-pla-verde-escuro.3mf) | PLA verde-escuro | Mancha do flanco direito (mancha-dir), Mancha do flanco esquerdo (mancha-esq) | 4 | 0,4 | As 2 manchas dos flancos. |
| 8 | [dino-mesa-06-pla-creme.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-06-pla-creme.3mf) | PLA creme | Barriga (barriga), Dedo do pé direito 3 (dedo-dir-3), Dedo do pé esquerdo 3 (dedo-esq-3), Dedo do pé direito 1 (dedo-dir-1), Dedo do pé direito 2 (dedo-dir-2), Dedo do pé esquerdo 1 (dedo-esq-1), Dedo do pé esquerdo 2 (dedo-esq-2) | 28 | 1,5 | Barriga e os 6 dedos dos pés: a face de colar vai na mesa. |
| 9 | [dino-mesa-11-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-11-pla-verde.3mf) | PLA verde | Mandíbula (mandibula) | 34 | 1,4 | Mandíbula: em pé, com um pouco de suporte atrás. |
| 10 | [dino-mesa-09-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-09-pla-verde.3mf) | PLA verde | Traseira (anca e cauda) (traseira) | 102 | 3,9 | Traseira: em pé sobre a costura, com suporte em árvore só por dentro. |
| 11 | [dino-mesa-08-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-08-pla-verde.3mf) | PLA verde | Crânio (cranio) | 179 | 6,8 | Crânio: suporte em árvore por dentro e sob o céu da boca. Nenhum suporte no rosto. |
| 12 | [dino-mesa-10-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-10-pla-verde.3mf) | PLA verde | Corpo (corpo), Gola do pescoço (gola), Braço direito (braco-dir), Braço esquerdo (braco-esq) | 295 | 11,3 | Corpo, gola e os 2 braços: a impressão mais longa. Deixe por último, com a impressora já ajustada. O corpo leva suporte em árvore só por dentro. |
| **Total** |  |  |  | **1002** | **39,9** |  |
<!-- /GERADO -->

## 3. Peça por peça

"Paredes" é o número de perímetros. A coluna "Suporte" diz se a peça pede suporte e onde. O nome entre parênteses é o
nome do arquivo.

<!-- GERADO:pecas -->
| Peça | Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Barriga (barriga) | [dino-barriga.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-barriga.stl) | 1 | PLA creme | 63,4 × 79,4 × 13,3 | base plana (face de colar) na mesa | não | 3 | 15 % | 22 | 0,9 |
| Dedo do pé direito 1 (dedo-dir-1) | [dino-dedo-dir-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-1.stl) | 1 | PLA creme | 17,2 × 12,7 × 8,5 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Dedo do pé direito 2 (dedo-dir-2) | [dino-dedo-dir-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-2.stl) | 1 | PLA creme | 17 × 12,7 × 7,4 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Dedo do pé direito 3 (dedo-dir-3) | [dino-dedo-dir-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-3.stl) | 1 | PLA creme | 12,7 × 17,4 × 6,9 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Dedo do pé esquerdo 1 (dedo-esq-1) | [dino-dedo-esq-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-1.stl) | 1 | PLA creme | 17,2 × 12,7 × 8,5 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Dedo do pé esquerdo 2 (dedo-esq-2) | [dino-dedo-esq-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-2.stl) | 1 | PLA creme | 17 × 12,7 × 7,4 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Dedo do pé esquerdo 3 (dedo-esq-3) | [dino-dedo-esq-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-3.stl) | 1 | PLA creme | 12,7 × 17,4 × 6,9 | base plana (face de colar) na mesa | não | 3 | 15 % | 1 | 0,1 |
| Mancha do flanco direito (mancha-dir) | [dino-mancha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-dir.stl) | 1 | PLA verde-escuro | 21,3 × 26,4 × 7,6 | base plana (face de colar) na mesa | não | 3 | 15 % | 2 | 0,2 |
| Mancha do flanco esquerdo (mancha-esq) | [dino-mancha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-esq.stl) | 1 | PLA verde-escuro | 21,3 × 26,4 × 7,6 | base plana (face de colar) na mesa | não | 3 | 15 % | 2 | 0,2 |
| Braço direito (braco-dir) | [dino-braco-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-dir.stl) | 1 | PLA verde | 27,5 × 59 × 16 | face de dentro (plana) na mesa | não | 3 | 20 % | 8 | 0,4 |
| Braço esquerdo (braco-esq) | [dino-braco-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-esq.stl) | 1 | PLA verde | 27,5 × 59 × 16 | face de dentro (plana) na mesa | não | 3 | 20 % | 8 | 0,4 |
| Cubo do braço (cubo-braco) | [dino-cubo-braco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cubo-braco.stl) | 2 | PETG grafite | 17 × 17 × 12,8 | ponta de fora (2 faces chatas) na mesa, rebaixo do horn para cima | não | 4 | 60 % | 6 | 0,4 |
| Corpo (corpo) | [dino-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-corpo.stl) | 1 | PLA verde | 194,1 × 113,7 × 129,4 | borda de baixo (z=5) na mesa, em pé como um vaso; boca (z=134) para cima | sim (árvore POR DENTRO: teto das 2 coxas, sobre as rodas; degraus de dentro dos assentos planos (barriga, braços, manchas); por fora nada) | 4 | 15 % | 200 | 7,5 |
| Traseira (anca e cauda) (traseira) | [dino-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-traseira.stl) | 1 | PLA verde | 126,1 × 131 × 131,9 | borda da frente (plano da costura) na mesa, cauda para cima | sim (árvore POR DENTRO: teto de cima da anca (53° da vertical) e nervura do rasgo da crista; por fora nada) | 4 | 15 % | 102 | 3,9 |
| Gola do pescoço (gola) | [dino-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-gola.stl) | 1 | PLA verde | 112,3 × 100,5 × 56,1 | base (z=134) na mesa; a esfera sobe e fica aberta em cima | não | 4 | 20 % | 79 | 3,0 |
| Crista das costas (crista-costas) | [dino-crista-costas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-costas.stl) | 1 | PLA azul | 46,4 × 67,3 × 6 | deitada (lâmina de 6 mm) | não | 3 | 15 % | 10 | 0,4 |
| Crânio (cranio) | [dino-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cranio.stl) | 1 | PLA verde | 134,2 × 174,5 × 118,2 | borda de baixo na mesa, em pé | sim (árvore POR DENTRO: teto do crânio, fundo dos copos dos olhos e nervura da crista; e por baixo, fora do rosto: borda do céu da boca, que fica 40 mm acima da mesa) | 3 | 15 % | 179 | 6,8 |
| Mandíbula (mandibula) | [dino-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mandibula.stl) | 1 | PLA verde | 91,4 × 37 × 35,6 | face de trás (plano de corte) na mesa, ponta do queixo para cima | sim (pouco: sob o recorte esférico de trás, que nasce 2 a 10 mm acima da mesa; face escondida, virada para o pescoço) | 4 | 20 % | 34 | 1,4 |
| Mesa da cabeça (mesa-cabeca) | [dino-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mesa-cabeca.stl) | 1 | PETG grafite | 75,1 × 122,3 × 45,8 | de cabeça para baixo: face de cima na mesa | não | 4 | 30 % | 29 | 1,1 |
| Crista da cabeça (crista-cabeca) | [dino-crista-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-cabeca.stl) | 1 | PLA azul | 104,9 × 128,3 × 6 | deitada (lâmina de 6 mm) | não | 3 | 15 % | 22 | 0,9 |
| Olho direito (olho) | [dino-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho.stl) | 1 | PLA branco | 44 × 44 × 22,6 | face de trás (plana) na mesa | não | 3 | 15 % | 13 | 0,6 |
| Olho esquerdo (olho-esq) | [dino-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho-esq.stl) | 1 | PLA branco | 44 × 44 × 22,6 | face de trás (plana) na mesa | não | 3 | 15 % | 15 | 0,6 |
| Íris direita (iris) | [dino-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris.stl) | 1 | PLA azul | 30 × 30 × 9,9 | face de trás na mesa | não | 3 | 15 % | 5 | 0,3 |
| Íris esquerda (iris-esq) | [dino-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris-esq.stl) | 1 | PLA azul | 30 × 30 × 9,9 | face de trás na mesa | não | 3 | 15 % | 5 | 0,3 |
| Pupila direita (pupila) | [dino-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila.stl) | 1 | PLA preto | 19 × 19 × 7,9 | face de trás na mesa | não | 3 | 15 % | 2 | 0,1 |
| Pupila esquerda (pupila-esq) | [dino-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila-esq.stl) | 1 | PLA preto | 19 × 19 × 8,2 | face de trás na mesa | não | 3 | 15 % | 2 | 0,2 |
| Chassi (chassi) | [dino-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-chassi.stl) | 1 | PETG grafite | 105,9 × 179,2 × 121 | piso na mesa (em pé) | não | 4 | 25 % | 173 | 6,4 |
| Capa da esfera (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 1 | PETG grafite | 29 × 29 × 5,6 | deitada | não | 3 | 15 % | 3 | 0,2 |
| Bandeja do Raspberry Pi (bandeja-pi) | [dino-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-pi.stl) | 1 | PETG amarelo | 61,4 × 89 × 8 | placa na mesa, pilares para cima | não | 4 | 25 % | 16 | 0,7 |
| Bandeja do Arduino (bandeja-uno) | [dino-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-uno.stl) | 1 | PETG amarelo | 67,7 × 58,8 × 6 | placa na mesa, pilares para cima | não | 4 | 25 % | 12 | 0,5 |
| Garfo do pescoço (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG grafite | 65 × 48 × 50,8 | base na mesa, montantes para cima | sim (1,8 mm sob a base, em volta do anel de centragem do horn; suporte normal, fora de vista) | 5 | 40 % | 17 | 0,7 |
| Berço do tilt (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG grafite | 38,5 × 23 × 77 | de cabeça para baixo: topo da coluna na mesa | sim (pouco, sob a ponte) | 5 | 40 % | 15 | 0,6 |
| Cupom de teste (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **34** |  |  |  |  |  |  | **1002** | **39,9** |
<!-- /GERADO -->

Filamento e tempo são estimativas por volume, sem fatiador. O fatiador vai dar o número de verdade.

## 4. Filamento por cor

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 28 | 1,2 |
| PETG grafite | 243 | 9,4 |
| PLA azul | 42 | 1,9 |
| PLA branco | 28 | 1,2 |
| PLA cinza | 15 | 0,6 |
| PLA creme | 28 | 1,5 |
| PLA preto | 4 | 0,3 |
| PLA verde | 610 | 23,4 |
| PLA verde-escuro | 4 | 0,4 |
| **Total** | **1002** | **39,9** |
<!-- /GERADO -->

## Onde cada peça é reforçada

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| Barriga (barriga) | — | barriga creme; cola no assento plano do corpo |
| Dedo do pé direito 1 (dedo-dir-1) | — | dedo do pé; cola |
| Dedo do pé direito 2 (dedo-dir-2) | — | dedo do pé; cola |
| Dedo do pé direito 3 (dedo-dir-3) | — | dedo do pé; cola |
| Dedo do pé esquerdo 1 (dedo-esq-1) | — | dedo do pé; cola |
| Dedo do pé esquerdo 2 (dedo-esq-2) | — | dedo do pé; cola |
| Dedo do pé esquerdo 3 (dedo-esq-3) | — | dedo do pé; cola |
| Mancha do flanco direito (mancha-dir) | — | mancha do flanco, de contorno orgânico e nivelada com a pele em volta: a janela do sensor de distância lateral (fase 2) é o furo pequeno, fora do centro; cola no assento plano do corpo |
| Mancha do flanco esquerdo (mancha-esq) | — | mancha do flanco, de contorno orgânico e nivelada com a pele em volta: a janela do sensor de distância lateral (fase 2) é o furo pequeno, fora do centro; cola no assento plano do corpo |
| Braço direito (braco-dir) | — | braço direito; encaixa por pressão no cubo (2 faces chatas), sem parafuso por fora |
| Braço esquerdo (braco-esq) | — | braço esquerdo |
| Cubo do braço (cubo-braco) | maciço em volta do rebaixo do horn | cubo do braço: entra pelo furo do ombro, abraça o horn do micro servo e é preso pelo parafuso central do servo (fica escondido pelo braço) |
| Corpo (corpo) | 2 abas maciças atrás (M3 horizontal nos postes do chassi); lábio por dentro da borda de trás; colarinho maciço atrás e 3 ressaltos com inserto na borda de cima; 4 perímetros porque o corpo é aberto atrás | pernas, barriga e peito; desce por cima do chassi; 2 M3 por trás (cobertos pela traseira); a borda de trás encaixa na traseira |
| Traseira (anca e cauda) (traseira) | nervura por dentro ao longo do rasgo da crista; 2 almofadas nos parafusos de baixo; ponta da cauda maciça em cone | anca + cauda: sai para trás e dá acesso à bateria e às bandejas sem tirar a cabeça; 2 M3 auto-atarraxantes por baixo |
| Gola do pescoço (gola) | maciça entre a esfera e a pele de fora (sem teto em balanço); 3 furos M3 com rebaixo fundo | gola: esfera em que a cabeça gira; assenta na borda do corpo; 3 M3 por cima, nos ressaltos do corpo (por dentro, antes da cabeça) |
| Crista das costas (crista-costas) | — | crista das costas e da raiz da cauda; pressão ou cola no rasgo da traseira |
| Crânio (cranio) | 3 orelhas internas com inserto M3 para a mesa; copos dos olhos fechados por trás (só a janela do cabo) | 3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto, sob a crista, dão acesso aos parafusos da coluna |
| Mandíbula (mandibula) | almofadas maciças nos 2 lados do eixo; 2 nervuras que abraçam o horn; ponta do queixo maciça à frente de um plano a 45° | sem parafuso por fora: o horn encaixa entre 2 nervuras (direita) e o pino da mesa entra no soquete cego (esquerda) |
| Mesa da cabeça (mesa-cabeca) | placa de 4 mm; janela do servo da boca com cantos em chanfro | mesa da cabeça: 2 M3x10 na coluna do berço (por cima, pelos furos sob a crista); segura o servo da boca e o pino do eixo da mandíbula |
| Crista da cabeça (crista-cabeca) | — | crista da cabeça; encaixe por pressão (sem cola): tampa os 2 furos de acesso aos parafusos da mesa |
| Olho direito (olho) | — | olho direito: bolso da câmera (Camera Module 3) aberto por trás; pressão ou cola no copo do crânio |
| Olho esquerdo (olho-esq) | — | olho esquerdo: bolso do sensor ToF aberto por trás |
| Íris direita (iris) | — | anel da íris: a placa da câmera encosta atrás dele (4 furos piloto M2) |
| Íris esquerda (iris-esq) | — |  |
| Pupila direita (pupila) | — | pupila escura VAZADA no centro (a lente da câmera olha pelo furo); pressão, sem cola (dá acesso à lente) |
| Pupila esquerda (pupila-esq) | — | pupila escura vazada (janela do ToF) |
| Chassi (chassi) | mísulas a 45° e parede em V sob o deck do pan; travessa inteira do piso ao deck; paredes do rack alargadas a 45° desde o piso; postes maciços nos insertos | piso recortado da seção da pele + rack das bandejas (atrás) + torre e deck do servo de pan + orelhas dos servos dos braços + ressalto da esfera de trás |
| Capa da esfera (capa-esfera) | — | anel que segura a esfera de apoio; 2 M3x8 |
| Bandeja do Raspberry Pi (bandeja-pi) | placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack | bandeja deslizante do Raspberry Pi 4/5 (nível de baixo); sai por trás, pela porta; 4 M2,5x8 auto-atarraxantes |
| Bandeja do Arduino (bandeja-uno) | placa de 3 mm; trilho na parede esquerda e apoio no topo da parede direita | bandeja do Arduino Uno + shield, atravessado (nível de cima); sai por trás, sem a traseira; 4 M3x8 Allen direto no plástico |
| Garfo do pescoço (garfo-pescoco) | camadas ao longo dos montantes NÃO: a carga do tilt flete os montantes no plano das camadas, por isso 5 perímetros e 40 % de miolo | gira com o servo de pan (horn redondo) e segura o eixo do tilt |
| Berço do tilt (berco-tilt) | coluna em D maciça (5 perímetros) e ponte de 4 mm entre as duas paredes do servo | segura o servo de tilt (MG996R em pé) e sobe pela abertura da gola até a mesa da cabeça; cabos pela face chata da coluna |
| Cupom de teste (teste-encaixe) | — | cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto |
<!-- /GERADO -->

Depois de imprimir: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) e [LIGACAO.md](LIGACAO.md).
