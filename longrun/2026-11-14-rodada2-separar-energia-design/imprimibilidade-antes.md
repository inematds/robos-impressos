# Imprimibilidade — estado ANTES das correções

Gerado em 14/11/2026 10:12 por `cad/comum/imprimibilidade.py --md` sobre os STL de `pecas/` (orientação de impressão declarada em cada peça).

Limites (`cad/parametros.py › IMPRESSAO_LIMITES`): balanço > 45° da vertical (+1° de tolerância); mesa = |z| < 0.3 mm; ponte plana até 20 mm; teto de furo/rasgo até 6 mm de vão; beira até 1 mm; região < 4 mm² ignorada; **precisa de suporte se a área sem apoio > max(30 mm², 0.2 % da área da peça) ou se algo nasce no ar**.

Veredito: **REPROVADA** = declarada sem suporte, mas o cálculo diz que precisa (é a lista de trabalho); *precisa de suporte (declarado)* = coerente, mas a ordem 9 pede reduzir; *ok sem suporte* = passa.

Coluna "onde": caixas em mm na ORIENTAÇÃO DE IMPRESSÃO (X, Y da mesa; Z = altura na mesa). A caixa na posição de montagem está em `pecas/<modelo>/verificacao.json › imprimibilidade › <peça> › regioes › caixa_montagem`.

## dino — Dinossauro (peças só deste modelo; STL lidos às 10:12:52)

| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |
|---|---|---:|---:|---:|---|---|
| cranio | sim (árvore) | 17039 | 13.3 | 6 | precisa de suporte (declarado) | teto 8375 mm² em x -58..58, y -71..31, z 93..118, vão 56; teto 2880 mm² em x -43..43, y 40..78, z 63..86, vão 89; balanço livre 1138 mm² em x 18..54, y 4..40, z 67..75, fundo 33; +18 regiões |
| torso-costas | sim (árvore, por dentro) | 16293 | 17.2 | 0 | precisa de suporte (declarado) | teto 15514 mm² em x -48..48, y -104..102, z 41..71, vão 206; balanço livre 328 mm² em x -5..5, y -19..22, z 64..68, fundo 29; teto 138 mm² em x -22..22, y 111..113, z 24..32, vão 45; +8 regiões |
| torso-frente | sim (árvore, por dentro) | 11676 | 13.7 | 0 | precisa de suporte (declarado) | teto 6647 mm² em x -38..38, y -102..-5, z 36..56, vão 77; balanço livre 1221 mm² em x -41..41, y 21..80, z 59..77, vão 11; teto 1137 mm² em x -29..28, y 69..103, z 56..78, vão 41; +14 regiões; nasce no ar em (-33.1, 0.3, 48.5) (saliência 3.1 mm); nasce no ar em (33.1, 0.3, 48.5) (saliência 3.3 mm) |
| cauda | não | 5924 | 15.7 | 0 | REPROVADA | teto 3513 mm² em x -32..32, y -48..45, z 37..67, vão 66; balanço livre 1647 mm² em x -35..35, y -49..51, z 0..14, vão 11; balanço livre 452 mm² em x -5..5, y -25..12, z 40..57, nasce no ar; +4 regiões |
| barriga | sim (árvore) | 5011 | 29.4 | 30 | precisa de suporte (declarado) | balanço livre 1846 mm² em x -39..39, y -12..12, z 0..16, vão 69; balanço livre 825 mm² em x -31..31, y 27..44, z 13..22, nasce no ar; balanço livre 786 mm² em x -38..38, y -25..-14, z 0..5, vão 30; +3 regiões; nasce no ar em (21.2, 17.0, 13.2) (saliência 0.6 mm); nasce no ar em (9.8, 34.1, 19.7) (saliência 0.9 mm) |
| mandibula | sim (árvore, por fora) | 3892 | 21.5 | 0 | precisa de suporte (declarado) | balanço livre 3892 mm² em x -47..46, y -29..18, z 0..18, vão 8 |
| perna-esq | não | 1707 | 4.5 | 0 | REPROVADA | teto 1071 mm² em x -7..20, y -46..7, z 101..111, vão 54; balanço livre 228 mm² em x -16..18, y 38..58, z 1..6, fundo 8; balanço livre 218 mm² em x 2..11, y 32..57, z 10..10, fundo 26; +4 regiões |
| perna-dir | não | 1706 | 4.5 | 0 | REPROVADA | teto 1071 mm² em x -20..7, y -46..7, z 101..111, vão 54; balanço livre 228 mm² em x -18..16, y 38..58, z 1..6, fundo 8; balanço livre 217 mm² em x -11..-2, y 32..57, z 10..10, fundo 26; +4 regiões |
| braco-dir | sim (pouco) | 936 | 14.2 | 8 | precisa de suporte (declarado) | balanço livre 888 mm² em x -16..15, y -34..29, z 0..16, vão 45; balanço livre 29 mm² em x 4..10, y 30..35, z 1..2, nasce no ar; balanço livre 11 mm² em x 11..14, y 32..35, z 7..8, fundo 4; +2 regiões |
| braco-esq | sim (pouco) | 932 | 14.1 | 8 | precisa de suporte (declarado) | balanço livre 884 mm² em x -15..16, y -34..29, z 0..16, vão 45; balanço livre 29 mm² em x -10..-4, y 30..35, z 1..2, nasce no ar; balanço livre 11 mm² em x -14..-11, y 32..35, z 7..8, fundo 4; +2 regiões |
| olho | não | 662 | 9.4 | 0 | REPROVADA | balanço livre 528 mm² em x -16..16, y -10..12, z 0..7, fundo 14; teto 133 mm² em x -5..12, y 2..12, z 39..43, vão 19 |
| olho-esq | não | 662 | 9.4 | 0 | REPROVADA | balanço livre 528 mm² em x -16..16, y -10..12, z 0..7, fundo 14; teto 133 mm² em x -12..5, y 2..12, z 39..43, vão 19 |
| iris | não | 232 | 9.5 | 0 | REPROVADA | balanço livre 174 mm² em x -9..10, y -3..8, z 0..6, nasce no ar; teto 57 mm² em x -4..6, y -2..5, z 22..24, vão 11 |
| iris-esq | não | 231 | 9.5 | 0 | REPROVADA | balanço livre 174 mm² em x -10..9, y -3..8, z 0..6, nasce no ar; teto 57 mm² em x -5..4, y -2..6, z 22..24, vão 11 |
| pupila | não | 89 | 11.2 | 0 | REPROVADA | balanço livre 89 mm² em x -6..6, y -2..6, z 0..4, nasce no ar |
| pupila-esq | não | 89 | 11.2 | 0 | REPROVADA | balanço livre 89 mm² em x -6..6, y -2..6, z 0..4, nasce no ar |
| mesa-cabeca | não | 65 | 0.3 | 24 | REPROVADA | ponte longa 65 mm² em x 24..27, y -61..-40, z 34..34, vão 24 |
| crista-costas | não | 0 | 0.0 | 0 | ok sem suporte | – |
| unha | não | 0 | 0.0 | 0 | ok sem suporte | – |
| crista-cauda | não | 0 | 0.0 | 0 | ok sem suporte | – |
| crista-cabeca | não | 0 | 0.0 | 0 | ok sem suporte | – |

## capivara — Capivara (peças só deste modelo; STL lidos às 10:12:56)

| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |
|---|---|---:|---:|---:|---|---|
| cranio | sim (árvore) | 17790 | 14.6 | 69 | precisa de suporte (declarado) | teto 11863 mm² em x -60..61, y -72..52, z 77..112, vão 118; balanço livre 984 mm² em x 26..58, y 7..40, z 49..56, nasce no ar; balanço livre 984 mm² em x -58..-26, y 7..40, z 49..56, nasce no ar; +12 regiões; nasce no ar em (-16.8, 87.3, 37.9) (saliência 1.0 mm); nasce no ar em (29.6, 81.0, 42.9) (saliência 1.0 mm) |
| torso-costas | sim (árvore, por dentro) | 17232 | 17.9 | 0 | precisa de suporte (declarado) | teto 16788 mm² em x -55..55, y -102..102, z 41..72, vão 204; teto 137 mm² em x -21..21, y 111..113, z 24..32, vão 45; balanço livre 76 mm² em x -5..5, y 10..19, z 46..46, nasce no ar; +6 regiões |
| torso-frente | sim (árvore, por dentro) | 12955 | 14.1 | 0 | precisa de suporte (declarado) | teto 8590 mm² em x -56..57, y -102..37, z 35..68, vão 85; teto 2239 mm² em x -53..53, y 37..102, z 59..94, vão 66; balanço livre 1282 mm² em x -44..44, y 34..80, z 66..80, fundo 56; +11 regiões; nasce no ar em (-26.8, -6.2, 50.4) (saliência 1.3 mm); nasce no ar em (26.8, -6.2, 50.4) (saliência 3.3 mm) |
| barriga | sim (árvore) | 5388 | 31.1 | 0 | precisa de suporte (declarado) | balanço livre 5387 mm² em x -39..39, y -44..43, z 0..26, vão 60; balanço livre 1 mm² em x -18..-17, y 22..23, z 16..16, fundo 2; nasce no ar em (-6.9, 4.5, 2.4) (saliência 0.9 mm); nasce no ar em (16.6, 28.8, 20.4) (saliência 1.1 mm) |
| rabo | sim (só sob as 2 orelhas) | 3208 | 13.7 | 0 | precisa de suporte (declarado) | teto 2728 mm² em x -31..31, y -25..24, z 37..48, vão 65; balanço livre 161 mm² em x 16..35, y 15..24, z 10..10, fundo 20; balanço livre 158 mm² em x -35..-16, y 15..24, z 10..10, fundo 20; +4 regiões |
| mandibula | sim (árvore, por fora) | 2967 | 20.8 | 0 | precisa de suporte (declarado) | balanço livre 2962 mm² em x -39..38, y -26..21, z 0..19, vão 45; balanço livre 5 mm² em x 33..36, y -28..-25, z 14..14, fundo 3; balanço livre 0 mm² em x -44..-44, y -23..-23, z 22..22, fundo 1 |
| bandana-frente | sim (árvore) | 2400 | 24.7 | 0 | precisa de suporte (declarado) | balanço livre 2400 mm² em x -41..41, y -22..23, z 0..17, fundo 62 |
| bandana-costas | sim (árvore) | 1832 | 20.1 | 27 | precisa de suporte (declarado) | balanço livre 443 mm² em x 12..41, y -17..0, z 10..24, vão 7; balanço livre 440 mm² em x -41..-12, y -17..0, z 10..24, vão 8; balanço livre 285 mm² em x 5..29, y -5..18, z 3..7, fundo 30; +6 regiões |
| coxa-esq | sim (só sob as 2 orelhas) | 1724 | 6.6 | 0 | precisa de suporte (declarado) | teto 1476 mm² em x -7..22, y -40..42, z 64..79, vão 85; balanço livre 116 mm² em x 4..13, y 36..50, z 10..10, fundo 15; balanço livre 63 mm² em x 4..10, y -53..-38, z 10..10, fundo 15; +3 regiões |
| coxa-dir | sim (só sob as 2 orelhas) | 1723 | 6.6 | 0 | precisa de suporte (declarado) | teto 1476 mm² em x -22..7, y -40..42, z 63..79, vão 85; balanço livre 116 mm² em x -13..-4, y 36..50, z 10..10, fundo 15; balanço livre 63 mm² em x -10..-4, y -53..-38, z 10..10, fundo 15; +3 regiões |
| focinho | sim (árvore) | 1590 | 17.9 | 0 | precisa de suporte (declarado) | balanço livre 1589 mm² em x -34..34, y -20..9, z 0..14, fundo 30; balanço livre 1 mm² em x 12..14, y 17..17, z 25..25, fundo 2; balanço livre 1 mm² em x -14..-12, y 17..17, z 25..25, fundo 2 |
| olho-esq | não | 527 | 10.1 | 0 | REPROVADA | balanço livre 442 mm² em x -14..14, y -9..11, z 0..6, fundo 12; teto 85 mm² em x -11..8, y 3..9, z 35..39, vão 21 |
| olho | não | 526 | 10.1 | 0 | REPROVADA | balanço livre 442 mm² em x -14..14, y -9..11, z 0..6, fundo 12; teto 84 mm² em x -8..11, y 3..9, z 35..39, vão 22 |
| pata-dir | não | 338 | 7.2 | 0 | REPROVADA | balanço livre 338 mm² em x -18..18, y -17..15, z 0..4, fundo 6 |
| pata-esq | não | 338 | 7.2 | 0 | REPROVADA | balanço livre 338 mm² em x -18..18, y -17..15, z 0..4, fundo 6 |
| iris | não | 176 | 7.5 | 0 | REPROVADA | balanço livre 123 mm² em x -10..11, y -2..4, z 0..5, nasce no ar; teto 54 mm² em x -6..7, y -2..4, z 24..26, vão 14 |
| iris-esq | não | 176 | 7.5 | 0 | REPROVADA | balanço livre 123 mm² em x -11..10, y -2..4, z 0..5, nasce no ar; teto 54 mm² em x -7..5, y -2..4, z 24..26, vão 14 |
| pupila | não | 85 | 8.6 | 0 | REPROVADA | balanço livre 85 mm² em x -7..7, y -2..4, z 0..4, nasce no ar |
| pupila-esq | não | 85 | 8.6 | 0 | REPROVADA | balanço livre 85 mm² em x -7..7, y -2..4, z 0..4, nasce no ar |
| mesa-cabeca | não | 65 | 0.3 | 24 | REPROVADA | ponte longa 65 mm² em x 15..18, y -62..-42, z 31..31, vão 24 |
| mao | não | 0 | 0.0 | 0 | ok sem suporte | – |
| aro | não | 0 | 0.0 | 0 | ok sem suporte | – |
| orelha | não | 0 | 0.0 | 0 | ok sem suporte | – |
| topete | não | 0 | 0.0 | 0 | ok sem suporte | – |

