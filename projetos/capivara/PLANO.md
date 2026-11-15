# Plano da capivara (`capivara`)

Robô de 30 cm que roda sobre 2 rodas, gira e inclina a cabeça e abre a boca. Este arquivo guarda as decisões do projeto deste robô e os porquês. Para fazer o robô, use os guias:
[LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md), [IMPRIMIR.md](IMPRIMIR.md) e [LIGACAO.md](LIGACAO.md). O resumo está no
[README.md](README.md); as decisões que valem para os 4 robôs, no [PLANO.md da raiz](../../PLANO.md).

Fase 1 = mecânica e encaixe: corpo impresso, montado e ligado. A fase 2 (programa, voz, câmera, sensores, IA) não está
feita; a seção 7 diz o que já tem lugar nas peças. **Nada foi impresso ainda.**

## 1. O que é e números

<!-- GERADO:numeros -->
- Altura montado: 300,0 mm.
- Peças impressas: 32 (29 arquivos diferentes), em 11 mesas.
- Filamento: 1129 g. Tempo de impressão: 44,4 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 18.
<!-- /GERADO -->
- Tamanho: 197 mm de largura × 274 mm do rabo ao focinho × 300 mm de altura. Maior peça: o corpo, com 197 mm.
- Massa: 1714 g montada (estimativa): 1129 g de peças impressas e cerca de 600 g de componentes.
- Movimentos: pan ±60°, tilt de −15° a +20°, boca de 0 a 18°. O verificador confere 8 poses. Não há braços móveis.

## 2. Decisões e porquês

| Decisão | Por quê | O que foi descartado |
|---|---|---|
| A forma vem de uma malha 3D da imagem de referência | A versão 1.0.2 era desenhada com formas simples e ficava longe do desenho. Uma malha gerada no computador a partir da imagem virou a pele do robô (`comum/cad/peles/capivara.npz`); a casca é essa pele com 2,4 mm de parede, cortada em peças. | Esculpir à mão com esferas e cilindros. |
| Esqueleto baixo próprio | A referência é uma pera com a cabeça encostada no corpo. A junta do pescoço desceu de 185 para 150 mm do chão e o servo de pan ficou deitado de lado. | Chassi comum com o dino, que obrigava a um pescoço comprido. |
| Duas esferas de apoio na frente, sob as patas | A cabeça é grande e fica à frente: o centro de massa cai 25 mm à frente do eixo das rodas. O apoio tem de ser na frente. | Uma esfera atrás, como no dino. |
| Rack atrás: Raspberry Pi embaixo, Arduino em cima | As 2 bandejas e a bateria saem por trás, pela porta, sem tirar a cabeça. | — |
| Casca em vasos: corpo inteiro, porta traseira e gola | Cada peça grande tem a base plana na mesa e paredes que sobem perto da vertical: imprime quase sem suporte. O corpo desce por cima do chassi. | Torso em duas metades, pernas e traseiro separados. |
| A gola é a faixa da bandana e prende o corpo em cima | A esfera em que a cabeça gira é a própria gola verde. Duas abas na base dela recebem 2 parafusos nas orelhas que sobem da torre. | — |
| Carregador USB-C dentro do rabo, de boca para baixo | Não aparece em nenhuma vista: o plugue entra por baixo do rabo, que fica 45 mm acima do chão. O rabo é uma peça separada, presa por 2 parafusos por dentro da porta. | Janela nas costas (aparece) ou por baixo do corpo (teria de deitar o robô para carregar). |
| A mandíbula encaixa sem furo no rosto | De um lado o braço do horn entra entre 2 nervuras; do outro, um pino da mesa entra num soquete cego. A mandíbula abre e encaixa por pressão. | Tampinhas sobre os parafusos: mais 2 peças e o rosto continuaria marcado. |
| Pan de ±60° e tilt de −15° a +20° mantidos; o laço da bandana ficou de fora | Com a cabeça inclinada para cima, a nuca passa exatamente pelo lugar do laço da referência. | Limitar o tilt a cerca de +5° para caber o laço. Fica como decisão em aberto. |
| Nenhum parafuso de frente nem no rosto | Corpo e porta: 4 parafusos por trás, embaixo. Capas das esferas: por baixo. Rabo e mesa da cabeça: por dentro. O topete encaixa por pressão e tampa os 2 furos de acesso. | — |

## 3. Peças impressas e imprimibilidade

