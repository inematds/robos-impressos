# Plano — robos-impressos (fase 1: corpo impresso, montado e ligado)

Quatro robôs impressos em 3D numa **Bambu Lab A1** (mesa de 256 × 256 × 256 mm), com as peças geradas por código.
Este arquivo guarda só o que vale para os quatro: as decisões gerais e os porquês, a semelhança com as imagens de
referência, o resumo da imprimibilidade e as fontes das medidas. As decisões de cada robô estão no plano dele:

| Robô | O que é | Plano | Resumo |
|---|---|---|---|
| **Dinossauro** (`dino`) | 30 cm; roda, vira e inclina a cabeça, abre a boca, mexe 2 braços | [projetos/dino/PLANO.md](projetos/dino/PLANO.md) | [README](projetos/dino/README.md) |
| **Capivara** (`capivara`) | 30 cm, de bandana verde; roda, vira e inclina a cabeça, abre a boca | [projetos/capivara/PLANO.md](projetos/capivara/PLANO.md) | [README](projetos/capivara/README.md) |
| **Robô quadrado de mesa** (`cubo`) | 20 cm; cabeça-cubo com tela de 3,5", gira ±170° e inclina; não roda | [projetos/cubo/PLANO.md](projetos/cubo/PLANO.md) | [README](projetos/cubo/README.md) |
| **Robô quadrado que roda** (`cubo_rodas`, pasta `cubo-rodas`) | 30 cm; a mesma cabeça, maior, com tela de 5", sobre uma base com 2 motores com encoder | [projetos/cubo-rodas/PLANO.md](projetos/cubo-rodas/PLANO.md) | [README](projetos/cubo-rodas/README.md) |

<!-- TABELA:resumo -->
| Modelo | Altura (mm) | Peças | Mesas (impressões) | Filamento total (g)* | Impressão total (h)* | Robô montado (g)* |
|---|---|---|---|---|---|---|
| Dinossauro | 300 | 34 | 12 | 1010 | 40 | 1605 |
| Capivara | 300 | 32 | 11 | 1129 | 44 | 1714 |
| Robô quadrado | 200 | 15 | 7 | 735 | 28 | 1147 |
| Robô quadrado que roda | 306 | 19 | 8 | 1143 | 43 | 2214 |

* estimativa por volume, sem fatiador
<!-- /TABELA -->

**Fase 1 = corpo impresso, montado e ligado:** peças, encaixes, lugar de cada componente, parafusos, lista de compras
e esquema de ligação. O programa (andar, voz, câmera, IA) é a fase 2 e não foi feito.
**Nada disto foi impresso nem montado ainda, e a parte elétrica não foi testada na bancada.** O que existe é um
protótipo digital conferido por script (`comum/cad/verificar.py`). Tempo, filamento e preço são **estimativas**. As
imagens são renders das peças, não fotos.

Por que o repositório se chama `robos-impressos` e não `dinobot`: o pedido começou com o dinossauro e virou quatro
robôs que dividem o mesmo código, as mesmas regras e o mesmo verificador.

---

## 1. Decisões gerais (e o porquê)

