# Cómo imprimir el carpincho

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Impresora de referencia: Bambu Lab A1 (cama de 256 × 256 × 256 mm), boquilla de 0,4 mm, capa de 0,2 mm.

Sugerencia de ajuste, todavía no probada con estas piezas:

- Placa PEI texturizada para los dos materiales.
- En Bambu Studio, perfil Generic PLA para el PLA y Generic PETG para el PETG, con las temperaturas del perfil.
- Valores habituales para que los compruebes: PLA con la boquilla a 220 °C y la cama a 55–65 °C; PETG con la boquilla a 250–255 °C y la cama a 70–80 °C. La [guía de filamentos de Bambu](https://wiki.bambulab.com/en/general/filament-guide-material-table) indica de 240 a 270 °C para la boquilla con PETG.

Página con las mismas tablas: https://inematds.github.io/robos-impressos/guia/es/capivara/#imprimir

## Los archivos ya están en la posición de impresión

- Cada STL de `projetos/capivara/stl/` está en la posición en la que debe imprimirse: la cara de apoyo en Z = 0. Ábrelo en el laminador e
  imprímelo sin girarlo.
- Cada 3MF de `projetos/capivara/mesas/` incluye las piezas de un color ya acomodadas en una cama de 256 mm.
- Todo de una vez: [capivara-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/capivara-stl.zip)
  (los STL, los 3MF de las camas, el programa de Arduino y las guías).
- Cómo se verificó (14/11/2026): en cada STL, la caja de la pieza tiene el mismo tamaño que el indicado "en la cama" en la tabla de abajo y el
  punto más bajo está en Z = 0.
- Los 3MF son genéricos: solo geometría y posición, sin perfil ni color. Se revisaron con un script, pero todavía no se
  abrieron en Bambu Studio. Si alguno no abre, usa los STL.

## Seis piezas necesitan soportes

Las demás se imprimen sin soportes. En estas seis, activa los soportes en el laminador (en árbol, salvo que la tabla indique otra cosa).
En ninguna parte el soporte toca la cara ni un encaje.

| Pieza | Dónde van los soportes | ¿Se ven? |
|---|---|---|
| Cráneo | Por dentro: techo del cráneo y fondo de las cuencas de los ojos. Por debajo: paladar y curva inferior de las mejillas. | No. Nada en la cara. |
| Cuerpo | Por dentro: techo de las 2 patas, sobre los resaltes de las esferas; esquinas inferiores del relieve de los brazos (1,0 % del área). | No. |
| Puerta trasera | Unos 110 mm² en la curva inferior, por fuera y por debajo. | No: queda orientada hacia el suelo. |
| Mandíbula | Debajo del relieve redondo trasero, por dentro. | No. |
| Horquilla del cuello | 1,8 mm debajo de la base, alrededor del anillo del horn. Soporte normal. | No: queda dentro del collar. |
| Cuna del tilt | Un poco, debajo del puente entre las 2 paredes del servo. | No: queda dentro del collar. |

El verificador del proyecto mide el área sin apoyo de cada pieza y rechaza la que se indicó sin soportes y los necesita.
Todavía nadie ha retirado los soportes de una de estas piezas impresas: empieza con una pieza pequeña, como la mandíbula.

## 1. Imprime primero el cupón de prueba

**Todavía no se imprimió nada de este proyecto.** El cupón de prueba (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
menos de 1 hora) está en la cama 06. Pruébalo:

- un inserto M3 en cada uno de los 3 orificios (3,9, 4,0 y 4,1 mm);
- un tornillo M3 en el orificio pasante (3,4 mm) y otro en el orificio para roscar directamente en el plástico (2,7 mm);
- el microservo en la ventana y el eje del motor de las ruedas en su orificio;
- los orificios M2,5 (Raspberry Pi) y M2 (tornillos de los microservos), para roscar directamente en el plástico.

El hoyuelo marca la medida que usa el proyecto. Si otro agujero queda mejor en tu impresora, no tienes que rehacer las
piezas: en Bambu Studio, la opción X-Y hole compensation (compensación de agujeros X-Y; pestaña Calidad, grupo Precisión, con el
modo avanzado activado) abre o cierra todos los agujeros de la pieza: un valor positivo los abre y uno negativo los cierra
([fuente: código de Bambu Studio](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
La fuente no indica si el valor cuenta por lado o por diámetro: empieza con 0,05 mm e imprime el cupón de prueba de nuevo. El cupón decide.

Quien modifica el código puede cambiar el valor en el bloque `FOLGA` de `comum/cad/parametros.py` y volver a generar las piezas
(`.venv/bin/python comum/cad/gerar.py capivara`).

Tres avisos:

- El cupón es común a los demás robots del proyecto. Los 3 conectores de pines que tiene no se usan en este robot.
- El encaje del servo MG996R no está en el cupón. Comprueba el servo en la cuna del tilt (cama 03, la cuarta en el orden de abajo),
  antes de las impresiones largas.
- El cupón se imprime en PLA, pero 13 de los 18 insertos quedan en piezas de PETG (chasis, cuna y horquilla). Imprime un segundo cupón en PETG. No está en ninguna cama ni en los totales: carga el archivo `comum-teste-encaixe.stl` por separado, con PETG, y calcula unos 15 g y 38 minutos más.

## 2. Orden sugerido de las camas

Primero las piezas pequeñas y el esqueleto; al final, las impresiones largas: el collar, el cráneo y el cuerpo.

<!-- GERADO:mesas -->
| Orden | Archivo de la cama | Material y color | Piezas | Filamento (g) | Tiempo (h) | Por qué va en este orden |
|---|---|---|---|---|---|---|
| 1 | [capivara-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-06-pla-cinza.3mf) | PLA gris | Cupón de prueba (teste-encaixe) | 15 | 0,6 | Empieza por aquí. El cupón de prueba muestra si los insertos roscados, los tornillos M3, el microservo y el eje del motor encajan con la holgura adecuada en TU impresora. Menos de 1 hora. |
| 2 | [capivara-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-01-petg-amarelo.3mf) | PETG amarillo | Bandeja para Raspberry Pi (bandeja-pi), Bandeja para Arduino (bandeja-uno) | 33 | 1,3 | Las 2 bandejas: piezas pequeñas que ya ponen a prueba los agujeros de la Raspberry Pi y del Arduino. |
| 3 | [capivara-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-02-petg-grafite.3mf) | PETG grafito | Placa de la cabeza (mesa-cabeca) | 36 | 1,4 | Placa de la cabeza: comprueba que el microservo de la boca entre en la ventana. |
| 4 | [capivara-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-03-petg-grafite.3mf) | PETG grafito | Chasis (chassi), Horquilla del cuello (garfo-pescoco), 2 × Cubierta de la esfera (capa-esfera), Cuna del tilt (berco-tilt) | 212 | 8,1 | El esqueleto en PETG: chasis, horquilla, cuna y las 2 cubiertas de las esferas. La horquilla y la cuna necesitan soportes. Comprueba que el servo MG996R entre en la cuna antes de las impresiones largas. |
| 5 | [capivara-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-04-pla-branco.3mf) | PLA blanco | Ojo derecho (olho), Ojo izquierdo (olho-esq) | 34 | 1,5 | Los 2 ojos. |
| 6 | [capivara-mesa-09-pla-marrom.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-09-pla-marrom.3mf) | PLA marrón | Hocico (focinho), Cola (rabo), Mano derecha (mao-dir), Mano izquierda (mao-esq), Iris derecha (iris), Iris izquierda (iris-esq), Oreja derecha (orelha-dir), Oreja izquierda (orelha-esq) | 84 | 3,8 | Las piezas marrones: hocico, cola, manos, orejas e iris. La cara para pegar va sobre la cama. |
| 7 | [capivara-mesa-10-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-10-pla-preto.3mf) | PLA negro | 2 × Disco central del aro (miolo), Pupila derecha (pupila), Pupila izquierda (pupila-esq) | 9 | 0,7 | Discos centrales de los aros y pupilas. |
| 8 | [capivara-mesa-05-pla-ciano.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-05-pla-ciano.3mf) | PLA cian | 2 × Aro de la cadera (aro) | 4 | 0,3 | Los 2 aros de las caderas. Filamento translúcido, si quieres poner luz detrás en la fase 2. |
| 9 | [capivara-mesa-11-pla-verde-bandana.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-11-pla-verde-bandana.3mf) | PLA verde-pañuelo | Collar-bandana (gola), Punta de la bandana (avental) | 182 | 6,9 | Collar bandana y la punta de la bandana. |
| 10 | [capivara-mesa-07-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-07-pla-laranja.3mf) | PLA naranja | Cráneo (cranio) | 251 | 9,5 | Cráneo: la pieza más larga de la cabeza. Soportes en árbol por dentro y debajo del paladar. Ningún soporte en la cara. |
| 11 | [capivara-mesa-08-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-08-pla-laranja.3mf) | PLA naranja | Cuerpo (carcasa del cuerpo) (corpo), Copete (topete), Puerta trasera (porta), Mandíbula (mandibula) | 269 | 10,3 | Cuerpo, puerta trasera, mandíbula y copete: la impresión más larga. Déjala para el final, cuando la impresora ya esté ajustada. El cuerpo lleva algunos soportes en árbol por dentro. |
| **Total** |  |  |  | **1129** | **44,4** |  |
<!-- /GERADO -->

## 3. Pieza por pieza

«Paredes» es el número de perímetros. La columna «Soportes» indica si la pieza necesita soportes y dónde. El nombre entre paréntesis es el
nombre del archivo.

<!-- GERADO:pecas -->
| Pieza | Archivo | Cant. | Material y color | Tamaño en la cama (mm) | Cómo va en la cama | Soporte | Paredes | Relleno | Filamento (g) | Tiempo (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Cola (rabo) | [capivara-rabo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-rabo.stl) | 1 | PLA marrón | 52,8 × 58,8 × 29,3 | base plana (cara del collar) en la cama | no | 3 | 15 % | 21 | 0,9 |
| Mano derecha (mao-dir) | [capivara-mao-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-dir.stl) | 1 | PLA marrón | 48,6 × 48,1 × 19,7 | base plana (cara del collar) en la cama | no | 3 | 15 % | 11 | 0,5 |
| Mano izquierda (mao-esq) | [capivara-mao-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-esq.stl) | 1 | PLA marrón | 48,6 × 48,1 × 19,7 | base plana (cara del collar) en la cama | no | 3 | 15 % | 11 | 0,5 |
| Punta de la bandana (avental) | [capivara-avental.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-avental.stl) | 1 | PLA verde-pañuelo | 68,9 × 38,4 × 12,1 | base plana (cara del collar) en la cama | no | 3 | 15 % | 9 | 0,4 |
| Aro de la cadera (aro) | [capivara-aro.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-aro.stl) | 2 | PLA cian | 40 × 40 × 3 | cara plana sobre la cama | no | 3 | 15 % | 4 | 0,3 |
| Disco central del aro (miolo) | [capivara-miolo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-miolo.stl) | 2 | PLA negro | 28 × 28 × 2,4 | cara plana sobre la cama | no | 3 | 15 % | 3 | 0,3 |
| Cuerpo (carcasa del cuerpo) (corpo) | [capivara-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-corpo.stl) | 1 | PLA naranja | 197 × 179,9 × 119 | borde inferior (z=5) sobre la cama, en posición vertical como un jarrón; boca (z=124) hacia arriba | sí (poco, árbol fino: techo interior de las 2 patas, sobre los resaltes de las esferas; esquinas inferiores del relieve de los brazos; extremos inferiores de los 2 bloques traseros; ~1,0 % del área) | 4 | 15 % | 196 | 7,4 |
| Puerta trasera (porta) | [capivara-porta.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-porta.stl) | 1 | PLA naranja | 76,1 × 36,7 × 119 | borde inferior en la cama, de pie | sí (poco: ~110 mm² en la curva inferior, por fuera y por debajo; no se ve) | 4 | 15 % | 38 | 1,5 |
| Collar-bandana (gola) | [capivara-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-gola.stl) | 1 | PLA verde-pañuelo | 159,4 × 155,7 × 68,6 | base (z=124) en la cama; la esfera sube hasta 45° y queda abierta arriba | no | 4 | 20 % | 173 | 6,5 |
| Cráneo (cranio) | [capivara-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-cranio.stl) | 1 | PLA naranja | 181,2 × 187,1 × 134,7 | borde inferior (z=152) en la cama, de pie | sí (árbol POR DENTRO: techo del cráneo y fondo de las copas de los ojos; y por debajo, fuera del rostro: paladar y curva inferior de las mejillas) | 3 | 15 % | 251 | 9,5 |
| Mandíbula (mandibula) | [capivara-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mandibula.stl) | 1 | PLA naranja | 130,4 × 30,8 × 44,3 | cara trasera (plano de corte) en la cama, punta del mentón hacia arriba | sí (poco: ~190 mm² en el alivio esférico trasero, por dentro) | 4 | 20 % | 20 | 0,8 |
| Placa de la cabeza (mesa-cabeca) | [capivara-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mesa-cabeca.stl) | 1 | PETG grafito | 97,2 × 146,5 × 50,3 | boca abajo: cara superior en la cama | no | 4 | 30 % | 36 | 1,4 |
| Ojo derecho (olho) | [capivara-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho.stl) | 1 | PLA blanco | 48 × 48 × 24 | cara trasera (plana) sobre la cama | no | 3 | 15 % | 16 | 0,7 |
| Ojo izquierdo (olho-esq) | [capivara-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho-esq.stl) | 1 | PLA blanco | 48 × 48 × 24 | cara trasera (plana) sobre la cama | no | 3 | 15 % | 18 | 0,8 |
| Iris derecha (iris) | [capivara-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris.stl) | 1 | PLA marrón | 34 × 34 × 10,5 | cara trasera sobre la cama | no | 3 | 15 % | 6 | 0,3 |
| Iris izquierda (iris-esq) | [capivara-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris-esq.stl) | 1 | PLA marrón | 34 × 34 × 10,5 | cara trasera sobre la cama | no | 3 | 15 % | 6 | 0,3 |
| Pupila derecha (pupila) | [capivara-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila.stl) | 1 | PLA negro | 22 × 22 × 8,7 | cara trasera sobre la cama | no | 3 | 15 % | 3 | 0,2 |
| Pupila izquierda (pupila-esq) | [capivara-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila-esq.stl) | 1 | PLA negro | 22 × 22 × 8,9 | cara trasera sobre la cama | no | 3 | 15 % | 3 | 0,2 |
| Hocico (focinho) | [capivara-focinho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-focinho.stl) | 1 | PLA marrón | 77,9 × 59,9 × 18,2 | base plana (cara del collar) en la cama | no | 3 | 15 % | 25 | 1,0 |
| Oreja derecha (orelha-dir) | [capivara-orelha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-dir.stl) | 1 | PLA marrón | 26,3 × 26,8 × 5,4 | base plana (cara del collar) en la cama | no | 3 | 15 % | 2 | 0,2 |
| Oreja izquierda (orelha-esq) | [capivara-orelha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-esq.stl) | 1 | PLA marrón | 26,3 × 26,8 × 5,4 | base plana (cara del collar) en la cama | no | 3 | 15 % | 2 | 0,1 |
| Copete (topete) | [capivara-topete.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-topete.stl) | 1 | PLA naranja | 43,1 × 51,4 × 24,4 | base plana en la cama | no | 3 | 15 % | 15 | 0,6 |
| Chasis (chassi) | [capivara-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-chassi.stl) | 1 | PETG grafito | 149 × 135,8 × 115 | piso sobre la cama (de pie) | no | 4 | 25 % | 174 | 6,4 |
| Cubierta de la esfera (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 2 | PETG grafito | 29 × 29 × 5,6 | acostada | no | 3 | 15 % | 6 | 0,4 |
| Bandeja para Raspberry Pi (bandeja-pi) | [capivara-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-pi.stl) | 1 | PETG amarillo | 61,4 × 93 × 8 | placa sobre la cama, pilares hacia arriba | no | 4 | 25 % | 17 | 0,7 |
| Bandeja para Arduino (bandeja-uno) | [capivara-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-uno.stl) | 1 | PETG amarillo | 61,4 × 77,5 × 8 | placa sobre la cama, pilares hacia arriba | no | 4 | 25 % | 16 | 0,6 |
| Horquilla del cuello (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG grafito | 65 × 48 × 50,8 | base sobre la cama, montantes hacia arriba | sí (1,8 mm bajo la base, alrededor del anillo de centrado del horn; soportes normales, fuera de la vista) | 5 | 40 % | 17 | 0,7 |
| Cuna del tilt (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG grafito | 38,5 × 23 × 77 | boca abajo: parte superior de la columna sobre la cama | sí (poco, bajo el puente) | 5 | 40 % | 15 | 0,6 |
| Cupón de prueba (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gris | 70 × 34 × 8 | acostada | no | 3 | 15 % | 15 | 0,6 |
| **Total** |  | **32** |  |  |  |  |  |  | **1129** | **44,4** |
<!-- /GERADO -->

El filamento y el tiempo son estimaciones por volumen, sin laminador. El laminador dará el valor exacto.

## 4. Filamento por color

<!-- GERADO:filamento -->
| Material y color | Filamento (g) | Tiempo (h) |
|---|---|---|
| PETG amarillo | 33 | 1,3 |
| PETG grafito | 248 | 9,5 |
| PLA blanco | 34 | 1,5 |
| PLA cian | 4 | 0,3 |
| PLA gris | 15 | 0,6 |
| PLA naranja | 520 | 19,8 |
| PLA marrón | 84 | 3,8 |
| PLA negro | 9 | 0,7 |
| PLA verde-pañuelo | 182 | 6,9 |
| **Total** | **1129** | **44,4** |
<!-- /GERADO -->

## Dónde se refuerza cada pieza

<!-- GERADO:reforcos -->
| Pieza | Refuerzo | Qué es |
|---|---|---|
| Cola (rabo) | — | cola; pega en el asiento plano de la puerta |
| Mano derecha (mao-dir) | — | mano derecha; pega |
| Mano izquierda (mao-esq) | — | mano izquierda; pega |
| Punta de la bandana (avental) | — | punta del pañuelo en el pecho; pega en el rebaje de fondo plano |
| Aro de la cadera (aro) | — | aro de las caderas (filamento translúcido para el LED de la fase 2); pega |
| Disco central del aro (miolo) | — | disco oscuro en el centro del aro: ventana del sensor de distancia lateral (fase 2); pega |
| Cuerpo (carcasa del cuerpo) (corpo) | 2 bloques macizos detrás (uno por tornillo M3, desde la piel hasta el poste del chasis; la punta inferior de cada uno nace ~2 mm por encima de la cama y entra en el soporte declarado); el vientre delantero y el fondo trasero están reforzados por debajo; 4 perímetros porque la carcasa del cuerpo está abierta atrás (puerta) | carcasa completa del cuerpo; baja por encima del chasis; 2 M3 por detrás (abajo) + sujeta arriba por el collar; por delante rodea los resaltes de las esferas |
| Puerta trasera (porta) | 2 bloques macizos (uno por tornillo M3, desde la cama hasta el poste); asiento plano de la cola con pared detrás | puerta trasera: la batería y las bandejas salen por aquí sin quitar la cabeza; 2 M3 por detrás (abajo); lleva la cola y el cargador USB-C |
| Collar-bandana (gola) | maciza entre la esfera y el rodillo exterior (sin techo en voladizo); 2 pestañas en la base para los M3 de las orejas de la torre | collar bandana: esfera sobre la que gira la cabeza; se apoya en el borde de la carcasa del cuerpo y la sujeta; 2 M3 por arriba, en las orejas de la torre (por dentro, antes de la cabeza) |
| Cráneo (cranio) | 3 orejas internas con inserto roscado M3 para la placa de la cabeza; copas de los ojos cerradas por detrás (solo la ventana del cable) | 3 M3x12 por debajo, desde la cama (en la mesa de trabajo); 2 orificios arriba dan acceso a los tornillos de la columna |
| Mandíbula (mandibula) | almohadillas macizas a ambos lados del eje; 2 nervaduras que abrazan el horn | sin tornillos por fuera: el horn encaja entre 2 nervaduras (derecha) y el pasador de la placa de la cabeza entra en el zócalo ciego (izquierda); se abre y encaja a presión |
| Placa de la cabeza (mesa-cabeca) | placa de 4 mm; ventana del servo de la boca con esquinas en chaflán (puente de 19,6 mm); asiento cónico del altavoz | placa de la cabeza: 2 M3x10 en la columna de la cuna (por arriba, por los orificios debajo del copete); sostiene el servo de la boca, el pasador del eje de la mandíbula y el altavoz |
| Ojo derecho (olho) | — | ojo derecho: cavidad de la cámara (Camera Module 3) abierta por detrás; a presión o con pegamento en la carcasa del cráneo |
| Ojo izquierdo (olho-esq) | — | ojo izquierdo: cavidad del sensor ToF abierta por detrás |
| Iris derecha (iris) | — | anillo del iris: la placa de la cámara toca su parte trasera (4 orificios guía M2) |
| Iris izquierda (iris-esq) | — |  |
| Pupila derecha (pupila) | — | pupila oscura HUECA en el centro (la lente de la cámara mira por el orificio); encaje a presión, sin pegamento (da acceso a la lente) |
| Pupila izquierda (pupila-esq) | — | pupila oscura hueca (ventana del ToF) |
| Hocico (focinho) | — | tapa marrón del hocico; pegar |
| Oreja derecha (orelha-dir) | — | oreja derecha; pegar |
| Oreja izquierda (orelha-esq) | — | oreja izquierda; pegar |
| Copete (topete) | — | copete; encaje a presión (sin pegamento): tapa los 2 orificios de acceso a los tornillos de la placa de la cabeza |
| Chasis (chassi) | ménsulas y arco a 45° bajo la cubierta del pan; travesaño completo desde el piso hasta la cubierta; postes traseros reforzados (pared de 10 mm alrededor de los insertos); orejas del collar en ménsula; rieles con techo en chaflán | piso recortado de la sección de la piel + soporte de las bandejas (detrás) + torre y cubierta del servo de pan (delante) + resaltes de las 2 esferas |
| Cubierta de la esfera (capa-esfera) | — | anillo que sujeta la esfera de apoyo; 2 M3x8 |
| Bandeja para Raspberry Pi (bandeja-pi) | placa de 3 mm apoyada en ambos rieles a lo largo de todo el rack | bandeja deslizante para Raspberry Pi 4/5 (nivel inferior); sale por detrás, por la abertura; 4 tornillos autorroscantes M2,5x8 |
| Bandeja para Arduino (bandeja-uno) | placa de 3 mm apoyada en ambos rieles a lo largo de todo el rack | bandeja deslizante del Arduino Uno + shield (nivel superior); sale por detrás, por la puerta; 4 M3x8 autorroscantes |
| Horquilla del cuello (garfo-pescoco) | NO imprimas las capas a lo largo de los montantes: la carga del tilt flexiona los montantes en el plano de las capas; por eso, 5 perímetros y 40 % de relleno | gira con el servo de pan (horn redondo) y sujeta el eje del tilt |
| Cuna del tilt (berco-tilt) | columna maciza en D (5 perímetros) y puente de 4 mm entre las dos paredes del servo | sujeta el servo de tilt (MG996R de pie) y sube por la abertura del collar hasta la placa de la cabeza; cables por la cara plana de la columna |
| Cupón de prueba (teste-encaixe) | — | cupón de holguras: ventana del servo, 3 orificios para inserto roscado (3,9/4,0/4,1), eje del motor TT, M3 pasante/M3 piloto/M2,5/M2, 3 alojamientos del pin (0,20/0,25/0,30); hoyuelo = medida del diseño |
<!-- /GERADO -->

Después de imprimir: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md) y [LIGACAO.es.md](LIGACAO.es.md).
