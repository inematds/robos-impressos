# Conexión eléctrica del robot cuadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**No probado en el banco de trabajo.** Este esquema se elaboró a partir de las fichas de los componentes; todavía no se conectó ningún cable en un robot montado.
Verifica cada conexión con el multímetro antes de encender el interruptor. Si tu placa tiene un nombre impreso diferente del
que aparece aquí, usa el nombre de la placa.

![Esquema de conexión del robot cuadrado de mesa: batería, fusible, placa de protección, cargador, interruptor, convertidores, Arduino con Sensor Shield, servos, Raspberry Pi y pantalla](ligacao.es.svg)

Página con el mismo esquema: https://inematds.github.io/robos-impressos/guia/es/cubo/#energia

Toda la soldadura del robot se hace en la mesa de trabajo, en los preparativos 1, 2 y 3. Durante el montaje solo hay bornes y encajes. Los pasos
numerados de los 4 preparativos son los mismos que aparecen en la página.

## Seguridad con baterías de litio

- **Polaridad:** rojo en el positivo, negro en el negativo. Mide con el multímetro antes de cada conexión nueva. Un cable invertido quema la placa de inmediato.
- **Ajuste antes de conectar la carga:** LM2596 a 5,1 V y UBEC a 6 V, medidos con el multímetro, sin el Raspberry Pi, sin el Arduino y sin los servos conectados.
- **Un cortocircuito puede provocar un incendio:** suelda con las celdas FUERA del soporte y aísla cada empalme con tubo termorretráctil. No debe quedar ningún metal expuesto.
- **Fusible:** 3 A, retardado (marcado T3A), en el cable positivo, a pocos centímetros del soporte de las baterías.
- **Celdas iguales:** las dos 18650 deben ser de la misma marca, del mismo modelo y nuevas. Las celdas abolladas, hinchadas o calientes se llevan a un punto de recolección de pilas, no se usan en el robot.
- **Primera carga:** quédate cerca, con el robot sobre una superficie que no se queme.

## Qué alimenta cada componente

- **Pack 2S:** dos celdas 18650 en serie, de 6 V (vacío) a 8,4 V (cargado). Pasa por el fusible y por la placa de protección (BMS).
- **Cargador USB-C:** queda conectado a la salida de la placa de protección, antes del interruptor. El robot se carga apagado, con una fuente USB-C de 15 W o más.
- **Interruptor:** corta el positivo que va a los dos convertidores.
- **LM2596, ajustado a 5,1 V:** la salida va a una barra de conexión en la base. De ella salen el par que alimenta la Raspberry Pi (por el adaptador USB-C con bornes) y el par que alimenta el Arduino (por los pines + y − del conector COM del Sensor Shield).
- **UBEC a 6 V:** alimenta solo los 2 servos, por el borne azul del Sensor Shield, con el jumper SEL retirado.
- **Negativo (GND):** es uno solo para todo el robot.

Por qué el Arduino recibe los 5,1 V del LM2596 y no el voltaje de la batería: la entrada VIN del Arduino Uno requiere de 7 a 12 V
([ficha del Arduino Uno R3](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)) y el pack pasa buena
parte de la descarga por debajo de 7 V.

## La barra de conexión

Es una barra de bornes de tornillo (tipo sindal) que queda suelta en la base. Usas 3 bornes:

- **Borne 1, los 5,1 V:** de un lado, el cable rojo que viene del LM2596. Del otro, el cable rojo que sube a la Raspberry Pi y el jumper que va al pin + del conector COM del shield.
- **Borne 2, el negativo:** de un lado, el cable negro del LM2596 y un extremo del par de resistencias. Del otro, el cable negro que sube a la Raspberry Pi y el jumper que va al pin − del conector COM.
- **Borne 3, la conexión serial:** de un lado, las resistencias del divisor. Del otro, el cable azul que baja de la Raspberry Pi.

## Tabla de conexiones, cable por cable

<!-- GERADO:ligacoes -->
### Batería, protección y carga

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Soporte de las baterías: cable rojo (positivo del pack) | Portafusible de 3 A y, después de este, pad B+ de la placa de protección | rojo | 22 AWG | El fusible queda a pocos centímetros del soporte. |
| Soporte de las baterías: cable negro (negativo del pack) | Pad B− de la placa de protección | negro | 22 AWG |  |
| Soporte de las baterías: lámina de metal que une las 2 celdas (punto medio) | Pad del punto medio de la placa de protección (BM o B1) | amarillo | 22 AWG | Es el 3.er cable. Suéldalo a la lámina con las celdas FUERA del soporte. |
| Pad del punto medio de la placa de protección (BM o B1) | Pad BM del cargador USB-C | amarillo | 22 AWG | Sin este cable, el cargador no equilibra las dos celdas. |
| Pad B+ del cargador USB-C | Salida positiva de la placa de protección (P+; si la placa no tiene P+, es el mismo pad B+) | rojo | 22 AWG | El cargador queda antes del interruptor: el robot se carga apagado. |
| Pad B− del cargador USB-C | Salida negativa de la placa de protección (P−; en la placa de la tienda consultada, el pad C−) | negro | 22 AWG | No conectes al pad B− de la placa de protección: la carga debe pasar por la protección. |

