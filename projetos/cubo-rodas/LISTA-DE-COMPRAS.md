# Lista de compras do robô quadrado que roda

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Tudo o que você precisa comprar para montar o robô quadrado que roda na fase 1: o corpo montado e ligado. O programa
vem depois, na fase 2.

Página do robô: https://inematds.github.io/robos-impressos/guia/cubo-rodas/

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
- A chave de 3 A é o ponto mais fraco da parte elétrica. Pela conta das fichas, o robô puxa cerca de 2 A em uso normal e cerca de 6,5 A no pior caso (as 2 rodas travadas, os 2 servos forçando e o Raspberry Pi no máximo). O fusível de 3 A protege a chave, mas pode abrir se o robô forçar contra um obstáculo. Trocar por uma chave maior exige mudar o recorte de 13,5 × 9 mm na base.
- Os 2 cabos da tela, HDMI e USB, não estão no modelo 3D. Pelo modelo sobram cerca de 22 mm abaixo do Raspberry Pi e cerca de 30 mm ao lado das portas USB dele: os cabos retos que vêm com a tela não cabem. É o principal risco de encaixe deste robô. Confira com as peças na mão antes de fechar a cabeça.
- O carregador vem pronto para 2 células. Passá-lo para 3 exige tirar um resistor minúsculo e fechar um jumper de solda. Se não der certo, as 3 células saem pelo alçapão e carregam num carregador de 18650 comum.
- Os nomes impressos nas ilhas da placa de proteção de 3 células e nas 2 ilhas do meio do carregador não foram lidos. Confira cada emenda com o multímetro (cerca de 4 V e cerca de 8 V) antes de soldar.
- A posição dos 6 furos do motor em volta do eixo é uma medida não confirmada. Se não bater, a peça a reimprimir é a flange, um disco pequeno. Confira com o motor na mão antes de imprimir a base.
- O Raspberry Pi recebe os 5,1 V pelos pinos 2 e 4, sem passar pela proteção da entrada USB-C. Tensão errada ou fio invertido ali queima o Pi. Meça na barra de emenda antes de encaixar.
- O cupom de teste não confere a janela do servo MG996R nem a rosca do parafuso M5. A janela do servo você confere no quadro da cabeça (mesa 01). A rosca do M5 fica no braço do garfo (mesa 04). As duas saem antes das impressões longas.
- Para regravar o Arduino depois do robô montado é preciso soltar os 4 parafusos de baixo e levantar o tronco com o pescoço e a cabeça.
- O porta-fusível, a barra de emenda e os 3 resistores da serial não têm lugar modelado: ficam soltos, isolados com termo-retrátil. O cabo de cada motor tem cerca de 14 cm e pode não chegar ao driver: se faltar, emende.
- Os conectores A0 e A1 do Sensor Shield, usados pelo segundo fio de cada encoder, não aparecem com clareza na foto da loja. Se a sua placa não tiver esses pinos, deixe os 2 fios verdes isolados: o programa da fase 2 pode contar as voltas só com o fio amarelo.
- As medidas marcadas como NC vêm de anúncios de loja. Meça a sua peça antes de imprimir a parte que encosta nela.
- A passagem dos 8 fios pelo furo do garfo e pelo rasgo do fundo da cabeça nunca foi ensaiada com as peças impressas.
- Equilíbrio: o verificador mostra que o robô não tomba parado, com a cabeça em qualquer posição. Andando, a conta é uma estimativa: ele aguenta frear até cerca de 3 m/s² sem tombar para a frente, e o programa da fase 2 deve usar no máximo a metade disso. O degrau mais alto que ele passa tem cerca de 8 mm.
- Calor: o Raspberry Pi 4 fica fechado na cabeça, que é de PLA e não tem abertura de ventilação. O PLA amolece perto de 60 °C e o Pi reduz a velocidade a partir de 80 °C. Cole os dissipadores e meça com o comando `vcgencmd measure_temp`. Se passar de 70 °C, imprima o copo da cabeça em PETG ou abra furos de ventilação atrás.
<!-- /GERADO -->

## Quanto custa

