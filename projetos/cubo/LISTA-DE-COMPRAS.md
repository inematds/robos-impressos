# Lista de compras — robô quadrado de mesa (`cubo`)

Tudo o que você precisa comprar para montar o robô quadrado de mesa na fase 1 (mecânica e encaixe).
A lista sai dos componentes que o modelo usa (`cad/modelos/cubo.py`, `cad/comum/quadrado.py`) e das decisões de
energia da rodada 2. As tabelas abaixo são geradas por `guia/src/pagina_robo.py docs cubo` a partir de
`guia/src/robos/cubo.dados.json`: para mudar um item, mude lá.

Página com a mesma lista: https://inematds.github.io/robos-impressos/guia/cubo/#comprar

## Como ler os preços

- **Preço estimado** é uma faixa em reais, não um orçamento. Serve para você saber a ordem de grandeza.
- **Visto em loja** é o preço lido em 14/11/2026 nas páginas públicas da usinainfo.com.br. Onde está
  "não conferido", a faixa é só referência (a loja não tinha o item ou estava sem preço).
- **Onde procurar** abre a busca do Mercado Livre. Os preços do Mercado Livre não foram lidos: a página de busca
  não abre sem navegador.
- **NC** = medida não confirmada. O modelo usa o valor mais comum daquele componente. Meça a sua peça com o
  paquímetro antes de imprimir a parte que encosta nela e, se for diferente, corrija `cad/parametros.py`.

## Quanto custa

<!-- GERADO:custo -->
- Peças compradas da fase 1 (sem ferramentas e sem filamento): **R$ 857–1793**.
- Tirando o que já está marcado como "já tem" (R$ 43–90): **R$ 814–1703**.
- Filamento, pelo peso (735 g a R$ 90–150 o quilo): R$ 66–110.
<!-- /GERADO -->

O Arduino Uno entra na conta de quem ainda não tem. O Nei já tem o dele.

## Fase 1: o que comprar

<!-- GERADO:compras -->
### Cérebro, tela e movimento

| Item | Qtd | Para que serve | Preço estimado | Visto em loja | Onde procurar |
|---|---|---|---|---|---|
| Raspberry Pi 4 Model B, 4 GB | 1 | Cérebro do robô. Fica dentro da cabeça, atrás da tela. O Pi 5 também serve, mas o conversor de 3 A limita as portas USB dele a 0,6 A. | R$ 450–800 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) |
| Cartão microSD 32 GB classe 10 | 1 | Sistema do Raspberry Pi. | R$ 25–50 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) |
| Tela TFT 3,5" 480 × 320 para Raspberry Pi (MPI3501, encaixa no GPIO) | 1 | O rosto do robô. Encaixa direto nos pinos do Pi, sem parafuso. NC: espessura do conjunto (7 mm) e altura sobre o Pi (24,5 mm). | R$ 90–200 (cada) | R$ 193,57 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/display-lcd-tft-3.5-raspberry-pi-mpi3501) |
| Servo MG996R de 180° (posição, não o de rotação contínua) | 2 | Um gira o pescoço (pan), o outro inclina a cabeça (tilt). O kit do servo precisa trazer o horn redondo (disco). NC: espessura e furos das abas, diâmetro e espessura do horn redondo. | R$ 30–75 (cada) | R$ 70,45 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) |
| Arduino Uno R3 (você talvez já tenha) | 1 | Comanda os 2 servos. Fica no piso da base, em 4 ressaltos. | R$ 43–90 (cada) | R$ 43,28 a R$ 89,95 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/arduino-uno-r3) |
| Sensor Shield V5.0 para Arduino | 1 | Encaixa em cima do Uno e dá os conectores de 3 pinos dos servos, com alimentação separada. | R$ 11–35 (cada) | R$ 18,13 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) |

### Energia

