# Plano do robô quadrado que roda (`cubo_rodas`)

As decisões deste robô, o porquê de cada uma, o que foi provado no computador e o que ainda falta provar.
Para comprar, imprimir e ligar, use os guias: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md), [IMPRIMIR.md](IMPRIMIR.md)
e [LIGACAO.md](LIGACAO.md). As decisões que valem para os quatro robôs estão no [PLANO.md da raiz](../../PLANO.md).

**Fase 1 = mecânica e encaixe. Nada foi impresso nem montado, e a parte elétrica não foi testada na bancada.**

## 1. O que é e números

É o quarto robô do projeto: a mesma cabeça em cubo do robô quadrado de mesa, maior, sobre um corpo que anda. De cima
para baixo: cabeça com tela de 5" → pescoço oco → tronco (casca de cima) → deck (bandeja das placas) → base com os
motores, as rodas, a bola de apoio e a bateria.

<!-- GERADO:numeros -->
- Altura montado: 306,5 mm.
- Peças impressas: 19 (15 arquivos diferentes), em 8 mesas.
- Filamento: 1143 g. Tempo de impressão: 43,4 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 31.
<!-- /GERADO -->
- Largura total com as rodas: 219 mm (corpo de 130 mm). Comprimento: 182 mm. Bitola: 181 mm. Entre-eixos (rodas à bola): 120 mm.
- Vão livre: 20 mm sob o piso e 8 mm sob a capa da bola.
- Robô montado: cerca de 2214 g (estimativa: peças por volume + componentes pela ficha).
- Com o LiDAR da fase 2 no topo: 341,3 mm de altura.

## 2. Decisões e porquês

| Decisão | Por quê | O que ficou de fora |
|---|---|---|
| Tela de 5" HDMI (Waveshare 5inch HDMI LCD (B), placa de 121 × 89,55 mm, área ativa de 108 × 64,8 mm), presa no painel do rosto | É a maior que deixa a cabeça com 152 mm de largura e o centro de massa baixo | Tela de 7" (193 × 111 mm): a cabeça passaria de 210 mm e o robô tombaria mais fácil |
| 2 motores JGB37-520 de 12 V, redução 1:56, com encoder (107 rpm, 4,8 kgf·cm travado, 158 g cada) | Subir um degrau de 10 mm pede cerca de 2 kgf·cm por roda; os 316 g de motor ficam embaixo e ajudam o equilíbrio | Motores N20 e TT: não têm torque para o degrau |
| Rodas de 85 × 38 mm com sextavado de 12 mm, na FRENTE | O raio de 42,5 mm sobe cerca de 15 mm com folga de torque de 2 vezes | — |
| Apoio de trás: bola de tênis de mesa de 40 mm num poço com assento cônico, presa por uma capa | Rola em qualquer direção, é leve e fácil de achar | 2 rodízios (um na frente e um atrás). A capa fica a 8 mm do chão: é ela que limita o degrau |
| Tração diferencial com encoder nas duas rodas | O programa sabe quanto cada roda andou | — |
| Pack de 3 células (3S, 9 a 12,6 V) num alçapão por baixo | Os motores são de 12 V; a bateria no fundo baixa o centro de massa e sai com 4 parafusos, sem abrir o robô | Pack de 2 células: não alimenta os motores de 12 V |
| Conversor XL4015 para os 5,1 V | Trabalha de 8 a 35 V de entrada e o pack de 3 células fica sempre acima de 9 V; entrega até 5 A | LM2596 (é o do robô de mesa, que usa 2 células) |
| UBEC de 6 V e 3 A só para os 2 servos | Os servos não derrubam os 5 V do Raspberry Pi quando partem | Servos no mesmo conversor do Pi |
| Driver L298N | Já era o driver do projeto; aguenta 2 A por canal e o motor travado puxa 1,2 A | TB6612, que perde menos tensão: o L298N tira cerca de 2 V dos motores |
| Carregador USB-C com balanceamento (LX-USC-V2, preparado para 3 células) + placa de proteção de 3 células (HX-3S-FL10) | Carrega sem abrir o robô, com a boca USB-C atrás | Carregador externo como rotina (continua possível: as células saem pelo alçapão) |
| Pan de ±170° por 2 engrenagens impressas (44 e 22 dentes, módulo 1,5) e tubo oco com 3 tirantes M3 × 50 | Um servo comum de 180° gira o pescoço quase uma volta; os cabos passam por dentro; os tirantes de aço deixam as camadas do tubo só em compressão | Servo de 360° ou anel coletor |
| Tilt de −25° a +30° por DENTRO da cabeça (garfo interno; pino M5 rosqueado direto no braço do garfo) | De fora só se vê o pescoço fino; nenhum rasgo de horn à mostra | Garfo externo, com os parafusos do horn aparecendo |
| Nenhum parafuso de frente nem de 3/4 | O tronco é preso por 4 M3 × 12 que entram por baixo da base; as flanges dos motores ficam atrás das rodas; o copo da cabeça é preso por trás | — |
| Os 2 postes da frente ficam no trecho reto da parede da frente | No canto arredondado o rebaixo do parafuso furaria a parede de fora (há uma trava no modelo que acusa isso) | Postes nos 4 cantos |
| Cada motor sai pela lateral, com a flange, sem abrir o robô | Motor é a peça que mais dá manutenção | Motor preso por dentro |
| O deck fica solto sobre os 4 postes; quem o prende é o tronco | Os mesmos 4 parafusos fecham base, deck e tronco | Parafusos próprios do deck |
| Raspberry Pi ↔ Arduino por serial de 3 fios (pinos 32, 33 e 34 do Pi; D0 e D1 do Arduino; divisor de 3 resistores de 1 kΩ) | Um plugue USB não passa pelo furo de 9 mm do pescoço; é a mesma ligação do robô de mesa | Cabo USB entre as duas placas |
| Raspberry Pi alimentado pelos pinos 2, 4, 6 e 9 | A tela não ocupa os pinos, e abaixo da entrada USB-C sobram só cerca de 22 mm | Adaptador USB-C com bornes (é o do robô de mesa; aqui só caberia em ângulo) |
| Driver nos pinos D5 e D6 (velocidade) e D4, D7, D8 e D12 (sentido); encoders no D2 e D3 (um fio de cada) e no A0 e A1 (o outro fio) | A biblioteca dos servos tira a variação de força dos pinos 9 e 10; sobram o 5 e o 6. O D2 e o D3 são os pinos que avisam o programa a cada pulso | Variar a força pelos pinos de sentido, com os jumpers do driver postos: economiza 2 pinos e complica o programa |

