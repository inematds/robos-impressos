# Ligação elétrica do robô quadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**Não testado na bancada.** Este esquema saiu das fichas dos componentes; nenhum fio foi ligado ainda num robô montado.
Confira cada ligação com o multímetro antes de ligar a chave. Se a sua placa trouxer um nome impresso diferente do
que está aqui, vale o nome da placa.

![Esquema de ligação do robô quadrado de mesa: bateria, fusível, placa de proteção, carregador, chave, conversores, Arduino com Sensor Shield, servos, Raspberry Pi e tela](ligacao.pt.svg)

Página com o mesmo esquema: https://inematds.github.io/robos-impressos/guia/cubo/#energia

## Segurança com bateria de lítio

- **Polaridade:** vermelho no positivo, preto no negativo. Meça com o multímetro antes de cada ligação nova. Fio invertido queima a placa na hora.
- **Ajuste antes de ligar a carga:** LM2596 em 5,1 V e UBEC em 6 V, medidos com o multímetro, sem o Raspberry Pi, sem o Arduino e sem os servos ligados.
- **Curto pega fogo:** solde com as células FORA do suporte e isole cada emenda com termo-retrátil. Nenhum metal pode ficar à mostra.
- **Fusível:** 5 A, no fio positivo, a poucos centímetros do suporte das baterias.
- **Células iguais:** as duas 18650 da mesma marca, do mesmo modelo e novas. Célula amassada, inchada ou quente vai para a coleta de pilhas, não para o robô.
- **Primeira carga:** fique por perto, com o robô sobre uma superfície que não queima.

## O que alimenta o quê

- **Pack 2S:** duas células 18650 em série, de 6 V (vazio) a 8,4 V (cheio). Passa pelo fusível e pela placa de proteção (BMS).
- **Carregador USB-C:** fica ligado na saída da placa de proteção, antes da chave. O robô carrega desligado, por uma fonte USB-C de 15 W ou mais.
- **Chave:** corta o positivo que vai para os dois conversores.
- **LM2596, ajustado em 5,1 V:** alimenta o Raspberry Pi (pelo adaptador USB-C com bornes) e o Arduino (pelo pino de 5 V do Sensor Shield).
- **UBEC em 6 V:** alimenta só os 2 servos, pelo borne azul do Sensor Shield, com o jumper SEL retirado.
- **Negativo (GND):** é um só para o robô inteiro.

Por que o Arduino recebe os 5,1 V do LM2596, e não a tensão da bateria: a entrada VIN do Arduino Uno pede de 7 a 12 V
([ficha do Arduino Uno R3](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)) e o pack passa boa
parte da descarga abaixo de 7 V.

## Tabela de ligações, fio a fio

<!-- GERADO:ligacoes -->
### Bateria, proteção e carga

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Suporte das baterias: fio vermelho (positivo do pack) | Porta-fusível de 5 A e, depois dele, ilha B+ da placa de proteção | vermelho | 22 AWG | O fusível fica a poucos centímetros do suporte. |
| Suporte das baterias: fio preto (negativo do pack) | Ilha B− da placa de proteção | preto | 22 AWG |  |
| Suporte das baterias: lâmina de metal que une as 2 células (ponto do meio) | Ilha BM da placa de proteção | amarelo | 22 AWG | É o 3º fio. Solde-o na lâmina com as células FORA do suporte. |
| Ilha BM da placa de proteção | Carregador USB-C: borne do meio (ponto do meio do pack) | amarelo | 22 AWG | Sem este fio o carregador não equilibra as duas células. |
| Carregador USB-C: saída positiva | Ilha P+ da placa de proteção | vermelho | 22 AWG | O carregador fica antes da chave: o robô carrega desligado. |
| Carregador USB-C: saída negativa | Ilha P− da placa de proteção | preto | 22 AWG |  |

### Chave e conversores

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Ilha P+ da placa de proteção | Chave liga/desliga e, depois dela, entrada IN+ do LM2596 e fio vermelho de entrada do UBEC | vermelho | 22 AWG | A chave corta só o positivo. |
| Ilha P− da placa de proteção | Entrada IN− do LM2596 e fio preto de entrada do UBEC | preto | 22 AWG | Este é o negativo comum (GND) de todo o robô. |