| Decisão | Por quê |
|---|---|
| **Cada robô na sua pasta** (`projetos/<robô>/`), com README, plano, lista de compras, guia de impressão, ligação, STL e zip; o que é de todos em `comum/` | Quem quer fazer um robô abre uma pasta e tem tudo dele. Na versão 1.0.2 era um plano só para os três, e a lista de compras misturava os robôs. |
| **Rodar, não andar** (dino, capivara e o robô quadrado que roda) | Duas rodas com motor e um terceiro apoio funcionam sem sensor de equilíbrio. Um bípede de cabeça grande pede de 6 a 10 servos fortes e cai com facilidade. |
| **Esqueleto de PETG, casca de PLA** | O esqueleto (chassi, bandejas, garfo, base, quadro) leva parafuso, inserto a quente e calor de motor. A casca só veste e sai sem desmontar o esqueleto. |
| **A forma dos bichos vem de uma malha 3D da imagem de referência** | Desenhados com formas simples, os bichos ficavam longe das referências. A malha foi gerada no computador, sem serviço externo, e virou a pele de cada bicho (`comum/cad/peles/`). A seção 2 mede o ganho. |
| **Cada bicho com o seu esqueleto** | Com a forma nova, o dino tem o peso atrás do eixo das rodas e a capivara, à frente: o terceiro apoio muda de lado. Continuam comuns o garfo do pescoço, o berço do tilt, a capa da esfera e o código da cabeça. |
| **Os dois robôs quadrados dividem a cabeça e o pescoço** (`comum/cad/comum/quadrado.py`) | Mesma solução: tilt por dentro da cabeça, pan por engrenagens 2:1 e tubo oco com 3 tirantes de aço. |
| **Imprimir sem suporte sempre que der** | Suporte marca a peça e gasta tempo. Regra: face plana na mesa, balanço de até 45°, ponte de até 20 mm, furo horizontal em gota, chanfro de 45° nas bordas viradas para baixo. Casca oca imprime em pé, como um vaso, com corte horizontal. Onde o suporte é inevitável, ele fica por dentro ou por baixo, em árvore, e é declarado peça por peça. A seção 3 traz o resultado. |
| **Reforço onde há carga** | Insertos em postes ou ressaltos maciços, 4 ou 5 perímetros nas peças estruturais, camadas ao longo da carga no garfo e nos braços, tirantes de aço no pescoço dos robôs quadrados. Cada peça declara orientação, perímetros, preenchimento e o motivo do reforço. |
| **Nenhum parafuso nem furo técnico de frente** | Parafusos só por baixo, por trás ou por dentro. Microfones nas narinas ou sob a cabeça, alto-falante sem grade à mostra, sensores atrás de detalhes que o robô já tem. O plano de cada robô diz onde está cada furo. |
| **Nos bichos, os sensores ficam nos olhos** | Câmera atrás de uma pupila e sensor de distância atrás da outra: funciona com o Raspberry Pi 4 e mede a distância do que a cabeça olha. Duas câmeras pediriam o Pi 5 e outra bateria. |
| **Energia: células 18650 com placa de proteção e carga por USB-C** | Carrega com fonte de celular, sem abrir o robô. A placa de proteção corta descarga funda e curto. |
| **O conversor de 5 V é escolhido pela tensão mínima de entrada** | No pack de 2 células (6 a 8,4 V) vai o LM2596, que entra a partir de 4,5 V. No pack de 3 células (9 a 12,6 V) do robô que roda vai o XL4015, que pede 8 V. |
| **Servos num UBEC de 6 V, separados dos 5 V das placas** | A partida de um servo não derruba o Raspberry Pi. |
| **Raspberry Pi e Arduino conversam por uma serial de 3 fios** | Serve nos quatro: passa pelo pescoço de 9 mm dos robôs quadrados, por onde um plugue USB não passa, e resolve os bichos, em que o cabo USB não cabe (dinossauro, com o Arduino atravessado na bandeja) ou não teve o espaço conferido (capivara). |
| **Toda medida de componente tem fonte ou a marca NC** | P = fabricante, T = loja ou terceiro, NC = não confirmada (valor usual: meça a sua peça). A seção 5 lista as fontes. |
| **Os números dos documentos são gerados, não digitados** | Tabelas de peças, parafusos, passos e custos saem do `montagem.json` e de `guia/src/robos/<robô>.dados.json`. Número digitado à mão envelhece. |
| **O verificador é o portão** | 11 testes sobre os arquivos exportados; nada é publicado com teste falhando. A seção 4 diz o que cada um prova. |

---

## 2. Semelhança com as imagens de referência (antes × depois)

Medida pelo contorno do robô nas mesmas vistas das imagens de referência. O número é o IoU: a área comum das duas
silhuetas dividida pela área total, de 0 a 1. Quanto maior, mais parecido o contorno; cor e detalhe não entram.
"Teto" é a malha crua gerada a partir da imagem: um robô com rodas, cortes e folgas não passa dela. O alvo foi
definido antes de medir o depois: metade do caminho entre o antes e o teto, ou 0,10 a mais quando não há malha.