## cubo — Robô quadrado de mesa (peças só deste modelo; STL lidos às 10:12:57)

| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |
|---|---|---:|---:|---:|---|---|
| cabeca-corpo | não | 9730 | 10.6 | 107 | REPROVADA | ponte longa 9422 mm² em x -52..52, y -47..47, z 87..87, vão 107; balanço livre 73 mm² em x 41..51, y -45..-35, z 5..5, fundo 12; balanço livre 73 mm² em x -51..-41, y 35..45, z 5..5, fundo 12; +5 regiões |
| cabeca-face | não | 5716 | 25.6 | 103 | REPROVADA | ponte longa 4278 mm² em x -50..50, y -44..44, z 40..40, vão 103; balanço livre 754 mm² em x -53..53, y -47..47, z 35..35, nasce no ar; balanço livre 603 mm² em x -56..56, y -50..50, z 40..40, fundo 3; +5 regiões |
| quadro-cabeca | não | 4356 | 24.3 | 86 | REPROVADA | balanço livre 3828 mm² em x -47..47, y -30..30, z 52..52, vão 86; ponte longa 514 mm² em x 12..46, y -14..5, z 54..54, vão 30; balanço livre 14 mm² em x -41..-40, y -8..-0, z 37..39, fundo 2 |
| base | não | 640 | 0.6 | 32 | REPROVADA | balanço livre 148 mm² em x -54..-22, y 65..68, z 7..14, fundo 4; teto 114 mm² em x -51..-25, y 65..68, z 45..50, vão 29; ponte longa 90 mm² em x -53..-23, y 69..72, z 31..31, vão 32; +4 regiões |
| garfo | não | 156 | 0.8 | 0 | REPROVADA | teto 50 mm² em x -4..4, y 37..41, z 18..19, vão 10; balanço livre 34 mm² em x -66..-62, y -42..-37, z 0..3, fundo 7; balanço livre 34 mm² em x 62..66, y -42..-37, z 0..3, fundo 7; +5 regiões |
| tubo-pescoco | não | 134 | 1.9 | 0 | REPROVADA | balanço livre 134 mm² em x -18..18, y -18..18, z 2..2, fundo 4 |
| engrenagem-servo | não | 113 | 1.1 | 21 | REPROVADA | ponte longa 113 mm² em x -9..9, y -9..9, z 3..3, vão 21 |
| tampa-base | não | 0 | 0.0 | 0 | ok sem suporte | – |
| porta-traseira | não | 0 | 0.0 | 0 | ok sem suporte | – |
| espacador-pi | não | 0 | 0.0 | 0 | ok sem suporte | – |

