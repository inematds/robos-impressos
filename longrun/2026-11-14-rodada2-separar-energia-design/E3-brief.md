# Etapa E3 — dino e capivara: forma perto da referência, furos discretos, sensores nos olhos, energia

Você vai executar a ETAPA E3 de uma rodada longa no projeto `~/projetos/robos-impressos`. Trabalhe e escreva em português do Brasil.

ANTES DE QUALQUER COISA leia, nesta ordem, na pasta `~/projetos/robos-impressos/longrun/2026-11-14-rodada2-separar-energia-design/`:
`CONTEXTO.md` (arquitetura, comandos, armadilhas e regras: siga à risca), `goal.md`, `plan.md` e `canal.md` (o que as etapas
E1 e E2 deixaram: componentes de energia já modelados, como rodar a régua de semelhança `cad/comparar.py`, números "antes",
onde estão as malhas de image-to-3D e o veredito sobre elas). Depois leia o código: `cad/parametros.py`, `cad/comum/geo.py`,
`cad/comum/base.py`, `cad/comum/bicho.py`, `cad/modelos/dino.py`, `cad/modelos/capivara.py`, `cad/verificar.py`, e o `PLANO.md`.
Abra com Read as referências `referencia/dino-4-angulos.png` e `referencia/capivara-4-vistas.png` e as imagens lado a lado
do "antes" em `referencia/comparacao/`.

NÃO edite `cad/modelos/cubo.py` nem `cad/modelos/cubo_rodas.py` (etapa E1, já fechada). Em `cad/parametros.py`, não altere
as seções CUBO/CUBO_RODAS nem os componentes já existentes (pode acrescentar).

## O que o dono disse
"O resultado está longe das imagens originais, temos que chegar mais próximo." Principalmente a capivara, que saiu alta e de
pescoço comprido, parecendo um cachorro. A referência é uma PERA sentada, com a cabeça larga encostada no corpo, a bandana
escondendo a junta, o focinho grande e largo, os olhos grandes, as patas da frente apoiadas na barriga e as patas de trás
grossas na frente, anel ciano na lateral das coxas, rabo redondo atrás. O dino também precisa ficar mais perto: cabeça maior
e mais redonda, olhos menos "esbugalhados para fora", barriga e pernas mais grossas, pés com dedos creme, boca sorridente.

## Entrega 1 — forma
Caminho (a), se o veredito da E2 permitir: usar a malha de image-to-3D como CASCA externa. Escale para ~30–33 cm, oriente
(X lados, +Y frente, Z cima, chão em Z=0), transforme em campo de distância numa grade (crie em `cad/comum/geo.py` uma
classe com a MESMA interface da `Pele`: `.solido()`, `.deslocado()`, `.ponto_na_pele()`, `.f_pontos()`), separe em regiões
(torso, cabeça, pernas/coxas que cobrem as rodas, traseiro) e reaproveite o resto do pipeline de `bicho.py` (parede de
2,4 mm, costura frente/costas, gola esférica do pescoço, mandíbula, olhos, painéis, orelhas de parafuso).
Caminho (b), se a malha não servir (ou só servir de guia): esculpir melhor com os blobs/campos que já existem (ou Blender),
seguindo a silhueta das referências.
Em qualquer caminho o esqueleto tem que caber. Você PODE mudar o esqueleto para a forma ficar certa (ex.: baixar a junta do
pescoço para a cabeça da capivara encostar no corpo; rearranjar as bandejas num corpo em pera, que é largo embaixo; usar
parâmetros de base diferentes por bicho se um chassi único impedir a semelhança). Mantenha em comum o que der, e diga no
relatório o que deixou de ser comum. Requisitos que não mudam: rodar com 2 motores TT + rodas de 65 mm escondidas + esfera
de apoio; pescoço pan + tilt (MG996R) e boca; braços do dino; Pi 4/5 E Arduino Uno + shield cabendo juntos; bateria
2×18650 acessível; cada peça ≤ 256 mm; parede medida ≥ 2,0 mm; folga parametrizada; os 9 testes passando, inclusive o
caminho de montagem e de abertura (se conseguir abrir as costas sem tirar a cabeça, melhor: hoje não dá).
Altura alvo: ~30 cm (hoje 33). Proporção "chibi": cabeça ~40 % da altura.