<!-- TABELA:semelhanca -->
| Modelo | Antes (v1.0.2) | Depois | Teto (malha da imagem) | Alvo | Resultado |
|---|---|---|---|---|---|
| Dinossauro | 0,814 | 0,871 | 0,897 | 0,855 | alvo atingido |
| Capivara | 0,777 | 0,920 | 0,926 | 0,852 | alvo atingido |
| Robô quadrado | 0,755 | 0,797 | — | 0,855 | alvo não atingido |
| Robô quadrado que roda | — | 0,669 | — | — | robô novo: compara com a foto do robô de mesa, não é meta |
<!-- /TABELA -->

- **Dinossauro e capivara:** passaram do alvo. A capivara ficou praticamente no teto.
- **Robô quadrado de mesa:** ficou abaixo do alvo. Com o servo de pan em pé e a engrenagem por cima dele, a base não fica
  mais baixa que cerca de 60 mm; na referência, base e pescoço somam 20 % da altura, e no robô, 41 %.
- **Robô quadrado que roda:** é um robô novo, sem imagem própria. O número compara com a foto do robô de mesa e não é meta.

Os números por vista, o método e a data de cada medida estão em [comparacao/semelhanca.md](comparacao/semelhanca.md),
gerado por `comum/cad/comparar.py`.

---

## 3. Imprimibilidade (resumo)

O teste 10 do verificador mede, em cada peça e na posição de impressão, a área de faces viradas para baixo a mais de
45° que não nasce na mesa nem é ponte curta. Peça declarada sem suporte com área acima do limite (o maior entre 30 mm²
e 0,2 % da área da peça) reprova. O teste 11 gira uma peça de cabeça para baixo e confere que o teste 10 acusa.

<!-- TABELA:imprimibilidade -->
| Modelo | Peças diferentes | Sem suporte | Com suporte declarado | Quais pedem suporte | Teste 10 |
|---|---|---|---|---|---|
| Dinossauro | 33 | 27 | 6 | corpo, traseira, cranio, mandibula, garfo-pescoco, berco-tilt | PASSOU |
| Capivara | 29 | 23 | 6 | corpo, porta, cranio, mandibula, garfo-pescoco, berco-tilt | PASSOU |
| Robô quadrado | 12 | 12 | 0 | — | PASSOU |
| Robô quadrado que roda | 15 | 15 | 0 | — | PASSOU |
<!-- /TABELA -->

Antes (versão 1.0.2, medida com o mesmo teste): no dinossauro, 8 peças sem suporte, 8 com suporte e 14 que seriam
reprovadas; na capivara, 8, 12 e 13; no robô quadrado de mesa, 7 das 10 peças próprias seriam reprovadas.

Nos bichos, as 6 peças que ainda pedem suporte são as mesmas: crânio, corpo, a tampa de trás (traseira ou porta),
mandíbula, garfo e berço. O suporte fica por dentro ou por baixo, nunca no rosto. O plano de cada robô diz onde, e o
guia de impressão (`projetos/<robô>/IMPRIMIR.md`) traz a tabela por peça: orientação, suporte, perímetros,
preenchimento, gramas e horas.

---

## 4. Verificação

`comum/cad/verificar.py` roda 11 testes sobre os arquivos exportados de cada robô. Todos têm de passar.