<!-- GERADO:custo -->
- Peças da fase 1 (sem filamento e sem ferramentas): **R$ 1353–2944**.
- Do zero (peças, 2 rolos de filamento e todas as ferramentas): **R$ 1737–3909**.
- Só os 2 rolos de filamento (1 de PETG e 1 de PLA): R$ 170–290.
- Se você já tem o Arduino Uno, desconte: R$ 43–90.
- Se você já tem todas as ferramentas, desconte: R$ 214–675.
<!-- /GERADO -->

Os itens mais caros são o Raspberry Pi, a tela de 5 polegadas e os 2 motores com encoder. Nenhum dos três teve o
preço conferido em loja: as faixas deles são só referência.

## Fase 1: o que comprar

<!-- GERADO:compras -->
### Cérebro, tela e servos

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | Cérebro do robô. Fica dentro da cabeça, atrás da tela. O Pi 5 também serve. | R$ 450–800 (cada) | não conferido |
| [Cartão microSD 32 GB classe 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema do Raspberry Pi. | R$ 25–50 (cada) | não conferido |
| [Tela de 5" HDMI, 800 × 480 (Waveshare 5inch HDMI LCD (B), placa de 121 × 89,5 mm)](https://lista.mercadolivre.com.br/display-5-polegadas-hdmi-800x480-raspberry-pi-waveshare) | 1 / 1 | O rosto do robô. Ela não espeta nos pinos do Raspberry Pi: é presa por 4 parafusos nos pilares do painel do rosto e liga no Pi por um cabo HDMI e um cabo USB. Os pilares foram feitos para a placa de 121 × 89,5 mm, com 4 furos a 115 × 84 mm. NC: espessura do conjunto (14 mm no modelo), diâmetro dos 4 furos e posição das entradas HDMI e USB na placa. | R$ 250–480 (cada) | não conferido |
| [Cabo HDMI flat curto (10 a 20 cm): micro-HDMI em ângulo de um lado, HDMI padrão do outro](https://lista.mercadolivre.com.br/cabo-hdmi-flat-fpv-micro-hdmi-angulo-20cm) | 1 / 1 | Liga a tela ao Raspberry Pi 4, que tem saída micro-HDMI. O cabo que vem com a tela é reto e comprido: pelo modelo sobram cerca de 22 mm abaixo do Pi, e ele não cabe. NC: os cabos da tela não estão no modelo 3D: confira o espaço com as peças na mão antes de fechar a cabeça. | R$ 25–70 (cada) | não conferido |
| [Cabo USB curto (15 a 20 cm): USB-A em ângulo de um lado, micro-USB do outro](https://lista.mercadolivre.com.br/cabo-usb-a-angulo-90-micro-usb-20cm) | 1 / 1 | Leva energia do Raspberry Pi para a tela. Pelo modelo sobram cerca de 30 mm entre as portas USB do Pi e a parede da cabeça: o plugue reto comum não cabe. NC: tipo da entrada USB da tela (micro-USB no kit do fabricante); os cabos não estão no modelo 3D. | R$ 10–30 (cada) | não conferido |
| [Servo MG996R de 180° (posição, não o de rotação contínua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Um gira o pescoço (pan), o outro inclina a cabeça (tilt). O kit do servo precisa trazer o horn redondo (disco). NC: espessura e furos das abas, diâmetro e espessura do horn redondo. | R$ 30–75 (cada) | R$ 70,45 |
| [Extensão de servo de 30 cm (cabo extensor de 3 fios, macho-fêmea)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Leva o cabo do servo de tilt, que fica na cabeça, pelo pescoço até o shield, que fica no deck, com folga para a cabeça girar. NC: comprimento do cabo de fábrica do servo (em geral 30 cm). | R$ 5–15 (cada) | não conferido |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (você talvez já tenha) | 1 / 1 | Comanda os 2 servos e os 2 motores e lê os encoders. Fica no deck, em 4 ressaltos. | R$ 43–90 (cada) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Encaixa em cima do Uno e dá os conectores de 3 pinos dos servos, do driver e dos encoders, com alimentação separada pelo borne azul. O Arduino recebe os 5,1 V pelo pino + do conector COM do shield. NC: pela foto da loja, o conector COM tem 4 pinos em pé, marcados TX, RX, − e +, e os conectores digitais têm 3 pinos (G, V, S). Os conectores A0 e A1, usados pelos encoders, não aparecem com clareza na foto. Há versões do shield com os pinos em outro lugar. Meça antes de ligar. | R$ 11–35 (cada) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pacote de 10 | Divisor de tensão na serial: baixa os 5 V do Arduino para os 3,3 V que o Raspberry Pi aceita. Os 3 ficam presos na barra de emenda, no deck. | R$ 1–5 (pacote) | não conferido |
| [Kit de dissipadores adesivos para Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | O Raspberry Pi fica fechado dentro da cabeça, que é de PLA e não tem abertura de ventilação. Os dissipadores colados nos chips baixam a temperatura. NC: altura do dissipador: tem de caber nos cerca de 20 mm entre o Pi e a tela. | R$ 8–25 (kit) | não conferido |

### Rodas e motores

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Motor JGB37-520 de 12 V com encoder, 107 rpm (redução 1:56), eixo de 6 mm em D](https://lista.mercadolivre.com.br/motor-jgb37-520-12v-encoder-107rpm) | 2 / 2 | Tração: um motor por roda. Cada motor vem com um cabo de 6 fios: 2 do motor e 4 do encoder, o sensor que conta as voltas da roda. Escolha a versão de 12 V e 107 rpm. NC: posição dos 6 furos M3 em volta do eixo, que fica 7 mm fora do centro, e fundo da rosca (3,5 a 4 mm). | R$ 60–150 (cada) | não conferido |
| [Roda de 85 × 38 mm com encaixe sextavado de 12 mm](https://lista.mercadolivre.com.br/roda-85mm-sextavado-12mm-robo) | 2 / 2 | As 2 rodas da frente. O raio de 42,5 mm é o que deixa o robô passar por soleiras baixas. | R$ 30–60 (cada) | R$ 38,87 cada |
| [Adaptador sextavado de 12 mm para eixo de 6 mm (acoplamento de roda, com parafuso de trava)](https://lista.mercadolivre.com.br/adaptador-sextavado-12mm-eixo-6mm-roda) | 2 / 2 | Prende a roda no eixo do motor. NC: comprimento (20 mm no modelo; o de latão comum tem cerca de 18 mm). | R$ 10–30 (cada) | não conferido |
| [Bola de tênis de mesa de 40 mm](https://lista.mercadolivre.com.br/bola-tenis-de-mesa-40mm) | 1 / 1 pacote | Apoio de trás: rola solta num poço da base, presa pela capa. É ela que limita o degrau que o robô passa: cerca de 8 mm. NC: as bolas marcadas 40+ medem de 40,0 a 40,6 mm; o poço tem 41,2 mm. | R$ 5–20 (pacote) | não conferido |
| [Driver de motor L298N (módulo ponte H dupla, 2 A por canal)](https://lista.mercadolivre.com.br/driver-motor-l298n-ponte-h) | 1 / 1 | Liga, desliga e inverte os 2 motores. Fica no deck, em 4 ressaltos. Ele tira cerca de 2 V dos motores: com o pack em 11 V chegam cerca de 9 V, o que este robô aceita. NC: distância entre os 4 furos (37 mm no modelo) e nome impresso dos pinos e dos jumpers. | R$ 18–35 (cada) | R$ 21,51 a R$ 29,18 |

### Energia

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Bateria 18650 de íon de lítio 3,7 V (célula solta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 3 / 3 | Pack 3S: 11,1 V nominais (12,6 V cheio). Compre as três iguais, novas e de marca conhecida. | R$ 13–45 (cada) | R$ 26,08 o kit com 2 |
| [Suporte para 3 baterias 18650 lado a lado, com fios](https://lista.mercadolivre.com.br/suporte-3-baterias-18650) | 1 / 1 | Segura as 3 células em série. Fica preso no alçapão, que sai por baixo do robô com 4 parafusos. NC: o berço do alçapão foi feito para 75 × 61 × 20 mm. | R$ 6–18 (cada) | R$ 7,80 |
| [Porta-fusível de fio para fusível de vidro 5 × 20 mm, com fusível retardado de 3 A (marcado T3A ou T3,15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (e 1 fusível de reserva) | No fio positivo, logo depois do suporte das baterias. É de 3 A porque a chave é de 3 A: numa sobrecarga, o fusível abre antes de a chave esquentar. É retardado porque a partida dos motores e dos servos e a carga do capacitor dão picos de uma fração de segundo, que queimariam um fusível rápido sem haver defeito. Não tem lugar modelado: fica solto no fio. | R$ 4–12 (conjunto) | não conferido |
| [Placa de proteção BMS 3S 10 A (modelo HX-3S-FL10, 50 × 15 mm)](https://lista.mercadolivre.com.br/bms-3s-10a-18650-hx-3s-fl10) | 1 / 1 | Corta a descarga funda, a sobrecarga e o curto. Vai soldada nos fios da bateria, presa com fita dupla-face no piso da base. Esta placa não equilibra as células: quem equilibra é o carregador. NC: nome impresso das ilhas de solda (não aparece na página da loja). Em geral são 0V, 4,2V, 8,4V e 12,6V do lado das células e P+ e P− do lado da saída. Confira com o multímetro. | R$ 15–30 (cada) | R$ 21,60 |
| [Carregador USB-C 2S/3S com balanceamento (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carrega o pack sem abrir o robô. Ele vem pronto para 2 células. Para 3 células é preciso tirar um resistor minúsculo da placa e fechar um jumper com solda, como mostra a figura da página da loja. No modo de 3 células ele usa 4 fios: positivo, negativo e as 2 emendas entre as células. NC: nome impresso das ilhas das 2 emendas (não dá para ler na foto da loja) e tamanho da boca USB-C na janela de trás (9,2 × 3,4 mm). | R$ 15–30 (cada) | R$ 17,90 |
| [Conversor step-down XL4015 ajustável (5 A)](https://lista.mercadolivre.com.br/modulo-step-down-xl4015-5a) | 1 / 1 | Baixa a tensão do pack para os 5,1 V do Raspberry Pi, do Arduino, do driver e dos encoders. Ajuste para 5,1 V com o multímetro ANTES de ligar qualquer placa. Ele pede no mínimo 8 V de entrada, e o pack de 3 células fica sempre acima disso. | R$ 12–30 (cada) | R$ 17,82 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S ou equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Alimenta os 2 servos em 6 V, separado do Pi. Ponha o jumper dele em 6 V. | R$ 25–60 (cada) | não conferido |
| [Capacitor eletrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | No borne de 6 V dos servos: segura o pico de corrente da partida. | R$ 1–4 (cada) | R$ 2,33 |
| [Chave gangorra KCD11-101 de 3 A (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Liga e desliga. Encaixa por pressão na parede de trás da base, por fora. A ficha dá 3 A em 250 V~ e 6 A em 125 V~, sem valor para corrente contínua: por isso o fusível é de 3 A. É o ponto mais fraco da parte elétrica deste robô (veja os riscos). NC: espessura de painel que a trava aceita. | R$ 3–8 (cada) | R$ 3,74 a R$ 5,40 (modelos KCD1; confira o recorte) |
| [Fio flexível 22 AWG (0,33 mm²): vermelho, preto e uma terceira cor](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | cerca de 50 cm de vermelho, 30 cm de preto e 80 cm de amarelo / 2 m de vermelho, 2 m de preto, 1 m de amarelo | Os fios finos da energia: os 4 fios das emendas das células (amarelos), as ligações do carregador e os 5,1 V do driver. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Fio flexível 20 AWG (0,5 mm²), vermelho e preto](https://lista.mercadolivre.com.br/fio-flexivel-20awg-vermelho-preto) | cerca de 1,1 m de cada cor / 2 m de cada cor | Os fios que levam mais corrente: da chave e da placa de proteção até a barra de emenda, da barra ao conversor e ao driver, e o par de 5,1 V que sobe pelo pescoço até o Raspberry Pi. Fio mais grosso perde menos tensão no caminho; com fio fino o Pi acusa subtensão. | R$ 8–25 (total) | não conferido |
| [Barra de bornes de emenda (tipo sindal) de 12 vias, para fio fino](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 5 vias (bornes 1 a 5) / 1 barra de 12 vias; corte um pedaço com 5 | Fica no deck e evita soldar com o robô montado. Borne 1: os 5,1 V. Borne 2: o negativo. Borne 3: o fio azul da serial e os resistores do divisor. Borne 4: o positivo do pack, depois da chave. Borne 5: o negativo do pack. Não tem lugar modelado: fica solta. | R$ 3–10 (barra) | não conferido |
| [Jumpers Dupont fêmea-fêmea de 40 cm (kit com 40)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-40cm) | 16 fios / 1 kit de 40 | São 16: 3 da serial (verde, azul e preto, do Raspberry Pi até o deck), 2 que levam os 5,1 V e o negativo da barra de emenda ao Arduino, 1 cortado ao meio para o divisor, 2 cortados ao meio para a energia do Raspberry Pi, 6 do driver dos motores e 2 cortados ao meio para os encoders. Os da serial ficam justos: se faltar fio, emende um pedaço de jumper na ponta do deck, com solda e termo-retrátil, ainda no preparo 3. | R$ 10–25 (kit) | não conferido |

### Fixação

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Inserto de latão M3 a quente (para furo de 4,0 mm, até 5,7 mm de comprimento)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 31 / 2 pacotes de 20 (ou 1 de 50) | A rosca de metal das peças: 8 nas paredes dos motores, 4 do alçapão e 4 da capa da bola (todos na base), 4 nas colunas do tronco, 4 nos pilares do painel do rosto, 4 nas colunas do quadro e 3 no garfo. | R$ 15–40 (pacote) | não conferido |
| [Parafuso M3 × 6 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x6) | 12 / 2 kits de 10 | 6 em cada motor: prendem o motor na flange, com a cabeça no rebaixo. NC: fundo da rosca do motor: 3,5 a 4 mm. Depois da flange sobram 4 mm de parafuso. Se ele encostar no fundo antes de apertar, troque por M3 × 5. | R$ 3–8 (kit com 10) | não conferido |
| [Parafuso M3 × 8 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 24 / 3 kits de 10 | 4 do alçapão, 4 da capa da bola, 4 do Arduino, 4 do driver, 4 do painel do rosto e 4 do copo da cabeça. | R$ 3–8 (kit com 10) | R$ 6,14 o kit com 10 (tipo de cabeça não informado) |
| [Parafuso M3 × 10 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 8 / 1 kit de 10 | 4 em cada flange de motor, nos insertos da parede da base. Ficam escondidos atrás da roda. | R$ 3–8 (kit com 10) | R$ 3,55 o kit com 10 (Phillips) |
| [Parafuso M3 × 12 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x12) | 12 / 2 kits de 10 | 4 em cada servo MG996R, rosqueados direto no plástico (furo de 2,7 mm), e 4 que entram por baixo da base, atravessam o deck e rosqueiam nos insertos do tronco. Estes 4 têm de ser Allen de cabeça cilíndrica: a cabeça fica no fundo de um furo de 68 mm. | R$ 3–8 (kit com 10) | não conferido |
| [Parafuso M3 × 50 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x50) | 3 / 3 (vendido por unidade) | Tirantes do pescoço: entram por dentro do tronco, pela engrenagem, atravessam o tubo e rosqueiam nos insertos do garfo. | R$ 1–4 (cada) | não conferido |
| [Parafuso M5 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit de 10 (ou 1 avulso) | Pino do tilt: passa pela lateral do quadro e rosqueia no braço do garfo. A cabeça inclina em volta dele. | R$ 3–8 (kit com 10) | R$ 6,04 o kit com 10 (Phillips) |
| [Parafuso M2,5 × 12 mm com porca M2,5](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 parafusos e 4 porcas / 1 kit | Prende o Raspberry Pi no quadro, com os 4 espaçadores impressos no meio. | R$ 5–15 (kit) | não conferido |
| [Parafuso M2,5 × 6 mm](https://lista.mercadolivre.com.br/parafuso-m2.5x6) | 4 / 1 kit | Prende a tela de 5 polegadas nos 4 pilares do painel do rosto, rosqueado direto no plástico. NC: diâmetro dos furos da placa da tela. | R$ 5–15 (kit) | não conferido |
| [Parafuso M2 × 8 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 em cada horn redondo: prende a engrenagem no servo de pan e o garfo no servo de tilt. NC: diâmetro dos furos do horn redondo. | R$ 3–8 (kit com 10) | R$ 3,31 o kit com 10 (confira se é auto-atarraxante) |
| [Abraçadeira de nylon de 3,6 mm de largura (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 4 / 1 pacote de 100 | Uma em cada berço: conversor de 5 V, UBEC, carregador e suporte das baterias, no alçapão. | R$ 8–20 (pacote) | não conferido |
| [Fita dupla-face de espuma](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | cerca de 5 cm / 1 rolo | Prende a placa de proteção (BMS) no piso da base. | R$ 8–20 (rolo) | não conferido |

### Filamento

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Filamento PETG de 1,75 mm, rolo de 1 kg](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 823 g, em 4 cores sugeridas (amarelo, branco, grafite e prata) / 1 rolo de qualquer cor (ou 4 rolos, um de cada cor sugerida) | As peças que fazem força: base, alçapão, capa da bola, flanges, deck, tronco, pescoço, engrenagens, garfo e quadro da cabeça. A cor é só sugestão; o material não: mantenha PETG. Um rolo de 1 kg dá com pouca sobra: a conta é uma estimativa sem fatiador, e se uma peça grande falhar no meio falta filamento. | R$ 90–150 (rolo) | não conferido |
| [Filamento PLA de 1,75 mm, rolo de 1 kg](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 320 g, em 3 cores sugeridas (branco, cinza e preto) / 1 rolo de qualquer cor (ou 3 rolos, um de cada cor sugerida) | As peças que só vestem o robô: copo da cabeça, painel do rosto, espaçadores e cupom de teste. A cor é só sugestão. | R$ 80–140 (rolo) | não conferido |

### Ferramentas e material de solda (se você não tiver)

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Ferro de solda de 30 a 60 W, de preferência com ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solda os fios de energia e assenta os 31 insertos a quente. Com ponta fina, também fecha o jumper de solda do carregador. | R$ 40–150 (cada) | não conferido |
| [Ponta de ferro de solda para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guia o inserto reto no furo. A ponta cônica comum também serve: apoie a ponta dentro do inserto e empurre devagar. | R$ 15–40 (cada) | não conferido |
| [Estanho de solda com fluxo, 0,8 a 1 mm (tubo pequeno)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todas as emendas de fio e as ilhas da placa de proteção. | R$ 8–25 (tubo) | não conferido |
| [Tubo termo-retrátil de 2 a 3 mm e de 5 a 6 mm (ou fita isolante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | cerca de 30 cm de cada / 1 m de cada | Isola cada emenda de fio. Nenhum metal pode ficar à mostra perto da bateria. | R$ 5–20 (total) | não conferido |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta o conversor em 5,1 V, confere os 6 V do UBEC, as emendas das células (cerca de 4 V e 8 V) e a polaridade antes de ligar as placas. | R$ 40–100 (cada) | não conferido |
| [Chave de fenda de precisão de 2 mm e chave Phillips pequena (PH0 ou PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | A de fenda gira o parafuso de ajuste do XL4015 e aperta os bornes. A Phillips aperta os parafusos M2 dos horns, o parafuso central dos servos e os parafusos de cabeça Phillips. | R$ 10–35 (cada) | não conferido |
| [Alicate de corte pequeno](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Corta os fios, as pernas dos resistores e a sobra das abraçadeiras. | R$ 15–40 (cada) | não conferido |
| [Descascador de fio (ou um estilete, com cuidado)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Tira a capa das pontas dos fios 20 e 22 AWG sem cortar os fiozinhos de cobre. | R$ 15–45 (cada) | não conferido |
| [Pinça de ponta fina](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Puxa as pontas dos fios pelo rasgo do fundo da cabeça, segura os resistores na hora de soldar e tira o resistor minúsculo do carregador. | R$ 5–20 (cada) | não conferido |
| [Chave Allen de 2,5 mm longa (haste de 80 mm ou mais)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa-haste-100mm) | 1 / 1 | Aperta os 4 parafusos que entram por baixo da base, no fundo de furos de 68 mm, e os 3 tirantes do pescoço. | R$ 8–25 (cada) | não conferido |
| [Paquímetro](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Confere as medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada) | não conferido |
| [Fonte USB-C de 5 V e 3 A (15 W), com cabo USB-C](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Carrega o pack pela boca USB-C de trás e liga o Raspberry Pi no preparo 4. Para o Pi 4 ela tem de entregar 5 V e 3 A: muita fonte de celular não chega a isso (leia a etiqueta). A fonte oficial do Raspberry Pi 4, de 5,1 V e 3 A, é a opção segura. | R$ 25–80 (cada) | não conferido |
| [Cabo USB A-B (o de impressora) e um computador com a Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Grava o sketch no Arduino Uno, antes de fechar o robô. | R$ 8–25 (cada) | não conferido |
| [Leitor de cartão microSD (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Grava o sistema do Raspberry Pi no cartão, pelo seu computador. Muitos notebooks já têm a entrada. | R$ 10–30 (cada) | não conferido |
<!-- /GERADO -->

## Parafusos e insertos, contados

31 insertos M3 a quente: 8 nas paredes dos motores, 4 do alçapão e 4 da capa da bola (os 16 ficam na base), 4 nas
colunas do tronco, 4 nos pilares do painel do rosto, 4 nas colunas do quadro da cabeça e 3 no garfo.

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

Os parafusos do horn central e os anéis de borracha dos servos vêm no kit do MG996R. O parafuso de trava e o parafuso
da ponta do adaptador sextavado vêm com o adaptador.

## Filamento

Gramas por cor, somando as 19 peças (estimativa por volume, sem fatiador). A cor é sugestão; o material não:
mantenha PETG onde está PETG. O mínimo são 2 rolos de 1 kg, um de PETG e um de PLA, de qualquer cor. O de PETG fica
quase todo no robô: se uma impressão longa falhar, vai faltar. Nas 7 cores sugeridas são 7 rolos, 4 de PETG e 3 de
PLA, e sobra muito filamento. As duas linhas de filamento estão na lista acima.

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 108 | 4,1 |
| PETG branco | 236 | 8,7 |
| PETG grafite | 454 | 17,1 |
| PETG prata | 25 | 1,1 |
| PLA branco | 248 | 9,3 |
| PLA cinza | 15 | 0,9 |
| PLA preto | 57 | 2,2 |
| **Total** | **1143** | **43,4** |
<!-- /GERADO -->

## Fase 2 (opcional agora)

Nada disto é necessário para imprimir, montar e ligar. As peças já têm o lugar, os furos e a passagem dos cabos, e
nenhum desses furos aparece de frente: a coluna "Onde vai" diz onde cada um está escondido.

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
| [Sensor de distância ToF VL53L1X (placa pequena)](https://lista.mercadolivre.com.br/sensor-vl53l1x-tof) | 3 | Por dentro da parede da base, 10 mm abaixo da borda de cima: um na frente e um de cada lado. Cada ponto tem 2 furos cegos para parafuso M2,5 e, entre eles, uma janela cega: por fora a parede é lisa, com 0,8 mm de plástico na frente da janela. Na instalação, fure essa pele por dentro com broca de 6 mm. Depois disso ficam 3 furos de 6 mm à vista na base. NC: tamanho da placa (25 × 10,7 mm) e distância entre os furos. | R$ 40–110 | R$ 102,32 |
| [Sensor de queda (reflexivo infravermelho, por exemplo TCRT5000)](https://lista.mercadolivre.com.br/sensor-reflexivo-infravermelho-tcrt5000) | 1 | Numa janela de 14 × 6 mm no piso da base, na frente, olhando para o chão, com um par de furos M3 a 20 mm. Só aparece por baixo. | R$ 5–15 | R$ 7,92 |
<!-- /GERADO -->

## Glossário

<!-- GERADO:glossario -->
- **GPIO:** A fileira de 40 pinos do Raspberry Pi, onde se ligam os fios de energia e de sinal. Neste guia, "pino 32" é a posição do pino na fileira; "GPIO12" é o nome do sinal que sai por ele.
- **UBEC:** Conversor pequeno, usado em aeromodelos, que baixa a tensão da bateria para um valor fixo. Aqui, 6 V para os servos.
- **BMS:** Placa de proteção da bateria de lítio. Desliga a bateria antes de ela descarregar demais, carregar demais ou entrar em curto.
- **3S:** Três células de lítio ligadas em série, uma depois da outra. As tensões somam: de 9 V (vazio) a 12,6 V (cheio).
- **Emenda (do pack):** O ponto em que uma célula se liga à seguinte. Num pack de 3 células são 2 emendas. A placa de proteção e o carregador medem cada célula por elas.
- **Horn:** A peça de plástico que encaixa no eixo do servo e gira com ele. Este robô usa o horn redondo, em forma de disco.
- **Inserto a quente:** Bucha de latão com rosca por dentro. Entra no furo do plástico empurrada com o ferro de solda e vira uma rosca de metal.
- **NC:** Não confirmado: uma medida que veio de anúncio de loja e ainda não foi conferida com a peça na mão.
- **Fatiador:** O programa que transforma o arquivo 3D nas camadas que a impressora imprime. O da Bambu Lab se chama Bambu Studio.
- **SSH:** Jeito de usar o Raspberry Pi pela rede: você digita os comandos no terminal do seu computador e eles rodam no Pi, sem ligar teclado nem monitor nele.
- **UART (serial):** Ligação de dados simples: um fio para falar (TX) e um para ouvir (RX). É por ela que o Raspberry Pi manda ordens ao Arduino.
- **Driver (ponte H):** Placa que liga os motores na bateria e inverte o sentido deles quando o Arduino manda. Aqui é o L298N.
- **Encoder:** Sensor preso atrás do motor que conta as voltas. Com ele o programa sabe quanto cada roda andou.
- **Jumper SEL:** Capinha de plástico sobre 2 pinos do Sensor Shield, ao lado do borne azul, com a marca SEL. Posta, ela liga os 5 V do Arduino aos conectores dos servos. Retirada, os servos recebem só o que entra pelo borne azul.
- **Borne:** Conector de parafuso: o fio entra no furo e o parafuso aperta. No Sensor Shield é o bloco azul marcado GND e VCC.
- **Sketch:** O nome que a Arduino dá a um programa. Você abre o arquivo na Arduino IDE e grava na placa pelo cabo USB.
- **Shield:** Placa que encaixa por cima do Arduino, nos pinos dele, e acrescenta conectores. Aqui, o Sensor Shield dá os conectores dos servos, do driver e dos encoders.
- **AWG:** Medida da grossura do fio. Quanto menor o número, mais grosso: o 20 AWG é mais grosso que o 22 AWG.
- **GND:** O negativo do circuito, também chamado de terra. Todos os negativos do robô são ligados entre si.
- **Dupont:** Fio fino que já vem com um conector de encaixe em cada ponta, do tamanho dos pinos das placas. Também é chamado de jumper.
- **Step-down:** Conversor que baixa a tensão. Aqui, o XL4015 baixa a tensão da bateria para 5,1 V.
- **Termo-retrátil:** Tubinho de plástico que encolhe com calor. Você veste sobre a emenda de solda e aquece: ele aperta e isola.
- **Alçapão:** A tampa por baixo da base. Ela leva o suporte das baterias e sai com 4 parafusos, sem abrir o resto do robô.
- **Flange:** O disco que prende cada motor na parede da base. Fica escondido atrás da roda.
- **Deck:** A bandeja que fica entre a base e o tronco. Nela vão o Arduino, o driver, os conversores e o servo que gira o pescoço.
<!-- /GERADO -->

Como ligar tudo o que está nesta lista: [LIGACAO.md](LIGACAO.md). Como imprimir: [IMPRIMIR.md](IMPRIMIR.md).
