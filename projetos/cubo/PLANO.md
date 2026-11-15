# Plano do robô quadrado de mesa (`cubo`)

Robô de mesa de 20 cm: uma cabeça em cubo, com tela no rosto, que gira quase uma volta e inclina. Não roda. Este arquivo
guarda as decisões do projeto deste robô e os porquês. Para fazer o robô, use os guias:
[LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md), [IMPRIMIR.md](IMPRIMIR.md) e [LIGACAO.md](LIGACAO.md). O resumo está no
[README.md](README.md); as decisões que valem para os 4 robôs, no [PLANO.md da raiz](../../PLANO.md).

Fase 1 = mecânica e encaixe: corpo impresso, montado e ligado. A fase 2 (programa, rosto na tela, voz, câmera, IA) não
está feita; a seção 7 diz o que já tem lugar nas peças. **Nada foi impresso ainda.**

## 1. O que é e números

<!-- GERADO:numeros -->
- Altura montado: 200,5 mm.
- Peças impressas: 15 (12 arquivos diferentes), em 7 mesas.
- Filamento: 735 g. Tempo de impressão: 28,2 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 16.
<!-- /GERADO -->
- Tamanho: base de 158 × 146 × 60,5 mm; cabeça de 136 × 102 × 118 mm, com raio de 20 mm nas arestas; pescoço de 28 mm de diâmetro, com 22 mm de vão entre a base e a cabeça.
- Massa: 1147 g montado (estimativa).
- Movimentos: pan de ±170°, tilt de −25° a +30°. O verificador confere 10 poses.

## 2. Decisões e porquês

| Decisão | Por quê | O que foi descartado |
|---|---|---|
| O servo que inclina fica dentro da cabeça | O garfo do tilt é interno, no topo do tubo do pescoço. De fora só se vê o pescoço fino, como na referência. | Garfo externo, com os rasgos do horn à mostra dos dois lados da cabeça. |
| Pan por 2 engrenagens impressas, de 44 e 22 dentes | Um servo comum de 180° passa a girar o pescoço 340°. O tubo do pescoço é oco e leva os cabos por dentro. | — |
| 3 tirantes M3 × 45 de aço atravessam o tubo do pescoço | As camadas do tubo trabalham só em compressão; quem segura a cabeça é o aço. | — |
| Cabeça = copo de 5 lados + painel escuro do rosto + quadro | O copo imprime com as costas na mesa, sem ponte nem teto. O painel entra 1 mm para dentro e é preso por trás, em 4 pilares. O quadro de PETG leva o Raspberry Pi, a tela e o servo. | — |
| Nenhum parafuso na frente nem em cima | Tampa da base: 4 parafusos por baixo, no fundo de um furo. Copo da cabeça: 4 na parede de trás. Porta da bateria: 1, atrás. | Parafusos de cabeça chata à vista na tampa e no rosto. |
| Pino do tilt = parafuso M5 × 16 rosqueado direto no braço do garfo | O furo dele é também a passagem da chave até o parafuso central do horn. | M3 com inserto: não deixava a chave passar. |
| Tela de 3,5" espetada nos pinos do Raspberry Pi | Não precisa de cabo nem de parafuso: a tela é o rosto. | — |
| Base baixa, com as placas e a bateria no piso | O peso fica embaixo: o centro de massa fica a 76 mm do chão. | — |
| Raspberry Pi e Arduino conversam por uma serial de 3 fios | O furo de cabos do pescoço tem 9 mm e um plugue USB não passa por ele. | Cabo USB pelo pescoço. |

## 3. Peças impressas e imprimibilidade

A regra do projeto: imprimir sem suporte sempre que der. Face plana na mesa, balanços de até 45°, pontes de até 20 mm,
furo horizontal em gota, chanfro de 45° nas bordas viradas para baixo. O verificador mede a área sem apoio de cada peça
(teste 10) e reprova a peça declarada sem suporte que precisaria dele.

Resultado: **as 12 peças diferentes saem sem suporte.** O que foi feito para chegar aí: copo da cabeça impresso como um
copo, com as costas na mesa; rasgo do pescoço e furos horizontais em gota; servo de tilt num rasgo em U, sem ponte;
flange do tubo do pescoço em cone de 45°; pilares do painel do rosto com nervuras a 45°; garfo deitado, com as camadas
correndo do bloco para os braços.