| # | Teste | O que prova |
|---|---|---|
| 1 | contagem | O número de peças é o esperado. |
| 2 | malha | Cada STL é fechado e tem um corpo só. |
| 3 | mesa | Cada peça cabe em 256 × 256 × 256 mm na posição de impressão. |
| 4 | parede | As cascas têm 2,0 mm ou mais (medida real entre a pele de fora e a de dentro). |
| 5 | interferência | Nenhuma peça atravessa outra nem um componente, em todas as poses. |
| 6 | negativo da interferência | O teste 5 acusa quando uma peça é posta fora do lugar. |
| 7 | peça solta | Toda peça montada encosta em outra: nenhuma fica flutuando. |
| 8 | equilíbrio | O centro de massa fica dentro dos apoios, com 10 mm ou mais de margem, em todas as poses. |
| 9 | caminho | Cada peça entra e sai pelo lado indicado na montagem, sem bater no que já está montado. |
| 10 | imprimibilidade | Peça declarada sem suporte não tem área sem apoio acima do limite. |
| 11 | negativo da imprimibilidade | O teste 10 acusa uma peça girada de cabeça para baixo. |

O que os testes não provam: folga real na impressora, medidas NC, caminho da ferramenta e dos fios, força das peças em
uso e toda a parte elétrica.

A saída de cada robô está em `projetos/<robô>/verificacao-saida.txt` e no fim do README dele; as tabelas de todos, em
[projetos/TABELAS.md](projetos/TABELAS.md).

---

## 5. Fontes das medidas dos componentes

Todas as medidas estão em `comum/cad/parametros.py`, cada uma com a marca **P** (fabricante), **T** (loja/terceiro) ou
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
| Alto-falante 40 mm, câmera (furos 21 × 12,5) | fase 2 | **NC** |
| Bambu Lab A1 | 256 × 256 × 256 mm | P: ficha técnica A1 (cópia em cdn.shopify.com/…/A1_Spec_EN_1.pdf) |
| Conversor LM2596 (5 V no pack de 2 células) | placa 43 × 21 × 14, 10 g; entrada a partir de 4,5 V, 3 A máx. | T: https://curtocircuito.com.br/conversor-dc-dc-step-down-lm2596.html · queda de 1,16 a 1,4 V a 3 A: P https://www.ti.com/lit/ds/symlink/lm2596.pdf |
| Conversor XL4015 (5 V no pack de 3 células) | placa 54 × 24 × 16 com dissipador, 15 g; entrada 8 a 35 V, 5 A | T: https://www.usinainfo.com.br/regulador-de-tensao/regulador-de-tensao-xl4015-step-down-saida-125-a-32v-dc-5a-8768.html |
| UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S) | 43 × 17 × 7, 11 g; 5 ou 6 V a 3 A contínuos, entrada 5,5 a 26 V | P: https://www.hobbywing.com/en/products/ubec-3a-2-6s99.html · corrente de pico **NC** |
| Carregador USB-C LX-USC-V2 (2S/3S, com balanceamento) | 32 × 18 × 5, 3 g; 8,4 V ou 12,6 V, 1,5 A | T: https://www.usinainfo.com.br/fonte-de-alimentacao/carregador-de-baterias-18650-litio-2s3s-com-balanceamento-usb-c-lx-usc-v2-8996.html · boca USB-C 9,2 × 3,4 **NC** |
| Placa de proteção BMS 2S 10 A (10A2S) | cerca de 24 × 11 × 3, 1,3 g | T: https://www.usinainfo.com.br/controladores-de-carga/controlador-de-carga-placa-de-protecao-de-carga-bms-para-bateria-18650-2s-10a-84v-5446.html |
| Placa de proteção BMS 3S 10 A (HX-3S-FL10) | 50 × 15 × 3, 3 g | T: https://www.usinainfo.com.br/controladores-de-carga-e-bms/placa-de-protecao-para-bateria-bms-18650-3s-10a-12v-hx-3s-fl10-8309.html |
| Suporte 3×18650 | 75 × 61 × 20, 19 g | T: https://www.usinainfo.com.br/suporte-para-pilhas/suporte-para-3-baterias-18650-litio-5654.html |
| Motor JGB37-520 12 V 1:56 com encoder | caixa Ø37 × 24, motor Ø33 × 22, eixo Ø6 a 7 mm do centro, 6 furos M3 num círculo de 31, 158 g, 107 rpm, bloqueio 4,8 kgf·cm | T: https://rcdrone.top/products/jgb37-520-dc-gear-motor-with-encoder · posição dos furos em relação ao eixo **NC** |
| Roda 85 × 38 mm, sextavado 12 mm | Ø85 × 38, 52 g | T: https://www.usinainfo.com.br/rodas-roboticas/roda-85x38mm-azul-off-road-de-borracha-para-carrinho-robotico-nd031-8706.html |
| Adaptador sextavado 12 mm para eixo de 6 mm | 20 mm de comprimento, 5,4 g | P: https://www.pololu.com/product/2686/specs · o de latão comum no Brasil (18 mm, ~14 g) **NC** |
| Bola de tênis de mesa (apoio de trás do robô que roda) | 40 mm, 2,7 g | **NC** (regra da ITTF, não relida) |
| Tela 5" HDMI (Waveshare 5inch HDMI LCD (B)) | placa 121 × 89,55, área ativa 108 × 64,8, furos 115 × 84 | P: https://www.waveshare.com/img/devkit/LCD/5BP/Exterior-Size.jpg · espessura (14) e massa (150 g) **NC** |
| LiDAR LD19 | 54 × 46,29 × 34,8, 47 g, 3 furos Ø2,5 | P: https://www.waveshare.com/dtof-lidar-ld19.htm · posição dos furos no corpo **NC** |
| Sensor de distância ToF VL53L1X, microfone INMP441 | placa 25 × 10,7 × 3,5; placa redonda Ø14 × 3,5 | **NC** |

