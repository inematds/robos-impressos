# Semelhança com as imagens de referência (IoU de silhueta)

Gerado por `cad/comparar.py` (não edite à mão). IoU = área comum ÷ área total das duas silhuetas, de 0 a 1: quanto maior, mais parecido o contorno. Mede só o CONTORNO em cada vista, não cor nem detalhe.

Protocolo v1: projeção ortográfica, silhuetas com 400 px de altura, base na mesma linha e centro horizontal coincidente; melhor azimute em nominal ± 25° (passo 5°) e elevação em nominal ± 10° (passo 5°). Entram as peças impressas + rodas/esfera, pose neutra. "Ajustado" = número secundário, deixando escala (±12%) e posição variarem.

## capivara

| vista | antes: IoU | antes: ajustado | antes: az/el |
|---|---:|---:|---|
| frente | 0,783 | 0,804 | 10°/5° |
| tres-quartos | 0,784 | 0,786 | -70°/10° |
| lado | 0,736 | 0,737 | -70°/10° |
| costas | 0,803 | 0,818 | 170°/5° |
| **média** | **0,777** | **0,786** |  |

- `antes`: .preview/v102/pecas/capivara · 2026-11-14 · tag v1.0.2

## cubo

| vista | antes: IoU | antes: ajustado | antes: az/el |
|---|---:|---:|---|
| tres-quartos | 0,755 | 0,773 | 10°/32° |
| **média** | **0,755** | **0,773** |  |

- `antes`: .preview/v102/pecas/cubo · 2026-11-14 · tag v1.0.2

## dino

| vista | antes: IoU | antes: ajustado | antes: az/el |
|---|---:|---:|---|
| frente | 0,875 | 0,875 | 0°/15° |
| tres-quartos-a | 0,808 | 0,817 | -65°/20° |
| tres-quartos-b | 0,787 | 0,824 | -45°/25° |
| lado | 0,786 | 0,788 | -70°/20° |
| **média** | **0,814** | **0,826** |  |

- `antes`: .preview/v102/pecas/dino · 2026-11-14 · tag v1.0.2