As decisões de ligação elétrica saíram das fichas dos componentes. Nenhuma foi testada na bancada.

## 3. Peças impressas e imprimibilidade

19 peças, 15 arquivos diferentes, em 8 mesas. **As 15 saem sem suporte** na posição em que o arquivo vem: é o teste 10
do verificador, que mede em cada peça a área virada para baixo a mais de 45° e os pontos que nasceriam no ar.

<!-- GERADO:pecas -->
| Peça | Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base com rodas (base-rodas) | [cubo_rodas-base-rodas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-base-rodas.stl) | 1 | PETG grafite | 130 × 182 × 72 | piso na mesa | não | 5 | 25 % | 267 | 9,8 |
| Alçapão da bateria (tampa-bateria) | [cubo_rodas-tampa-bateria.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tampa-bateria.stl) | 1 | PETG grafite | 108 × 84 × 7 | face de baixo na mesa, cantoneiras para cima | não | 4 | 25 % | 34 | 1,3 |
| Capa da bola (capa-esfera) | [cubo_rodas-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-capa-esfera.stl) | 1 | PETG grafite | 56,9 × 47,2 × 12 | de cabeça para baixo: a face que encosta no piso na mesa; a boca fecha a 45° | não | 4 | 40 % | 9 | 0,4 |
| Flange do motor (flange-motor) | [cubo_rodas-flange-motor.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-flange-motor.stl) | 2 | PETG grafite | 62 × 62 × 4 | deitada, a face que encosta na parede na mesa | não | 5 | 60 % | 28 | 1,2 |
| Deck (bandeja das placas) (deck) | [cubo_rodas-deck.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-deck.stl) | 1 | PETG grafite | 127 × 179 × 29,8 | face de baixo na mesa | não | 4 | 25 % | 97 | 3,6 |
| Tronco (tronco) | [cubo_rodas-tronco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tronco.stl) | 1 | PETG branco | 130 × 182 × 57,5 | de cabeça para baixo: o topo na mesa | não | 4 | 15 % | 236 | 8,7 |
| Tubo do pescoço (tubo-pescoco) | [cubo_rodas-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tubo-pescoco.stl) | 1 | PETG prata | 40 × 40 × 36,6 | de cabeça para baixo: o topo (lado do garfo) na mesa, a flange cônica abre a 45° | não | 5 | 40 % | 17 | 0,7 |
| Engrenagem do pescoço (engrenagem-pescoco) | [cubo_rodas-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-pescoco.stl) | 1 | PETG prata | 35,8 × 36 × 8 | deitada | não | 5 | 60 % | 8 | 0,4 |
| Engrenagem do servo (engrenagem-servo) | [cubo_rodas-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-servo.stl) | 1 | PETG amarelo | 68,9 × 68,9 × 8 | de cabeça para baixo: a face de cima na mesa, o rebaixo do horn para cima | não | 5 | 60 % | 23 | 0,9 |
| Garfo (garfo) | [cubo_rodas-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-garfo.stl) | 1 | PETG grafite | 44 × 41,9 × 24 | deitado, costas na mesa: as camadas correm do bloco para os braços | não | 5 | 40 % | 19 | 0,8 |
| Quadro da cabeça (quadro-cabeca) | [cubo_rodas-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-quadro-cabeca.stl) | 1 | PETG amarelo | 145,2 × 93,5 × 62,7 | frente da travessa na mesa, laterais para cima | não | 4 | 30 % | 85 | 3,2 |
| Copo da cabeça (cabeca-corpo) | [cubo_rodas-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-corpo.stl) | 1 | PLA branco | 152 × 128 × 110 | costas na mesa, boca (frente) para cima, como um copo | não | 3 | 15 % | 248 | 9,3 |
| Painel do rosto (cabeca-face) | [cubo_rodas-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-face.stl) | 1 | PLA preto | 145,9 × 121,9 × 43,2 | face da frente (a que aparece) na mesa, pilares para cima | não | 3 | 20 % | 57 | 2,2 |
| Espaçador do Raspberry Pi (espacador-pi) | [cubo_rodas-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-espacador-pi.stl) | 4 | PLA cinza | 6 × 6 × 4 | em pé | não | 3 | 15 % | <1 | 0,3 |
| Cupom de teste (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **19** |  |  |  |  |  |  | **1143** | **43,4** |
<!-- /GERADO -->

O que foi feito para nenhuma peça pedir suporte:

- **Base:** piso na mesa; o furo por onde o motor entra é em gota; o poço da bola fecha em cone a 45°; a borda de baixo tem chanfro de 45°.
- **Tronco:** impresso de cabeça para baixo, com o topo na mesa; o chanfro do topo é de 45°; os trilhos do alto-falante e as 4 colunas nascem do topo.
- **Deck e alçapão:** placas planas, com os ressaltos e as cantoneiras para cima.
- **Flange e engrenagens:** deitadas.
- **Tubo do pescoço:** de cabeça para baixo, com a flange abrindo em cone a 45°.
- **Garfo:** deitado, com as costas na mesa, para as camadas correrem ao longo dos braços; furos em gota.
- **Quadro da cabeça:** frente da travessa na mesa; o servo de tilt entra num rasgo em U, sem ponte.
- **Copo da cabeça:** costas na mesa, boca para cima, como um copo; o rasgo do pescoço é em gota; não há teto.
- **Painel do rosto:** a face que aparece vai na mesa.
- **Furos da fase 2** (LiDAR, sensores de distância): cegos, por dentro. Não mudam a impressão nem aparecem por fora.

Onde cada peça é reforçada:

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| Base com rodas (base-rodas) | paredes dos motores com reforço de 4 mm e furo em gota; 4 postes Ø12 nos cantos; ressaltos nervurados do alçapão e da capa; assento cônico da bola a 45°; chanfro de 45° embaixo | cuba da base móvel: motores entram pela lateral (flange atrás da roda), bateria num alçapão por baixo, carregador USB-C e chave atrás, janela do sensor de queda no piso; por dentro, 3 janelas cegas dos sensores de distância da fase 2 (frente e lados): por fora a parede é lisa |
| Alçapão da bateria (tampa-bateria) | 4 cantoneiras + abraçadeira seguram o suporte 3x18650 | alçapão da bateria: 4 M3x8 por baixo; a bateria desce junto com ele |
| Capa da bola (capa-esfera) | 4 orelhas; boca cônica a 45° | segura a bola de 40 mm no poço; 4 M3x8 por baixo; a 8 mm do chão |
| Flange do motor (flange-motor) | disco quase maciço (5 perímetros, 60 %): leva o peso e o torque do motor | prende o motor JGB37 (6 M3x6) e fecha o furo lateral da base (4 M3x10); fica escondida atrás da roda |
| Deck (bandeja das placas) (deck) | postes do servo de pan com mãos-francesas; ressaltos nervurados do Uno e do L298N; berços com abraçadeira | bandeja de eletrônica: servo de pan, Arduino Uno, L298N, step-down do Pi e UBEC; 1,5 mm para dentro (fresta de sombra entre base e tronco) |
| Tronco (tronco) | 4 colunas Ø12 fundidas nas paredes (inserto na ponta); chanfro de 45° de 6 mm no topo; trilhos do alto-falante nascem do topo | casca de cima: 4 M3x12 entram POR BAIXO da base, atravessam o deck e rosqueiam aqui; grade do alto-falante atrás |
| Tubo do pescoço (tubo-pescoco) | 3 tirantes M3 de aço atravessam o tubo inteiro: as camadas trabalham só em compressão; flange cônica a 45° | pescoço oco (cabos por dentro); 3 M3x50 entram por baixo, pela engrenagem, e rosqueiam nos insertos do garfo |
| Engrenagem do pescoço (engrenagem-pescoco) | dentes módulo 1.5 com 5 perímetros (dente quase maciço); presa pelos 3 tirantes | 22 dentes; fica por baixo da tampa e, com a flange do tubo por cima, impede o pescoço de bambear |
| Engrenagem do servo (engrenagem-servo) | dentes módulo 1.5 com 5 perímetros; 4 parafusos no horn redondo | 44 dentes, presa no horn redondo do servo de pan (o pescoço gira 2x o servo) |
| Garfo (garfo) | camadas ao longo dos braços (flexão); bloco maciço com 3 insertos dos tirantes; furos em gota | garfo interno do tilt: fica dentro da cabeça, no topo do tubo; horn do servo num braço, pino M5 (rosca no plástico) no outro; furos de passagem da chave no braço esquerdo |
| Quadro da cabeça (quadro-cabeca) | laterais inteiras até o fundo com colunas Ø10 nos 4 insertos e mãos-francesas a 45° na travessa; servo de tilt em rasgo em U (sem ponte), 4 parafusos | esqueleto da cabeça: Raspberry Pi (4 M2,5), servo de tilt, mancal do pino; recebe o painel (4 M3 por trás) e o copo (4 M3 pela parede de trás) |
| Copo da cabeça (cabeca-corpo) | arestas compridas com raio de 20 mm (verticais na impressão) e chanfro de 45° na aresta de trás; rasgo do pescoço em gota; sem ponte nem teto | casca da cabeça (5 lados); entra por trás, 4 M3 na parede de trás; rasgo do pescoço e furos de microfone por baixo |
| Painel do rosto (cabeca-face) | 4 pilares Ø10 com 2 nervuras a 45° cada (insertos M3 na ponta); postes da câmera | painel escuro do rosto: janela da tela, furo de 8 mm da câmera acima dela; nenhum parafuso na frente |
| Espaçador do Raspberry Pi (espacador-pi) | — | 4 espaçadores de 4 mm do Raspberry Pi |
| Cupom de teste (teste-encaixe) | — | cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto |
<!-- /GERADO -->

## 4. Montagem e abertura

São 31 insertos M3 a quente. Toda a solda fica nos 4 preparos da bancada ([LIGACAO.md](LIGACAO.md)); na montagem só há
bornes e encaixes.

<!-- GERADO:parafusos -->
| Onde fica | Qtd | Parafuso | Onde rosqueia |
|---|---|---|---|
| Motor na flange (6 em cada motor) | 12 | M3 × 6 Allen | rosca do próprio motor |
| Flange na parede da base (4 em cada lado) | 8 | M3 × 10 Allen | inserto na parede da base |
| Alçapão da bateria (por baixo) | 4 | M3 × 8 | inserto no piso da base |
| Capa da bola (por baixo) | 4 | M3 × 8 | inserto no piso da base, em volta do poço |
| Arduino Uno (deck) | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Driver L298N (deck) | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Servo de pan (deck) | 4 | M3 × 12 | direto no plástico (furo de 2,7 mm) |
| Base + deck + tronco (por baixo, no fundo dos 4 postes) | 4 | M3 × 12 Allen | inserto na coluna do tronco |
| Servo de tilt (quadro da cabeça) | 4 | M3 × 12 | direto no plástico (furo de 2,7 mm) |
| Tela de 5 polegadas (pilares do painel do rosto) | 4 | M2,5 × 6 | direto no plástico (furo de 2,2 mm) |
| Painel do rosto (por trás do quadro) | 4 | M3 × 8 | inserto nos pilares do painel |
| Copo da cabeça (parede de trás) | 4 | M3 × 8 | inserto nas colunas do quadro |
| Tirantes do pescoço (por dentro do tronco) | 3 | M3 × 50 Allen | inserto no garfo |
| Pino do tilt | 1 | M5 × 16 | direto no plástico do garfo (furo de 4,4 mm) |
| Raspberry Pi | 4 | M2,5 × 12 + porca | porca atrás da travessa |
| Horn redondo dos 2 servos | 8 | M2 × 8 auto-atarraxante | nos furos do horn |
<!-- /GERADO -->

A ordem abaixo é a que o verificador percorreu (teste 9): cada peça entra pelo lado indicado sem bater no que já está
montado. O passo "fiação da cabeça" não é uma peça e por isso não é testado: ele entra antes do copo porque o rasgo
do pescoço, no fundo do copo, é fechado.

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | base-rodas | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, servos em 90°, cabos prontos, cartão gravado) e assente os 31 insertos a quente. |
| 2 | motor direito com a flange, pela lateral (6 M3x6 + 4 M3x10) | pela direita | Na bancada, prenda o motor na flange com 6 × M3 × 6: a cabeça de cada parafuso fica no rebaixo. Passe o cabo de 6 fios para dentro da base pelo furo da parede e enfie o motor, com o eixo para baixo (ele fica 7 mm abaixo do centro). Depois, 4 × M3 × 10 nos insertos da parede. |
| 3 | motor esquerdo com a flange, pela lateral | pela esquerda | Igual ao motor direito. |
| 4 | roda direita com o adaptador sextavado | pela direita | Adaptador no eixo do motor, com o parafuso de trava apertado sobre a face chata do eixo. Roda no sextavado, presa pelo parafuso da ponta do adaptador. Sobram cerca de 2,5 mm entre a flange e a roda. |
| 5 | roda esquerda com o adaptador sextavado | pela esquerda | Igual à roda direita. |
| 6 | bola e capa, por baixo (4 M3x8) | por baixo | Bola no poço e capa por baixo, com 4 × M3 × 8. A bola tem de girar solta. |
| 7 | carregador USB-C e BMS no piso | por cima | O chicote já vem soldado e conferido do preparo 1. O carregador vai no berço, com 1 abraçadeira e a boca USB-C encostada na janela de trás. A placa de proteção vai com fita dupla-face. |
| 8 | chave (por fora, atrás) | por trás | Já está no lugar desde o preparo 1. Ela encaixa por pressão no recorte, por fora, com os 2 fios passando pelo recorte. |
| 9 | bateria no alçapão, por baixo (4 M3x8) | por baixo | Prenda o suporte nas 4 cantoneiras do alçapão, com 1 abraçadeira. Com a chave desligada, ponha as 3 células, conferindo o lado do positivo com o multímetro. Suba o alçapão e prenda com 4 × M3 × 8. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 10 | servo de pan, Uno, L298N, step-down e UBEC no deck (bancada) | por cima | Servo de pan: 4 × M3 × 12, eixo para cima. Ele já está em 90° (preparo 2): não gire o eixo com a mão. Arduino Uno: 4 × M3 × 8, com o sketch já gravado. Se o shield cobrir os furos de fixação do Uno (não confirmado), parafuse o Uno sem ele e encaixe o shield depois, com o jumper SEL retirado. Driver L298N: 4 × M3 × 8, já sem os 3 jumpers (preparo 1). Conversor e UBEC nos berços, com 1 abraçadeira cada. A barra de emenda, com o divisor já preso nela, fica solta ao lado do Arduino. Refaça no shield as ligações que você desfez no fim do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra no + e no − do conector COM, servo de pan no D9. Ligue os 6 jumpers do driver. No COM, os pinos TX e RX ficam vazios. |
| 11 | engrenagem do servo no horn (bancada) | por cima | Horn redondo no rebaixo da engrenagem, 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 6 mm. Não gire o eixo: ele está em 90°. |
| 12 | deck montado sobre a base | por cima | Chave desligada. Antes de assentar o deck, passe para cima os fios que vêm da base: o cabo de cada motor por um dos 2 rasgos laterais e os 2 fios da chave e da placa de proteção pelo rasgo de trás. O deck fica solto sobre os 4 postes: quem o prende é o tronco. Agora ligue, só por borne e encaixe: o fio vermelho da chave no borne 4 e o preto da placa de proteção no borne 5; de cada motor, o vermelho e o branco nos bornes de saída do driver (motor direito em OUT1 e OUT2, esquerdo em OUT3 e OUT4), o azul no borne +5V do driver, o preto no borne GND do driver, o amarelo e o verde nos conectores do shield (direito: D2 e A0; esquerdo: D3 e A1), sempre no pino S. |
| 13 | Raspberry Pi e espaçadores no quadro (bancada) | pela frente | 4 × M2,5 × 12 com porca; os 4 espaçadores ficam entre o Pi e a travessa. O cartão microSD já gravado (preparo 4) entra antes. Cole os dissipadores. Encaixe agora os 3 jumpers da serial nos pinos 32, 33 e 34 e os 4 conectores do cabo de energia nos pinos 2, 4, 6 e 9 (preparo 3): depois que o painel com a tela entra, fica difícil alcançar os pinos. |
| 14 | tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada) | pela frente | Primeiro prenda a tela nos 4 pilares do painel do rosto, com 4 × M2,5 × 6, e encaixe nela o cabo HDMI e o cabo USB. A câmera é da fase 2: é opcional agora, e o furo dela fica vazio. Depois, 4 × M3 × 8 por trás da travessa, nos insertos dos pilares do painel. Ligue os 2 cabos da tela no Raspberry Pi. Depois que o servo entra, esses parafusos ficam sem acesso. |
| 15 | servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada) | por trás | 4 × M3 × 12. O servo já está em 90° (preparo 2). Os 2 parafusos de cima são apertados pelos furos de acesso da lateral esquerda. |
| 16 | garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada) | por baixo | Prenda o horn no braço direito do garfo com 4 × M2 × 8. Com o servo em 90°, encaixe o garfo apontando para baixo, com o rosto na vertical. O parafuso central do horn entra pelo furo do pino. Por último, o M5 × 16: aperte até encostar e volte um quarto de volta, porque a cabeça gira nele. |
| 17 | fiação da cabeça, antes de fechar com o copo (bancada) | fios, de cima para baixo | É a última vez que você alcança o Raspberry Pi. 1) Confira nos pinos do Pi os 4 conectores do cabo de energia (pinos 2, 4, 6 e 9) e os 3 da serial (pinos 32, 33 e 34), postos antes da tela. 2) Confira os 2 cabos da tela, HDMI e USB, encaixados no Pi e sem forçar a parede da cabeça. 3) Ligue a extensão de 30 cm no cabo do servo de tilt. 4) Desça os 8 fios pelo furo de 9 mm do garfo, de cima para baixo, primeiro o conector da extensão. Pare quando as pontas ficarem rentes à face de baixo do garfo. 5) Deixe uma barriga de uns 5 cm de fio dentro da cabeça: ela inclina em volta do garfo e os fios dobram ali. |
| 18 | copo da cabeça por trás; 4 M3 na parede de trás (bancada) | por trás | O fundo do copo passa por baixo do garfo: confira que nenhum fio sobra para fora do furo do garfo. 4 × M3 × 8. Depois, com a pinça, puxe as pontas dos 8 fios para fora pelo rasgo do fundo do copo. |
| 19 | alto-falante nos trilhos do tronco, por baixo (bancada) | por baixo | Fase 2: é opcional agora, pode pular. |
| 20 | tubo do pescoço no tronco, por cima (bancada) | por cima | A flange cônica apoia no topo do tronco. |
| 21 | engrenagem do pescoço por dentro do tronco (bancada) | por baixo | Alinhe os 3 furos com os do tubo. |
| 22 | cabeça sobre o tubo; 3 tirantes M3 por dentro do tronco (bancada) | por cima | Enfie os 8 fios pelo tubo do pescoço, de cima para baixo, e só então assente a cabeça, sem prender fio entre o garfo e o tubo. 3 × M3 × 50 por dentro do tronco, de baixo para cima, pela engrenagem, até os insertos do garfo. |
| 23 | LiDAR no topo da cabeça (fase 2) | por cima | Fase 2: é opcional agora, pode pular. Os furos são cegos: por fora não aparece nada enquanto o sensor não for instalado. |
| 24 | tronco + pescoço + cabeça sobre o deck; 4 M3x12 por baixo da base | por cima | Chave desligada. Nenhuma solda aqui, só bornes e encaixes: os 2 fios de 5,1 V nos bornes 1 e 2 da barra de emenda; o fio azul no borne 3; o conector do fio verde no pino S do D0 e o do preto no pino G do D0; o jumper do divisor no pino S do D1; a extensão do servo de tilt no D10. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos, que queimam o Raspberry Pi. Deixe 10 cm de folga para o giro. Com a cabeça olhando para a frente e o servo de pan em 90°, engrene os dentes. Deite o robô de lado, com cuidado, e ponha os 4 × M3 × 12 por baixo, no fundo dos furos dos 4 postes, com a chave Allen longa: eles atravessam o deck e rosqueiam nos insertos do tronco. |
<!-- /GERADO -->