### Interruptor y convertidores

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Salida positiva de la placa de protección (P+ o B+) | Interruptor de encendido/apagado y, después, entrada IN+ del LM2596 y cable rojo de entrada del UBEC | rojo | 22 AWG | El interruptor corta solo el positivo. |
| Salida negativa de la placa de protección (P−; en la placa de la tienda consultada, el pad C−) | Entrada IN− del LM2596 y cable negro de entrada del UBEC | negro | 22 AWG | Este es el negativo común (GND) de todo el robot. |

### 5 V: Raspberry Pi y Arduino

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Salida OUT+ del LM2596 (5,1 V) | Barra de conexión, borne 1 | rojo | 20 AWG, corto | Ajusta los 5,1 V ANTES de conectar cualquier cosa del otro lado de la barra. |
| Salida OUT− del LM2596 | Barra de conexión, borne 2 | negro | 20 AWG, corto |  |
| Barra de conexión, borne 1 (5,1 V) | Por el cuello, hasta el borne + del adaptador USB-C, que se conecta al puerto USB-C del Raspberry Pi | rojo | 20 AWG | Usa el cable más grueso y corto posible: un cable delgado hace que el Pi indique baja tensión. |
| Barra de conexión, borne 2 (negativo) | Por el cuello, hasta el borne − del adaptador USB-C | negro | 20 AWG |  |
| Barra de conexión, borne 1 (5,1 V) | Pin + del conector COM del Sensor Shield | rojo | jumper Dupont con un extremo cortado y pelado | Por aquí recibe energía el Arduino. Antes, con el Uno conectado solo por USB y el jumper SEL retirado, confirma con el multímetro que este pin marca cerca de 5 V y que el pin V del D9 marca 0 V. Un pin incorrecto aquí envía los 6 V de los servos al Raspberry Pi. |
| Barra de conexión, borne 2 (negativo) | Pin − del conector COM del Sensor Shield | negro | jumper Dupont con un extremo cortado y pelado |  |

### 6 V: servos

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Cable rojo de salida del UBEC (6 V) | Borne azul VCC del Sensor Shield | rojo | cable del UBEC, con el conector de 3 pines cortado | Jumper SEL del shield RETIRADO y jumper del UBEC en 6 V. La salida del UBEC viene con un conector de servo: corta el conector y pela los cables. El rojo es el positivo. |
| Cable negro o marrón de salida del UBEC | Borne azul GND del Sensor Shield | negro | cable del UBEC, con el conector de 3 pines cortado | Si el conector tiene un tercer cable, blanco o naranja, aísla su punta con tubo termorretráctil: no se conecta. |
| Capacitor de 1000 µF: pata larga (+) | Borne azul VCC; la pata con la franja (−) va en el borne azul GND | sin cable | patas del capacitor | El capacitor invertido explota. |
| Servo de pan (en la base) | Conector D9 del Sensor Shield | cable del servo | cable de 3 hilos del servo | G = marrón o negro, V = rojo, S = naranja o amarillo. |
| Servo de tilt (en la cabeza) | Por el cuello, con la extensión de 30 cm, hasta el conector D10 del Sensor Shield | cable del servo | cable de 3 hilos del servo | Mismo orden de colores que en D9. |

### Conexión serial entre Raspberry Pi y Arduino

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Raspberry Pi: pin 32 (GPIO12, TX), en el conector inferior 2 × 2 | Por el cuello, hasta el pin S de D0 (RX) del Sensor Shield | verde | jumper de 40 cm: un extremo soldado al conector 2 × 2, el otro con el conector hembra | Directo: los 3,3 V del Pi ya sirven como nivel alto para Arduino. |
| Raspberry Pi: pin 34 (GND), en el conector inferior 2 × 2 | Por el cuello, hasta el pin G de D0 del Sensor Shield | negro | jumper de 40 cm: un extremo soldado al conector 2 × 2, el otro con el conector hembra |  |
| Raspberry Pi: pin 33 (GPIO13, RX), en el conector inferior 2 × 2 | Por el cuello, hasta el borne 3 de la barra de conexión | azul | jumper de 40 cm: un extremo soldado al conector 2 × 2, el otro cortado y pelado | Este cable nunca va directo a D1: son 5 V en un pin de 3,3 V. |
| Barra de conexión, borne 3 | Resistencia de 1 kΩ y, después de ella, pin S de D1 (TX) del Sensor Shield | azul | mitad de un jumper, soldada a la pata de la resistencia, con el conector hembra en el shield | Montado en la mesa de trabajo, en el preparativo 3. |
| Barra de conexión, borne 3 | 2 resistencias de 1 kΩ en serie y, después de ellas, borne 2 de la barra (negativo) | sin cable | patas de los resistores | Los 3 resistores forman el divisor: 5 V se convierten en 3,3 V. |
| Pantalla MPI3501 | Conectada a los pines 1 a 26 de Raspberry Pi | sin cable | conector de la propia pantalla | Usa SPI y los 5 V de los pines 2 y 4. |
<!-- /GERADO -->

## Preparativo 1: suelda la alimentación y ajusta los dos voltajes

Hazlo en la mesa de trabajo, con la base impresa al lado. El interruptor es la primera pieza que se coloca en la base y se instala antes de soldarlo
al resto. Los nombres de los pads de soldadura cambian de una placa a otra. En el cargador son B+, BM y B−. En la placa de protección de la tienda
consultada, solo el reverso tiene nombres: B+, B1 (medio), B− y C−. Según la foto, C− es la salida negativa y la salida positiva es la
propia B+; es una interpretación de la foto, no está confirmada: compruébalo con el multímetro. En el Sensor Shield de la misma tienda, la foto muestra
el conector COM con 4 pines verticales (TX, RX, − y +) y el jumper SEL al lado del borne azul.

<!-- GERADO:prep1 -->
1. Suelda el 3.er cable (amarillo) a la lámina de metal que une las dos celdas, con las celdas fuera del soporte.
2. Suelda 2 cables rojos de 10 cm a los 2 terminales del interruptor. Pasa los extremos libres por el recorte de la base, de afuera hacia adentro, y encaja el interruptor en el recorte. Hazlo ANTES de soldar el interruptor al resto: conectado al mazo de cables, no pasa por el recorte de 13,5 × 9 mm.
3. Con la base al lado como guía para medir el largo de los cables, conecta el soporte, el fusible, la placa de protección y el cargador según la tabla de conexiones. Deja unos 8 cm de holgura en los cables del soporte para que salga por la puerta trasera cuando cambies las celdas.
4. Suelda un extremo del interruptor a la salida positiva de la placa de protección. Suelda el otro a la entrada IN+ del LM2596 y al cable rojo de entrada del UBEC. Los negativos de ambas entradas van a la salida negativa de la placa de protección.
5. En la salida del LM2596, suelda 2 cables cortos de 20 AWG y aprieta los otros extremos en la barra de conexión: el rojo en el borne 1 y el negro en el borne 2. No conectes nada más a las salidas.
6. Pon las celdas en el soporte, verificando el lado positivo, y enciende el interruptor.
7. Con el multímetro conectado a la barra de conexión, gira el tornillo de ajuste del LM2596 con el destornillador hasta que marque 5,1 V. Son varias vueltas.
8. Mide la salida del UBEC: debe marcar 6 V. Si marca 5 V, cambia su jumper a 6 V.
9. Apaga el interruptor.
<!-- /GERADO -->

## Preparativo 2: carga el programa y coloca los 2 servos a 90°

El programa es el sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). Lleva los dos servos
al centro y los mantiene allí.

