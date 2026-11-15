# Lista de compras del robot cuadrado con ruedas

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Todo lo que necesitas comprar para montar el robot cuadrado con ruedas en la fase 1: el cuerpo montado y conectado. El programa
viene después, en la fase 2.

Página del robot: https://inematds.github.io/robos-impressos/guia/es/cubo-rodas/

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
- El interruptor de 3 A es el punto más débil de la parte eléctrica. Según los datos de las fichas, el robot consume cerca de 2 A en uso normal y cerca de 6,5 A en el peor caso (las 2 ruedas bloqueadas, los 2 servos haciendo fuerza y el Raspberry Pi al máximo). El fusible de 3 A protege el interruptor, pero puede fundirse si el robot hace fuerza contra un obstáculo. Cambiarlo por un interruptor más grande requiere modificar el recorte de 13,5 × 9 mm de la base.
- Los 2 cables de la pantalla, HDMI y USB, no están en el modelo 3D. Según el modelo, quedan cerca de 22 mm debajo del Raspberry Pi y cerca de 30 mm junto a sus puertos USB: los cables rectos que vienen con la pantalla no caben. Este es el principal riesgo de ajuste de este robot. Comprueba el espacio con las piezas en la mano antes de cerrar la cabeza.
- El cargador viene preparado para 2 celdas. Adaptarlo para 3 requiere quitar un resistor diminuto y cerrar un puente de soldadura. Si no funciona, las 3 celdas salen por la tapa de la batería y se cargan en un cargador común para 18650.
- No se pudieron leer los nombres impresos en los pads de soldadura de la placa de protección de 3 celdas ni en los 2 pads de soldadura del medio del cargador. Comprueba cada unión con el multímetro (cerca de 4 V y cerca de 8 V) antes de soldar.
- La posición de los 6 agujeros del motor alrededor del eje es una medida no confirmada. Si no coincide, la pieza que debes volver a imprimir es la brida, un disco pequeño. Compruébalo con el motor en la mano antes de imprimir la base.
- El Raspberry Pi recibe los 5,1 V por los pines 2 y 4, sin pasar por la protección de la entrada USB-C. Un voltaje incorrecto o un cable invertido ahí quema el Pi. Mide en la barra de conexión antes de conectarla.
- El cupón de prueba no verifica la abertura del servo MG996R ni la rosca del tornillo M5. Comprueba la abertura del servo en el marco de la cabeza (mesa 01). La rosca del M5 está en el brazo de la horquilla (mesa 04). Ambas piezas se imprimen antes de las impresiones largas.
- Para volver a grabar el Arduino después de montar el robot, hay que soltar los 4 tornillos de abajo y levantar el torso con el cuello y la cabeza.
- El portafusible, la barra de conexión y los 3 resistores de la comunicación serial no tienen un lugar diseñado: quedan sueltos, aislados con tubo termorretráctil. El cable de cada motor mide cerca de 14 cm y puede que no llegue al driver del motor: si no alcanza, empálmalo.
- Los conectores A0 y A1 del Sensor Shield, que se usan para el segundo cable de cada encoder, no se ven con claridad en la foto de la tienda. Si tu placa no tiene esos pines, deja aislados los 2 cables verdes: el programa de la fase 2 puede contar las vueltas solo con el cable amarillo.
- Las medidas marcadas como NC provienen de anuncios de tiendas. Mide tu pieza antes de imprimir la parte que hace contacto con ella.
- Nunca se probó el paso de los 8 cables por el agujero de la horquilla y la ranura de la parte inferior de la cabeza con las piezas impresas.
- Equilibrio: el verificador muestra que el robot no se cae cuando está quieto, con la cabeza en cualquier posición. Al moverse, el cálculo es una estimación: puede frenar hasta cerca de 3 m/s² sin caerse hacia delante, y el programa de la fase 2 debe usar como máximo la mitad de ese valor. El escalón más alto que puede superar mide cerca de 8 mm.
- Calor: Raspberry Pi 4 queda encerrado en la cabeza, que es de PLA y no tiene abertura de ventilación. El PLA se ablanda cerca de los 60 °C y el Pi reduce la velocidad a partir de los 80 °C. Pega los disipadores y mide con el comando `vcgencmd measure_temp`. Si supera los 70 °C, imprime la carcasa de la cabeza en PETG o abre orificios de ventilación atrás.
<!-- /GERADO -->

## Cuánto cuesta

<!-- GERADO:custo -->
- Piezas de la fase 1 (sin filamento ni herramientas): **R$ 1353–2944**.
- Desde cero (piezas, 2 rollos de filamento y todas las herramientas): **R$ 1737–3909**.
- Solo los 2 rollos de filamento (1 de PETG y 1 de PLA): R$ 170–290.
- Si ya tienes el Arduino Uno, descuenta: R$ 43–90.
- Si ya tienes todas las herramientas, descuenta: R$ 214–675.
<!-- /GERADO -->