Para manutenção, três aberturas independentes, também percorridas pelo teste 9:

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | abrir: alçapão com a bateria sai por baixo | Desligue a chave antes. Solte os 4 parafusos de baixo e desça o alçapão: a bateria vem junto, presa pelos fios, que têm folga. |
| 2 | abrir: motor direito sai pela lateral (roda, depois flange + motor) | Tire o parafuso da ponta do adaptador e puxe a roda. Solte os 4 parafusos da flange e puxe o motor para fora. Antes, solte no deck os 6 fios do cabo dele; para isso é preciso levantar o tronco. |
| 3 | abrir: tronco + pescoço + cabeça saem por cima (placas do deck à mostra) | Solte os 4 parafusos por baixo da base e levante o conjunto inteiro, devagar: os fios do pescoço continuam ligados. É assim que se chega ao USB do Arduino. |
<!-- /GERADO -->

O teste prova o caminho da peça, não o da ferramenta. Os 4 parafusos de baixo ficam no fundo de furos de 68 mm: é
preciso uma chave Allen de 2,5 mm com haste de 80 mm ou mais.

## 5. Energia

Pack 3S → fusível T3A → placa de proteção → chave → barra de emenda no deck → XL4015 (5,1 V), UBEC (6 V) e driver
L298N (motores). O carregador USB-C fica ligado na saída da placa de proteção, antes da chave. O esquema, a tabela
fio a fio, os 4 preparos e os avisos de segurança estão em [LIGACAO.md](LIGACAO.md).

