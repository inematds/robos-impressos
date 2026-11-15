# Plano do dinossauro (`dino`)

Robô de 30 cm que roda sobre 2 rodas, gira e inclina a cabeça, abre a boca e mexe os 2 braços. Este arquivo guarda as decisões do projeto deste robô e os porquês. Para fazer o robô, use os guias:
[LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md), [IMPRIMIR.md](IMPRIMIR.md) e [LIGACAO.md](LIGACAO.md). O resumo está no
[README.md](README.md); as decisões que valem para os 4 robôs, no [PLANO.md da raiz](../../PLANO.md).

Fase 1 = mecânica e encaixe: corpo impresso, montado e ligado. A fase 2 (programa, voz, câmera, sensores, IA) não está
feita; a seção 7 diz o que já tem lugar nas peças. **Nada foi impresso ainda.**

## 1. O que é e números

<!-- GERADO:numeros -->
- Altura montado: 300,0 mm.
- Peças impressas: 34 (33 arquivos diferentes), em 12 mesas.
- Filamento: 1002 g. Tempo de impressão: 39,9 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 13.
<!-- /GERADO -->
- Tamanho: 194 mm de largura (nas coxas) × 293 mm da cauda ao focinho × 300 mm de altura (ponta da crista). Maior peça: o corpo, com 194 mm.
- Massa: 1597 g montado (estimativa): 1002 g de peças impressas e cerca de 600 g de componentes.
- Movimentos: pan ±60°, tilt de −15° a +20°, boca de 0 a 12°, braços de −15° a +20°. O verificador confere 12 poses, inclusive tudo ao mesmo tempo.

## 2. Decisões e porquês

| Decisão | Por quê | O que foi descartado |
|---|---|---|
| A forma vem de uma malha 3D da imagem de referência | A versão 1.0.2 era desenhada com formas simples e ficava longe do desenho. Uma malha gerada no computador a partir da imagem virou a pele do robô (`comum/cad/peles/dino.npz`); a casca é essa pele com 2,4 mm de parede, cortada em peças. | Esculpir à mão com esferas e cilindros. |
| Esqueleto próprio, com as rodas dentro das coxas | Na forma nova as pernas ficam na frente e a cauda atrás. O eixo das rodas passa pelas coxas e a casca cobre as rodas. | Esqueleto comum com a capivara: o dino tombaria para trás. |
| Uma esfera de apoio atrás, sob a raiz da cauda | O centro de massa fica 18,6 mm atrás do eixo das rodas: o terceiro apoio tem de ser atrás. | Esferas na frente, como na capivara. |
| Servo de pan numa torre sobre o eixo das rodas; placas num rack atrás | O peso fica baixo e perto do eixo. O Raspberry Pi vai na bandeja de baixo; o Arduino com o shield, atravessado, na de cima, porque o corpo é estreito no alto. | Arduino ao comprido: a pilha de 30 mm não cabe sob as costas. |
| Junta do pescoço a 164 mm do chão (era 185) | Pescoço mais curto, como na referência. | Chassi antigo, de pescoço comprido. |
| Casca em vasos: corpo, traseira e gola | Cada peça grande tem uma borda plana na mesa e paredes que sobem perto da vertical: imprime quase sem suporte. O corpo desce por cima do chassi; a traseira (anca e cauda) sai para trás. | Torso em duas metades (frente e costas), que deixava tetos em balanço. |
| A boca abre 12° e é um corte quase reto | A mandíbula da forma nova é funda e fica colada à esfera do pescoço: cada grau a mais faz o queixo recuar contra a esfera. A malha vinha de boca aberta; o vão foi fechado. | Abrir 18° como a capivara: comeria mais 4 mm do queixo. |
| Braços que giram, sem parafuso por fora | Um micro servo no chassi move cada braço pelo ombro. Um cubo entra pelo furo do ombro, abraça o horn e é preso pelo parafuso central do servo; o braço encaixa nele por pressão. | Braços parados em relevo; parafuso pelo lado de fora, que apareceria de três quartos. |
| Nenhum parafuso de frente nem no rosto | O corpo prende por 2 parafusos atrás das coxas, cobertos pela traseira; a traseira, por 2 por baixo; a gola, por 3 por dentro; a mesa da cabeça, por 2 sob a crista, que encaixa por pressão. | — |
| A mandíbula encaixa sem furo no rosto | De um lado o braço do horn entra entre 2 nervuras; do outro, um pino da mesa entra num soquete cego. A mandíbula abre e encaixa por pressão. | Parafuso-eixo atravessando a bochecha. |

