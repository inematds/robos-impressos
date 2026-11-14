# Conexión eléctrica del robot cuadrado de mesa

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**No probado en el banco de trabajo.** Este esquema se elaboró a partir de las fichas de los componentes; todavía no se conectó ningún cable en un robot montado.
Verifica cada conexión con el multímetro antes de encender el interruptor. Si tu placa tiene un nombre impreso diferente del
que aparece aquí, usa el nombre de la placa.

![Esquema de conexión del robot cuadrado de mesa: batería, fusible, placa de protección, cargador, interruptor, convertidores, Arduino con Sensor Shield, servos, Raspberry Pi y pantalla](ligacao.es.svg)

Página con el mismo esquema: https://inematds.github.io/robos-impressos/guia/es/cubo/#energia

## Seguridad con baterías de litio

- **Polaridad:** rojo al positivo, negro al negativo. Mide con el multímetro antes de cada conexión nueva. Un cable invertido quema la placa de inmediato.
- **Ajuste antes de conectar la carga:** LM2596 a 5,1 V y UBEC a 6 V, medidos con el multímetro, sin Raspberry Pi, sin Arduino y sin los servos conectados.
- **Un cortocircuito puede provocar un incendio:** suelda con las celdas FUERA del soporte y aísla cada empalme con tubo termorretráctil. Ninguna parte metálica debe quedar expuesta.
- **Fusible:** 5 A, en el cable positivo, a pocos centímetros del soporte de baterías.
- **Celdas iguales:** las dos 18650 deben ser de la misma marca, del mismo modelo y nuevas. Una celda aplastada, hinchada o caliente debe llevarse a un punto de recolección de pilas, no al robot.
- **Primera carga:** quédate cerca, con el robot sobre una superficie que no se queme.

## Qué alimenta cada componente

- **Pack 2S:** dos celdas 18650 en serie, de 6 V (descargado) a 8,4 V (cargado). La corriente pasa por el fusible y la placa de protección (BMS).
- **Cargador USB-C:** se conecta a la salida de la placa de protección, antes del interruptor. El robot se carga apagado, con una fuente USB-C de 15 W o más.
- **Interruptor:** corta el positivo que va a los dos convertidores.
- **LM2596, ajustado a 5,1 V:** alimenta la Raspberry Pi (mediante el adaptador USB-C con bornes) y el Arduino (por el pin de 5 V del Sensor Shield).
- **UBEC a 6 V:** alimenta solo los 2 servos, por el borne azul del Sensor Shield, con el jumper SEL retirado.
- **Negativo (GND):** es común para todo el robot.

Por qué el Arduino recibe los 5,1 V del LM2596 y no el voltaje de la batería: la entrada VIN del Arduino Uno requiere de 7 a 12 V
([ficha del Arduino Uno R3](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)) y el pack pasa buena
parte de la descarga por debajo de 7 V.

## Tabla de conexiones, cable por cable

<!-- GERADO:ligacoes -->
### Batería, protección y carga

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Soporte de las baterías: cable rojo (positivo del pack) | Portafusible de 5 A y, después, pad B+ de la placa de protección | rojo | 22 AWG | El fusible queda a pocos centímetros del soporte. |
| Soporte de las baterías: cable negro (negativo del pack) | Pad B− de la placa de protección | negro | 22 AWG |  |
| Soporte de las baterías: lámina de metal que une las 2 celdas (punto medio) | Pad BM de la placa de protección | amarillo | 22 AWG | Es el 3.er cable. Suéldalo a la lámina con las celdas FUERA del soporte. |
| Pad BM de la placa de protección | Cargador USB-C: borne del medio (punto medio del pack) | amarillo | 22 AWG | Sin este cable, el cargador no equilibra las dos celdas. |
| Cargador USB-C: salida positiva | Pad P+ de la placa de protección | rojo | 22 AWG | El cargador queda antes del interruptor: el robot se carga apagado. |
| Cargador USB-C: salida negativa | Pad P− de la placa de protección | negro | 22 AWG |  |