| Linha | De onde vem | O que alimenta | Conta (pelas fichas, não medida) |
|---|---|---|---|
| 5,1 V | XL4015, até 5 A | Raspberry Pi, tela, Arduino, comando do driver, encoders | cerca de 1,5 A em uso normal |
| 6 V | UBEC, 3 A contínuos | 2 servos MG996R | menos de 1 A em uso normal; os 2 travados podem pedir mais que os 3 A do UBEC |
| 9 a 12,6 V | pack, pelo driver L298N | 2 motores JGB37 | 0,2 A cada andando; 1,2 A cada travado |

- **Uso normal:** cerca de 2 A saindo do pack. **Pior caso:** cerca de 6,5 A (rodas travadas, servos no limite, Pi no máximo, pack em 9 V).
- **A chave é de 3 A** (KCD11-101: 3 A em 250 V~, sem valor para corrente contínua). O fusível T3A protege a chave. É o ponto mais fraco: no pior caso o fusível abre. Trocar por uma chave maior exige mudar o recorte de 13,5 × 9 mm na base.
- **O programa da fase 2** tem de acelerar em rampa, parar o motor que travar e não deixar os servos forçando no fim do curso.
- **O carregador vem pronto para 2 células.** Passá-lo para 3 exige tirar um resistor e fechar um jumper de solda. Os nomes das ilhas das emendas, nele e na placa de proteção, não foram lidos: o guia manda conferir com o multímetro.

