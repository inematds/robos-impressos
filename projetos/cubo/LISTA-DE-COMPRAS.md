# Lista de compras do robô quadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Tudo o que você precisa comprar para montar o robô quadrado de mesa na fase 1: o corpo montado e ligado. O programa
vem depois, na fase 2.

Página com a mesma lista: https://inematds.github.io/robos-impressos/guia/cubo/#comprar

## Como ler a lista

- **Usa / comprar:** o primeiro número é o que o robô usa; o segundo é o que você compra, porque parafuso e inserto
  vêm em kit.
- **Os preços estão em reais (R$)** e os links abrem a busca do Mercado Livre do Brasil. O nome de cada item é o link.
- **Preço estimado** é uma faixa, não um orçamento. Serve para você saber a ordem de grandeza.
- **Visto em loja** é o preço lido em 14/11/2026 nas páginas públicas da usinainfo.com.br. Onde está
  "não conferido", a faixa é só referência. Os preços do Mercado Livre não foram lidos.
- **NC** = medida não confirmada. O modelo usa o valor mais comum daquele componente. Meça a sua peça com o
  paquímetro antes de imprimir a parte que encosta nela.

## Riscos antes de comprar

O que ainda não foi testado. Leia antes de gastar.

<!-- GERADO:riscos -->
- Nada foi impresso nem montado ainda. A parte elétrica desta página não foi testada na bancada: ela saiu das fichas dos componentes.
- Os arquivos 3MF das mesas nunca foram abertos no Bambu Studio. Se algum não abrir, use os STL.
- O plugue USB-C que alimenta o Raspberry Pi não está no modelo 3D. Pode não haver espaço para ele ao lado do Pi, dentro da cabeça.
- Os pinos 31 a 34 do Raspberry Pi ficam embaixo da placa da tela. A folga ali (17,5 mm no modelo) é uma medida não confirmada: se o conector baixo não couber, os 3 fios da serial terão de ser soldados.
- O cupom de teste não confere a janela do servo MG996R nem o furo do pino M5. Você confere os dois na mesa 01, antes das impressões longas.
- Com o Arduino parafusado na base, o cabo USB não entra: sobram cerca de 10 mm até a parede. Para regravar o programa é preciso soltar os 4 parafusos dele.
- O porta-fusível e os 3 resistores da serial não têm lugar modelado: ficam soltos nos fios, isolados com termo-retrátil.
- As medidas marcadas como NC vêm de anúncios de loja. Meça a sua peça antes de imprimir a parte que encosta nela.
<!-- /GERADO -->

## Quanto custa

<!-- GERADO:custo -->
- Peças compradas da fase 1 (sem ferramentas e sem filamento): **R$ 872–1840**.
- Se você já tem o Arduino Uno: **R$ 829–1750**.
- Filamento, pelo peso das peças: R$ 66–110 (735 g; R$ 90–150 o quilo).
<!-- /GERADO -->

## Fase 1: o que comprar