## Entrega 2 — furos discretos (ordem do dono)
Nos renders de frente e de 3/4 nenhum furo técnico pode chamar atenção.
- microfones: nas narinas, nas orelhas, atrás da bandana (capivara) ou dos espinhos (dino);
- alto-falante: pela boca, por baixo ou por trás; se for na barriga, a grade tem a forma das faixas da barriga, sem fendas evidentes;
- sensores de distância: no lugar de detalhes que já existem (dedos/garras, manchas, o anel ciano da capivara);
- parafusos: só por baixo ou por trás, nunca na frente nem no rosto (hoje o painel da barriga tem 2 parafusos na frente e a
  mandíbula tem parafuso no rosto: resolva).

## Entrega 3 — sensores nos olhos (ordem do dono)
Avalie e escolha, justificando: (a) 2 câmeras, uma em cada pupila (estéreo / campo largo, ex.: 2× Camera Module 3 Wide;
Pi 5 tem 2 CSI, Pi 4 só 1); (b) câmera num olho e ToF no outro; (c) câmera grande-angular num olho e outro sensor escondido.
Modele a PUPILA como peça separada, escura (semitransparente ou vazada no centro), com o bolso da câmera/sensor atrás
(medidas com fonte) e a passagem do cabo flat pela cabeça até o pescoço (ele tem que aguentar pan e tilt). Tire o furo de
câmera do focinho/testa. Escreva a decisão e o porquê em `decisions.md` da pasta do longrun (a etapa de documentação vai
copiar para o PLANO e para a lista de compras de cada robô).

## Entrega 4 — auditoria de energia dos bichos
O L298N sozinho não resolve: o Pi 4/5 precisa de 5 V / 3 A e os servos de ~6 V. Use os componentes de energia que a E1 já
criou em `cad/parametros.py`/`cad/comum/componentes.py` (veja `canal.md`): step-down 5 V para o Pi, regulador/UBEC dos
servos (2 MG996R + micro servos: dimensione a corrente e diga o número), driver dos motores, bateria e carregador.
Modele o volume de cada um no chassi com fixação, como `Comp` com massa e passo em `ordem`, e prove no verificador.

## Régua
Rode `cad/comparar.py` (veja `canal.md`) no começo e a cada iteração de forma. Itere até a semelhança ficar clara a olho nas
4 vistas e o IoU subir de forma nítida em relação ao "antes". Registre os números finais ("depois") no arquivo de tabela
da régua e as imagens lado a lado em `referencia/comparacao/` (não públicas).

## Fechamento
- `cad/verificar.py todos` passando nos 4 modelos (os dois cubos não podem quebrar).
- Atualize `n_pecas`, `ordem`, `encaixes`; linhas em `FALHAS.md` para cada falha real corrigida; fatos para a etapa de
  documentação em `canal.md` (peças novas/renomeadas, o que deixou de ser comum, decisão dos olhos, onde ficou cada furo
  disfarçado, corrente e módulos de energia, altura final, limites de movimento conferidos).
- Não renderize as imagens finais nem mexa em docs/guia. Commit local (autor e rodapé do CONTEXTO.md). Sem push.

## Relatório final (curto)
Caminho usado (malha ou escultura) e por quê; IoU antes × depois por bicho e por vista; caminhos das imagens lado a lado;
o que mudou no esqueleto; decisão dos olhos; onde está cada furo disfarçado; módulos de energia e corrente; saída REAL do
verificador dos 4 modelos; hash do commit local; o que falhou ou ficou pendente, sem enfeite.

## Entrega 5 — imprimibilidade e reforços (ordem 9 do goal.md; leia o item inteiro)
Vale para TODAS as peças dos dois bichos e para as peças comuns (chassi, bandejas, garfo, berço, capa da esfera, mesa da
cabeça etc.): orientação de impressão pensada, sem suporte sempre que der (corte da casca escolhido para dar face plana na
mesa; se o corte gerar área sem apoio, mude a linha de corte antes de aceitar suporte), suporte só onde não aparece e
declarado por peça, e reforços (nervuras, ressaltos nervurados nos insertos, filetes, camadas ao longo da carga no garfo,
no berço e nas abas). O teste 10 do verificador (`cad/comum/imprimibilidade.py`, criado pela etapa E6; veja `canal.md`)
tem que passar nos dois bichos. Preencha por peça: suporte (sim/não, onde, tipo), perímetros, infill e motivo do reforço.

