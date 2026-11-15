# Cómo imprimir el robot cuadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impresora de referencia: Bambu Lab A1 (cama de 256 × 256 × 256 mm), boquilla de 0,4 mm, capa de 0,2 mm.

Sugerencia de ajuste, todavía no probada con estas piezas:

- Placa PEI texturizada para los dos materiales.
- En Bambu Studio, perfil Generic PLA para el PLA y Generic PETG para el PETG, con las temperaturas del perfil.
- Valores habituales para que los compruebes: PLA con la boquilla a 220 °C y la cama a 55–65 °C; PETG con la boquilla a 250–255 °C y la cama a 70–80 °C. La [guía de filamentos de Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) indica de 240 a 270 °C para la boquilla con PETG.

Página con las mismas tablas: https://inematds.github.io/robos-impressos/guia/es/cubo/#imprimir

## Los archivos ya están en la posición de impresión

- Cada STL de `pecas/cubo/stl/` está acostado como debe imprimirse: la cara de apoyo en Z = 0. Ábrelo en el laminador e
  imprímelo sin girarlo.
- Cada 3MF de `pecas/cubo/mesas/` incluye las piezas de un color, ya ordenadas en una cama de 256 mm.
- Todo de una vez: [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip)
  (los STL, los 3MF de las camas, el programa de Arduino y las guías).
- Cómo se verificó (14/11/2026): en cada STL, el tamaño de la caja de la pieza coincide con el tamaño "en la cama" de la tabla siguiente, el
  punto más bajo está en Z = 0 y el área plana apoyada en la cama es la misma que midió el verificador del proyecto.
  Ninguna pieza necesita soportes.
- Los 3MF son genéricos: solo incluyen geometría y posición, sin perfil ni color. Se volvieron a leer con un script, pero aún no se han
  abierto en Bambu Studio. Si alguno no se abre, usa los STL.

## 1. Imprime primero el cupón de prueba