## 3. Peças impressas e imprimibilidade

A regra do projeto: imprimir sem suporte sempre que der. Face plana na mesa, balanços de até 45°, pontes de até 20 mm,
chanfro de 45° nas bordas viradas para baixo. Suporte só onde é inevitável, em árvore, fora do rosto e dos encaixes, e
declarado peça por peça. O verificador mede a área sem apoio de cada peça (teste 10) e reprova a peça declarada sem
suporte que precisaria dele.

Resultado: **27 das 33 peças saem sem suporte.** As 6 que pedem suporte:

| Peça | Área sem apoio | Onde |
|---|---|---|
| Crânio | 12 051 mm² (9,8 %) | teto de dentro, fundo dos copos dos olhos e nervura da crista; por fora, só a borda do céu da boca |
| Corpo | 2 674 mm² (2,3 %) | teto das 2 coxas, sobre as rodas, e degraus de dentro dos assentos |
| Traseira | 1 596 mm² (2,4 %) | teto de cima da anca e nervura da crista, por dentro |
| Mandíbula | 455 mm² | recorte redondo de trás, virado para o pescoço |
| Garfo do pescoço | 1 488 mm² (16,1 %) | 1,8 mm sob a base, em volta do anel do horn |
| Berço do tilt | 516 mm² (7,0 %) | sob a ponte entre as 2 paredes do servo |

Na versão 1.0.2 eram 8 peças sem suporte, 8 com suporte e 14 que o teste reprovaria.

O que foi feito para chegar aí: cascas em vasos (corpo com a borda de baixo na mesa, gola com a base na mesa, traseira de pé sobre a costura); gola maciça entre a esfera e a pele de fora; colarinho maciço atrás, na borda do corpo; ponta da cauda e do queixo maciças, fechando a 45°; paredes do rack que nascem de um alargamento a 45°; língua do deck apoiada num arco em V; peças coloridas em relevo, com base plana; cristas deitadas, como lâminas de 6 mm.

Parede medida da casca (mínimo exigido: 2,0 mm): corpo de 2,28 a 2,64 mm, cabeça de 2,31 a 2,55 mm, gola a partir de 3,38 mm (casca esférica).

Peças estruturais (chassi, bandejas, garfo, berço, mesa da cabeça) são de PETG, com 4 ou 5 perímetros. As tabelas
abaixo trazem, por peça, a orientação na mesa, o suporte, os perímetros, o preenchimento e o motivo de cada reforço.

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

## 4. Montagem e abertura

A ordem abaixo é a que o verificador percorre (teste 9): cada peça entra pelo lado indicado, contra o que já está
montado, sem bater. O teste prova o caminho da peça, não o da ferramenta nem o dos fios.

### Parafusos

