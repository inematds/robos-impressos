# Robô quadrado de mesa (`cubo`)

Robô de mesa para imprimir na Bambu Lab A1 e montar em casa. A cabeça é um cubo com tela de 3,5" no rosto; gira
±170° e inclina de −25° a +30°. Dentro vão um Raspberry Pi, um Arduino Uno, dois servos MG996R e um pack de duas
baterias 18650 que carrega por USB-C. Não roda. Fase 1 = mecânica e encaixe; a programação é a fase 2.

**Nada foi impresso ainda.** As peças foram conferidas por 11 testes no computador (resultado no fim).

<!-- GERADO:numeros -->
- Altura montado: 200,5 mm.
- Peças impressas: 15 (12 arquivos diferentes), em 7 mesas.
- Filamento: 735 g. Tempo de impressão: 28,2 h. As duas contas são estimativas por volume, sem fatiador.
- Insertos M3 a quente: 16.
<!-- /GERADO -->

| Para | Onde |
|---|---|
| Ver o robô e seguir o guia | https://inematds.github.io/robos-impressos/guia/cubo/ (também em `/guia/en/cubo/` e `/guia/es/cubo/`) |
| Comprar | [LISTA-DE-COMPRAS.md](LISTA-DE-COMPRAS.md) |
| Imprimir | [IMPRIMIR.md](IMPRIMIR.md) |
| Baixar tudo | [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip) (STL + 3MF das mesas) |
| STL, 3MF, mesas | `pecas/cubo/stl/`, `pecas/cubo/3mf/`, `pecas/cubo/mesas/` (+ `pecas/comum/stl/comum-teste-encaixe.stl`) |
| Modelo | `cad/modelos/cubo.py`, `cad/comum/quadrado.py`, seção `CUBO` de `cad/parametros.py` |

## Montagem

Comece pelos 16 insertos M3 a quente. Depois siga a ordem abaixo, que é a que o verificador testou (teste 9): cada
peça entra pelo lado indicado sem bater no que já está montado. Os passos com "(bancada)" são feitos fora do robô.

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
| 1 | base | por cima | Antes de começar, assente os 16 insertos a quente (lista na tabela de parafusos). |
| 2 | servo de pan nos 2 postes | por cima | 4 × M3 × 12, eixo para cima. Ligue o servo e deixe-o no centro (90°) antes de pôr a engrenagem. |
| 3 | Arduino Uno nos 4 ressaltos | por cima | 4 × M3 × 8, USB virado para a esquerda. O shield encaixa por cima. |
| 4 | módulos de energia nos berços (1 abraçadeira cada) | por cima | Solde os fios antes de prender. 3 abraçadeiras (conversor, UBEC, carregador) e fita dupla-face na placa de proteção. A boca USB-C do carregador encosta na janela de trás. |
| 5 | chave (por fora, atrás) | por trás | Encaixa por pressão no recorte. |
| 6 | alto-falante nos trilhos da parede de trás | por cima | Fase 2: pode pular agora. |
| 7 | engrenagem do servo no horn | por cima | Horn redondo no rebaixo da engrenagem, 4 × M2 × 8 pelos rasgos e o parafuso central do servo pelo furo de 6 mm. |
| 8 | bateria (pela porta de trás) | por trás | Confira a polaridade com o multímetro antes de ligar a chave. |
| 9 | Raspberry Pi e espaçadores no quadro (bancada) | pela frente | 4 × M2,5 × 12 com porca; os 4 espaçadores ficam entre o Pi e a travessa. Grave o cartão microSD antes. |
| 10 | tela, painel do rosto e câmera pela frente; 4 M3 por trás do quadro, ANTES do servo (bancada) | pela frente | A tela encaixa nos pinos do Pi. 4 × M3 × 8 por trás da travessa, nos insertos dos pilares do painel. Depois que o servo entra, esses parafusos ficam sem acesso. |
| 11 | servo de tilt no rasgo do quadro, por trás; 4 parafusos pela esquerda (bancada) | por trás | 4 × M3 × 12. Os 2 de cima são apertados pelos furos de acesso da lateral esquerda. |
| 12 | garfo (com o horn já preso no braço) no eixo do tilt, por baixo; parafuso central do horn pelo furo do pino; pino M5 (bancada) | por baixo | Prenda o horn no braço direito do garfo com 4 × M2 × 8. O parafuso central do horn entra pelo furo do pino. Por último, o M5 × 16: aperte até encostar e volte um quarto de volta, porque a cabeça gira nele. |
| 13 | copo da cabeça por trás; 4 M3 na parede de trás (bancada) | por trás | 4 × M3 × 8. |
| 14 | tubo do pescoço na tampa, por cima (bancada) | por cima | A flange cônica apoia na tampa. |
| 15 | engrenagem do pescoço por baixo da tampa (bancada) | por baixo | Alinhe os 3 furos com os do tubo. |
| 16 | cabeça sobre o tubo; 3 tirantes M3 por baixo (bancada) | por cima | Passe os cabos pelo furo de 9 mm do pescoço ANTES de fechar. 3 × M3 × 45 por baixo da engrenagem, até os insertos do garfo. |
| 17 | tampa + pescoço + cabeça sobre a base; 4 M3 por baixo | por cima | Com a cabeça olhando para a frente e o servo no centro, engrene os dentes. 4 × M3 × 10 por baixo, com a chave Allen longa. |
| 18 | porta traseira (1 M3) | por trás | 1 × M3 × 8 na orelha da tampa; o pé da porta encosta nos 2 batentes do piso. |
<!-- /GERADO -->

