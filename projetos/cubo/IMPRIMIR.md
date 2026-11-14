# Como imprimir — robô quadrado de mesa (`cubo`)

Impressora de referência: Bambu Lab A1 (mesa de 256 × 256 × 256 mm), bico de 0,4 mm, camada de 0,2 mm.
As tabelas são geradas por `guia/src/pagina_robo.py docs cubo` a partir de `pecas/cubo/montagem.json` e `mesas.json`.

## Os arquivos já estão na posição de impressão

- Cada STL de `pecas/cubo/stl/` está deitado como deve ser impresso: a face de apoio em Z = 0. Abra no fatiador e
  imprima sem girar.
- Cada 3MF de `pecas/cubo/mesas/` traz as peças de uma cor já arrumadas numa mesa de 256 mm.
- Tudo de uma vez: [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip)
  (STL + 3MF das mesas + este arquivo).
- Como foi conferido (14/11/2026): em cada STL, a caixa da peça é igual ao tamanho "na mesa" do `montagem.json`, o
  ponto mais baixo está em Z = 0 e a área plana encostada na mesa é a mesma que o verificador mediu
  (teste 10: nenhuma peça precisa de suporte; teste 11: a tampa virada 180° é acusada).
- Os 3MF são genéricos: só geometria e posição, sem perfil nem cor. Foram relidos por script, mas ainda não foram
  abertos no Bambu Studio. Se algum não abrir, use os STL.

## 1. Imprima primeiro o `teste-encaixe`