<!-- GERADO:parafusos -->
| Onde fica | Qtd | Parafuso | Onde rosqueia |
|---|---|---|---|
| Motores das rodas nas paredes do chassi | 4 | M3 × 30 + porca | porca do lado de dentro da parede |
| Servo de pan no deck | 4 | M3 × 12 + porca | porca por baixo do deck |
| Servo de tilt no berço | 4 | M3 × 12 + porca | porca por dentro do berço |
| Pino do berço, no lado esquerdo do garfo | 1 | M3 × 10 | inserto no garfo |
| Driver L298N na travessa | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Capa da esfera de apoio (por baixo) | 2 | M3 × 8 | inserto no chassi |
| Corpo nos postes do chassi (por trás das coxas) | 2 | M3 × 16 | inserto nos postes do chassi |
| Gola no corpo (por cima) | 3 | M3 × 10 | inserto na borda do corpo |
| Traseira (por baixo) | 2 | auto-atarraxante 3 × 8 mm, cabeça abaulada | direto no piso do chassi (furo de 2,7 mm) |
| Arduino Uno na bandeja | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Raspberry Pi na bandeja | 4 | M2,5 × 8 auto-atarraxante | direto no plástico (furo de 2,2 mm) |
| Mesa da cabeça no crânio (por baixo) | 3 | M3 × 12 | inserto no crânio |
| Mesa da cabeça na coluna do berço (por cima) | 2 | M3 × 10 | inserto no topo do berço |
| Horn redondo dos 2 servos MG996R | 8 | M2 × 8 auto-atarraxante | nos furos do horn |
| Micro servos da boca e dos 2 braços | 6 | parafuso que vem com o servo | direto no plástico (furo de 1,7 mm) |
<!-- /GERADO -->