## Abrir para manutenção

Trocar a bateria ou mexer nas placas não exige desmontar a cabeça.

<!-- GERADO:abrir -->
| # | Passo | Parafusos e atenção |
|---|---|---|
| 1 | abrir: porta traseira | Solte 1 parafuso. |
| 2 | abrir: bateria sai por trás | Desligue a chave antes. |
| 3 | abrir: tampa + pescoço + cabeça saem por cima (placas à mostra) | Solte os 4 parafusos por baixo da base e levante o conjunto inteiro. |
<!-- /GERADO -->

## Energia

Pack 2S (2 × 18650, 6 a 8,4 V) → placa de proteção BMS 2S e chave → duas linhas separadas:

- **5 V do Raspberry Pi:** conversor LM2596. Mantém os 5 V até o pack cair a cerca de 6,5 V. Ajuste em 5,1 V com o
  multímetro antes de ligar o Pi. Limite de 3 A: Pi 4, ou Pi 5 sem USB pesada.
- **6 V dos 2 servos:** UBEC de 3 A, com capacitor de 1000 µF na saída.
- **Carga:** módulo USB-C com balanceamento, com a boca numa janela atrás da base. Pede um 3º fio no ponto que une
  as duas células.

O esquema fio a fio e o teste elétrico ainda não foram feitos.

## Verificação

Saída real de `.venv/bin/python cad/verificar.py cubo` (cópia completa em `verificacao-saida.txt`):

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
.venv/bin/python cad/gerar.py cubo                      # STL, 3MF, mesas, montagem.json
.venv/bin/python cad/verificar.py cubo                  # 11 testes
.venv/bin/python guia/src/pagina_robo.py docs cubo      # tabelas destes arquivos
.venv/bin/python guia/src/pagina_robo.py zip cubo       # cubo-stl.zip
.venv/bin/python guia/src/pagina_robo.py pagina cubo    # guia/cubo/ + en + es
```

## Pendências

- Imprimir e montar: comece pelo `teste-encaixe`.
- Medidas NC dos componentes (tela, abas e horn do MG996R, chave, boca do USB-C): medir e corrigir `cad/parametros.py`.
- Abrir os 3MF das mesas no Bambu Studio.
- O cupom `teste-encaixe` é comum aos bichos: não testa a janela do MG996R nem o furo do pino M5 (falta um cupom próprio do robô quadrado).
- O plugue USB-C que alimenta o Raspberry Pi não está no modelo 3D: conferir se cabe ao lado do Pi, dentro da cabeça.
- Esquema elétrico fio a fio e ligação Raspberry Pi ↔ Arduino (o furo de cabos do pescoço tem 9 mm: plugue USB não
  passa; passe os fios soltos e ponha os conectores depois).
- Amplificador de áudio e microfones da fase 2 ainda não têm fixação modelada.