<!-- GERADO:prep2 -->
1. Abre el sketch `centrar_servos.ino` en Arduino IDE. Conecta el Arduino Uno a la computadora con el cable USB, sin el shield ni la batería.
2. En el menú Herramientas, elige la placa Arduino Uno y el puerto en el que apareció. Haz clic en Cargar.
3. Desconecta el cable USB, coloca el Sensor Shield en el Uno y quita el jumper SEL del shield: es la cubierta de plástico sobre 2 pines, junto al borne azul.
4. Vuelve a conectar el cable USB, solo para medir con el multímetro. El conector COM del shield tiene 4 pines verticales, marcados TX, RX, − y +. Entre el + y el − debe marcar unos 5 V. En el conector D9, entre el pin V y el pin G, debe marcar 0 V.
5. Si el pin V de D9 marca 5 V, el jumper SEL todavía está puesto. Si el + de COM no marca 5 V, tu shield es diferente al de la foto de la tienda: busca otro pin marcado + o 5V que marque 5 V con el SEL retirado. Un pin equivocado aquí lleva los 6 V de los servos a la Raspberry Pi.
6. Desconecta el cable USB.
7. La salida del UBEC viene con un conector de servo de 3 pines: corta el conector y pela los cables. El rojo es el positivo y el negro (o marrón), el negativo. Si hay un tercer cable, blanco o naranja, aísla su punta con tubo termorretráctil. Aprieta el rojo en VCC y el negro en GND de la barra de conexión azul. En el mismo borne va el capacitor de 1000 µF, con la pata larga en VCC.
8. Toma 2 jumpers de 40 cm, corta el conector de un extremo de cada uno y pela los cables. Aprieta uno en el borne 1 de la barra de conexión, del lado opuesto al conversor, y encaja su conector en el pin + del conector COM. El otro va del borne 2 al pin − del mismo conector. Los pines TX y RX de al lado quedan vacíos: los 5 V de uno de ellos llegan al Raspberry Pi por el cable serial.
9. Conecta el servo de pan al D9 y el servo de tilt al D10: cable marrón o negro a G, rojo a V, naranja o amarillo a S.
10. Enciende el interruptor: los dos servos se colocan en el centro (90°) y el LED del Uno parpadea una vez por segundo.
11. Apaga el interruptor. A partir de ahora, no gires los ejes de los servos con la mano.
12. Deshaz las conexiones de prueba para el montaje: quita los 2 servos del D9 y del D10, suelta del borne azul los cables del UBEC y el capacitor, y quita los 2 jumpers del conector COM. Si el shield cubre los orificios de fijación del Uno, retíralo también. Quita las 2 celdas del soporte: solo vuelven a colocarse durante el montaje, en el paso de la batería.
<!-- /GERADO -->

Tres avisos:

- No alimentes el servo MG996R con los 5 V del USB. El puerto USB suministra 0,5 A y el servo necesita más al arrancar.
- Nunca conectes el cable USB de la computadora con la batería encendida: ambas fuentes quedarían en paralelo.
- Carga el sketch antes de atornillar el Uno a la base. Una vez colocado, quedan unos 10 mm entre el conector USB y la pared, y el cable no entra.

El sketch compila para Arduino Uno (arduino-cli, core arduino:avr 1.8.8, biblioteca Servo 1.3.0). Todavía no se ha
probado en un robot montado.

## Preparativo 3: prepara el cable serial y el divisor de resistores

La Raspberry Pi queda en la cabeza y el Arduino en la base. Se comunican por 3 cables que bajan por el cuello: verde, azul
y negro. En este preparativo sueldas estos 3 cables a un conector bajo, que se conecta a los pines de la Pi, y montas el divisor de 3
resistencias en la barra de conexión. Son 6 jumpers de 40 cm en todo el robot: 3 en este cable, 1 cortado por la mitad para el
divisor y 2 que llevan energía al Arduino (preparativo 2). Sobra un kit de 40. El largo queda justo: según el modelo, hay
cerca de 21 cm en línea recta desde los pines de la Pi hasta el shield, más 15 cm de holgura (estimación). Si falta cable, empalma
un tramo de jumper en la punta de la base, con soldadura y tubo termorretráctil, todavía en este preparativo. Haz este preparativo con las
celdas fuera del soporte.

