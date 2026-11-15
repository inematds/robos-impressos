# Cómo imprimir el dinosaurio

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impresora de referencia: Bambu Lab A1 (cama de 256 × 256 × 256 mm), boquilla de 0,4 mm, capa de 0,2 mm.

Sugerencia de ajuste, todavía no probada con estas piezas:

- Placa PEI texturizada para los dos materiales.
- En Bambu Studio, perfil Generic PLA para el PLA y Generic PETG para el PETG, con las temperaturas del perfil.
- Valores habituales para que los compruebes: PLA con la boquilla a 220 °C y la cama a 55–65 °C; PETG con la boquilla a 250–255 °C y la cama a 70–80 °C. La [guía de filamentos de Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) indica de 240 a 270 °C para la boquilla con PETG.

Página con las mismas tablas: https://inematds.github.io/robos-impressos/guia/es/dino/#imprimir

## Los archivos ya están en la posición de impresión

- Cada STL de `projetos/dino/stl/` está en la posición en la que debe imprimirse: la cara de apoyo en Z = 0. Ábrelo en el laminador e
  imprímelo sin girarlo.
- Cada 3MF de `projetos/dino/mesas/` incluye las piezas de un color, ya organizadas en una cama de 256 mm.
- Todo de una vez: [dino-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/dino-stl.zip)
  (los STL, los 3MF de las camas, el programa de Arduino y las guías).
- Cómo se comprobó (14/11/2026): en cada STL, la caja de la pieza coincide con el tamaño «en la cama» de la tabla de abajo y el
  punto más bajo está en Z = 0.
- Los 3MF son genéricos: solo tienen geometría y posición, sin perfil ni color. Se volvieron a leer con un script, pero aún no se han
  abierto en Bambu Studio. Si alguno no abre, usa los STL.

## Seis piezas necesitan soportes

Las demás se imprimen sin soportes. En estas seis, activa los soportes en el laminador (en árbol, salvo que la tabla indique otra cosa).
En ninguna parte el soporte toca la cara ni un encaje.

| Pieza | Dónde van los soportes | ¿Se ven? |
|---|---|---|
| Cráneo | Por dentro: techo del cráneo, fondo de las cuencas de los ojos y nervadura de la cresta. Por debajo: borde del paladar. | No. Nada en la cara. |
| Cuerpo | Por dentro: techo de los 2 muslos, sobre las ruedas, y escalones de los asientos planos (2,3 % del área). | No. |
| Carcasa trasera | Por dentro: techo superior de la cadera y nervadura de la ranura de la cresta (2,4 % del área). | No. |
| Mandíbula | Debajo del recorte redondo trasero, orientado hacia el cuello. | No. |
| Horquilla del cuello | 1,8 mm debajo de la base, alrededor del anillo del horn. Soporte normal. | No: queda dentro del collar. |
| Cuna del tilt | Un poco, debajo del puente entre las 2 paredes del servo. | No: queda dentro del collar. |

El verificador del proyecto mide el área sin apoyo de cada pieza y rechaza la que se indicó sin soportes y los necesita.
Todavía nadie ha retirado los soportes de una de estas piezas impresas: empieza con una pieza pequeña, como la mandíbula.

## 1. Imprime primero el cupón de prueba