### 5 V: Raspberry Pi e Arduino

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Saída OUT+ do LM2596 (5,1 V) | Pelo pescoço, até o borne + do adaptador USB-C, que entra na porta USB-C do Raspberry Pi | vermelho | 22 AWG | Ajuste os 5,1 V ANTES de ligar este fio. |
| Saída OUT− do LM2596 | Pelo pescoço, até o borne − do adaptador USB-C | preto | 22 AWG |  |
| Saída OUT+ do LM2596 (5,1 V) | Pino de 5 V do Sensor Shield (o + do conector COM ou IIC) | vermelho | Dupont | É por aqui que o Arduino recebe energia. Antes, com o Uno só na USB e o jumper SEL retirado, confirme com o multímetro que esse pino marca cerca de 5 V e que o pino V do D9 marca 0 V. Um pino errado aqui põe os 6 V dos servos no Raspberry Pi. |
| Saída OUT− do LM2596 | Pino − (GND) do mesmo conector do Sensor Shield | preto | Dupont |  |

### 6 V: servos

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Fio vermelho de saída do UBEC (6 V) | Borne azul VCC do Sensor Shield | vermelho | fio do UBEC | Jumper SEL do shield RETIRADO e jumper do UBEC em 6 V. |
| Fio preto de saída do UBEC | Borne azul GND do Sensor Shield | preto | fio do UBEC |  |
| Capacitor de 1000 µF: perna comprida (+) | Borne azul VCC; a perna da listra (−) vai no borne azul GND | sem fio | pernas do capacitor | Capacitor invertido estoura. |
| Servo de pan (na base) | Conector D9 do Sensor Shield | cabo do servo | cabo de 3 fios do servo | G = marrom ou preto, V = vermelho, S = laranja ou amarelo. |
| Servo de tilt (na cabeça) | Pelo pescoço, com a extensão de 30 cm, até o conector D10 do Sensor Shield | cabo do servo | cabo de 3 fios do servo | Mesma ordem de cores do D9. |

### Serial entre o Raspberry Pi e o Arduino

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Raspberry Pi: pino 32 (GPIO12, TX) | Pelo pescoço, até o pino S do D0 (RX) do Sensor Shield | verde | Dupont | Direto: os 3,3 V do Pi já valem como nível alto para o Arduino. |
| Pino S do D1 (TX) do Sensor Shield | Resistor de 1 kΩ e, depois dele, pelo pescoço até o pino 33 (GPIO13, RX) do Raspberry Pi | azul | Dupont | Nunca ligue o D1 direto no Pi: são 5 V num pino de 3,3 V. |
| Ponto entre o resistor de 1 kΩ e o fio azul | 2 resistores de 1 kΩ em série e, depois deles, um pino G (GND) do Sensor Shield | preto | pernas dos resistores | Os 3 resistores formam o divisor: 5 V viram 3,3 V. |
| Raspberry Pi: pino 34 (GND) | Pelo pescoço, até um pino G (GND) do Sensor Shield | preto | Dupont |  |
| Tela MPI3501 | Encaixada nos pinos 1 a 26 do Raspberry Pi | sem fio | conector da própria tela | Usa SPI e os 5 V dos pinos 2 e 4. |
<!-- /GERADO -->

## Preparo 1: solde a energia e ajuste as duas tensões

Faça na bancada, antes de montar o robô, com a base impressa ao lado servindo de gabarito do comprimento dos fios.

1. Solde o 3º fio (amarelo) na lâmina de metal que une as duas células, com as células fora do suporte.
2. Ligue o suporte, o fusível, a placa de proteção e o carregador, conforme a tabela.
3. Encaixe a chave no recorte da base, por fora, com os fios passando pelo recorte, e solde-a no positivo.
4. Ligue as entradas do LM2596 e do UBEC. Deixe as saídas soltas, sem nada ligado.
5. Ponha as células no suporte, conferindo o lado do positivo, e ligue a chave.
6. Com o multímetro na saída do LM2596, gire o parafuso de ajuste com a chave de fenda até marcar 5,1 V. São várias voltas.
7. Meça a saída do UBEC: tem de marcar 6 V. Se marcar 5 V, mude o jumper dele para 6 V.
8. Desligue a chave.

