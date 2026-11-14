# Tabelas geradas (não edite: rode `cad/tabelas.py`)

## Resumo

| Modelo | Altura (mm) | Peças | Mesa | Filamento total (g)* | Impressão total (h)* | Robô montado (g)* |
|---|---|---|---|---|---|---|
| Dinossauro | 329 | 38 | 12 | 1107 | 44 | 1666 |
| Capivara | 326 | 39 | 13 | 1049 | 42 | 1581 |
| Robô quadrado | 201 | 14 | 8 | 638 | 25 | 1020 |

* estimativa por volume, sem fatiador


## Dinossauro — peças impressas

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
| **Total** |  | 38 |  |  |  | **1107** | **44** |

* estimativa por volume, sem fatiador

### Dinossauro — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 30 peças distintas, 38 no total (esperado 38); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 30 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 226.4 mm (torso-frente) |
| 4 parede | PASSOU | torso 2.36–2.41 mm; cabeça 2.36–2.42 mm; perna 2.35–2.41 mm; cauda 2.35–2.41 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 54 sólidos (37 impressos + 17 componentes), 12 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 13 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 37 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1666 g; CG neutro em x=0.1 y=-26.1 z=118.2 mm, margem 26.1 mm (tomba com 12°); pior pose 'tilt-baixo': margem 22.1 mm (11°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 31 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |

## Capivara — peças impressas

| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| torso-frente | 156 × 226 × 96 | 1 | PLA | laranja | sim | 133 | 5.0 |
| torso-costas | 156 × 226 × 74 | 1 | PLA | laranja | sim | 139 | 5.3 |
| barriga | 79 × 87 × 29 | 1 | PLA | laranja | sim | 26 | 1.1 |
| bandana-frente | 119 × 47 × 60 | 1 | PLA | verde-bandana | sim | 9 | 0.4 |
| bandana-costas | 119 × 38 × 67 | 1 | PLA | verde-bandana | sim | 10 | 0.5 |
| mao | 20 × 20 × 11 | 2 | PLA | marrom | não | 5 | 0.3 |
| pino-guia (comum) | 4 × 4 × 9 | 4 | PLA | cinza | não | 0 | 0.3 |
| coxa-dir | 46 × 119 × 82 | 1 | PLA | laranja | sim | 37 | 1.5 |
| coxa-esq | 46 × 119 × 82 | 1 | PLA | laranja | sim | 37 | 1.5 |
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
| **Total** |  | 39 |  |  |  | **1049** | **42** |

* estimativa por volume, sem fatiador

### Capivara — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 33 peças distintas, 39 no total (esperado 39); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 33 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 226.4 mm (torso-frente) |
| 4 parede | PASSOU | torso 2.36–2.41 mm; cabeça 2.36–2.41 mm; coxa 2.36–2.40 mm; rabo 2.36–2.41 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 53 sólidos (38 impressos + 15 componentes), 8 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 12 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 38 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1581 g; CG neutro em x=-0.0 y=-24.9 z=117.4 mm, margem 24.9 mm (tomba com 12°); pior pose 'tilt-baixo': margem 21.0 mm (10°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 27 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |

## Robô quadrado — peças impressas

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

### Robô quadrado — verificação

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
| 9 caminho | PASSOU | 12 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |
