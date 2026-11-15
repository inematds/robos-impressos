# Como imprimir o robô quadrado que roda

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impressora de referência: Bambu Lab A1 (mesa de 256 × 256 × 256 mm), bico de 0,4 mm, camada de 0,2 mm.

Sugestão de ajuste, ainda não testada com estas peças:

- Placa PEI texturizada para os dois materiais.
- No Bambu Studio, perfil Generic PLA para o PLA e Generic PETG para o PETG, com as temperaturas que o perfil traz.
- Valores usuais, para você conferir: PLA com bico a 220 °C e mesa a 55–65 °C; PETG com bico a 250–255 °C e mesa a 70–80 °C. O [guia de filamentos da Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) dá de 240 a 270 °C para o bico no PETG.

Página do robô: https://inematds.github.io/robos-impressos/guia/cubo-rodas/

## Os arquivos já estão na posição de impressão

- Cada STL de `projetos/cubo-rodas/stl/` está deitado como deve ser impresso: a face de apoio em Z = 0. Abra no fatiador e
  imprima sem girar.
- Cada 3MF de `projetos/cubo-rodas/mesas/` traz as peças de uma cor já arrumadas numa mesa de 256 mm.
- Tudo de uma vez: [cubo-rodas-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/cubo-rodas-stl.zip)
  (os STL, os 3MF das mesas, o programa do Arduino e os guias).
- Como foi conferido (14/11/2026): em cada um dos 15 STL, a caixa da peça é igual ao tamanho "na mesa" da tabela
  abaixo, o ponto mais baixo está em Z = 0 e há uma face plana encostada na mesa. Nenhuma peça precisa de suporte.
- Os 3MF são genéricos: só geometria e posição, sem perfil nem cor. Foram relidos por script, mas ainda não foram
  abertos no Bambu Studio. Se algum não abrir, use os STL.

## 1. Imprima primeiro o cupom de teste

