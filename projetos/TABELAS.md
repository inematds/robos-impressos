# Tabelas geradas (não edite: rode `comum/cad/tabelas.py`)

## Resumo

| Modelo | Altura (mm) | Peças | Mesas (impressões) | Filamento total (g)* | Impressão total (h)* | Robô montado (g)* |
|---|---|---|---|---|---|---|
| Dinossauro | 300 | 34 | 12 | 1002 | 40 | 1597 |
| Capivara | 300 | 32 | 11 | 1129 | 44 | 1714 |
| Robô quadrado | 200 | 15 | 7 | 735 | 28 | 1147 |
| Robô quadrado que roda | 306 | 19 | 8 | 1143 | 43 | 2214 |

* estimativa por volume, sem fatiador


## Dinossauro — peças impressas

| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| barriga | 63 × 79 × 13 | 1 | PLA | creme | não | 22 | 0.9 |
| dedo-dir-1 | 17 × 13 × 8 | 1 | PLA | creme | não | 1 | 0.1 |
| dedo-dir-2 | 17 × 13 × 7 | 1 | PLA | creme | não | 1 | 0.1 |
| dedo-dir-3 | 13 × 17 × 7 | 1 | PLA | creme | não | 1 | 0.1 |
| dedo-esq-1 | 17 × 13 × 8 | 1 | PLA | creme | não | 1 | 0.1 |
| dedo-esq-2 | 17 × 13 × 7 | 1 | PLA | creme | não | 1 | 0.1 |
| dedo-esq-3 | 13 × 17 × 7 | 1 | PLA | creme | não | 1 | 0.1 |
| mancha-dir | 21 × 26 × 8 | 1 | PLA | verde-escuro | não | 2 | 0.1 |
| mancha-esq | 21 × 26 × 8 | 1 | PLA | verde-escuro | não | 2 | 0.1 |
| braco-dir | 28 × 59 × 16 | 1 | PLA | verde | não | 8 | 0.4 |
| braco-esq | 28 × 59 × 16 | 1 | PLA | verde | não | 8 | 0.4 |
| cubo-braco | 17 × 17 × 13 | 2 | PETG | grafite | não | 5 | 0.4 |
| corpo | 194 × 114 × 129 | 1 | PLA | verde | sim | 200 | 7.5 |
| traseira | 126 × 131 × 132 | 1 | PLA | verde | sim | 102 | 3.9 |
| gola | 112 × 100 × 56 | 1 | PLA | verde | não | 79 | 3.0 |
| crista-costas | 46 × 67 × 6 | 1 | PLA | azul | não | 10 | 0.4 |
| cranio | 134 × 174 × 118 | 1 | PLA | verde | sim | 179 | 6.8 |
| mandibula | 91 × 37 × 36 | 1 | PLA | verde | sim | 34 | 1.4 |
| mesa-cabeca | 75 × 122 × 46 | 1 | PETG | grafite | não | 29 | 1.1 |
| crista-cabeca | 105 × 128 × 6 | 1 | PLA | azul | não | 22 | 0.9 |
| olho | 44 × 44 × 23 | 1 | PLA | branco | não | 13 | 0.6 |
| olho-esq | 44 × 44 × 23 | 1 | PLA | branco | não | 15 | 0.6 |
| iris | 30 × 30 × 10 | 1 | PLA | azul | não | 4 | 0.2 |
| iris-esq | 30 × 30 × 10 | 1 | PLA | azul | não | 4 | 0.2 |
| pupila | 19 × 19 × 8 | 1 | PLA | preto | não | 2 | 0.1 |
| pupila-esq | 19 × 19 × 8 | 1 | PLA | preto | não | 2 | 0.2 |
| chassi | 106 × 179 × 121 | 1 | PETG | grafite | não | 173 | 6.4 |
| capa-esfera (comum) | 29 × 29 × 6 | 1 | PETG | grafite | não | 3 | 0.2 |
| bandeja-pi | 61 × 89 × 8 | 1 | PETG | amarelo | não | 16 | 0.7 |
| bandeja-uno | 68 × 59 × 6 | 1 | PETG | amarelo | não | 12 | 0.5 |
| garfo-pescoco (comum) | 65 × 48 × 51 | 1 | PETG | grafite | sim | 17 | 0.7 |
| berco-tilt (comum) | 38 × 23 × 77 | 1 | PETG | grafite | sim | 15 | 0.6 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 34 |  |  |  | **1002** | **40** |