**Todavía no se ha impreso nada de este proyecto.** El cupón de prueba (`pecas/comum/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está en la cama 06, con los 4 espaciadores del Raspberry Pi. En el robot cuadrado, prueba en él:

- un inserto M3 en cada uno de los 3 orificios (3,9, 4,0 y 4,1 mm);
- un tornillo M3 en el orificio pasante (3,4 mm) y otro en el orificio para roscar directamente en el plástico (2,7 mm).

El hoyuelo marca la medida que usa el proyecto. Si otro agujero queda mejor en tu impresora, no tienes que rehacer las
piezas: en Bambu Studio, la opción X-Y hole compensation (compensación de agujeros X-Y; pestaña Calidad, grupo Precisión, con el
modo avanzado activado) abre o cierra todos los agujeros de la pieza: un valor positivo los abre y uno negativo los cierra
([fuente: código de Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
La fuente no indica si el valor cuenta por lado o por diámetro: empieza con 0,05 mm e imprime el cupón de prueba de nuevo. El cupón decide.

Si trabajas con el código, puedes cambiar el valor en el bloque `FOLGA` de `cad/parametros.py` y volver a generar las piezas
(`.venv/bin/python cad/gerar.py cubo`).

Tres avisos:

- El cupón es común a los otros robots del proyecto. Su abertura para el servo es para el micro servo (SG90/MG90S), y los alojamientos para pines y el agujero del motor TT son para los otros robots: el robot cuadrado no usa ninguno de los tres. Los agujeros M2,5 y M2 del cupón son para roscar en el plástico; en el robot cuadrado, Raspberry Pi usa un agujero pasante con tuerca.
- El encaje del servo MG996R y la rosca del tornillo M5 no están en el cupón. Comprueba el servo en el marco de la cabeza (mesa 01, la tercera en el orden de abajo). La rosca M5 está en el brazo de la horquilla (mesa 03, la cuarta). Ambas comprobaciones se hacen antes de las impresiones largas.
- El cupón se imprime en PLA, pero 12 de los 16 insertos roscados van en piezas de PETG. Imprime un segundo cupón en PETG.

## 2. Orden sugerido de las camas

Primero, las piezas pequeñas que encajan entre sí; al final, las dos impresiones largas.

<!-- GERADO:mesas -->
| Orden | Archivo de la cama | Material y color | Piezas | Filamento (g) | Tiempo (h) | Por qué va en este orden |
|---|---|---|---|---|---|---|
| 1 | [cubo-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-06-pla-cinza.3mf) | PLA gris | Cupón de prueba (teste-encaixe), 4 × Espaciador de Raspberry Pi (espacador-pi) | 15 | 0,9 | Empieza por aquí. El cupón de prueba muestra si los insertos y los tornillos M3 entran con la holgura correcta en TU impresora. Menos de 1 hora. |
| 2 | [cubo-mesa-04-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-04-petg-prata.3mf) | PETG plateado | Tubo del cuello (tubo-pescoco), Engranaje del cuello (engrenagem-pescoco) | 24 | 1,1 | Tubo y engranaje del cuello: piezas pequeñas que ya prueban el ajuste con las varillas de unión. |
| 3 | [cubo-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-01-petg-amarelo.3mf) | PETG amarillo | Marco de la cabeza (quadro-cabeca), Engranaje del servo (engrenagem-servo) | 88 | 3,3 | Marco de la cabeza y engranaje del servo: comprueba si el servo entra en la ranura y si los dos engranajes giran juntos sin trabarse. |
| 4 | [cubo-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-03-petg-grafite.3mf) | PETG grafito | Tapa de la base (tampa-base), Puerta trasera (porta-traseira), Horquilla (garfo) | 129 | 5,0 | Tapa, puerta y horquilla. En la horquilla, comprueba que el tornillo M5 enrosque en el orificio del brazo de la horquilla; con el marco de la mesa anterior, verifica que la cabeza se incline sin trabarse. |
| 5 | [cubo-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-02-petg-grafite.3mf) | PETG grafito | Base (base) | 222 | 8,2 | Base: la impresión más larga en PETG. |
| 6 | [cubo-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-07-pla-preto.3mf) | PLA negro | Panel de la cara (cabeca-face) | 53 | 2,0 | Panel de la cara: la cara visible va en la cama, así que limpia bien la cama antes. |
| 7 | [cubo-mesa-05-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-05-pla-branco.3mf) | PLA blanco | Carcasa de la cabeza (cabeca-corpo) | 204 | 7,7 | Copa de la cabeza: la impresión más larga en PLA. Déjala para el final, cuando la impresora ya esté ajustada. |
| **Total** |  |  |  | **735** | **28,2** |  |
<!-- /GERADO -->

## 3. Pieza por pieza

"Paredes" es el número de perímetros. Ninguna pieza necesita soportes en la posición en que viene el archivo. El nombre entre
paréntesis es el nombre del archivo.

<!-- GERADO:pecas -->
| Pieza | Archivo | Cant. | Material y color | Tamaño en la cama (mm) | Cómo va en la cama | Soporte | Paredes | Relleno | Filamento (g) | Tiempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base (base) | [cubo-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-base.stl) | 1 | PETG grafito | 158 × 146 × 56,5 | piso sobre la cama | no | 4 | 20 % | 222 | 8,2 |
| Tapa de la base (tampa-base) | [cubo-tampa-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tampa-base.stl) | 1 | PETG grafito | 158 × 146 × 18 | boca abajo: la cara superior sobre la cama | no | 4 | 25 % | 101 | 3,8 |
| Puerta trasera (porta-traseira) | [cubo-porta-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-porta-traseira.stl) | 1 | PETG grafito | 45,4 × 52,6 × 5 | cara exterior sobre la cama | no | 3 | 20 % | 9 | 0,4 |
| Tubo del cuello (tubo-pescoco) | [cubo-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tubo-pescoco.stl) | 1 | PETG plateado | 40 × 40 × 32,6 | boca abajo: la parte superior (lado de la horquilla) sobre la cama, la brida cónica se abre a 45° | no | 5 | 40 % | 16 | 0,7 |
| Engranaje del cuello (engrenagem-pescoco) | [cubo-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-pescoco.stl) | 1 | PETG plateado | 36 × 36 × 8 | acostada | no | 5 | 60 % | 8 | 0,4 |
| Engranaje del servo (engrenagem-servo) | [cubo-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-servo.stl) | 1 | PETG amarillo | 69 × 69 × 8 | boca abajo: la cara superior sobre la cama, el hueco del horn hacia arriba | no | 5 | 60 % | 23 | 0,9 |
| Horquilla (garfo) | [cubo-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-garfo.stl) | 1 | PETG grafito | 44 × 41,9 × 24 | acostada, con la parte trasera sobre la cama: las capas van del bloque hacia los brazos | no | 5 | 40 % | 19 | 0,8 |
| Marco de la cabeza (quadro-cabeca) | [cubo-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-quadro-cabeca.stl) | 1 | PETG amarillo | 129,2 × 74,6 × 63,7 | frente del travesaño sobre la cama, laterales hacia arriba | no | 4 | 30 % | 65 | 2,4 |
| Carcasa de la cabeza (cabeca-corpo) | [cubo-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-corpo.stl) | 1 | PLA blanco | 136 × 118 × 102 | espalda sobre la cama, abertura (frente) hacia arriba, como un vaso | no | 3 | 15 % | 204 | 7,7 |
| Panel de la cara (cabeca-face) | [cubo-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-face.stl) | 1 | PLA negro | 129,9 × 111,9 × 34,2 | cara frontal (la que queda visible) sobre la cama, pilares hacia arriba | no | 3 | 20 % | 53 | 2,0 |
| Espaciador de Raspberry Pi (espacador-pi) | [cubo-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-espacador-pi.stl) | 4 | PLA gris | 6 × 6 × 5 | de pie | no | 3 | 15 % | <1 | 0,3 |
| Cupón de prueba (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/comum/stl/comum-teste-encaixe.stl) | 1 | PLA gris | 70 × 34 × 8 | acostada | no | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **15** |  |  |  |  |  |  | **735** | **28,2** |
<!-- /GERADO -->

El filamento y el tiempo son estimaciones por volumen, sin laminador. El laminador dará el valor exacto.

## 4. Filamento por color

<!-- GERADO:filamento -->
| Material y color | Filamento (g) | Tiempo (h) |
|---|---|---|
| PETG amarillo | 88 | 3,3 |
| PETG grafito | 351 | 13,2 |
| PETG plateado | 24 | 1,1 |
| PLA blanco | 204 | 7,7 |
| PLA gris | 15 | 0,9 |
| PLA negro | 53 | 2,0 |
| **Total** | **735** | **28,2** |
<!-- /GERADO -->

## Dónde se refuerza cada pieza

<!-- GERADO:reforcos -->
| Pieza | Refuerzo | Qué es |
|---|---|---|
| Base (base) | chaflán de 45° en el borde inferior; postes de la tapa Ø12 integrados en las esquinas; postes del servo con cartabones; resaltes nervados del Uno; ranuras verticales en la rejilla | cuba: piso, paredes, postes del servo de pan, del Uno y de la tapa, soportes de los módulos de energía (abrazadera), rieles del altavoz; interruptor, USB-C y rejilla en la parte trasera |
| Tapa de la base (tampa-base) | 4 resaltes para insertos con 3 nervaduras a 45°; chaflán de 45° en el borde que toca la cama | sujeta con 4 M3x10 que entran POR DEBAJO de la base; la brida del cuello gira sobre ella; oreja para el tornillo de la puerta |
| Puerta trasera (porta-traseira) | — | puerta de la batería (atrás); 1 M3 en la oreja de la tapa, pata contra 2 topes del piso |
| Tubo del cuello (tubo-pescoco) | 3 tirantes M3 de acero atraviesan todo el tubo: las capas trabajan solo a compresión; brida cónica a 45° | cuello hueco (cables por dentro); 3 M3x45 entran por debajo, a través del engranaje, y se enroscan en los insertos de la horquilla |
| Engranaje del cuello (engrenagem-pescoco) | dientes módulo 1.5 con 5 perímetros (diente casi macizo); sujeta con los 3 tirantes | 22 dientes; queda debajo de la tapa y, con la brida del tubo encima, evita que el cuello se tambalee |
| Engranaje del servo (engrenagem-servo) | dientes módulo 1.5 con 5 perímetros; 4 tornillos en el horn redondo | 44 dientes, fijada al horn redondo del servo de pan (el cuello gira 2x el servo) |
| Horquilla (garfo) | capas a lo largo de los brazos (flexión); bloque macizo con 3 insertos de los tirantes; agujeros en forma de gota | horquilla interna del tilt: queda dentro de la cabeza, en la parte superior del tubo; horn del servo en un brazo, pin M5 (rosca en el plástico) en el otro; orificios de acceso para la llave en el brazo izquierdo |
| Marco de la cabeza (quadro-cabeca) | laterales enteros hasta el fondo con columnas Ø10 en los 4 insertos y cartabones a 45° en el travesaño; servo de tilt en una ranura en U (sin puente), 4 tornillos | esqueleto de la cabeza: Raspberry Pi (4 M2,5), servo de tilt, soporte del pasador; recibe el panel (4 M3 por detrás) y la copa (4 M3 por la pared trasera) |
| Carcasa de la cabeza (cabeca-corpo) | bordes largos con radio de 20 mm (verticales en la impresión) y chaflán de 45° en el borde trasero; ranura del cuello en forma de gota; sin puente ni techo | carcasa de la cabeza (5 lados); entra por detrás, 4 M3 en la pared trasera; ranura del cuello y orificios del micrófono por debajo |
| Panel de la cara (cabeca-face) | 4 pilares Ø10 con 2 nervaduras a 45° cada uno (insertos roscados M3 en la punta); postes de la cámara | panel oscuro del rostro: ventana de la pantalla, orificio de 8 mm de la cámara encima; ningún tornillo al frente |
| Espaciador de Raspberry Pi (espacador-pi) | — | 4 separadores de 5 mm para Raspberry Pi |
| Cupón de prueba (teste-encaixe) | — | cupón de holguras: ventana del servo, 3 orificios para inserto roscado (3,9/4,0/4,1), eje del motor TT, M3 pasante/M3 piloto/M2,5/M2, 3 alojamientos del pin (0,20/0,25/0,30); hoyuelo = medida del diseño |
<!-- /GERADO -->

Después de imprimir: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md) y [LIGACAO.es.md](LIGACAO.es.md).
