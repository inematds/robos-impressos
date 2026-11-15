# Robô quadrado de mesa (`cubo`)

Robô de mesa para imprimir na Bambu Lab A1 e montar em casa. A cabeça é um cubo com tela de 3,5" no rosto; gira
±170° e inclina de −25° a +30°. Dentro vão um Raspberry Pi, um Arduino Uno, dois servos MG996R e um pack de duas
baterias 18650 que carrega por USB-C. Não roda. Fase 1 = corpo montado e ligado; o programa vem depois, na fase 2.

**Nada foi impresso ainda, e a parte elétrica não foi testada na bancada.** As peças foram conferidas por 11 testes
no computador (resultado no fim).

<!-- GERADO:numeros -->
- Altura montado: 200,5 mm.
- Peças impressas: 15 (12 arquivos diferentes), em 7 mesas.
- Filamento: 735 g. Tempo de impressão: 28,2 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 16.
<!-- /GERADO -->

| Para | Onde |
|---|---|
| Ver o robô e seguir o guia | https://inematds.github.io/robos-impressos/guia/cubo/ (também em `/guia/en/cubo/` e `/guia/es/cubo/`) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) · [English](LISTA-DE-COMPRAS.en.md) · [Español](LISTA-DE-COMPRAS.es.md) |
| Imprimir | [IMPRIMIR.md](IMPRIMIR.md) · [English](IMPRIMIR.en.md) · [Español](IMPRIMIR.es.md) |
| Ligar os fios | [LIGACAO.md](LIGACAO.md) · [English](LIGACAO.en.md) · [Español](LIGACAO.es.md) |
| Pôr os servos no centro | [firmware/centrar_servos/centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino) |
| Baixar tudo | [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip) (STL, 3MF das mesas, sketch e guias nos 3 idiomas) |
| STL, 3MF, mesas | `projetos/cubo/stl/`, `projetos/cubo/3mf/`, `projetos/cubo/mesas/` (+ `comum/pecas/stl/comum-teste-encaixe.stl`) |
| Modelo | `projetos/cubo/modelo.py`, `comum/cad/comum/quadrado.py`, seção `CUBO` de `comum/cad/parametros.py` |

## Montagem

Antes de montar, faça os 4 preparos da bancada descritos em [LIGACAO.md](LIGACAO.md): energia soldada e ajustada
(5,1 V e 6 V), programa gravado no Arduino com os 2 servos em 90°, cabo da serial e divisor prontos, cartão microSD
gravado. Toda a solda fica nesses preparos; na montagem só há bornes e encaixes. Depois assente os 16
insertos M3 a quente e siga a ordem abaixo, que é a que o verificador testou (teste 9): cada peça entra pelo lado
indicado sem bater no que já está montado. Os passos com "(bancada)" são feitos fora do robô.

### Parafusos

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

### Passo a passo