A regra do projeto: imprimir sem suporte sempre que der. Face plana na mesa, balanços de até 45°, pontes de até 20 mm,
chanfro de 45° nas bordas viradas para baixo. Suporte só onde é inevitável, em árvore, fora do rosto e dos encaixes, e
declarado peça por peça. O verificador mede a área sem apoio de cada peça (teste 10) e reprova a peça declarada sem
suporte que precisaria dele.

Resultado: **23 das 29 peças saem sem suporte.** As 6 que pedem suporte:

| Peça | Área sem apoio | Onde |
|---|---|---|
| Crânio | 20 415 mm² (12,0 %) | teto de dentro e fundo dos copos dos olhos; por fora, só o céu da boca e a curva de baixo das bochechas |
| Corpo | 1 306 mm² (1,0 %) | teto de dentro das 2 patas, sobre os ressaltos das esferas, e quinas de baixo do relevo dos braços |
| Porta traseira | 111 mm² (0,5 %) | curva de baixo, por fora e por baixo |
| Mandíbula | 236 mm² (2,1 %) | alívio redondo de trás, por dentro |
| Garfo do pescoço | 1 488 mm² (16,1 %) | 1,8 mm sob a base, em volta do anel do horn |
| Berço do tilt | 516 mm² (7,0 %) | sob a ponte entre as 2 paredes do servo |

Na versão 1.0.2 eram 8 peças sem suporte, 12 com suporte e 13 que o teste reprovaria; só o crânio e os 2 torsos somavam 48 000 mm² sem apoio.

O que foi feito para chegar aí: cascas em vasos de corte horizontal, com a base plana na mesa (corpo, gola e crânio); gola maciça entre a esfera e o rolo de fora, aberta em cima a 45°; mandíbula em pé sobre o plano de corte de trás; peças coloridas em relevo, com base plana e borda chanfrada; chassi com trilhos de teto chanfrado, soquete das esferas em cone e reforço a 45° sob o deck; janela do servo da boca com cantos chanfrados; parafusos de trás em blocos maciços que nascem na mesa.

Parede medida da casca (mínimo exigido: 2,0 mm): corpo de 2,29 a 2,75 mm, cabeça de 2,27 a 2,73 mm, gola a partir de 3,38 mm (casca esférica).

Peças estruturais (chassi, bandejas, garfo, berço, mesa da cabeça) são de PETG, com 4 ou 5 perímetros. As tabelas
abaixo trazem, por peça, a orientação na mesa, o suporte, os perímetros, o preenchimento e o motivo de cada reforço.

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
| Bandeja do Arduino (bandeja-uno) | placa de 3 mm apoiada nos dois trilhos em todo o comprimento do rack | bandeja deslizante do Arduino Uno + shield (nível de cima); sai por trás, pela porta; 4 M3x8 auto-atarraxantes |
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
| Capas das 2 esferas de apoio (por baixo) | 4 | M3 × 8 | inserto no chassi |
| Corpo nos postes do chassi (por trás, embaixo) | 2 | M3 × 10 | inserto nos postes do chassi |
| Gola nas orelhas da torre (por cima) | 2 | M3 × 8 | inserto nas orelhas da torre |
| Porta traseira (por trás, embaixo) | 2 | M3 × 10 | inserto nos postes do chassi |
| Rabo na porta (por dentro da porta) | 2 | M3 × 10 | inserto no rabo |
| Arduino Uno na bandeja | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Raspberry Pi na bandeja | 4 | M2,5 × 8 auto-atarraxante | direto no plástico (furo de 2,2 mm) |
| Mesa da cabeça no crânio (por baixo) | 3 | M3 × 12 | inserto no crânio |
| Mesa da cabeça na coluna do berço (por cima) | 2 | M3 × 10 | inserto no topo do berço |
| Horn redondo dos 2 servos MG996R | 8 | M2 × 8 auto-atarraxante | nos furos do horn |
| Micro servo da boca | 2 | parafuso que vem com o servo | direto no plástico (furo de 1,7 mm) |
<!-- /GERADO -->

