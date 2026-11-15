# Conexión eléctrica del robot cuadrado con ruedas

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**No probado en el banco de trabajo.** Este esquema se elaboró a partir de las fichas de los componentes; todavía no se conectó ningún cable en un robot montado.
Verifica cada conexión con el multímetro antes de encender el interruptor. Si tu placa tiene un nombre impreso diferente del
que aparece aquí, usa el nombre de la placa.

![Esquema de conexión del robot cuadrado con ruedas, en dos dibujos. Energía: baterías, fusible, placa de protección, cargador, interruptor, barra de conexión, convertidores y driver. Señales: Arduino con Sensor Shield, driver, motores con encoder, servos y Raspberry Pi](ligacao.es.svg)

Página del robot: https://inematds.github.io/robos-impressos/guia/es/cubo-rodas/

Toda la soldadura del robot se hace en la mesa de trabajo, durante los preparativos 1, 2 y 3. En el montaje solo hay bornes y conectores.

## Seguridad con baterías de litio

- **Polaridad:** rojo al positivo, negro al negativo. Mide con el multímetro antes de cada conexión nueva. Un cable invertido quema la placa de inmediato.
- **Ajuste antes de conectar la carga:** XL4015 a 5,1 V y UBEC a 6 V, medidos con el multímetro, sin el Raspberry Pi, el Arduino ni los servos conectados.
- **Un cortocircuito provoca un incendio:** suelda con las celdas FUERA del soporte y aísla cada unión entre celdas con tubo termorretráctil. No debe quedar metal expuesto. Un pack de 3 celdas en cortocircuito libera mucha más energía que una pila común.
- **Fusible:** 3 A, de acción retardada (marcado T3A), en el cable positivo, a pocos centímetros del soporte de las baterías.
- **Celdas iguales:** las tres 18650 deben ser de la misma marca y modelo, y nuevas. Las celdas abolladas, hinchadas o calientes van al punto de recolección de pilas, no al robot.
- **Primera carga:** quédate cerca, con el robot sobre una superficie que no se queme.

## Qué alimenta cada componente

- **Pack 3S:** tres celdas 18650 en serie, de 9 V (descargado) a 12,6 V (cargado). Pasa por el fusible y la placa de protección (BMS).
- **Cargador USB-C:** se conecta a la salida de la placa de protección, antes del interruptor. El robot se carga apagado, con una fuente USB-C de 15 W o más. Hay que prepararlo para 3 celdas (preparativo 1).
- **Interruptor:** corta el positivo que va a los dos convertidores y al driver.
- **XL4015, ajustado a 5,1 V:** la salida va a la barra de conexión, en el deck. De ahí salen el par que alimenta el Raspberry Pi (por los pines 2, 4, 6 y 9), el par que alimenta el Arduino (por los pines + y − del conector COM del Sensor Shield) y el cable de 5 V del driver y los encoders.
- **UBEC a 6 V:** alimenta solo los 2 servos, por el borne azul del Sensor Shield, con el jumper SEL retirado.
- **Driver L298N:** recibe el voltaje del pack y lo entrega a los 2 motores. Pierde unos 2 V en el recorrido.
- **Negativo (GND):** es uno solo para todo el robot.

Por qué el Arduino recibe los 5,1 V del convertidor y no el voltaje de la batería: la entrada VIN del Arduino Uno requiere de 7 a 12 V
([ficha del Arduino Uno R3](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)) y el pack cargado supera
los 12 V.

Por qué el Raspberry Pi recibe energía por los pines y no por la entrada USB-C: la entrada USB-C está en el borde inferior de la placa, donde quedan unos 22 mm hasta el fondo de la cabeza (medida del modelo, no confirmada), y un conector recto no cabe ahí. Los pines 2 y 4 aceptan una entrada de 5 V
([documentación de Raspberry Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc)).
Por esos pines, la energía no pasa por la protección de la entrada USB-C: mide los 5,1 V antes de conectarlos. Si prefieres la entrada USB-C, usa un adaptador USB-C con bornes en ángulo y comprueba el espacio.

## La barra de conexión

Es una barra de conexión con bornes de tornillo (tipo sindal) que queda suelta en el deck. Usas 5 bornes, numerados del 1 al 5:

- **Borne 1, los 5,1 V:** de un lado, el cable rojo que viene del XL4015. Del otro, el cable rojo que sube al Raspberry Pi, el jumper que va al pin + del conector COM del shield y el cable que va al borne +5V del driver.
- **Borne 2, el negativo:** de un lado, el cable negro del XL4015 y un extremo del par de resistencias. Del otro, el cable negro que sube al Raspberry Pi y el jumper que va al pin − del conector COM.
- **Borne 3, la conexión serial:** de un lado, las resistencias del divisor. Del otro, el cable azul que baja del Raspberry Pi.
- **Borne 4, el positivo del pack:** de un lado, el cable rojo que sube del interruptor. Del otro, la entrada del XL4015, la entrada del UBEC y el borne +12V del driver.
- **Borne 5, el negativo del pack:** de un lado, el cable negro que sube de la placa de protección. Del otro, el negativo del XL4015, del UBEC y del driver.

Los bornes 4 y 5 permiten separar el deck de la base sin desoldar nada: los 2 cables que suben desde la base pasan por una ranura del deck y se fijan en la barra.

## Tabla de conexiones, cable por cable

<!-- GERADO:ligacoes -->
### Batería, protección y carga

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Soporte de las baterías: cable rojo (positivo del pack) | Portafusibles de 3 A y, después, pad del positivo de las celdas en la placa de protección (B+ o 12,6V) | rojo | 22 AWG | El fusible queda a pocos centímetros del soporte. |
| Soporte de las baterías: cable negro (negativo del pack) | Pad del negativo de las celdas en la placa de protección (B− o 0V) | negro | 22 AWG |  |
| Soporte de las baterías: lengüeta de la unión superior (la del lado del cable rojo) | Pad de la unión superior en la placa de protección (por lo general 8,4V) | amarillo, marcado con cinta | 22 AWG | Desde el cable negro del soporte hasta este cable, el multímetro marca cerca de 8 V. Suelda en la lengüeta con las celdas FUERA del soporte. |
| Soporte de las baterías: lengüeta de la unión inferior (la del lado del cable negro) | Pad de la unión inferior en la placa de protección (por lo general 4,2V) | amarillo | 22 AWG | Desde el cable negro del soporte hasta este cable, el multímetro marca cerca de 4 V. |
| Lengüeta de la unión superior (un segundo cable en la misma lengüeta) | Cargador USB-C: el pad del medio que está más cerca de B+ | amarillo, marcado con cinta | 22 AWG | Sin los 2 cables de las uniones, el cargador no equilibra las tres celdas. |
| Lengüeta de la unión inferior (un segundo cable en la misma lengüeta) | Cargador USB-C: el pad del medio que está más cerca de B− | amarillo | 22 AWG | El orden de los 2 pads del medio se basa en la imagen de la tienda; los nombres impresos no se alcanzan a leer en la foto. |
| Pad B+ del cargador USB-C | Salida positiva de la placa de protección (P+) | rojo | 22 AWG | El cargador queda antes del interruptor: el robot se carga apagado. |
| Pad B− del cargador USB-C | Salida negativa de la placa de protección (P−) | negro | 22 AWG | No conectes al pad del negativo de las celdas: la carga debe pasar por la protección. |

### Interruptor y distribución del pack

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Salida positiva de la placa de protección (P+) | Interruptor de encendido/apagado y, después, borne 4 de la barra de conexión | rojo | 20 AWG | El interruptor corta solo el positivo. Este cable sube desde la base hasta el deck por la ranura trasera. |
| Salida negativa de la placa de protección (P−) | Borne 5 de la barra de conexión | negro | 20 AWG | Este es el negativo común (GND) de todo el robot. |
| Barra de conexión, borne 4 (positivo del pack, de 9 a 12,6 V) | Entrada IN+ del XL4015, cable rojo de entrada del UBEC y borne +12V del driver L298N | rojo | 20 AWG | Son 3 cables en el mismo borne. |
| Barra de conexión, borne 5 (negativo del pack) | Entrada IN− del XL4015, cable negro de entrada del UBEC y borne GND del driver L298N | negro | 20 AWG |  |

### 5,1 V: Raspberry Pi, Arduino, driver y encoders

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Salida OUT+ del XL4015 (5,1 V) | Barra de conexión, borne 1 | rojo | 20 AWG, corto | Ajusta los 5,1 V ANTES de conectar cualquier cosa del otro lado de la barra. |
| Salida OUT− del XL4015 | Barra de conexión, borne 2 | negro | 20 AWG, corto |  |
| Barra de conexión, borne 1 (5,1 V) | Por el cuello, hasta los pines 2 y 4 de la Raspberry Pi | rojo | 20 AWG, con 2 mitades de jumper soldadas en la punta | Los pines 2 y 4 son la entrada de 5 V de la Pi. Por ellos, la energía no pasa por la protección de la entrada USB-C: mide los 5,1 V y la polaridad en la barra antes de conectar. |
| Barra de conexión, borne 2 (negativo) | Por el cuello, hasta los pines 6 y 9 de Raspberry Pi | negro | 20 AWG, con 2 mitades de jumper soldadas en la punta |  |
| Barra de conexión, borne 1 (5,1 V) | Pin + del conector COM del Sensor Shield | rojo | jumper Dupont con un extremo cortado y pelado | Por aquí recibe energía el Arduino. Antes, con el Uno conectado solo por USB y el jumper SEL retirado, confirma con el multímetro que este pin marca cerca de 5 V y que el pin V del D9 marca 0 V. Un pin incorrecto aquí envía los 6 V de los servos al Raspberry Pi. |
| Barra de conexión, borne 2 (negativo) | Pin − del conector COM del Sensor Shield | negro | jumper Dupont con un extremo cortado y pelado |  |
| Barra de conexión, borne 1 (5,1 V) | Borne +5V del driver L298N | rojo | 22 AWG | Solo con el jumper del regulador de 5 V del driver RETIRADO. Si está puesto, el regulador del driver y el XL4015 quedan conectados uno contra el otro. |
| Cable azul del cable de cada motor (alimentación del encoder) | Borne +5V del driver L298N, junto con el cable que viene del borne 1 | azul | cable de 6 hilos del motor | El encoder acepta de 3,3 a 5 V. Nunca conectes este cable a la tensión del motor ni al pin V del shield, que tiene 6 V. |
| Cable negro del cable de cada motor (negativo del encoder) | Borne GND del driver L298N | negro | cable de 6 hilos del motor |  |

