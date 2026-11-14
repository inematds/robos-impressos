# Plano — robos-impressos (fase 1: mecânica e encaixe)

Três robôs impressos em 3D numa **Bambu Lab A1** (mesa de 256 × 256 × 256 mm), com as peças geradas por código:

| Modelo | O que é | Como se move |
|---|---|---|
| **Dinossauro** (`dino`) | filhote cartoon, ~33 cm | roda (2 motores TT escondidos nas pernas + esfera sob a cauda); pescoço vira e inclina, boca abre, 2 braços |
| **Capivara** (`capivara`) | filhote sentado, ~33 cm, bandana verde | roda (rodas dentro das coxas, aro ciano na lateral; esfera dentro do rabo); pescoço vira e inclina, boca abre |
| **Robô quadrado** (`cubo`) | cabeça-cubo com tela de 3,5", de mesa, ~20 cm | não roda; a cabeça gira ±170° e inclina |

**Fase 1 = só mecânica:** peças, encaixes, lugar de cada componente, parafusos. Nada de fiação, firmware ou IA.
**Nada disto foi impresso nem montado ainda.** O que existe é um protótipo digital conferido por script
(`cad/verificar.py`). Tempo, filamento e preço são **estimativas**. As imagens do guia são renders das peças, não fotos.

Por que o repo se chama `robos-impressos` e não `dinobot`: o pedido começou com o dinossauro e virou três modelos
que dividem as mesmas peças e o mesmo verificador. Um nome neutro evita ter uma capivara dentro de um "dinobot".

<!-- TABELA:resumo -->
| Modelo | Altura (mm) | Peças | Mesa (1 mesa = 1 impressão) | Filamento total (g)* | Impressão total (h)* | Robô montado (g)* |
|---|---|---|---|---|---|---|
| Dinossauro | 329 | 38 | 12 | 1108 | 44 | 1668 |
| Capivara | 326 | 39 | 13 | 1050 | 42 | 1583 |
| Robô quadrado | 201 | 14 | 8 | 638 | 25 | 1020 |

* estimativa por volume, sem fatiador
<!-- /TABELA -->

---

## 1. Decisões de projeto (e o porquê)

### 1.1 Locomoção: rodar. Andar fica como variante futura

| Opção | Avaliação para um boneco de ~33 cm com cabeça grande |
|---|---|
| **Rodar (escolhida)** | 2 motores TT + rodas de 65 mm, tração diferencial, 3º apoio numa esfera. Funciona sem sensor, aguenta ~1,7 kg, peças de R$ 15. |
| Andar com servos | Bípede de cabeça pesada precisa de 6 a 10 servos fortes e controle de equilíbrio. Cai com facilidade e gasta engrenagem. Ruim para "fase 1 confiável". |
| Rodar + andar | A fase 1 não constrói pernas que andam. As pernas/coxas são **cascas presas por 2 parafusos nas asas do piso**: uma perna articulada futura usa os mesmos 2 furos. |

- **Onde ficam as rodas:** dentro das pernas do dino e das coxas da capivara, com 3 mm de vão até o chão.
  O motor TT fica **em pé**, aparafusado por fora na parede do rack; a roda sai pela lateral.
- **3º apoio:** esfera de 16 mm num soquete na ponta da lança do chassi, coberta pela cauda (dino) ou pelo rabo (capivara).
- **Centro de gravidade (calculado pelo verificador, com massas estimadas):** no dino fica 26 mm atrás do eixo das
  rodas e 118 mm acima do chão (capivara: 25 e 117 mm). O robô só tomba para a frente depois de ~12° de inclinação
  (~10° com a cabeça toda para baixo), e antes disso os dedos/patas (3 mm acima do chão, ~69 mm à frente do eixo)
  encostam e seguram. Para chegar nisso o corpo foi recuado 16 mm em relação às rodas (a primeira versão tinha só 15 mm de margem).
- **Largura:** ~204 mm entre as faces de fora das pernas. É o preço de usar roda de 65 mm com motor TT e um rack de 58 mm
  entre eles. Motor N20 com roda de 43 mm deixaria o robô ~40 mm mais estreito, mas é menos comum e mais fraco; fica como troca possível.

### 1.2 Movimentos que a fase 1 já deixa prontos

| Movimento | Dino | Capivara | Cubo | Servo | Faixa conferida sem colisão |
|---|---|---|---|---|---|
| Pescoço para os lados (pan) | sim | sim | sim | MG996R | bichos ±60°; cubo ±170° |
| Pescoço para cima/baixo (tilt) | sim | sim | sim | MG996R | bichos −15° a +20°; cubo −25° a +30° |
| Boca | sim | sim | — (boca é desenhada na tela) | SG90 ou MG90S | 0 a 18° |
| Braços | 2 | parados (parte da casca) | — | SG90 ou MG90S | −15° a +40° (até +70° com a cabeça reta) |
| Cauda | fixa (é o 3º apoio) | fixa | — | — | — |