* estimativa por volume, sem fatiador

### Dinossauro — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 33 peças distintas, 34 no total (esperado 34); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 33 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 194.1 mm (corpo) |
| 4 parede | PASSOU | corpo 2.27–2.62 mm; gola 2.89–9.75 mm; cabeça 2.31–2.55 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 59 sólidos (33 impressos + 26 componentes), 12 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 15 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 33 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1597 g; CG neutro em x=-0.3 y=-18.7 z=108.2 mm, margem 18.7 mm (tomba com 10°); pior pose 'tilt-baixo': margem 14.9 mm (8°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 31 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |
| 10 imprimibilidade | PASSOU | 33 peças distintas: 27 saem sem suporte; 6 com suporte declarado: cranio (12051 mm² = 9.8 %, ponte de 65 mm, 2 ponto(s) no ar), corpo (2514 mm² = 2.2 %, ponte de 20 mm, 2 ponto(s) no ar), traseira (1596 mm² = 2.4 %, ponte de 24 mm, 1 ponto(s) no ar), garfo-pescoco (1488 mm² = 16.1 %, ponte de 21 mm), berco-tilt (516 mm² = 7.0 %, ponte de 21 mm), mandibula (455 mm² = 4.9 %); 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar) |
| 11 negativo impr. | PASSOU | 'chassi' na orientação declarada: 158 mm² sem apoio (limite 163); girada 180° em X → 11537 mm² = 14.1 % (acusou; tem que acusar) |

## Capivara — peças impressas

| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| rabo | 53 × 59 × 29 | 1 | PLA | marrom | não | 21 | 0.9 |
| mao-dir | 49 × 48 × 20 | 1 | PLA | marrom | não | 11 | 0.5 |
| mao-esq | 49 × 48 × 20 | 1 | PLA | marrom | não | 11 | 0.5 |
| avental | 69 × 38 × 12 | 1 | PLA | verde-bandana | não | 9 | 0.4 |
| aro | 40 × 40 × 3 | 2 | PLA | ciano | não | 4 | 0.3 |
| miolo | 28 × 28 × 2 | 2 | PLA | preto | não | 3 | 0.3 |
| corpo | 197 × 180 × 119 | 1 | PLA | laranja | sim | 196 | 7.4 |
| porta | 76 × 37 × 119 | 1 | PLA | laranja | sim | 38 | 1.5 |
| gola | 159 × 156 × 69 | 1 | PLA | verde-bandana | não | 173 | 6.5 |
| cranio | 181 × 187 × 135 | 1 | PLA | laranja | sim | 251 | 9.4 |
| mandibula | 130 × 31 × 44 | 1 | PLA | laranja | sim | 20 | 0.8 |
| mesa-cabeca | 97 × 146 × 50 | 1 | PETG | grafite | não | 36 | 1.4 |
| olho | 48 × 48 × 24 | 1 | PLA | branco | não | 16 | 0.7 |
| olho-esq | 48 × 48 × 24 | 1 | PLA | branco | não | 18 | 0.8 |
| iris | 34 × 34 × 10 | 1 | PLA | marrom | não | 6 | 0.3 |
| iris-esq | 34 × 34 × 10 | 1 | PLA | marrom | não | 6 | 0.3 |
| pupila | 22 × 22 × 9 | 1 | PLA | preto | não | 3 | 0.2 |
| pupila-esq | 22 × 22 × 9 | 1 | PLA | preto | não | 3 | 0.2 |
| focinho | 78 × 60 × 18 | 1 | PLA | marrom | não | 25 | 1.0 |
| orelha-dir | 26 × 27 × 5 | 1 | PLA | marrom | não | 2 | 0.1 |
| orelha-esq | 26 × 27 × 5 | 1 | PLA | marrom | não | 2 | 0.1 |
| topete | 43 × 51 × 24 | 1 | PLA | laranja | não | 15 | 0.6 |
| chassi | 149 × 136 × 115 | 1 | PETG | grafite | não | 174 | 6.4 |
| capa-esfera (comum) | 29 × 29 × 6 | 2 | PETG | grafite | não | 6 | 0.4 |
| bandeja-pi | 61 × 93 × 8 | 1 | PETG | amarelo | não | 17 | 0.7 |
| bandeja-uno | 61 × 78 × 8 | 1 | PETG | amarelo | não | 16 | 0.7 |
| garfo-pescoco (comum) | 65 × 48 × 51 | 1 | PETG | grafite | sim | 17 | 0.7 |
| berco-tilt (comum) | 38 × 23 × 77 | 1 | PETG | grafite | sim | 15 | 0.6 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 32 |  |  |  | **1129** | **44** |