### 6 V: servos

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Cable rojo de salida del UBEC (6 V) | Borne azul VCC del Sensor Shield | rojo | cable del UBEC, con el conector de 3 pines cortado | Jumper SEL del shield RETIRADO y jumper del UBEC en 6 V. La salida del UBEC viene con un conector de servo: corta el conector y pela los cables. El rojo es el positivo. |
| Cable negro o marrón de salida del UBEC | Borne azul GND del Sensor Shield | negro | cable del UBEC, con el conector de 3 pines cortado | Si el conector tiene un tercer cable, blanco o naranja, aísla su punta con tubo termorretráctil: no se conecta. |
| Capacitor de 1000 µF: pata larga (+) | Borne azul VCC; la pata con la franja (−) va en el borne azul GND | sin cable | patas del capacitor | El capacitor invertido explota. |
| Servo de pan (en el deck) | Conector D9 del Sensor Shield | cable del servo | cable de 3 hilos del servo | G = marrón o negro, V = rojo, S = naranja o amarillo. |
| Servo de tilt (en la cabeza) | Por el cuello, con la extensión de 30 cm, hasta el conector D10 del Sensor Shield | cable del servo | cable de 3 hilos del servo | Mismo orden de colores que en D9. |

### Motores y encoders

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Motor derecho: cables rojo y blanco | Bornes OUT1 y OUT2 del driver L298N | rojo y blanco | cable de 6 hilos del motor | Si la rueda gira al revés cuando el programa de la fase 2 indique avanzar, cambia de lugar estos 2 cables. |
| Motor izquierdo: cables rojo y blanco | Bornes OUT3 y OUT4 del driver L298N | rojo y blanco | cable de 6 hilos del motor |  |
| Driver L298N: pin ENA | Pin S del D5 del Sensor Shield | cualquiera, marcado ENA | jumper Dupont de 40 cm, entero | Con el jumper ENA retirado. El cable va en el pin de entrada, no en el pin de 5 V que está a su lado (preparativo 3). D5 y D6 controlan la velocidad. |
| Driver L298N: pines IN1 e IN2 | Pin S del D4 (IN1) y pin S del D7 (IN2) | cualquiera, marcados | jumper Dupont de 40 cm, entero | Sentido del motor derecho. |
| Driver L298N: pines IN3 e IN4 | Pin S del D8 (IN3) y pin S del D12 (IN4) | cualquiera, marcados | jumper Dupont de 40 cm, entero | Sentido del motor izquierdo. |
| Driver L298N: pin ENB | Pin S del D6 del Sensor Shield | cualquiera, marcado ENB | jumper Dupont de 40 cm, entero | Con el jumper ENB retirado; aplica la misma precaución que con ENA. |
| Encoder derecho: cable amarillo | Pin S del D2 del Sensor Shield | amarillo | mitad de jumper soldada al cable | La ficha del motor no indica cuál de los 2 cables, amarillo o verde, es el canal A. Si el conteo sale al revés, puedes corregirlo en el programa. |
| Encoder derecho: cable verde | Pin S del conector A0 del Sensor Shield | verde | mitad de jumper soldada al cable | Los conectores A0 y A1 están en la fila ANALOG IN del shield; comprueba que tu placa tenga los pines verticales ahí. |
| Encoder izquierdo: cable amarillo | Pin S del D3 del Sensor Shield | amarillo | mitad de jumper soldada al cable |  |
| Encoder izquierdo: cable verde | Pin S del conector A1 del Sensor Shield | verde | mitad de jumper soldada al cable |  |

### Conexión serial entre Raspberry Pi y Arduino

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Raspberry Pi: pin 32 (GPIO12, TX) | Por el cuello, hasta el pin S de D0 (RX) del Sensor Shield | verde | jumper Dupont de 40 cm, entero | Directo: los 3,3 V del Pi ya sirven como nivel alto para Arduino. |
| Raspberry Pi: pin 34 (GND) | Por el cuello, hasta el pin G de D0 del Sensor Shield | negro | jumper Dupont de 40 cm, entero |  |
| Raspberry Pi: pin 33 (GPIO13, RX) | Por el cuello, hasta el borne 3 de la barra de conexión | azul | jumper de 40 cm con una punta cortada y pelada | Este cable nunca va directo a D1: son 5 V en un pin de 3,3 V. |
| Barra de conexión, borne 3 | Resistencia de 1 kΩ y, después de ella, pin S de D1 (TX) del Sensor Shield | azul | mitad de un jumper, soldada a la pata de la resistencia, con el conector hembra en el shield | Montado en la mesa de trabajo, en el preparativo 3. |
| Barra de conexión, borne 3 | 2 resistencias de 1 kΩ en serie y, después de ellas, borne 2 de la barra (negativo) | sin cable | patas de los resistores | Los 3 resistores forman el divisor: 5 V se convierten en 3,3 V. |
| Pantalla de 5 pulgadas | Raspberry Pi: salida micro-HDMI (la más cercana a la entrada USB-C) y un puerto USB | sin cable | cable HDMI flat corto y cable USB corto | La pantalla no usa los pines del Pi. Los 2 cables quedan dentro de la cabeza y no están en el modelo 3D. |
<!-- /GERADO -->