- **Junta do pescoço dos bichos = esfera.** O topo do torso é uma esfera de 58 mm de raio e a cabeça é um "capacete"
  com 2 mm de folga em volta dela. Como a esfera é a mesma para pan e tilt, a folga não muda quando a cabeça mexe e
  não aparece pescoço. Dentro da esfera ficam o garfo (gira com o pan) e o berço (inclina com o tilt).
- **Tilt com servo padrão (MG996R), não micro servo:** a cabeça impressa pesa ~330 g (estimativa por volume), mais os
  servos. Um MG90S seguraria parada, mas trabalharia perto do limite.
- **Cubo: 360° ou limitado?** Avaliado: (a) servo de rotação contínua não sabe onde está; (b) motor de passo + anel
  coletor (slip ring) exige sensor de zero, driver e passa a alimentação do Pi por contatos de 2 A; (c) servo de 270°
  resolve, mas as abas do DS3218 não têm medida confirmada. **Escolhido:** servo comum de 180° com **engrenagens
  impressas 2:1** (44 dentes no servo, 22 no pescoço, módulo 1,5). O pescoço gira ±170° sabendo a posição, e os cabos
  sobem por dentro do **tubo oco do pescoço** (furo de 14 mm), torcendo no máximo meia volta para cada lado.
  Giro contínuo com anel coletor fica como variante: o tubo oco já é o lugar dele.

### 1.3 Esqueleto separado da casca

- **Bichos:** o **chassi** (uma peça só, PETG) é piso + rack + deck. Ele segura motores, bateria, placas e o servo de pan.
  As cascas (PLA) só cobrem: saem todas sem desmontar o esqueleto.
- **Mesmo esqueleto nos dois bichos:** chassi, bandejas, garfo, berço, capa da esfera, pinos e bucha são **os mesmos STL**
  (`pecas/comum/`). Só a casca e a mesa da cabeça mudam.
- **Cubo:** a base é caixa e estrutura ao mesmo tempo; a cabeça tem um **quadro** interno (PETG) que segura o Pi, o servo
  de tilt e o eixo, e a casca branca entra por trás.

### 1.4 Onde ficam Arduino Uno e Raspberry Pi

- **Bichos: rack de bandejas deslizantes.** Entre as duas paredes do chassi (58 mm) há 2 trilhos. Cada bandeja
  (`bandeja-uno`, `bandeja-pi`) tem o mesmo contorno e entra em qualquer trilho, por trás, travada por 1 parafuso M3.
  Na fase 1 usa-se uma; na fase 2 as duas ao mesmo tempo (Uno + shield embaixo, Pi em cima). A bateria passa por baixo.
- **Acesso:** tirando a cauda ou o rabo (2 parafusos por baixo) e o `torso-costas` (3 parafusos), as bandejas saem por trás sem mexer no resto. As pernas ficam no lugar: a casca delas foi recortada pelo caminho que as costas fazem ao sair.
- **Limite honesto:** o Pi fica com as portas USB-C/HDMI a 1 mm da parede. Na bandeja ele é alimentado pelos pinos
  de 5 V do GPIO; as USB grandes ficam livres, viradas para trás. Sob o servo de pan sobram 14 mm acima da placa do Pi.
- **Cubo:** Uno + shield no piso da base (USB virado para a porta de trás); Pi dentro da cabeça, atrás da tela.

### 1.5 Bateria e chave

- **Bichos:** baia no piso, 58 × 114 × 23 mm, para suporte 2×18650 (até 78 × 41 × 22). Largura útil de 48 mm na altura
  do eixo dos motores (a ponta interna do eixo entra 4 mm na baia). A bateria entra e sai por trás, inclinada por cima
  da chave, com a bandeja de baixo fora; fica presa pelo batente da frente e por fita dupla-face ou velcro. Chave gangorra KCD11 e furo de 8,2 mm para conector
  de carga P4 ficam **no piso, sob a cauda/rabo** (como em brinquedo: liga por baixo).
- **Cubo:** suporte 2×18650 no piso da base; sai pela **porta traseira** (1 parafuso), que leva a chave e o conector de carga.

### 1.6 Impressão

| Material | Onde | Por quê |
|---|---|---|
| **PETG** | chassi, bandejas, garfo, berço, mesa da cabeça, base/tampa/garfo/quadro/engrenagens do cubo | aguenta parafuso, inserto a quente e calor de motor |
| **PLA** | cascas, olhos, cristas, unhas, painéis | acabamento e cor |
| **TPU** | nenhuma peça nesta versão | pneus já vêm nas rodas; pés de borracha do cubo são comprados |

- Parede das cascas: 2,4 mm nominal. Na geração, o script mede a distância real entre a pele de fora e a de dentro
  (4.000 pontos por casca) e grava no `montagem.json`: **2,35 a 2,42 mm**. O verificador confere esse valor contra o mínimo de 2,0 mm.
- Folga de encaixe: 0,25 mm (parâmetro `FOLGA.encaixe`). Imprima primeiro o `comum-teste-encaixe.stl`
  (janela do micro servo, 3 furos de inserto, furos M3/M2,5/M2, 3 soquetes de pino) e ajuste antes das peças grandes.
