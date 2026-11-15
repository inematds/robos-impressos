# Como imprimir a capivara

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impressora de referência: Bambu Lab A1 (mesa de 256 × 256 × 256 mm), bico de 0,4 mm, camada de 0,2 mm.

Sugestão de ajuste, ainda não testada com estas peças:

- Placa PEI texturizada para os dois materiais.
- No Bambu Studio, perfil Generic PLA para o PLA e Generic PETG para o PETG, com as temperaturas que o perfil traz.
- Valores usuais, para você conferir: PLA com bico a 220 °C e mesa a 55–65 °C; PETG com bico a 250–255 °C e mesa a 70–80 °C. O [guia de filamentos da Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) dá de 240 a 270 °C para o bico no PETG.

Página com as mesmas tabelas: https://inematds.github.io/robos-impressos/guia/capivara/#imprimir

## Os arquivos já estão na posição de impressão

- Cada STL de `projetos/capivara/stl/` está na posição em que deve ser impresso: a face de apoio em Z = 0. Abra no fatiador e
  imprima sem girar.
- Cada 3MF de `projetos/capivara/mesas/` traz as peças de uma cor já arrumadas numa mesa de 256 mm.
- Tudo de uma vez: [capivara-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/capivara-stl.zip)
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
| Crânio | Por dentro: teto do crânio e fundo dos copos dos olhos. Por baixo: céu da boca e curva de baixo das bochechas. | Não. Nada no rosto. |
| Corpo | Por dentro: teto das 2 patas, sobre os ressaltos das esferas; quinas de baixo do relevo dos braços (1,0 % da área). | Não. |
| Porta traseira | Cerca de 110 mm² na curva de baixo, por fora e por baixo. | Não: fica virado para o chão. |
| Mandíbula | Sob o alívio redondo de trás, por dentro. | Não. |
| Garfo do pescoço | 1,8 mm sob a base, em volta do anel do horn. Suporte normal. | Não: fica dentro da gola. |
| Berço do tilt | Pouco, sob a ponte entre as 2 paredes do servo. | Não: fica dentro da gola. |

O verificador do projeto mede a área sem apoio de cada peça e reprova a que foi declarada sem suporte e precisaria
dele. Ninguém tirou ainda o suporte de uma destas peças impressas: comece por uma peça pequena, como a mandíbula.

## 1. Imprima primeiro o cupom de teste

