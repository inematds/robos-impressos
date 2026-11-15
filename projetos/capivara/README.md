# Capivara (`capivara`)

Robô de 30 cm para imprimir na Bambu Lab A1 e montar em casa. Roda sobre 2 rodas escondidas nas ancas e 2 esferas de apoio na frente, sob as patas. A cabeça gira ±60° e inclina de −15° a +20°; a boca abre 18°. Dentro vão um Raspberry Pi, um Arduino Uno, 2 servos MG996R, 1 micro servo, 2 motores com redução e um pack de duas baterias 18650 que carrega por USB-C. Fase 1 = corpo montado e ligado; o programa vem depois, na fase 2.

**Nada foi impresso ainda, e a parte elétrica não foi testada na bancada.** As peças foram conferidas por 11 testes
no computador (resultado no fim).

<!-- GERADO:numeros -->
- Altura montado: 300,0 mm.
- Peças impressas: 32 (29 arquivos diferentes), em 11 mesas.
- Filamento: 1129 g. Tempo de impressão: 44,4 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 18.
<!-- /GERADO -->
- Tamanho: 197 mm de largura × 274 mm do rabo ao focinho × 300 mm de altura. Massa estimada do robô montado: 1,7 kg.

| Para | Onde |
|---|---|
| Entender as decisões do projeto | [PLANO.md](PLANO.md) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) · [English](LISTA-DE-COMPRAS.en.md) · [Español](LISTA-DE-COMPRAS.es.md) |
| Imprimir | [IMPRIMIR.md](IMPRIMIR.md) · [English](IMPRIMIR.en.md) · [Español](IMPRIMIR.es.md) |
| Ligar os fios | [LIGACAO.md](LIGACAO.md) · [English](LIGACAO.en.md) · [Español](LIGACAO.es.md) |
| Pôr os servos no centro | [firmware/centrar_servos/centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino) |
| Baixar tudo | [capivara-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/capivara-stl.zip) (STL, 3MF das mesas, sketch e guias nos 3 idiomas) |
| STL, 3MF, mesas | `projetos/capivara/stl/`, `projetos/capivara/3mf/`, `projetos/capivara/mesas/` (+ as peças comuns de `comum/pecas/stl/`) |
| Imagens | `projetos/capivara/imagens/` (renders do modelo: montado, explodido, esqueleto, mesas e 4 vistas) |
| Modelo | `projetos/capivara/modelo.py`, `comum/cad/comum/` (casca, cabeça, esqueleto), seção `CAPIVARA` de `comum/cad/parametros.py` |
| Ver o robô e seguir o guia | https://inematds.github.io/robos-impressos/guia/capivara/ (também em `/guia/en/capivara/` e `/guia/es/capivara/`) |

![Capivara montado](imagens/capivara-montado.jpg)

## Montagem

Antes de montar, faça os 4 preparos da bancada descritos em [LIGACAO.md](LIGACAO.md): energia soldada e ajustada
(5,1 V e 6 V), programa gravado no Arduino com os 3 servos em 90°, cabos do Raspberry Pi e divisor prontos, cartão
microSD gravado. Toda a solda fica nesses preparos; na montagem só há bornes e encaixes. Depois assente os 18
insertos M3 a quente e siga a ordem abaixo, que é a que o verificador testou (teste 9): cada peça entra pelo lado
indicado sem bater no que já está montado.

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

## Abrir para manutenção

Trocar a bateria ou mexer nas placas não exige tirar a cabeça: sai só a porta traseira, com 2 parafusos.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | ABRIR: porta traseira sai | Solte os 2 parafusos de trás, embaixo, e puxe a porta. Ela sai com o rabo e o carregador e fica pendurada pelos 3 fios, que têm uns 15 cm de folga. A cabeça fica no lugar. |
| 2 | ABRIR: bandeja do Uno sai | Desencaixe os conectores do shield, marcando cada um com fita e o nome do pino, e solte do borne azul os fios do UBEC. Puxe a bandeja para trás. |
| 3 | ABRIR: bandeja do Pi sai | Desencaixe os conectores dos pinos do Raspberry Pi e puxe a bandeja para trás. |
| 4 | ABRIR: bateria sai | Desligue a chave antes. O suporte desliza no piso e sai por trás. |
<!-- /GERADO -->

