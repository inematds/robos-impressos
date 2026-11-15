# Lista de compras do dinossauro

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Tudo o que você precisa comprar para montar o dinossauro na fase 1: o corpo montado e ligado. O programa vem depois, na fase 2.

Página com a mesma lista: https://inematds.github.io/robos-impressos/guia/dino/#comprar

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
- Nada foi impresso nem montado ainda. A parte elétrica não foi testada na bancada: ela saiu das fichas dos componentes.
- Seis peças pedem suporte de impressão: crânio, corpo, traseira, mandíbula, garfo do pescoço e berço do tilt. O suporte fica por dentro ou por baixo, fora do rosto, mas ninguém o tirou ainda de uma peça de verdade.
- Os arquivos 3MF das mesas nunca foram abertos no Bambu Studio. Se algum não abrir, use os STL.
- A chave liga/desliga é de 3 A e, pela conta das fichas, o uso normal chega perto disso (entre 2,5 e 3 A com as rodas andando, a cabeça e os braços mexendo). O fusível de 3 A protege a chave e pode abrir quando o robô fizer força. Uma chave maior pede mudar o recorte da peça: é uma pendência do projeto.
- O Raspberry Pi recebe os 5,1 V pelos pinos de 5 V, porque na bandeja a porta USB-C dele fica encostada na parede do rack. É uma ligação comum, mas não foi testada neste robô: fio trocado ou tensão errada nesses pinos queima o Pi. Meça antes de encaixar.
- Sobre o Raspberry Pi sobram cerca de 17 mm até a bandeja de cima (medida do modelo, não confirmada). O conector Dupont comum tem cerca de 16,5 mm em pé e pode não caber. Plano B: soldar os fios numa barra de pinos fêmea baixa, com os fios saindo de lado.
- O cupom de teste não confere a janela do servo MG996R. Confira o servo no berço do tilt, que sai numa das primeiras mesas, antes das impressões longas.
- O porta-fusível, a barra de emenda e os 3 resistores da serial não têm lugar modelado: ficam soltos dentro do corpo, isolados com termo-retrátil.
- Os comprimentos dos cabos (servos da cabeça, extensões e jumpers) foram estimados pelo modelo. A cabeça gira e inclina e puxa esses cabos: deixe folga e confira os dois extremos antes de fechar.
- O horn do micro servo de cada braço não está no modelo 3D: o teste de montagem não prova que o corpo desce com ele no lugar. Monte o horn apontando para trás e para cima e só gire depois.
- O Arduino vai atravessado na bandeja e o USB dele fica de lado: para regravar o programa é preciso puxar a bandeja.
- As medidas marcadas como NC vêm de anúncios de loja. Meça a sua peça antes de imprimir a parte que encosta nela.
- O estriado do micro servo tem passos de uns 17° (valor usual, não confirmado): o horn da boca e os dos braços podem não cair exatamente na posição de 90°. Escolha o dente mais próximo; o ajuste fino é no programa, na fase 2.
- Calor: o Raspberry Pi fica fechado no corpo, que é de PLA e não tem abertura de ventilação. O PLA amolece perto de 60 °C e o Pi reduz a velocidade a partir de 80 °C. Cole os dissipadores e meça com o comando `vcgencmd measure_temp`. Se passar de 70 °C, abra furos de ventilação na traseira.
<!-- /GERADO -->

## Quanto custa

<!-- GERADO:custo -->
- Peças da fase 1 (sem filamento e sem ferramentas): **R$ 889–1953**.
- Do zero (peças, 2 rolos de filamento e todas as ferramentas): **R$ 1273–2918**.
- Só os 2 rolos de filamento (1 de PETG e 1 de PLA): R$ 170–290.
- Se você já tem o Arduino Uno, desconte: R$ 43–90.
- Se você já tem todas as ferramentas, desconte: R$ 214–675.
<!-- /GERADO -->

## Fase 1: o que comprar

