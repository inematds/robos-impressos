# Cómo imprimir el robot cuadrado con ruedas

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impresora de referencia: Bambu Lab A1 (cama de 256 × 256 × 256 mm), boquilla de 0,4 mm, capa de 0,2 mm.

Sugerencia de ajuste, todavía no probada con estas piezas:

- Placa PEI texturizada para los dos materiales.
- En Bambu Studio, perfil Generic PLA para el PLA y Generic PETG para el PETG, con las temperaturas del perfil.
- Valores habituales para que los compruebes: PLA con la boquilla a 220 °C y la cama a 55–65 °C; PETG con la boquilla a 250–255 °C y la cama a 70–80 °C. La [guía de filamentos de Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) indica de 240 a 270 °C para la boquilla con PETG.

Página del robot: https://inematds.github.io/robos-impressos/guia/es/cubo-rodas/

## Los archivos ya están en la posición de impresión

- Cada STL de `projetos/cubo-rodas/stl/` está colocado como debe imprimirse: la cara de apoyo en Z = 0. Ábrelo en el laminador e
  imprímelo sin girarlo.
- Cada 3MF de `projetos/cubo-rodas/mesas/` incluye las piezas de un color, ya acomodadas en una cama de 256 mm.
- Todo de una vez: [cubo-rodas-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/cubo-rodas-stl.zip)
  (los STL, los 3MF de las camas, el programa del Arduino y las guías).
- Cómo se verificó (14/11/2026): en cada uno de los 15 STL, el tamaño de la caja de la pieza coincide con el tamaño «en la cama» de la tabla de abajo, el punto más bajo está en Z = 0 y hay una cara plana apoyada en la cama. Ninguna pieza necesita soportes.
- Los 3MF son genéricos: solo contienen geometría y posición, sin perfil ni color. Se volvieron a leer con un script, pero todavía no se abrieron en Bambu Studio. Si alguno no abre, usa los STL.

## 1. Imprime primero el cupón de prueba