**Nada deste projeto foi impresso ainda.** O cupom de teste (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está na mesa 06. Teste nele:

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
(`.venv/bin/python comum/cad/gerar.py capivara`).

Três avisos:

- O cupom é comum aos outros robôs do projeto. Os 3 soquetes de pino dele não são usados neste robô.
- O encaixe do servo MG996R não está no cupom. Confira o servo no berço do tilt (mesa 03, a quarta da ordem abaixo),
  antes das impressões longas.
- O cupom sai em PLA, mas 13 dos 18 insertos ficam em peças de PETG (chassi, berço e garfo). Imprima um segundo cupom em PETG. Ele não está em nenhuma mesa nem nos totais: carregue o arquivo `comum-teste-encaixe.stl` à parte, com PETG, e conte cerca de 15 g e 38 minutos a mais.

## 2. Ordem sugerida das mesas

Primeiro as peças pequenas e o esqueleto; por último as impressões longas: a gola, o crânio e o corpo.

<!-- GERADO:mesas -->
| Ordem | Arquivo da mesa | Material e cor | Peças | Filamento (g) | Tempo (h) | Por que nesta ordem |
|---|---|---|---|---|---|---|
| 1 | [capivara-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-06-pla-cinza.3mf) | PLA cinza | Cupom de teste (teste-encaixe) | 15 | 0,6 | Comece por aqui. O cupom de teste mostra se os insertos, os parafusos M3, o micro servo e o eixo do motor entram com a folga certa na SUA impressora. Menos de 1 hora. |
| 2 | [capivara-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-01-petg-amarelo.3mf) | PETG amarelo | Bandeja do Raspberry Pi (bandeja-pi), Bandeja do Arduino (bandeja-uno) | 33 | 1,3 | As 2 bandejas: peças pequenas que já testam os furos do Raspberry Pi e do Arduino. |
| 3 | [capivara-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-02-petg-grafite.3mf) | PETG grafite | Mesa da cabeça (mesa-cabeca) | 36 | 1,4 | Mesa da cabeça: confira se o micro servo da boca entra na janela. |
| 4 | [capivara-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-03-petg-grafite.3mf) | PETG grafite | Chassi (chassi), Garfo do pescoço (garfo-pescoco), 2 × Capa da esfera (capa-esfera), Berço do tilt (berco-tilt) | 212 | 8,1 | O esqueleto em PETG: chassi, garfo, berço e as 2 capas das esferas. Garfo e berço pedem suporte. Confira no berço se o servo MG996R entra, antes das impressões longas. |
| 5 | [capivara-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-04-pla-branco.3mf) | PLA branco | Olho direito (olho), Olho esquerdo (olho-esq) | 34 | 1,5 | Os 2 olhos. |
| 6 | [capivara-mesa-09-pla-marrom.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-09-pla-marrom.3mf) | PLA marrom | Focinho (focinho), Rabo (rabo), Mão direita (mao-dir), Mão esquerda (mao-esq), Íris direita (iris), Íris esquerda (iris-esq), Orelha direita (orelha-dir), Orelha esquerda (orelha-esq) | 84 | 3,8 | As peças marrons: focinho, rabo, mãos, orelhas e íris. A face de colar vai na mesa. |
| 7 | [capivara-mesa-10-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-10-pla-preto.3mf) | PLA preto | 2 × Miolo do aro (miolo), Pupila direita (pupila), Pupila esquerda (pupila-esq) | 9 | 0,7 | Miolos dos aros e pupilas. |
| 8 | [capivara-mesa-05-pla-ciano.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-05-pla-ciano.3mf) | PLA ciano | 2 × Aro da anca (aro) | 4 | 0,3 | Os 2 aros das ancas. Filamento translúcido, se você quiser pôr luz atrás deles na fase 2. |
| 9 | [capivara-mesa-11-pla-verde-bandana.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-11-pla-verde-bandana.3mf) | PLA verde-bandana | Gola-bandana (gola), Ponta da bandana (avental) | 182 | 6,9 | Gola-bandana e a ponta da bandana. |
| 10 | [capivara-mesa-07-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-07-pla-laranja.3mf) | PLA laranja | Crânio (cranio) | 251 | 9,5 | Crânio: a peça mais longa da cabeça. Suporte em árvore por dentro e sob o céu da boca. Nenhum suporte no rosto. |
| 11 | [capivara-mesa-08-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-08-pla-laranja.3mf) | PLA laranja | Corpo (bacia) (corpo), Topete (topete), Porta traseira (porta), Mandíbula (mandibula) | 269 | 10,3 | Corpo, porta traseira, mandíbula e topete: a impressão mais longa. Deixe por último, com a impressora já ajustada. O corpo leva um pouco de suporte em árvore por dentro. |
| **Total** |  |  |  | **1129** | **44,4** |  |
<!-- /GERADO -->

## 3. Peça por peça

"Paredes" é o número de perímetros. A coluna "Suporte" diz se a peça pede suporte e onde. O nome entre parênteses é o
nome do arquivo.

<!-- GERADO:pecas -->
| Peça | Arquivo | Qtd | Material e cor | Tamanho na mesa (mm) | Como vai na mesa | Suporte | Paredes | Preenchimento | Filamento (g) | Tempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Rabo (rabo) | [capivara-rabo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-rabo.stl) | 1 | PLA marrom | 52,8 × 58,8 × 29,3 | base plana (face de colar) na mesa | não | 3 | 15 % | 21 | 0,9 |
| Mão direita (mao-dir) | [capivara-mao-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-dir.stl) | 1 | PLA marrom | 48,6 × 48,1 × 19,7 | base plana (face de colar) na mesa | não | 3 | 15 % | 11 | 0,5 |
| Mão esquerda (mao-esq) | [capivara-mao-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-esq.stl) | 1 | PLA marrom | 48,6 × 48,1 × 19,7 | base plana (face de colar) na mesa | não | 3 | 15 % | 11 | 0,5 |
| Ponta da bandana (avental) | [capivara-avental.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-avental.stl) | 1 | PLA verde-bandana | 68,9 × 38,4 × 12,1 | base plana (face de colar) na mesa | não | 3 | 15 % | 9 | 0,4 |
| Aro da anca (aro) | [capivara-aro.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-aro.stl) | 2 | PLA ciano | 40 × 40 × 3 | face plana na mesa | não | 3 | 15 % | 4 | 0,3 |
| Miolo do aro (miolo) | [capivara-miolo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-miolo.stl) | 2 | PLA preto | 28 × 28 × 2,4 | face plana na mesa | não | 3 | 15 % | 3 | 0,3 |
| Corpo (bacia) (corpo) | [capivara-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-corpo.stl) | 1 | PLA laranja | 197 × 179,9 × 119 | borda de baixo (z=5) na mesa, em pé como um vaso; boca (z=124) para cima | sim (pouco, árvore fina: teto de dentro das 2 patas, sobre os ressaltos das esferas; quinas de baixo do relevo dos braços; ponta de baixo dos 2 blocos de trás; ~1,0 % da área) | 4 | 15 % | 196 | 7,4 |
| Porta traseira (porta) | [capivara-porta.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-porta.stl) | 1 | PLA laranja | 76,1 × 36,7 × 119 | borda de baixo na mesa, em pé | sim (pouco: ~110 mm² na curva de baixo, por fora e por baixo; não aparece) | 4 | 15 % | 38 | 1,5 |
| Gola-bandana (gola) | [capivara-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-gola.stl) | 1 | PLA verde-bandana | 159,4 × 155,7 × 68,6 | base (z=124) na mesa; a esfera sobe até 45° e fica aberta em cima | não | 4 | 20 % | 173 | 6,5 |
| Crânio (cranio) | [capivara-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-cranio.stl) | 1 | PLA laranja | 181,2 × 187,1 × 134,7 | borda de baixo (z=152) na mesa, em pé | sim (árvore POR DENTRO: teto do crânio e fundo dos copos dos olhos; e por baixo, fora do rosto: céu da boca e curva de baixo das bochechas) | 3 | 15 % | 251 | 9,5 |
| Mandíbula (mandibula) | [capivara-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mandibula.stl) | 1 | PLA laranja | 130,4 × 30,8 × 44,3 | face de trás (plano de corte) na mesa, ponta do queixo para cima | sim (pouco: ~190 mm² no alívio esférico de trás, por dentro) | 4 | 20 % | 20 | 0,8 |
| Mesa da cabeça (mesa-cabeca) | [capivara-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mesa-cabeca.stl) | 1 | PETG grafite | 97,2 × 146,5 × 50,3 | de cabeça para baixo: face de cima na mesa | não | 4 | 30 % | 36 | 1,4 |
| Olho direito (olho) | [capivara-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho.stl) | 1 | PLA branco | 48 × 48 × 24 | face de trás (plana) na mesa | não | 3 | 15 % | 16 | 0,7 |
| Olho esquerdo (olho-esq) | [capivara-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho-esq.stl) | 1 | PLA branco | 48 × 48 × 24 | face de trás (plana) na mesa | não | 3 | 15 % | 18 | 0,8 |
| Íris direita (iris) | [capivara-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris.stl) | 1 | PLA marrom | 34 × 34 × 10,5 | face de trás na mesa | não | 3 | 15 % | 6 | 0,3 |
| Íris esquerda (iris-esq) | [capivara-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris-esq.stl) | 1 | PLA marrom | 34 × 34 × 10,5 | face de trás na mesa | não | 3 | 15 % | 6 | 0,3 |
| Pupila direita (pupila) | [capivara-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila.stl) | 1 | PLA preto | 22 × 22 × 8,7 | face de trás na mesa | não | 3 | 15 % | 3 | 0,2 |
| Pupila esquerda (pupila-esq) | [capivara-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila-esq.stl) | 1 | PLA preto | 22 × 22 × 8,9 | face de trás na mesa | não | 3 | 15 % | 3 | 0,2 |
| Focinho (focinho) | [capivara-focinho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-focinho.stl) | 1 | PLA marrom | 77,9 × 59,9 × 18,2 | base plana (face de colar) na mesa | não | 3 | 15 % | 25 | 1,0 |
| Orelha direita (orelha-dir) | [capivara-orelha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-dir.stl) | 1 | PLA marrom | 26,3 × 26,8 × 5,4 | base plana (face de colar) na mesa | não | 3 | 15 % | 2 | 0,2 |
| Orelha esquerda (orelha-esq) | [capivara-orelha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-esq.stl) | 1 | PLA marrom | 26,3 × 26,8 × 5,4 | base plana (face de colar) na mesa | não | 3 | 15 % | 2 | 0,1 |
| Topete (topete) | [capivara-topete.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-topete.stl) | 1 | PLA laranja | 43,1 × 51,4 × 24,4 | base plana na mesa | não | 3 | 15 % | 15 | 0,6 |
| Chassi (chassi) | [capivara-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-chassi.stl) | 1 | PETG grafite | 149 × 135,8 × 115 | piso na mesa (em pé) | não | 4 | 25 % | 174 | 6,4 |
| Capa da esfera (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 2 | PETG grafite | 29 × 29 × 5,6 | deitada | não | 3 | 15 % | 6 | 0,4 |
| Bandeja do Raspberry Pi (bandeja-pi) | [capivara-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-pi.stl) | 1 | PETG amarelo | 61,4 × 93 × 8 | placa na mesa, pilares para cima | não | 4 | 25 % | 17 | 0,7 |
| Bandeja do Arduino (bandeja-uno) | [capivara-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-uno.stl) | 1 | PETG amarelo | 61,4 × 77,5 × 8 | placa na mesa, pilares para cima | não | 4 | 25 % | 16 | 0,6 |
| Garfo do pescoço (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG grafite | 65 × 48 × 50,8 | base na mesa, montantes para cima | sim (1,8 mm sob a base, em volta do anel de centragem do horn; suporte normal, fora de vista) | 5 | 40 % | 17 | 0,7 |
| Berço do tilt (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG grafite | 38,5 × 23 × 77 | de cabeça para baixo: topo da coluna na mesa | sim (pouco, sob a ponte) | 5 | 40 % | 15 | 0,6 |
| Cupom de teste (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA cinza | 70 × 34 × 8 | deitada | não | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **32** |  |  |  |  |  |  | **1129** | **44,4** |
<!-- /GERADO -->

Filamento e tempo são estimativas por volume, sem fatiador. O fatiador vai dar o número de verdade.

## 4. Filamento por cor

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 33 | 1,3 |
| PETG grafite | 248 | 9,5 |
| PLA branco | 34 | 1,5 |
| PLA ciano | 4 | 0,3 |
| PLA cinza | 15 | 0,6 |
| PLA laranja | 520 | 19,8 |
| PLA marrom | 84 | 3,8 |
| PLA preto | 9 | 0,7 |
| PLA verde-bandana | 182 | 6,9 |
| **Total** | **1129** | **44,4** |
<!-- /GERADO -->

## Onde cada peça é reforçada

<!-- GERADO:reforcos -->
| Peça | Reforço | O que é |
|---|---|---|
| Rabo (rabo) | — | rabo; cola no assento plano da porta |
| Mão direita (mao-dir) | — | mão direita; cola |
| Mão esquerda (mao-esq) | — | mão esquerda; cola |
| Ponta da bandana (avental) | — | ponta da bandana no peito; cola no rebaixo de fundo plano |
| Aro da anca (aro) | — | aro das ancas (filamento translúcido para o LED da fase 2); cola |
| Miolo do aro (miolo) | — | disco escuro no centro do aro: janela do sensor de distância lateral (fase 2); cola |
| Corpo (bacia) (corpo) | 2 blocos maciços atrás (um por parafuso M3, da pele até o poste do chassi; a ponta de baixo de cada um nasce ~2 mm acima da mesa e entra no suporte declarado); barriga da frente e fundo de trás engrossados por baixo; 4 perímetros porque a bacia é aberta atrás (porta) | bacia inteira do corpo; desce por cima do chassi; 2 M3 por trás (embaixo) + presa em cima pela gola; na frente abraça os ressaltos das esferas |
| Porta traseira (porta) | 2 blocos maciços (um por parafuso M3, da mesa até o poste); assento plano do rabo com parede atrás | porta traseira: bateria e bandejas saem por aqui sem tirar a cabeça; 2 M3 por trás (embaixo); leva o rabo e o carregador USB-C |
| Gola-bandana (gola) | maciça entre a esfera e o rolo de fora (sem teto em balanço); 2 abas na base para os M3 das orelhas da torre | gola-bandana: esfera em que a cabeça gira; assenta na borda da bacia e a prende; 2 M3 por cima, nas orelhas da torre (por dentro, antes da cabeça) |
| Crânio (cranio) | 3 orelhas internas com inserto M3 para a mesa; copos dos olhos fechados por trás (só a janela do cabo) | 3 M3x12 por baixo, pela mesa (na bancada); 2 furos no alto dão acesso aos parafusos da coluna |
| Mandíbula (mandibula) | almofadas maciças nos 2 lados do eixo; 2 nervuras que abraçam o horn | sem parafuso por fora: o horn encaixa entre 2 nervuras (direita) e o pino da mesa entra no soquete cego (esquerda); abre e encaixa por pressão |
| Mesa da cabeça (mesa-cabeca) | placa de 4 mm; janela do servo da boca com cantos em chanfro (ponte de 19,6 mm); assento cônico do alto-falante | mesa da cabeça: 2 M3x10 na coluna do berço (por cima, pelos furos sob o topete); segura o servo da boca, o pino do eixo da mandíbula e o alto-falante |
| Olho direito (olho) | — | olho direito: bolso da câmera (Camera Module 3) aberto por trás; pressão ou cola no copo do crânio |
| Olho esquerdo (olho-esq) | — | olho esquerdo: bolso do sensor ToF aberto por trás |
| Íris direita (iris) | — | anel da íris: a placa da câmera encosta atrás dele (4 furos piloto M2) |
| Íris esquerda (iris-esq) | — |  |
| Pupila direita (pupila) | — | pupila escura VAZADA no centro (a lente da câmera olha pelo furo); pressão, sem cola (dá acesso à lente) |
| Pupila esquerda (pupila-esq) | — | pupila escura vazada (janela do ToF) |
| Focinho (focinho) | — | tampa marrom do focinho; cola |
| Orelha direita (orelha-dir) | — | orelha direita; cola |
| Orelha esquerda (orelha-esq) | — | orelha esquerda; cola |
| Topete (topete) | — | topete; encaixe por pressão (sem cola): tampa os 2 furos de acesso aos parafusos da mesa |
| Chassi (chassi) | mísulas e arco a 45° sob o deck do pan; travessa inteira do piso ao deck; postes de trás engrossados (10 mm de parede em volta dos insertos); orelhas da gola em mísula; trilhos com teto em chanfro | piso recortado da seção da pele + rack das bandejas (atrás) + torre e deck do servo de pan (frente) + ressaltos das 2 esferas |
| Capa da esfera (capa-esfera) | — | anel que segura a esfera de apoio; 2 M3x8 |
| Bandeja do Raspberry Pi (bandeja-pi) | placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack | bandeja deslizante do Raspberry Pi 4/5 (nível de baixo); sai por trás, pela porta; 4 M2,5x8 auto-atarraxantes |
| Bandeja do Arduino (bandeja-uno) | placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack | bandeja deslizante do Arduino Uno + shield (nível de cima); sai por trás, pela porta; 4 M3x8 Allen direto no plástico |
| Garfo do pescoço (garfo-pescoco) | camadas ao longo dos montantes NÃO: a carga do tilt flete os montantes no plano das camadas, por isso 5 perímetros e 40 % de miolo | gira com o servo de pan (horn redondo) e segura o eixo do tilt |
| Berço do tilt (berco-tilt) | coluna em D maciça (5 perímetros) e ponte de 4 mm entre as duas paredes do servo | segura o servo de tilt (MG996R em pé) e sobe pela abertura da gola até a mesa da cabeça; cabos pela face chata da coluna |
| Cupom de teste (teste-encaixe) | — | cupom de folgas: janela do servo, 3 furos de inserto (3,9/4,0/4,1), eixo do motor TT, M3 passante/M3 piloto/M2,5/M2, 3 soquetes do pino (0,20/0,25/0,30); covinha = medida do projeto |
<!-- /GERADO -->

Depois de imprimir: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) e [LIGACAO.md](LIGACAO.md).