## 6. Estabilidade

O robô apoia em 3 pontos: as 2 rodas na frente e a bola atrás. O verificador (teste 8) exige o centro de massa a pelo
menos 10 mm de dentro do triângulo de apoio, com a cabeça em 11 posições.

- Centro de massa com a cabeça reta: 41,1 mm atrás do eixo das rodas e 127,4 mm acima do chão. Margem: 41,1 mm (tomba só com 18° de inclinação).
- Pior posição parado: cabeça girada 170° e inclinada para baixo. Margem: 37,6 mm (17°).

Andando, a conta é de corpo rígido (aceleração máxima = gravidade × alcance ÷ altura do centro de massa), no pior caso
de posição da cabeça:

| Manobra | Aceleração máxima sem tombar |
|---|---|
| Frear andando para a frente | 2,98 m/s² (0,30 g) |
| Arrancar para a frente ou frear de ré | 4,93 m/s² (0,50 g) |
| Curva | 3,72 m/s² (0,38 g) |

- Velocidade máxima, com o motor sem carga: 0,48 m/s. Nessa velocidade, a parada mais curta sem tombar leva 38 mm.
- É estimativa: o programa da fase 2 deve usar no máximo a metade desses valores.
- Degrau: a capa da bola fica a 8 mm do chão. A norma brasileira de acessibilidade (NBR 9050) trata desníveis de até 5 mm como piso contínuo; soleiras mais altas que 8 mm o robô não passa.