### Interruptor y convertidores

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Pad P+ de la placa de protección | Interruptor de encendido/apagado y, después, entrada IN+ del LM2596 y cable rojo de entrada del UBEC | rojo | 22 AWG | El interruptor corta solo el positivo. |
| Pad P− de la placa de protección | Entrada IN− del LM2596 y cable negro de entrada del UBEC | negro | 22 AWG | Este es el negativo común (GND) de todo el robot. |

### 5 V: Raspberry Pi y Arduino

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Salida OUT+ del LM2596 (5,1 V) | Por el cuello, hasta el borne + del adaptador USB-C, que va al puerto USB-C de la Raspberry Pi | rojo | 22 AWG | Ajusta los 5,1 V ANTES de conectar este cable. |
| Salida OUT− del LM2596 | Por el cuello, hasta el borne − del adaptador USB-C | negro | 22 AWG |  |
| Salida OUT+ del LM2596 (5,1 V) | Pin de 5 V del Sensor Shield (el + del conector COM o IIC) | rojo | Dupont | Por aquí recibe energía el Arduino. Antes, confirma con el multímetro que este pin NO tenga continuidad con el borne azul VCC. |
| Salida OUT− del LM2596 | Pin − (GND) del mismo conector del Sensor Shield | negro | Dupont |  |

### 6 V: servos

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Cable rojo de salida del UBEC (6 V) | Borne azul VCC del Sensor Shield | rojo | cable del UBEC | Jumper SEL del shield RETIRADO y jumper del UBEC en 6 V. |
| Cable negro de salida del UBEC | Borne azul GND del Sensor Shield | negro | cable del UBEC |  |
| Capacitor de 1000 µF: pata larga (+) | Borne azul VCC; la pata con la franja (−) va en el borne azul GND | sin cable | patas del capacitor | El capacitor invertido explota. |
| Servo de pan (en la base) | Conector D9 del Sensor Shield | cable del servo | cable de 3 hilos del servo | G = marrón o negro, V = rojo, S = naranja o amarillo. |
| Servo de tilt (en la cabeza) | Por el cuello, con la extensión de 30 cm, hasta el conector D10 del Sensor Shield | cable del servo | cable de 3 hilos del servo | Mismo orden de colores que en D9. |

### Conexión serial entre Raspberry Pi y Arduino

| De | Para | Color | Cable | Atención |
|---|---|---|---|---|
| Raspberry Pi: pin 32 (GPIO12, TX) | Por el cuello, hasta el pin S de D0 (RX) del Sensor Shield | verde | Dupont | Directo: los 3,3 V del Pi ya sirven como nivel alto para Arduino. |
| Pin S de D1 (TX) del Sensor Shield | Resistor de 1 kΩ y, después de él, por el cuello hasta el pin 33 (GPIO13, RX) de Raspberry Pi | azul | Dupont | Nunca conectes D1 directamente al Pi: son 5 V en un pin de 3,3 V. |
| Punto entre el resistor de 1 kΩ y el cable azul | 2 resistores de 1 kΩ en serie y, después de ellos, un pin G (GND) del Sensor Shield | negro | patas de los resistores | Los 3 resistores forman el divisor: 5 V se convierten en 3,3 V. |
| Raspberry Pi: pin 34 (GND) | Por el cuello, hasta un pin G (GND) del Sensor Shield | negro | Dupont |  |
| Pantalla MPI3501 | Conectada a los pines 1 a 26 de Raspberry Pi | sin cable | conector de la propia pantalla | Usa SPI y los 5 V de los pines 2 y 4. |
<!-- /GERADO -->

## Preparativo 1: suelda la alimentación y ajusta los dos voltajes

Hazlo en la mesa de trabajo, antes de montar el robot, con la base impresa al lado como plantilla para medir la longitud de los cables.

