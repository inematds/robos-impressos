# Lista de compras del robot cuadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Todo lo que necesitas comprar para armar el robot cuadrado de mesa en la fase 1: el cuerpo ensamblado y conectado. El programa
viene después, en la fase 2.

Página con la misma lista: https://inematds.github.io/robos-impressos/guia/es/cubo/#comprar

## Cómo leer la lista

- **Usa / comprar:** el primer número es lo que usa el robot; el segundo es lo que compras, porque los tornillos y los insertos
  vienen en kits.
- **Los precios están en reales (R$)** y los enlaces abren la búsqueda de Mercado Livre de Brasil. El nombre de cada artículo es el enlace.
- **Precio estimado** es un rango, no un presupuesto. Te sirve para saber el orden de magnitud.
- **Visto en tienda** es el precio consultado el 14/11/2026 en las páginas públicas de usinainfo.com.br. Donde dice
  "no verificado", el rango es solo una referencia. No se consultaron los precios de Mercado Livre.
- **NC** = medida no confirmada. El modelo usa el valor más común de ese componente. Mide tu pieza con el
  calibrador antes de imprimir la parte que hará contacto con ella.

## Riesgos antes de comprar

Lo que aún no se ha probado. Léelo antes de gastar.

<!-- GERADO:riscos -->
- Todavía no se imprimió ni se montó nada. La parte eléctrica de esta página no se probó en el banco de trabajo: se preparó a partir de las fichas de los componentes.
- Los archivos 3MF de las camas nunca se abrieron en Bambu Studio. Si alguno no abre, usa los STL.
- El enchufe USB-C que alimenta la Raspberry Pi no está en el modelo 3D. Puede que no haya espacio para él junto a la Pi, dentro de la cabeza.
- Los pines 31 a 34 de la Raspberry Pi quedan debajo de la placa de la pantalla. El espacio libre allí (17,5 mm en el modelo) es una medida sin confirmar: si el conector bajo no cabe, habrá que soldar los 3 cables de la serial.
- El cupón de prueba no verifica la ventana del servo MG996R ni el agujero del pin M5. Comprueba ambos en la cama 01, antes de las impresiones largas.
- Con el Arduino atornillado a la base, el cable USB no entra: quedan unos 10 mm hasta la pared. Para volver a grabar el programa, hay que quitarle los 4 tornillos.
- El portafusible y los 3 resistores de la serial no tienen un lugar modelado: quedan sueltos en los cables, aislados con tubo termorretráctil.
- Las medidas marcadas como NC provienen de anuncios de tiendas. Mide tu pieza antes de imprimir la parte que hace contacto con ella.
<!-- /GERADO -->

## Cuánto cuesta

<!-- GERADO:custo -->
- Piezas compradas de la fase 1 (sin herramientas ni filamento): **R$ 872–1840**.
- Si ya tienes el Arduino Uno: **R$ 829–1750**.
- Filamento, según el peso de las piezas: R$ 66–110 (735 g; R$ 90–150 el kilo).
<!-- /GERADO -->

## Fase 1: qué comprar