As peças que fazem força (base, tampa, pescoço, engrenagens, garfo e quadro da cabeça) são de PETG, com 4 ou 5
perímetros. As tabelas abaixo trazem, por peça, a orientação na mesa, o suporte, os perímetros, o preenchimento e o
motivo de cada reforço.

<!-- GERADO:pecas -->
| Peça | Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base (base) | [cubo-base.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-base.stl) | 1 | PETG grafite | 158 × 146 × 56,5 | piso na mesa | não | 4 | 20 % | 222 | 8,2 |
| Tampa da base (tampa-base) | [cubo-tampa-base.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-tampa-base.stl) | 1 | PETG grafite | 158 × 146 × 18 | de cabeça para baixo: a face de cima na mesa | não | 4 | 25 % | 101 | 3,8 |
| Porta traseira (porta-traseira) | [cubo-porta-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-porta-traseira.stl) | 1 | PETG grafite | 45,4 × 52,6 × 5 | face de fora na mesa | não | 3 | 20 % | 9 | 0,4 |
| Tubo do pescoço (tubo-pescoco) | [cubo-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-tubo-pescoco.stl) | 1 | PETG prata | 40 × 40 × 32,6 | de cabeça para baixo: o topo (lado do garfo) na mesa, a flange cônica abre a 45° | não | 5 | 40 % | 16 | 0,7 |
| Engrenagem do pescoço (engrenagem-pescoco) | [cubo-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-engrenagem-pescoco.stl) | 1 | PETG prata | 36 × 36 × 8 | deitada | não | 5 | 60 % | 8 | 0,4 |
| Engrenagem do servo (engrenagem-servo) | [cubo-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-engrenagem-servo.stl) | 1 | PETG amarelo | 69 × 69 × 8 | de cabeça para baixo: a face de cima na mesa, o rebaixo do horn para cima | não | 5 | 60 % | 23 | 0,9 |
| Garfo (garfo) | [cubo-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-garfo.stl) | 1 | PETG grafite | 44 × 41,9 × 24 | deitado, costas na mesa: as camadas correm do bloco para os braços | não | 5 | 40 % | 19 | 0,8 |
| Quadro da cabeça (quadro-cabeca) | [cubo-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-quadro-cabeca.stl) | 1 | PETG amarelo | 129,2 × 74,6 × 63,7 | frente da travessa na mesa, laterais para cima | não | 4 | 30 % | 65 | 2,4 |
| Copo da cabeça (cabeca-corpo) | [cubo-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-cabeca-corpo.stl) | 1 | PLA branco | 136 × 118 × 102 | costas na mesa, boca (frente) para cima, como um copo | não | 3 | 15 % | 204 | 7,7 |
| Painel do rosto (cabeca-face) | [cubo-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-cabeca-face.stl) | 1 | PLA preto | 129,9 × 111,9 × 34,2 | face da frente (a que aparece) na mesa, pilares para cima | não | 3 | 20 % | 53 | 2,0 |
| Espaçador do Raspberry Pi (espacador-pi) | [cubo-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/stl/cubo-espacador-pi.stl) | 4 | PLA cinza | 6 × 6 × 5 | em pé | não | 3 | 15 % | <1 | 0,3 |
| Cupom de teste (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **15** |  |  |  |  |  |  | **735** | **28,2** |
<!-- /GERADO -->

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| Base (base) | chanfro de 45° na aresta de baixo; postes da tampa Ø12 fundidos nos cantos; postes do servo com mãos-francesas; ressaltos nervurados do Uno; fendas verticais na grade | cuba: piso, paredes, postes do servo de pan, do Uno e da tampa, berços dos módulos de energia (abraçadeira), trilhos do alto-falante; chave, USB-C e grade atrás |
| Tampa da base (tampa-base) | 4 ressaltos de inserto com 3 nervuras a 45°; chanfro de 45° na aresta que encosta na mesa | presa por 4 M3x10 que entram POR BAIXO da base; a flange do pescoço gira sobre ela; orelha do parafuso da porta |
| Porta traseira (porta-traseira) | — | porta da bateria (atrás); 1 M3 na orelha da tampa, pé contra 2 batentes do piso |
| Tubo do pescoço (tubo-pescoco) | 3 tirantes M3 de aço atravessam o tubo inteiro: as camadas trabalham só em compressão; flange cônica a 45° | pescoço oco (cabos por dentro); 3 M3x45 entram por baixo, pela engrenagem, e rosqueiam nos insertos do garfo |
| Engrenagem do pescoço (engrenagem-pescoco) | dentes módulo 1.5 com 5 perímetros (dente quase maciço); presa pelos 3 tirantes | 22 dentes; fica por baixo da tampa e, com a flange do tubo por cima, impede o pescoço de bambear |
| Engrenagem do servo (engrenagem-servo) | dentes módulo 1.5 com 5 perímetros; 4 parafusos no horn redondo | 44 dentes, presa no horn redondo do servo de pan (o pescoço gira 2x o servo) |
| Garfo (garfo) | camadas ao longo dos braços (flexão); bloco maciço com 3 insertos dos tirantes; furos em gota | garfo interno do tilt: fica dentro da cabeça, no topo do tubo; horn do servo num braço, pino M5 (rosca no plástico) no outro; furos de passagem da chave no braço esquerdo |
| Quadro da cabeça (quadro-cabeca) | laterais inteiras até o fundo com colunas Ø10 nos 4 insertos e mãos-francesas a 45° na travessa; servo de tilt em rasgo em U (sem ponte), 4 parafusos | esqueleto da cabeça: Raspberry Pi (4 M2,5), servo de tilt, mancal do pino; recebe o painel (4 M3 por trás) e o copo (4 M3 pela parede de trás) |
| Copo da cabeça (cabeca-corpo) | arestas compridas com raio de 20 mm (verticais na impressão) e chanfro de 45° na aresta de trás; rasgo do pescoço em gota; sem ponte nem teto | casca da cabeça (5 lados); entra por trás, 4 M3 na parede de trás; rasgo do pescoço e furos de microfone por baixo |
| Painel do rosto (cabeca-face) | 4 pilares Ø10 com 2 nervuras a 45° cada (insertos M3 na ponta); postes da câmera | painel escuro do rosto: janela da tela, furo de 8 mm da câmera acima dela; nenhum parafuso na frente |
| Espaçador do Raspberry Pi (espacador-pi) | — | 4 espaçadores de 5 mm do Raspberry Pi |
| Cupom de teste (teste-encaixe) | — | cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto |
<!-- /GERADO -->

## 4. Montagem e abertura

A ordem abaixo é a que o verificador percorre (teste 9): cada peça entra pelo lado indicado, contra o que já está
montado, sem bater. O teste prova o caminho da peça, não o da ferramenta nem o dos fios: a passagem dos 8 fios pelo
pescoço é um passo à parte, descrito em [LIGACAO.md](LIGACAO.md).

### Parafusos

<!-- GERADO:parafusos -->
| Onde fica | Qtd | Parafuso | Onde rosqueia |
|---|---|---|---|
| Tampa na base (por baixo) | 4 | M3 × 10 Allen | inserto na tampa |
| Porta traseira | 1 | M3 × 8 | inserto na orelha da tampa |
| Arduino Uno | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Servo de pan (base) | 4 | M3 × 12 | direto no plástico (furo de 2,7 mm) |
| Servo de tilt (quadro da cabeça) | 4 | M3 × 12 | direto no plástico (furo de 2,7 mm) |
| Painel do rosto (por trás do quadro) | 4 | M3 × 8 | inserto nos pilares do painel |
| Copo da cabeça (parede de trás) | 4 | M3 × 8 | inserto nas colunas do quadro |
| Tirantes do pescoço | 3 | M3 × 45 Allen | inserto no garfo |
| Pino do tilt | 1 | M5 × 16 | direto no plástico do garfo (furo de 4,4 mm) |
| Raspberry Pi | 4 | M2,5 × 12 + porca | porca atrás da travessa |
| Horn redondo dos 2 servos | 8 | M2 × 8 auto-atarraxante | nos furos do horn |
<!-- /GERADO -->

### Passo a passo

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | base | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, servos em 90°, cabo da serial e divisor prontos, cartão gravado) e assente os 16 insertos a quente. |
| 2 | servo de pan nos 2 postes | por cima | 4 × M3 × 12, eixo para cima. O servo já está em 90° (preparo 2): não gire o eixo com a mão. |
| 3 | Arduino Uno nos 4 ressaltos | por cima | 4 × M3 × 8, USB virado para a esquerda. Se o shield cobrir os furos de fixação do Uno (não confirmado), parafuse o Uno sem ele e encaixe o shield depois, com o jumper SEL retirado. O sketch já tem de estar gravado (preparo 2): com o Uno parafusado, o cabo USB não entra. |
| 4 | módulos de energia nos berços (1 abraçadeira cada) | por cima | O chicote já vem soldado e conferido do preparo 1. 3 abraçadeiras (conversor, UBEC, carregador) e fita dupla-face na placa de proteção. A boca USB-C do carregador encosta na janela de trás. A barra de emenda, com o divisor já preso nela (preparo 3), fica solta ao lado do Arduino. Refaça no shield as ligações que você desfez no fim do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra de emenda no + e no − do conector COM, servo de pan no D9. No COM, os pinos TX e RX ficam vazios. |
| 5 | chave (por fora, atrás) | por trás | Já está no lugar desde o preparo 1. Ela encaixa por pressão no recorte, por fora, com os 2 fios passando pelo recorte. |
| 6 | alto-falante nos trilhos da parede de trás | por cima | Fase 2: é opcional agora, pode pular. |
| 7 | engrenagem do servo no horn | por cima | Horn redondo no rebaixo da engrenagem, 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 6 mm. Não gire o eixo: ele está em 90°. |
| 8 | bateria (pela porta de trás) | por trás | O suporte já está soldado no chicote desde o preparo 1, sem as células: assente-o no berço. Com a chave desligada, ponha agora as 2 células, conferindo o lado do positivo com o multímetro. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 9 | Raspberry Pi e espaçadores no quadro (bancada) | pela frente | 4 × M2,5 × 12 com porca; os 4 espaçadores ficam entre o Pi e a travessa. O cartão microSD já gravado (preparo 4) entra antes. Cole os dissipadores. Encaixe agora, nos pinos 31 a 34, o conector baixo com os 3 fios da serial (feito no preparo 3): depois que a tela entra, ele não entra mais. |
| 10 | tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada) | pela frente | A tela encaixa nos pinos 1 a 26 do Pi. A câmera é da fase 2: é opcional agora, e o furo dela fica vazio. 4 × M3 × 8 por trás da travessa, nos insertos dos pilares do painel. Depois que o servo entra, esses parafusos ficam sem acesso. |
| 11 | servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada) | por trás | 4 × M3 × 12. O servo já está em 90° (preparo 2). Os 2 parafusos de cima são apertados pelos furos de acesso da lateral esquerda. |
| 12 | garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada) | por baixo | Prenda o horn no braço direito do garfo com 4 × M2 × 8. Com o servo em 90°, encaixe o garfo apontando para baixo, com o rosto na vertical. O parafuso central do horn entra pelo furo do pino. Por último, o M5 × 16: aperte até encostar e volte um quarto de volta, porque a cabeça gira nele. |
| 13 | fiação da cabeça, antes de fechar com o copo (bancada) | fios, de cima para baixo | É a última vez que você alcança o Raspberry Pi. 1) Parafuse os 2 fios de 5,1 V (20 AWG) no adaptador USB-C, vermelho no + e preto no −, e encaixe o adaptador na porta USB-C do Pi. 2) Confira o conector baixo da serial nos pinos 31 a 34 (ele entrou antes da tela, com os 3 fios já soldados no preparo 3). 3) Ligue a extensão de 30 cm no cabo do servo de tilt. 4) Desça os 8 fios pelo furo de 9 mm do garfo, de cima para baixo, primeiro o conector da extensão. Pare quando as pontas ficarem rentes à face de baixo do garfo. 5) Deixe uma barriga de uns 5 cm de fio dentro da cabeça: ela inclina em volta do garfo e os fios dobram ali. |
| 14 | copo da cabeça por trás; 4 M3 na parede de trás (bancada) | por trás | O fundo do copo passa por baixo do garfo: confira que nenhum fio sobra para fora do furo do garfo. 4 × M3 × 8. Depois, com a pinça, puxe as pontas dos 8 fios para fora pelo rasgo do fundo do copo. |
| 15 | tubo do pescoço na tampa, por cima (bancada) | por cima | A flange cônica apoia na tampa. |
| 16 | engrenagem do pescoço por baixo da tampa (bancada) | por baixo | Alinhe os 3 furos com os do tubo. |
| 17 | cabeça sobre o tubo; 3 tirantes M3 por baixo (bancada) | por cima | Enfie os 8 fios pelo tubo do pescoço, de cima para baixo, e só então assente a cabeça, sem prender fio entre o garfo e o tubo. 3 × M3 × 45 por baixo da engrenagem, até os insertos do garfo. |
| 18 | tampa + pescoço + cabeça sobre a base; 4 M3 por baixo | por cima | Chave desligada. Nenhuma solda aqui, só bornes e encaixes: os 2 fios de 5,1 V nos bornes 1 e 2 da barra de emenda; o fio azul no borne 3; o conector do fio verde no pino S do D0 e o do preto no pino G do D0; o jumper do divisor no pino S do D1; a extensão do servo de tilt no D10. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos, que queimam o Raspberry Pi. Deixe 10 cm de folga para o giro. Com a cabeça olhando para a frente e o servo de pan em 90°, engrene os dentes. 4 × M3 × 10 por baixo, com a chave Allen longa. |
| 19 | porta traseira (1 M3) | por trás | 1 × M3 × 8 na orelha da tampa; o pé da porta encosta nos 2 batentes do piso. |
<!-- /GERADO -->

