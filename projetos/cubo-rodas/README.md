# Robô quadrado que roda (`cubo_rodas`)

Robô de 31 cm para imprimir na Bambu Lab A1 e montar em casa. A cabeça é um cubo com tela de 5" no rosto; gira
±170° e inclina de −25° a +30°. Embaixo, uma base com 2 motores com encoder, 2 rodas de 85 mm na frente e uma bola de
apoio atrás. Dentro vão um Raspberry Pi, um Arduino Uno, dois servos MG996R, um driver L298N e um pack de três
baterias 18650 que carrega por USB-C. Fase 1 = corpo montado e ligado; o programa vem depois, na fase 2.

**Nada foi impresso ainda, e a parte elétrica não foi testada na bancada.** As peças foram conferidas por 11 testes
no computador (resultado no fim).

<!-- GERADO:numeros -->
- Altura montado: 306,5 mm.
- Peças impressas: 19 (15 arquivos diferentes), em 8 mesas.
- Filamento: 1143 g. Tempo de impressão: 43,4 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 31.
<!-- /GERADO -->
- Robô montado: cerca de 2,2 kg (estimativa). Largura total com as rodas: 219 mm. Com o LiDAR da fase 2: 341 mm de altura.

| Para | Onde |
|---|---|
| Ver o robô e seguir o guia | https://inematds.github.io/robos-impressos/guia/cubo-rodas/ (também em `/guia/en/cubo-rodas/` e `/guia/es/cubo-rodas/`) |
| Entender as decisões | [PLANO.md](PLANO.md) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) · [English](LISTA-DE-COMPRAS.en.md) · [Español](LISTA-DE-COMPRAS.es.md) |
| Imprimir | [IMPRIMIR.md](IMPRIMIR.md) · [English](IMPRIMIR.en.md) · [Español](IMPRIMIR.es.md) |
| Ligar os fios | [LIGACAO.md](LIGACAO.md) · [English](LIGACAO.en.md) · [Español](LIGACAO.es.md) |
| Pôr os servos no centro | [firmware/centrar_servos/centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino) |
| Baixar tudo | [cubo-rodas-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/cubo-rodas-stl.zip) (STL, 3MF das mesas, sketch e guias nos 3 idiomas) |
| STL, 3MF, mesas | `projetos/cubo-rodas/stl/`, `projetos/cubo-rodas/3mf/`, `projetos/cubo-rodas/mesas/` (+ `comum/pecas/stl/comum-teste-encaixe.stl`) |
| Modelo | `projetos/cubo-rodas/modelo.py`, `comum/cad/comum/quadrado.py`, seção `CUBO_RODAS` de `comum/cad/parametros.py` |

A pasta se chama `cubo-rodas`; no código, nos comandos do gerador e no nome dos STL o id é `cubo_rodas`.

## Montagem

Antes de montar, faça os 4 preparos da bancada descritos em [LIGACAO.md](LIGACAO.md): energia soldada e ajustada
(5,1 V e 6 V), programa gravado no Arduino com os 2 servos em 90°, cabos da serial, do Raspberry Pi, do driver e dos
encoders prontos, cartão microSD gravado. Toda a solda fica nesses preparos; na montagem só há bornes e encaixes.
Depois assente os 31 insertos M3 a quente e siga a ordem abaixo, que é a que o verificador testou (teste 9): cada
peça entra pelo lado indicado sem bater no que já está montado. Os passos com "(bancada)" são feitos fora do robô.

### Parafusos

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

### Passo a passo

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | base-rodas | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, servos em 90°, cabos prontos, cartão gravado) e assente os 31 insertos a quente. |
| 2 | motor direito com a flange, pela lateral (6 M3x6 + 4 M3x10) | pela direita | Na bancada, prenda o motor na flange com 6 × M3 × 6: a cabeça de cada parafuso fica no rebaixo. Passe o cabo de 6 fios para dentro da base pelo furo da parede e enfie o motor, com o eixo para baixo (ele fica 7 mm abaixo do centro). Depois, 4 × M3 × 10 nos insertos da parede. |
| 3 | motor esquerdo com a flange, pela lateral | pela esquerda | Igual ao motor direito. |
| 4 | roda direita com o adaptador sextavado | pela direita | Adaptador no eixo do motor, com o parafuso de trava apertado sobre a face chata do eixo. Roda no sextavado, presa pelo parafuso da ponta do adaptador. Sobram cerca de 2,5 mm entre a flange e a roda. |
| 5 | roda esquerda com o adaptador sextavado | pela esquerda | Igual à roda direita. |
| 6 | bola e capa, por baixo (4 M3x8) | por baixo | Bola no poço e capa por baixo, com 4 × M3 × 8. A bola tem de girar solta. |
| 7 | carregador USB-C e BMS no piso | por cima | O chicote já vem soldado e conferido do preparo 1. O carregador vai no berço, com 1 abraçadeira e a boca USB-C encostada na janela de trás. A placa de proteção vai com fita dupla-face. |
| 8 | chave (por fora, atrás) | por trás | Já está no lugar desde o preparo 1. Ela encaixa por pressão no recorte, por fora, com os 2 fios passando pelo recorte. |
| 9 | bateria no alçapão, por baixo (4 M3x8) | por baixo | Prenda o suporte nas 4 cantoneiras do alçapão, com 1 abraçadeira. Com a chave desligada, ponha as 3 células, conferindo o lado do positivo com o multímetro. Suba o alçapão e prenda com 4 × M3 × 8. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 10 | servo de pan, Uno, L298N, step-down e UBEC no deck (bancada) | por cima | Servo de pan: 4 × M3 × 12, eixo para cima. Ele já está em 90° (preparo 2): não gire o eixo com a mão. Arduino Uno: 4 × M3 × 8, com o sketch já gravado. Se o shield cobrir os furos de fixação do Uno (não confirmado), parafuse o Uno sem ele e encaixe o shield depois, com o jumper SEL retirado. Driver L298N: 4 × M3 × 8, já sem os 3 jumpers (preparo 1). Conversor e UBEC nos berços, com 1 abraçadeira cada. A barra de emenda, com o divisor já preso nela, fica solta ao lado do Arduino. Refaça no shield as ligações que você desfez no fim do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra no + e no − do conector COM, servo de pan no D9. Ligue os 6 jumpers do driver. No COM, os pinos TX e RX ficam vazios. |
| 11 | engrenagem do servo no horn (bancada) | por cima | Horn redondo no rebaixo da engrenagem, 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 6 mm. Não gire o eixo: ele está em 90°. |
| 12 | deck montado sobre a base | por cima | Chave desligada. Antes de assentar o deck, passe para cima os fios que vêm da base: o cabo de cada motor por um dos 2 rasgos laterais e os 2 fios da chave e da placa de proteção pelo rasgo de trás. O deck fica solto sobre os 4 postes: quem o prende é o tronco. Agora ligue, só por borne e encaixe: o fio vermelho da chave no borne 4 e o preto da placa de proteção no borne 5; de cada motor, o vermelho e o branco nos bornes de saída do driver (motor direito em OUT1 e OUT2, esquerdo em OUT3 e OUT4), o azul no borne +5V do driver, o preto no borne GND do driver, o amarelo e o verde nos conectores do shield (direito: D2 e A0; esquerdo: D3 e A1), sempre no pino S. |
| 13 | Raspberry Pi e espaçadores no quadro (bancada) | pela frente | 4 × M2,5 × 12 com porca; os 4 espaçadores ficam entre o Pi e a travessa. O cartão microSD já gravado (preparo 4) entra antes. Cole os dissipadores. Encaixe agora os 3 jumpers da serial nos pinos 32, 33 e 34 e os 4 conectores do cabo de energia nos pinos 2, 4, 6 e 9 (preparo 3): depois que o painel com a tela entra, fica difícil alcançar os pinos. |
| 14 | tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada) | pela frente | Primeiro prenda a tela nos 4 pilares do painel do rosto, com 4 × M2,5 × 6, e encaixe nela o cabo HDMI e o cabo USB. A câmera é da fase 2: é opcional agora, e o furo dela fica vazio. Depois, 4 × M3 × 8 por trás da travessa, nos insertos dos pilares do painel. Ligue os 2 cabos da tela no Raspberry Pi. Depois que o servo entra, esses parafusos ficam sem acesso. |
| 15 | servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada) | por trás | 4 × M3 × 12. O servo já está em 90° (preparo 2). Os 2 parafusos de cima são apertados pelos furos de acesso da lateral esquerda. |
| 16 | garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada) | por baixo | Prenda o horn no braço direito do garfo com 4 × M2 × 8. Com o servo em 90°, encaixe o garfo apontando para baixo, com o rosto na vertical. O parafuso central do horn entra pelo furo do pino. Por último, o M5 × 16: aperte até encostar e volte um quarto de volta, porque a cabeça gira nele. |
| 17 | fiação da cabeça, antes de fechar com o copo (bancada) | fios, de cima para baixo | É a última vez que você alcança o Raspberry Pi. 1) Confira nos pinos do Pi os 4 conectores do cabo de energia (pinos 2, 4, 6 e 9) e os 3 da serial (pinos 32, 33 e 34), postos antes da tela. 2) Confira os 2 cabos da tela, HDMI e USB, encaixados no Pi e sem forçar a parede da cabeça. 3) Ligue a extensão de 30 cm no cabo do servo de tilt. 4) Desça os 8 fios pelo furo de 9 mm do garfo, de cima para baixo, primeiro o conector da extensão. Pare quando as pontas ficarem rentes à face de baixo do garfo. 5) Deixe uma barriga de uns 5 cm de fio dentro da cabeça: ela inclina em volta do garfo e os fios dobram ali. |
| 18 | copo da cabeça por trás; 4 M3 na parede de trás (bancada) | por trás | O fundo do copo passa por baixo do garfo: confira que nenhum fio sobra para fora do furo do garfo. 4 × M3 × 8. Depois, com a pinça, puxe as pontas dos 8 fios para fora pelo rasgo do fundo do copo. |
| 19 | alto-falante nos trilhos do tronco, por baixo (bancada) | por baixo | Fase 2: é opcional agora, pode pular. |
| 20 | tubo do pescoço no tronco, por cima (bancada) | por cima | A flange cônica apoia no topo do tronco. |
| 21 | engrenagem do pescoço por dentro do tronco (bancada) | por baixo | Alinhe os 3 furos com os do tubo. |
| 22 | cabeça sobre o tubo; 3 tirantes M3 por dentro do tronco (bancada) | por cima | Enfie os 8 fios pelo tubo do pescoço, de cima para baixo, e só então assente a cabeça, sem prender fio entre o garfo e o tubo. 3 × M3 × 50 por dentro do tronco, de baixo para cima, pela engrenagem, até os insertos do garfo. |
| 23 | LiDAR no topo da cabeça (fase 2) | por cima | Fase 2: é opcional agora, pode pular. Os furos são cegos: por fora não aparece nada enquanto o sensor não for instalado. |
| 24 | tronco + pescoço + cabeça sobre o deck; 4 M3x12 por baixo da base | por cima | Chave desligada. Nenhuma solda aqui, só bornes e encaixes: os 2 fios de 5,1 V nos bornes 1 e 2 da barra de emenda; o fio azul no borne 3; o conector do fio verde no pino S do D0 e o do preto no pino G do D0; o jumper do divisor no pino S do D1; a extensão do servo de tilt no D10. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos, que queimam o Raspberry Pi. Deixe 10 cm de folga para o giro. Com a cabeça olhando para a frente e o servo de pan em 90°, engrene os dentes. Deite o robô de lado, com cuidado, e ponha os 4 × M3 × 12 por baixo, no fundo dos furos dos 4 postes, com a chave Allen longa: eles atravessam o deck e rosqueiam nos insertos do tronco. |
<!-- /GERADO -->