| Item | Qtd | Para que serve | Preço estimado | Visto em loja | Onde procurar |
|---|---|---|---|---|---|
| Bateria 18650 de íon de lítio 3,7 V (célula solta) | 2 | Pack 2S: 7,4 V nominais (8,4 V cheio). Compre células de marca conhecida. | R$ 13–45 (cada) | R$ 26,08 o kit com 2 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/bateria-18650-3.7v) |
| Suporte para 2 baterias 18650 lado a lado, com fios | 1 | Segura as 2 células. Desliza no berço da base e sai pela porta de trás. NC: o berço aceita até 78 × 41 × 22 mm. | R$ 5–15 (cada) | R$ 6,22 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) |
| Placa de proteção BMS 2S 10 A (modelo 10A2S, ~24 × 11 mm) | 1 | Corta a descarga funda, a sobrecarga e o curto. Vai soldada nos fios da bateria, presa com fita dupla-face. | R$ 8–20 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/bms-2s-10a-18650) |
| Carregador USB-C 2S/3S com balanceamento (LX-USC-V2) | 1 | Carrega o pack com qualquer fonte USB-C de celular, sem abrir o robô. Pede um 3º fio soldado no ponto do meio do suporte (entre as duas células). NC: tamanho da boca USB-C na janela de trás (9,2 × 3,4 mm). | R$ 15–30 (cada) | R$ 17,90 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) |
| Conversor step-down LM2596 ajustável (placa azul, 3 A) | 1 | Baixa a tensão do pack para os 5 V do Raspberry Pi. Ajuste para 5,1 V com o multímetro ANTES de ligar o Pi. O XL4015 não serve aqui: pede no mínimo 8 V. | R$ 8–20 (cada) | R$ 10,22 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) |
| UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S ou equivalente) | 1 | Alimenta os 2 servos em 6 V, separado do Pi. | R$ 25–60 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) |
| Capacitor eletrolítico 1000 µF 16 V | 1 | No barramento de 6 V dos servos: segura o pico de corrente da partida. | R$ 1–4 (cada) | R$ 2,33 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) |
| Chave gangorra KCD11 (recorte de 13,5 × 9 mm) | 1 | Liga e desliga. Encaixa por pressão na parede de trás. NC: espessura de painel que a trava da chave aceita. | R$ 3–8 (cada) | R$ 3,74 a R$ 5,40 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) |
| Adaptador USB-C macho com bornes (2 pinos) | 1 | Leva os 5 V do conversor até a entrada USB-C do Raspberry Pi (os pinos do GPIO ficam ocupados pela tela). | R$ 8–20 (cada) | R$ 13,11 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/adaptador-usb-c-macho-borne) |
| Fio flexível 22 AWG, vermelho e preto (2 m de cada) | 1 | Ligações de energia e o 3º fio do balanceamento. | R$ 10–25 (total) | R$ 22,40 (5 m bicolor) | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) |
| Jumpers Dupont de 20 cm (kit com 20, fêmea-fêmea e macho-fêmea) | 2 kits | Sinais entre as placas. O cabo do servo de tilt desce pelo pescoço: use uma extensão de servo de 30 cm se o cabo dele não alcançar o shield. | R$ 6–12 (kit) | R$ 6,61 o kit | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/jumper-dupont-20cm) |

### Fixação

| Item | Qtd | Para que serve | Preço estimado | Visto em loja | Onde procurar |
|---|---|---|---|---|---|
| Inserto de latão M3 a quente (para furo de 4,0 mm, até 5,7 mm de comprimento) | 16 (compre 20) | A rosca de metal das peças: 4 na tampa, 1 na orelha da porta, 4 nos pilares do painel do rosto, 4 nas colunas do quadro, 3 no garfo. | R$ 15–40 (pacote) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) |
| Parafuso M3 × 8 mm, cabeça cilíndrica Allen | 13 | 4 do Arduino, 4 do painel do rosto, 4 do copo da cabeça, 1 da porta. | R$ 3–8 (kit com 10) | R$ 6,14 o kit com 10 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) |
| Parafuso M3 × 10 mm, cabeça cilíndrica Allen | 4 | Tampa da base, por baixo. Tem de ser Allen de cabeça cilíndrica: a cabeça fica no fundo de um furo de 44 mm. | R$ 3–8 (kit com 10) | R$ 3,55 o kit com 10 (Phillips) | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) |
| Parafuso M3 × 12 mm | 8 | 4 em cada servo MG996R, rosqueados direto no plástico (furo de 2,7 mm). | R$ 3–8 (kit com 10) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-m3x12) |
| Parafuso M3 × 45 mm, cabeça cilíndrica Allen | 3 | Tirantes do pescoço: entram por baixo da engrenagem, atravessam o tubo e rosqueiam nos insertos do garfo. | R$ 1–3 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-allen-m3x45) |
| Parafuso M5 × 16 mm | 1 | Pino do tilt: passa pela lateral do quadro e rosqueia no braço do garfo. A cabeça inclina em volta dele. | R$ 3–8 (kit com 10) | R$ 6,04 o kit com 10 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-m5x16) |
| Parafuso M2,5 × 12 mm com porca M2,5 | 4 + 4 | Prende o Raspberry Pi no quadro, com os 4 espaçadores impressos no meio. | R$ 5–15 (kit) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) |
| Parafuso M2 × 8 mm auto-atarraxante | 8 | 4 em cada horn redondo: prende a engrenagem no servo de pan e o garfo no servo de tilt. NC: diâmetro dos furos do horn redondo. | R$ 3–8 (kit com 10) | R$ 3,31 o kit com 10 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) |
| Abraçadeira de nylon de 3,6 mm de largura (150 a 200 mm) | 3 (pacote com 100) | Uma em cada berço: conversor de 5 V, UBEC e carregador. | R$ 8–20 (pacote) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) |
| Fita dupla-face de espuma | 1 rolo | Prende a placa de proteção (BMS) no bolso raso do piso. | R$ 8–20 (rolo) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) |