### Passo a passo

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | chassi | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, 5 servos em 90°, cabos do Raspberry Pi e divisor prontos, cartão gravado) e assente os 13 insertos a quente: 2 nos postes do chassi, 2 no ressalto da esfera, 3 na borda do corpo, 3 no crânio, 2 no topo do berço e 1 no garfo. |
| 2 | motor direito | pela direita | 2 × M3 × 30 com porca, pelos rasgos da parede. A ponta de dentro do eixo passa pelo furo da parede. Leve os 2 fios do motor pelo furo de 6 mm, à frente dele, até o lugar do driver. |
| 3 | motor esquerdo | pela esquerda | Igual ao direito. |
| 4 | step-down 5 V (parede esquerda, abraçadeira) | pela esquerda | O conversor já vem soldado no chicote do preparo 1. 1 abraçadeira; fica em pé na face de fora da parede esquerda do rack, com o parafuso de ajuste à mostra. |
| 5 | UBEC 6 V (parede direita, abraçadeira) | pela direita | 1 abraçadeira, em pé na face de fora da parede direita do rack. |
| 6 | BMS 2S (no piso, sob o lugar do L298N) | por cima | 1 abraçadeira. A placa de proteção já está soldada no chicote e fica deitada no piso. |
| 7 | chave (por baixo do piso) | por baixo | Já está no lugar desde o preparo 1: encaixada por baixo, com os 2 fios passando pelo recorte. |
| 8 | roda direita | pela direita | Encaixa por pressão no eixo do motor. Se a roda trouxer parafuso, aperte-o pelo centro. |
| 9 | roda esquerda | pela esquerda | Igual à direita. |
| 10 | esfera de apoio + capa | por baixo | A esfera entra no soquete por baixo e a capa prende com 2 × M3 × 8. A esfera tem de girar solta. |
| 11 | driver L298N (pela frente da torre) | pela frente | Antes, tire do módulo os 3 jumpers: ENA, ENB e o do regulador de 5 V. 4 × M3 × 8 na travessa. Aperte nos bornes: os 2 fios de cada motor, o vermelho e o preto do chicote (alimentação dos motores e GND) e o fio de 5,1 V que vem do borne 1 da barra de emenda. Encaixe os 6 jumpers de sinal nos pinos ENA, IN1, IN2, IN3, IN4 e ENB e deixe as outras pontas soltas, marcadas com fita. |
| 12 | servo de pan | por cima | 4 × M3 × 12 com porca, eixo para cima. O servo já está em 90° (preparo 2): não gire o eixo com a mão. |
| 13 | servo do braço direito | pela direita | Micro servo na orelha do chassi, eixo para fora, com os 2 parafusos do kit. Já está em 90° (preparo 2). Encaixe o horn de 1 braço apontando para trás e para cima: apontado para a frente ele raspa no corpo quando o corpo desce. |
| 14 | servo do braço esquerdo | pela esquerda | Igual ao direito. |
| 15 | carregador USB-C (na mesinha de trás, fita dupla-face) | por cima | Fita dupla-face, com a boca USB-C para trás. Já está soldado no chicote. |
| 16 | corpo desce por cima do chassi | por cima | Cole antes a barriga, os 6 dedos e as 2 manchas nos assentos planos (as manchas só na fase 2, se você for pôr os sensores laterais). O corpo desce por cima do chassi. 2 × M3 × 16 horizontais, por trás das coxas, nos insertos dos postes. Na frente não há parafuso: quem trava a frente é o encaixe com a traseira. |
| 17 | garfo (por dentro da boca do corpo) | por cima | Prenda o horn redondo do servo de pan por baixo do garfo, com 4 × M2 × 8 pelos rasgos. Com o servo em 90°, encaixe o garfo no eixo com os montantes para os lados e aperte o parafuso central do servo pelo furo do meio. |
| 18 | berço + servo de tilt | por cima | Na bancada: servo de tilt em pé no berço, 4 × M3 × 12 com porca, e o horn redondo encaixado no eixo. Desça o berço entre os montantes do garfo até o horn assentar no rebaixo do montante direito (abra os montantes 1 mm com os dedos). Prenda o horn por FORA, com 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 9 mm. No montante esquerdo entra o M3 × 10, pelo inserto: a ponta dele é o pino do berço. Aperte até encostar e volte um quarto de volta, porque a cabeça inclina nele. Passe o cabo do servo pela face chata da coluna e pelo rasgo da base do garfo. |
| 19 | gola | por cima | A gola assenta na borda do corpo. 3 × M3 × 10 por cima, nos insertos da borda. Passe por dentro dela o cabo do servo de tilt (e, na fase 2, o cabo flat da câmera). |
| 20 | cubo + braço direito | pela direita | O cubo entra pelo furo do ombro e abraça o horn do micro servo. Prenda-o com o parafuso central do servo. O braço encaixa no cubo por pressão, pelas 2 faces chatas, sem parafuso por fora. |
| 21 | cubo + braço esquerdo | pela esquerda | Igual ao direito. |
| 22 | bateria (entra por trás, por cima do carregador, e desce no piso) | por cima | O suporte já está soldado no chicote desde o preparo 1, sem as células. Ele entra por trás, passa por cima do carregador e desce no piso; prenda com fita dupla-face. Com a chave desligada, ponha agora as 2 células, conferindo o lado do positivo com o multímetro. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 23 | bandeja do Pi | por trás | Na bancada: Raspberry Pi na bandeja com 4 × M2,5 × 8, blocos USB para trás, cartão microSD já gravado (preparo 4) e dissipadores colados. Encaixe os conectores ANTES de deslizar a bandeja: vermelhos nos pinos 2 e 4, pretos nos pinos 6 e 9, verde no 32, azul no 33 e preto da serial no 34. Dobre os fios logo acima dos conectores: sobra pouca altura sobre o Pi. É o trilho de baixo. |
| 24 | bandeja do Uno | por trás | Na bancada: Arduino Uno com o shield na bandeja, 4 × M3 × 8, atravessado (o USB fica de lado). Deslize a bandeja no trilho de cima e refaça no shield as ligações do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra no + e no − do conector COM, os 5 servos (D9, D10, D11, D2 e D3). Ligue os 6 sinais do driver (D5, D4, D7, D8, D12 e D6, só no pino S) e a serial: verde no S do D0, preto no G do D0 e o jumper do divisor no S do D1. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos. Faça essas ligações com a bandeja ainda para fora, apoiada na entrada do trilho, e só então empurre-a até o fim, acomodando os fios. Esta manobra nunca foi ensaiada com as peças impressas. |
| 25 | traseira (com a crista das costas) | por trás | Encaixe a crista das costas no rasgo da traseira (pressão ou cola). A traseira entra por trás e a borda dela encaixa no lábio do corpo. 2 parafusos auto-atarraxantes de 3 × 8 mm por baixo. |
| 26 | mesa dentro do crânio (na bancada) | por baixo | Micro servo da boca na mesa, com os 2 parafusos do kit, já em 90°. A mesa entra por baixo, para dentro do crânio: 3 × M3 × 12 nos insertos. Mandíbula, com a boca fechada: o braço do horn entra entre as 2 nervuras (lado direito) e o pino da mesa entra no soquete cego (lado esquerdo), por pressão. Olhos e íris: pressão ou cola. Pupilas: só pressão. O alto-falante é da fase 2. |
| 27 | cabeça no pescoço | por cima | Ligue a extensão de 30 cm no cabo do servo da boca e desça-a pela face chata da coluna, junto com o cabo do servo de tilt. A cabeça desce até a mesa assentar na coluna do berço: 2 × M3 × 10 por cima, pelos 2 furos do alto do crânio. A crista da cabeça tampa os furos: encaixe por pressão, sem cola. |
<!-- /GERADO -->