## 7. Preparado para a fase 2

A fase 2 (andar, rosto na tela, voz, câmera, sensores, IA) não foi feita. As peças já têm o lugar, os furos e a
passagem dos cabos.

**Olhos e câmera.** Os outros robôs do projeto têm olhos de plástico, e neles a escolha foi entre (a) uma câmera em
cada pupila, (b) câmera numa pupila e sensor de distância na outra, ou (c) câmera grande-angular num olho e o sensor
escondido em outro lugar. Aqui essa escolha não se aplica: os olhos são desenhados na tela, e não há pupila onde
esconder nada. A decisão foi **uma câmera só, atrás do painel escuro do rosto, num furo de 8 mm acima da tela**. Ela
gira e inclina com a cabeça, e o Raspberry Pi 4 só tem uma entrada de câmera. A distância fica com os 3 sensores da
borda da base e, para mapear, com o LiDAR no topo.

Nenhum furo técnico aparece de frente nem de 3/4:

| Sensor ou peça da fase 2 | Onde está o furo | O que se vê por fora |
|---|---|---|
| Câmera | Atrás do painel do rosto, acima da tela; 4 postes para parafuso M2 | Um furo escuro de 8 mm no painel escuro |
| Microfones (2) | Por baixo da cabeça, 2 furos de 2 mm | Nada, de frente ou de lado |
| Alto-falante de 40 mm | Parede de trás do tronco, em 2 trilhos | Grade de fendas verticais, só por trás |
| Sensores de distância (3) | Por dentro da parede da base, 10 mm abaixo da borda de cima: frente e 2 lados; em cada ponto, 2 furos cegos e, entre eles, uma janela cega de 6,5 mm | Nada, até a pele de 0,8 mm ser furada na instalação (centro marcado por dentro, broca de 6 mm por fora); depois, 3 furos de 6 mm |
| Sensor de queda | Janela de 14 × 6 mm no piso da base, na frente | Só por baixo |
| Sensor de movimento (IMU) | Par de furos M3 a 20 mm no deck, perto do eixo das rodas | Nada (fica dentro) |
| LiDAR LD19 | Topo da cabeça: 3 furos cegos por dentro e um rebaixo cego do cabo | Nada, até a pele de 0,8 mm ser furada na instalação |
| Carga USB-C e chave | Parede de trás da base | Só por trás |

