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
- **Fusível:** 3 A, no fio positivo, a poucos centímetros do suporte das baterias.
- **Células iguais:** as duas 18650 da mesma marca, do mesmo modelo e novas. Célula amassada, inchada ou quente vai para a coleta de pilhas, não para o robô.
- **Primeira carga:** fique por perto, com o robô sobre uma superfície que não queima.

## O que alimenta o quê

- **Pack 2S:** duas células 18650 em série, de 6 V (vazio) a 8,4 V (cheio). Passa pelo fusível e pela placa de proteção (BMS).
- **Carregador USB-C:** fica ligado na saída da placa de proteção, antes da chave. O robô carrega desligado, por uma fonte USB-C de 15 W ou mais.
- **Chave:** corta o positivo que vai para os dois conversores.
- **LM2596, ajustado em 5,1 V:** alimenta o Raspberry Pi (pelo adaptador USB-C com bornes) e o Arduino (pelo pino 5V do conector POWER do Sensor Shield).
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
| Suporte das baterias: fio vermelho (positivo do pack) | Porta-fusível de 3 A e, depois dele, ilha B+ da placa de proteção | vermelho | 22 AWG | O fusível fica a poucos centímetros do suporte. |
| Suporte das baterias: fio preto (negativo do pack) | Ilha B− da placa de proteção | preto | 22 AWG |  |
| Suporte das baterias: lâmina de metal que une as 2 células (ponto do meio) | Ilha do meio da placa de proteção (BM ou B1) | amarelo | 22 AWG | É o 3º fio. Solde-o na lâmina com as células FORA do suporte. |
| Ilha do meio da placa de proteção (BM ou B1) | Ilha BM do carregador USB-C | amarelo | 22 AWG | Sem este fio o carregador não equilibra as duas células. |
| Ilha B+ do carregador USB-C | Saída positiva da placa de proteção (P+; se a placa não tiver P+, é a própria ilha B+) | vermelho | 22 AWG | O carregador fica antes da chave: o robô carrega desligado. |
| Ilha B− do carregador USB-C | Saída negativa da placa de proteção (P− ou C−) | preto | 22 AWG | Não ligue na ilha B− da placa de proteção: a carga tem de passar pela proteção. |

### Chave e conversores

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Saída positiva da placa de proteção (P+ ou B+) | Chave liga/desliga e, depois dela, entrada IN+ do LM2596 e fio vermelho de entrada do UBEC | vermelho | 22 AWG | A chave corta só o positivo. |
| Saída negativa da placa de proteção (P− ou C−) | Entrada IN− do LM2596 e fio preto de entrada do UBEC | preto | 22 AWG | Este é o negativo comum (GND) de todo o robô. |

### 5 V: Raspberry Pi e Arduino

| De | Para | Cor | Fio | Atenção |
|---|---|---|---|---|
| Saída OUT+ do LM2596 (5,1 V) | Barra de emenda na base e, dela, pelo pescoço, até o borne + do adaptador USB-C, que entra na porta USB-C do Raspberry Pi | vermelho | 20 AWG | Ajuste os 5,1 V ANTES de ligar este fio. Fio curto e grosso: fio fino faz o Pi acusar subtensão. |
| Saída OUT− do LM2596 | Barra de emenda na base e, dela, pelo pescoço, até o borne − do adaptador USB-C | preto | 20 AWG |  |
| Saída OUT+ do LM2596 (5,1 V) | Pino 5V do conector POWER do Sensor Shield | vermelho | Dupont | É por aqui que o Arduino recebe energia. Antes, com o Uno só na USB e o jumper SEL retirado, confirme com o multímetro que esse pino marca cerca de 5 V e que o pino V do D9 marca 0 V. Um pino errado aqui põe os 6 V dos servos no Raspberry Pi. |
| Saída OUT− do LM2596 | Pino GND do conector POWER do Sensor Shield | preto | Dupont |  |

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
2. Ligue o suporte, o fusível, a placa de proteção e o carregador, conforme a tabela. Os nomes das ilhas mudam de placa para placa: na placa de proteção da loja consultada são B+, B1 (meio), B− e C− (saída negativa); no carregador são B+, BM e B−.
3. Encaixe a chave no recorte da base, por fora, com os fios passando pelo recorte, e solde-a no positivo.
4. Ligue as entradas do LM2596 e do UBEC. Na saída do LM2596, solde 2 fios curtos (20 AWG) que terminam na barra de emenda. Não ligue mais nada nas saídas.
5. Ponha as células no suporte, conferindo o lado do positivo, e ligue a chave.
6. Com o multímetro na saída do LM2596, gire o parafuso de ajuste com a chave de fenda até marcar 5,1 V. São várias voltas.
7. Meça a saída do UBEC: tem de marcar 6 V. Se marcar 5 V, mude o jumper dele para 6 V.
8. Desligue a chave.