### Ferramentas (se você não tiver)

| Item | Qtd | Para que serve | Preço estimado | Visto em loja | Onde procurar |
|---|---|---|---|---|---|
| Chave Allen de 2,5 mm longa (haste de 50 mm ou mais) | 1 | Aperta os 4 parafusos da tampa pelo fundo dos furos da base e os 3 tirantes do pescoço. | R$ 8–25 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) |
| Ferro de solda | 1 | Assenta os 16 insertos a quente e solda os fios de energia. | R$ 40–120 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/ferro-de-solda-60w) |
| Multímetro | 1 | Ajusta o conversor em 5,1 V e confere a polaridade antes de ligar as placas. | R$ 40–100 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/multimetro-digital) |
| Paquímetro | 1 | Confere as medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada) | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) |
<!-- /GERADO -->

## Parafusos e insertos, contados

16 insertos M3 a quente: 4 na tampa da base, 1 na orelha da porta, 4 nos pilares do painel do rosto, 4 nas colunas do
quadro da cabeça e 3 no garfo.

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

Os parafusos do horn central e os anéis de borracha dos servos vêm no kit do MG996R.

## Filamento

Gramas por cor, somando as 15 peças (estimativa por volume, sem fatiador). A cor é sugestão; o material não:
mantenha PETG onde está PETG. Um rolo de 1 kg de PETG e um de PLA bastam se você não fizer questão das cores.

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

## Fase 2 (opcional agora)

Nada disto é necessário para imprimir e montar. As peças já têm o lugar, os furos e a passagem dos cabos.

<!-- GERADO:fase2 -->
| Item | Qtd | Onde fica | Preço estimado | Visto em loja | Onde procurar |
|---|---|---|---|---|---|
| Raspberry Pi Camera Module 3 (placa de 25 × 24 mm) com cabo flat | 1 | Atrás do painel do rosto, no furo de 8 mm acima da tela. 4 postes com furo para parafuso M2. NC: furos e altura da lente. | R$ 180–350 | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) |
| Parafuso M2 × 6 mm auto-atarraxante | 4 | Prende a câmera nos 4 postes. | R$ 3–8 | R$ 5,98 o kit com 10 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) |
| Microfone I2S INMP441 | 2 | Dentro da cabeça, sobre os 2 furos de 2 mm que ficam por baixo dela. NC: fixação do microfone ainda não modelada. | R$ 15–55 | R$ 54,26 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) |
| Alto-falante de 40 mm, 3 W | 1 | Desliza nos 2 trilhos da parede de trás da base, contra a grade de fendas verticais. NC: diâmetro e profundidade. | R$ 7–20 | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) |
| Amplificador de áudio pequeno (PAM8403 ou MAX98357A) | 1 | Sem lugar modelado ainda: vai solto na base, com fita dupla-face. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/amplificador-pam8403) |
| Sensor de movimento IMU MPU-6050 | 1 | No ponto universal do piso da base (par de furos M3 a 20 mm). | R$ 15–35 | R$ 34,09 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/mpu-6050-gy-521) |
| LiDAR LD19 ou LD06 | 1 | No topo da cabeça: 2 furos cegos por dentro; a pele de 0,8 mm só é furada quando o sensor for instalado. NC: padrão de furos do sensor. | R$ 400–900 | não conferido | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/lidar-ld19) |
| Conversor de nível lógico 3,3 V / 5 V | 1 | Na conversa serial entre o Raspberry Pi (3,3 V) e o Arduino (5 V), se você não usar o cabo USB. | R$ 5–12 | R$ 5,59 a R$ 8,55 | [buscar no Mercado Livre](https://lista.mercadolivre.com.br/conversor-nivel-logico-3.3v-5v) |
<!-- /GERADO -->

## O que mudou em relação à lista antiga (v1.0.2)

- Entraram: conversor LM2596 (5 V do Raspberry Pi), UBEC 6 V 3 A (servos), carregador USB-C com balanceamento,
  placa de proteção BMS 2S, capacitor de 1000 µF, abraçadeiras de 3,6 mm, parafuso M5 × 16 (pino do tilt),
  chave Allen de 2,5 mm longa.
- Mudaram: insertos de 14 para 16; tirantes do pescoço de M3 × 35 com porca para M3 × 45 em inserto.
- Saíram: conector de carga P4 (a carga agora é pelo USB-C do carregador) e os pés de borracha.