## Preparo 2: grave o programa e ponha os 2 servos em 90°

O programa é o sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). Ele leva os dois servos para
o centro e os mantém lá.

1. Abra o sketch na Arduino IDE. Ligue o Arduino Uno ao computador pelo cabo USB, sem o shield e sem bateria.
2. Em Ferramentas, escolha a placa Arduino Uno e a porta em que ela apareceu. Clique em Carregar.
3. Tire o cabo USB, encaixe o Sensor Shield no Uno e retire o jumper SEL do shield.
4. Ligue o cabo USB de novo, só para medir com o multímetro: o pino de 5 V que você vai usar no shield (o + do conector COM ou IIC) tem de marcar cerca de 5 V, e o pino V do D9 tem de marcar 0 V.
5. Se o V do D9 marcar 5 V, o jumper SEL ainda está posto. Se o pino de 5 V marcar 0 V, escolha outro pino + e meça de novo. Um pino errado aqui põe os 6 V dos servos no Raspberry Pi.
6. Tire o cabo USB.
7. Ligue os 6 V do UBEC no borne azul (VCC e GND) e o capacitor de 1000 µF no mesmo borne.
8. Ligue os 5,1 V do LM2596 no pino de 5 V do shield e o negativo num pino G.
9. Ligue o servo de pan no D9 e o servo de tilt no D10.
10. Ligue a chave: os dois servos vão para o centro (90°) e o LED do Uno pisca uma vez por segundo.
11. Desligue. Daqui em diante não gire os eixos dos servos com a mão.

Três avisos:

- Não alimente o servo MG996R pelos 5 V da USB. A porta USB dá 0,5 A e o servo pede mais do que isso ao partir.
- Nunca ligue o cabo USB do computador com a bateria ligada: as duas fontes ficariam em paralelo.
- Grave o sketch antes de parafusar o Uno na base. Com ele no lugar sobram cerca de 10 mm entre o conector USB e a parede, e o cabo não entra.

O sketch compila para o Arduino Uno (arduino-cli, core arduino:avr 1.8.8, biblioteca Servo 1.3.0). Ele ainda não foi
rodado num robô montado.

## Preparo 3: grave o cartão microSD e instale o driver da tela

1. Grave o cartão com o Raspberry Pi Imager, o programa gratuito da Raspberry Pi. Escolha o modelo do seu Pi, o sistema Raspberry Pi OS (64-bit) e o cartão.
2. Antes de gravar, abra as configurações do Imager: defina usuário, senha e Wi-Fi e ative o SSH. Assim você acessa o Pi pela rede, sem teclado.
3. A tela é a MPI3501: 3,5 polegadas, 480 × 320, controlador ILI9486, ligada por SPI nos pinos 1 a 26. Ela só acende depois de instalado o driver.
4. O fabricante indica o pacote LCD-show. No Pi, pela rede, rode os três comandos abaixo.

```
git clone https://github.com/goodtft/LCD-show.git
cd LCD-show
sudo ./LCD35-show
```

Fonte do modelo, dos pinos e do driver: [página da MPI3501 na lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display).
O script troca o arquivo de configuração do Pi e reinicia. Não testado na bancada: o fabricante lista testes até o
Raspberry Pi 3B+; no Pi 4 e no Pi 5 pode ser preciso ajustar.

## Como o Raspberry Pi conversa com o Arduino

O Raspberry Pi fica na cabeça e o Arduino na base. O furo de cabos do pescoço tem 9 mm e um plugue USB não passa por
ele. Por isso os dois conversam por uma serial (UART) de 3 fios soltos, que passam pelo furo.