1. Suelda el 3.er cable (amarillo) a la lámina metálica que une las dos celdas, con las celdas fuera del soporte.
2. Conecta el soporte, el fusible, la placa de protección y el cargador, según la tabla.
3. Encaja el interruptor en el recorte de la base, desde afuera, pasa los cables por el recorte y suéldalo al positivo.
4. Conecta las entradas del LM2596 y del UBEC. Deja las salidas sueltas, sin conectar nada.
5. Coloca las celdas en el soporte, verifica el lado positivo y enciende el interruptor.
6. Con el multímetro en la salida del LM2596, gira el tornillo de ajuste con el destornillador hasta que marque 5,1 V. Necesitarás varias vueltas.
7. Mide la salida del UBEC: debe marcar 6 V. Si marca 5 V, cambia su jumper a 6 V.
8. Apaga el interruptor.

## Preparativo 2: carga el programa y coloca los 2 servos a 90°

El programa es el sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). Lleva los dos servos
al centro y los mantiene allí.

1. Abre el sketch en Arduino IDE. Conecta el Arduino Uno a la computadora con el cable USB, sin el shield y sin la batería.
2. En Herramientas, elige la placa Arduino Uno y el puerto en el que apareció. Haz clic en Cargar.
3. Desconecta el cable USB.
4. Encaja el Sensor Shield en el Uno y retira el jumper SEL del shield.
5. Con el multímetro en modo de continuidad, confirma que el pin de 5 V que vas a usar en el shield NO emita un pitido con el borne azul VCC.
6. Conecta los 6 V del UBEC al borne azul (VCC y GND) y el capacitor de 1000 µF al mismo borne.
7. Conecta los 5,1 V del LM2596 al pin de 5 V del shield y el negativo a un pin G.
8. Conecta el servo de pan a D9 y el servo de tilt a D10.
9. Enciende el interruptor: los dos servos irán al centro (90°) y el LED del Uno parpadeará una vez por segundo.
10. Apaga el interruptor. A partir de ahora, no gires los ejes de los servos con la mano.

Tres avisos:

- No alimentes el servo MG996R con los 5 V del USB. El puerto USB suministra 0,5 A y el servo necesita más al arrancar.
- Nunca conectes el cable USB de la computadora con la batería encendida: ambas fuentes quedarían en paralelo.
- Carga el sketch antes de atornillar el Uno a la base. Una vez colocado, quedan unos 10 mm entre el conector USB y la pared, y el cable no entra.

El sketch compila para Arduino Uno (arduino-cli, core arduino:avr 1.8.8, biblioteca Servo 1.3.0). Todavía no se ha
probado en un robot montado.

## Preparativo 3: graba la tarjeta microSD e instala el controlador de la pantalla

1. Graba la tarjeta con Raspberry Pi Imager, el programa gratuito de Raspberry Pi. Elige el modelo de tu Pi, el sistema Raspberry Pi OS (64-bit) y la tarjeta.
2. Antes de grabar, abre la configuración de Imager: define el usuario, la contraseña y el Wi-Fi, y activa SSH. Así podrás acceder al Pi por la red, sin teclado.
3. La pantalla es la MPI3501: 3,5 pulgadas, 480 × 320, controlador ILI9486, conectada por SPI en los pines 1 a 26. Solo se enciende después de instalar el controlador.
4. El fabricante recomienda el paquete LCD-show. En el Pi, por la red, ejecuta los tres comandos siguientes.

```
git clone https://github.com/goodtft/LCD-show.git
cd LCD-show
sudo ./LCD35-show
```

Fuente del modelo, los pines y el controlador: [página de la MPI3501 en lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display).
El script reemplaza el archivo de configuración del Pi y lo reinicia. No probado en el banco de trabajo: el fabricante enumera pruebas hasta
Raspberry Pi 3B+; en Pi 4 y Pi 5 quizá sea necesario hacer ajustes.

## Cómo se comunica la Raspberry Pi con el Arduino

La Raspberry Pi va en la cabeza y el Arduino en la base. El orificio para los cables del cuello tiene 9 mm y un conector USB no pasa por
él. Por eso, ambos se comunican mediante una conexión serial (UART) de 3 cables sueltos que pasan por el orificio.