- Cascas orgânicas (torso, crânio, mandíbula, painéis) pedem **suporte em árvore**. Pernas, coxas, cauda e rabo só sob as 2 orelhas de parafuso.
- Cada STL já sai deitado na posição de imprimir. `pecas/<modelo>/mesas/` tem um 3MF por mesa (peças juntas por cor e material); a lista está em `mesas.json`.

---

## 2. Peças impressas

Números gerados de `pecas/<modelo>/montagem.json` por `cad/tabelas.py`. Tempo e filamento: volume de plástico ÷ vazão
média de 6 mm³/s (suposição conservadora) e densidade do filamento; peça maciça conta 1,6 mm de casca + 15 % de miolo.
**Não há fatiador nesta máquina: trate como ordem de grandeza** e confira no Bambu Studio. Suportes não entram na conta.

### Dinossauro

<!-- TABELA:pecas:dino -->
| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| torso-frente | 145 × 226 × 96 | 1 | PLA | verde | sim | 122 | 4.7 |
| torso-costas | 145 × 226 × 74 | 1 | PLA | verde | sim | 136 | 5.2 |
| barriga | 79 × 87 × 26 | 1 | PLA | creme | sim | 24 | 1.0 |
| crista-costas | 47 × 27 × 6 | 1 | PLA | azul | não | 5 | 0.3 |
| pino-guia (comum) | 4 × 4 × 9 | 4 | PLA | cinza | não | 0 | 0.3 |
| perna-dir | 60 × 127 × 113 | 1 | PLA | verde | não | 55 | 2.1 |
| perna-esq | 60 × 127 × 113 | 1 | PLA | verde | não | 55 | 2.1 |
| unha | 18 × 18 × 13 | 6 | PLA | creme | não | 13 | 1.0 |
| cauda | 92 × 112 × 69 | 1 | PLA | verde | não | 55 | 2.1 |
| crista-cauda | 26 × 38 × 6 | 1 | PLA | azul | não | 4 | 0.2 |
| cranio | 156 × 184 × 120 | 1 | PLA | verde | sim | 187 | 7.1 |
| mandibula | 116 × 59 × 49 | 1 | PLA | verde | sim | 26 | 1.1 |
| mesa-cabeca | 104 × 138 × 36 | 1 | PETG | grafite | não | 41 | 1.6 |
| crista-cabeca | 61 × 83 × 6 | 1 | PLA | azul | não | 7 | 0.4 |
| olho | 48 × 38 × 48 | 1 | PLA | branco | não | 18 | 0.8 |
| olho-esq | 48 × 38 × 48 | 1 | PLA | branco | não | 18 | 0.8 |
| iris | 29 × 19 × 29 | 1 | PLA | azul | não | 5 | 0.3 |
| iris-esq | 29 × 19 × 29 | 1 | PLA | azul | não | 5 | 0.3 |
| pupila | 17 × 13 × 18 | 1 | PLA | preto | não | 2 | 0.1 |
| pupila-esq | 17 × 13 × 18 | 1 | PLA | preto | não | 2 | 0.1 |
| bucha-eixo (comum) | 7 × 7 × 3 | 1 | PLA | cinza | não | 0 | 0.1 |
| braco-dir | 38 × 73 × 31 | 1 | PLA | verde | sim | 16 | 0.7 |
| braco-esq | 38 × 73 × 31 | 1 | PLA | verde | sim | 16 | 0.7 |
| chassi (comum) | 152 × 190 × 148 | 1 | PETG | grafite | não | 206 | 7.6 |
| capa-esfera (comum) | 29 × 29 × 6 | 1 | PETG | grafite | não | 3 | 0.2 |
| bandeja-uno (comum) | 61 × 90 × 16 | 1 | PETG | amarelo | não | 19 | 0.8 |
| bandeja-pi (comum) | 61 × 90 × 16 | 1 | PETG | amarelo | não | 16 | 0.7 |
| garfo-pescoco (comum) | 65 × 48 × 51 | 1 | PETG | grafite | não | 17 | 0.7 |
| berco-tilt (comum) | 38 × 23 × 77 | 1 | PETG | grafite | sim | 15 | 0.6 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 38 |  |  |  | **1108** | **44** |

* estimativa por volume, sem fatiador
<!-- /TABELA -->

### Capivara