<!-- GERADO:passos -->
| # | Passo | Entra | Parafusos e atenção |
|---|---|---|---|
| 1 | base | por cima | Antes deste passo, faça os 4 preparos da bancada (energia ajustada, servos em 90°, cabo da serial e divisor prontos, cartão gravado) e assente os 16 insertos a quente. |
| 2 | servo de pan nos 2 postes | por cima | 4 × M3 × 12, eixo para cima. O servo já está em 90° (preparo 2): não gire o eixo com a mão. |
| 3 | Arduino Uno nos 4 ressaltos | por cima | 4 × M3 × 8, USB virado para a esquerda. Se o shield cobrir os furos de fixação do Uno (não confirmado), parafuse o Uno sem ele e encaixe o shield depois, com o jumper SEL retirado. O sketch já tem de estar gravado (preparo 2): com o Uno parafusado, o cabo USB não entra. |
| 4 | módulos de energia nos berços (1 abraçadeira cada) | por cima | O chicote já vem soldado e conferido do preparo 1. 3 abraçadeiras (conversor, UBEC, carregador) e fita dupla-face na placa de proteção. A boca USB-C do carregador encosta na janela de trás. A barra de emenda, com o divisor já preso nela (preparo 3), fica solta ao lado do Arduino. Refaça no shield as ligações que você desfez no fim do preparo 2: fios do UBEC e capacitor no borne azul, os 2 jumpers da barra de emenda no + e no − do conector COM, servo de pan no D9. No COM, os pinos TX e RX ficam vazios. |
| 5 | chave (por fora, atrás) | por trás | Já está no lugar desde o preparo 1. Ela encaixa por pressão no recorte, por fora, com os 2 fios passando pelo recorte. |
| 6 | alto-falante nos trilhos da parede de trás | por cima | Fase 2: é opcional agora, pode pular. |
| 7 | engrenagem do servo no horn | por cima | Horn redondo no rebaixo da engrenagem, 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 6 mm. Não gire o eixo: ele está em 90°. |
| 8 | bateria (pela porta de trás) | por trás | O suporte já está soldado no chicote desde o preparo 1, sem as células: assente-o no berço. Com a chave desligada, ponha agora as 2 células, conferindo o lado do positivo com o multímetro. Daqui em diante o chicote tem tensão: não deixe ponta de fio solta encostar em metal. |
| 9 | Raspberry Pi e espaçadores no quadro (bancada) | pela frente | 4 × M2,5 × 12 com porca; os 4 espaçadores ficam entre o Pi e a travessa. O cartão microSD já gravado (preparo 4) entra antes. Cole os dissipadores. Encaixe agora, nos pinos 31 a 34, o conector baixo com os 3 fios da serial (feito no preparo 3): depois que a tela entra, ele não entra mais. |
| 10 | tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada) | pela frente | A tela encaixa nos pinos 1 a 26 do Pi. A câmera é da fase 2: é opcional agora, e o furo dela fica vazio. 4 × M3 × 8 por trás da travessa, nos insertos dos pilares do painel. Depois que o servo entra, esses parafusos ficam sem acesso. |
| 11 | servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada) | por trás | 4 × M3 × 12. O servo já está em 90° (preparo 2). Os 2 parafusos de cima são apertados pelos furos de acesso da lateral esquerda. |
| 12 | garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada) | por baixo | Prenda o horn no braço direito do garfo com 4 × M2 × 8. Com o servo em 90°, encaixe o garfo apontando para baixo, com o rosto na vertical. O parafuso central do horn entra pelo furo do pino. Por último, o M5 × 16: aperte até encostar e volte um quarto de volta, porque a cabeça gira nele. |
| 13 | fiação da cabeça, antes de fechar com o copo (bancada) | fios, de cima para baixo | É a última vez que você alcança o Raspberry Pi. 1) Parafuse os 2 fios de 5,1 V (20 AWG) no adaptador USB-C, vermelho no + e preto no −, e encaixe o adaptador na porta USB-C do Pi. 2) Confira o conector baixo da serial nos pinos 31 a 34 (ele entrou antes da tela, com os 3 fios já soldados no preparo 3). 3) Ligue a extensão de 30 cm no cabo do servo de tilt. 4) Desça os 8 fios pelo furo de 9 mm do garfo, de cima para baixo, primeiro o conector da extensão. Pare quando as pontas ficarem rentes à face de baixo do garfo. 5) Deixe uma barriga de uns 5 cm de fio dentro da cabeça: ela inclina em volta do garfo e os fios dobram ali. |
| 14 | copo da cabeça por trás; 4 M3 na parede de trás (bancada) | por trás | O fundo do copo passa por baixo do garfo: confira que nenhum fio sobra para fora do furo do garfo. 4 × M3 × 8. Depois, com a pinça, puxe as pontas dos 8 fios para fora pelo rasgo do fundo do copo. |
| 15 | tubo do pescoço na tampa, por cima (bancada) | por cima | A flange cônica apoia na tampa. |
| 16 | engrenagem do pescoço por baixo da tampa (bancada) | por baixo | Alinhe os 3 furos com os do tubo. |
| 17 | cabeça sobre o tubo; 3 tirantes M3 por baixo (bancada) | por cima | Enfie os 8 fios pelo tubo do pescoço, de cima para baixo, e só então assente a cabeça, sem prender fio entre o garfo e o tubo. 3 × M3 × 45 por baixo da engrenagem, até os insertos do garfo. |
| 18 | tampa + pescoço + cabeça sobre a base; 4 M3 por baixo | por cima | Chave desligada. Nenhuma solda aqui, só bornes e encaixes: os 2 fios de 5,1 V nos bornes 1 e 2 da barra de emenda; o fio azul no borne 3; o conector do fio verde no pino S do D0 e o do preto no pino G do D0; o jumper do divisor no pino S do D1; a extensão do servo de tilt no D10. No D0 e no D1, o pino do meio (V) fica vazio: ele tem os 6 V dos servos, que queimam o Raspberry Pi. Deixe 10 cm de folga para o giro. Com a cabeça olhando para a frente e o servo de pan em 90°, engrene os dentes. 4 × M3 × 10 por baixo, com a chave Allen longa. |
| 19 | porta traseira (1 M3) | por trás | 1 × M3 × 8 na orelha da tampa; o pé da porta encosta nos 2 batentes do piso. |
<!-- /GERADO -->

## Abrir para manutenção

Trocar a bateria ou mexer nas placas não exige desmontar a cabeça.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | abrir: porta traseira | Solte 1 parafuso. |
| 2 | abrir: bateria sai por trás | Desligue a chave antes. |
| 3 | abrir: tampa + pescoço + cabeça saem por cima (placas à mostra) | Solte os 4 parafusos por baixo da base e levante o conjunto inteiro, devagar: os fios do pescoço continuam ligados. |
<!-- /GERADO -->

## Energia e ligação

Pack 2S (2 × 18650, 6 a 8,4 V) → fusível retardado de 3 A (T3A) → placa de proteção BMS 2S → chave (KCD11-101, 3 A) → duas linhas separadas:

- **5,1 V do Raspberry Pi e do Arduino:** conversor LM2596 (cerca de 2 A contínuos). Mantém os 5 V até o pack cair a cerca de 6,5 V. O Arduino recebe pelos pinos + e − do conector COM do Sensor Shield.
- **6 V dos 2 servos:** UBEC de 3 A, pelo borne azul do Sensor Shield (jumper SEL retirado), com capacitor de 1000 µF.
- **Carga:** módulo USB-C com balanceamento, antes da chave, com a boca numa janela atrás da base e um 3º fio no
  ponto que une as duas células.
- **Raspberry Pi ↔ Arduino:** serial (UART) de 3 fios pelo pescoço. Pi: pinos 32 (TX), 33 (RX) e 34 (GND). Arduino:
  D0 e D1, com um divisor de 3 resistores de 1 kΩ, preso na barra de emenda da base, no fio que vai do Arduino para o Pi.

O esquema, a tabela fio a fio e os avisos de segurança estão em [LIGACAO.md](LIGACAO.md). Nada disso foi testado na
bancada.

## Verificação

Saída real de `.venv/bin/python comum/cad/verificar.py cubo` (cópia completa em `verificacao-saida.txt`):

<!-- GERADO:verificacao -->
```
== verificação: cubo
  [PASSOU] 1 contagem: 12 peças distintas, 15 no total (esperado 15); faltando 0; sobrando 0
  [PASSOU] 2 malha: 12 STL fechados, 1 corpo cada
  [PASSOU] 3 mesa: todas cabem em 256 x 256 x 256 mm; maior dimensão 158.0 mm (base)
  [PASSOU] 4 parede: modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm)
  [PASSOU] 5 interferência: 28 sólidos (14 impressos + 14 componentes), 10 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem)
  [PASSOU] 6 teste negativo: 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0)
  [PASSOU] 7 peça solta: as 14 peças montadas encostam (≤ 1.5 mm) em outra
  [PASSOU] 8 equilíbrio: massa estimada 1147 g; CG neutro em x=1.3 y=0.7 z=76.1 mm, margem 69.3 mm (tomba com 42°); pior pose 'pan+170+tilt-baixo': margem 57.5 mm (38°); mínimo exigido 10 mm
  [PASSOU] 9 caminho: 21 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado
  [PASSOU] 10 imprimibilidade: 12 peças distintas: 12 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar)
  [PASSOU] 11 negativo impr.: 'tampa-base' na orientação declarada: 0 mm² sem apoio (limite 96); girada 180° em X → 21240 mm² = 44.0 % (acusou; tem que acusar)
```
<!-- /GERADO -->

## Como regenerar

```
.venv/bin/python comum/cad/gerar.py cubo                      # STL, 3MF, mesas, montagem.json
.venv/bin/python comum/cad/verificar.py cubo                  # 11 testes
.venv/bin/python guia/src/pagina_robo.py docs cubo pt   # blocos GERADO destes arquivos
.venv/bin/python guia/src/pagina_robo.py traduzir cubo  # EN e ES pelo inema-traduz (só o que mudou)
.venv/bin/python guia/src/pagina_robo.py docs cubo      # versões .en.md e .es.md
.venv/bin/python guia/src/pagina_robo.py pagina cubo    # guia/cubo/ + en + es + esquema ligacao.<idioma>.svg
.venv/bin/python guia/src/pagina_robo.py zip cubo       # cubo-stl.zip
.venv/bin/python guia/src/pagina_robo.py conferir cubo  # links, tags, idiomas, zip
```

Os arquivos `*.en.md`, `*.es.md` e `ligacao.*.svg` são gerados: mude o texto em português (ou
`guia/src/robos/cubo.dados.json`) e rode os comandos acima.

## Pendências

- Imprimir e montar: comece pelo cupom de teste.
- Testar a parte elétrica na bancada (nenhum fio foi ligado ainda).
- Medidas NC dos componentes (tela, abas e horn do MG996R, chave, boca do USB-C): medir e corrigir `comum/cad/parametros.py`.
- Abrir os 3MF das mesas no Bambu Studio.
- O cupom de teste é comum aos outros robôs: não testa a janela do MG996R nem o furo do pino M5 (falta um cupom próprio do robô quadrado).
- O plugue USB-C que alimenta o Raspberry Pi não está no modelo 3D: conferir se cabe ao lado do Pi, dentro da cabeça.
- Os pinos 31 a 34 do Raspberry Pi ficam embaixo da tela: conferir se o conector baixo da serial cabe.
- Calor: o Raspberry Pi fica fechado numa cabeça de PLA sem ventilação; medir a temperatura em uso.
- Com o Arduino parafusado na base o cabo USB não entra: para regravar é preciso soltar os 4 parafusos dele.
- Porta-fusível, barra de emenda, resistores da serial, amplificador de áudio e microfones ainda não têm fixação modelada.
- A passagem dos 8 fios pelo garfo e pelo rasgo do fundo da cabeça nunca foi ensaiada (o rasgo do copo é fechado: os fios só saem depois de o copo entrar).