## Abrir para manutenção

Trocar a bateria ou tirar um motor não exige abrir o robô. Para mexer nas placas, o tronco sai inteiro, com o pescoço
e a cabeça.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | abrir: alçapão com a bateria sai por baixo | Desligue a chave antes. Solte os 4 parafusos de baixo e desça o alçapão: a bateria vem junto, presa pelos fios, que têm folga. |
| 2 | abrir: motor direito sai pela lateral (roda, depois flange + motor) | Tire o parafuso da ponta do adaptador e puxe a roda. Solte os 4 parafusos da flange e puxe o motor para fora. Antes, solte no deck os 6 fios do cabo dele; para isso é preciso levantar o tronco. |
| 3 | abrir: tronco + pescoço + cabeça saem por cima (placas do deck à mostra) | Solte os 4 parafusos por baixo da base e levante o conjunto inteiro, devagar: os fios do pescoço continuam ligados. É assim que se chega ao USB do Arduino. |
<!-- /GERADO -->

## Energia e ligação

Pack 3S (3 × 18650, 9 a 12,6 V) → fusível retardado de 3 A (T3A) → placa de proteção BMS 3S → chave (KCD11-101, 3 A) → barra de emenda no deck → três linhas:

- **5,1 V do Raspberry Pi, do Arduino, do driver e dos encoders:** conversor XL4015. O Pi recebe pelos pinos 2, 4, 6
  e 9; o Arduino, pelos pinos + e − do conector COM do Sensor Shield.