<!-- GERADO:compras -->
### Cerebro, pantalla y movimiento

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | El cerebro del robot. Va dentro de la cabeza, detrás de la pantalla. El Pi 5 también sirve, pero el convertidor de 3 A limita sus puertos USB a 0,6 A. | R$ 450–800 (cada uno) | no verificado |
| [Tarjeta microSD de 32 GB clase 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema del Raspberry Pi. | R$ 25–50 (cada uno) | no verificado |
| [Pantalla TFT de 3,5" 480 × 320 para Raspberry Pi (MPI3501, encaja en el GPIO)](https://lista.mercadolivre.com.br/display-lcd-tft-3.5-raspberry-pi-mpi3501) | 1 / 1 | La cara del robot. Se encaja directamente en los pines 1 a 26 de la Pi, sin tornillos. NC: grosor del conjunto (7 mm) y altura sobre el Pi (24,5 mm). | R$ 90–200 (cada uno) | R$ 193,57 |
| [Servo MG996R de 180° (de posición, no de rotación continua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Uno gira el cuello (pan), el otro inclina la cabeza (tilt). El kit del servo debe incluir el horn redondo (disco). NC: grosor y orificios de las pestañas, diámetro y grosor del horn redondo. | R$ 30–75 (cada uno) | R$ 70,45 |
| [Extensión de servo de 30 cm (cable extensor de 3 hilos, macho-hembra)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Lleva el cable del servo de tilt, que está en la cabeza, por el cuello hasta el shield, que está en la base, con holgura para que la cabeza gire. NC: longitud del cable de fábrica del servo (por lo general 30 cm). | R$ 5–15 (cada uno) | no verificado |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (quizás ya tienes) | 1 / 1 | Controla los 2 servos. Va en el piso de la base, sobre 4 salientes. | R$ 43–90 (cada uno) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Se encaja encima del Uno y ofrece conectores de 3 pines para los servos, con alimentación separada por el borne azul. NC: nombre impreso de los pines de 5 V; compruébalo con el multímetro. | R$ 11–35 (cada uno) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 paquete de 10 | Divisor de tensión en la serial: baja los 5 V del Arduino a los 3,3 V que acepta la Raspberry Pi. | R$ 1–5 (paquete) | no verificado |
| [Barra de pines hembra de 2 filas, paso de 2,54 mm (2 × 20)](https://lista.mercadolivre.com.br/barra-pinos-femea-2x20-2.54mm) | 1 pieza de 2 × 2 / 1 barra | Conector bajo para los pines 31 a 34 de la Raspberry Pi, que quedan debajo de la pantalla. El cable Dupont común no cabe allí en posición vertical. NC: espacio libre entre la Pi y la placa de la pantalla (17,5 mm en el modelo). | R$ 3–10 (cada uno) | no verificado |

### Energía

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Batería 18650 de ion de litio de 3,7 V (celda suelta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | Pack 2S: 7,4 V nominales (8,4 V con carga completa). Compra dos iguales, nuevas y de una marca conocida. | R$ 13–45 (cada uno) | R$ 26,08 el kit con 2 |
| [Soporte para 2 baterías 18650 lado a lado, con cables](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Sujeta las 2 celdas en serie. Se desliza en el soporte de la base y sale por la puerta trasera. NC: la cuna admite hasta 78 × 41 × 22 mm. | R$ 5–15 (cada uno) | R$ 6,22 |
| [Portafusible con cables para fusible de vidrio de 5 × 20 mm, con fusible de 5 A](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (y 1 fusible de repuesto) | En el cable positivo, justo después del soporte de las baterías. Abre el circuito si hay un cortocircuito, antes de que el cable se caliente. No tiene un lugar modelado: queda suelto en el cable. | R$ 4–12 (conjunto) | no verificado |
| [Placa de protección BMS 2S 10 A (modelo 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Corta la descarga profunda, la sobrecarga y el cortocircuito. Va soldada a los cables de la batería y fijada con cinta doble faz. NC: nombre impreso de los pads de soldadura (por lo general B+, BM, B−, P+, P−). | R$ 8–20 (cada uno) | no verificado |
| [Cargador USB-C 2S/3S con balanceo (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carga el pack sin abrir el robot. Requiere un 3.er cable soldado en el punto medio del soporte (entre las dos celdas). NC: tamaño de la abertura USB-C en la ventana trasera (9,2 × 3,4 mm) y nombre impreso de los bornes. | R$ 15–30 (cada uno) | R$ 17,90 |
| [Convertidor step-down LM2596 ajustable (placa azul, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Baja la tensión del pack a los 5 V de la Raspberry Pi y del Arduino. Ajústalo a 5,1 V con el multímetro ANTES de conectar cualquier placa. El XL4015 no sirve aquí: requiere un mínimo de 8 V. | R$ 8–20 (cada uno) | R$ 10,22 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S o equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Alimenta los 2 servos a 6 V, por separado de la Pi. Pon su jumper en 6 V. | R$ 25–60 (cada uno) | no verificado |
| [Capacitor electrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | En el borne de 6 V de los servos: soporta el pico de corriente del arranque. | R$ 1–4 (cada uno) | R$ 2,33 |
| [Interruptor basculante KCD11 (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Enciende y apaga. Se encaja a presión en la pared trasera, por fuera. NC: grosor de panel que acepta el seguro y corriente del interruptor (por lo general 3 A). | R$ 3–8 (cada uno) | R$ 3,74 a R$ 5,40 (modelos KCD1; comprueba el recorte) |
| [Adaptador USB-C macho con bornes (2 pines)](https://lista.mercadolivre.com.br/adaptador-usb-c-macho-borne) | 1 / 1 | Lleva los 5 V del convertidor hasta la entrada USB-C de la Raspberry Pi (los pines de 5 V del GPIO quedan debajo de la pantalla). El enchufe no está en el modelo 3D: comprueba que quepa al lado de la Pi, dentro de la cabeza. | R$ 8–20 (cada uno) | R$ 13,11 |
| [Cable flexible de 22 AWG (0,33 mm²): rojo, negro y un tercer color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | alrededor de 1,5 m de rojo, 1,5 m de negro y 30 cm de amarillo / 2 m de rojo, 2 m de negro, 1 m de amarillo | Toda la parte de alimentación. El amarillo es el 3.º cable, del punto medio del paquete. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Jumpers Dupont de 20 cm (kits de 20: uno hembra-hembra, uno macho-hembra)](https://lista.mercadolivre.com.br/jumper-dupont-20cm) | alrededor de 8 cables / 2 kits de 20 | Señales seriales y los 5 V del Arduino. Para bajarlos por el cuello, empalma dos jumpers o usa un cable de 40 cm con un conector Dupont en un extremo. | R$ 6–12 (kit) | R$ 6,61 el kit |

### Fijación

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Inserto de latón M3 para inserción en caliente (para orificio de 4,0 mm, hasta 5,7 mm de largo)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 16 / 1 paquete de 20 o más | La rosca de metal de las piezas: 4 en la tapa, 1 en la oreja de la puerta, 4 en los pilares del panel del rostro, 4 en las columnas de la estructura, 3 en la horquilla. | R$ 15–40 (paquete) | no verificado |
| [Tornillo M3 × 8 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 13 / 2 kits de 10 | 4 del Arduino, 4 del panel del rostro, 4 del vaso de la cabeza, 1 de la puerta. | R$ 3–8 (kit de 10) | R$ 6,14 el kit de 10 (tipo de cabeza no informado) |
| [Tornillo M3 × 10 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 4 / 1 kit de 10 | Tapa de la base, por debajo. Debe ser Allen de cabeza cilíndrica: la cabeza queda en el fondo de un orificio de 44 mm. | R$ 3–8 (kit de 10) | R$ 3,55 el kit de 10 (Phillips) |
| [Tornillo M3 × 12 mm](https://lista.mercadolivre.com.br/parafuso-m3x12) | 8 / 1 kit de 10 | 4 en cada servo MG996R, enroscados directamente en el plástico (orificio de 2,7 mm). | R$ 3–8 (kit de 10) | no verificado |
| [Tornillo M3 × 45 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x45) | 3 / 3 (se venden por unidad) | Tirantes del cuello: entran por debajo del engranaje, atraviesan el tubo y se enroscan en los insertos de la horquilla. | R$ 1–3 (cada uno) | no verificado |
| [Tornillo M5 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit de 10 (o 1 suelto) | Pin del tilt: pasa por el lateral de la estructura y se enrosca en el brazo de la horquilla. La cabeza se inclina alrededor de él. | R$ 3–8 (kit de 10) | R$ 6,04 el kit de 10 (Phillips) |
| [Tornillo M2,5 × 12 mm con tuerca M2,5](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 tornillos y 4 tuercas / 1 kit | Sujeta la Raspberry Pi al marco, con los 4 espaciadores impresos en el medio. | R$ 5–15 (kit) | no verificado |
| [Tornillo autorroscante M2 × 8 mm](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 en cada horn redondo: fija el engranaje al servo de pan y la horquilla al servo de tilt. NC: diámetro de los orificios del horn redondo. | R$ 3–8 (kit de 10) | R$ 3,31 el kit de 10 (comprueba si es autorroscante) |
| [Brida de nylon de 3,6 mm de ancho (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 paquete de 100 | Una en cada soporte: convertidor de 5 V, UBEC y cargador. | R$ 8–20 (paquete) | no verificado |
| [Cinta de espuma de doble cara](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | alrededor de 5 cm / 1 rollo | Sujeta la placa de protección (BMS) en el compartimento poco profundo del piso. | R$ 8–20 (rollo) | no verificado |

### Herramientas y materiales de soldadura (si no los tienes)

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Cautín de 30 a 60 W, de preferencia con ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Suelda los cables de alimentación y coloca los 16 insertos con calor. | R$ 40–150 (cada uno) | no verificado |
| [Punta de cautín para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guía el inserto recto dentro del agujero. La punta cónica común también sirve: apoya la punta dentro del inserto y empuja despacio. | R$ 15–40 (cada uno) | no verificado |
| [Estaño para soldar con fundente, de 0,8 a 1 mm (tubo pequeño)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todos los empalmes de cables y los pads de soldadura de la placa de protección. | R$ 8–25 (tubo) | no verificado |
| [Tubo termorretráctil de 2 a 3 mm y de 5 a 6 mm (o cinta aislante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | alrededor de 30 cm de cada uno / 1 m de cada uno | Aísla cada empalme de cable. No puede quedar ningún metal expuesto cerca de la batería. | R$ 5–20 (total) | no verificado |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta el convertidor a 5,1 V, comprueba los 6 V del UBEC y la polaridad antes de conectar las placas. | R$ 40–100 (cada uno) | no verificado |
| [Destornillador de precisión de 2 mm](https://lista.mercadolivre.com.br/chave-de-fenda-precisao-2mm) | 1 / 1 | Gira el tornillo de ajuste del LM2596 y aprieta los bornes. | R$ 5–20 (cada uno) | no verificado |
| [Llave Allen larga de 2,5 mm (vástago de 50 mm o más)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Aprieta los 4 tornillos de la tapa desde el fondo de los orificios de la base y los 3 tirantes del cuello. | R$ 8–25 (cada uno) | no verificado |
| [Calibrador](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Comprueba las medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada uno) | no verificado |
| [Fuente USB-C de 15 W o más (5 V 3 A; sirve la del celular) con cable USB-C](https://lista.mercadolivre.com.br/carregador-usb-c-20w) | 1 / 1 | Carga el pack por el puerto USB-C de atrás. El cargador acepta hasta 15 W. | R$ 25–80 (cada uno) | no verificado |
| [Cable USB A-B (el de impresora) y una computadora con Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Graba el sketch en el Arduino Uno antes de atornillarlo a la base. | R$ 8–25 (cada uno) | no verificado |
<!-- /GERADO -->

Opcional: 4 patas de goma adhesivas debajo de la base. No modifican ningún encaje.

## Tornillos e insertos, contados

16 insertos M3 para calor: 4 en la tapa de la base, 1 en la oreja de la puerta, 4 en los pilares del panel de la cara, 4 en las columnas del
marco de la cabeza y 3 en la horquilla.

<!-- GERADO:parafusos -->
| Dónde está | Cant. | Tornillo | Dónde se enrosca |
|---|---|---|---|
| Tapa de la base (por debajo) | 4 | M3 × 10 Allen | inserto en la tapa |
| Puerta trasera | 1 | M3 × 8 | inserto en la oreja de la tapa |
| Arduino Uno | 4 | M3 × 8 | directo en el plástico (orificio de 2,7 mm) |
| Servo de paneo (base) | 4 | M3 × 12 | directo en el plástico (orificio de 2,7 mm) |
| Servo de inclinación (marco de la cabeza) | 4 | M3 × 12 | directo en el plástico (orificio de 2,7 mm) |
| Panel del rostro (por detrás del marco) | 4 | M3 × 8 | inserto en los pilares del panel |
| Copa de la cabeza (pared trasera) | 4 | M3 × 8 | inserto en las columnas del marco |
| Tirantes del cuello | 3 | M3 × 45 Allen | inserto en la horquilla |
| Pasador de inclinación | 1 | M5 × 16 | directamente en el plástico de la horquilla (orificio de 4,4 mm) |
| Raspberry Pi | 4 | M2,5 × 12 + tuerca | tuerca detrás del travesaño |
| Horn redondo de los 2 servos | 8 | M2 × 8 autorroscante | en los orificios del horn |
<!-- /GERADO -->

Los tornillos del horn central y los anillos de goma de los servos vienen en el kit del MG996R.

## Filamento

Gramos por color, sumando las 15 piezas (estimación por volumen, sin laminador). El color es una sugerencia; el material no:
mantén el PETG donde se indica PETG. Un rollo de 1 kg de PETG y uno de PLA son suficientes si no te importan los colores.

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

## Fase 2 (opcional por ahora)

Nada de esto es necesario para imprimir, ensamblar y conectar. Las piezas ya tienen el espacio, los orificios y el paso de los cables.

<!-- GERADO:fase2 -->
| Artículo (el nombre abre la búsqueda) | Cant. | Dónde está | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (placa de 25 × 24 mm) con cable plano](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Detrás del panel de la cara, en el orificio de 8 mm encima de la pantalla. 4 postes con orificio para tornillo M2. NC: orificios y altura de la lente. | R$ 180–350 | no verificado |
| [Tornillo autorroscante M2 × 6 mm](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Sujeta la cámara a los 4 postes. | R$ 3–8 | R$ 5,98 el kit de 10 |
| [Micrófono I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Dentro de la cabeza, sobre los 2 orificios de 2 mm que están debajo de ella. NC: soporte del micrófono aún no modelado. | R$ 15–55 | R$ 54,26 |
| [Altavoz de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Se desliza por los 2 rieles de la pared trasera de la base, contra la rejilla de ranuras verticales. NC: diámetro y profundidad. | R$ 7–20 | no verificado |
| [Amplificador de audio pequeño (PAM8403 o MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Aún no tiene un lugar modelado: va suelto en la base, con cinta doble faz. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimiento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | En el punto universal del piso de la base (par de orificios M3 a 20 mm). | R$ 15–35 | R$ 34,09 |
| [LiDAR LD19 o LD06](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | En la parte superior de la cabeza: 2 orificios ciegos por dentro; la capa de 0,8 mm solo se perfora cuando se instala el sensor. NC: patrón de orificios del sensor. | R$ 400–900 | no verificado |
<!-- /GERADO -->

## Glosario

<!-- GERADO:glossario -->
- **GPIO:** La fila de 40 pines de Raspberry Pi, donde se conectan la pantalla y los cables de señal.
- **UBEC:** Convertidor pequeño, usado en aeromodelos, que reduce el voltaje de la batería a un valor fijo. Aquí, 6 V para los servos.
- **BMS:** Placa de protección de la batería de litio. Desconecta la batería antes de que se descargue demasiado, se sobrecargue o entre en cortocircuito.
- **2S:** Dos celdas de litio conectadas en serie, una después de la otra. Los voltajes se suman: de 6 V (vacía) a 8,4 V (cargada).
- **Horn:** La pieza de plástico que encaja en el eje del servo y gira con él. Este robot usa el horn redondo, en forma de disco.
- **Inserto en caliente:** Buje de latón con rosca interna. Se introduce en el orificio del plástico con el cautín y se convierte en una rosca metálica.
- **NC:** No confirmado: una medida tomada de un anuncio de una tienda que aún no se ha verificado con la pieza en mano.
- **Laminador:** El programa que convierte el archivo 3D en las capas que imprime la impresora. El de Bambu Lab se llama Bambu Studio.
<!-- /GERADO -->

Cómo conectar todo lo que aparece en esta lista: [LIGACAO.es.md](LIGACAO.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