* estimativa por volume, sem fatiador

### Capivara — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 29 peças distintas, 32 no total (esperado 32); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 29 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 197.0 mm (corpo) |
| 4 parede | PASSOU | corpo 2.29–2.75 mm; gola 3.38–8.27 mm; cabeça 2.27–2.73 mm (mínimo exigido 2.0) |
| 5 interferência | PASSOU | 56 sólidos (31 impressos + 25 componentes), 8 poses, 0 sobreposições; 2 encaixe(s) previsto(s) fora da conta: motor-tt-dir x roda-dir (eixo do motor entra no cubo da roda); motor-tt-esq x roda-esq (eixo do motor entra no cubo da roda) |
| 6 teste negativo | PASSOU | 'chassi' deslocada 3 mm em X → 13 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 31 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1714 g; CG neutro em x=0.4 y=25.1 z=110.4 mm, margem 25.1 mm (tomba com 13°); pior pose 'pan+tilt-cima': margem 17.7 mm (9°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 26 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |
| 10 imprimibilidade | PASSOU | 29 peças distintas: 23 saem sem suporte; 6 com suporte declarado: cranio (20415 mm² = 12.0 %), garfo-pescoco (1488 mm² = 16.1 %, ponte de 21 mm), corpo (1306 mm² = 1.0 %, 4 ponto(s) no ar), berco-tilt (516 mm² = 7.0 %, ponte de 21 mm), mandibula (236 mm² = 2.1 %, ponte de 71 mm), porta (111 mm² = 0.5 %); 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar) |
| 11 negativo impr. | PASSOU | 'chassi' na orientação declarada: 84 mm² sem apoio (limite 166); girada 180° em X → 11522 mm² = 13.9 % (acusou; tem que acusar) |

## Robô quadrado — peças impressas

| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| base | 158 × 146 × 56 | 1 | PETG | grafite | não | 222 | 8.2 |
| tampa-base | 158 × 146 × 18 | 1 | PETG | grafite | não | 101 | 3.8 |
| porta-traseira | 45 × 53 × 5 | 1 | PETG | grafite | não | 9 | 0.4 |
| tubo-pescoco | 40 × 40 × 33 | 1 | PETG | prata | não | 16 | 0.7 |
| engrenagem-pescoco | 36 × 36 × 8 | 1 | PETG | prata | não | 8 | 0.3 |
| engrenagem-servo | 69 × 69 × 8 | 1 | PETG | amarelo | não | 23 | 0.9 |
| garfo | 44 × 42 × 24 | 1 | PETG | grafite | não | 19 | 0.8 |
| quadro-cabeca | 129 × 75 × 64 | 1 | PETG | amarelo | não | 65 | 2.4 |
| cabeca-corpo | 136 × 118 × 102 | 1 | PLA | branco | não | 204 | 7.7 |
| cabeca-face | 130 × 112 × 34 | 1 | PLA | preto | não | 53 | 2.0 |
| espacador-pi | 6 × 6 × 5 | 4 | PLA | cinza | não | 0 | 0.3 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 15 |  |  |  | **735** | **28** |

* estimativa por volume, sem fatiador

### Robô quadrado — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 12 peças distintas, 15 no total (esperado 15); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 12 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 158.0 mm (base) |
| 4 parede | PASSOU | modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm) |
| 5 interferência | PASSOU | 28 sólidos (14 impressos + 14 componentes), 10 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem) |
| 6 teste negativo | PASSOU | 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 14 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 1147 g; CG neutro em x=1.3 y=0.7 z=76.1 mm, margem 69.3 mm (tomba com 42°); pior pose 'pan+170+tilt-baixo': margem 57.5 mm (38°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 21 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |
| 10 imprimibilidade | PASSOU | 12 peças distintas: 12 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar) |
| 11 negativo impr. | PASSOU | 'tampa-base' na orientação declarada: 0 mm² sem apoio (limite 96); girada 180° em X → 21240 mm² = 44.0 % (acusou; tem que acusar) |