### Abrir sem tirar a cabeça

Tirando 2 parafusos por baixo, a traseira sai para trás com a crista das costas. Por ali saem a bandeja do Arduino, a do Raspberry Pi e a bateria, que sobe 15 mm por cima do carregador. O carregador e a esfera ficam no chassi. Para tirar o corpo: cabeça, gola (3 parafusos por dentro), braços e cubos, berço e garfo, e os 2 parafusos de trás das coxas.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | ABRIR: traseira sai | Solte os 2 parafusos de baixo e puxe a traseira para trás. A cabeça fica no lugar. |
| 2 | ABRIR: bandeja do Uno sai | Desencaixe os conectores do shield, marcando cada um com fita e o nome do pino, e solte do borne azul os fios do UBEC. Puxe a bandeja para trás. |
| 3 | ABRIR: bandeja do Pi sai | Desencaixe os conectores dos pinos do Raspberry Pi e puxe a bandeja para trás. |
| 4 | ABRIR: bateria sai | Desligue a chave antes. O suporte sobe 15 mm, passa por cima do carregador e sai por trás. |
<!-- /GERADO -->

## 5. Energia

Pack de 2 células 18650 em série (6 a 8,4 V) → fusível retardado de 3 A → placa de proteção (BMS 2S) → chave → três
linhas: 5,1 V (conversor LM2596) para o Raspberry Pi, o Arduino e a lógica do driver; 6 V (UBEC de 3 A) para os servos;
tensão da bateria para o driver L298N dos 2 motores. O esquema e a tabela fio a fio estão em [LIGACAO.md](LIGACAO.md).

| Decisão | Por quê |
|---|---|
| Conversor LM2596 para os 5 V, não o XL4015 | Quem decide é a tensão mínima de entrada. O XL4015 pede 8 V e o pack de 2 células passa quase toda a descarga abaixo disso. O LM2596 mantém os 5 V até o pack cair a cerca de 6,5 V. Limite: cerca de 2 A contínuos, o que pede o Pi 4 (ou o Pi 5 com 1 câmera e sem acessórios USB). |
| UBEC de 6 V e 3 A só para os servos | Os servos não derrubam os 5 V das placas quando partem. Servos: 2 MG996R (pan e tilt) e 3 micro servos (boca e 2 braços). Travados todos juntos pedem perto de 5 A, mais do que o UBEC dá: o programa tem de parar antes do fim do curso, e há um capacitor de 1000 µF no borne. |
| Carregador USB-C com balanceamento e placa de proteção | O robô carrega com fonte de celular, sem abrir. Células soltas não têm proteção: quem corta a descarga funda e o curto é a placa. O balanceamento pede um 3º fio no ponto que une as células. |
| Driver L298N com os 3 jumpers retirados | A velocidade vem do Arduino (pinos D5 e D6). O regulador de 5 V do módulo não segura os 5 V abaixo de uns 7 V de bateria: a lógica dele recebe os 5,1 V do LM2596. |
| Raspberry Pi alimentado pelos pinos de 5 V | Na bandeja, a porta USB-C do Pi fica a cerca de 1 mm da parede do rack. |
| Fusível de 3 A | A chave liga/desliga é de 3 A. O uso normal calculado é de entre 2,5 e 3 A: fica perto do limite. É a pendência principal da parte elétrica. |