<!-- TABELA:pecas:capivara -->
| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| torso-frente | 156 × 226 × 96 | 1 | PLA | laranja | sim | 133 | 5.0 |
| torso-costas | 156 × 226 × 74 | 1 | PLA | laranja | sim | 139 | 5.3 |
| barriga | 79 × 87 × 29 | 1 | PLA | laranja | sim | 26 | 1.1 |
| bandana-frente | 119 × 47 × 60 | 1 | PLA | verde-bandana | sim | 9 | 0.4 |
| bandana-costas | 119 × 38 × 67 | 1 | PLA | verde-bandana | sim | 10 | 0.5 |
| mao | 20 × 20 × 11 | 2 | PLA | marrom | não | 5 | 0.3 |
| pino-guia (comum) | 4 × 4 × 9 | 4 | PLA | cinza | não | 0 | 0.3 |
| coxa-dir | 46 × 119 × 82 | 1 | PLA | laranja | sim | 38 | 1.5 |
| coxa-esq | 46 × 119 × 82 | 1 | PLA | laranja | sim | 38 | 1.5 |
| aro | 40 × 40 × 3 | 2 | PLA | ciano | não | 4 | 0.3 |
| pata-dir | 44 × 37 × 25 | 1 | PLA | marrom | não | 10 | 0.5 |
| pata-esq | 44 × 37 × 25 | 1 | PLA | marrom | não | 10 | 0.5 |
| rabo | 84 × 72 × 50 | 1 | PLA | marrom | sim | 34 | 1.4 |
| cranio | 160 × 185 × 114 | 1 | PLA | laranja | sim | 179 | 6.8 |
| mandibula | 119 × 58 × 44 | 1 | PLA | laranja | sim | 21 | 0.8 |
| focinho | 79 × 41 × 40 | 1 | PLA | marrom | sim | 12 | 0.5 |
| mesa-cabeca | 98 × 140 × 33 | 1 | PETG | grafite | não | 40 | 1.5 |
| orelha | 28 × 28 × 15 | 2 | PLA | marrom | não | 9 | 0.5 |
| topete | 16 × 26 × 6 | 1 | PLA | laranja | não | 2 | 0.2 |
| olho | 42 × 29 × 42 | 1 | PLA | branco | não | 13 | 0.6 |
| olho-esq | 42 × 29 × 42 | 1 | PLA | branco | não | 13 | 0.6 |
| iris | 30 × 15 × 30 | 1 | PLA | marrom | não | 5 | 0.2 |
| iris-esq | 30 × 15 × 30 | 1 | PLA | marrom | não | 5 | 0.2 |
| pupila | 21 × 11 × 21 | 1 | PLA | preto | não | 2 | 0.2 |
| pupila-esq | 21 × 11 × 21 | 1 | PLA | preto | não | 2 | 0.2 |
| bucha-eixo (comum) | 7 × 7 × 3 | 1 | PLA | cinza | não | 0 | 0.1 |
| chassi (comum) | 152 × 190 × 148 | 1 | PETG | grafite | não | 206 | 7.6 |
| capa-esfera (comum) | 29 × 29 × 6 | 1 | PETG | grafite | não | 3 | 0.2 |
| bandeja-uno (comum) | 61 × 90 × 16 | 1 | PETG | amarelo | não | 19 | 0.8 |
| bandeja-pi (comum) | 61 × 90 × 16 | 1 | PETG | amarelo | não | 16 | 0.7 |
| garfo-pescoco (comum) | 65 × 48 × 51 | 1 | PETG | grafite | não | 17 | 0.7 |
| berco-tilt (comum) | 38 × 23 × 77 | 1 | PETG | grafite | sim | 15 | 0.6 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 39 |  |  |  | **1050** | **42** |

* estimativa por volume, sem fatiador
<!-- /TABELA -->

### Robô quadrado

<!-- TABELA:pecas:cubo -->
| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| base | 150 × 144 × 66 | 1 | PETG | grafite | não | 220 | 8.1 |
| tampa-base | 150 × 144 × 18 | 1 | PETG | grafite | não | 94 | 3.5 |
| porta-traseira | 137 × 62 × 5 | 1 | PETG | grafite | não | 32 | 1.3 |
| tubo-pescoco | 36 × 36 × 28 | 1 | PETG | prata | não | 15 | 0.6 |
| engrenagem-servo | 69 × 69 × 8 | 1 | PETG | amarelo | não | 23 | 0.9 |
| garfo | 133 × 92 × 24 | 1 | PETG | grafite | não | 40 | 1.6 |
| quadro-cabeca | 94 × 60 × 55 | 1 | PETG | amarelo | não | 30 | 1.2 |
| cabeca-corpo | 112 × 100 × 89 | 1 | PLA | branco | não | 135 | 5.1 |
| cabeca-face | 112 × 100 × 43 | 1 | PLA | preto | não | 34 | 1.3 |
| espacador-pi | 6 × 6 × 5 | 4 | PLA | cinza | não | 0 | 0.3 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 14 |  |  |  | **638** | **25** |

* estimativa por volume, sem fatiador
<!-- /TABELA -->

---

## 3. Peças compradas (estimativa de preço, nov/2026, lojas brasileiras)

| Item | Dino | Capivara | Cubo | R$ (cada, estimativa) |
|---|---|---|---|---|
| Servo padrão MG996R (pan e tilt) | 2 | 2 | 2 | 30–45 |
| Micro servo SG90 ou MG90S (boca, braços) | 3 | 1 | — | 12–30 |
| Motor TT amarelo 1:48 + roda 65 mm | 2 | 2 | — | 12–20 |
| Esfera de aço de 16 mm (ou bolinha de gude medida) | 1 | 1 | — | 3–10 |
| Suporte 2×18650 + 2 células | 1 | 1 | 1 | 50–90 |
| Chave gangorra KCD11 | 1 | 1 | 1 | 3–6 |
| Arduino Uno R3 + Sensor Shield V5 | 1 | 1 | 1 | 70–165 |
| Raspberry Pi 4 ou 5 (obrigatório só na fase 2; no cubo, já na fase 1 por causa da tela) | opcional | opcional | 1 | 400–700 |
| Tela TFT 3,5" para Raspberry Pi (MPI3501) | — | — | 1 | 90–150 |
| Driver L298N | 1 | 1 | — | 20–35 |
| Inserto M3 a quente (compre 30) | 25 | 25 | 14 | 0,40–0,80 |
| Parafusos M3 (6, 8, 10, 12, 16, 25 mm), porcas e arruelas M3 | kit | kit | kit | 25–40 o kit |
| Parafuso M3×12 cabeça chata | 2 | 2 | 8 | — |
| Parafuso M3×35 + porca (tubo do pescoço) | — | — | 3 | — |
| Parafuso M2,5×8 (bandeja do Pi) / M2,5×12 + porca (cubo) | 4 | 4 | 4 | — |
| 4 pés de borracha adesivos | — | — | 4 | 5–10 |