<!-- GERADO:prep3 -->
1. Con el alicate de corte, corta de la barra de pines hembra una pieza de 2 × 2: 2 filas con 2 orificios cada una. Es el conector bajo que va en los pines 31 a 34 del Raspberry Pi.
2. Separa 3 jumpers de 40 cm: uno verde, uno azul y uno negro (o marca 3 de otro color con cinta). Corta el conector de UN extremo de cada uno y pela 3 mm.
3. Ubica los pines de la Raspberry Pi: el pin 1 está en la esquina, del lado de la tarjeta microSD, en la fila interior; el pin 40 está en la esquina opuesta, en la fila exterior. Los impares están en la fila interior y los pares en la fila exterior. Los pines 31 y 32 son el 16.º par; los pines 33 y 34, el 17.º.
4. Suelda los 3 extremos a los terminales del conector 2 × 2, con los cables extendidos hacia un lado: el verde en el orificio que entrará en el pin 32, el azul en el del pin 33 y el negro en el del pin 34. Deja vacío el terminal del pin 31. Coloca un trozo de tubo termorretráctil fino en cada soldadura.
5. Marca con un bolígrafo la esquina del conector donde quedó el terminal vacío, el del pin 31. Al conectarlo, la marca queda en la fila interior, orientada hacia la tarjeta microSD. Para verificarlo: entre el conector y la pantalla quedan 2 pares de pines vacíos (27 a 30) y, del otro lado, 3 pares (35 a 40). Si lo conectas al revés, los cables quedan intercambiados.
6. En el cable azul, corta también el conector del otro extremo y pela 6 mm: ese extremo va en un borne. El verde y el negro se quedan con el conector hembra, que encaja en el shield.
7. Ahora prepara el divisor. Suelda 2 resistencias de 1 kΩ una con otra, pata con pata, y cubre la unión con tubo termorretráctil. Este par equivale a 2 kΩ.
8. Corta un jumper por la mitad. Suelda el extremo cortado de una de las mitades a una pata de la 3.ª resistencia y cúbrelo con tubo termorretráctil. El conector hembra de esta mitad es el que va al D1.
9. En la barra de conexión, del lado del convertidor, aprieta en el borne 3 la pata libre de la 3.ª resistencia junto con un extremo del par de 2 kΩ. Aprieta el otro extremo del par en el borne 2, junto con el cable negro que ya está ahí. Dobla la punta de cada pata antes de apretar para que el tornillo la sujete.
10. Verifica con el multímetro, en ohmios: entre el conector hembra del jumper del D1 y el borne 3, cerca de 1 kΩ; entre el borne 3 y el borne 2, cerca de 2 kΩ.
11. Guarda el cable: el conector 2 × 2 se conecta a la Raspberry Pi durante el montaje, antes de la pantalla. En la base, el azul va al borne 3 de la barra de conexión, el verde al pin S de D0 y el negro al pin G de D0; todo se conecta con bornes o conectores, sin soldar. Atención: en los conectores de 3 pines de D0 y D1, el pin del medio (V) siempre queda vacío. Con el jumper SEL retirado, lleva los 6 V de los servos, y 6 V en un cable serial queman la Raspberry Pi.
<!-- /GERADO -->

Por qué un conector bajo: los pines 31 a 34 quedan debajo de la placa de la pantalla, donde sobran cerca de 17,5 mm (medida no
confirmada). El conector Dupont común, de 14 mm, no cabe en posición vertical.

Dónde está el pin 1 y por qué el número del pin no es el número del GPIO:
[documentación de la Raspberry Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc).
En la Pi ya encendida, el comando `pinout` muestra el mapa de los pines.

## Preparativo 4: graba la tarjeta microSD, instala el controlador de la pantalla y conecta la serial

La tarjeta se graba en tu computadora con un lector de tarjetas microSD. Después te conectas a Raspberry Pi por la red,
mediante SSH: escribes los comandos en tu computadora y se ejecutan en el Pi.

<!-- GERADO:prep4 -->
1. Instala Raspberry Pi Imager, el programa gratuito de Raspberry Pi, en la computadora y coloca la tarjeta en el lector.
2. En Imager, elige el modelo de tu Pi, el sistema Raspberry Pi OS (64-bit) y la tarjeta.
3. Antes de grabar, abre la configuración de Imager: ponle un nombre al Pi (por ejemplo `robo`), crea un usuario y una contraseña, ingresa el nombre y la contraseña de tu Wi-Fi y activa SSH. Graba la imagen.
4. Pon la tarjeta en el Pi, conecta la pantalla a los pines 1 a 26 solo para esta prueba y enciende el Pi con una fuente USB-C de 5 V y 3 A. Espera unos 2 minutos.
5. En la computadora, abre la terminal: en Windows es el programa PowerShell; en Mac y Linux, Terminal.
6. Escribe `ssh usuario@robo.local`, reemplazando `usuario` y `robo` por los nombres que creaste. Responde `yes` la primera vez y escribe la contraseña.
7. Si `robo.local` no responde, abre la página de tu router, busca el Pi en la lista de dispositivos conectados y usa su número (la dirección IP), por ejemplo `ssh usuario@192.168.0.50`.
8. Cuando la terminal muestre el nombre del Pi, ya estás dentro. Escribe los tres comandos del controlador, uno por línea, presionando Enter después de cada uno: `git clone https://github.com/goodtft/LCD-show.git`, luego `cd LCD-show` y después `sudo ./LCD35-show`. El Pi necesita tener conexión a internet. Se reinicia solo y la pantalla se enciende.
9. Vuelve a conectarte por SSH y activa la conexión serial DESPUÉS del script de la pantalla, porque este sobrescribe el archivo de configuración. Escribe `sudo nano /boot/firmware/config.txt`, ve hasta el final del archivo y agrega una línea: `dtoverlay=uart5` en Raspberry Pi 4 o `dtoverlay=uart4-pi5` en Raspberry Pi 5. Guarda con Ctrl+O y Enter, y sal con Ctrl+X.
10. Escribe `sudo poweroff`, espera a que el LED verde del Pi deje de parpadear, desconecta la fuente de alimentación y retira la pantalla: volverá a colocarse durante el montaje.
<!-- /GERADO -->