Onde fica cada módulo: LM2596 em pé na face de fora da parede esquerda do rack; UBEC na parede direita; placa de proteção no piso, sob o driver; L298N na travessa, por dentro da torre; carregador USB-C numa mesinha do chassi sobre o ressalto da esfera, com o plugue entrando por um rasgo de 13 × 7 mm sob a raiz da cauda; chave por baixo do piso, entre as pernas.

## 6. Estabilidade

Centro de massa 18,6 mm atrás do eixo das rodas e 108 mm acima do chão. Apoios: as 2 rodas e a esfera de trás, a 117 mm do eixo. Margem de 18,6 mm na pose neutra (tomba com 10° de inclinação) e 14,8 mm na pior pose, com a cabeça baixa (8°). O mínimo exigido pelo teste é 10 mm. A conta é de corpo parado: aceleração e freada não entram.

## 7. Preparado para a fase 2

### Os olhos

A pergunta era onde pôr a câmera e o sensor que mede distância sem abrir furo no rosto. Três opções foram avaliadas:

| Opção | O que é | Resultado |
|---|---|---|
| (a) | 2 câmeras, uma em cada pupila (visão estéreo ou campo largo) | Descartada. Pede o Raspberry Pi 5 (2 portas de câmera; o Pi 4 tem 1) com 5 V e 5 A. O único conversor de 5 A da lista (XL4015) não trabalha no pack de 2 células, porque pede 8 V de entrada: mudaria a bateria e o conversor para ganhar um estéreo que a fase 2 ainda não usa. |
| **(b)** | **Câmera numa pupila e sensor de distância ToF na outra** | **Escolhida.** Funciona no Pi 4 e no Pi 5 (1 porta de câmera basta). O ToF dá a distância real do que a cabeça está olhando, coisa que uma câmera sozinha não dá. Por fora os dois olhos ficam iguais: pupila preta com um furinho escuro. Cabe no conversor LM2596 de 3 A. |
| (c) | Câmera grande-angular num olho e o outro sensor escondido em outro lugar | Descartada. Um sensor fora da cabeça não acompanha o olhar. |

Como ficou: câmera (Raspberry Pi Camera Module 3 Wide) atrás da pupila do olho **direito**, sensor de distância ToF
(VL53L1X) atrás da pupila do olho **esquerdo**. A pupila é uma peça separada, preta, vazada no centro: furo de 8,5 mm
para a lente e de 6 mm para a janela do ToF. Ela entra por pressão, sem cola, e dá acesso à lente. A placa entra por
trás do olho e encosta na íris.

O cabo flat da câmera sai pela janela de trás do copo do olho e desce pelo pescoço até o Raspberry Pi; são cerca de
50 cm, com uma barriga em S dentro da gola para a cabeça girar e inclinar. O cérebro previsto é o Raspberry Pi 4, ou o
Pi 5 com 1 câmera.

### Onde está cada furo

A ordem era: nenhum furo técnico chamando atenção de frente nem de três quartos. Cada sensor ficou atrás de um detalhe
que o bicho já tem.

| O quê | Onde |
|---|---|
| Câmera | Pupila do olho direito (furo de 8,5 mm) |
| Distância à frente (ToF) | Pupila do olho esquerdo (janela de 6 mm) |
| Distância nas laterais (ToF) | Dentro de 2 manchas verde-escuras de contorno irregular nos flancos (janela de 5 mm, fora do centro da mancha) |
| Microfones | As 2 narinas, no alto do focinho (furo de 2 mm, com anel de encaixe por dentro) |
| Alto-falante | Em cima da mesa da cabeça, virado para baixo: o som sai pela fresta da boca e pelo vão do pescoço |
| Carga USB-C | Rasgo de 13 × 7 mm sob a raiz da cauda: só aparece por trás e por baixo |
| Chave liga/desliga | Por baixo do piso, entre as pernas |
| Cabos da cabeça | Face chata da coluna do berço, rasgo do garfo e rasgo de 18 × 2,5 mm no deck, à direita do servo de pan |