## Energia e ligação

Pack 2S (2 × 18650, 6 a 8,4 V) → fusível retardado de 3 A (T3A) → placa de proteção BMS 2S → chave (KCD11-101, 3 A) → três linhas:

- **5,1 V do Raspberry Pi, do Arduino e da lógica do driver:** conversor LM2596 (cerca de 2 A contínuos). O Pi recebe
  pelos pinos 2 e 4 (5 V) e 6 e 9 (GND); o Arduino, pelos pinos + e − do conector COM do Sensor Shield.
- **6 V dos servos:** UBEC de 3 A, pelo borne azul do Sensor Shield (jumper SEL retirado), com capacitor de 1000 µF.
  Servos: pan no D9, tilt no D10 e boca no D11.
- **Motores das rodas:** driver L298N, com a tensão da bateria. Sinais: ENA no D5, IN1 no D4, IN2 no D7, IN3 no D8,
  IN4 no D12 e ENB no D6.
- **Carga:** módulo USB-C com balanceamento, antes da chave, em pé dentro do rabo, com a boca para baixo: o plugue entra por baixo do rabo, com um 3º fio no ponto que une as
  duas células.
- **Raspberry Pi ↔ Arduino:** serial (UART) de 3 fios. Pi: pinos 32 (TX), 33 (RX) e 34 (GND). Arduino: D0 e D1, com um
  divisor de 3 resistores de 1 kΩ, preso na barra de emenda, no fio que vai do Arduino para o Pi.

O esquema, a tabela fio a fio e os avisos de segurança estão em [LIGACAO.md](LIGACAO.md). Nada disso foi testado na
bancada.

## Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py capivara` (cópia completa em `verificacao-saida.txt`):

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

## Como regenerar

```
.venv/bin/python comum/cad/gerar.py capivara                      # STL, 3MF, mesas, montagem.json
.venv/bin/python comum/cad/verificar.py capivara                  # 11 testes
.venv/bin/python guia/src/pagina_robo.py docs capivara pt     # blocos GERADO destes arquivos
.venv/bin/python guia/src/pagina_robo.py traduzir capivara    # EN e ES pelo inema-traduz (só o que mudou)
.venv/bin/python guia/src/pagina_robo.py docs capivara        # versões .en.md e .es.md
.venv/bin/python guia/src/pagina_robo.py esquema capivara     # ligacao.<idioma>.svg
.venv/bin/python guia/src/pagina_robo.py zip capivara         # capivara-stl.zip
.venv/bin/python guia/src/pagina_robo.py conferir capivara    # links, idiomas, zip
```

Os arquivos `*.en.md`, `*.es.md` e `ligacao.*.svg` são gerados: mude o texto em português (ou
`guia/src/robos/capivara.dados.json`) e rode os comandos acima.

## Pendências

- Imprimir e montar: comece pelo cupom de teste.
- Testar a parte elétrica na bancada (nenhum fio foi ligado ainda).
- A chave de 3 A é o ponto fraco da parte elétrica: o uso normal calculado fica perto do limite. Uma chave maior pede mudar o recorte da peça.
- Medidas NC dos componentes (micro servo, motores, rodas, esfera, driver, sensores da fase 2): medir e corrigir `comum/cad/parametros.py`.
- Abrir os 3MF das mesas no Bambu Studio e tirar o suporte das 6 peças que pedem suporte.
- Conferir os comprimentos dos parafusos M3 e dos cabos com as peças na mão.
- Conferir se os conectores cabem em pé sobre o Raspberry Pi, sob a bandeja de cima.
- Calor: o Raspberry Pi fica fechado num corpo de PLA sem ventilação; medir a temperatura em uso.
- Porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e sensor de movimento ainda não têm fixação modelada.
- 4 pontos de apoio (2 rodas e 2 esferas): num piso irregular uma esfera pode ficar no ar. Se incomodar, dê 0,5 mm de folga a uma delas.
- A porta traseira só tem os 2 parafusos de baixo; em cima ela só encosta na gola.
- Os 3 fios do carregador atravessam a porta traseira: ela fica presa ao robô por eles (falta um conector de 3 vias).
- Acabamento: as patas da frente saem na cor do corpo (na referência são marrons); o laço da bandana na nuca não existe, porque a cabeça passa por ali quando inclina.