## Robô quadrado que roda — peças impressas

| Peça | Tamanho deitada (mm) | Qtd | Material | Cor | Suporte | Filamento (g)* | Tempo (h)* |
|---|---|---|---|---|---|---|---|
| base-rodas | 130 × 182 × 72 | 1 | PETG | grafite | não | 266 | 9.8 |
| tampa-bateria | 108 × 84 × 7 | 1 | PETG | grafite | não | 34 | 1.3 |
| capa-esfera | 57 × 47 × 12 | 1 | PETG | grafite | não | 9 | 0.4 |
| flange-motor | 62 × 62 × 4 | 2 | PETG | grafite | não | 28 | 1.2 |
| deck | 127 × 179 × 30 | 1 | PETG | grafite | não | 97 | 3.6 |
| tronco | 130 × 182 × 58 | 1 | PETG | branco | não | 236 | 8.7 |
| tubo-pescoco | 40 × 40 × 37 | 1 | PETG | prata | não | 17 | 0.7 |
| engrenagem-pescoco | 36 × 36 × 8 | 1 | PETG | prata | não | 8 | 0.3 |
| engrenagem-servo | 69 × 69 × 8 | 1 | PETG | amarelo | não | 23 | 0.9 |
| garfo | 44 × 42 × 24 | 1 | PETG | grafite | não | 19 | 0.8 |
| quadro-cabeca | 145 × 94 × 63 | 1 | PETG | amarelo | não | 85 | 3.2 |
| cabeca-corpo | 152 × 128 × 110 | 1 | PLA | branco | não | 248 | 9.3 |
| cabeca-face | 146 × 122 × 43 | 1 | PLA | preto | não | 57 | 2.2 |
| espacador-pi | 6 × 6 × 4 | 4 | PLA | cinza | não | 0 | 0.3 |
| teste-encaixe (comum) | 70 × 34 × 8 | 1 | PLA | cinza | não | 15 | 0.6 |
| **Total** |  | 19 |  |  |  | **1143** | **43** |

* estimativa por volume, sem fatiador

### Robô quadrado que roda — verificação

| Teste | Resultado |  |
|---|---|---|
| 1 contagem | PASSOU | 15 peças distintas, 19 no total (esperado 19); faltando 0; sobrando 0 |
| 2 malha | PASSOU | 15 STL fechados, 1 corpo cada |
| 3 mesa | PASSOU | todas cabem em 256 x 256 x 256 mm; maior dimensão 182.0 mm (base-rodas) |
| 4 parede | PASSOU | modelo sem casca orgânica (paredes são sólidos exatos ≥ 2,4 mm) |
| 5 interferência | PASSOU | 41 sólidos (18 impressos + 23 componentes), 11 poses, 0 sobreposições; 1 encaixe(s) previsto(s) fora da conta: engrenagem-servo x servo-pan MG996R (horn do servo fica no rebaixo da engrenagem) |
| 6 teste negativo | PASSOU | 'quadro-cabeca' deslocada 3 mm em X → 2 sobreposições acusadas (tem que ser > 0) |
| 7 peça solta | PASSOU | as 18 peças montadas encostam (≤ 1.5 mm) em outra |
| 8 equilíbrio | PASSOU | massa estimada 2214 g; CG neutro em x=1.0 y=-41.1 z=127.4 mm, margem 41.1 mm (tomba com 18°); pior pose 'pan+170+tilt-baixo': margem 37.6 mm (17°); mínimo exigido 10 mm |
| 9 caminho | PASSOU | 26 passos (montagem + abertura para manutenção), cada peça entra ou sai pela direção declarada sem atravessar o que está montado |
| 10 imprimibilidade | PASSOU | 15 peças distintas: 15 saem sem suporte; 0 com suporte declarado; 0 REPROVADA(S) (declaradas sem suporte, mas com área sem apoio acima de max(30 mm², 0.2 % da área) a mais de 45° ou ponto que nasce no ar) |
| 11 negativo impr. | PASSOU | 'deck' na orientação declarada: 0 mm² sem apoio (limite 106); girada 180° em X → 19084 mm² = 36.1 % (acusou; tem que acusar) |