**Todavía no se imprimió nada de este proyecto.** El cupón de prueba (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está en la cama 07, junto con los 4 separadores del Raspberry Pi. Para este robot, pruébalo ahí:

- un inserto M3 en cada uno de los 3 orificios (3,9, 4,0 y 4,1 mm);
- un tornillo M3 en el orificio pasante (3,4 mm) y otro en el orificio para enroscar directamente en el plástico (2,7 mm);
- un tornillo M2,5 en el orificio para enroscar directamente en el plástico: así se fija la pantalla al panel del rostro.

El hoyuelo marca la medida que usa el proyecto. Si otro agujero queda mejor en tu impresora, no tienes que rehacer las
piezas: en Bambu Studio, la opción X-Y hole compensation (compensación de agujeros X-Y; pestaña Calidad, grupo Precisión, con el
modo avanzado activado) abre o cierra todos los agujeros de la pieza: un valor positivo los abre y uno negativo los cierra
([fuente: código de Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
La fuente no indica si el valor cuenta por lado o por diámetro: empieza con 0,05 mm e imprime el cupón de prueba de nuevo. El cupón decide.

Quien modifique el código puede cambiar el valor en el bloque `FOLGA` de `comum/cad/parametros.py` y volver a generar las piezas
(`.venv/bin/python comum/cad/gerar.py cubo_rodas`).

Cuatro avisos:

- El cupón es común a los demás robots del proyecto. Su abertura para el servo es para el microservo (SG90/MG90S) y los conectores para pines y el orificio para el motor TT son para los otros robots: este robot no usa ninguno de los tres. Aquí, el Raspberry Pi usa un orificio pasante con tuerca.
- El ajuste del servo MG996R y la rosca del tornillo M5 no están en el cupón. Comprueba el servo en el marco de la cabeza (cama 01, la tercera en el orden de abajo). La rosca del M5 está en el brazo de la horquilla (cama 04, la cuarta). Ambas comprobaciones se hacen antes de las impresiones largas.
- El ajuste del motor tampoco está en el cupón. La brida sale en la cama 04: con el motor en la mano, comprueba los 6 orificios alrededor del eje antes de imprimir la base, que es la impresión más larga. Si los orificios no coinciden, corrige la medida y vuelve a imprimir solo la brida.
- El cupón se imprime en PLA, pero 27 de los 31 insertos van en piezas de PETG. Imprime un segundo cupón en PETG. No está en ninguna cama ni en los totales: carga el archivo `comum-teste-encaixe.stl` por separado, con PETG, y cuenta con unos 15 g y 38 minutos adicionales.

## 2. Orden sugerido de las camas

Primero, las piezas pequeñas que encajan entre sí; al final, las impresiones largas.

<!-- GERADO:mesas -->
| Orden | Archivo de la cama | Material y color | Piezas | Filamento (g) | Tiempo (h) | Por qué va en este orden |
|---|---|---|---|---|---|---|
| 1 | [cubo_rodas-mesa-07-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-07-pla-cinza.3mf) | PLA gris | Cupón de prueba (teste-encaixe), 4 × Espaciador de Raspberry Pi (espacador-pi) | 16 | 0,9 | Empieza aquí. El cupón de prueba muestra si los insertos y los tornillos M3 entran con la holgura adecuada en TU impresora. Menos de 1 hora, con los 4 separadores del Raspberry Pi. |
| 2 | [cubo_rodas-mesa-05-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-05-petg-prata.3mf) | PETG plateado | Tubo del cuello (tubo-pescoco), Engranaje del cuello (engrenagem-pescoco) | 25 | 1,1 | Tubo y engranaje del cuello: piezas pequeñas que ya prueban el ajuste con las varillas de unión. |
| 3 | [cubo_rodas-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-01-petg-amarelo.3mf) | PETG amarillo | Marco de la cabeza (quadro-cabeca), Engranaje del servo (engrenagem-servo) | 108 | 4,1 | Marco de la cabeza y engranaje del servo: comprueba si el servo entra en la ranura y si los dos engranajes giran juntos sin trabarse. |
| 4 | [cubo_rodas-mesa-04-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-04-petg-grafite.3mf) | PETG grafito | Deck (bandeja de las placas) (deck), Tapa de la batería (tampa-bateria), 2 × Brida del motor (flange-motor), Tapa de la bola (capa-esfera), Horquilla (garfo) | 187 | 7,3 | Deck, tapa de la batería, las 2 bridas, tapa de la bola y horquilla. Revisa ahora: los 6 agujeros de la brida contra el motor, el tornillo M5 en el brazo de la horquilla y las placas en los resaltes del deck. |
| 5 | [cubo_rodas-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-03-petg-grafite.3mf) | PETG grafito | Base con ruedas (base-rodas) | 266 | 9,8 | Base con ruedas: la impresión más larga. Antes de imprimirla, comprueba con la brida de la mesa anterior si el motor pasa por un agujero de 40,6 mm. |
| 6 | [cubo_rodas-mesa-02-petg-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-02-petg-branco.3mf) | PETG blanco | Torso (tronco) | 236 | 8,7 | Torso: imprímelo boca abajo, con la parte superior sobre la cama. |
| 7 | [cubo_rodas-mesa-08-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-08-pla-preto.3mf) | PLA negro | Panel de la cara (cabeca-face) | 57 | 2,2 | Panel de la cara: la cara visible va en la cama, así que limpia bien la cama antes. |
| 8 | [cubo_rodas-mesa-06-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-06-pla-branco.3mf) | PLA blanco | Carcasa de la cabeza (cabeca-corpo) | 248 | 9,3 | Copa de la cabeza: la impresión más larga en PLA. Déjala para el final, cuando la impresora ya esté ajustada. |
| **Total** |  |  |  | **1143** | **43,4** |  |
<!-- /GERADO -->

## 3. Pieza por pieza

"Paredes" es el número de perímetros. Ninguna pieza necesita soportes en la posición en que viene el archivo. El nombre entre
paréntesis es el nombre del archivo.

<!-- GERADO:pecas -->
| Pieza | Archivo | Cant. | Material y color | Tamaño en la cama (mm) | Cómo va en la cama | Soporte | Paredes | Relleno | Filamento (g) | Tiempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base con ruedas (base-rodas) | [cubo_rodas-base-rodas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-base-rodas.stl) | 1 | PETG grafito | 130 × 182 × 72 | piso sobre la cama | no | 5 | 25 % | 266 | 9,8 |
| Tapa de la batería (tampa-bateria) | [cubo_rodas-tampa-bateria.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tampa-bateria.stl) | 1 | PETG grafito | 108 × 84 × 7 | cara inferior sobre la cama, escuadras hacia arriba | no | 4 | 25 % | 34 | 1,3 |
| Tapa de la bola (capa-esfera) | [cubo_rodas-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-capa-esfera.stl) | 1 | PETG grafito | 56,9 × 47,2 × 12 | boca abajo: la cara que toca el piso sobre la cama; la abertura cierra a 45° | no | 4 | 40 % | 9 | 0,4 |
| Brida del motor (flange-motor) | [cubo_rodas-flange-motor.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-flange-motor.stl) | 2 | PETG grafito | 62 × 62 × 4 | acostada, la cara que toca la pared sobre la cama | no | 5 | 60 % | 28 | 1,2 |
| Deck (bandeja de las placas) (deck) | [cubo_rodas-deck.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-deck.stl) | 1 | PETG grafito | 127 × 179 × 29,8 | cara inferior sobre la cama | no | 4 | 25 % | 97 | 3,6 |
| Torso (tronco) | [cubo_rodas-tronco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tronco.stl) | 1 | PETG blanco | 130 × 182 × 57,5 | boca abajo: la parte superior sobre la cama | no | 4 | 15 % | 236 | 8,7 |
| Tubo del cuello (tubo-pescoco) | [cubo_rodas-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tubo-pescoco.stl) | 1 | PETG plateado | 40 × 40 × 36,6 | boca abajo: la parte superior (lado de la horquilla) sobre la cama, la brida cónica se abre a 45° | no | 5 | 40 % | 17 | 0,7 |
| Engranaje del cuello (engrenagem-pescoco) | [cubo_rodas-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-pescoco.stl) | 1 | PETG plateado | 35,8 × 36 × 8 | acostada | no | 5 | 60 % | 8 | 0,4 |
| Engranaje del servo (engrenagem-servo) | [cubo_rodas-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-servo.stl) | 1 | PETG amarillo | 68,9 × 68,9 × 8 | boca abajo: la cara superior sobre la cama, el hueco del horn hacia arriba | no | 5 | 60 % | 23 | 0,9 |
| Horquilla (garfo) | [cubo_rodas-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-garfo.stl) | 1 | PETG grafito | 44 × 41,9 × 24 | acostada, con la parte trasera sobre la cama: las capas van del bloque hacia los brazos | no | 5 | 40 % | 19 | 0,8 |
| Marco de la cabeza (quadro-cabeca) | [cubo_rodas-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-quadro-cabeca.stl) | 1 | PETG amarillo | 145,2 × 93,5 × 62,7 | frente del travesaño sobre la cama, laterales hacia arriba | no | 4 | 30 % | 85 | 3,2 |
| Carcasa de la cabeza (cabeca-corpo) | [cubo_rodas-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-corpo.stl) | 1 | PLA blanco | 152 × 128 × 110 | espalda sobre la cama, abertura (frente) hacia arriba, como un vaso | no | 3 | 15 % | 248 | 9,3 |
| Panel de la cara (cabeca-face) | [cubo_rodas-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-face.stl) | 1 | PLA negro | 145,9 × 121,9 × 43,2 | cara frontal (la que queda visible) sobre la cama, pilares hacia arriba | no | 3 | 20 % | 57 | 2,2 |
| Espaciador de Raspberry Pi (espacador-pi) | [cubo_rodas-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-espacador-pi.stl) | 4 | PLA gris | 6 × 6 × 4 | de pie | no | 3 | 15 % | 1 | 0,3 |
| Cupón de prueba (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gris | 70 × 34 × 8 | acostada | no | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **19** |  |  |  |  |  |  | **1143** | **43,4** |
<!-- /GERADO -->

El filamento y el tiempo son estimaciones por volumen, sin laminador. El laminador dará el valor exacto.

## 4. Filamento por color

<!-- GERADO:filamento -->
| Material y color | Filamento (g) | Tiempo (h) |
|---|---|---|
| PETG amarillo | 108 | 4,1 |
| PETG blanco | 236 | 8,7 |
| PETG grafito | 453 | 17,1 |
| PETG plateado | 25 | 1,1 |
| PLA blanco | 248 | 9,3 |
| PLA gris | 16 | 0,9 |
| PLA negro | 57 | 2,2 |
| **Total** | **1143** | **43,4** |
<!-- /GERADO -->

## Dónde se refuerza cada pieza

<!-- GERADO:reforcos -->
| Pieza | Refuerzo | Qué es |
|---|---|---|
| Base con ruedas (base-rodas) | paredes de los motores con refuerzo de 4 mm y orificio en forma de gota; 4 postes Ø12 en las esquinas; resaltes nervados de la tapa y la cubierta; asiento cónico de la bola a 45°; chaflán de 45° abajo | cuba de la base móvil: los motores entran por el lateral (brida detrás de la rueda), la batería va en una tapa por debajo, el cargador USB-C y el interruptor van atrás, ventana del sensor de caída y muescas para los ToF |
| Tapa de la batería (tampa-bateria) | 4 escuadras + abrazadera sujetan el soporte 3x18650 | tapa de la batería: 4 M3x8 por debajo; la batería baja junto con ella |
| Tapa de la bola (capa-esfera) | 4 orejas; abertura cónica a 45° | sujeta la pelota de 40 mm en el pozo; 4 M3x8 por debajo; a 8 mm del suelo |
| Brida del motor (flange-motor) | disco casi macizo (5 perímetros, 60 %): soporta el peso y el torque del motor | sujeta el motor JGB37 (6 M3x6) y cierra el orificio lateral de la base (4 M3x10); queda oculta detrás de la rueda |
| Deck (bandeja de las placas) (deck) | postes del servo de pan con cartelas; resaltes nervados del Uno y del L298N; soportes con abrazadera | bandeja electrónica: servo de pan, Arduino Uno, L298N, step-down del Pi y UBEC; 1,5 mm hacia adentro (ranura de sombra entre la base y el torso) |
| Torso (tronco) | 4 columnas Ø12 integradas en las paredes (inserto en la punta); chaflán de 45° de 6 mm en la parte superior; los rieles del altavoz nacen de la parte superior | carcasa superior: 4 M3x12 entran POR DEBAJO de la base, atraviesan el deck y se enroscan aquí; rejilla del altavoz atrás |
| Tubo del cuello (tubo-pescoco) | 3 tirantes M3 de acero atraviesan todo el tubo: las capas trabajan solo a compresión; brida cónica a 45° | cuello hueco (cables por dentro); 3 M3x50 entran por debajo, por el engranaje, y se enroscan en los insertos de la horquilla |
| Engranaje del cuello (engrenagem-pescoco) | dientes módulo 1.5 con 5 perímetros (diente casi macizo); sujeta con los 3 tirantes | 22 dientes; queda debajo de la tapa y, con la brida del tubo encima, evita que el cuello se tambalee |
| Engranaje del servo (engrenagem-servo) | dientes módulo 1.5 con 5 perímetros; 4 tornillos en el horn redondo | 44 dientes, fijada al horn redondo del servo de pan (el cuello gira 2x el servo) |
| Horquilla (garfo) | capas a lo largo de los brazos (flexión); bloque macizo con 3 insertos de los tirantes; agujeros en forma de gota | horquilla interna del tilt: queda dentro de la cabeza, en la parte superior del tubo; horn del servo en un brazo, pin M5 (rosca en el plástico) en el otro; orificios de acceso para la llave en el brazo izquierdo |
| Marco de la cabeza (quadro-cabeca) | laterales enteros hasta el fondo con columnas Ø10 en los 4 insertos y cartabones a 45° en el travesaño; servo de tilt en una ranura en U (sin puente), 4 tornillos | esqueleto de la cabeza: Raspberry Pi (4 M2,5), servo de tilt, soporte del pasador; recibe el panel (4 M3 por detrás) y la copa (4 M3 por la pared trasera) |
| Carcasa de la cabeza (cabeca-corpo) | bordes largos con radio de 20 mm (verticales en la impresión) y chaflán de 45° en el borde trasero; ranura del cuello en forma de gota; sin puente ni techo | carcasa de la cabeza (5 lados); entra por detrás, 4 M3 en la pared trasera; ranura del cuello y orificios del micrófono por debajo |
| Panel de la cara (cabeca-face) | 4 pilares Ø10 con 2 nervaduras a 45° cada uno (insertos roscados M3 en la punta); postes de la cámara | panel oscuro del rostro: ventana de la pantalla, orificio de 8 mm de la cámara encima; ningún tornillo al frente |
| Espaciador de Raspberry Pi (espacador-pi) | — | 4 separadores de 4 mm del Raspberry Pi |
| Cupón de prueba (teste-encaixe) | — | cupón de holguras: ventana del servo, 3 orificios para inserto roscado (3,9/4,0/4,1), eje del motor TT, M3 pasante/M3 piloto/M2,5/M2, 3 alojamientos del pin (0,20/0,25/0,30); hoyuelo = medida del diseño |
<!-- /GERADO -->

Después de imprimir: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md) y [LIGACAO.es.md](LIGACAO.es.md).