**Nada deste projeto foi impresso ainda.** O cupom de teste (`pecas/comum/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está na mesa 06, com os 4 espaçadores do Raspberry Pi. Teste nele:

- o servo na janela;
- um inserto M3 em cada um dos 3 furos (3,9, 4,0 e 4,1 mm);
- os parafusos M3 (passante e direto no plástico), M2,5 e M2;
- os 3 soquetes do pino (folgas de 0,20, 0,25 e 0,30 mm).

A covinha marca a medida que o projeto usa. Se outra folga ficar melhor na sua impressora, mude o valor no bloco
`FOLGA` de `cad/parametros.py` e gere as peças de novo (`.venv/bin/python cad/gerar.py cubo`).

## 2. Ordem sugerida das mesas

Primeiro as peças pequenas que se encaixam umas nas outras; por último as duas impressões longas.

<!-- GERADO:mesas -->
| Ordem | Arquivo da mesa | Material e cor | Peças | Filamento (g) | Tempo (h) | Por que nesta ordem |
|---|---|---|---|---|---|---|
| 1 | [cubo-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-06-pla-cinza.3mf) | PLA cinza | teste-encaixe, 4 × espacador-pi | 15 | 1,0 | Comece por aqui. O cupom de teste mostra se o servo, os insertos e os parafusos entram com a folga certa na SUA impressora. Menos de 1 hora. |
| 2 | [cubo-mesa-04-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-04-petg-prata.3mf) | PETG prata | tubo-pescoco, engrenagem-pescoco | 23 | 1,0 | Tubo e engrenagem do pescoço: peças pequenas que já testam o encaixe com os tirantes. |
| 3 | [cubo-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-01-petg-amarelo.3mf) | PETG amarelo | quadro-cabeca, engrenagem-servo | 88 | 3,4 | Quadro da cabeça e engrenagem do servo: confira se o servo entra no rasgo e se as duas engrenagens rodam juntas sem prender. |
| 4 | [cubo-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-03-petg-grafite.3mf) | PETG grafite | tampa-base, porta-traseira, garfo | 129 | 5,0 | Tampa, porta e garfo. |
| 5 | [cubo-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-02-petg-grafite.3mf) | PETG grafite | base | 222 | 8,2 | Base: a impressão mais longa em PETG. |
| 6 | [cubo-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-07-pla-preto.3mf) | PLA preto | cabeca-face | 53 | 2,0 | Painel do rosto: a face que aparece vai na mesa, então limpe bem a mesa antes. |
| 7 | [cubo-mesa-05-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-05-pla-branco.3mf) | PLA branco | cabeca-corpo | 204 | 7,7 | Copo da cabeça: a impressão mais longa em PLA. Deixe por último, com a impressora já ajustada. |
<!-- /GERADO -->

## 3. Peça por peça

"Paredes" é o número de perímetros. Nenhuma peça precisa de suporte na posição em que o arquivo vem.

<!-- GERADO:pecas -->
| Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|
| [cubo-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-base.stl) | 1 | PETG grafite | 158 × 146 × 56,5 | piso na mesa | não | 4 | 20 % | 222 | 8,2 |
| [cubo-tampa-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tampa-base.stl) | 1 | PETG grafite | 158 × 146 × 18 | de cabeça para baixo: a face de cima na mesa | não | 4 | 25 % | 101 | 3,8 |
| [cubo-porta-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-porta-traseira.stl) | 1 | PETG grafite | 45,4 × 52,6 × 5 | face de fora na mesa | não | 3 | 20 % | 9 | 0,4 |
| [cubo-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tubo-pescoco.stl) | 1 | PETG prata | 40 × 40 × 32,6 | de cabeça para baixo: o topo (lado do garfo) na mesa, a flange cônica abre a 45° | não | 5 | 40 % | 16 | 0,7 |
| [cubo-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-pescoco.stl) | 1 | PETG prata | 36 × 36 × 8 | deitada | não | 5 | 60 % | 8 | 0,3 |
| [cubo-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-servo.stl) | 1 | PETG amarelo | 69 × 69 × 8 | de cabeça para baixo: a face de cima na mesa, o rebaixo do horn para cima | não | 5 | 60 % | 23 | 0,9 |
| [cubo-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-garfo.stl) | 1 | PETG grafite | 44 × 41,9 × 24 | deitado, costas na mesa: as camadas correm do bloco para os braços | não | 5 | 40 % | 19 | 0,8 |
| [cubo-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-quadro-cabeca.stl) | 1 | PETG amarelo | 129,2 × 74,6 × 63,7 | frente da travessa na mesa, laterais para cima | não | 4 | 30 % | 65 | 2,4 |
| [cubo-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-corpo.stl) | 1 | PLA branco | 136 × 118 × 102 | costas na mesa, boca (frente) para cima, como um copo | não | 3 | 15 % | 204 | 7,7 |
| [cubo-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-face.stl) | 1 | PLA preto | 129,9 × 111,9 × 34,2 | face da frente (a que aparece) na mesa, pilares para cima | não | 3 | 20 % | 53 | 2,0 |
| [cubo-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-espacador-pi.stl) | 4 | PLA cinza | 6 × 6 × 5 | em pé | não | 3 | 15 % | 0 | 0,3 |
| [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/comum/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** | **15** |  |  |  |  |  |  | **735** | **28,2** |
<!-- /GERADO -->

Filamento e tempo são estimativas por volume, sem fatiador. O fatiador vai dar o número de verdade.

## 4. Filamento por cor

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 88 | 3,4 |
| PETG grafite | 352 | 13,1 |
| PETG prata | 23 | 1,0 |
| PLA branco | 204 | 7,7 |
| PLA cinza | 15 | 1,0 |
| PLA preto | 53 | 2,0 |
| **Total** | **735** | **28,2** |
<!-- /GERADO -->

## Onde cada peça é reforçada

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| base | chanfro de 45° na aresta de baixo; postes da tampa Ø12 fundidos nos cantos; postes do servo com mãos-francesas; ressaltos nervurados do Uno; fendas verticais na grade | cuba: piso, paredes, postes do servo de pan, do Uno e da tampa, berços dos módulos de energia (abraçadeira), trilhos do alto-falante; chave, USB-C e grade atrás |
| tampa-base | 4 ressaltos de inserto com 3 nervuras a 45°; chanfro de 45° na aresta que encosta na mesa | presa por 4 M3x10 que entram POR BAIXO da base; a flange do pescoço gira sobre ela; orelha do parafuso da porta |
| porta-traseira | — | porta da bateria (atrás); 1 M3 na orelha da tampa, pé contra 2 batentes do piso |
| tubo-pescoco | 3 tirantes M3 de aço atravessam o tubo inteiro: as camadas trabalham só em compressão; flange cônica a 45° | pescoço oco (cabos por dentro); 3 M3x45 entram por baixo, pela engrenagem, e rosqueiam nos insertos do garfo |
| engrenagem-pescoco | dentes módulo 1.5 com 5 perímetros (dente quase maciço); presa pelos 3 tirantes | 22 dentes; fica por baixo da tampa e, com a flange do tubo por cima, impede o pescoço de bambear |
| engrenagem-servo | dentes módulo 1.5 com 5 perímetros; 4 parafusos no horn redondo | 44 dentes, presa no horn redondo do servo de pan (o pescoço gira 2x o servo) |
| garfo | camadas ao longo dos braços (flexão); bloco maciço com 3 insertos dos tirantes; furos em gota | garfo interno do tilt: fica dentro da cabeça, no topo do tubo; horn do servo num braço, pino M5 (rosca no plástico) no outro; furos de passagem da chave no braço esquerdo |
| quadro-cabeca | laterais inteiras até o fundo com colunas Ø10 nos 4 insertos e mãos-francesas a 45° na travessa; servo de tilt em rasgo em U (sem ponte), 4 parafusos | esqueleto da cabeça: Raspberry Pi (4 M2,5), servo de tilt, mancal do pino; recebe o painel (4 M3 por trás) e o copo (4 M3 pela parede de trás) |
| cabeca-corpo | arestas compridas com raio de 20 mm (verticais na impressão) e chanfro de 45° na aresta de trás; rasgo do pescoço em gota; sem ponte nem teto | casca da cabeça (5 lados); entra por trás, 4 M3 na parede de trás; rasgo do pescoço e furos de microfone por baixo |
| cabeca-face | 4 pilares Ø10 com 2 nervuras a 45° cada (insertos M3 na ponta); postes da câmera | painel escuro do rosto: janela da tela, furo de 8 mm da câmera acima dela; nenhum parafuso na frente |
| espacador-pi | — | 4 espaçadores de 5 mm do Raspberry Pi |
| teste-encaixe | — | cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto |
<!-- /GERADO -->
