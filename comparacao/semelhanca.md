# Semelhança com as imagens de referência (IoU de silhueta)

Gerado por `comum/cad/comparar.py` (não edite à mão). IoU = área comum ÷ área total das duas silhuetas, de 0 a 1: quanto maior, mais parecido o contorno. Mede só o CONTORNO em cada vista, não cor nem detalhe.

Protocolo v1: projeção ortográfica, silhuetas com 400 px de altura, base na mesma linha e centro horizontal coincidente; melhor azimute em nominal ± 25° (passo 5°) e elevação em nominal ± 10° (passo 5°). Entram as peças impressas + rodas/esfera, pose neutra. "Ajustado" = número secundário, deixando escala (±12%) e posição variarem.

## capivara

| vista | antes: IoU | antes: ajustado | antes: az/el | malha-capivara-hy2mv-flb-s1: IoU | malha-capivara-hy2mv-flb-s1: ajustado | malha-capivara-hy2mv-flb-s1: az/el | malha-capivara-hy2mv-flb-s2: IoU | malha-capivara-hy2mv-flb-s2: ajustado | malha-capivara-hy2mv-flb-s2: az/el | depois: IoU | depois: ajustado | depois: az/el |
|---|---:|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|
| frente | 0,783 | 0,804 | 10°/5° | 0,936 | 0,936 | -5°/5° | 0,943 | 0,943 | 0°/5° | 0,944 | 0,944 | 0°/5° |
| tres-quartos | 0,784 | 0,786 | -70°/10° | 0,901 | 0,901 | -45°/5° | 0,911 | 0,911 | -45°/5° | 0,908 | 0,908 | -45°/5° |
| lado | 0,736 | 0,737 | -70°/10° | 0,917 | 0,917 | -70°/10° | 0,925 | 0,925 | -70°/10° | 0,906 | 0,906 | -70°/10° |
| costas | 0,803 | 0,818 | 170°/5° | 0,923 | 0,924 | 185°/10° | 0,927 | 0,927 | 180°/10° | 0,925 | 0,925 | 190°/10° |
| **média** | **0,777** | **0,786** |  | **0,919** | **0,919** |  | **0,926** | **0,926** |  | **0,920** | **0,920** |  |

- `antes`: .preview/v102/pecas/capivara · 2026-11-14 · tag v1.0.2
- `malha-capivara-hy2mv-flb-s1`: referencia/malhas/capivara-hy2mv-flb-s1.glb · 2026-11-14
- `malha-capivara-hy2mv-flb-s2`: referencia/malhas/capivara-hy2mv-flb-s2.glb · 2026-11-14
- `depois`: pecas/capivara · 2026-11-14

## cubo

| vista | antes: IoU | antes: ajustado | antes: az/el | depois: IoU | depois: ajustado | depois: az/el |
|---|---:|---:|---|---:|---:|---|
| tres-quartos | 0,755 | 0,773 | 10°/32° | 0,797 | 0,805 | 30°/12° |
| **média** | **0,755** | **0,773** |  | **0,797** | **0,805** |  |

- `antes`: .preview/v102/pecas/cubo · 2026-11-14 · tag v1.0.2
- `depois`: pecas/cubo · 2026-11-14

## cubo_rodas

| vista | depois: IoU | depois: ajustado | depois: az/el |
|---|---:|---:|---|
| tres-quartos | 0,669 | 0,709 | 45°/12° |
| **média** | **0,669** | **0,709** |  |

- `depois`: pecas/cubo_rodas · 2026-11-14

## dino

| vista | antes: IoU | antes: ajustado | antes: az/el | malha-dino-hy2mv-fl-s1: IoU | malha-dino-hy2mv-fl-s1: ajustado | malha-dino-hy2mv-fl-s1: az/el | malha-dino-hy2mv-fl-s2: IoU | malha-dino-hy2mv-fl-s2: ajustado | malha-dino-hy2mv-fl-s2: az/el | depois: IoU | depois: ajustado | depois: az/el |
|---|---:|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|
| frente | 0,875 | 0,875 | 0°/15° | 0,930 | 0,935 | 0°/20° | 0,942 | 0,942 | 0°/15° | 0,913 | 0,913 | 5°/10° |
| tres-quartos-a | 0,808 | 0,817 | -65°/20° | 0,866 | 0,870 | -55°/15° | 0,888 | 0,888 | -55°/15° | 0,874 | 0,874 | -55°/15° |
| tres-quartos-b | 0,787 | 0,824 | -45°/25° | 0,897 | 0,897 | -45°/20° | 0,889 | 0,889 | -50°/20° | 0,862 | 0,862 | -50°/20° |
| lado | 0,786 | 0,788 | -70°/20° | 0,869 | 0,869 | -55°/5° | 0,870 | 0,884 | -75°/10° | 0,837 | 0,837 | -65°/10° |
| **média** | **0,814** | **0,826** |  | **0,891** | **0,893** |  | **0,897** | **0,901** |  | **0,871** | **0,871** |  |

- `antes`: .preview/v102/pecas/dino · 2026-11-14 · tag v1.0.2
- `malha-dino-hy2mv-fl-s1`: referencia/malhas/dino-hy2mv-fl-s1.glb · 2026-11-14
- `malha-dino-hy2mv-fl-s2`: referencia/malhas/dino-hy2mv-fl-s2.glb · 2026-11-14
- `depois`: pecas/dino · 2026-11-14