## comum — peças iguais em mais de um modelo (`pecas/comum`)

| peça | suporte declarado | sem apoio (mm²) | % da área | maior ponte (mm) | veredito | onde está o problema |
|---|---|---:|---:|---:|---|---|
| bandeja-uno (dino, capivara) | não | 4478 | 39.4 | 0 | REPROVADA | balanço livre 4478 mm² em x -30..31, y -45..44, z 8..8, fundo 74 |
| bandeja-pi (dino, capivara) | não | 3950 | 38.4 | 0 | REPROVADA | balanço livre 3950 mm² em x -30..31, y -45..45, z 8..8, fundo 74 |
| chassi (dino, capivara) | não | 2153 | 2.2 | 58 | REPROVADA | balanço livre 1432 mm² em x -28..28, y -29..51, z 124..124, vão 35; ponte longa 167 mm² em x -27..27, y 40..43, z 27..27, vão 58; teto 78 mm² em x -4..4, y -85..-76, z 6..7, vão 12; +17 regiões; nasce no ar em (-4.9, -28.7, 115.5) (saliência 8.5 mm) |
| garfo-pescoco (dino, capivara) | não | 1488 | 16.1 | 21 | REPROVADA | balanço livre 1318 mm² em x -29..32, y -23..24, z 2..2, fundo 18; ponte longa 136 mm² em x -8..11, y -9..9, z 2..2, vão 21; balanço livre 19 mm² em x 30..32, y -3..3, z 32..33, nasce no ar; +3 regiões |
| berco-tilt (dino, capivara) | sim (pouco, sob a ponte) | 516 | 7.0 | 21 | precisa de suporte (declarado) | balanço livre 440 mm² em x -19..13, y -11..10, z 15..15, fundo 16; ponte longa 75 mm² em x 9..13, y -10..9, z 69..69, vão 21 |
| pino-guia (dino, capivara) | não | 0 | 0.0 | 0 | ok sem suporte | – |
| bucha-eixo (dino, capivara) | não | 0 | 0.0 | 0 | ok sem suporte | – |
| capa-esfera (dino, capivara) | não | 0 | 0.0 | 0 | ok sem suporte | – |
| teste-encaixe (dino, capivara, cubo) | não | 0 | 0.0 | 0 | ok sem suporte | – |

## Resumo

- 64 peças distintas analisadas: **15 passam sem suporte**, **30 REPROVADAS**, 19 com suporte declarado e necessário, 0 com suporte declarado sem necessidade pelo cálculo.

### As 10 piores (área sem apoio)

| # | peça | suporte declarado | sem apoio (mm²) | % | veredito |
|---:|---|---|---:|---:|---|
| 1 | capivara/cranio | sim (árvore) | 17790 | 14.6 | precisa de suporte (declarado) |
| 2 | capivara/torso-costas | sim (árvore, por dentro) | 17232 | 17.9 | precisa de suporte (declarado) |
| 3 | dino/cranio | sim (árvore) | 17039 | 13.3 | precisa de suporte (declarado) |
| 4 | dino/torso-costas | sim (árvore, por dentro) | 16293 | 17.2 | precisa de suporte (declarado) |
| 5 | capivara/torso-frente | sim (árvore, por dentro) | 12955 | 14.1 | precisa de suporte (declarado) |
| 6 | dino/torso-frente | sim (árvore, por dentro) | 11676 | 13.7 | precisa de suporte (declarado) |
| 7 | cubo/cabeca-corpo | não | 9730 | 10.6 | REPROVADA |
| 8 | dino/cauda | não | 5924 | 15.7 | REPROVADA |
| 9 | cubo/cabeca-face | não | 5716 | 25.6 | REPROVADA |
| 10 | capivara/barriga | sim (árvore) | 5388 | 31.1 | precisa de suporte (declarado) |