**Todavía no se ha impreso nada de este proyecto.** El cupón de prueba (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está en la cama 05. Pruébalo para comprobar:

- un inserto M3 en cada uno de los 3 orificios (3,9, 4,0 y 4,1 mm);
- un tornillo M3 en el orificio pasante (3,4 mm) y otro en el orificio para roscar directamente en el plástico (2,7 mm);
- el microservo en la ventana y el eje del motor de las ruedas en su orificio;
- los orificios M2,5 (Raspberry Pi) y M2 (tornillos de los microservos), para roscar directamente en el plástico.

El hoyuelo marca la medida que usa el proyecto. Si otro agujero queda mejor en tu impresora, no tienes que rehacer las
piezas: en Bambu Studio, la opción X-Y hole compensation (compensación de agujeros X-Y; pestaña Calidad, grupo Precisión, con el
modo avanzado activado) abre o cierra todos los agujeros de la pieza: un valor positivo los abre y uno negativo los cierra
([fuente: código de Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
La fuente no indica si el valor cuenta por lado o por diámetro: empieza con 0,05 mm e imprime el cupón de prueba de nuevo. El cupón decide.

Quien modifique el código puede cambiar el valor del bloque `FOLGA` de `comum/cad/parametros.py` y volver a generar las piezas
(`.venv/bin/python comum/cad/gerar.py dino`).

Tres avisos:

- El cupón es común a los demás robots del proyecto. Los 3 conectores de pines no se usan en este robot.
- El encaje del servo MG996R no está en el cupón. Comprueba el servo en la cuna del tilt (cama 02, la tercera en el orden de abajo),
  antes de las impresiones largas.
- El cupón se imprime en PLA, pero 7 de los 13 insertos van en piezas de PETG (chasis, cuna y horquilla). Imprime un segundo cupón en PETG. No está incluido en ninguna cama ni en los totales: carga el archivo `comum-teste-encaixe.stl` por separado, con PETG, y calcula unos 15 g y 38 minutos más.

## 2. Orden sugerido de las camas

Primero las piezas pequeñas y el esqueleto; al final, las impresiones largas: el cráneo, la carcasa trasera y el cuerpo.

<!-- GERADO:mesas -->
| Orden | Archivo de la cama | Material y color | Piezas | Filamento (g) | Tiempo (h) | Por qué va en este orden |
|---|---|---|---|---|---|---|
| 1 | [dino-mesa-05-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-05-pla-cinza.3mf) | PLA gris | Cupón de prueba (teste-encaixe) | 15 | 0,6 | Empieza por aquí. El cupón de prueba muestra si los insertos roscados, los tornillos M3, el microservo y el eje del motor encajan con la holgura adecuada en TU impresora. Menos de 1 hora. |
| 2 | [dino-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-01-petg-amarelo.3mf) | PETG amarillo | Bandeja para Raspberry Pi (bandeja-pi), Bandeja para Arduino (bandeja-uno) | 28 | 1,2 | Las 2 bandejas: piezas pequeñas que ya ponen a prueba los agujeros de la Raspberry Pi y del Arduino. |
| 3 | [dino-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-02-petg-grafite.3mf) | PETG grafito | Chasis (chassi), Placa de la cabeza (mesa-cabeca), Horquilla del cuello (garfo-pescoco), Cubierta de la esfera (capa-esfera), Cuna del tilt (berco-tilt), 2 × Cubo del brazo (cubo-braco) | 243 | 9,4 | Todo el esqueleto en PETG: chasis, placa de la cabeza, horquilla, cuna, cubierta de la esfera y los 2 cubos de los brazos. La horquilla y la cuna requieren soportes. Comprueba si el servo MG996R cabe en la cuna antes de las impresiones largas. |
| 4 | [dino-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-04-pla-branco.3mf) | PLA blanco | Ojo derecho (olho), Ojo izquierdo (olho-esq) | 28 | 1,2 | Los 2 ojos. |
| 5 | [dino-mesa-03-pla-azul.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-03-pla-azul.3mf) | PLA azul | Cresta de la cabeza (crista-cabeca), Cresta de la espalda (crista-costas), Iris derecha (iris), Iris izquierda (iris-esq) | 42 | 1,9 | Crestas e iris, en azul. |
| 6 | [dino-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-07-pla-preto.3mf) | PLA negro | Pupila derecha (pupila), Pupila izquierda (pupila-esq) | 4 | 0,4 | Las 2 pupilas. |
| 7 | [dino-mesa-12-pla-verde-escuro.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-12-pla-verde-escuro.3mf) | PLA verde oscuro | Mancha del flanco derecho (mancha-dir), Mancha del flanco izquierdo (mancha-esq) | 4 | 0,2 | Las 2 manchas de los flancos. |
| 8 | [dino-mesa-06-pla-creme.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-06-pla-creme.3mf) | PLA crema | Barriga (barriga), Dedo del pie derecho 3 (dedo-dir-3), Dedo del pie izquierdo 3 (dedo-esq-3), Dedo del pie derecho 1 (dedo-dir-1), Dedo del pie derecho 2 (dedo-dir-2), Dedo del pie izquierdo 1 (dedo-esq-1), Dedo del pie izquierdo 2 (dedo-esq-2) | 28 | 1,5 | Vientre y los 6 dedos de los pies: la cara que se pega va en la cama. |
| 9 | [dino-mesa-11-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-11-pla-verde.3mf) | PLA verde | Mandíbula (mandibula) | 34 | 1,4 | Mandíbula: de pie, con un poco de soporte detrás. |
| 10 | [dino-mesa-09-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-09-pla-verde.3mf) | PLA verde | Carcasa trasera (cadera y cola) (traseira) | 102 | 3,9 | Carcasa trasera: de pie sobre la costura, con soportes tipo árbol solo por dentro. |
| 11 | [dino-mesa-08-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-08-pla-verde.3mf) | PLA verde | Cráneo (cranio) | 179 | 6,8 | Cráneo: soportes tipo árbol por dentro y debajo del paladar. Ningún soporte en la cara. |
| 12 | [dino-mesa-10-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-10-pla-verde.3mf) | PLA verde | Cuerpo (corpo), Collar del cuello (gola), Brazo derecho (braco-dir), Brazo izquierdo (braco-esq) | 303 | 11,7 | Cuerpo, collar y los 2 brazos: la impresión más larga. Déjala para el final, con la impresora ya ajustada. El cuerpo lleva soportes tipo árbol solo por dentro. |
| **Total** |  |  |  | **1010** | **40,2** |  |
<!-- /GERADO -->

## 3. Pieza por pieza

«Paredes» es el número de perímetros. La columna «Soportes» indica si la pieza necesita soportes y dónde. El nombre entre paréntesis es el
nombre del archivo.

<!-- GERADO:pecas -->
| Pieza | Archivo | Cant. | Material y color | Tamaño en la cama (mm) | Cómo va en la cama | Soporte | Paredes | Relleno | Filamento (g) | Tiempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Barriga (barriga) | [dino-barriga.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-barriga.stl) | 1 | PLA crema | 63,4 × 79,4 × 13,3 | base plana (cara del collar) en la cama | no | 3 | 15 % | 22 | 0,9 |
| Dedo del pie derecho 1 (dedo-dir-1) | [dino-dedo-dir-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-1.stl) | 1 | PLA crema | 17,2 × 12,7 × 8,5 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Dedo del pie derecho 2 (dedo-dir-2) | [dino-dedo-dir-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-2.stl) | 1 | PLA crema | 17 × 12,7 × 7,4 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Dedo del pie derecho 3 (dedo-dir-3) | [dino-dedo-dir-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-3.stl) | 1 | PLA crema | 12,7 × 17,4 × 6,9 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Dedo del pie izquierdo 1 (dedo-esq-1) | [dino-dedo-esq-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-1.stl) | 1 | PLA crema | 17,2 × 12,7 × 8,5 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Dedo del pie izquierdo 2 (dedo-esq-2) | [dino-dedo-esq-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-2.stl) | 1 | PLA crema | 17 × 12,7 × 7,4 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Dedo del pie izquierdo 3 (dedo-esq-3) | [dino-dedo-esq-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-3.stl) | 1 | PLA crema | 12,7 × 17,4 × 6,9 | base plana (cara del collar) en la cama | no | 3 | 15 % | 1 | 0,1 |
| Mancha del flanco derecho (mancha-dir) | [dino-mancha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-dir.stl) | 1 | PLA verde oscuro | 17,4 × 17,4 × 8,6 | base plana (cara del collar) en la cama | no | 3 | 15 % | 2 | 0,1 |
| Mancha del flanco izquierdo (mancha-esq) | [dino-mancha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-esq.stl) | 1 | PLA verde oscuro | 17,4 × 17,4 × 8,6 | base plana (cara del collar) en la cama | no | 3 | 15 % | 2 | 0,1 |
| Brazo derecho (braco-dir) | [dino-braco-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-dir.stl) | 1 | PLA verde | 27,5 × 59 × 16 | cara interior (plana) en la cama | no | 3 | 20 % | 8 | 0,4 |
| Brazo izquierdo (braco-esq) | [dino-braco-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-esq.stl) | 1 | PLA verde | 27,5 × 59 × 16 | cara interior (plana) en la cama | no | 3 | 20 % | 8 | 0,4 |
| Cubo del brazo (cubo-braco) | [dino-cubo-braco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cubo-braco.stl) | 2 | PETG grafito | 17 × 17 × 12,8 | punta exterior (2 caras planas) en la cama, rebaje del horn hacia arriba | no | 4 | 60 % | 6 | 0,4 |
| Cuerpo (corpo) | [dino-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-corpo.stl) | 1 | PLA verde | 194,1 × 113,7 × 129,4 | borde inferior (z=5) en la cama, de pie como un vaso; boca (z=134) hacia arriba | sí (soportes en árbol POR DENTRO: techo de los 2 muslos, sobre las ruedas; escalones interiores de los asientos planos (vientre, brazos, manchas); nada por fuera) | 4 | 15 % | 201 | 7,6 |
| Carcasa trasera (cadera y cola) (traseira) | [dino-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-traseira.stl) | 1 | PLA verde | 126,1 × 131 × 131,9 | borde delantero (plano de la unión) en la cama, cola hacia arriba | sí (soportes en árbol POR DENTRO: techo superior de la cadera (53° de la vertical) y nervadura de la ranura de la cresta; nada por fuera) | 4 | 15 % | 102 | 3,9 |
| Collar del cuello (gola) | [dino-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-gola.stl) | 1 | PLA verde | 120,6 × 100,5 × 56,1 | base (z=134) en la cama; la esfera queda hacia arriba y abierta en la parte superior | no | 4 | 20 % | 86 | 3,3 |
| Cresta de la espalda (crista-costas) | [dino-crista-costas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-costas.stl) | 1 | PLA azul | 46,4 × 67,3 × 6 | acostada (lámina de 6 mm) | no | 3 | 15 % | 10 | 0,4 |
| Cráneo (cranio) | [dino-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cranio.stl) | 1 | PLA verde | 134,2 × 174,5 × 118,2 | borde inferior en la cama, de pie | sí (soportes en árbol POR DENTRO: techo del cráneo, fondo de las copas de los ojos y nervadura de la cresta; y por debajo, fuera de la cara: borde del paladar, que queda 40 mm por encima de la cama) | 3 | 15 % | 179 | 6,8 |
| Mandíbula (mandibula) | [dino-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mandibula.stl) | 1 | PLA verde | 91,4 × 37 × 35,6 | cara trasera (plano de corte) en la cama, punta del mentón hacia arriba | sí (poco: bajo el recorte esférico trasero, que nace entre 2 y 10 mm por encima de la cama; cara oculta, orientada hacia el cuello) | 4 | 20 % | 34 | 1,4 |
| Placa de la cabeza (mesa-cabeca) | [dino-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mesa-cabeca.stl) | 1 | PETG grafito | 75,1 × 122,3 × 45,8 | boca abajo: cara superior en la cama | no | 4 | 30 % | 29 | 1,1 |
| Cresta de la cabeza (crista-cabeca) | [dino-crista-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-cabeca.stl) | 1 | PLA azul | 104,9 × 128,3 × 6 | acostada (lámina de 6 mm) | no | 3 | 15 % | 22 | 0,9 |
| Ojo derecho (olho) | [dino-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho.stl) | 1 | PLA blanco | 44 × 44 × 22,6 | cara trasera (plana) sobre la cama | no | 3 | 15 % | 13 | 0,6 |
| Ojo izquierdo (olho-esq) | [dino-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho-esq.stl) | 1 | PLA blanco | 44 × 44 × 22,6 | cara trasera (plana) sobre la cama | no | 3 | 15 % | 15 | 0,6 |
| Iris derecha (iris) | [dino-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris.stl) | 1 | PLA azul | 30 × 30 × 9,9 | cara trasera sobre la cama | no | 3 | 15 % | 5 | 0,3 |
| Iris izquierda (iris-esq) | [dino-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris-esq.stl) | 1 | PLA azul | 30 × 30 × 9,9 | cara trasera sobre la cama | no | 3 | 15 % | 5 | 0,3 |
| Pupila derecha (pupila) | [dino-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila.stl) | 1 | PLA negro | 19 × 19 × 7,9 | cara trasera sobre la cama | no | 3 | 15 % | 2 | 0,2 |
| Pupila izquierda (pupila-esq) | [dino-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila-esq.stl) | 1 | PLA negro | 19 × 19 × 8,2 | cara trasera sobre la cama | no | 3 | 15 % | 2 | 0,2 |
| Chasis (chassi) | [dino-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-chassi.stl) | 1 | PETG grafito | 105,9 × 179,2 × 121 | piso sobre la cama (de pie) | no | 4 | 25 % | 173 | 6,4 |
| Cubierta de la esfera (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 1 | PETG grafito | 29 × 29 × 5,6 | acostada | no | 3 | 15 % | 3 | 0,2 |
| Bandeja para Raspberry Pi (bandeja-pi) | [dino-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-pi.stl) | 1 | PETG amarillo | 61,4 × 89 × 8 | placa sobre la cama, pilares hacia arriba | no | 4 | 25 % | 16 | 0,7 |
| Bandeja para Arduino (bandeja-uno) | [dino-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-uno.stl) | 1 | PETG amarillo | 67,7 × 58,8 × 6 | placa sobre la cama, pilares hacia arriba | no | 4 | 25 % | 12 | 0,5 |
| Horquilla del cuello (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG grafito | 65 × 48 × 50,8 | base sobre la cama, montantes hacia arriba | sí (1,8 mm bajo la base, alrededor del anillo de centrado del horn; soportes normales, fuera de la vista) | 5 | 40 % | 17 | 0,7 |
| Cuna del tilt (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG grafito | 38,5 × 23 × 77 | boca abajo: parte superior de la columna sobre la cama | sí (poco, bajo el puente) | 5 | 40 % | 15 | 0,6 |
| Cupón de prueba (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gris | 70 × 34 × 8 | acostada | no | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **34** |  |  |  |  |  |  | **1010** | **40,2** |
<!-- /GERADO -->

El filamento y el tiempo son estimaciones por volumen, sin laminador. El laminador dará el valor exacto.

## 4. Filamento por color

<!-- GERADO:filamento -->
| Material y color | Filamento (g) | Tiempo (h) |
|---|---|---|
| PETG amarillo | 28 | 1,2 |
| PETG grafito | 243 | 9,4 |
| PLA azul | 42 | 1,9 |
| PLA blanco | 28 | 1,2 |
| PLA gris | 15 | 0,6 |
| PLA crema | 28 | 1,5 |
| PLA negro | 4 | 0,4 |
| PLA verde | 618 | 23,8 |
| PLA verde oscuro | 4 | 0,2 |
| **Total** | **1010** | **40,2** |
<!-- /GERADO -->

## Dónde se refuerza cada pieza

<!-- GERADO:reforcos -->
| Pieza | Refuerzo | Qué es |
|---|---|---|
| Barriga (barriga) | — | vientre crema; pega en el asiento plano del cuerpo |
| Dedo del pie derecho 1 (dedo-dir-1) | — | dedo del pie; pega |
| Dedo del pie derecho 2 (dedo-dir-2) | — | dedo del pie; pega |
| Dedo del pie derecho 3 (dedo-dir-3) | — | dedo del pie; pega |
| Dedo del pie izquierdo 1 (dedo-esq-1) | — | dedo del pie; pega |
| Dedo del pie izquierdo 2 (dedo-esq-2) | — | dedo del pie; pega |
| Dedo del pie izquierdo 3 (dedo-esq-3) | — | dedo del pie; pega |
| Mancha del flanco derecho (mancha-dir) | — | mancha del flanco: ventana del sensor de distancia lateral (fase 2); pega en el asiento plano del cuerpo |
| Mancha del flanco izquierdo (mancha-esq) | — | mancha del flanco: ventana del sensor de distancia lateral (fase 2); pega en el asiento plano del cuerpo |
| Brazo derecho (braco-dir) | — | brazo derecho; encaja a presión en el cubo (2 caras planas), sin tornillo por fuera |
| Brazo izquierdo (braco-esq) | — | brazo izquierdo |
| Cubo del brazo (cubo-braco) | macizo alrededor del rebaje del horn | cubo del brazo: entra por el orificio del hombro, abraza el horn del microservo y se sujeta con el tornillo central del servo (queda oculto por el brazo) |
| Cuerpo (corpo) | 2 pestañas macizas atrás (M3 horizontal en los postes del chasis); labio por dentro del borde trasero; collarín macizo atrás y 3 salientes con inserto roscado en el borde superior; 4 perímetros porque el cuerpo está abierto atrás | piernas, vientre y pecho; baja por encima del chasis; 2 M3 por detrás (cubiertos por la carcasa trasera); el borde trasero encaja en la carcasa trasera |
| Carcasa trasera (cadera y cola) (traseira) | nervadura por dentro a lo largo de la ranura de la cresta; 2 almohadillas en los tornillos inferiores; punta de la cola maciza en forma de cono | cadera + cola: sale hacia atrás y permite acceder a la batería y a las bandejas sin quitar la cabeza; 2 M3 autorroscantes por debajo |
| Collar del cuello (gola) | macizo entre la esfera y la piel exterior (sin techo en voladizo); 3 orificios M3 con rebaje profundo | collar: esfera sobre la que gira la cabeza; se apoya en el borde del cuerpo; 3 M3 por arriba, en los salientes del cuerpo (por dentro, antes de la cabeza) |
| Cresta de la espalda (crista-costas) | — | cresta de la espalda y de la raíz de la cola; encaja a presión o se pega en la ranura de la carcasa trasera |
| Cráneo (cranio) | 3 orejas internas con inserto roscado M3 para la placa de la cabeza; copas de los ojos cerradas por detrás (solo la ventana del cable) | 3 M3x12 por debajo, a través de la placa de la cabeza (en la mesa de trabajo); 2 orificios en la parte superior, bajo la cresta, permiten acceder a los tornillos de la columna |
| Mandíbula (mandibula) | almohadillas macizas a ambos lados del eje; 2 nervaduras que abrazan el horn; punta del mentón maciza delante de un plano a 45° | sin tornillo por fuera: el horn encaja entre 2 nervaduras (derecha) y el pasador de la placa entra en el casquillo ciego (izquierda) |
| Placa de la cabeza (mesa-cabeca) | placa de 4 mm; ventana del servo de la boca con esquinas biseladas | placa de la cabeza: 2 M3x10 en la columna de la cuna (por arriba, por los orificios bajo la cresta); sujeta el servo de la boca y el pasador del eje de la mandíbula |
| Cresta de la cabeza (crista-cabeca) | — | cresta de la cabeza; encaje a presión (sin pegamento): tapa los 2 orificios de acceso a los tornillos de la placa |
| Ojo derecho (olho) | — | ojo derecho: cavidad de la cámara (Camera Module 3) abierta por detrás; a presión o con pegamento en la carcasa del cráneo |
| Ojo izquierdo (olho-esq) | — | ojo izquierdo: cavidad del sensor ToF abierta por detrás |
| Iris derecha (iris) | — | anillo del iris: la placa de la cámara toca su parte trasera (4 orificios guía M2) |
| Iris izquierda (iris-esq) | — |  |
| Pupila derecha (pupila) | — | pupila oscura HUECA en el centro (la lente de la cámara mira por el orificio); encaje a presión, sin pegamento (da acceso a la lente) |
| Pupila izquierda (pupila-esq) | — | pupila oscura hueca (ventana del ToF) |
| Chasis (chassi) | ménsulas a 45° y pared en V bajo la plataforma del pan; travesaño completo desde el piso hasta la plataforma; paredes del rack ensanchadas a 45° desde el piso; postes macizos en los insertos | piso recortado de la sección de la carcasa + rack de bandejas (atrás) + torre y plataforma del servo de pan + orejas de los servos de los brazos + resalte de la esfera trasera |
| Cubierta de la esfera (capa-esfera) | — | anillo que sujeta la esfera de apoyo; 2 M3x8 |
| Bandeja para Raspberry Pi (bandeja-pi) | placa de 3 mm apoyada en ambos rieles a lo largo de todo el rack | bandeja deslizante para Raspberry Pi 4/5 (nivel inferior); sale por detrás, por la abertura; 4 tornillos autorroscantes M2,5x8 |
| Bandeja para Arduino (bandeja-uno) | placa de 3 mm; riel en la pared izquierda y apoyo en la parte superior de la pared derecha | bandeja del Arduino Uno + shield, atravesada (nivel superior); sale por detrás, sin la carcasa trasera; 4 tornillos autorroscantes M3x8 |
| Horquilla del cuello (garfo-pescoco) | NO imprimas las capas a lo largo de los montantes: la carga del tilt flexiona los montantes en el plano de las capas; por eso, 5 perímetros y 40 % de relleno | gira con el servo de pan (horn redondo) y sujeta el eje del tilt |
| Cuna del tilt (berco-tilt) | columna maciza en D (5 perímetros) y puente de 4 mm entre las dos paredes del servo | sujeta el servo de tilt (MG996R de pie) y sube por la abertura del collar hasta la placa de la cabeza; cables por la cara plana de la columna |
| Cupón de prueba (teste-encaixe) | — | cupón de holguras: ventana del servo, 3 orificios para inserto roscado (3,9/4,0/4,1), eje del motor TT, M3 pasante/M3 piloto/M2,5/M2, 3 alojamientos del pin (0,20/0,25/0,30); hoyuelo = medida del diseño |
<!-- /GERADO -->

Después de imprimir: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md) y [LIGACAO.es.md](LIGACAO.es.md).