<!-- GERADO:compras -->
### Cérebro, tela e movimento

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | Cérebro do robô. Fica dentro da cabeça, atrás da tela. O Pi 5 também serve, mas o conversor de 3 A limita as portas USB dele a 0,6 A. | R$ 450–800 (cada) | não conferido |
| [Cartão microSD 32 GB classe 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema do Raspberry Pi. | R$ 25–50 (cada) | não conferido |
| [Tela TFT 3,5" 480 × 320 para Raspberry Pi (MPI3501, encaixa no GPIO)](https://lista.mercadolivre.com.br/display-lcd-tft-3.5-raspberry-pi-mpi3501) | 1 / 1 | O rosto do robô. Encaixa direto nos pinos 1 a 26 do Pi, sem parafuso. NC: espessura do conjunto (7 mm) e altura sobre o Pi (24,5 mm). | R$ 90–200 (cada) | R$ 193,57 |
| [Servo MG996R de 180° (posição, não o de rotação contínua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Um gira o pescoço (pan), o outro inclina a cabeça (tilt). O kit do servo precisa trazer o horn redondo (disco). NC: espessura e furos das abas, diâmetro e espessura do horn redondo. | R$ 30–75 (cada) | R$ 70,45 |
| [Extensão de servo de 30 cm (cabo extensor de 3 fios, macho-fêmea)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Leva o cabo do servo de tilt, que fica na cabeça, pelo pescoço até o shield, que fica na base, com folga para a cabeça girar. NC: comprimento do cabo de fábrica do servo (em geral 30 cm). | R$ 5–15 (cada) | não conferido |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (você talvez já tenha) | 1 / 1 | Comanda os 2 servos. Fica no piso da base, em 4 ressaltos. | R$ 43–90 (cada) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Encaixa em cima do Uno e dá os conectores de 3 pinos dos servos, com alimentação separada pelo borne azul. NC: nome impresso dos pinos de 5 V; confira com o multímetro. | R$ 11–35 (cada) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pacote de 10 | Divisor de tensão na serial: baixa os 5 V do Arduino para os 3,3 V que o Raspberry Pi aceita. | R$ 1–5 (pacote) | não conferido |
| [Barra de pinos fêmea de 2 fileiras, passo 2,54 mm (2 × 20)](https://lista.mercadolivre.com.br/barra-pinos-femea-2x20-2.54mm) | 1 pedaço de 2 × 2 / 1 barra | Conector baixo para os pinos 31 a 34 do Raspberry Pi, que ficam embaixo da tela. O fio Dupont comum não cabe em pé ali. NC: folga entre o Pi e a placa da tela (17,5 mm no modelo). | R$ 3–10 (cada) | não conferido |

### Energia

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Bateria 18650 de íon de lítio 3,7 V (célula solta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | Pack 2S: 7,4 V nominais (8,4 V cheio). Compre as duas iguais, novas e de marca conhecida. | R$ 13–45 (cada) | R$ 26,08 o kit com 2 |
| [Suporte para 2 baterias 18650 lado a lado, com fios](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Segura as 2 células em série. Desliza no berço da base e sai pela porta de trás. NC: o berço aceita até 78 × 41 × 22 mm. | R$ 5–15 (cada) | R$ 6,22 |
| [Porta-fusível de fio para fusível de vidro 5 × 20 mm, com fusível de 5 A](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (e 1 fusível de reserva) | No fio positivo, logo depois do suporte das baterias. Abre o circuito num curto, antes de o fio esquentar. Não tem lugar modelado: fica solto no fio. | R$ 4–12 (conjunto) | não conferido |
| [Placa de proteção BMS 2S 10 A (modelo 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Corta a descarga funda, a sobrecarga e o curto. Vai soldada nos fios da bateria, presa com fita dupla-face. NC: nome impresso das ilhas de solda (em geral B+, BM, B−, P+, P−). | R$ 8–20 (cada) | não conferido |
| [Carregador USB-C 2S/3S com balanceamento (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carrega o pack sem abrir o robô. Pede um 3º fio soldado no ponto do meio do suporte (entre as duas células). NC: tamanho da boca USB-C na janela de trás (9,2 × 3,4 mm) e nome impresso dos bornes. | R$ 15–30 (cada) | R$ 17,90 |
| [Conversor step-down LM2596 ajustável (placa azul, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Baixa a tensão do pack para os 5 V do Raspberry Pi e do Arduino. Ajuste para 5,1 V com o multímetro ANTES de ligar qualquer placa. O XL4015 não serve aqui: pede no mínimo 8 V. | R$ 8–20 (cada) | R$ 10,22 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S ou equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Alimenta os 2 servos em 6 V, separado do Pi. Ponha o jumper dele em 6 V. | R$ 25–60 (cada) | não conferido |
| [Capacitor eletrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | No borne de 6 V dos servos: segura o pico de corrente da partida. | R$ 1–4 (cada) | R$ 2,33 |
| [Chave gangorra KCD11 (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Liga e desliga. Encaixa por pressão na parede de trás, por fora. NC: espessura de painel que a trava aceita e corrente da chave (em geral 3 A). | R$ 3–8 (cada) | R$ 3,74 a R$ 5,40 (modelos KCD1; confira o recorte) |
| [Adaptador USB-C macho com bornes (2 pinos)](https://lista.mercadolivre.com.br/adaptador-usb-c-macho-borne) | 1 / 1 | Leva os 5 V do conversor até a entrada USB-C do Raspberry Pi (os pinos de 5 V do GPIO ficam embaixo da tela). O plugue não está no modelo 3D: confira se ele cabe ao lado do Pi, dentro da cabeça. | R$ 8–20 (cada) | R$ 13,11 |
| [Fio flexível 22 AWG (0,33 mm²): vermelho, preto e uma terceira cor](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | cerca de 1,5 m de vermelho, 1,5 m de preto e 30 cm de amarelo / 2 m de vermelho, 2 m de preto, 1 m de amarelo | Toda a parte de energia. O amarelo é o 3º fio, do ponto do meio do pack. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Jumpers Dupont de 20 cm (kits com 20: um fêmea-fêmea, um macho-fêmea)](https://lista.mercadolivre.com.br/jumper-dupont-20cm) | cerca de 8 fios / 2 kits de 20 | Sinais da serial e os 5 V do Arduino. Para descer pelo pescoço, emende dois jumpers ou use fio de 40 cm com um conector Dupont numa ponta. | R$ 6–12 (kit) | R$ 6,61 o kit |

### Fixação

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Inserto de latão M3 a quente (para furo de 4,0 mm, até 5,7 mm de comprimento)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 16 / 1 pacote de 20 ou mais | A rosca de metal das peças: 4 na tampa, 1 na orelha da porta, 4 nos pilares do painel do rosto, 4 nas colunas do quadro, 3 no garfo. | R$ 15–40 (pacote) | não conferido |
| [Parafuso M3 × 8 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 13 / 2 kits de 10 | 4 do Arduino, 4 do painel do rosto, 4 do copo da cabeça, 1 da porta. | R$ 3–8 (kit com 10) | R$ 6,14 o kit com 10 (tipo de cabeça não informado) |
| [Parafuso M3 × 10 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 4 / 1 kit de 10 | Tampa da base, por baixo. Tem de ser Allen de cabeça cilíndrica: a cabeça fica no fundo de um furo de 44 mm. | R$ 3–8 (kit com 10) | R$ 3,55 o kit com 10 (Phillips) |
| [Parafuso M3 × 12 mm](https://lista.mercadolivre.com.br/parafuso-m3x12) | 8 / 1 kit de 10 | 4 em cada servo MG996R, rosqueados direto no plástico (furo de 2,7 mm). | R$ 3–8 (kit com 10) | não conferido |
| [Parafuso M3 × 45 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x45) | 3 / 3 (vendido por unidade) | Tirantes do pescoço: entram por baixo da engrenagem, atravessam o tubo e rosqueiam nos insertos do garfo. | R$ 1–3 (cada) | não conferido |
| [Parafuso M5 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit de 10 (ou 1 avulso) | Pino do tilt: passa pela lateral do quadro e rosqueia no braço do garfo. A cabeça inclina em volta dele. | R$ 3–8 (kit com 10) | R$ 6,04 o kit com 10 (Phillips) |
| [Parafuso M2,5 × 12 mm com porca M2,5](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 parafusos e 4 porcas / 1 kit | Prende o Raspberry Pi no quadro, com os 4 espaçadores impressos no meio. | R$ 5–15 (kit) | não conferido |
| [Parafuso M2 × 8 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 em cada horn redondo: prende a engrenagem no servo de pan e o garfo no servo de tilt. NC: diâmetro dos furos do horn redondo. | R$ 3–8 (kit com 10) | R$ 3,31 o kit com 10 (confira se é auto-atarraxante) |
| [Abraçadeira de nylon de 3,6 mm de largura (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 pacote de 100 | Uma em cada berço: conversor de 5 V, UBEC e carregador. | R$ 8–20 (pacote) | não conferido |
| [Fita dupla-face de espuma](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | cerca de 5 cm / 1 rolo | Prende a placa de proteção (BMS) no bolso raso do piso. | R$ 8–20 (rolo) | não conferido |

### Ferramentas e material de solda (se você não tiver)

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Ferro de solda de 30 a 60 W, de preferência com ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solda os fios de energia e assenta os 16 insertos a quente. | R$ 40–150 (cada) | não conferido |
| [Ponta de ferro de solda para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guia o inserto reto no furo. A ponta cônica comum também serve: apoie a ponta dentro do inserto e empurre devagar. | R$ 15–40 (cada) | não conferido |
| [Estanho de solda com fluxo, 0,8 a 1 mm (tubo pequeno)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todas as emendas de fio e as ilhas da placa de proteção. | R$ 8–25 (tubo) | não conferido |
| [Tubo termo-retrátil de 2 a 3 mm e de 5 a 6 mm (ou fita isolante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | cerca de 30 cm de cada / 1 m de cada | Isola cada emenda de fio. Nenhum metal pode ficar à mostra perto da bateria. | R$ 5–20 (total) | não conferido |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta o conversor em 5,1 V, confere os 6 V do UBEC e a polaridade antes de ligar as placas. | R$ 40–100 (cada) | não conferido |
| [Chave de fenda de precisão de 2 mm](https://lista.mercadolivre.com.br/chave-de-fenda-precisao-2mm) | 1 / 1 | Gira o parafuso de ajuste do LM2596 e aperta os bornes. | R$ 5–20 (cada) | não conferido |
| [Chave Allen de 2,5 mm longa (haste de 50 mm ou mais)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Aperta os 4 parafusos da tampa pelo fundo dos furos da base e os 3 tirantes do pescoço. | R$ 8–25 (cada) | não conferido |
| [Paquímetro](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Confere as medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada) | não conferido |
| [Fonte USB-C de 15 W ou mais (5 V 3 A; a de celular serve) com cabo USB-C](https://lista.mercadolivre.com.br/carregador-usb-c-20w) | 1 / 1 | Carrega o pack pela boca USB-C de trás. O carregador aceita até 15 W. | R$ 25–80 (cada) | não conferido |
| [Cabo USB A-B (o de impressora) e um computador com a Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Grava o sketch no Arduino Uno, antes de parafusá-lo na base. | R$ 8–25 (cada) | não conferido |
<!-- /GERADO -->

Opcional: 4 pés de borracha adesivos por baixo da base. Não mudam nenhum encaixe.

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
| PETG amarelo | 88 | 3,3 |
| PETG grafite | 351 | 13,2 |
| PETG prata | 24 | 1,1 |
| PLA branco | 204 | 7,7 |
| PLA cinza | 15 | 0,9 |
| PLA preto | 53 | 2,0 |
| **Total** | **735** | **28,2** |
<!-- /GERADO -->

## Fase 2 (opcional agora)

Nada disto é necessário para imprimir, montar e ligar. As peças já têm o lugar, os furos e a passagem dos cabos.

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

## Glossário

<!-- GERADO:glossario -->
- **GPIO:** A fileira de 40 pinos do Raspberry Pi, onde se ligam a tela e os fios de sinal.
- **UBEC:** Conversor pequeno, usado em aeromodelos, que baixa a tensão da bateria para um valor fixo. Aqui, 6 V para os servos.
- **BMS:** Placa de proteção da bateria de lítio. Desliga a bateria antes de ela descarregar demais, carregar demais ou entrar em curto.
- **2S:** Duas células de lítio ligadas em série, uma depois da outra. As tensões somam: de 6 V (vazio) a 8,4 V (cheio).
- **Horn:** A peça de plástico que encaixa no eixo do servo e gira com ele. Este robô usa o horn redondo, em forma de disco.
- **Inserto a quente:** Bucha de latão com rosca por dentro. Entra no furo do plástico empurrada com o ferro de solda e vira uma rosca de metal.
- **NC:** Não confirmado: uma medida que veio de anúncio de loja e ainda não foi conferida com a peça na mão.
- **Fatiador:** O programa que transforma o arquivo 3D nas camadas que a impressora imprime. O da Bambu Lab se chama Bambu Studio.
<!-- /GERADO -->

Como ligar tudo o que está nesta lista: [LIGACAO.md](LIGACAO.md). Como imprimir: [IMPRIMIR.md](IMPRIMIR.md).