La pantalla es la MPI3501: 3,5 pulgadas, 480 × 320, controlador ILI9486, conectada por SPI a los pines 1 a 26. Fuentes:
[página de la MPI3501 en lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display) (modelo, pines y controlador) y
documentación de la Raspberry Pi en GitHub: [SSH](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/ssh.adoc) y [cómo encontrar la dirección de la Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/find-your-ip-address.adoc).
No probado en el banco de trabajo: el fabricante enumera pruebas hasta la Raspberry Pi 3B+, y el script reemplaza el archivo de configuración de la Pi.

La línea serial viene de la [lista de overlays del firmware de Raspberry Pi](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
Después de reiniciar, el nombre del puerto aparece con `ls /dev/ttyAMA*`. El programa que usa esta serial es de la fase 2.

Plan B, tampoco probado, si la pantalla queda blanca o apagada:

- En lugar del script, agrega la línea `dtoverlay=piscreen,drm` al final del archivo `/boot/firmware/config.txt` y reinicia. Es el overlay oficial para una pantalla de 3,5 pulgadas con el mismo controlador ILI9486 ([lista de overlays](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README)); la fuente no garantiza que funcione con MPI3501.
- Si aun así no se enciende, vuelve a grabar la tarjeta con Raspberry Pi OS (Legacy) y repite el script del fabricante.

## Cómo se comunica la Raspberry Pi con el Arduino

El agujero para cables del cuello tiene 9 mm y un conector USB no pasa por ahí. Por eso se comunican mediante una serial
(UART) de 3 cables sueltos.

- **En el Arduino:** pines D0 (RX) y D1 (TX), que son el puerto serie real de la placa. No interfieren con la señal de los servos.
- **En la Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX) y pin 34 (GND). La pantalla ocupa los pines 1 a 26; estos tres quedan libres.
- **Número del pin y número del GPIO:** "pin 32" es la posición en la fila de 40 pines, contada desde la esquina de la tarjeta microSD. "GPIO12" es el nombre de la señal que sale por ese pin. Los dos números no son iguales.
- **Voltaje:** el Arduino funciona a 5 V y la Pi a 3,3 V. El cable que va del Arduino a la Pi pasa por un divisor de 3 resistencias de 1 kΩ, que baja de 5 V a 3,3 V. El cable que va de la Pi al Arduino es directo.
- **Por qué usar resistencias y no un módulo convertidor de nivel:** el divisor funciona con 3 resistencias sujetas a la barra de conexión, sin otra placa suelta en la base. El módulo también serviría, pero requiere un pin de 3,3 V: en la foto del shield se ve la marca 3V3, pero no se puede confirmar si hay un pin vertical allí.

## Los 8 cables que pasan por el cuello

Son 8 cables: 2 de alimentación (5,1 V de Raspberry Pi, 20 AWG), 3 de la conexión serial y los 3 del cable del servo de tilt. Deben
conectarse dentro de la cabeza ANTES del copo, porque después Raspberry Pi queda encerrado. Tampoco pueden quedar colgando por
debajo de la horquilla en ese momento, porque la parte inferior del copo pasa por debajo de ella. Este es el orden:

1. Al montar la Raspberry Pi, antes de la pantalla, conecta el conector bajo del cable serial a los pines 31 a 34.
2. Con la cabeza todavía abierta (marco, pantalla, servo de tilt y horquilla en su lugar), atornilla los 2 cables de 5,1 V al adaptador USB-C y conéctalo a la Raspberry Pi.
3. Conecta la extensión de 30 cm al cable del servo de tilt.
4. Baja los 8 cables por el agujero de 9 mm de la horquilla, de arriba hacia abajo. Primero, el conector de la extensión, que tiene 7,6 mm de ancho y pasa justo.
5. Detente cuando las puntas queden al ras de la cara inferior de la horquilla. Deja unos 5 cm de cable sobrante dentro de la cabeza: se inclina alrededor de la horquilla.
6. Cierra la cabeza con la carcasa. Con las pinzas, saca las puntas de los 8 cables por la ranura del fondo de la carcasa.
7. Pasa los cables por el tubo del cuello y coloca la cabeza sobre él.
8. En la base, con el interruptor apagado y sin soldar: los 2 cables de 5,1 V a los bornes 1 y 2 de la barra de conexión; el cable azul al borne 3; el conector del verde al pin S de D0 y el del negro al pin G de D0; el jumper del divisor al pin S de D1; la extensión del servo a D10.