- **No Arduino:** pinos D0 (RX) e D1 (TX), que são a serial de verdade da placa. Ela não atrapalha o sinal dos servos.
- **No Raspberry Pi:** pino 32 (GPIO12, TX), pino 33 (GPIO13, RX) e pino 34 (GND). A tela ocupa os pinos 1 a 26; estes três ficam livres.
- **Tensão:** o Arduino trabalha em 5 V e o Pi em 3,3 V. O fio que vai do Arduino para o Pi passa por um divisor de 3 resistores de 1 kΩ, que baixa 5 V para 3,3 V. O fio que vai do Pi para o Arduino é direto.
- **Por que resistores e não um módulo conversor de nível:** o módulo pede uma referência de 3,3 V, e os pinos de 3,3 V do Pi ficam embaixo da tela.

Como montar o divisor: solde um resistor de 1 kΩ no fio que sai do D1. Na outra perna dele, solde o fio azul que sobe
para o pino 33 do Pi e mais dois resistores de 1 kΩ em série, que terminam num pino G do shield. Cubra tudo com
termo-retrátil.

Como ligar no Pi: os pinos 31 a 34 ficam embaixo da placa da tela, onde sobram cerca de 17,5 mm (medida não
confirmada). O conector Dupont comum, de 14 mm, não cabe em pé. Corte um pedaço de 2 × 2 da barra de pinos fêmea,
solde os 3 fios de lado nos terminais dele e encaixe nos pinos 31 a 34 antes de pôr a tela.

Para ligar a serial no sistema do Pi, acrescente uma linha no fim do arquivo `/boot/firmware/config.txt`, DEPOIS de
instalar o driver da tela, porque o script do driver reescreve esse arquivo:

- Raspberry Pi 4: `dtoverlay=uart5`
- Raspberry Pi 5: `dtoverlay=uart4-pi5`

Fonte: [lista de overlays do firmware do Raspberry Pi](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
Depois de reiniciar, veja o nome da porta com `ls /dev/ttyAMA*`. Não testado na bancada. O programa que usa essa
serial é da fase 2.

## Os 8 fios que passam pelo pescoço

Passe os fios pelo furo de 9 mm antes de fechar a cabeça sobre o tubo, nesta ordem:

1. A extensão do servo de tilt: o conector de 3 pinos tem 7,6 mm de largura e passa justo.
2. Os 2 fios de 5,1 V do Raspberry Pi (vermelho e preto). O adaptador USB-C é parafusado neles depois.
3. Os 3 fios da serial (verde, azul e preto).

Deixe cerca de 10 cm de folga dentro da base: o pescoço gira quase uma volta e torce os fios.

## Corrente, fio e fusível

Os valores abaixo são calculados a partir das fichas, não medidos.

- Uso normal: cerca de 2 A saindo do pack (Raspberry Pi com cerca de 1 A em 5 V e servos com menos de 1 A em 6 V).
- Pior caso: cerca de 6 A, com o LM2596 e o UBEC nos 3 A de limite e o pack em 6,5 V.
- Fio 22 AWG (0,33 mm²) em toda a parte de energia. No trecho do pescoço, com 2 A, a queda calculada é de 0,1 V: por isso o ajuste é 5,1 V e não 5,0 V.
- Fusível de 5 A: fica acima do uso normal e abaixo dos 10 A da placa de proteção.
- Chave KCD11: em geral é de 3 A (medida não confirmada; leia o valor gravado no corpo da sua).
- O programa da fase 2 não pode deixar os dois servos forçando ao mesmo tempo no fim do curso.

## Primeira vez que você liga o robô montado

1. Chave desligada. Confira com o multímetro que não há continuidade entre o positivo e o negativo do pack.
2. Ligue a chave. Meça 5,1 V no adaptador USB-C, ainda fora do Pi, e 6 V no borne azul.
3. Desligue, encaixe o adaptador USB-C no Raspberry Pi e ligue de novo.
4. O LED do Arduino pisca, os dois servos seguram o centro e o LED de energia do Raspberry Pi acende.

## O que ainda não foi testado

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

O que comprar: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md). Como imprimir: [IMPRIMIR.md](IMPRIMIR.md).