## Preparo 2: grave o programa e ponha os 2 servos em 90°

O programa é o sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). Ele leva os dois servos para
o centro e os mantém lá.

1. Abra o sketch na Arduino IDE. Ligue o Arduino Uno ao computador pelo cabo USB, sem o shield e sem bateria.
2. Em Ferramentas, escolha a placa Arduino Uno e a porta em que ela apareceu. Clique em Carregar.
3. Tire o cabo USB, encaixe o Sensor Shield no Uno e retire o jumper SEL do shield: é a capinha de plástico sobre 2 pinos, ao lado do borne azul.
4. Ligue o cabo USB de novo, só para medir com o multímetro: o pino 5V do conector POWER do shield tem de marcar cerca de 5 V, e o pino V do D9 tem de marcar 0 V.
5. Se o V do D9 marcar 5 V, o jumper SEL ainda está posto. Se o seu shield não tiver o conector POWER, use o pino + do conector COM e meça do mesmo jeito. Um pino errado aqui põe os 6 V dos servos no Raspberry Pi.
6. Tire o cabo USB.
7. Ligue os 6 V do UBEC no borne azul (VCC e GND) e o capacitor de 1000 µF no mesmo borne.
8. Ligue os 5,1 V do LM2596 no pino 5V do conector POWER do shield e o negativo no pino GND do mesmo conector.
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

O cartão é gravado no seu computador, com um leitor de cartão microSD. Depois você fala com o Raspberry Pi pela rede,
por SSH: digita os comandos no seu computador e eles rodam no Pi.

1. Instale no computador o Raspberry Pi Imager, o programa gratuito da Raspberry Pi, e ponha o cartão no leitor.
2. No Imager, escolha o modelo do seu Pi, o sistema Raspberry Pi OS (64-bit) e o cartão.
3. Antes de gravar, abra as configurações do Imager: dê um nome ao Pi (por exemplo `robo`), crie um usuário e uma senha, ponha o nome e a senha do seu Wi-Fi e ative o SSH. Grave.
4. Ponha o cartão no Pi, encaixe a tela nos pinos 1 a 26 só para este teste e ligue o Pi por uma fonte USB-C de 5 V e 3 A. Espere uns 2 minutos.
5. No computador, abra o terminal: no Windows é o programa PowerShell; no Mac e no Linux, o Terminal.
6. Digite `ssh usuario@robo.local`, trocando `usuario` e `robo` pelos nomes que você criou. Responda `yes` na primeira vez e digite a senha.
7. Se `robo.local` não responder, abra a página do seu roteador, ache o Pi na lista de aparelhos ligados e use o número dele (o endereço IP), por exemplo `ssh usuario@192.168.0.50`.
8. Quando o terminal mostrar o nome do Pi, você está dentro dele. Digite os três comandos abaixo, um por linha, com Enter depois de cada um. O Pi precisa estar na internet.

```
git clone https://github.com/goodtft/LCD-show.git
cd LCD-show
sudo ./LCD35-show
```