### Passo a passo

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | chassi | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, 3 servos em 90°, cabos do Raspberry Pi e divisor prontos, cartão gravado) e assente os 18 insertos a quente: 10 no chassi (4 nos ressaltos das esferas, 4 nos postes de trás e 2 nas orelhas da torre), 2 no rabo, 3 no crânio, 2 no topo do berço e 1 no garfo. |
| 2 | motor direito | pela direita | 2 × M3 × 30 com porca, pelos rasgos da parede. A ponta de dentro do eixo passa pelo furo da parede. Leve os 2 fios do motor pelo furo de 6 mm, à frente dele, até o lugar do driver. |
| 3 | motor esquerdo | pela esquerda | Igual ao direito. |
| 4 | step-down 5 V (parede esquerda da torre, abraçadeira) | pela esquerda | O conversor já vem soldado no chicote do preparo 1. 1 abraçadeira; fica em pé na parede esquerda da torre, com o parafuso de ajuste à mostra. |
| 5 | UBEC 6 V (parede direita da torre, abraçadeira) | pela direita | 1 abraçadeira, em pé na parede direita da torre. |
| 6 | BMS 2S (no piso, sob o lugar do L298N) | por cima | 1 abraçadeira. A placa de proteção já está soldada no chicote e fica deitada no piso. |
| 7 | chave (por baixo do piso) | por baixo | Já está no lugar desde o preparo 1: encaixada por baixo, com os 2 fios passando pelo recorte. |
| 8 | roda direita | pela direita | Encaixa por pressão no eixo do motor. Se a roda trouxer parafuso, aperte-o pelo centro. |
| 9 | roda esquerda | pela esquerda | Igual à direita. |
| 10 | esferas de apoio + capas | por baixo | Cada esfera entra no soquete por baixo e a capa prende com 2 × M3 × 8. As esferas têm de girar soltas. |
| 11 | driver L298N (pela frente da torre) | pela frente | Antes, tire do módulo os 3 jumpers: ENA, ENB e o do regulador de 5 V. 4 × M3 × 8 na travessa. Aperte nos bornes: os 2 fios de cada motor, o vermelho e o preto do chicote (alimentação dos motores e GND) e o fio de 5,1 V que vem do borne 1 da barra de emenda. Encaixe os 6 jumpers de sinal nos pinos ENA, IN1, IN2, IN3, IN4 e ENB e deixe as outras pontas soltas, marcadas com fita. |
| 12 | servo de pan | por cima | 4 × M3 × 12 com porca, eixo para cima. O servo já está em 90° (preparo 2): não gire o eixo com a mão. |
| 13 | corpo (bacia) desce por cima do chassi | por cima | Cole antes as 2 mãos e a ponta da bandana nos assentos planos (os aros e os miolos podem ficar para a fase 2, se você for pôr os sensores laterais). O corpo desce por cima do chassi e abraça os ressaltos das esferas. 2 × M3 × 10 por trás, embaixo, nos postes do chassi: a cabeça do parafuso fica rebaixada na casca, use a chave Allen longa. |
| 14 | garfo (por dentro da boca da bacia) | por cima | Prenda o horn redondo do servo de pan por baixo do garfo, com 4 × M2 × 8 pelos rasgos. Com o servo em 90°, encaixe o garfo no eixo com os montantes para os lados e aperte o parafuso central do servo pelo furo do meio. |
| 15 | berço + servo de tilt | por cima | Na bancada: servo de tilt em pé no berço, 4 × M3 × 12 com porca, e o horn redondo encaixado no eixo. Desça o berço entre os montantes do garfo até o horn assentar no rebaixo do montante direito (abra os montantes 1 mm com os dedos). Prenda o horn por FORA, com 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 9 mm. No montante esquerdo entra o M3 × 10, pelo inserto: a ponta dele é o pino do berço. Aperte até encostar e volte um quarto de volta, porque a cabeça inclina nele. Passe o cabo do servo pela face chata da coluna e pelo rasgo da base do garfo. |
| 16 | gola-bandana | por cima | A gola assenta na borda do corpo e é ela que o prende em cima. 2 × M3 × 8 por cima, pelas 2 abas da base, nos insertos das orelhas da torre. Passe por dentro dela o cabo do servo de tilt (e, na fase 2, o cabo flat da câmera). |
| 17 | bateria (entra por trás, pelo piso) | por trás | O suporte já está soldado no chicote desde o preparo 1, sem as células. Ele entra por trás, deslizando no piso; prenda com fita dupla-face. Com a chave desligada, ponha agora as 2 células, conferindo o lado do positivo com o multímetro. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 18 | bandeja do Pi | por trás | Na bancada: Raspberry Pi na bandeja com 4 × M2,5 × 8, blocos USB para trás, cartão microSD já gravado (preparo 4) e dissipadores colados. Encaixe os conectores ANTES de deslizar a bandeja: vermelhos nos pinos 2 e 4, pretos nos pinos 6 e 9, verde no 32, azul no 33 e preto da serial no 34. Dobre os fios logo acima dos conectores: sobre o Pi sobram cerca de 19 mm. É o trilho de baixo. |
| 19 | bandeja do Uno | por trás | Na bancada: Arduino Uno com o shield na bandeja, 4 × M3 × 8, USB para trás. Deslize a bandeja no trilho de cima e refaça no shield as ligações do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra no + e no − do conector COM, os 3 servos (D9, D10 e D11). Ligue os 6 sinais do driver (D5, D4, D7, D8, D12 e D6, só no pino S) e a serial: verde no S do D0, preto no G do D0 e o jumper do divisor no S do D1. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos. Faça essas ligações com a bandeja ainda para fora, apoiada na entrada do trilho, e só então empurre-a até o fim, acomodando os fios. Esta manobra nunca foi ensaiada com as peças impressas. |
| 20 | porta traseira (com o rabo e o carregador USB-C) | por trás | A porta já está presa ao chicote desde o preparo 1, pelos 3 fios do carregador que atravessam o furo dela. Na bancada: o carregador entra em pé no bolso do rabo, com a boca USB-C para baixo, e o rabo prende na porta com 2 × M3 × 10, por dentro. Depois a porta fecha por trás com 2 × M3 × 10, embaixo; acomode a folga dos fios para dentro do corpo. |
| 21 | mesa dentro do crânio (na bancada) | por baixo | Micro servo da boca na mesa, com os 2 parafusos do kit, já em 90°. A mesa entra por baixo, para dentro do crânio: 3 × M3 × 12 nos insertos. Mandíbula, com a boca fechada: o braço do horn entra entre as 2 nervuras (lado direito) e o pino da mesa entra no soquete cego (lado esquerdo), por pressão. Cole o focinho e as 2 orelhas. Olhos e íris: pressão ou cola. Pupilas: só pressão. O alto-falante é da fase 2. |
| 22 | cabeça no pescoço | por cima | Ligue a extensão de 30 cm no cabo do servo da boca e desça-a pela face chata da coluna, junto com o cabo do servo de tilt. A cabeça desce até a mesa assentar na coluna do berço: 2 × M3 × 10 por cima, pelos 2 furos do alto do crânio. O topete tampa os furos: encaixe por pressão, sem cola. |
<!-- /GERADO -->