- **En el Arduino:** pines D0 (RX) y D1 (TX), que son la conexión serial real de la placa. No interfieren con la señal de los servos.
- **En la Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX) y pin 34 (GND). La pantalla ocupa los pines 1 a 26; estos tres quedan libres.
- **Voltaje:** el Arduino trabaja a 5 V y el Pi a 3,3 V. El cable que va del Arduino al Pi pasa por un divisor de 3 resistencias de 1 kΩ, que reduce los 5 V a 3,3 V. El cable que va del Pi al Arduino va directo.
- **Por qué usar resistencias y no un módulo conversor de nivel:** el módulo necesita una referencia de 3,3 V, y los pines de 3,3 V del Pi quedan debajo de la pantalla.

Cómo montar el divisor: suelda una resistencia de 1 kΩ al cable que sale de D1. En el otro extremo, suelda el cable azul que sube
al pin 33 del Pi y otras dos resistencias de 1 kΩ en serie, que terminan en un pin G del shield. Cubre todo con
tubo termorretráctil.

Cómo conectar al Pi: los pines 31 a 34 quedan debajo de la placa de la pantalla, donde sobran unos 17,5 mm (medida no
confirmada). El conector Dupont común, de 14 mm, no cabe en posición vertical. Corta un trozo de 2 × 2 de la barra de pines hembra,
suelda los 3 cables de lado a sus terminales y encájalo en los pines 31 a 34 antes de colocar la pantalla.

Para activar la conexión serial en el sistema del Pi, agrega una línea al final del archivo `/boot/firmware/config.txt`, DESPUÉS de
instalar el controlador de la pantalla, porque el script del controlador vuelve a escribir ese archivo:

- Raspberry Pi 4: `dtoverlay=uart5`
- Raspberry Pi 5: `dtoverlay=uart4-pi5`

Fuente: [lista de overlays del firmware de Raspberry Pi](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
Después de reiniciar, consulta el nombre del puerto con `ls /dev/ttyAMA*`. No probado en el banco de trabajo. El programa que usa esta
conexión serial corresponde a la fase 2.

## Los 8 cables que pasan por el cuello

Pasa los cables por el orificio de 9 mm antes de cerrar la cabeza sobre el tubo, en este orden:

1. La extensión del servo de tilt: el conector de 3 pines tiene 7,6 mm de ancho y pasa justo.
2. Los 2 cables de 5,1 V de la Raspberry Pi (rojo y negro). El adaptador USB-C se atornilla a ellos después.
3. Los 3 cables de la conexión serial (verde, azul y negro).

Deja unos 10 cm de holgura dentro de la base: el cuello gira casi una vuelta y tuerce los cables.

## Corriente, cable y fusible

Los valores de abajo se calculan a partir de las fichas técnicas; no se midieron.

- Uso normal: cerca de 2 A desde el pack (Raspberry Pi con cerca de 1 A a 5 V y servos con menos de 1 A a 6 V).
- Peor caso: cerca de 6 A, con el LM2596 y el UBEC en el límite de 3 A y el pack a 6,5 V.
- Cable 22 AWG (0,33 mm²) en toda la parte de alimentación. En el tramo del cuello, con 2 A, la caída calculada es de 0,1 V: por eso el ajuste es 5,1 V y no 5,0 V.
- Fusible de 5 A: está por encima del uso normal y por debajo de los 10 A de la placa de protección.
- Interruptor KCD11: en general es de 3 A (medida no confirmada; lee el valor grabado en el cuerpo del tuyo).
- El programa de la fase 2 no puede hacer que los dos servos ejerzan fuerza al mismo tiempo al final del recorrido.

## La primera vez que enciendes el robot montado

1. Interruptor apagado. Comprueba con el multímetro que no haya continuidad entre el positivo y el negativo del pack.
2. Enciende el interruptor. Mide 5,1 V en el adaptador USB-C, todavía desconectado del Pi, y 6 V en el borne azul.
3. Apaga, conecta el adaptador USB-C al Raspberry Pi y vuelve a encender.
4. El LED del Arduino parpadea, los dos servos mantienen el centro y se enciende el LED de alimentación del Raspberry Pi.

## Lo que todavía no se probó

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

Qué comprar: [LISTA-DE-COMPRAS.es.md](LISTA-DE-COMPRAS.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