Deja unos 10 cm de holgura dentro de la base: el cuello gira casi una vuelta y tuerce los cables. Este paso nunca se ha
ensayado con las piezas impresas.

## Corriente, cable y fusible

Los valores de abajo se calculan a partir de las fichas técnicas; no se midieron.

- Uso normal: cerca de 2 A desde el pack. El Raspberry Pi consume cerca de 1 A a 5,1 V y los servos menos de 1 A a 6 V.
- Pico: cerca de 5 A, con el LM2596 a 2 A, el UBEC en el límite de 3 A y el pack a 6,5 V.
- Interruptor KCD11-101: 3 A a 250 V~ y 6 A a 125 V~ ([ficha de la tienda](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). La ficha no indica el valor para corriente continua.
- Fusible de 3 A: es el valor más bajo del interruptor. El uso normal queda por debajo, y una sobrecarga sostenida abre el fusible antes de que se caliente el interruptor.
- Fusible retardado (marcado T3A o T3,15A): el arranque de los servos y la carga del capacitor de 1000 µF generan picos de una fracción de segundo. Un fusible rápido puede abrirse con esos picos aunque no haya una falla; el retardado soporta el pico corto y se abre ante una sobrecarga sostenida (comportamiento habitual de este tipo de fusible, medida no confirmada).
- Si el fusible se abre con el robot en uso normal, no pongas uno de mayor capacidad: mide la corriente y busca qué está haciendo esfuerzo.
- Cable 22 AWG (0,33 mm²) para la energía de la base. Cable 20 AWG (0,5 mm²) para el par de 5,1 V que sube hasta el Raspberry Pi: con 2 A, la caída calculada en ese tramo es de 0,06 V.
- El LM2596 soporta cerca de 2 A continuos sin disipador (valor habitual, medida no confirmada). Usa el Raspberry Pi 4, o el Pi 5 sin accesorios USB.
- Si el Raspberry Pi indica subtensión, acorta el par de 5,1 V y comprueba el ajuste. Para ver el dato, escribe `vcgencmd get_throttled` en el Pi: la respuesta correcta es `throttled=0x0`.
- El programa de la fase 2 no debe hacer que los dos servos hagan fuerza al mismo tiempo al final del recorrido.

## Calor dentro de la cabeza

El Raspberry Pi 4 queda encerrado en la cabeza, que es de PLA y no tiene aberturas de ventilación. Es un riesgo que no se ha medido.

- El PLA se ablanda cerca de 60 °C (valor habitual, medida no confirmada).
- El Pi reduce la velocidad cuando el procesador alcanza entre 80 y 85 °C ([documentación de Raspberry Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)).
- Pega los disipadores adhesivos a los chips del Pi antes de montarlo.
- Con el robot encendido durante media hora, escribe `vcgencmd measure_temp` en el Pi. Si supera los 70 °C, imprime la carcasa de la cabeza en PETG o abre agujeros de ventilación en la pared trasera.

## La primera vez que enciendes el robot montado

1. Interruptor apagado. Con el multímetro en continuidad, comprueba que el positivo y el negativo del pack no estén en cortocircuito.
2. Antes de apretar en la barra los 2 cables que bajan de la Raspberry Pi, enciende el interruptor y mide en la barra de conexión, del lado del convertidor: 5,1 V entre los bornes 1 y 2, con la punta roja en el positivo. Mide 6 V en el borne azul. Apaga.
3. Aprieta los cables de la Pi en la barra, rojo en el borne 1 y negro en el borne 2, y vuelve a encender el interruptor.
4. El LED del Arduino parpadea, los dos servos mantienen el centro, el LED de encendido de la Raspberry Pi se ilumina y, en aproximadamente 1 minuto, la pantalla muestra el sistema.
5. Si no se enciende nada, apaga y revisa el fusible.

## Lo que todavía no se probó

<!-- GERADO:riscos -->
- Todavía no se imprimió ni se montó nada. La parte eléctrica de esta página no se probó en el banco de trabajo: se preparó a partir de las fichas de los componentes.
- Los archivos 3MF de las camas nunca se abrieron en Bambu Studio. Si alguno no abre, usa los STL.
- El enchufe USB-C que alimenta la Raspberry Pi no está en el modelo 3D. Puede que no haya espacio para él junto a la Pi, dentro de la cabeza.
- Los pines 31 a 34 de la Raspberry Pi quedan debajo de la placa de la pantalla. El espacio libre allí (17,5 mm en el modelo) es una medida sin confirmar: si el conector bajo no cabe, habrá que soldar los 3 cables de la serial.
- El cupón de prueba no verifica la ventana del servo MG996R ni la rosca del tornillo M5. Comprueba la ventana del servo en el marco de la cabeza (mesa 01). La rosca para el M5 está en el brazo de la horquilla (mesa 03). Ambas se revisan antes de las impresiones largas.
- Con el Arduino atornillado a la base, el cable USB no entra: quedan unos 10 mm hasta la pared. Para volver a grabar el programa, hay que quitarle los 4 tornillos.
- El portafusibles, la barra de conexión y las 3 resistencias de la conexión serial no tienen un espacio modelado: quedan sueltos entre los cables, aislados con tubo termorretráctil.
- Las medidas marcadas como NC provienen de anuncios de tiendas. Mide tu pieza antes de imprimir la parte que hace contacto con ella.
- Nunca se probó el paso de los 8 cables por el agujero de la horquilla y la ranura de la parte inferior de la cabeza con las piezas impresas.
- Calor: Raspberry Pi 4 queda encerrado en la cabeza, que es de PLA y no tiene abertura de ventilación. El PLA se ablanda cerca de los 60 °C y el Pi reduce la velocidad a partir de los 80 °C. Pega los disipadores y mide con el comando `vcgencmd measure_temp`. Si supera los 70 °C, imprime la carcasa de la cabeza en PETG o abre orificios de ventilación atrás.
<!-- /GERADO -->

## Glosario

<!-- GERADO:glossario -->
- **GPIO:** La fila de 40 pines de Raspberry Pi, donde se conectan la pantalla y los cables de señal. En esta guía, «pin 32» es la posición del pin en la fila; «GPIO12» es el nombre de la señal que sale por él.
- **UBEC:** Convertidor pequeño, usado en aeromodelos, que reduce el voltaje de la batería a un valor fijo. Aquí, 6 V para los servos.
- **BMS:** Placa de protección de la batería de litio. Desconecta la batería antes de que se descargue demasiado, se sobrecargue o entre en cortocircuito.
- **2S:** Dos celdas de litio conectadas en serie, una después de la otra. Los voltajes se suman: de 6 V (vacía) a 8,4 V (cargada).
- **Horn:** La pieza de plástico que encaja en el eje del servo y gira con él. Este robot usa el horn redondo, en forma de disco.
- **Inserto en caliente:** Buje de latón con rosca interna. Se introduce en el orificio del plástico con el cautín y se convierte en una rosca metálica.
- **NC:** No confirmado: una medida tomada de un anuncio de una tienda que aún no se ha verificado con la pieza en mano.
- **Laminador:** El programa que convierte el archivo 3D en las capas que imprime la impresora. El de Bambu Lab se llama Bambu Studio.
- **SSH:** Forma de usar el Raspberry Pi por la red: escribes los comandos en la terminal de tu computadora y se ejecutan en el Pi, sin conectarle teclado ni monitor.
- **SPI:** Conexión de datos con pocos cables y un reloj que marca el ritmo. Por ella, el Raspberry Pi envía la imagen a la pantalla.
- **UART (serial):** Conexión de datos sencilla: un cable para hablar (TX) y otro para escuchar (RX). Por ella, el Raspberry Pi envía órdenes al Arduino.
- **Jumper SEL:** Cubierta de plástico sobre 2 pines del Sensor Shield, junto al borne azul, con la marca SEL. Colocada, conecta los 5 V del Arduino a los conectores de los servos. Retirada, los servos reciben solo lo que entra por el borne azul.
- **Borne:** Conector de tornillo: el cable entra por el orificio y se aprieta con el tornillo. En el Sensor Shield es el bloque azul marcado GND y VCC.
- **Sketch:** El nombre que Arduino le da a un programa. Abres el archivo en Arduino IDE y lo grabas en la placa con el cable USB.
- **Shield:** Placa que se conecta encima de Arduino, en sus pines, y agrega conectores. Aquí, el Sensor Shield proporciona los conectores de los servos.
- **AWG:** Medida del grosor del cable. Cuanto menor es el número, más grueso es: el de 20 AWG es más grueso que el de 22 AWG.
- **GND:** El negativo del circuito, también llamado tierra. Todos los negativos del robot están conectados entre sí.
- **Dupont:** Cable delgado que ya viene con un conector de encaje en cada extremo, del tamaño de los pines de las placas. También se llama jumper.
- **Step-down:** Convertidor que reduce el voltaje. Aquí, el LM2596 reduce el voltaje de la batería a 5,1 V.
- **Tubo termorretráctil:** Tubito de plástico que se encoge con el calor. Lo colocas sobre la unión soldada y lo calientas: se ajusta y aísla.
<!-- /GERADO -->

Qué comprar: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