## Preparativo 1: suelda la alimentación y ajusta los dos voltajes

Hazlo en la mesa de trabajo, con la base y el deck impresos uno al lado del otro. El interruptor es la primera pieza que se coloca en la base, antes de soldarla al resto. Los nombres de los pads de soldadura cambian de una placa a otra, y no se leyeron los de las placas de este robot: la página de la tienda de la placa de protección para 3 celdas no muestra los nombres, y en la foto del cargador no se alcanzan a leer los 2 pads de soldadura del medio. Por eso esta guía nombra las conexiones por lo que son (positivo, negativo, unión superior, unión inferior) y te indica que compruebes cada una con el multímetro.

El cargador viene preparado para 2 celdas. La página de la tienda muestra en una figura qué cambia para 3 celdas: se retira una resistencia y se cierra con soldadura un jumper, junto a la marca ROV
([página del cargador](https://www.usinainfo.com.br/fonte-de-alimentacao/carregador-de-baterias-18650-litio-2s3s-com-balanceamento-usb-c-lx-usc-v2-8996.html)).
Es una soldadura muy pequeña. Plan B, sin modificar el cargador: saca las 3 celdas por la tapa de la batería y cárgalas en un cargador común para 18650.

<!-- GERADO:prep1 -->
1. Con las 3 celdas fuera del soporte, suelda 2 cables amarillos de 20 cm a cada una de las 2 láminas de metal que unen las celdas: son las 2 uniones del pack, y de cada una sale un cable hacia la placa de protección y otro hacia el cargador. Marca con cinta los 2 cables de la unión que está del lado del cable rojo del soporte: es la unión superior.
2. Prepara el cargador para 3 celdas siguiendo la figura de la página de la tienda: retira la resistencia diminuta indicada y cierra con una gota de soldadura el jumper junto a la marca ROV. Sin esto, solo carga hasta 8,4 V. Si no tienes experiencia con soldaduras tan pequeñas, no uses este cargador: saca las 3 celdas por la tapa de la batería y cárgalas en un cargador común para 18650.
3. Suelda 2 cables rojos de 20 AWG y 15 cm a los 2 terminales del interruptor. Pasa los extremos libres por el recorte trasero de la base, de afuera hacia adentro, y encaja el interruptor en el recorte. Hazlo ANTES de soldar el interruptor al resto: conectado al mazo de cables, no pasa por el recorte de 13,5 × 9 mm.
4. Con la base al lado como guía para el largo de los cables, conecta el soporte, el fusible, la placa de protección y el cargador según la tabla de conexiones. Deja unos 15 cm de holgura en los 4 cables del soporte: baja junto con la tapa de la batería cuando llegue el momento de cambiar las celdas.
5. Suelda un extremo del interruptor a la salida positiva de la placa de protección (P+). Pela 6 mm del otro extremo: va al borne 4. Suelda un cable negro de 20 AWG y 20 cm a la salida negativa (P−), y pela el extremo libre: va al borne 5.
6. Ahora el deck, todavía fuera del robot. Corta un tramo de la barra de conexión con 5 bornes y numéralos del 1 al 5. Suelda 2 cables cortos de 20 AWG a la entrada del XL4015 y aprieta los otros extremos en la barra: el de IN+ en el borne 4 y el de IN− en el borne 5. El cable rojo de entrada del UBEC va junto con el borne 4 y el negro con el borne 5.
7. Retira del driver L298N los 3 jumpers (las tapas de plástico): los 2 marcados ENA y ENB y el del regulador de 5 V, junto al borne de alimentación. Después, del mismo lado de la barra, aprieta un cable rojo de 20 AWG desde el borne 4 hasta el borne +12V del driver y uno negro desde el borne 5 hasta el borne GND del driver.
8. En la salida del XL4015, suelda 2 cables cortos de 20 AWG y aprieta los otros extremos en la barra: el de OUT+ en el borne 1 y el de OUT− en el borne 2. No conectes nada más a las salidas.
9. Pon la base y el deck uno al lado del otro. Del otro lado de la barra, conecta en el borne 4 el cable rojo que viene del interruptor y, en el borne 5, el cable negro que viene de la placa de protección.
10. Pon las 3 celdas en el soporte y comprueba el lado positivo. Con el multímetro, mide desde el cable negro del soporte hasta cada cable amarillo: cerca de 4 V en la unión inferior y cerca de 8 V en la unión superior (la marcada con cinta). Enciende el interruptor.
11. Mide entre los bornes 4 y 5: debe dar de 9 a 12,6 V, con el rojo en el positivo.
12. Con el multímetro en los bornes 1 y 2, gira el tornillo de ajuste del XL4015 con el destornillador hasta que marque 5,1 V. Son varias vueltas.
13. Mide la salida del UBEC: debe marcar 6 V. Si marca 5 V, cambia su jumper a 6 V.
14. Apaga el interruptor.
<!-- /GERADO -->

## Preparativo 2: carga el programa y coloca los 2 servos a 90°

El programa es el sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). Lleva los dos servos al centro,
los mantiene ahí y deja apagados los motores de las ruedas.

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
10. Enciende el interruptor: los dos servos irán al centro (90°) y el LED del Uno parpadeará una vez por segundo. El driver de los motores todavía no está conectado al Arduino: las ruedas no se mueven.
11. Apaga el interruptor. A partir de ahora, no gires los ejes de los servos con la mano.
12. Deshaz las conexiones de prueba para el montaje: desconecta los 2 servos de D9 y D10, suelta del borne azul los cables del UBEC y el capacitor, y quita los 2 jumpers del conector COM. Suelta de los bornes 4 y 5 los 2 cables que vienen de la base: volverán a conectarse durante el montaje, después de pasar por la ranura del deck. Si el shield cubre los agujeros de fijación del Uno, desconéctalo también. Saca las 3 celdas del soporte: solo volverán durante el montaje, en el paso de la batería.
<!-- /GERADO -->

Tres avisos:

- No alimentes el servo MG996R con los 5 V del USB. El puerto USB entrega 0,5 A y el servo pide más al arrancar.
- Nunca conectes el cable USB de la computadora con la batería conectada: las dos fuentes quedarían en paralelo.
- Carga el sketch antes de cerrar el robot. Después, para acceder al USB del Arduino, hay que soltar los 4 tornillos de abajo y levantar el torso.

El sketch compila para Arduino Uno (arduino-cli, core arduino:avr 1.8.8, biblioteca Servo 1.3.0). Todavía no se ha
probado en un robot montado.

## Preparativo 3: haz los cables de la conexión serial, del Raspberry Pi, del driver y de los encoders

El Raspberry Pi va en la cabeza y el Arduino en el deck. Se comunican por 3 cables que bajan por el cuello: verde, azul
y negro. Por el mismo cuello sube el par de cables que alimenta el Pi. En el deck, el Arduino controla el driver con 6 cables y lee
los 2 encoders con 4. Hay 16 jumpers de 40 cm en todo el robot; sobra un kit de 40. Haz este preparativo con las celdas
fuera del soporte.

<!-- GERADO:prep3 -->
1. Serial. Separa 3 jumpers de 40 cm: uno verde, uno azul y uno negro (o marca 3 de otro color con cinta). El verde y el negro quedan enteros, con sus 2 conectores hembra. En el azul, corta el conector de UN extremo y pela 6 mm: ese extremo va a un borne.
2. Ubica los pines del Raspberry Pi: el pin 1 está en la esquina, del lado de la tarjeta microSD, en la fila interior; el pin 40 está en la esquina opuesta, en la fila del borde. Los impares están en la fila interior y los pares en la fila del borde. Los pines 2, 4 y 6 son los 3 primeros de la fila del borde; el pin 9 es el 5.º de la fila interior. Los pines 32 y 34 son el 16.º y el 17.º de la fila del borde; el pin 33 es el 17.º de la fila interior.
3. Marca con cinta el extremo de cada jumper de la serial que va al Pi: verde = pin 32, azul = pin 33, negro = pin 34.
4. Divisor. Suelda 2 resistencias de 1 kΩ entre sí, pata con pata, y cubre la unión con tubo termorretráctil. Este par equivale a 2 kΩ.
5. Corta un jumper por la mitad. Suelda el extremo cortado de una de las mitades a una pata de la 3.ª resistencia y cúbrelo con tubo termorretráctil. El conector hembra de esta mitad es el que va al D1.
6. En la barra de conexión, del lado del convertidor, aprieta en el borne 3 la pata libre de la 3.ª resistencia junto con un extremo del par de 2 kΩ. Aprieta el otro extremo del par en el borne 2, junto con el cable negro que ya está ahí. Dobla la punta de cada pata antes de apretar para que el tornillo la sujete.
7. Verifica con el multímetro, en ohmios: entre el conector hembra del jumper del D1 y el borne 3, cerca de 1 kΩ; entre el borne 3 y el borne 2, cerca de 2 kΩ.
8. Alimentación del Raspberry Pi. Corta 2 jumpers por la mitad: quedan 4 mitades con conector hembra. Corta 45 cm de cable rojo y 45 cm de cable negro de 20 AWG. Suelda 2 mitades al extremo del cable rojo y 2 al del negro, y cubre cada empalme con tubo termorretráctil. Marca con cinta las 2 del cable rojo: van a los pines 2 y 4 (5 V). Las 2 del negro van a los pines 6 y 9 (GND). Pela 6 mm del otro extremo de cada cable: van a los bornes 1 y 2.
9. Driver. Los 3 jumpers ya se retiraron en el preparativo 1. Donde estaban los jumpers ENA y ENB hay 2 pines en cada lugar: uno es la entrada (ENA o ENB) y el otro está conectado a los 5 V de la placa. Con el multímetro en continuidad y el interruptor apagado, identifica en cada par el pin que emite un pitido con el borne +5V del driver: déjalo vacío. Marca el otro con un marcador: ahí va el cable del Arduino. Un cable del Arduino en el pin de 5 V puede quemar la salida del Arduino.
10. Guarda 6 jumpers enteros para las señales del driver y marca cada uno con cinta: ENA, IN1, IN2, IN3, IN4 y ENB.
11. Conecta un cable rojo de 22 AWG y 15 cm al borne 1 de la barra, del lado opuesto al del convertidor. El otro extremo va al borne +5V del driver durante el montaje, junto con los cables azules de los encoders.
12. Encoders. Cada motor viene con un cable de 6 hilos. Conecta el cable al motor y corta el conector del otro extremo. Pela 6 mm de los cables rojo, blanco, azul y negro: van a bornes. Al amarillo y al verde, suelda a cada uno una mitad de jumper con conector hembra (son 2 jumpers más cortados por la mitad) y cúbrelos con tubo termorretráctil. Marca los cables: derecho e izquierdo.
13. Guarda los cables. Durante el montaje, todo se conecta con bornes o conectores, sin soldadura. Atención: en los conectores de 3 pines del shield, solo el pin S (señal) recibe un cable de señal. El pin del medio (V) siempre queda vacío: con el jumper SEL retirado, tiene los 6 V de los servos, y 6 V en un cable de señal pueden quemar el Raspberry Pi o el encoder.
<!-- /GERADO -->

Por qué aquí sirve el conector Dupont común: la pantalla de este robot no se conecta directamente a los pines del Raspberry Pi. Entre el Pi y la pantalla quedan unos 20 mm (medida del modelo, no confirmada), y el conector Dupont mide 14 mm. Si no cabe en tu pantalla, dobla los cables justo encima del conector o suéldalos a un tramo de barra de pines hembra, con los cables saliendo hacia un lado.

Dónde está el pin 1 y por qué el número del pin no es el número del GPIO:
[documentación de la Raspberry Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc).
En la Pi ya encendida, el comando `pinout` muestra el mapa de los pines.

El cable de cada motor mide unos 14 cm
([tabla del motor en una tienda](https://rcdrone.top/products/jgb37-520-dc-gear-motor-with-encoder)). Si algún cable
no llega al driver o al shield, empálmale un tramo de cable 22 AWG con soldadura y tubo termorretráctil, todavía durante este preparativo.

## Preparativo 4: graba la tarjeta microSD, prueba la pantalla y conecta la comunicación serial

La tarjeta se graba en tu computadora con un lector de tarjetas microSD. Después te conectas a Raspberry Pi por la red,
mediante SSH: escribes los comandos en tu computadora y se ejecutan en el Pi.

<!-- GERADO:prep4 -->
1. Instala Raspberry Pi Imager, el programa gratuito de Raspberry Pi, en la computadora y coloca la tarjeta en el lector.
2. En Imager, elige el modelo de tu Pi, el sistema Raspberry Pi OS (64-bit) y la tarjeta.
3. Antes de grabar, abre la configuración de Imager: ponle un nombre al Pi (por ejemplo `robo`), crea un usuario y una contraseña, ingresa el nombre y la contraseña de tu Wi-Fi y activa SSH. Graba la imagen.
4. Inserta la tarjeta en el Pi. Solo para esta prueba, conecta la pantalla con el cable HDMI y el cable USB, y alimenta el Pi con una fuente USB-C de 5 V y 3 A. Espera unos 2 minutos: la pantalla debe mostrar el sistema. El fabricante indica que funciona con Raspberry Pi OS sin instalar un driver.
5. En la computadora, abre la terminal: en Windows es el programa PowerShell; en Mac y Linux, Terminal.
6. Escribe `ssh usuario@robo.local`, reemplazando `usuario` y `robo` por los nombres que creaste. Responde `yes` la primera vez y escribe la contraseña.
7. Si `robo.local` no responde, abre la página de tu router, busca el Pi en la lista de dispositivos conectados y usa su número (la dirección IP), por ejemplo `ssh usuario@192.168.0.50`.
8. Cuando la terminal muestre el nombre del Pi, ya estás dentro. Activa la serial: escribe `sudo nano /boot/firmware/config.txt`, ve al final del archivo y agrega una línea: `dtoverlay=uart5` en Raspberry Pi 4, o `dtoverlay=uart4-pi5` en Raspberry Pi 5. Guarda con Ctrl+O y Enter, y sal con Ctrl+X.
9. Escribe `sudo poweroff`, espera a que el LED verde del Pi deje de parpadear, desconecta la fuente y suelta los 2 cables de la pantalla: volverá a conectarse durante el montaje.
<!-- /GERADO -->

La pantalla es la Waveshare 5inch HDMI LCD (B): 5 pulgadas, 800 × 480, conectada por HDMI, con un cable USB para la alimentación. El fabricante dice que funciona con Raspberry Pi OS sin driver
([página del fabricante](https://www.waveshare.com/5inch-hdmi-lcd-b.htm)). Si la imagen no ocupa toda la pantalla, consulta la
[wiki del fabricante](https://www.waveshare.com/wiki/5inch_HDMI_LCD_%28B%29). No probado en el banco de trabajo. Documentación de Raspberry Pi en GitHub: [SSH](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/ssh.adoc) y [cómo encontrar la dirección del Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/find-your-ip-address.adoc).

La línea serial viene de la [lista de overlays del firmware de Raspberry Pi](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
Después de reiniciar, el nombre del puerto aparece con `ls /dev/ttyAMA*`. El programa que usa esta serial es de la fase 2.

## Los cables de la pantalla

La pantalla se conecta a la Raspberry Pi con 2 cables que quedan dentro de la cabeza: uno HDMI y uno USB. No aparecen en el modelo 3D.

- La Raspberry Pi 4 tiene una salida micro-HDMI en el borde inferior de la placa. Según el modelo, quedan unos 22 mm desde allí hasta el fondo de la cabeza.
- Los puertos USB de la Pi quedan orientados hacia la derecha. Según el modelo, quedan unos 30 mm hasta la pared de la cabeza.
- Los cables que vienen con la pantalla son rectos y largos, y no caben en esos espacios. Por eso, la lista pide un cable HDMI plano y corto, con el conector micro-HDMI en ángulo, y un cable USB corto, con el conector USB-A en ángulo.
- Revisa los 2 cables con las piezas en la mano, antes de cerrar la cabeza. Este es el principal riesgo de ajuste de este robot.

## Cómo se comunica la Raspberry Pi con el Arduino

El agujero para cables del cuello tiene 9 mm y un conector USB no pasa por ahí. Por eso se comunican mediante una serial
(UART) de 3 cables sueltos.

- **En el Arduino:** pines D0 (RX) y D1 (TX), que son el puerto serial real de la placa. No interfieren con la señal de los servos.
- **En la Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX) y pin 34 (GND).
- **Número del pin y número del GPIO:** «pin 32» es la posición en la fila de 40 pines, contada desde la esquina de la tarjeta microSD. «GPIO12» es el nombre de la señal que sale por ese pin. Los dos números son distintos.
- **Voltaje:** el Arduino trabaja a 5 V y la Pi a 3,3 V. El cable que va del Arduino a la Pi pasa por un divisor de 3 resistencias de 1 kΩ, que reduce 5 V a 3,3 V. El cable que va de la Pi al Arduino es directo.
- **Por qué usar resistencias y no un módulo conversor de nivel:** el divisor funciona con 3 resistencias conectadas a la barra de conexión, sin otra placa suelta en el deck.

## Cómo controla el Arduino los motores

El driver L298N tiene 6 pines de control. El Arduino usa 6 conectores del Sensor Shield, siempre solo el pin S.

- **Velocidad:** ENA en D5 (motor derecho) y ENB en D6 (motor izquierdo). Estos dos pines del Arduino pueden variar la fuerza del motor, y la biblioteca de servos no los modifica. Se quitan los puentes ENA y ENB del driver: si están puestos, el motor funciona siempre a la fuerza máxima.
- **Sentido:** IN1 en D4 e IN2 en D7 (motor derecho); IN3 en D8 e IN4 en D12 (motor izquierdo).
- **Los 5 V del driver:** se quita el puente del regulador de 5 V del driver y su borne +5V recibe los 5,1 V de la barra de conexión. Así, la parte de control del driver no depende del voltaje del pack.
- **Encoders:** cada motor tiene un sensor que genera 2 señales. El cable amarillo va a D2 (derecho) y a D3 (izquierdo), los dos pines del Arduino que avisan al programa con cada pulso. El cable verde va a A0 (derecho) y a A1 (izquierdo). El encoder genera 11 pulsos por vuelta del motor, antes de la reducción de 1:56 (tabla de la tienda citada arriba).
- **Alimentación de los encoders:** de 3,3 a 5 V, por los cables azul (positivo) y negro (negativo). Van a los bornes +5V y GND del driver. Nunca al pin V del shield, que tiene los 6 V de los servos.

Mientras el sketch `centrar_servos.ino` esté grabado, los 6 pines del driver quedan en nivel bajo y las ruedas no giran.
El programa que hace andar el robot corresponde a la fase 2.

## Los 8 cables que pasan por el cuello

Son 8 cables: 2 de alimentación (5,1 V de Raspberry Pi, 20 AWG), 3 de la conexión serial y los 3 del cable del servo de tilt. Deben
conectarse dentro de la cabeza ANTES del copo, porque después Raspberry Pi queda encerrado. Tampoco pueden quedar colgando por
debajo de la horquilla en ese momento, porque la parte inferior del copo pasa por debajo de ella. Este es el orden:

1. Al montar la Raspberry Pi, antes de colocar el panel con la pantalla, conecta los 3 jumpers del puerto serial a los pines 32, 33 y 34, y los 4 conectores del cable de alimentación a los pines 2, 4, 6 y 9.
2. Con la cabeza todavía abierta (marco, pantalla, servo de inclinación y horquilla en su lugar), revisa esos 7 conectores y los 2 cables de la pantalla.
3. Conecta la extensión de 30 cm al cable del servo de inclinación.
4. Baja los 8 cables por el orificio de 9 mm de la horquilla, de arriba hacia abajo. Primero pasa el conector de la extensión, que tiene 7,6 mm de ancho y entra justo.
5. Detente cuando las puntas queden al ras de la cara inferior de la horquilla. Deja unos 5 cm de cable sobrante dentro de la cabeza: se inclina alrededor de la horquilla.
6. Cierra la cabeza con la carcasa. Con unas pinzas, saca las puntas de los 8 cables por la ranura del fondo de la carcasa.
7. Pasa los cables por el tubo del cuello y coloca la cabeza encima.
8. En el deck, con el interruptor apagado y sin soldar: los 2 cables de 5,1 V en los bornes 1 y 2 de la barra de conexión; el cable azul en el borne 3; el conector del verde en el pin S de D0 y el del negro en el pin G de D0; el jumper del divisor en el pin S de D1; la extensión del servo en D10.

Deja unos 10 cm de holgura dentro del torso: el cuello gira casi una vuelta y retuerce los cables. Este paso nunca se ha
ensayado con las piezas impresas.

## Corriente, cable y fusible

Los valores de abajo se calculan a partir de las fichas técnicas; no se midieron.

- Uso normal: unos 2 A de salida del pack. La Raspberry Pi con la pantalla consume unos 1,5 A a 5,1 V, los servos menos de 1 A a 6 V y cada motor unos 0,2 A al andar.
- Peor caso: unos 6,5 A, con las 2 ruedas bloqueadas (1,2 A cada una, según la tabla del motor), el UBEC en el límite de 3 A, el XL4015 a 3 A y el pack a 9 V.
- Interruptor KCD11-101: 3 A a 250 V~ y 6 A a 125 V~ ([ficha de la tienda](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). La ficha no indica un valor para corriente continua.
- Fusible de 3 A: es el valor más bajo del interruptor. El uso normal queda por debajo, y una sobrecarga prolongada hace que se funda el fusible antes de que se caliente el interruptor.
- **El interruptor es el punto más débil de este robot.** Si hace fuerza contra un obstáculo mientras los servos están bajo carga, la corriente supera los 3 A y el fusible puede fundirse. Cambiarlo por un interruptor más grande exige modificar el recorte de 13,5 × 9 mm en la base: queda pendiente del proyecto.
- Fusible de acción retardada (marcado T3A o T3,15A): el arranque de los motores y los servos, y la carga del capacitor de 1000 µF, generan picos de una fracción de segundo. Un fusible rápido puede fundirse con esos picos aunque no haya una falla; el retardado soporta el pico breve y se funde ante una sobrecarga prolongada (comportamiento habitual de este tipo de fusible; medida no confirmada).
- Si el fusible se funde durante el uso normal del robot, no pongas uno de mayor capacidad: mide la corriente e identifica qué está haciendo fuerza.
- Driver L298N: 2 A por canal (valor del anuncio de la tienda). El motor bloqueado consume 1,2 A, dentro de ese límite.
- Cable 20 AWG (0,5 mm²) desde el pack hasta la barra de conexión, desde la barra hasta el conversor y el driver, y en el par de 5,1 V que sube hasta la Raspberry Pi: con 1,5 A, la caída calculada en ese par es de unos 0,05 V. No se ha medido la caída que suman los contactos de los conectores Dupont. Cable 22 AWG (0,33 mm²) para el resto de la alimentación.
- Si la Raspberry Pi indica bajo voltaje, acorta el par de 5,1 V y revisa el ajuste. Para comprobarlo, escribe `vcgencmd get_throttled` en la Pi: la respuesta correcta es `throttled=0x0`.
- El programa de la fase 2 debe acelerar y frenar gradualmente, y no debe hacer que los motores y los servos hagan fuerza al mismo tiempo.

## Calor dentro de la cabeza

El Raspberry Pi 4 queda encerrado en la cabeza, que es de PLA y no tiene aberturas de ventilación. Es un riesgo que no se ha medido.

- El PLA se ablanda cerca de 60 °C (valor habitual, medida no confirmada).
- El Pi reduce la velocidad cuando el procesador alcanza entre 80 y 85 °C ([documentación de Raspberry Pi](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)).
- Pega los disipadores adhesivos a los chips del Pi antes de montarlo.
- Con el robot encendido durante media hora, escribe `vcgencmd measure_temp` en el Pi. Si supera los 70 °C, imprime la carcasa de la cabeza en PETG o abre agujeros de ventilación en la pared trasera.

## La primera vez que enciendes el robot montado

1. Interruptor apagado. Con el multímetro en modo continuidad, comprueba que el positivo y el negativo del pack no estén en corto.
2. Coloca el robot sobre un soporte, con las 2 ruedas en el aire.
3. Antes de apretar en la barra los 2 cables que bajan de la Raspberry Pi, enciende el interruptor y mide en la barra de conexión: 5,1 V entre los bornes 1 y 2, con el rojo en el positivo, y de 9 a 12,6 V entre los bornes 4 y 5. Mide 6 V en el borne azul. Apaga el interruptor.
4. Conecta los cables de la Pi a la barra, el rojo al borne 1 y el negro al borne 2, y vuelve a encender el interruptor.
5. El LED del Arduino parpadea, los dos servos mantienen el centro, las ruedas quedan quietas, se enciende el LED de alimentación de la Raspberry Pi y, en alrededor de 1 minuto, la pantalla muestra el sistema.
6. Si no se enciende nada, apaga el interruptor y revisa el fusible.

## Lo que todavía no se probó

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

Qué comprar: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