<!-- GERADO:compras -->
### Cérebro e movimento

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | Cérebro do robô. Vai na bandeja de baixo, dentro do corpo. Na fase 1 ele só é ligado e configurado; quem quiser adiar esta compra pode montar tudo sem ele e deixar a bandeja vazia. O Pi 5 também serve, com 1 câmera e sem acessórios USB: o conversor entrega cerca de 2 A. | R$ 450–800 (cada) | não conferido |
| [Cartão microSD 32 GB classe 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema do Raspberry Pi. | R$ 25–50 (cada) | não conferido |
| [Kit de dissipadores adesivos para Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | O Raspberry Pi fica fechado dentro do corpo, que é de PLA e não tem abertura de ventilação. Os dissipadores colados nos chips baixam a temperatura. NC: altura do dissipador: sobre o Raspberry Pi sobram cerca de 17 mm até a bandeja de cima. | R$ 8–25 (kit) | não conferido |
| [Servo MG996R de 180° (posição, não o de rotação contínua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Um gira a cabeça para os lados (pan) e o outro inclina (tilt). NC: espessura e furos das abas, diâmetro e espessura do horn redondo. | R$ 30–75 (cada) | R$ 70,45 |
| [Micro servo de 9 g, de 180°: MG90S ou SG90 (posição, não o de rotação contínua)](https://lista.mercadolivre.com.br/micro-servo-mg90s-180-graus) | 3 / 3 | Abre a boca (1) e move os braços (2). Prefira o MG90S, que tem engrenagens de metal. NC: espessura da aba, distância entre os furos e tamanho do horn de 1 braço. | R$ 15–45 (cada) | R$ 17,71 (SG90) a R$ 41,84 (MG90S) |
| [Extensão de servo de 30 cm (cabo extensor de 3 fios, macho-fêmea)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 2 / 2 | Uma leva o cabo do servo da boca até o Arduino; a outra é para o servo de tilt, se o cabo dele não alcançar. NC: comprimento do cabo de fábrica de cada servo (de 15 a 30 cm): meça o caminho antes de fechar. | R$ 5–15 (cada) | não conferido |
| [Motor DC 3 a 6 V com caixa de redução 1:48 (motor TT amarelo)](https://lista.mercadolivre.com.br/motor-dc-3-6v-caixa-de-reducao-48-1) | 2 / 2 | Tração: um em cada roda. Se vier sem fios, você solda 2 fios em cada um no preparo 1. NC: distância entre os 2 furos de trás (o rasgo aceita de 12,3 a 17,6 mm) e espessura da caixa (18,6 mm no modelo). | R$ 7–20 (cada) | R$ 9,01 |
| [Roda de 65 mm para motor TT](https://lista.mercadolivre.com.br/roda-65mm-motor-dc-arduino) | 2 / 2 | Encaixa por pressão no eixo do motor. Muitas lojas vendem o par motor + roda. NC: diâmetro (65 mm no modelo; há rodas de 64 a 68 mm) e largura (até 27 mm). | R$ 5–15 (cada) | R$ 20,54 o kit de 1 motor com 1 roda de 64 mm |
| [Esfera de aço de 16 mm (ou bolinha de gude, medida)](https://lista.mercadolivre.com.br/esfera-de-aco-16mm) | 1 / 1 | Terceiro apoio do robô, atrás, sob a raiz da cauda. Gira solta num soquete, presa por uma capa. NC: diâmetro: o soquete é para 16 mm; bolinha de gude varia de 14 a 25 mm. | R$ 3–10 (cada) | não conferido |
| [Driver de motores L298N (ponte H dupla)](https://lista.mercadolivre.com.br/driver-ponte-h-l298n) | 1 / 1 | Liga e inverte os 2 motores das rodas, a mando do Arduino. NC: distância entre os 4 furos (37 mm no modelo); se não bater, prenda com fita dupla-face. | R$ 20–35 (cada) | R$ 21,51 a R$ 29,18 |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (você talvez já tenha) | 1 / 1 | Comanda os 5 servos e os 2 motores. Vai na bandeja de cima, dentro do corpo. | R$ 43–90 (cada) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Encaixa em cima do Uno e dá os conectores de 3 pinos dos servos, com alimentação separada pelo borne azul. O Arduino recebe os 5,1 V pelo pino + do conector COM do shield. NC: pela foto da loja, o conector COM tem 4 pinos em pé, marcados TX, RX, − e +; há versões do shield com os pinos em outro lugar. Meça antes de ligar. | R$ 11–35 (cada) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pacote de 10 | Divisor de tensão na serial: baixa os 5 V do Arduino para os 3,3 V que o Raspberry Pi aceita. Os 3 ficam presos na barra de emenda. | R$ 1–5 (pacote) | não conferido |

### Energia

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Bateria 18650 de íon de lítio 3,7 V (célula solta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | Pack 2S: 7,4 V nominais (8,4 V cheio). Compre as duas iguais, novas e de marca conhecida. | R$ 13–45 (cada) | R$ 26,08 o kit com 2 |
| [Suporte para 2 baterias 18650 lado a lado, com fios](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Segura as 2 células em série. Fica no piso do chassi e sai por trás. NC: a baia do chassi aceita até 78 × 41 × 22 mm. | R$ 5–15 (cada) | R$ 6,22 |
| [Porta-fusível de fio para fusível de vidro 5 × 20 mm, com fusível retardado de 3 A (marcado T3A ou T3,15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (e 1 fusível de reserva) | No fio positivo, logo depois do suporte das baterias. É de 3 A porque a chave é de 3 A: numa sobrecarga, o fusível abre antes de a chave esquentar. É retardado porque a partida dos servos e a carga do capacitor dão picos de uma fração de segundo, que queimariam um fusível rápido sem haver defeito. Não tem lugar modelado: fica solto no fio. | R$ 4–12 (conjunto) | não conferido |
| [Placa de proteção BMS 2S 10 A (modelo 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Corta a descarga funda, a sobrecarga e o curto. Vai soldada nos fios da bateria, presa com fita dupla-face. NC: nome impresso das ilhas de solda. Na placa da loja consultada só o verso tem nomes: B+, B1 (meio), B− e C−. Pela foto, a C− é a saída negativa (o papel da P− de outras placas) e a saída positiva é a própria B+; é leitura de foto, confira com o multímetro. | R$ 8–20 (cada) | não conferido |
| [Carregador USB-C 2S/3S com balanceamento (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carrega as duas células sem abrir o robô. Fica numa mesinha do chassi, atrás; o plugue entra por um rasgo sob a raiz da cauda. NC: altura da boca USB-C no rasgo de 13 × 7 mm sob a raiz da cauda. | R$ 15–30 (cada) | R$ 17,90 |
| [Conversor step-down LM2596 ajustável (placa azul, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Baixa a tensão do pack para os 5 V do Raspberry Pi e do Arduino. Ajuste para 5,1 V com o multímetro ANTES de ligar qualquer placa. A placa aguenta cerca de 2 A contínuos sem dissipador. O XL4015 não serve aqui: pede no mínimo 8 V. NC: os 2 A contínuos são o valor usual desta placa, sem ficha que confirme. | R$ 8–20 (cada) | R$ 10,22 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S ou equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Dá os 6 V dos 5 servos, separados dos 5 V das placas. | R$ 25–60 (cada) | não conferido |
| [Capacitor eletrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | No borne de 6 V dos servos: segura o pico de corrente da partida. | R$ 1–4 (cada) | R$ 2,33 |
| [Chave gangorra KCD11-101 de 3 A (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Liga e desliga. Encaixa por baixo do piso, entre as pernas. NC: espessura de painel que a trava aceita. | R$ 3–8 (cada) | R$ 3,74 a R$ 5,40 (modelos KCD1; confira o recorte) |
| [Fio flexível 22 AWG (0,33 mm²): vermelho, preto e uma terceira cor](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | cerca de 2 m de vermelho, 2 m de preto e 30 cm de amarelo / 3 m de vermelho, 3 m de preto, 1 m de amarelo | Toda a parte de energia e os fios dos 2 motores. O amarelo é o 3º fio, do ponto do meio do pack. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Barra de bornes de emenda (tipo sindal) de 12 vias, para fio fino](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 3 vias (bornes 1, 2 e 3) / 1 barra de 12 vias; corte um pedaço com 3 | Fica dentro do corpo e evita soldar com o robô montado. Borne 1: os 5,1 V. Borne 2: o negativo. Borne 3: o fio azul da serial e os resistores do divisor. De um lado entram os fios que vêm do conversor; do outro, os que vão ao Raspberry Pi, ao Arduino e ao driver. Não tem lugar modelado: fica solta. | R$ 3–10 (barra) | não conferido |
| [Jumpers Dupont fêmea-fêmea de 20 cm (kit com 40)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-20cm) | 16 fios / 1 kit de 40 | Energia e serial do Raspberry Pi, energia do Arduino e os 6 sinais do driver dos motores. | R$ 8–20 (o kit) | não conferido |

### Fixação

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Inserto de latão M3 a quente (para furo de 4,0 mm, até 5,7 mm de comprimento)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 13 / 1 pacote de 20 ou mais | A rosca de metal das peças. Onde vai cada um está na tabela de parafusos. | R$ 15–40 (pacote) | não conferido |
| [Parafuso M3 × 8 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 10 / 2 kits de 10 | Driver dos motores, Arduino e capa da esfera. | R$ 3–8 (kit com 10) | R$ 6,14 o kit com 10 (tipo de cabeça não informado) |
| [Parafuso M3 × 10 mm, cabeça cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 6 / 1 kit de 10 | Gola, mesa da cabeça e pino do berço. | R$ 3–8 (kit com 10) | R$ 3,55 o kit com 10 (Phillips) |
| [Parafuso M3 × 12 mm](https://lista.mercadolivre.com.br/parafuso-m3x12) | 11 / 2 kits de 10 | 4 em cada servo MG996R, com porca, e 3 que prendem a mesa da cabeça no crânio. | R$ 3–8 (kit com 10) | não conferido |
| [Parafuso M3 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m3x16) | 2 / 1 kit de 10 | Prende o corpo nos postes do chassi, por trás das coxas. | R$ 3–8 (o kit de 10) | não conferido |
| [Parafuso M3 × 30 mm](https://lista.mercadolivre.com.br/parafuso-m3x30) | 4 / 1 kit de 10 | Prende os 2 motores das rodas. Com M3 × 25 a porca pega só 1,4 mm de rosca: são 18,6 mm de motor mais 5 mm de parede. | R$ 3–10 (o kit de 10) | R$ 3,44 o kit com 10 de M3 × 25 (o de 30 mm não foi visto) |
| [Porca sextavada M3](https://lista.mercadolivre.com.br/porca-sextavada-m3) | 12 / 1 kit de 20 ou mais | Nos parafusos dos 2 servos MG996R e dos 2 motores. | R$ 3–10 (o kit) | não conferido |
| [Parafuso M2,5 × 8 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2.5x8-auto-atarraxante) | 4 / 1 kit | Prende o Raspberry Pi na bandeja. | R$ 5–15 (o kit) | não conferido |
| [Parafuso M2 × 8 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 em cada horn redondo: prendem o garfo no servo de pan e o berço no servo de tilt. NC: diâmetro dos furos do horn redondo. | R$ 3–8 (kit com 10) | R$ 3,31 o kit com 10 (confira se é auto-atarraxante) |
| [Parafuso auto-atarraxante de 3 × 8 mm para plástico, cabeça abaulada](https://lista.mercadolivre.com.br/parafuso-auto-atarraxante-3x8-cabeca-panela) | 2 / 1 kit de 10 | Prende a traseira por baixo, direto no piso do chassi. | R$ 3–8 (o kit de 10) | não conferido |
| [Abraçadeira de nylon de 3,6 mm de largura (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 pacote de 100 | Prendem o conversor, o UBEC e a placa de proteção nos berços do chassi. | R$ 8–20 (pacote) | não conferido |
| [Fita dupla-face de espuma](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | cerca de 15 cm / 1 rolo | Segura o suporte das baterias no piso e o carregador na mesinha de trás. | R$ 8–20 (rolo) | não conferido |
| [Cola instantânea (cianoacrilato)](https://lista.mercadolivre.com.br/cola-instantanea-cianoacrilato) | algumas gotas / 1 tubo pequeno | Cola as peças coloridas que não têm parafuso nem pressão. | R$ 5–20 (o tubo) | não conferido |

### Filamento

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Filamento PETG de 1,75 mm, rolo de 1 kg](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 271 g, em 2 cores sugeridas (grafite e amarelo) / 1 rolo de qualquer cor (ou um rolo de cada cor sugerida) | As peças que fazem força: chassi, bandejas, garfo, berço, mesa da cabeça e capa da esfera. A cor é só sugestão; o material não: mantenha PETG. | R$ 90–150 (rolo) | não conferido |
| [Filamento PLA de 1,75 mm, rolo de 1 kg](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 739 g, em 7 cores sugeridas (verde, azul, creme, branco, cinza, verde-escuro e preto) / 1 rolo de 1 kg, se for tudo de uma cor só; nas cores sugeridas, 1 rolo da cor do corpo e sobras ou rolos pequenos das outras | As peças que vestem o robô: corpo, cabeça, olhos e as peças coloridas. A cor é só sugestão. | R$ 80–140 (rolo) | não conferido |

### Ferramentas e material de solda (se você não tiver)

| Item (o nome abre a busca) | Usa / comprar | Para que serve | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Ferro de solda de 30 a 60 W, de preferência com ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solda os fios de energia e assenta os 13 insertos a quente. | R$ 40–150 (cada) | não conferido |
| [Ponta de ferro de solda para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guia o inserto reto no furo. A ponta cônica comum também serve: apoie a ponta dentro do inserto e empurre devagar. | R$ 15–40 (cada) | não conferido |
| [Estanho de solda com fluxo, 0,8 a 1 mm (tubo pequeno)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todas as emendas de fio e as ilhas da placa de proteção. | R$ 8–25 (tubo) | não conferido |
| [Tubo termo-retrátil de 2 a 3 mm e de 5 a 6 mm (ou fita isolante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | cerca de 30 cm de cada / 1 m de cada | Isola cada emenda de fio. Nenhum metal pode ficar à mostra perto da bateria. | R$ 5–20 (total) | não conferido |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta o conversor em 5,1 V, confere os 6 V do UBEC e a polaridade antes de ligar as placas. | R$ 40–100 (cada) | não conferido |
| [Chave de fenda de precisão de 2 mm e chave Phillips pequena (PH0 ou PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | A de fenda gira o parafuso de ajuste do LM2596 e aperta os bornes. A Phillips aperta os parafusos M2 dos horns, o parafuso central dos servos e os parafusos de cabeça Phillips. | R$ 10–35 (cada) | não conferido |
| [Alicate de corte pequeno](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Corta os fios, as pernas dos resistores e a sobra das abraçadeiras. | R$ 15–40 (cada) | não conferido |
| [Descascador de fio (ou um estilete, com cuidado)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Tira a capa das pontas dos fios sem cortar os fiozinhos de cobre. | R$ 15–45 (cada) | não conferido |
| [Pinça de ponta fina](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Segura os resistores na hora de soldar e alcança os conectores dentro do corpo. | R$ 5–20 (cada) | não conferido |
| [Chave Allen de 2,5 mm longa (haste de 50 mm ou mais)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Aperta os parafusos Allen M3, inclusive os 2 do corpo, por trás das coxas. | R$ 8–25 (cada) | não conferido |
| [Paquímetro](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Confere as medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada) | não conferido |
| [Fonte USB-C de 5 V e 3 A (15 W), com cabo USB-C](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Carrega o pack pela boca USB-C do carregador e liga o Raspberry Pi na bancada, no preparo 4. Para o Pi 4 ela tem de entregar 5 V e 3 A: muita fonte de celular não chega a isso (leia a etiqueta). A fonte oficial do Raspberry Pi 4, de 5,1 V e 3 A, é a opção segura. | R$ 25–80 (cada) | não conferido |
| [Cabo USB A-B (o de impressora) e um computador com a Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Grava o sketch no Arduino Uno, com a bandeja dele fora do robô. | R$ 8–25 (cada) | não conferido |
| [Leitor de cartão microSD (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Grava o sistema do Raspberry Pi no cartão, pelo seu computador. Muitos notebooks já têm a entrada. | R$ 10–30 (cada) | não conferido |
<!-- /GERADO -->

## Parafusos e insertos, contados

13 insertos M3 a quente: 2 nos postes do chassi, 2 no ressalto da esfera de apoio, 3 na borda de cima do corpo, 3 no crânio, 2 no topo do berço do tilt e 1 no garfo do pescoço.

<!-- GERADO:parafusos -->
| Onde fica | Qtd | Parafuso | Onde rosqueia |
|---|---|---|---|
| Motores das rodas nas paredes do chassi | 4 | M3 × 30 + porca | porca do lado de dentro da parede |
| Servo de pan no deck | 4 | M3 × 12 + porca | porca por baixo do deck |
| Servo de tilt no berço | 4 | M3 × 12 + porca | porca por dentro do berço |
| Pino do berço, no lado esquerdo do garfo | 1 | M3 × 10 | inserto no garfo |
| Driver L298N na travessa | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Capa da esfera de apoio (por baixo) | 2 | M3 × 8 | inserto no chassi |
| Corpo nos postes do chassi (por trás das coxas) | 2 | M3 × 16 | inserto nos postes do chassi |
| Gola no corpo (por cima) | 3 | M3 × 10 | inserto na borda do corpo |
| Traseira (por baixo) | 2 | auto-atarraxante 3 × 8 mm, cabeça abaulada | direto no piso do chassi (furo de 2,7 mm) |
| Arduino Uno na bandeja | 4 | M3 × 8 | direto no plástico (furo de 2,7 mm) |
| Raspberry Pi na bandeja | 4 | M2,5 × 8 auto-atarraxante | direto no plástico (furo de 2,2 mm) |
| Mesa da cabeça no crânio (por baixo) | 3 | M3 × 12 | inserto no crânio |
| Mesa da cabeça na coluna do berço (por cima) | 2 | M3 × 10 | inserto no topo do berço |
| Horn redondo dos 2 servos MG996R | 8 | M2 × 8 auto-atarraxante | nos furos do horn |
| Micro servos da boca e dos 2 braços | 6 | parafuso que vem com o servo | direto no plástico (furo de 1,7 mm) |
<!-- /GERADO -->

O parafuso central, os parafusos do horn e os anéis de borracha vêm no kit de cada servo. Os comprimentos dos parafusos
M3 saíram das medidas do modelo e ainda não foram conferidos com as peças impressas.

## Filamento

Gramas por cor, somando as 34 peças (estimativa por volume, sem fatiador). A cor é sugestão; o material não:
mantenha PETG onde está PETG. O mínimo são 2 rolos de 1 kg, um de PETG e um de PLA, de qualquer cor. Nas cores
sugeridas, a cor do corpo gasta a maior parte de um rolo e as outras gastam poucos gramas cada: sobras de filamento
resolvem. As duas linhas de filamento estão na lista acima.

<!-- GERADO:filamento -->
| Material e cor | Filamento (g) | Tempo (h) |
|---|---|---|
| PETG amarelo | 28 | 1,2 |
| PETG grafite | 243 | 9,4 |
| PLA azul | 42 | 1,9 |
| PLA branco | 28 | 1,2 |
| PLA cinza | 15 | 0,6 |
| PLA creme | 28 | 1,5 |
| PLA preto | 4 | 0,4 |
| PLA verde | 618 | 23,8 |
| PLA verde-escuro | 4 | 0,2 |
| **Total** | **1010** | **40,2** |
<!-- /GERADO -->

## Fase 2 (opcional agora)

Nada disto é necessário para imprimir, montar e ligar. Os olhos já são feitos para os sensores: a pupila direita tem o
furo da lente da câmera e a pupila esquerda tem a janela do sensor de distância.

<!-- GERADO:fase2 -->
| Item (o nome abre a busca) | Qtd | Onde fica | Preço estimado | Visto em loja |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide (placa de 25 × 24 mm)](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3-wide) | 1 | Atrás da pupila do olho direito: a placa entra por trás do olho e encosta na íris, em 4 furos para parafuso M2. A lente olha pelo furo de 8,5 mm da pupila. NC: furos da placa e altura da lente. | R$ 200–400 | não conferido |
| [Cabo flat de câmera de 50 cm (no Raspberry Pi 5, o cabo de 22 para 15 vias)](https://lista.mercadolivre.com.br/cabo-flat-camera-raspberry-pi-50cm) | 1 | Sai pela janela de trás do olho, desce pela face chata da coluna do pescoço e pelo rasgo do garfo, até o Raspberry Pi. Deixe uma barriga em S dentro da gola: a cabeça gira 60° para cada lado. NC: comprimento: os 50 cm são estimativa pelo modelo. | R$ 15–45 | não conferido |
| [Parafuso M2 × 6 mm auto-atarraxante](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Prende a câmera nos 4 furos da íris direita. | R$ 3–8 | R$ 5,98 o kit com 10 |
| [Sensor de distância ToF VL53L1X (placa de cerca de 25 × 11 mm)](https://lista.mercadolivre.com.br/sensor-distancia-vl53l1x) | 3 | 1 atrás da pupila do olho esquerdo (janela de 6 mm): mede a distância do que a cabeça está olhando. 2 nas laterais, atrás das 2 manchas verde-escuras dos flancos (janela de 6 mm no miolo de cada mancha). NC: tamanho da placa e lugar da janela: meça antes de imprimir o olho esquerdo. | R$ 30–110 | R$ 102,32 (VL53L1X, até 4 m); R$ 31,81 (VL53L0X, até 2 m) |
| [Microfone I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Atrás das 2 narinas: cada narina é um furo de som de 2 mm e a placa redonda encaixa por dentro. NC: placa redonda de 14 mm de diâmetro: meça a sua. | R$ 15–55 | R$ 54,26 |
| [Alto-falante de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Em cima da mesa da cabeça, virado para baixo. O som sai pela fresta da boca e pelo vão do pescoço: não há grade à mostra. NC: diâmetro e profundidade. | R$ 7–20 | não conferido |
| [Amplificador de áudio pequeno (PAM8403 ou MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Sem lugar modelado ainda: vai solto dentro do corpo, com fita dupla-face. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | Sem lugar modelado neste robô: fita dupla-face no piso do chassi, perto do eixo das rodas. | R$ 15–35 | R$ 34,09 |
<!-- /GERADO -->

O LiDAR não entra nesta lista: neste robô a cabeça tampa a volta inteira de que ele precisa.

## Glossário

<!-- GERADO:glossario -->
- **GPIO:** A fileira de 40 pinos do Raspberry Pi, onde se ligam os fios de energia e de sinal. Neste guia, "pino 32" é a posição do pino na fileira; "GPIO12" é o nome do sinal que sai por ele.
- **UBEC:** Conversor pequeno, usado em aeromodelos, que baixa a tensão da bateria para um valor fixo. Aqui, 6 V para os servos.
- **BMS:** Placa de proteção da bateria de lítio. Desliga a bateria antes de ela descarregar demais, carregar demais ou entrar em curto.
- **2S:** Duas células de lítio ligadas em série, uma depois da outra. As tensões somam: de 6 V (vazio) a 8,4 V (cheio).
- **Horn:** A peça de plástico que encaixa no eixo do servo e gira com ele. Os 2 servos grandes usam o horn redondo, em forma de disco; os micro servos, o de 1 braço.
- **Inserto a quente:** Bucha de latão com rosca por dentro. Entra no furo do plástico empurrada com o ferro de solda e vira uma rosca de metal.
- **NC:** Não confirmado: uma medida que veio de anúncio de loja e ainda não foi conferida com a peça na mão.
- **Fatiador:** O programa que transforma o arquivo 3D nas camadas que a impressora imprime. O da Bambu Lab se chama Bambu Studio.
- **SSH:** Jeito de usar o Raspberry Pi pela rede: você digita os comandos no terminal do seu computador e eles rodam no Pi, sem ligar teclado nem monitor nele.
- **UART (serial):** Ligação de dados simples: um fio para falar (TX) e um para ouvir (RX). É por ela que o Raspberry Pi manda ordens ao Arduino.
- **Jumper SEL:** Capinha de plástico sobre 2 pinos do Sensor Shield, ao lado do borne azul, com a marca SEL. Posta, ela liga os 5 V do Arduino aos conectores dos servos. Retirada, os servos recebem só o que entra pelo borne azul.
- **Borne:** Conector de parafuso: o fio entra no furo e o parafuso aperta. No Sensor Shield é o bloco azul marcado GND e VCC.
- **Sketch:** O nome que a Arduino dá a um programa. Você abre o arquivo na Arduino IDE e grava na placa pelo cabo USB.
- **Shield:** Placa que encaixa por cima do Arduino, nos pinos dele, e acrescenta conectores. Aqui, o Sensor Shield dá os conectores dos servos.
- **AWG:** Medida da grossura do fio. Quanto menor o número, mais grosso: o 20 AWG é mais grosso que o 22 AWG.
- **GND:** O negativo do circuito, também chamado de terra. Todos os negativos do robô são ligados entre si.
- **Dupont:** Fio fino que já vem com um conector de encaixe em cada ponta, do tamanho dos pinos das placas. Também é chamado de jumper.
- **Step-down:** Conversor que baixa a tensão. Aqui, o LM2596 baixa a tensão da bateria para 5,1 V.
- **Termo-retrátil:** Tubinho de plástico que encolhe com calor. Você veste sobre a emenda de solda e aquece: ele aperta e isola.
- **Ponte H (L298N):** Placa que liga, desliga e inverte os motores das rodas a mando do Arduino. Também é chamada de driver de motores.
- **Micro servo:** Servo pequeno, de 9 gramas (SG90 ou MG90S). Aqui ele abre a boca e move os braços.
- **Pan e tilt:** Os dois movimentos da cabeça: pan é girar para os lados, tilt é inclinar para cima e para baixo.
- **ToF:** Sensor que mede distância pelo tempo que a luz leva para ir e voltar. É da fase 2.
- **Suporte (de impressão):** Material extra que o fatiador imprime embaixo de uma parte da peça que nasceria no ar. Você arranca depois de imprimir. Suporte em árvore é o tipo que sobe em galhos finos e sai mais fácil.
<!-- /GERADO -->

Como ligar tudo o que está nesta lista: [LIGACAO.md](LIGACAO.md). Como imprimir: [IMPRIMIR.md](IMPRIMIR.md).