Los artículos más caros son el Raspberry Pi, la pantalla de 5 pulgadas y los 2 motores con encoder. No se verificó el
precio de ninguno de los tres en una tienda: sus rangos son solo una referencia.

## Fase 1: qué comprar

<!-- GERADO:compras -->
### Cerebro, pantalla y servos

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | Cerebro del robot. Está dentro de la cabeza, detrás de la pantalla. El Pi 5 también sirve. | R$ 450–800 (cada uno) | no verificado |
| [Tarjeta microSD de 32 GB clase 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema del Raspberry Pi. | R$ 25–50 (cada uno) | no verificado |
| [Pantalla de 5" HDMI, 800 × 480 (Waveshare 5inch HDMI LCD (B), placa de 121 × 89,5 mm)](https://lista.mercadolivre.com.br/display-5-polegadas-hdmi-800x480-raspberry-pi-waveshare) | 1 / 1 | La cara del robot. No se conecta a los pines del Raspberry Pi: se sujeta con 4 tornillos a los pilares del panel de la cara y se conecta al Pi mediante un cable HDMI y un cable USB. Los pilares están diseñados para la placa de 121 × 89,5 mm, con 4 agujeros separados 115 × 84 mm. NC: grosor del conjunto (14 mm en el modelo), diámetro de los 4 agujeros y posición de las entradas HDMI y USB en la placa. | R$ 250–480 (cada uno) | no verificado |
| [Cable HDMI plano y corto (10 a 20 cm): micro-HDMI en ángulo en un extremo, HDMI estándar en el otro](https://lista.mercadolivre.com.br/cabo-hdmi-flat-fpv-micro-hdmi-angulo-20cm) | 1 / 1 | Conecta la pantalla al Raspberry Pi 4, que tiene salida micro-HDMI. El cable que viene con la pantalla es recto y largo: según el modelo, quedan cerca de 22 mm debajo del Pi, así que no cabe. NC: los cables de la pantalla no están en el modelo 3D: comprueba el espacio con las piezas en la mano antes de cerrar la cabeza. | R$ 25–70 (cada uno) | no verificado |
| [Cable USB corto (15 a 20 cm): USB-A en ángulo en un extremo, micro-USB en el otro](https://lista.mercadolivre.com.br/cabo-usb-a-angulo-90-micro-usb-20cm) | 1 / 1 | Lleva energía del Raspberry Pi a la pantalla. Según el modelo, quedan cerca de 30 mm entre los puertos USB del Pi y la pared de la cabeza: el conector recto común no cabe. NC: tipo de entrada USB de la pantalla (micro-USB en el kit del fabricante); los cables no están en el modelo 3D. | R$ 10–30 (cada uno) | no verificado |
| [Servo MG996R de 180° (de posición, no de rotación continua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Uno gira el cuello (pan), el otro inclina la cabeza (tilt). El kit del servo debe incluir el horn redondo (disco). NC: grosor y orificios de las pestañas, diámetro y grosor del horn redondo. | R$ 30–75 (cada uno) | R$ 70,45 |
| [Extensión de servo de 30 cm (cable extensor de 3 hilos, macho-hembra)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Lleva el cable del servo de inclinación, que está en la cabeza, por el cuello hasta el shield, que está en el deck, con holgura para que la cabeza gire. NC: longitud del cable de fábrica del servo (por lo general 30 cm). | R$ 5–15 (cada uno) | no verificado |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (quizás ya tienes) | 1 / 1 | Controla los 2 servos y los 2 motores y lee los encoders. Está en el deck, sobre 4 salientes. | R$ 43–90 (cada uno) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Se conecta encima del Uno y proporciona conectores de 3 pines para los servos, el driver del motor y los encoders, con alimentación separada por el borne azul. El Arduino recibe los 5,1 V por el pin + del conector COM del shield. NC: según la foto de la tienda, el conector COM tiene 4 pines verticales, marcados TX, RX, − y +, y los conectores digitales tienen 3 pines (G, V, S). Los conectores A0 y A1, que se usan para los encoders, no se ven con claridad en la foto. Hay versiones del shield con los pines en otro lugar. Mide antes de conectar. | R$ 11–35 (cada uno) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 paquete de 10 | Divisor de voltaje en la comunicación serial: baja los 5 V del Arduino a los 3,3 V que acepta el Raspberry Pi. Los 3 quedan sujetos en la barra de conexión, en el deck. | R$ 1–5 (paquete) | no verificado |
| [Kit de disipadores adhesivos para Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | Raspberry Pi queda encerrado dentro de la cabeza, que es de PLA y no tiene abertura de ventilación. Los disipadores pegados a los chips reducen la temperatura. NC: altura del disipador: debe caber en los cerca de 20 mm entre el Pi y la pantalla. | R$ 8–25 (kit) | no verificado |

### Ruedas y motores

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Motor JGB37-520 de 12 V con encoder, 107 rpm (reducción 1:56), eje en D de 6 mm](https://lista.mercadolivre.com.br/motor-jgb37-520-12v-encoder-107rpm) | 2 / 2 | Tracción: un motor por rueda. Cada motor viene con un cable de 6 hilos: 2 del motor y 4 del encoder, el sensor que cuenta las vueltas de la rueda. Elige la versión de 12 V y 107 rpm. NC: posición de los 6 orificios M3 alrededor del eje, que queda a 7 mm del centro, y profundidad de la rosca (3,5 a 4 mm). | R$ 60–150 (cada uno) | no verificado |
| [Rueda de 85 × 38 mm con acople hexagonal de 12 mm](https://lista.mercadolivre.com.br/roda-85mm-sextavado-12mm-robo) | 2 / 2 | Las 2 ruedas delanteras. El radio de 42,5 mm permite que el robot pase por umbrales bajos. | R$ 30–60 (cada uno) | R$ 38,87 cada una |
| [Adaptador hexagonal de 12 mm para eje de 6 mm (acople de rueda, con tornillo de fijación)](https://lista.mercadolivre.com.br/adaptador-sextavado-12mm-eixo-6mm-roda) | 2 / 2 | Sujeta la rueda al eje del motor. NC: longitud (20 mm en el modelo; el de latón común mide cerca de 18 mm). | R$ 10–30 (cada uno) | no verificado |
| [Pelota de tenis de mesa de 40 mm](https://lista.mercadolivre.com.br/bola-tenis-de-mesa-40mm) | 1 / 1 paquete | Apoyo trasero: rueda libre dentro de un alojamiento de la base, sujeta por la tapa. Es lo que limita el escalón que el robot puede pasar: cerca de 8 mm. NC: las pelotas marcadas 40+ miden de 40,0 a 40,6 mm; el alojamiento mide 41,2 mm. | R$ 5–20 (paquete) | no verificado |
| [Driver del motor L298N (módulo de puente H doble, 2 A por canal)](https://lista.mercadolivre.com.br/driver-motor-l298n-ponte-h) | 1 / 1 | Enciende, apaga e invierte los 2 motores. Va en el deck, sobre 4 salientes. Reduce cerca de 2 V para los motores: con el pack a 11 V, reciben cerca de 9 V, lo que este robot admite. NC: distancia entre los 4 orificios (37 mm en el modelo) y nombre impreso de los pines y los jumpers. | R$ 18–35 (cada uno) | R$ 21,51 a R$ 29,18 |

### Energía

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Batería 18650 de ion de litio de 3,7 V (celda suelta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 3 / 3 | Pack 3S: 11,1 V nominales (12,6 V con carga completa). Compra las tres iguales, nuevas y de una marca conocida. | R$ 13–45 (cada uno) | R$ 26,08 el kit con 2 |
| [Soporte para 3 baterías 18650 lado a lado, con cables](https://lista.mercadolivre.com.br/suporte-3-baterias-18650) | 1 / 1 | Sujeta las 3 celdas en serie. Va fijado a la tapa de la batería, que se retira por debajo del robot con 4 tornillos. NC: el alojamiento de la tapa de la batería se diseñó para 75 × 61 × 20 mm. | R$ 6–18 (cada uno) | R$ 7,80 |
| [Portafusible con cables para fusible de vidrio de 5 × 20 mm, con fusible retardado de 3 A (marcado T3A o T3,15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (y 1 fusible de repuesto) | En el cable positivo, justo después del soporte de las baterías. Es de 3 A porque el interruptor es de 3 A: ante una sobrecarga, el fusible se abre antes de que el interruptor se caliente. Es de acción retardada porque el arranque de los motores y los servos y la carga del capacitor producen picos de una fracción de segundo, que quemarían un fusible rápido aunque no hubiera ninguna falla. No tiene un lugar diseñado en el modelo: queda suelto en el cable. | R$ 4–12 (conjunto) | no verificado |
| [Placa de protección BMS 3S 10 A (modelo HX-3S-FL10, 50 × 15 mm)](https://lista.mercadolivre.com.br/bms-3s-10a-18650-hx-3s-fl10) | 1 / 1 | Corta la descarga profunda, la sobrecarga y el cortocircuito. Va soldada a los cables de la batería y fijada con cinta doble faz al piso de la base. Esta placa no equilibra las celdas: el cargador es el que las equilibra. NC: nombre impreso de los pads de soldadura (no aparece en la página de la tienda). En general son 0V, 4,2V, 8,4V y 12,6V del lado de las celdas, y P+ y P− del lado de la salida. Comprueba con el multímetro. | R$ 15–30 (cada uno) | R$ 21,60 |
| [Cargador USB-C 2S/3S con balanceo (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carga el pack sin abrir el robot. Viene listo para 2 celdas. Para 3 celdas hay que quitar un resistor diminuto de la placa y cerrar un jumper con soldadura, como muestra la figura de la página de la tienda. En el modo de 3 celdas usa 4 cables: positivo, negativo y las 2 uniones entre las celdas. NC: nombre impreso de los pads de las 2 uniones (no se alcanza a leer en la foto de la tienda) y tamaño de la abertura USB-C en la ventana trasera (9,2 × 3,4 mm). | R$ 15–30 (cada uno) | R$ 17,90 |
| [Convertidor step-down XL4015 ajustable (5 A)](https://lista.mercadolivre.com.br/modulo-step-down-xl4015-5a) | 1 / 1 | Reduce el voltaje del pack a los 5,1 V del Raspberry Pi, el Arduino, el driver y los encoders. Ajústalo a 5,1 V con el multímetro ANTES de conectar cualquier placa. Requiere un mínimo de 8 V de entrada, y el pack de 3 celdas siempre está por encima de ese valor. | R$ 12–30 (cada uno) | R$ 17,82 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S o equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Alimenta los 2 servos a 6 V, por separado de la Pi. Pon su jumper en 6 V. | R$ 25–60 (cada uno) | no verificado |
| [Capacitor electrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | En el borne de 6 V de los servos: soporta el pico de corriente del arranque. | R$ 1–4 (cada uno) | R$ 2,33 |
| [Interruptor basculante KCD11-101 de 3 A (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Enciende y apaga. Encaja a presión en la pared trasera de la base, por fuera. La ficha indica 3 A a 250 V~ y 6 A a 125 V~, sin especificar un valor para corriente continua: por eso el fusible es de 3 A. Es el punto más débil de la parte eléctrica de este robot (mira los riesgos). NC: grosor de panel que admite el seguro. | R$ 3–8 (cada uno) | R$ 3,74 a R$ 5,40 (modelos KCD1; comprueba el recorte) |
| [Cable flexible de 22 AWG (0,33 mm²): rojo, negro y un tercer color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | cerca de 50 cm de rojo, 30 cm de negro y 80 cm de amarillo / 2 m de rojo, 2 m de negro, 1 m de amarillo | Los cables finos de alimentación: los 4 cables de las uniones entre las celdas (amarillos), las conexiones del cargador y los 5,1 V del driver. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Cable flexible 20 AWG (0,5 mm²), rojo y negro](https://lista.mercadolivre.com.br/fio-flexivel-20awg-vermelho-preto) | cerca de 1,1 m de cada color / 2 m de cada color | Los cables que llevan más corriente: desde el interruptor y la placa de protección hasta la barra de conexión, desde la barra hasta el convertidor y el driver del motor, y el par de 5,1 V que sube por el cuello hasta la Raspberry Pi. Un cable más grueso pierde menos tensión en el recorrido; con un cable fino, la Pi indica subtensión. | R$ 8–25 (total) | no verificado |
| [Barra de conexión de 12 vías (tipo sindal), para cable fino](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 5 vías (bornes 1 a 5) / 1 barra de 12 vías; corta un tramo de 5 | Va en el deck y evita soldar con el robot montado. Borne 1: los 5,1 V. Borne 2: el negativo. Borne 3: el cable azul de la comunicación serial y los resistores del divisor. Borne 4: el positivo del paquete de baterías, después del interruptor. Borne 5: el negativo del paquete de baterías. No tiene un lugar modelado: queda suelta. | R$ 3–10 (barra) | no verificado |
| [Jumpers Dupont hembra-hembra de 40 cm (kit con 40)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-40cm) | 16 cables / 1 kit de 40 | Son 16: 3 de la comunicación serial (verde, azul y negro, desde la Raspberry Pi hasta el deck), 2 que llevan los 5,1 V y el negativo de la barra de conexión al Arduino, 1 cortado por la mitad para el divisor, 2 cortados por la mitad para la alimentación de la Raspberry Pi, 6 del driver del motor y 2 cortados por la mitad para los encoders. Los de la comunicación serial quedan justos: si falta cable, empalma un tramo de jumper en la punta del deck, con soldadura y tubo termorretráctil, todavía en el preparativo 3. | R$ 10–25 (kit) | no verificado |

### Fijación

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Inserto de latón M3 para inserción en caliente (para orificio de 4,0 mm, hasta 5,7 mm de largo)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 31 / 2 paquetes de 20 (o 1 de 50) | La rosca metálica de las piezas: 8 en las paredes de los motores, 4 de la tapa de la batería y 4 de la tapa de la bola (todas en la base), 4 en las columnas del torso, 4 en los pilares del panel del rostro, 4 en las columnas del cuadro y 3 en la horquilla. | R$ 15–40 (paquete) | no verificado |
| [Tornillo M3 × 6 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x6) | 12 / 2 kits de 10 | 6 en cada motor: sujetan el motor a la brida, con la cabeza en el rebaje. NC: fondo de la rosca del motor: 3,5 a 4 mm. Después de la brida quedan 4 mm de tornillo. Si toca el fondo antes de apretarlo, cámbialo por M3 × 5. | R$ 3–8 (kit de 10) | no verificado |
| [Tornillo M3 × 8 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 24 / 3 kits de 10 | 4 de la tapa de la batería, 4 de la tapa de la bola, 4 del Arduino, 4 del driver del motor, 4 del panel del rostro y 4 de la carcasa de la cabeza. | R$ 3–8 (kit de 10) | R$ 6,14 el kit de 10 (tipo de cabeza no informado) |
| [Tornillo M3 × 10 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 8 / 1 kit de 10 | 4 en cada brida del motor, en los insertos de la pared de la base. Quedan ocultos detrás de la rueda. | R$ 3–8 (kit de 10) | R$ 3,55 el kit de 10 (Phillips) |
| [Tornillo M3 × 12 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x12) | 12 / 2 kits de 10 | 4 en cada servo MG996R, atornillados directamente al plástico (orificio de 2,7 mm), y 4 que entran por debajo de la base, atraviesan el deck y se atornillan en los insertos del torso. Estos 4 deben ser Allen de cabeza cilíndrica: la cabeza queda al fondo de un orificio de 68 mm. | R$ 3–8 (kit de 10) | no verificado |
| [Tornillo M3 × 50 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x50) | 3 / 3 (se venden por unidad) | Tirantes del cuello: entran por dentro del torso, pasan por el engranaje, atraviesan el tubo y se atornillan en los insertos de la horquilla. | R$ 1–4 (cada uno) | no verificado |
| [Tornillo M5 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit de 10 (o 1 suelto) | Pin del tilt: pasa por el lateral de la estructura y se enrosca en el brazo de la horquilla. La cabeza se inclina alrededor de él. | R$ 3–8 (kit de 10) | R$ 6,04 el kit de 10 (Phillips) |
| [Tornillo M2,5 × 12 mm con tuerca M2,5](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 tornillos y 4 tuercas / 1 kit | Sujeta la Raspberry Pi al marco, con los 4 espaciadores impresos en el medio. | R$ 5–15 (kit) | no verificado |
| [Tornillo M2,5 × 6 mm](https://lista.mercadolivre.com.br/parafuso-m2.5x6) | 4 / 1 kit | Sujeta la pantalla de 5 pulgadas a los 4 pilares del panel del rostro, atornillado directamente al plástico. NC: diámetro de los orificios de la placa de la pantalla. | R$ 5–15 (kit) | no verificado |
| [Tornillo autorroscante M2 × 8 mm](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 en cada horn redondo: fija el engranaje al servo de pan y la horquilla al servo de tilt. NC: diámetro de los orificios del horn redondo. | R$ 3–8 (kit de 10) | R$ 3,31 el kit de 10 (comprueba si es autorroscante) |
| [Brida de nylon de 3,6 mm de ancho (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 4 / 1 paquete de 100 | Una en cada soporte: convertidor de 5 V, UBEC, cargador y soporte de las baterías, en la tapa de la batería. | R$ 8–20 (paquete) | no verificado |
| [Cinta de espuma de doble cara](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | alrededor de 5 cm / 1 rollo | Sujeta la placa de protección (BMS) al piso de la base. | R$ 8–20 (rollo) | no verificado |

### Filamento

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Filamento PETG de 1,75 mm, rollo de 1 kg](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 823 g, en 4 colores sugeridos (amarillo, blanco, grafito y plata) / 1 rollo de cualquier color (o 4 rollos, uno de cada color sugerido) | Las piezas que soportan esfuerzo: base, tapa de la batería, tapa de la bola, bridas, deck, torso, cuello, engranajes, horquilla y cuadro de la cabeza. El color es solo una sugerencia; el material no: mantén PETG. Un rollo de 1 kg alcanza con poco sobrante: el cálculo es una estimación sin laminador, y si una pieza grande falla a mitad de impresión, faltará filamento. | R$ 90–150 (rollo) | no verificado |
| [Filamento PLA de 1,75 mm, rollo de 1 kg](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 320 g, en 3 colores sugeridos (blanco, gris y negro) / 1 rollo de cualquier color (o 3 rollos, uno de cada color sugerido) | Las piezas que solo recubren el robot: carcasa de la cabeza, panel del rostro, espaciadores y cupón de prueba. El color es solo una sugerencia. | R$ 80–140 (rollo) | no verificado |

### Herramientas y materiales de soldadura (si no los tienes)

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Cautín de 30 a 60 W, de preferencia con ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Suelda los cables de alimentación y coloca los 31 insertos en caliente. Con la punta fina, también cierra el puente de soldadura del cargador. | R$ 40–150 (cada uno) | no verificado |
| [Punta de cautín para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guía el inserto recto dentro del agujero. La punta cónica común también sirve: apoya la punta dentro del inserto y empuja despacio. | R$ 15–40 (cada uno) | no verificado |
| [Estaño para soldar con fundente, de 0,8 a 1 mm (tubo pequeño)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todos los empalmes de cables y los pads de soldadura de la placa de protección. | R$ 8–25 (tubo) | no verificado |
| [Tubo termorretráctil de 2 a 3 mm y de 5 a 6 mm (o cinta aislante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | alrededor de 30 cm de cada uno / 1 m de cada uno | Aísla cada empalme de cable. No puede quedar ningún metal expuesto cerca de la batería. | R$ 5–20 (total) | no verificado |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta el convertidor a 5,1 V, comprueba los 6 V del UBEC, las uniones entre celdas (cerca de 4 V y 8 V) y la polaridad antes de conectar las placas. | R$ 40–100 (cada uno) | no verificado |
| [Destornillador plano de precisión de 2 mm y destornillador Phillips pequeño (PH0 o PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | El destornillador plano gira el tornillo de ajuste del XL4015 y aprieta los bornes. El Phillips aprieta los tornillos M2 de los horns, el tornillo central de los servos y los tornillos de cabeza Phillips. | R$ 10–35 (cada uno) | no verificado |
| [Alicates de corte pequeños](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Corta los cables, las patas de los resistores y el sobrante de las bridas. | R$ 15–40 (cada uno) | no verificado |
| [Pelacables (o un cúter, con cuidado)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Retira el aislamiento de los extremos de los cables 20 y 22 AWG sin cortar los hilitos de cobre. | R$ 15–45 (cada uno) | no verificado |
| [Pinzas de punta fina](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Pasa las puntas de los cables por la ranura de la parte inferior de la cabeza, sujeta los resistores al soldar y retira el resistor diminuto del cargador. | R$ 5–20 (cada uno) | no verificado |
| [Llave Allen larga de 2,5 mm (vástago de 80 mm o más)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa-haste-100mm) | 1 / 1 | Aprieta los 4 tornillos que entran por debajo de la base, al fondo de orificios de 68 mm, y los 3 tirantes del cuello. | R$ 8–25 (cada uno) | no verificado |
| [Calibrador](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Comprueba las medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada uno) | no verificado |
| [Fuente USB-C de 5 V y 3 A (15 W), con cable USB-C](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Carga el paquete por el puerto USB-C trasero y alimenta el Raspberry Pi en el preparativo 4. Para el Pi 4, debe entregar 5 V y 3 A: muchas fuentes de celular no alcanzan esa capacidad (lee la etiqueta). La fuente oficial del Raspberry Pi 4, de 5,1 V y 3 A, es la opción segura. | R$ 25–80 (cada uno) | no verificado |
| [Cable USB A-B (el de impresora) y una computadora con Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Graba el sketch en el Arduino Uno antes de cerrar el robot. | R$ 8–25 (cada uno) | no verificado |
| [Lector de tarjetas microSD (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Graba el sistema del Raspberry Pi en la tarjeta desde tu computadora. Muchas laptops ya tienen una ranura. | R$ 10–30 (cada uno) | no verificado |
<!-- /GERADO -->

## Tornillos e insertos, contados

31 insertos M3 de inserción en caliente: 8 en las paredes de los motores, 4 de la tapa de la batería y 4 de la tapa de la bola (los 16 quedan en la base), 4 en las columnas del torso, 4 en los pilares del panel del rostro, 4 en las columnas del marco de la cabeza y 3 en la horquilla.

<!-- GERADO:parafusos -->
| Dónde está | Cant. | Tornillo | Dónde se enrosca |
|---|---|---|---|
| Motor en la brida (6 por motor) | 12 | M3 × 6 Allen | rosca del propio motor |
| Brida en la pared de la base (4 en cada lado) | 8 | M3 × 10 Allen | inserto en la pared de la base |
| Tapa de la batería (por debajo) | 4 | M3 × 8 | inserto en el piso de la base |
| Tapa de la bola (por debajo) | 4 | M3 × 8 | inserto en el piso de la base, alrededor del hueco |
| Arduino Uno (deck) | 4 | M3 × 8 | directo en el plástico (orificio de 2,7 mm) |
| Driver L298N (deck) | 4 | M3 × 8 | directo en el plástico (orificio de 2,7 mm) |
| Servo de pan (deck) | 4 | M3 × 12 | directo en el plástico (orificio de 2,7 mm) |
| Base + deck + torso (por debajo, en la base de los 4 postes) | 4 | M3 × 12 Allen | inserto en la columna del torso |
| Servo de inclinación (marco de la cabeza) | 4 | M3 × 12 | directo en el plástico (orificio de 2,7 mm) |
| Pantalla de 5 pulgadas (pilares del panel del rostro) | 4 | M2,5 × 6 | directo en el plástico (orificio de 2,2 mm) |
| Panel del rostro (por detrás del marco) | 4 | M3 × 8 | inserto en los pilares del panel |
| Copa de la cabeza (pared trasera) | 4 | M3 × 8 | inserto en las columnas del marco |
| Tirantes del cuello (por dentro del torso) | 3 | M3 × 50 Allen | inserto en la horquilla |
| Pasador de inclinación | 1 | M5 × 16 | directamente en el plástico de la horquilla (orificio de 4,4 mm) |
| Raspberry Pi | 4 | M2,5 × 12 + tuerca | tuerca detrás del travesaño |
| Horn redondo de los 2 servos | 8 | M2 × 8 autorroscante | en los orificios del horn |
<!-- /GERADO -->

Los tornillos del horn central y los anillos de goma de los servos vienen en el kit del MG996R. El tornillo de bloqueo y el tornillo de la punta del adaptador hexagonal vienen con el adaptador.

## Filamento

Gramos por color, sumando las 19 piezas (estimación por volumen, sin laminador). El color es una sugerencia; el material no:
mantén PETG donde indica PETG. El mínimo son 2 rollos de 1 kg, uno de PETG y otro de PLA, de cualquier color. Casi todo el PETG se usa en el robot: si falla una impresión larga, faltará material. Con los 7 colores sugeridos son 7 rollos, 4 de PETG y 3 de PLA, y sobrará mucho filamento. Las dos líneas de filamento están en la lista de arriba.

<!-- GERADO:filamento -->
| Material y color | Filamento (g) | Tiempo (h) |
|---|---|---|
| PETG amarillo | 108 | 4,1 |
| PETG blanco | 236 | 8,7 |
| PETG grafito | 454 | 17,1 |
| PETG plateado | 25 | 1,1 |
| PLA blanco | 248 | 9,3 |
| PLA gris | 15 | 0,9 |
| PLA negro | 57 | 2,2 |
| **Total** | **1143** | **43,4** |
<!-- /GERADO -->

## Fase 2 (opcional por ahora)

Nada de esto es necesario para imprimir, montar y conectar. Las piezas ya tienen su lugar, los orificios y el paso de los cables, y ninguno de esos orificios se ve de frente: la columna «Dónde va» indica dónde queda escondido cada uno.

<!-- GERADO:fase2 -->
| Artículo (el nombre abre la búsqueda) | Cant. | Dónde está | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (placa de 25 × 24 mm) con cable plano](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Detrás del panel de la cara, en el orificio de 8 mm encima de la pantalla. 4 postes con orificio para tornillo M2. NC: orificios y altura de la lente. | R$ 180–350 | no verificado |
| [Tornillo autorroscante M2 × 6 mm](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Sujeta la cámara a los 4 postes. | R$ 3–8 | R$ 5,98 el kit de 10 |
| [Micrófono I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Dentro de la cabeza, sobre los 2 orificios de 2 mm que están debajo. No se ven de frente ni de lado. NC: soporte del micrófono aún no modelado. | R$ 15–55 | R$ 54,26 |
| [Altavoz de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Se desliza por los 2 rieles de la pared trasera del torso, contra la rejilla de ranuras verticales. Solo se ve por detrás. NC: diámetro y profundidad. | R$ 7–20 | no verificado |
| [Amplificador de audio pequeño (PAM8403 o MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Todavía no tiene un lugar diseñado: queda suelto sobre el deck, con cinta doble cara. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimiento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | En el punto universal del deck (par de orificios M3 separados por 20 mm), cerca del eje de las ruedas. | R$ 15–35 | R$ 34,09 |
| [LiDAR LD19](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | En la parte superior de la cabeza, el único lugar con 360° libres: 3 orificios ciegos por dentro y un rebaje ciego para el cable. La pared de 0,8 mm solo se perfora cuando se instala el sensor; hasta entonces, no se ve nada por fuera. Con él, el robot queda con 341 mm de altura. NC: posición de los 3 orificios en el cuerpo del sensor. | R$ 400–900 | no verificado |
| [Sensor de distancia ToF VL53L1X (placa pequeña)](https://lista.mercadolivre.com.br/sensor-vl53l1x-tof) | 3 | Por dentro de la pared de la base, 10 mm por debajo del borde superior: uno al frente y uno a cada lado. Cada punto tiene 2 agujeros ciegos para tornillos M2,5 y, entre ellos, una ventana ciega: por fuera, la pared es lisa, con 0,8 mm de plástico delante de la ventana. Durante la instalación, perfora esa capa desde dentro, en el centro de la ventana, con un clavo o una aguja caliente: el taladro no cabe dentro de la base. El pequeño agujero marca el centro por fuera; ensánchalo desde fuera con una broca de 6 mm. Después de eso, quedan 3 agujeros de 6 mm visibles en la base. NC: tamaño de la placa (25 × 10,7 mm) y distancia entre los orificios. | R$ 40–110 | R$ 102,32 |
| [Sensor de caída (infrarrojo reflectivo, por ejemplo TCRT5000)](https://lista.mercadolivre.com.br/sensor-reflexivo-infravermelho-tcrt5000) | 1 | En una ventana de 14 × 6 mm en el piso de la base, al frente, apuntando al suelo, con un par de orificios M3 separados por 20 mm. Solo se ve desde abajo. | R$ 5–15 | R$ 7,92 |
<!-- /GERADO -->

## Glosario

<!-- GERADO:glossario -->
- **GPIO:** La fila de 40 pines del Raspberry Pi, donde se conectan los cables de alimentación y señal. En esta guía, "pin 32" es la posición del pin en la fila; "GPIO12" es el nombre de la señal que sale por él.
- **UBEC:** Convertidor pequeño, usado en aeromodelos, que reduce el voltaje de la batería a un valor fijo. Aquí, 6 V para los servos.
- **BMS:** Placa de protección de la batería de litio. Desconecta la batería antes de que se descargue demasiado, se sobrecargue o entre en cortocircuito.
- **3S:** Tres celdas de litio conectadas en serie, una después de la otra. Los voltajes se suman: de 9 V (vacía) a 12,6 V (llena).
- **Unión entre celdas (del pack):** El punto donde una celda se conecta con la siguiente. En un pack de 3 celdas hay 2 uniones. La placa de protección y el cargador miden cada celda a través de ellas.
- **Horn:** La pieza de plástico que encaja en el eje del servo y gira con él. Este robot usa el horn redondo, en forma de disco.
- **Inserto en caliente:** Buje de latón con rosca interna. Se introduce en el orificio del plástico con el cautín y se convierte en una rosca metálica.
- **NC:** No confirmado: una medida tomada de un anuncio de una tienda que aún no se ha verificado con la pieza en mano.
- **Laminador:** El programa que convierte el archivo 3D en las capas que imprime la impresora. El de Bambu Lab se llama Bambu Studio.
- **SSH:** Forma de usar el Raspberry Pi por la red: escribes los comandos en la terminal de tu computadora y se ejecutan en el Pi, sin conectarle teclado ni monitor.
- **UART (serial):** Conexión de datos sencilla: un cable para hablar (TX) y otro para escuchar (RX). Por ella, el Raspberry Pi envía órdenes al Arduino.
- **Driver del motor (puente H):** Placa que conecta los motores a la batería e invierte su sentido cuando Arduino lo indica. Aquí es el L298N.
- **Encoder:** Sensor sujeto detrás del motor que cuenta las vueltas. Con él, el programa sabe cuánto avanzó cada rueda.
- **Jumper SEL:** Cubierta de plástico sobre 2 pines del Sensor Shield, junto al borne azul, con la marca SEL. Colocada, conecta los 5 V del Arduino a los conectores de los servos. Retirada, los servos reciben solo lo que entra por el borne azul.
- **Borne:** Conector de tornillo: el cable entra por el orificio y se aprieta con el tornillo. En el Sensor Shield es el bloque azul marcado GND y VCC.
- **Sketch:** El nombre que Arduino le da a un programa. Abres el archivo en Arduino IDE y lo grabas en la placa con el cable USB.
- **Shield:** Placa que se conecta encima del Arduino, en sus pines, y agrega conectores. Aquí, el Sensor Shield proporciona los conectores para los servos, el driver y los encoders.
- **AWG:** Medida del grosor del cable. Cuanto menor es el número, más grueso es: el de 20 AWG es más grueso que el de 22 AWG.
- **GND:** El negativo del circuito, también llamado tierra. Todos los negativos del robot están conectados entre sí.
- **Dupont:** Cable delgado que ya viene con un conector de encaje en cada extremo, del tamaño de los pines de las placas. También se llama jumper.
- **Step-down:** Convertidor que reduce el voltaje. Aquí, el XL4015 reduce el voltaje de la batería a 5,1 V.
- **Tubo termorretráctil:** Tubito de plástico que se encoge con el calor. Lo colocas sobre la unión soldada y lo calientas: se ajusta y aísla.
- **Tapa de la batería:** La tapa que va debajo de la base. Lleva el soporte de las baterías y se quita con 4 tornillos, sin abrir el resto del robot.
- **Brida:** El disco que fija cada motor a la pared de la base. Queda oculto detrás de la rueda.
- **Deck:** La bandeja que queda entre la base y el torso. Allí van el Arduino, el driver, los convertidores y el servo que gira el cuello.
<!-- /GERADO -->

Cómo conectar todo lo que aparece en esta lista: [LIGACAO.es.md](LIGACAO.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