De frente e de três quartos aparecem só as narinas, o furinho das pupilas, o furinho de cada mancha e a fresta da boca.

LiDAR: avaliado e deixado de fora. Num bicho, a cabeça tampa a volta inteira de que o sensor precisa.

### O que comprar na fase 2

<!-- GERADO:fase2 -->
| Item (o nome abre a busca) | Qtd | Onde fica | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide (placa de 25 × 24 mm)](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3-wide) | 1 | Atrás da pupila do olho direito: a placa entra por trás do olho e encosta na íris, em 4 furos para parafuso M2. A lente olha pelo furo de 8,5 mm da pupila. NC: furos da placa e altura da lente. | R$ 200–400 | não conferido |
| [Cabo flat de câmera de 50 cm (no Raspberry Pi 5, o cabo de 22 para 15 vias)](https://lista.mercadolivre.com.br/cabo-flat-camera-raspberry-pi-50cm) | 1 | Sai pela janela de trás do olho, desce pela face chata da coluna do pescoço e pelo rasgo do garfo, até o Raspberry Pi. Deixe uma barriga em S dentro da gola: a cabeça gira 60° para cada lado. NC: comprimento: os 50 cm são estimativa pelo modelo. | R$ 15–45 | não conferido |
| [Parafuso M2 × 6 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Prende a câmera nos 4 furos da íris direita. | R$ 3–8 | R$ 5,98 o kit com 10 |
| [Sensor de distância ToF VL53L1X (placa de cerca de 25 × 11 mm)](https://lista.mercadolivre.com.br/sensor-distancia-vl53l1x) | 3 | 1 atrás da pupila do olho esquerdo (janela de 6 mm): mede a distância do que a cabeça está olhando. 2 nas laterais, atrás das 2 manchas verde-escuras dos flancos (janela de 5 mm em cada mancha, fora do centro). NC: tamanho da placa e lugar da janela: meça antes de imprimir o olho esquerdo. | R$ 30–110 | R$ 102,32 (VL53L1X, até 4 m); R$ 31,81 (VL53L0X, até 2 m) |
| [Microfone I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Atrás das 2 narinas: cada narina é um furo de som de 2 mm e a placa redonda encaixa por dentro. NC: placa redonda de 14 mm de diâmetro: meça a sua. | R$ 15–55 | R$ 54,26 |
| [Alto-falante de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Em cima da mesa da cabeça, virado para baixo. O som sai pela fresta da boca e pelo vão do pescoço: não há grade à mostra. NC: diâmetro e profundidade. | R$ 7–20 | não conferido |
| [Amplificador de áudio pequeno (PAM8403 ou MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Sem lugar modelado ainda: vai solto dentro do corpo, com fita dupla-face. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | Sem lugar modelado neste robô: fita dupla-face no piso do chassi, perto do eixo das rodas. | R$ 15–35 | R$ 34,09 |
<!-- /GERADO -->

## 8. Semelhança com a referência

Medida pelo contorno do robô em 4 vistas, contra as imagens de referência (IoU: área comum dividida pela área total das
duas silhuetas, de 0 a 1). "Teto" é a malha crua gerada a partir da imagem: um robô com rodas, cortes e folgas não passa
dela.

| Vista | Antes (v1.0.2) | Depois | Teto (malha) |
|---|---|---|---|
| frente | 0,875 | 0,910 | 0,942 |
| três quartos (a) | 0,808 | 0,873 | 0,888 |
| três quartos (b) | 0,787 | 0,862 | 0,889 |
| lado | 0,786 | 0,842 | 0,870 |
| **média** | **0,814** | **0,872** | **0,897** |

Alvo definido antes de medir o depois: 0,855. O alvo (metade do caminho entre o antes e o teto) foi passado. O que ainda separa o robô da malha: a boca fechada, a faixa reta entre as pernas e os braços lisos. A tabela completa e o método estão em
[comparacao/semelhanca.md](../../comparacao/semelhanca.md).

## 9. Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py dino`:

<!-- GERADO:verificacao -->
```
== verificação: dino
  [PASSOU] 1 contagem: 33 peças distintas, 34 no total (esperado 34); faltando 0; sobrando 0
  [PASSOU] 2 malha: 33 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 194.1 mm (corpo)
  [PASSOU] 4 parede: corpo 2.27–2.62 mm; gola 2.89–9.75 mm; cabeça 2.31–2.55 mm (mínimo exigido 2.0)
  [PASSOU] 5 interferência: 59 sólidos (33 impressos + 26 componentes), 12 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda)
  [PASSOU] 6 teste negativo: 'chassi' deslocada 3 mm em X → 15 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 33 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 1597 g; CG neutro em x=-0.3 y=-18.7 z=108.2 mm, margem 18.7 mm (tomba com 10°); pior pose 'tilt-baixo': margem 14.9 mm (8°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 31 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 33 peças distintas: 27 saem sem suporte; 6 com suporte declarado: cranio (12051 mm² = 9.8 %, ponte de 65 mm, 2 ponto(s) no ar), corpo (2514 mm² = 2.2 %, ponte de 20 mm, 2 ponto(s) no ar), traseira (1596 mm² = 2.4 %, ponte de 24 mm, 1 ponto(s) no ar), garfo-pescoco (1488 mm² = 16.1 %, ponte de 21 mm), berco-tilt (516 mm² = 7.0 %, ponte de 21 mm), mandibula (455 mm² = 4.9 %); 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'chassi' na orientação declarada: 158 mm² sem apoio (limite 163); girada 180° em X → 11537 mm² = 14.1 % (acusou; tem que acusar)
```
<!-- /GERADO -->

## 10. Pendências

- O canto de trás do queixo fica recortado e a boca é uma fresta reta, não o sorriso aberto da referência.
- Entre as pernas a barriga desce reta até perto do chão: é o que mantém o chassi inteiro sobre o piso.
- Os braços são lisos, sem os 3 dedinhos. Entre o corpo e a base de cada braço fica uma junta de 0,6 mm.
- Os espinhos da cauda saem na cor do corpo (são relevo da casca) e os da nuca não existem, porque a cabeça passa por ali.
- O 3º dedo de cada pé ficou na lateral de fora, não na frente.
- Na base da gola, atrás de cada ombro, aparece de lado um ponto escuro de cerca de 2 mm: é o rebaixo do parafuso de trás da gola.
- O sensor de distância lateral fica cerca de 9,5 mm atrás da pele: o campo de visão pela janela de 5 mm não foi conferido.
- O crânio ainda pede suporte por dentro.
- O chassi chega a 2,8 mm da casca num canto dos postes do corpo (o projeto pedia 2,9 mm; não há interferência).
- O chassi passa no teste de imprimibilidade por pouco: 158 mm² sem apoio, para um limite de 163 mm².
- A bandeja do Arduino corre só no trilho da parede esquerda e o USB dele fica de lado: para regravar, puxe a bandeja.
- O horn do micro servo dos braços não está no modelo: o teste 9 não prova que o corpo desce com ele montado.
- Os insertos ficam em postes e ressaltos maciços; o ressalto com nervuras do projeto (`ressalto_nervurado`) não foi usado aqui.
- Medidas NC: sensor ToF, microfone, câmera, horn do micro servo, altura da pilha Arduino + shield (30 mm).
- A chave liga/desliga de 3 A é o ponto fraco da parte elétrica: uma chave maior pede mudar o recorte no chassi.
- Porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e sensor de movimento não têm lugar modelado.
- Nada foi impresso, e a parte elétrica não foi testada na bancada.
- Os 3MF das mesas ainda não foram abertos num fatiador; tempo e filamento são estimativas por volume.