- **6 V dos 2 servos:** UBEC de 3 A, pelo borne azul do Sensor Shield (jumper SEL retirado), com capacitor de 1000 µF.
- **Motores:** tensão do pack pelo driver L298N, comandado pelo Arduino por 6 fios (D5, D4, D7, D6, D8 e D12). Encoders
  no D2 e A0 (direito) e no D3 e A1 (esquerdo).
- **Carga:** módulo USB-C com balanceamento, antes da chave, com a boca numa janela atrás da base. Ele precisa ser
  preparado para 3 células e usa 2 fios a mais, nas emendas entre as células.
- **Raspberry Pi ↔ Arduino:** serial (UART) de 3 fios pelo pescoço. Pi: pinos 32 (TX), 33 (RX) e 34 (GND). Arduino:
  D0 e D1, com um divisor de 3 resistores de 1 kΩ, preso na barra de emenda, no fio que vai do Arduino para o Pi.

O esquema, a tabela fio a fio e os avisos de segurança estão em [LIGACAO.md](LIGACAO.md). Nada disso foi testado na
bancada. A chave de 3 A é o ponto mais fraco: a conta de corrente está no mesmo arquivo.

## Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py cubo_rodas` (cópia completa em `verificacao-saida.txt`):

<!-- GERADO:verificacao -->
```
== verificação: cubo_rodas
  [PASSOU] 1 contagem: 15 peças distintas, 19 no total (esperado 19); faltando 0; sobrando 0
  [PASSOU] 2 malha: 15 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 182.0 mm (base-rodas)
  [PASSOU] 4 parede: modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm)
  [PASSOU] 5 interferência: 41 sólidos (18 impressos + 23 componentes), 11 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem)
  [PASSOU] 6 teste negativo: 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 18 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 2214 g; CG neutro em x=1.0 y=-41.1 z=127.4 mm, margem 41.1 mm (tomba com 18°); pior pose 'pan+170+tilt-baixo': margem 37.6 mm (17°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 26 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 15 peças distintas: 15 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'deck' na orientação declarada: 0 mm² sem apoio (limite 106); girada 180° em X → 19084 mm² = 36.1 % (acusou; tem que acusar)
```
<!-- /GERADO -->

## Como regenerar

```
.venv/bin/python comum/cad/gerar.py cubo_rodas                      # STL, 3MF, mesas, montagem.json
.venv/bin/python comum/cad/verificar.py cubo_rodas                  # 11 testes
.venv/bin/python guia/src/pagina_robo.py docs cubo-rodas pt     # blocos GERADO destes arquivos
.venv/bin/python guia/src/pagina_robo.py traduzir cubo-rodas    # EN e ES pelo inema-traduz (só o que mudou)
.venv/bin/python guia/src/pagina_robo.py docs cubo-rodas        # versões .en.md e .es.md
.venv/bin/python guia/src/pagina_robo.py esquema cubo-rodas     # ligacao.<idioma>.svg
.venv/bin/python guia/src/pagina_robo.py zip cubo-rodas         # cubo-rodas-stl.zip
.venv/bin/python guia/src/pagina_robo.py conferir cubo-rodas    # links, idiomas, zip
```

Os arquivos `*.en.md`, `*.es.md` e `ligacao.*.svg` são gerados: mude o texto em português (ou
`guia/src/robos/cubo-rodas.dados.json`) e rode os comandos acima. O desenho do esquema está em
`guia/src/esquema_cubo_rodas.py`.

## Pendências

A lista completa, com o porquê de cada uma, está no fim do [PLANO.md](PLANO.md). As principais:

- Imprimir e montar: comece pelo cupom de teste.
- Testar a parte elétrica na bancada (nenhum fio foi ligado ainda).
- A chave de 3 A é pequena para o pior caso de corrente deste robô.
- Os 2 cabos da tela (HDMI e USB) não estão no modelo 3D: conferir se cabem dentro da cabeça.
- Medidas NC dos componentes (motor, tela, chave, boca do USB-C): medir e corrigir `comum/cad/parametros.py`.