### Abrir sem tirar a cabeça

Tirando 2 parafusos por trás, embaixo, a porta traseira sai com o rabo e o carregador. Por ali saem a bandeja do Arduino, a do Raspberry Pi e a bateria. Para tirar o corpo: cabeça, gola (2 parafusos por cima), garfo e berço, e os 2 parafusos de trás, embaixo.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | ABRIR: porta traseira sai | Solte os 2 parafusos de trás, embaixo, e puxe a porta. Ela sai com o rabo e o carregador e fica pendurada pelos 3 fios, que têm uns 15 cm de folga. A cabeça fica no lugar. |
| 2 | ABRIR: bandeja do Uno sai | Desencaixe os conectores do shield, marcando cada um com fita e o nome do pino, e solte do borne azul os fios do UBEC. Puxe a bandeja para trás. |
| 3 | ABRIR: bandeja do Pi sai | Desencaixe os conectores dos pinos do Raspberry Pi e puxe a bandeja para trás. |
| 4 | ABRIR: bateria sai | Desligue a chave antes. O suporte desliza no piso e sai por trás. |
<!-- /GERADO -->

## 5. Energia

Pack de 2 células 18650 em série (6 a 8,4 V) → fusível retardado de 3 A → placa de proteção (BMS 2S) → chave → três
linhas: 5,1 V (conversor LM2596) para o Raspberry Pi, o Arduino e a lógica do driver; 6 V (UBEC de 3 A) para os servos;
tensão da bateria para o driver L298N dos 2 motores. O esquema e a tabela fio a fio estão em [LIGACAO.md](LIGACAO.md).