## COMO EXECUTAR (ordem obrigatória; vale mais do que a ordem das entregas acima)
Esta etapa é feita UM BICHO POR VEZ (o brief que você recebeu diz qual). Os dois bichos dividem `base.py`/`bicho.py`:
não quebre o outro (rode `cad/verificar.py <outro>` antes de cada commit; os testes 1–9 dele têm que continuar passando).
**Pacote 1 — esqueleto e forma.** PRIMEIRO passo, antes de mexer em casca: recorte a silhueta de lado e de frente da
referência, escale para ~300 mm de altura e SOBREPONHA ao esqueleto atual (chassi, deck em Z=137, centro do pescoço em
Z=185, servo de tilt em pé, mesa da cabeça) nas mesmas vistas. Salve a imagem em `.preview/`. Se o esqueleto não cabe
dentro da silhueta, nenhuma casca resolve: reprojete a pilha (baixar o deck, deitar o servo, mover o pan, alargar/baixar
o rack) até caber, e só então refaça a casca. A malha de image-to-3D, se a E2 a deu como utilizável, serve no máximo
para TORSO e CABEÇA; olhos, focinho, orelhas, bandana, mãos, patas, crista, unhas continuam peças paramétricas coloridas
sobre a pele nova. Feche com régua (IoU), verificador 1–9, commit e uma linha em `state.md`.
**Pacote 2 — furos discretos, olhos com sensor, energia.** Se a decisão dos olhos for 2 câmeras CSI, o cérebro vira
Pi 5: confira a alimentação dele (5 V / 5 A recomendados; com 3 A ele limita a corrente das USB) e o envelope contra o
módulo de 5 V escolhido pela E1, e registre em `decisions.md`. Feche com verificador, commit e linha em `state.md`.
**Pacote 3 — imprimibilidade e reforços.** Leia o "ACRÉSCIMO 2" do CONTEXTO.md (política do interior das cascas) e
`imprimibilidade-antes.md` (lista de trabalho). Use `ressalto_nervurado` de `geo.py`. Teste 10 passando sem afrouxar
limite. Feche com `verificar.py todos`, commit e linha em `state.md`.
**Regra de parada da forma (definida antes de ver o resultado):** alvo = IoU médio pelo menos na metade do caminho entre
o "antes" e o teto da malha crua (ou +0,10 se não houver malha); no máximo 6 iterações de forma; 3 seguidas sem ganho
≥ 0,01 → pare, registre os números e relate o que impede.

## Medidas tiradas das máscaras de referência pelo orquestrador (largura ÷ ALTURA total; use como alvo de proporção)
Largura da silhueta a 10/25/40/50/60/75/90 % da altura, contada de cima para baixo:
- **capivara frente:** 0,49 · 0,53 · 0,60 · 0,44 · 0,50 · 0,63 · 0,65 (largura total 0,68). **Lado:** 0,44 · 0,60 · 0,66 ·
  0,54 · 0,54 · 0,67 · 0,59 (total 0,84, com focinho e rabo). **Costas:** total 0,71.
  Leitura: o estrangulamento do pescoço fica a ~50 % da altura (a cabeça ocupa a METADE de cima e tem 0,60 H de largura);
  o corpo tem 0,65 H de largura na base. Para 300 mm: cabeça ~180 mm de largura × ~145 de altura, pescoço ~130 mm de
  largura em Z ≈ 150, corpo ~195 mm de largura, ~250 mm de profundidade total. O modelo v1.0.2 tem a junta em Z=185,
  326 mm de altura e corpo de ~150 mm: daí o "cachorro de pescoço comprido". A junta do pescoço precisa descer para
  Z ≈ 145–155 (deck perto de Z ≈ 100) e o corpo alargar; com corpo de 195 mm cabe um rack mais baixo e largo.
- **dino frente:** 0,34 · 0,44 · 0,34 · 0,34 · 0,44 · 0,47 · 0,61 (total 0,62). **Lado:** 0,48 · 0,60 · 0,49 · 0,36 · 0,47 ·
  0,67 · 0,50 (total 0,86, com cauda).
  Leitura: cabeça nos ~40 % de cima (largura 0,44 H de frente, 0,60 H de lado: focinho comprido), pescoço a 40–50 % da
  altura com 0,34 H, pés abertos com 0,61 H. Para 300 mm: cabeça ~132 × 180 mm (frente × lado), pescoço ~100 mm em
  Z ≈ 160–170, largura nos pés ~185 mm, profundidade total ~258 mm (a cauda pode precisar encurtar ou sair em peça à parte).
Cada peça continua limitada a 256 mm na orientação de impressão.