---

## 6. Como gerar e conferir

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python 3.12 ou mais novo
.venv/bin/python comum/cad/gerar.py todos          # STL, 3MF, montagem.json, montagem.glb, mesas/   (ou um id: dino, capivara, cubo, cubo_rodas)
.venv/bin/python comum/cad/verificar.py todos      # os 11 testes; sai com código 1 se algum falhar
.venv/bin/python comum/cad/comparar.py <id> --sem-gravar   # semelhança com a referência (precisa das imagens, que ficam fora do repositório)
.venv/bin/python comum/cad/tabelas.py --docs       # tabelas deste arquivo, dos README e de projetos/TABELAS.md
.venv/bin/python guia/src/pagina_robo.py docs <robô>       # documentos do robô (blocos gerados); veja o README de cada robô
comum/cad/renders.sh <id>                          # imagens (precisa do Blender)
```

Um robô novo entra como `projetos/<pasta>/modelo.py` + uma linha no registro `comum/cad/caminhos.py` + uma seção em
`comum/cad/parametros.py`. O que é comum e como cada robô usa está em [comum/README.md](comum/README.md).

---

## 7. Pendências gerais

- **Imprimir e montar.** Nada foi testado em plástico. Comece pelo cupom de teste e por uma peça pequena de cada tipo.
- **Testar a parte elétrica na bancada.** Os esquemas saíram das fichas dos componentes.
- **Chave liga/desliga de 3 A nos robôs que rodam.** Pela conta das fichas, nos dois bichos o uso normal (2,5 a 3 A) fica
  perto do limite da chave; no robô quadrado que roda são cerca de 2 A em uso normal e 6,5 A no pior caso. Em esforço o
  fusível de 3 A pode abrir. Uma chave maior pede mudar o recorte nas peças.
- **Medidas NC** da seção 5: medir com paquímetro e corrigir `comum/cad/parametros.py`.
- **Os 3MF das mesas** ainda não foram abertos num fatiador (só relidos por script). Fatiar dá o tempo e o filamento de verdade.
- **Cupom de teste próprio dos robôs quadrados:** o atual não testa a janela do servo MG996R nem o furo do pino M5.
- **Sem lugar modelado:** porta-fusível, barra de emenda, resistores da serial e amplificador de áudio, nos quatro robôs.
- **Semelhança do robô quadrado de mesa** abaixo do alvo.
- **Pendências de cada robô:** no fim do plano de cada um.
- **IA, voz, visão, navegação e mapa da casa = fase 2.**