| Decisão | Por quê |
|---|---|
| Conversor LM2596 para os 5 V, não o XL4015 | Quem decide é a tensão mínima de entrada. O XL4015 pede 8 V e o pack de 2 células passa quase toda a descarga abaixo disso. O LM2596 mantém os 5 V até o pack cair a cerca de 6,5 V. Limite: cerca de 2 A contínuos, o que pede o Pi 4 (ou o Pi 5 com 1 câmera e sem acessórios USB). |
| UBEC de 6 V e 3 A só para os servos | Os servos não derrubam os 5 V das placas quando partem. Servos: 2 MG996R (pan e tilt) e 1 micro servo (boca). Travados todos juntos pedem 3,5 A, mais do que o UBEC dá: o programa tem de parar antes do fim do curso, e há um capacitor de 1000 µF no borne. |
| Carregador USB-C com balanceamento e placa de proteção | O robô carrega com fonte de celular, sem abrir. Células soltas não têm proteção: quem corta a descarga funda e o curto é a placa. O balanceamento pede um 3º fio no ponto que une as células. |
| Driver L298N com os 3 jumpers retirados | A velocidade vem do Arduino (pinos D5 e D6). O regulador de 5 V do módulo não segura os 5 V abaixo de uns 7 V de bateria: a lógica dele recebe os 5,1 V do LM2596. |
| Raspberry Pi alimentado pelos pinos de 5 V | Na bandeja, a porta USB-C do Pi fica a cerca de 1 mm da parede do rack. |
| Fusível de 3 A | A chave liga/desliga é de 3 A. O uso normal calculado é de cerca de 2,5 A: fica perto do limite. É a pendência principal da parte elétrica. |

Onde fica cada módulo: LM2596 em pé na parede esquerda da torre; UBEC na parede direita; placa de proteção no piso, sob o driver; L298N na travessa; carregador USB-C em pé dentro do rabo, com a boca para baixo; chave por baixo do piso, atrás do motor direito.

## 6. Estabilidade

Centro de massa 25,1 mm à frente do eixo das rodas e 110 mm acima do chão. Apoios: as 2 rodas e as 2 esferas da frente, a 54 mm do eixo. Margem de 25,1 mm na pose neutra (tomba com 13° de inclinação) e 17,7 mm na pior pose, com a cabeça virada e para cima (9°). O mínimo exigido pelo teste é 10 mm. A conta é de corpo parado: aceleração e freada não entram.

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
| Distância nas laterais (ToF) | Miolo escuro dos 2 aros cianos das ancas (janela de 5 a 6 mm) |
| Microfones | As 2 narinas, na tampa marrom do focinho (furo de 2 mm; a placa redonda encaixa num bolso por trás) |
| Alto-falante | Em cima da mesa da cabeça, virado para baixo: o som sai pela fresta da boca e pelo vão do pescoço |
| Luz (opcional) | Atrás dos 2 aros cianos, se forem impressos em filamento translúcido |
| Carga USB-C | Dentro do rabo, com a boca para baixo: o plugue entra por baixo |
| Chave liga/desliga | Por baixo do piso, atrás do motor direito |
| Cabos da cabeça | Rasgo de 18 × 7 mm na mesa da cabeça, face chata da coluna do berço, boca da gola e rasgo do garfo |

De frente e de três quartos aparecem só as 2 narinas, o furinho das pupilas e o miolo dos aros. De lado, a roda aparece por um recorte de cerca de 10 mm embaixo de cada anca. Por trás aparecem 4 cabeças de parafuso rebaixadas, a costura da porta e o canal do plugue sob o rabo.

LiDAR: avaliado e deixado de fora. Num bicho, a cabeça tampa a volta inteira de que o sensor precisa.

### O que comprar na fase 2