O LiDAR vai no topo da cabeça porque é o único lugar com 360° livres. Como a cabeça gira e inclina, o programa deve
mapear com a cabeça reta e descontar o ângulo do pescoço.

<!-- GERADO:fase2 -->
| Item (o nome abre a busca) | Qtd | Onde fica | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (placa de 25 × 24 mm) com cabo flat](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Atrás do painel do rosto, no furo de 8 mm acima da tela. 4 postes com furo para parafuso M2. NC: furos e altura da lente. | R$ 180–350 | não conferido |
| [Parafuso M2 × 6 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Prende a câmera nos 4 postes. | R$ 3–8 | R$ 5,98 o kit com 10 |
| [Microfone I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Dentro da cabeça, sobre os 2 furos de 2 mm que ficam por baixo dela. De frente e de lado não aparecem. NC: fixação do microfone ainda não modelada. | R$ 15–55 | R$ 54,26 |
| [Alto-falante de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Desliza nos 2 trilhos da parede de trás do tronco, contra a grade de fendas verticais. Só aparece por trás. NC: diâmetro e profundidade. | R$ 7–20 | não conferido |
| [Amplificador de áudio pequeno (PAM8403 ou MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Sem lugar modelado ainda: vai solto no deck, com fita dupla-face. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | No ponto universal do deck (par de furos M3 a 20 mm), perto do eixo das rodas. | R$ 15–35 | R$ 34,09 |
| [LiDAR LD19](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | No topo da cabeça, o único lugar com 360° livres: 3 furos cegos por dentro e um rebaixo cego para o cabo. A pele de 0,8 mm só é furada quando o sensor for instalado; até lá, nada aparece por fora. Com ele o robô fica com 341 mm de altura. NC: posição dos 3 furos no corpo do sensor. | R$ 400–900 | não conferido |
| [Sensor de distância ToF VL53L1X (placa pequena)](https://lista.mercadolivre.com.br/sensor-vl53l1x-tof) | 3 | Por dentro da parede da base, 10 mm abaixo da borda de cima: um na frente e um de cada lado. Cada ponto tem 2 furos cegos para parafuso M2,5 e, entre eles, uma janela cega: por fora a parede é lisa, com 0,8 mm de plástico na frente da janela. Na instalação, vare essa pele por dentro, no centro da janela, com um prego ou uma agulha quente: a furadeira não cabe dentro da base. O furinho marca o centro do lado de fora; alargue por fora com broca de 6 mm. Depois disso ficam 3 furos de 6 mm à vista na base. NC: tamanho da placa (25 × 10,7 mm) e distância entre os furos. | R$ 40–110 | R$ 102,32 |
| [Sensor de queda (reflexivo infravermelho, por exemplo TCRT5000)](https://lista.mercadolivre.com.br/sensor-reflexivo-infravermelho-tcrt5000) | 1 | Numa janela de 14 × 6 mm no piso da base, na frente, olhando para o chão, com um par de furos M3 a 20 mm. Só aparece por baixo. | R$ 5–15 | R$ 7,92 |
<!-- /GERADO -->

Sem lugar modelado ainda: o amplificador de áudio e a fixação dos microfones. O alto-falante fica no tronco e o
Raspberry Pi na cabeça: os fios do áudio também terão de passar pelo pescoço.

## 8. Semelhança com a referência

O projeto mede a semelhança de cada robô com a imagem de referência pela sobreposição das silhuetas (IoU: 1,0 = igual).
Para este robô não existe imagem de referência própria. A medida foi feita contra a imagem do robô quadrado de mesa,
na vista de 3/4: **IoU 0,669** (0,709 com o enquadramento ajustado). O número serve só de registro: o corpo com rodas
não existe naquela imagem, e por isso ele **não é uma meta**.

## 9. Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py cubo_rodas` (cópia completa em `verificacao-saida.txt`):

<!-- GERADO:verificacao -->
```
== verificação: cubo_rodas
  [PASSOU] 1 contagem: 15 peças distintas, 19 no total (esperado 19); faltando 0; sobrando 0
  [PASSOU] 2 malha: 15 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 182.0 mm (base-rodas)
  [PASSOU] 4 parede: modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm)
  [PASSOU] 5 interferência: 41 sólidos (18 impressos + 23 componentes), 11 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem)
  [PASSOU] 6 teste negativo: 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 18 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 2214 g; CG neutro em x=1.0 y=-41.1 z=127.4 mm, margem 41.1 mm (tomba com 18°); pior pose 'pan+170+tilt-baixo': margem 37.6 mm (17°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 26 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 15 peças distintas: 15 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'deck' na orientação declarada: 0 mm² sem apoio (limite 106); girada 180° em X → 19084 mm² = 36.1 % (acusou; tem que acusar)
```
<!-- /GERADO -->

O que os testes não veem: o caminho da chave até cada parafuso, furo que vaza uma parede de fora, os cabos (nenhum fio
está no modelo) e tudo o que depende de medida não confirmada.

## 10. Pendências

1. **Imprimir e montar.** Nada foi testado em plástico. Comece pelo cupom de teste.
2. **Testar a parte elétrica na bancada.** O esquema saiu das fichas; nenhum fio foi ligado.
3. **Chave de 3 A.** Pequena para o pior caso (cerca de 6,5 A). Decidir entre trocar a chave (e o recorte na base) ou aceitar o limite com o programa em rampa.
4. **Cabos da tela.** O HDMI e o USB não estão no modelo: sobram cerca de 22 mm abaixo do Raspberry Pi e cerca de 30 mm ao lado das portas USB. Conferir com as peças na mão.
5. **Carregador para 3 células.** Exige uma solda muito pequena na placa. Avaliar um carregador que já venha para 3 células.
6. **Medidas não confirmadas (NC):** posição dos 6 furos do motor em volta do eixo e fundo da rosca; espessura (14 mm) e massa (150 g) da tela; posição dos 3 furos do LiDAR; nomes das ilhas da placa de proteção e do carregador; conectores A0 e A1 do shield; distância entre os furos do driver.
7. **Cupom de teste próprio dos robôs quadrados.** O cupom comum não testa a janela do MG996R, a rosca do M5 nem os furos do motor.
8. **Sem fixação modelada:** porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e microfones.
9. **Passagem dos 8 fios** pelo furo do garfo e pelo rasgo do fundo da cabeça: nunca ensaiada. O rasgo do copo é fechado; abri-lo até a borda facilitaria.
10. **Calor.** O Raspberry Pi fica fechado numa cabeça de PLA sem ventilação. Medir em uso.
11. **Estabilidade andando.** A conta é de corpo rígido; medir com o robô montado.
12. **Driver.** O L298N tira cerca de 2 V dos motores. Trocar por um TB6612 fica para depois.
13. **Regravar o Arduino** exige levantar o tronco. Uma janela para o cabo USB resolveria.
14. **3MF das mesas** ainda não foram abertos no Bambu Studio.
15. **Semelhança:** falta uma imagem de referência própria deste robô.
