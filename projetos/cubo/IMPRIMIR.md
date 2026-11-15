# Como imprimir o robô quadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impressora de referência: Bambu Lab A1 (mesa de 256 × 256 × 256 mm), bico de 0,4 mm, camada de 0,2 mm.

Sugestão de ajuste, ainda não testada com estas peças:

- Placa PEI texturizada para os dois materiais.
- No Bambu Studio, perfil Generic PLA para o PLA e Generic PETG para o PETG, com as temperaturas que o perfil traz.
- Valores usuais, para você conferir: PLA com bico a 220 °C e mesa a 55–65 °C; PETG com bico a 250–255 °C e mesa a 70–80 °C. O [guia de filamentos da Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) dá de 240 a 270 °C para o bico no PETG.

Página com as mesmas tabelas: https://inematds.github.io/robos-impressos/guia/cubo/#imprimir

## Os arquivos já estão na posição de impressão

- Cada STL de `projetos/cubo/stl/` está deitado como deve ser impresso: a face de apoio em Z = 0. Abra no fatiador e
  imprima sem girar.
- Cada 3MF de `projetos/cubo/mesas/` traz as peças de uma cor já arrumadas numa mesa de 256 mm.
- Tudo de uma vez: [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip)
  (os STL, os 3MF das mesas, o programa do Arduino e os guias).
- Como foi conferido (14/11/2026): em cada STL, a caixa da peça é igual ao tamanho "na mesa" da tabela abaixo, o
  ponto mais baixo está em Z = 0 e a área plana encostada na mesa é a mesma que o verificador do projeto mediu.
  Nenhuma peça precisa de suporte.
- Os 3MF são genéricos: só geometria e posição, sem perfil nem cor. Foram relidos por script, mas ainda não foram
  abertos no Bambu Studio. Se algum não abrir, use os STL.

## 1. Imprima primeiro o cupom de teste

**Nada deste projeto foi impresso ainda.** O cupom de teste (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está na mesa 06, com os 4 espaçadores do Raspberry Pi. No robô quadrado, teste nele:

- um inserto M3 em cada um dos 3 furos (3,9, 4,0 e 4,1 mm);
- um parafuso M3 no furo passante (3,4 mm) e outro no furo de rosquear direto no plástico (2,7 mm).

A covinha marca a medida que o projeto usa. Se outro furo ficar melhor na sua impressora, você não precisa refazer as
peças: no Bambu Studio, a opção X-Y hole compensation (compensação de furo X-Y; aba Qualidade, grupo Precisão, com o
modo avançado ligado) abre ou fecha todos os furos da peça: valor positivo abre, negativo fecha
([fonte: código do Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
A fonte não diz se o valor conta por lado ou no diâmetro: comece com 0,05 mm e imprima o cupom de novo. O cupom decide.

Quem mexe no código pode mudar o valor no bloco `FOLGA` de `comum/cad/parametros.py` e gerar as peças de novo
(`.venv/bin/python comum/cad/gerar.py cubo`).

Três avisos:

- O cupom é comum aos outros robôs do projeto. A janela de servo dele é do micro servo (SG90/MG90S) e os soquetes de
  pino e o furo do motor TT são dos outros robôs: o robô quadrado não usa nenhum dos três. Os furos M2,5 e M2 do cupom
  são de rosquear no plástico; no robô quadrado o Raspberry Pi usa furo passante com porca.
- O encaixe do servo MG996R e a rosca do parafuso M5 não estão no cupom. O servo você confere no quadro da cabeça
  (mesa 01, a terceira da ordem abaixo). A rosca do M5 fica no braço do garfo (mesa 03, a quarta). As duas saem antes
  das impressões longas.
- O cupom sai em PLA, mas 12 dos 16 insertos ficam em peças de PETG. Imprima um segundo cupom em PETG. Ele não está em nenhuma mesa nem nos totais: carregue o arquivo `comum-teste-encaixe.stl` à parte, com PETG, e conte cerca de 15 g e 38 minutos a mais.

## 2. Ordem sugerida das mesas

Primeiro as peças pequenas que se encaixam umas nas outras; por último as duas impressões longas.

<!-- GERADO:mesas -->
| Ordem | Arquivo da mesa | Material e cor | Peças | Filamento (g) | Tempo (h) | Por que nesta ordem |
|---|---|---|---|---|---|---|
| 1 | [cubo-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-06-pla-cinza.3mf) | PLA cinza | Cupom de teste (teste-encaixe), 4 × Espaçador do Raspberry Pi (espacador-pi) | 15 | 0,9 | Comece por aqui. O cupom de teste mostra se os insertos e os parafusos M3 entram com a folga certa na SUA impressora. Menos de 1 hora. |
| 2 | [cubo-mesa-04-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-04-petg-prata.3mf) | PETG prata | Tubo do pescoço (tubo-pescoco), Engrenagem do pescoço (engrenagem-pescoco) | 24 | 1,1 | Tubo e engrenagem do pescoço: peças pequenas que já testam o encaixe com os tirantes. |
| 3 | [cubo-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-01-petg-amarelo.3mf) | PETG amarelo | Quadro da cabeça (quadro-cabeca), Engrenagem do servo (engrenagem-servo) | 88 | 3,3 | Quadro da cabeça e engrenagem do servo: confira se o servo entra no rasgo e se as duas engrenagens rodam juntas sem prender. |
| 4 | [cubo-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-03-petg-grafite.3mf) | PETG grafite | Tampa da base (tampa-base), Porta traseira (porta-traseira), Garfo (garfo) | 129 | 5,0 | Tampa, porta e garfo. No garfo, confira se o parafuso M5 rosqueia no furo do braço; com o quadro da mesa anterior, veja se a cabeça inclina sem prender. |
| 5 | [cubo-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-02-petg-grafite.3mf) | PETG grafite | Base (base) | 222 | 8,2 | Base: a impressão mais longa em PETG. |
| 6 | [cubo-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-07-pla-preto.3mf) | PLA preto | Painel do rosto (cabeca-face) | 53 | 2,0 | Painel do rosto: a face que aparece vai na mesa, então limpe bem a mesa antes. |
| 7 | [cubo-mesa-05-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/mesas/cubo-mesa-05-pla-branco.3mf) | PLA branco | Copo da cabeça (cabeca-corpo) | 204 | 7,7 | Copo da cabeça: a impressão mais longa em PLA. Deixe por último, com a impressora já ajustada. |
| **Total** |  |  |  | **735** | **28,2** |  |
<!-- /GERADO -->

## 3. Peça por peça

"Paredes" é o número de perímetros. Nenhuma peça precisa de suporte na posição em que o arquivo vem. O nome entre
parênteses é o nome do arquivo.

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

Filamento e tempo são estimativas por volume, sem fatiador. O fatiador vai dar o número de verdade.

## 4. Filamento por cor

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 88 | 3,3 |
| PETG grafite | 351 | 13,2 |
| PETG prata | 24 | 1,1 |
| PLA branco | 204 | 7,7 |
| PLA cinza | 15 | 0,9 |
| PLA preto | 53 | 2,0 |
| **Total** | **735** | **28,2** |
<!-- /GERADO -->

## Onde cada peça é reforçada

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

Depois de imprimir: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) e [LIGACAO.md](LIGACAO.md).