**Nada deste projeto foi impresso ainda.** O cupom de teste (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está na mesa 07, com os 4 espaçadores do Raspberry Pi. Neste robô, teste nele:

- um inserto M3 em cada um dos 3 furos (3,9, 4,0 e 4,1 mm);
- um parafuso M3 no furo passante (3,4 mm) e outro no furo de rosquear direto no plástico (2,7 mm);
- um parafuso M2,5 no furo de rosquear direto no plástico: é assim que a tela é presa no painel do rosto.

A covinha marca a medida que o projeto usa. Se outro furo ficar melhor na sua impressora, você não precisa refazer as
peças: no Bambu Studio, a opção X-Y hole compensation (compensação de furo X-Y; aba Qualidade, grupo Precisão, com o
modo avançado ligado) abre ou fecha todos os furos da peça: valor positivo abre, negativo fecha
([fonte: código do Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
A fonte não diz se o valor conta por lado ou no diâmetro: comece com 0,05 mm e imprima o cupom de novo. O cupom decide.

Quem mexe no código pode mudar o valor no bloco `FOLGA` de `comum/cad/parametros.py` e gerar as peças de novo
(`.venv/bin/python comum/cad/gerar.py cubo_rodas`).

Quatro avisos:

- O cupom é comum aos outros robôs do projeto. A janela de servo dele é do micro servo (SG90/MG90S) e os soquetes de
  pino e o furo do motor TT são dos outros robôs: este robô não usa nenhum dos três. O Raspberry Pi, aqui, usa furo
  passante com porca.
- O encaixe do servo MG996R e a rosca do parafuso M5 não estão no cupom. O servo você confere no quadro da cabeça
  (mesa 01, a terceira da ordem abaixo). A rosca do M5 fica no braço do garfo (mesa 04, a quarta). As duas saem antes
  das impressões longas.
- O encaixe do motor também não está no cupom. A flange sai na mesa 04: com o motor na mão, confira os 6 furos em
  volta do eixo antes de imprimir a base, que é a impressão mais longa. Se os furos não baterem, corrija a medida e
  reimprima só a flange.
- O cupom sai em PLA, mas 27 dos 31 insertos ficam em peças de PETG. Imprima um segundo cupom em PETG. Ele não está em nenhuma mesa nem nos totais: carregue o arquivo `comum-teste-encaixe.stl` à parte, com PETG, e conte cerca de 15 g e 38 minutos a mais.

## 2. Ordem sugerida das mesas

Primeiro as peças pequenas que se encaixam umas nas outras; por último as impressões longas.

<!-- GERADO:mesas -->
| Ordem | Arquivo da mesa | Material e cor | Peças | Filamento (g) | Tempo (h) | Por que nesta ordem |
|---|---|---|---|---|---|---|
| 1 | [cubo_rodas-mesa-07-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-07-pla-cinza.3mf) | PLA cinza | Cupom de teste (teste-encaixe), 4 × Espaçador do Raspberry Pi (espacador-pi) | 16 | 0,9 | Comece por aqui. O cupom de teste mostra se os insertos e os parafusos M3 entram com a folga certa na SUA impressora. Menos de 1 hora, com os 4 espaçadores do Raspberry Pi. |
| 2 | [cubo_rodas-mesa-05-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-05-petg-prata.3mf) | PETG prata | Tubo do pescoço (tubo-pescoco), Engrenagem do pescoço (engrenagem-pescoco) | 25 | 1,1 | Tubo e engrenagem do pescoço: peças pequenas que já testam o encaixe com os tirantes. |
| 3 | [cubo_rodas-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-01-petg-amarelo.3mf) | PETG amarelo | Quadro da cabeça (quadro-cabeca), Engrenagem do servo (engrenagem-servo) | 108 | 4,1 | Quadro da cabeça e engrenagem do servo: confira se o servo entra no rasgo e se as duas engrenagens rodam juntas sem prender. |
| 4 | [cubo_rodas-mesa-04-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-04-petg-grafite.3mf) | PETG grafite | Deck (bandeja das placas) (deck), Alçapão da bateria (tampa-bateria), 2 × Flange do motor (flange-motor), Capa da bola (capa-esfera), Garfo (garfo) | 187 | 7,3 | Deck, alçapão, as 2 flanges, capa da bola e garfo. Confira já: os 6 furos da flange contra o motor, o parafuso M5 no braço do garfo e as placas nos ressaltos do deck. |
| 5 | [cubo_rodas-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-03-petg-grafite.3mf) | PETG grafite | Base com rodas (base-rodas) | 266 | 9,8 | Base com rodas: a impressão mais longa. Antes dela, confira com a flange da mesa anterior se o motor passa num furo de 40,6 mm. |
| 6 | [cubo_rodas-mesa-02-petg-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-02-petg-branco.3mf) | PETG branco | Tronco (tronco) | 236 | 8,7 | Tronco: imprime de cabeça para baixo, com o topo na mesa. |
| 7 | [cubo_rodas-mesa-08-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-08-pla-preto.3mf) | PLA preto | Painel do rosto (cabeca-face) | 57 | 2,2 | Painel do rosto: a face que aparece vai na mesa, então limpe bem a mesa antes. |
| 8 | [cubo_rodas-mesa-06-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-06-pla-branco.3mf) | PLA branco | Copo da cabeça (cabeca-corpo) | 248 | 9,3 | Copo da cabeça: a impressão mais longa em PLA. Deixe por último, com a impressora já ajustada. |
| **Total** |  |  |  | **1143** | **43,4** |  |
<!-- /GERADO -->

## 3. Peça por peça

"Paredes" é o número de perímetros. Nenhuma peça precisa de suporte na posição em que o arquivo vem. O nome entre
parênteses é o nome do arquivo.

<!-- GERADO:pecas -->
| Peça | Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base com rodas (base-rodas) | [cubo_rodas-base-rodas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-base-rodas.stl) | 1 | PETG grafite | 130 × 182 × 72 | piso na mesa | não | 5 | 25 % | 266 | 9,8 |
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
| Espaçador do Raspberry Pi (espacador-pi) | [cubo_rodas-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-espacador-pi.stl) | 4 | PLA cinza | 6 × 6 × 4 | em pé | não | 3 | 15 % | 1 | 0,3 |
| Cupom de teste (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **19** |  |  |  |  |  |  | **1143** | **43,4** |
<!-- /GERADO -->

Filamento e tempo são estimativas por volume, sem fatiador. O fatiador vai dar o número de verdade.

## 4. Filamento por cor

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 108 | 4,1 |
| PETG branco | 236 | 8,7 |
| PETG grafite | 453 | 17,1 |
| PETG prata | 25 | 1,1 |
| PLA branco | 248 | 9,3 |
| PLA cinza | 16 | 0,9 |
| PLA preto | 57 | 2,2 |
| **Total** | **1143** | **43,4** |
<!-- /GERADO -->

## Onde cada peça é reforçada

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| Base com rodas (base-rodas) | paredes dos motores com reforço de 4 mm e furo em gota; 4 postes Ø12 nos cantos; ressaltos nervurados do alçapão e da capa; assento cônico da bola a 45°; chanfro de 45° embaixo | cuba da base móvel: motores entram pela lateral (flange atrás da roda), bateria num alçapão por baixo, carregador USB-C e chave atrás, janela do sensor de queda e entalhes dos ToF |
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

Depois de imprimir: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) e [LIGACAO.md](LIGACAO.md).