### Abrir sem desmontar a cabeça

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | abrir: porta traseira | Solte 1 parafuso. |
| 2 | abrir: bateria sai por trás | Desligue a chave antes. |
| 3 | abrir: tampa + pescoço + cabeça saem por cima (placas à mostra) | Solte os 4 parafusos por baixo da base e levante o conjunto inteiro, devagar: os fios do pescoço continuam ligados. |
<!-- /GERADO -->

## 5. Energia

Pack de 2 células 18650 em série (6 a 8,4 V) → fusível retardado de 3 A → placa de proteção (BMS 2S) → chave → duas
linhas: 5,1 V (conversor LM2596) para o Raspberry Pi e o Arduino; 6 V (UBEC de 3 A) para os 2 servos. O esquema e a
tabela fio a fio estão em [LIGACAO.md](LIGACAO.md).

| Decisão | Por quê |
|---|---|
| Conversor LM2596 para os 5 V, não o XL4015 | Quem decide é a tensão mínima de entrada. O XL4015 pede 8 V e o pack de 2 células passa quase toda a descarga abaixo disso. O LM2596 mantém os 5 V até o pack cair a cerca de 6,5 V. Limite: cerca de 2 A contínuos, o que pede o Pi 4 (ou o Pi 5 sem acessórios USB). |
| UBEC de 6 V e 3 A só para os servos | Os servos não derrubam os 5 V das placas quando partem. Há um capacitor de 1000 µF no borne. |
| Carregador USB-C com balanceamento e placa de proteção | O robô carrega com fonte de celular, sem abrir, por uma janela atrás da base. Células soltas não têm proteção: quem corta a descarga funda e o curto é a placa. O balanceamento pede um 3º fio no ponto que une as células. |
| Arduino alimentado pelos 5,1 V, e não pela bateria | A entrada VIN do Arduino Uno pede de 7 a 12 V e o pack passa boa parte da descarga abaixo de 7 V. |
| Fusível retardado de 3 A | A chave liga/desliga é de 3 A. O uso normal calculado é de cerca de 2 A. |