O Pi reinicia sozinho e a tela acende. Depois desligue o Pi com `sudo poweroff`, espere o LED verde parar e tire a tela para a montagem.

A tela é a MPI3501: 3,5 polegadas, 480 × 320, controlador ILI9486, ligada por SPI nos pinos 1 a 26. Fontes:
[página da MPI3501 na lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display) (modelo, pinos e driver) e
[documentação da Raspberry Pi](https://www.raspberrypi.com/documentation/computers/remote-access.html) (SSH).
Não testado na bancada: o fabricante lista testes até o Raspberry Pi 3B+, e o script troca o arquivo de configuração do Pi.

Plano B, também não testado, se a tela ficar branca ou apagada:

- Em vez do script, acrescente a linha `dtoverlay=piscreen,drm` ao fim do arquivo `/boot/firmware/config.txt` e reinicie. É o overlay oficial para uma tela de 3,5 polegadas com o mesmo controlador ILI9486 ([lista de overlays](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README)); a fonte não garante que sirva na MPI3501.
- Se ainda assim não acender, grave o cartão de novo com o Raspberry Pi OS (Legacy) e repita o script do fabricante.

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

São 8 fios: 2 de energia (5,1 V do Raspberry Pi, 20 AWG), 3 da serial e os 3 do cabo do servo de tilt. Eles têm de ser
ligados dentro da cabeça ANTES do copo, porque depois o Raspberry Pi fica fechado. E não podem ficar pendurados por
baixo do garfo nessa hora, porque o fundo do copo passa por baixo dele. A ordem é esta:

1. Com a cabeça ainda aberta (quadro, tela, servo de tilt e garfo no lugar), parafuse os 2 fios de 5,1 V no adaptador USB-C e encaixe-o no Raspberry Pi.
2. Confira o conector baixo da serial nos pinos 31 a 34. Ele entra antes da tela, já com os 3 fios soldados.
3. Ligue a extensão de 30 cm no cabo do servo de tilt.
4. Desça os 8 fios pelo furo de 9 mm do garfo, de cima para baixo. Primeiro o conector da extensão, que tem 7,6 mm de largura e passa justo.
5. Pare quando as pontas ficarem rentes à face de baixo do garfo. Deixe uns 5 cm de fio sobrando dentro da cabeça: ela inclina em volta do garfo.
6. Feche a cabeça com o copo. Com a pinça, puxe as pontas dos 8 fios para fora pelo rasgo do fundo do copo.
7. Enfie os fios pelo tubo do pescoço e assente a cabeça sobre ele.
8. Na base, com a chave desligada: os 2 fios de 5,1 V na barra de emenda, a extensão no D10 e os 3 da serial conforme a tabela.

Deixe cerca de 10 cm de folga dentro da base: o pescoço gira quase uma volta e torce os fios. Esta passagem nunca foi
ensaiada com as peças impressas.

## Corrente, fio e fusível

Os valores abaixo são calculados a partir das fichas, não medidos.

- Uso normal: cerca de 2 A saindo do pack. O Raspberry Pi puxa cerca de 1 A em 5,1 V e os servos menos de 1 A em 6 V.
- Pico: cerca de 5 A, com o LM2596 em 2 A, o UBEC nos 3 A de limite e o pack em 6,5 V.
- Chave KCD11-101: 3 A em 250 V~ e 6 A em 125 V~ ([ficha de loja](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). A ficha não traz valor para corrente contínua.
- Fusível de 3 A: é o menor valor da chave. O uso normal fica abaixo dele. Um pico de segundos não o abre; uma sobrecarga que dura abre o fusível antes de a chave esquentar (comportamento usual de fusível de vidro, medida não confirmada).
- Se o fusível abrir com o robô em uso normal, não ponha um maior: meça a corrente e procure o que está forçando.
- Fio 22 AWG (0,33 mm²) na energia da base. Fio 20 AWG (0,5 mm²) no par de 5,1 V que sobe até o Raspberry Pi: com 2 A, a queda calculada nesse trecho é de 0,06 V.
- O LM2596 aguenta cerca de 2 A contínuos sem dissipador (valor usual, medida não confirmada). Use o Raspberry Pi 4, ou o Pi 5 sem acessórios USB.
- Se o Raspberry Pi acusar subtensão, encurte o par de 5,1 V e confira o ajuste. Para ver, digite `vcgencmd get_throttled` no Pi: a resposta boa é `throttled=0x0`.
- O programa da fase 2 não pode deixar os dois servos forçando ao mesmo tempo no fim do curso.

## Primeira vez que você liga o robô montado

1. Chave desligada. Com o multímetro em continuidade, confira que o positivo e o negativo do pack não estão em curto.
2. Antes de emendar os 2 fios que descem do Raspberry Pi, ligue a chave e meça na barra de emenda, do lado do conversor: 5,1 V, com o vermelho no positivo. Meça 6 V no borne azul. Desligue.
3. Emende os fios do Pi na barra, vermelho com vermelho e preto com preto, e ligue a chave de novo.
4. O LED do Arduino pisca, os dois servos seguram o centro, o LED de energia do Raspberry Pi acende e, em cerca de 1 minuto, a tela mostra o sistema.
5. Se nada acender, desligue e confira o fusível.

## O que ainda não foi testado

<!-- GERADO:riscos -->
- Nada foi impresso nem montado ainda. A parte elétrica desta página não foi testada na bancada: ela saiu das fichas dos componentes.
- Os arquivos 3MF das mesas nunca foram abertos no Bambu Studio. Se algum não abrir, use os STL.
- O plugue USB-C que alimenta o Raspberry Pi não está no modelo 3D. Pode não haver espaço para ele ao lado do Pi, dentro da cabeça.
- Os pinos 31 a 34 do Raspberry Pi ficam embaixo da placa da tela. A folga ali (17,5 mm no modelo) é uma medida não confirmada: se o conector baixo não couber, os 3 fios da serial terão de ser soldados.
- O cupom de teste não confere a janela do servo MG996R nem a rosca do parafuso M5. A janela do servo você confere no quadro da cabeça (mesa 01). A rosca do M5 fica no braço do garfo (mesa 03). As duas saem antes das impressões longas.
- Com o Arduino parafusado na base, o cabo USB não entra: sobram cerca de 10 mm até a parede. Para regravar o programa é preciso soltar os 4 parafusos dele.
- O porta-fusível, a barra de emenda e os 3 resistores da serial não têm lugar modelado: ficam soltos nos fios, isolados com termo-retrátil.
- As medidas marcadas como NC vêm de anúncios de loja. Meça a sua peça antes de imprimir a parte que encosta nela.
- A passagem dos 8 fios pelo furo do garfo e pelo rasgo do fundo da cabeça nunca foi ensaiada com as peças impressas.
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
- **SSH:** Jeito de usar o Raspberry Pi pela rede: você digita os comandos no terminal do seu computador e eles rodam no Pi, sem ligar teclado nem monitor nele.
- **SPI:** Ligação de dados por poucos fios, com um relógio que marca o passo. É por ela que o Raspberry Pi manda a imagem para a tela.
- **UART (serial):** Ligação de dados simples: um fio para falar (TX) e um para ouvir (RX). É por ela que o Raspberry Pi manda ordens ao Arduino.
- **Jumper SEL:** Capinha de plástico sobre 2 pinos do Sensor Shield, ao lado do borne azul, com a marca SEL. Posta, ela liga os 5 V do Arduino aos conectores dos servos. Retirada, os servos recebem só o que entra pelo borne azul.
- **Borne:** Conector de parafuso: o fio entra no furo e o parafuso aperta. No Sensor Shield é o bloco azul marcado GND e VCC.
<!-- /GERADO -->

O que comprar: [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md). Como imprimir: [IMPRIMIR.md](IMPRIMIR.md).