**Total estimado sem a impressora e sem o Raspberry Pi:** R$ 330–560 por bicho; R$ 260–430 no cubo (+ Pi e tela).

Ferramentas: chaves Phillips e Allen 2,5, ferro de solda (insertos), paquímetro, cola instantânea.

---

## 4. Fontes das medidas dos componentes

Todas as medidas estão em `cad/parametros.py`, cada uma com a marca **P** (fabricante), **T** (loja/terceiro) ou
**NC** (não confirmada em fonte lida: valor usual de mercado, **meça a sua peça**). Clones variam; os bolsos têm
0,4 mm de folga por lado e, onde dá, rasgo em vez de furo.

| Componente | Medida usada | Fonte |
|---|---|---|
| Arduino Uno R3 | furos Ø3,2 em (15,24; 2,54), (66,04; 17,78), (66,04; 45,72), (13,97; 50,80) mm do canto superior esquerdo. O x do 4º furo foi lido pela escala do desenho. | P: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf (§5.4) |
| Arduino Uno R3 | placa 68,6 × 53,4 | T: https://www.pololu.com/product/2191/specs |
| Arduino Uno + shield | 30 mm de altura reservada | **NC** |
| Raspberry Pi 4 / 5 | 85 × 56; furos Ø2,7 a 3,5 da borda, 58 × 49; blocos USB a 16,0 da placa | P: https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf · https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf |
| SG90 | corpo 22,7 × 12,2; com abas 32,3; base→aba 17; altura 30,3 | P: https://www.towerpro.com.tw/product/sg90-7/ |
| MG90S | corpo 22,8 × 12,4; com abas 32,1–32,5; base→aba 18,5; altura 32,5 | P: https://www.towerpro.com.tw/product/mg90s-3/ |
| SG90 / MG90S | espessura da aba 2,5; furos a 27,8; eixo a 5,9 da ponta; horn de 1 braço | **NC** |
| MG996R | corpo 40,9 × 20; com abas 54; base→aba 26,8; topo da caixa 37 | P: https://www.towerpro.com.tw/product/mg996r/ |
| MG996R | aba→topo do horn 21 (47,6 − 26,6 do desenho) | T: cópia do datasheet (Cornell ECE5725) |
| MG996R | furos das abas 49,5 × 10 (rasgos); eixo a 10 da ponta; horn Ø21 | **NC** |
| Motor TT 1:48 | caixa 37 × 22,44 × 18,6; total 70; eixo Ø5,4 com chatos 3,7; furos a 22,55 atrás do eixo e furo da orelha 14 à frente | T: https://cdn-shop.adafruit.com/product-files/3777/3777_diagram.jpg |
| Motor TT | distância entre os 2 furos de trás: 17,6 cotado, 12,3 pela escala → **rasgo** que cobre os dois | T / **NC** |
| Roda 65 mm | Ø65 × 26–27; vão caixa→roda 3,5 | T: https://handsontec.com/index.php/product/65mm-yellow-rim-rubber-wheel-for-robotics-car-2-pcs · vão **NC** |
| Suporte 2×18650 | 74,5–80 × 40–41 × 17,7–22 (usado o maior) | T: https://www.sparkfun.com/battery-holder-2x18650-wire-leads.html · https://www.tinytronics.nl/ |
| L298N | 43 × 43 × 27; furos a 37 mm | T: https://docs.cirkitdesigner.com/component/2b8b27ac-c774-4363-a812-915f09471178/l298n-motor-driver-board-module · furos **NC** |
| Chave KCD11 | corpo 15 × 10,5 × 17,2; recorte 13,5 × 9 (do KCD117S) | T: https://jlcpcb.com/partdetail/SHOUHAN-KCD11_2PW/C5884415 · https://envistiamall.com/ |
| Inserto M3 | furo de 4,0 (Ruthex RX-M3x5,7) | T: https://3djake.com/ruthex/threaded-insert-m3-100-pieces |
| Porca M3 | 5,5 entre faces, 2,4 de espessura (DIN 934) | T: https://westfieldfasteners.co.uk/Standards/Nut-Hex-M.pdf |
| Tela 3,5" MPI3501 | placa 85,42 × 55,60; área ativa 73,44 × 48,96 | P: https://www.lcdwiki.com/3.5inch_RPi_Display |
| Tela 3,5" | espessura 7 e altura do vidro acima do Pi 24,5 | **NC** |
| Esfera de apoio | 16 mm | **NC** (bolinha de gude varia de 14 a 25 mm) |
| Alto-falante 40 mm, câmera (furos 21 × 12,5), LiDAR Ø38, conector P4 Ø8,2 | fase 2 | **NC** |
| Bambu Lab A1 | 256 × 256 × 256 mm | P: ficha técnica A1 (cópia em cdn.shopify.com/…/A1_Spec_EN_1.pdf) |