Os 4 módulos (conversor, UBEC, carregador e placa de proteção) ficam no piso da base, cada um num berço de 4
cantoneiras, presos por abraçadeira ou fita dupla-face.

## 6. Estabilidade

Centro de massa a 76 mm do chão. Margem de 69 mm na pose neutra e de 57,5 mm na pior das 10 poses. O mínimo exigido
pelo teste é 10 mm. O robô não roda: não há aceleração nem freada a considerar.

## 7. Preparado para a fase 2

### Câmera e sensores: por que aqui não há "olhos com sensor"

Nos bichos do projeto, a câmera e o sensor de distância ficam atrás das pupilas. Aqui os olhos são desenhados na tela
e não há pupila física. A câmera é uma só e fica atrás do painel escuro do rosto, num furo de 8 mm acima da tela: de
frente, é um ponto escuro num painel escuro. Um sensor de distância na cabeça não foi previsto, porque o robô fica
parado na mesa.

### Onde está cada furo

| O quê | Onde |
|---|---|
| Câmera | Atrás do painel escuro do rosto, furo de 8 mm acima da tela, em 4 postes |
| Microfones | 2 furos de 2 mm por baixo da cabeça |
| Alto-falante | Parede de trás da base, atrás de uma grade de fendas verticais; desliza em 2 trilhos |
| Sensor de movimento (IMU) | Par de furos M3 a 20 mm no piso da base |
| LiDAR | Topo da cabeça: 2 furos cegos por dentro; a pele de 0,8 mm só é furada quando o sensor for instalado |
| Carga USB-C e chave liga/desliga | Atrás da base |