<!-- GERADO:fase2 -->
| Item (o nome abre a busca) | Qtd | Onde fica | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide (placa de 25 × 24 mm)](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3-wide) | 1 | Atrás da pupila do olho direito: a placa entra por trás do olho e encosta na íris, em 4 furos para parafuso M2. A lente olha pelo furo de 8,5 mm da pupila. NC: furos da placa e altura da lente. | R$ 200–400 | não conferido |
| [Cabo flat de câmera de 50 cm (no Raspberry Pi 5, o cabo de 22 para 15 vias)](https://lista.mercadolivre.com.br/cabo-flat-camera-raspberry-pi-50cm) | 1 | Sai pela janela de trás do olho, desce pela face chata da coluna do pescoço e pelo rasgo do garfo, até o Raspberry Pi. Deixe uma barriga em S dentro da gola: a cabeça gira 60° para cada lado. NC: comprimento: os 50 cm são estimativa pelo modelo. | R$ 15–45 | não conferido |
| [Parafuso M2 × 6 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Prende a câmera nos 4 furos da íris direita. | R$ 3–8 | R$ 5,98 o kit com 10 |
| [Sensor de distância ToF VL53L1X (placa de cerca de 25 × 11 mm)](https://lista.mercadolivre.com.br/sensor-distancia-vl53l1x) | 3 | 1 atrás da pupila do olho esquerdo (janela de 6 mm): mede a distância do que a cabeça está olhando. 2 nas laterais, atrás do miolo escuro dos 2 aros cianos das ancas (janela de 5 a 6 mm). NC: tamanho da placa e lugar da janela: meça antes de imprimir o olho esquerdo. | R$ 30–110 | R$ 102,32 (VL53L1X, até 4 m); R$ 31,81 (VL53L0X, até 2 m) |
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
| frente | 0,783 | 0,944 | 0,943 |
| três quartos | 0,784 | 0,908 | 0,911 |
| lado | 0,736 | 0,906 | 0,925 |
| costas | 0,803 | 0,925 | 0,927 |
| **média** | **0,777** | **0,920** | **0,926** |

Alvo definido antes de medir o depois: 0,852. O robô ficou praticamente no teto da malha. O que ainda separa os dois: o laço da bandana na nuca e a faceta chata que ficou no lugar dele. A tabela completa e o método estão em
[comparacao/semelhanca.md](../../comparacao/semelhanca.md).

## 9. Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py capivara`:

<!-- GERADO:verificacao -->
```
== verificação: capivara
  [PASSOU] 1 contagem: 29 peças distintas, 32 no total (esperado 32); faltando 0; sobrando 0
  [PASSOU] 2 malha: 29 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 197.0 mm (corpo)
  [PASSOU] 4 parede: corpo 2.29–2.75 mm; gola 3.38–8.27 mm; cabeça 2.27–2.73 mm (mínimo exigido 2.0)
  [PASSOU] 5 interferência: 56 sólidos (31 impressos + 25 componentes), 8 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda)
  [PASSOU] 6 teste negativo: 'chassi' deslocada 3 mm em X → 13 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 31 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 1714 g; CG neutro em x=0.4 y=25.1 z=110.4 mm, margem 25.1 mm (tomba com 13°); pior pose 'pan+tilt-cima': margem 17.7 mm (9°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 26 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 29 peças distintas: 23 saem sem suporte; 6 com suporte declarado: cranio (20415 mm² = 12.0 %), garfo-pescoco (1488 mm² = 16.1 %, ponte de 21 mm), corpo (1306 mm² = 1.0 %, 4 ponto(s) no ar), berco-tilt (516 mm² = 7.0 %, ponte de 21 mm), mandibula (236 mm² = 2.1 %, ponte de 71 mm), porta (111 mm² = 0.5 %); 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'chassi' na orientação declarada: 84 mm² sem apoio (limite 166); girada 180° em X → 11522 mm² = 13.9 % (acusou; tem que acusar)
```
<!-- /GERADO -->

## 10. Pendências

- O laço da bandana na nuca não existe: a cabeça passa por ali quando inclina para cima. Decisão em aberto: limitar o tilt ou deixar sem laço.
- As patas da frente saem na cor do corpo (são parte da casca, com as esferas de apoio dentro). Na referência são marrons: pintar ou virar peça à parte.
- A porta traseira só tem os 2 parafusos de baixo; em cima ela só encosta na gola.
- Os 3 fios do carregador atravessam um furo de 7 mm da porta: a porta fica presa ao chicote. Um conector de 3 vias nesses fios resolveria; não está na lista nem no modelo.
- O crânio ainda pede suporte por dentro (o teto é largo; fechá-lo em ponta pesaria cerca de 570 cm³ de plástico).
- 4 pontos de apoio (2 rodas e 2 esferas): num piso irregular uma esfera pode ficar no ar.
- Os insertos ficam em blocos e postes maciços; o ressalto com nervuras do projeto (`ressalto_nervurado`) não foi usado aqui.
- O rabo tem insertos para 2 parafusos por dentro da porta, mas o texto da peça ainda fala em cola: vale o parafuso.
- Medidas NC: sensor ToF, microfone, câmera e horn do micro servo.
- A chave liga/desliga de 3 A é o ponto fraco da parte elétrica: uma chave maior pede mudar o recorte no chassi.
- Porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e sensor de movimento não têm lugar modelado.
- Nada foi impresso, e a parte elétrica não foi testada na bancada.
- Os 3MF das mesas ainda não foram abertos num fatiador; tempo e filamento são estimativas por volume.