---

## 5. Verificação (saída real de `cad/verificar.py`)

O script lê os **STL exportados** e o `montagem.json`. São 9 testes:

- **Interferência (5):** volume da interseção booleana entre cada par de sólidos (peças impressas + envelopes dos
  componentes), em todas as poses declaradas. Encostar face com face não conta.
- **Teste negativo (6):** desloca uma peça 3 mm de propósito e exige que a interferência apareça.
- **Caminho de montagem (9):** para cada passo da ordem de montagem, a peça (ou o conjunto) é trazida de fora, na
  direção declarada, de 2,5 em 2,5 mm, contra tudo o que já está montado. Foi este teste que mostrou que a mesa da
  cabeça não entrava no crânio, que as rodas têm de ir depois do torso e que as costas não saíam com a chave no caminho.

Saída completa da última rodada: [`pecas/verificacao-saida.txt`](pecas/verificacao-saida.txt).

### Dinossauro
<!-- TABELA:verif:dino -->
| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 30 peças distintas, 38 no total (esperado 38); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 30 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 226.4 mm (torso-frente) |
| 4 parede | PASSOU | torso 2.36–2.41 mm; cabeça 2.36–2.42 mm; perna 2.35–2.41 mm; cauda 2.35–2.41 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 54 sólidos (37 impressos + 17 componentes), 12 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 13 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 37 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1668 g; CG neutro em x=0.1 y=-26.1 z=118.1 mm, margem 26.1 mm (tomba com 12°); pior pose 'tilt-baixo': margem 22.1 mm (11°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 26 passos de montagem, cada peça entra pela direção declarada sem atravessar o que já está montado |
<!-- /TABELA -->

### Capivara
<!-- TABELA:verif:capivara -->
| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 33 peças distintas, 39 no total (esperado 39); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 33 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 226.4 mm (torso-frente) |
| 4 parede | PASSOU | torso 2.36–2.41 mm; cabeça 2.36–2.41 mm; coxa 2.36–2.40 mm; rabo 2.36–2.41 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 53 sólidos (38 impressos + 15 componentes), 8 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 12 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 38 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1583 g; CG neutro em x=-0.0 y=-24.9 z=117.3 mm, margem 24.9 mm (tomba com 12°); pior pose 'tilt-baixo': margem 21.0 mm (10°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 22 passos de montagem, cada peça entra pela direção declarada sem atravessar o que já está montado |
<!-- /TABELA -->

### Robô quadrado
<!-- TABELA:verif:cubo -->
| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 11 peças distintas, 14 no total (esperado 14); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 11 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 150.0 mm (base) |
| 4 parede | PASSOU | modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm) |
| 5 interferência | PASSOU | 22 sólidos (13 impressos + 9 componentes), 9 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem) |
| 6 teste negativo | PASSOU | 'quadro-cabeca' deslocada 3 mm em X → 1 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 13 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1020 g; CG neutro em x=-2.2 y=5.0 z=74.5 mm, margem 59.0 mm (tomba com 38°); pior pose 'pan+37': margem 58.8 mm (38°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 12 passos de montagem, cada peça entra pela direção declarada sem atravessar o que já está montado |
<!-- /TABELA -->

**O que o script NÃO confere** (só a montagem real confirma): o encaixe lateral de 3 mm dos horns e da mandíbula
no estriado dos servos, se a chave de fenda alcança cada parafuso, a passagem e a folga dos cabos, a resistência das
peças e a qualidade de impressão das cascas com suporte. O caminho de montagem é testado em linha reta (a bateria, em dois trechos).

---

## 6. Montagem, passo a passo

### 6.1 Bichos (dino e capivara)

A ordem abaixo é a mesma que o teste 9 do verificador percorre (`ordem_bicho` em `cad/comum/base.py`).

| # | Etapa | Parafusos | Atenção |
|---|---|---|---|
| 0 | Imprima `comum-teste-encaixe.stl` e teste servo, insertos e pino | — | Ajuste `FOLGA` em `cad/parametros.py` e gere de novo se algo ficar duro ou frouxo |
| 1 | Insertos M3 a quente: chassi (2 postes da frente, 1 atrás do deck, 2 da esfera), garfo (1), berço (2 no topo da coluna), mesa (1), bandejas (1 cada), crânio (3), torso-frente (1 + 2 do painel), torso-costas (2), pernas (2 cada), cauda/rabo (2) | 25 insertos | Ferro a ~230 °C em PETG; não afunde além da face |
| 2 | Motores TT nas paredes do chassi, por fora, motor para cima | 2× M3×25 + porca e arruela por motor (rasgos) | O rasgo aceita 12,3 a 17,6 mm entre furos. A ponta interna do eixo passa pelo furo da parede |
| 3 | Esfera no soquete da lança + `capa-esfera` por baixo | 2× M3×8 | A esfera tem que girar solta |
| 4 | Chave no recorte do piso (por baixo) e, se quiser, conector de carga no furo ao lado | encaixe | O piso tem 1,6 mm de espessura só em volta da chave |
| 5 | Servo de pan (MG996R) no deck, eixo para cima, corpo para a frente | 4× M3×12 + porca (rasgos) | Centralize o servo (90°) antes de pôr o horn |
| 6 | Horn redondo no servo de pan; `garfo-pescoco` por cima do horn | parafusinhos do horn pelos 4 rasgos + parafuso central | O anel de baixo do garfo centra no horn |
| 7 | Servo de tilt (MG996R) em pé no `berco-tilt`; horn redondo no montante direito do garfo | 4× M3×12 + porca; parafusinhos do horn por fora | — |
| 8 | Berço dentro do garfo, por cima: estriado no horn (direita), parafuso-pino na esquerda | 1× M3×10 (entra no inserto do garfo e a ponta vira o pino) | Passe os cabos pela frente chata da coluna e pelo rasgo da base do garfo |
| 9 | (Dino) 2 micro servos dos braços nas janelas das paredes, eixo para fora | 2 parafusinhos cada | — |
| 10 | Bateria por trás, inclinada por cima da chave; L298N na travessa da frente; placas nas bandejas e bandejas nos trilhos | L298N 4× M3×8; Uno 4× M3×8; Pi 4× M2,5×8; trava 1× M3×12 por bandeja | Furos do L298N **não confirmados** (37 mm): confira ou use fita dupla-face. Bateria presa com fita ou velcro |
| 11 | `torso-frente` pela frente, deslizando para trás | 1× M3×10 por baixo (na frente) + 2× M3×12 cabeça chata nos postes | Os 2 de cabeça chata ficam escondidos sob o painel da barriga |
| 12 | **Rodas**, pelos poços laterais | pressão no eixo | As rodas vão **depois** do torso-frente: antes, a parede do torso não passa por elas |
| 13 | `barriga` (painel = tampa da frente) | 2× M3×8 | Na fase 2 o alto-falante vai no anel de dentro do painel |
| 14 | 4 pinos-guia na costura; `torso-costas` por trás | 2× M3×10 por baixo + 1× M3×10 no alto | No dino a `crista-costas` tampa o parafuso do alto: encaixe **sem cola** |
| 15 | Pernas/coxas pelos lados | 2× M3×10 cada, por baixo | Cole antes as unhas (dino) ou as patas e o aro (capivara) |
| 16 | Cauda/rabo por trás | 2× M3×10 por baixo | — |
| 17 | **Cabeça na bancada:** `mesa-cabeca` por baixo, para dentro do `cranio`; micro servo da boca na mesa; `mandibula` (horn na almofada direita, bucha + parafuso na esquerda); olhos, íris e pupilas | 3× M3×12 por baixo, pela mesa; 2 parafusinhos do servo; parafuso central do horn por fora; 1× M3×16 | Desloque a mandíbula 3 mm para a esquerda para entrar no estriado. Este encaixe lateral **não** é coberto pelo teste 9 |
| 18 | Cabeça inteira por cima do pescoço, até a mesa assentar na coluna do berço | 2× M3×10 por cima, pelos 2 furos do alto do crânio | A `crista-cabeca` (dino) ou o `topete` (capivara) tampa os 2 furos: encaixe **sem cola** |
| 19 | Cristas/topete, orelhas, mãos, bandana | pressão ou cola | — |
| 20 | (Dino) braços nos horns | parafuso central pelo furo de fora | — |

**Para abrir depois:** cauda/rabo (2 parafusos) → costas (3 parafusos) → bandejas (1 parafuso cada) → bateria.

### 6.2 Robô quadrado

| # | Etapa | Parafusos | Atenção |
|---|---|---|---|
| 1 | Insertos: 4 postes da base, 1 orelha da tampa, 4 cantos do corpo da cabeça, 4 blocos + 1 eixo do quadro | 14 insertos | — |
| 2 | Servo de pan nos 2 postes do piso, eixo para cima | 4× M3×12 auto-atarraxante | — |
| 3 | Horn redondo no servo; depois do Uno (passo 4), a `engrenagem-servo` (44 dentes) | parafusinhos do horn pelos rasgos | Centralize o servo antes: é o "olhar para a frente" |
| 4 | Uno nos 4 pilares (USB para a porta), **antes** da engrenagem do servo; alto-falante (fase 2) por dentro, contra a grade; bateria no berço | 4× M3×8 | A engrenagem de 44 dentes fica por cima de um canto do Uno |
| 5 | `tubo-pescoco` por baixo da `tampa-base`; tampa na base | 4× M3×10 cabeça chata | A engrenagem de 22 dentes fica sob a tampa e engrena na do servo |
| 6 | `garfo` sobre a tampa, encaixado no topo do tubo | 3× M3×35 de cima + 3 porcas nos bolsos da engrenagem | Passe os cabos pelo furo do tubo antes |
| 7 | No `quadro-cabeca`: servo de tilt na lateral direita; Pi na travessa com os 4 espaçadores; tela no GPIO | 4× M3×12 + porca; 4× M2,5×12 + porca | — |
| 8 | `cabeca-corpo` por trás do quadro (o eixo do servo corre pelo rasgo lateral) | 4× M3×8 pelo fundo | Cabos saem pelo rasgo de baixo |
| 9 | `cabeca-face` | 4× M3×10 cabeça chata | A lingueta da face fecha o rasgo lateral. A placa da tela encosta atrás da moldura (use espuma fina) |
| 10 | Cabeça entre os braços do garfo: horn no estriado (direita), parafuso no inserto (esquerda) | parafusinhos do horn por fora; 1× M3×12 | — |
| 11 | `porta-traseira` com a chave | 1× M3×8 | — |

---

## 7. Preparado para a fase 2

A fase 2 (eletrônica, voz, visão, navegação, IA) **não está feita**. A mecânica já deixa o lugar, os furos e a passagem de cabos:

| Componente da fase 2 | Dino | Capivara | Robô quadrado |
|---|---|---|---|
| **Cérebro: Raspberry Pi 4/5** | bandeja-pi no trilho de cima do rack; 5 rasgos de ventilação nas costas | igual | dentro da cabeça, atrás da tela |
| **Arduino Uno + shield** (motores e servos) | bandeja-uno no trilho de baixo (as duas bandejas cabem juntas) | igual | 4 pilares no piso da base |
| **Microfone** (array de 2 a 4) | 4 furos Ø2 no peito, acima da barriga | 4 furos Ø2 no peito | 4 furos Ø2 no topo da cabeça + 4 na tampa da base |
| **Alto-falante 40 mm** | anel por dentro do painel da barriga; as fendas do painel são a grade | igual (painel da frente) | anel + grade na parede da frente da base |
| **Câmera do Pi** (25 × 24, cabo flat) | 4 pilares M2 dentro do focinho + furo da lente; move com a cabeça | 4 pilares na testa + furo da lente | 4 pilares atrás da face, acima da tela |
| **Cabo flat / cabos da cabeça** | sobem pela face chata da coluna do berço, passam pelo rasgo do garfo e pelo rasgo do deck | igual | pelo tubo oco do pescoço (Ø14) e pelo rasgo de baixo da cabeça |
| **Distância na frente** (ToF ou HC-SR04) | janela Ø10 abaixo da barriga | igual | não se aplica (de mesa) |
| **Distância nas laterais / queda** | 4 pontos universais (par de furos M3 a 20 mm) no piso, na frente e atrás de cada roda | igual | 2 pontos universais no piso da base |
| **Encoders** | 12 mm livres acima de cada motor TT (versão com encoder) + furo para a ponta interna do eixo | igual | — |
| **IMU** | 2 furos M3 no deck, ao lado do eixo do pescoço | igual | ponto universal no piso da base |
| **LiDAR (LD06/LD19)** | **não comporta** com 360° livres (a cabeça tampa). Lugar possível: sob a barriga, com ~180° para a frente | idem | **comporta**: ponto universal + furo de cabo no topo plano da cabeça |
| **Bateria maior** | baia de 58 × 114 × 23 mm (2×18650 ou LiPo 2S até ~110 × 46 × 21); sai por trás, depois da bandeja de baixo; furo de 8,2 mm para carga no piso, para não precisar tirar | igual | 2×18650 no berço + espaço livre atrás, à direita; porta traseira |

Limite conhecido: a baia dos bichos não recebe power bank nem 4 células lado a lado. Se a fase 2 pedir mais autonomia,
a saída é LiPo 2S maior ou alongar o piso (parâmetro `BASE.piso_y`).

---

## 8. Como gerar e conferir

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python 3.12 ou mais novo
.venv/bin/python cad/gerar.py todos        # STL, 3MF, montagem.json, montagem.glb, mesas/
.venv/bin/python cad/verificar.py todos    # os 9 testes; sai com código 1 se algum falhar
.venv/bin/python cad/tabelas.py            # reescreve as tabelas dos documentos
cad/renders.sh dino                        # imagens (precisa do Blender)
```

Um quarto modelo entra como `cad/modelos/<nome>.py` + uma seção em `cad/parametros.py`; se for um bicho que roda,
reaproveita `cad/comum/base.py` (esqueleto) e `cad/comum/bicho.py` (casca, cabeça, painéis).

---

## 9. Pendências

- **Imprimir e montar.** Nada foi testado em plástico. Comece pelo cupom de teste e por uma peça pequena de cada tipo.
- **Medidas NC** da tabela 4: medir com paquímetro e corrigir `cad/parametros.py`.
- **Altura:** os bichos ficaram com ~33 cm, não 30. O que manda é a pilha bateria + Uno com shield + Pi sob o servo de pan.
- **Fatiar** para ter tempo e filamento de verdade.
- **Vídeo explicativo do guia:** ainda não gravado.
- **IA (Claude por `claude -p` ou API), reconhecimento e mapa da casa = fase 2.**