De frente e de três quartos não aparece furo técnico nem parafuso.

### O que comprar na fase 2

<!-- GERADO:fase2 -->
| Item (o nome abre a busca) | Qtd | Onde fica | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (placa de 25 × 24 mm) com cabo flat](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Atrás do painel do rosto, no furo de 8 mm acima da tela. 4 postes com furo para parafuso M2. NC: furos e altura da lente. | R$ 180–350 | não conferido |
| [Parafuso M2 × 6 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Prende a câmera nos 4 postes. | R$ 3–8 | R$ 5,98 o kit com 10 |
| [Microfone I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Dentro da cabeça, sobre os 2 furos de 2 mm que ficam por baixo dela. NC: fixação do microfone ainda não modelada. | R$ 15–55 | R$ 54,26 |
| [Alto-falante de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Desliza nos 2 trilhos da parede de trás da base, contra a grade de fendas verticais. NC: diâmetro e profundidade. | R$ 7–20 | não conferido |
| [Amplificador de áudio pequeno (PAM8403 ou MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Sem lugar modelado ainda: vai solto na base, com fita dupla-face. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | No ponto universal do piso da base (par de furos M3 a 20 mm). | R$ 15–35 | R$ 34,09 |
| [LiDAR LD19 ou LD06](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | No topo da cabeça: 2 furos cegos por dentro; a pele de 0,8 mm só é furada quando o sensor for instalado. NC: padrão de furos do sensor. | R$ 400–900 | não conferido |
<!-- /GERADO -->

## 8. Semelhança com a referência

Medida pelo contorno do robô numa vista de três quartos, contra a imagem de referência (IoU: área comum dividida pela
área total das duas silhuetas, de 0 a 1).

| Vista | Antes (v1.0.2) | Depois |
|---|---|---|
| três quartos | 0,755 | 0,797 |

O alvo era ganhar 0,10 (chegar a 0,855) e **não foi atingido**. O motivo é mecânico: com o servo de pan em pé e a
engrenagem por cima dele, a base não fica mais baixa que cerca de 60 mm. Na referência, base e pescoço somam 20 % da
altura; aqui somam 41 %. A tabela completa e o método estão em [comparacao/semelhanca.md](../../comparacao/semelhanca.md).

## 9. Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py cubo`:

<!-- GERADO:verificacao -->
```
== verificação: cubo
  [PASSOU] 1 contagem: 12 peças distintas, 15 no total (esperado 15); faltando 0; sobrando 0
  [PASSOU] 2 malha: 12 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 158.0 mm (base)
  [PASSOU] 4 parede: modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm)
  [PASSOU] 5 interferência: 28 sólidos (14 impressos + 14 componentes), 10 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem)
  [PASSOU] 6 teste negativo: 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 14 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 1147 g; CG neutro em x=1.3 y=0.7 z=76.1 mm, margem 69.3 mm (tomba com 42°); pior pose 'pan+170+tilt-baixo': margem 57.5 mm (38°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 21 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 12 peças distintas: 12 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'tampa-base' na orientação declarada: 0 mm² sem apoio (limite 96); girada 180° em X → 21240 mm² = 44.0 % (acusou; tem que acusar)
```
<!-- /GERADO -->

## 10. Pendências

- Nada foi impresso, e a parte elétrica não foi testada na bancada.
- A semelhança com a referência ficou abaixo do alvo: a base é alta demais para o desenho.
- O cupom de teste é comum aos outros robôs: não testa a janela do servo MG996R nem o furo do pino M5. Falta um cupom próprio dos robôs quadrados.
- O plugue USB-C que alimenta o Raspberry Pi não está no modelo 3D: conferir se cabe ao lado do Pi, dentro da cabeça.
- Os pinos 31 a 34 do Raspberry Pi ficam embaixo da tela: conferir se o conector baixo da serial cabe.
- Calor: o Raspberry Pi fica fechado numa cabeça de PLA sem ventilação.
- Com o Arduino parafusado na base o cabo USB não entra: para regravar é preciso soltar os 4 parafusos dele.
- O rasgo do pescoço no fundo do copo da cabeça é fechado: os 8 fios só saem depois de o copo entrar. A passagem nunca foi ensaiada.
- Porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e microfones não têm fixação modelada.
- Medidas NC dos componentes (tela, abas e horn do MG996R, chave, boca do USB-C): medir e corrigir `comum/cad/parametros.py`.
- Os 3MF das mesas ainda não foram abertos num fatiador; tempo e filamento são estimativas por volume.
