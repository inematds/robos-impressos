# Lista de compras del dinosaurio

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Todo lo que necesitas comprar para montar el dinosaurio en la fase 1: el cuerpo montado y conectado. El programa viene después, en la fase 2.

Página con la misma lista: https://inematds.github.io/robos-impressos/guia/es/dino/#comprar

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
- Todavía no se imprimió ni se montó ninguna pieza. La parte eléctrica no se probó en el banco de trabajo: se diseñó a partir de las fichas de los componentes.
- Seis piezas necesitan soportes de impresión: cráneo, cuerpo, carcasa trasera, mandíbula, horquilla del cuello y cuna del tilt. Los soportes quedan por dentro o por debajo, fuera de la cara, pero todavía nadie los retiró de una pieza real.
- Los archivos 3MF de las camas nunca se abrieron en Bambu Studio. Si alguno no abre, usa los STL.
- El interruptor de encendido y apagado es de 3 A y, según el cálculo de las fichas, el uso normal se acerca a ese valor (entre 2,5 y 3 A con las ruedas en movimiento y la cabeza y los brazos moviéndose). El fusible de 3 A protege el interruptor y puede abrirse cuando el robot haga fuerza. Un interruptor más grande requiere modificar el recorte de la pieza: es una tarea pendiente del proyecto.
- El Raspberry Pi recibe los 5,1 V por los pines de 5 V, porque en la bandeja su puerto USB-C queda pegado a la pared del rack. Es una conexión común, pero no se probó en este robot: si cambias los cables o aplicas una tensión incorrecta en esos pines, quemarás el Pi. Mide antes de conectarlo.
- Sobre el Raspberry Pi quedan cerca de 17 mm hasta la bandeja de arriba (medida del modelo, sin confirmar). El conector Dupont común mide cerca de 16,5 mm de alto y puede no caber. Plan B: soldar los cables a una barra de pines hembra baja, con los cables saliendo hacia un lado.
- El cupón de prueba no verifica la abertura para el servo MG996R. Comprueba el servo en la cuna del tilt, que se imprime en una de las primeras camas, antes de las impresiones largas.
- El portafusible, la barra de conexión y los 3 resistores de la conexión serial no tienen un lugar modelado: quedan sueltos dentro del cuerpo, aislados con tubo termorretráctil.
- Las longitudes de los cables (servos de la cabeza, extensiones y jumpers) se estimaron a partir del modelo. La cabeza gira e inclina y tira de esos cables: deja holgura y comprueba ambos extremos antes de cerrar.
- El horn del microservo de cada brazo no aparece en el modelo 3D: la prueba de montaje no demuestra que el cuerpo baje con el horn en su lugar. Monta el horn apuntando hacia atrás y hacia arriba, y gíralo solo después.
- El Arduino va atravesado en la bandeja y su USB queda de lado: para volver a cargar el programa, hay que sacar la bandeja.
- Las medidas marcadas como NC provienen de anuncios de tiendas. Mide tu pieza antes de imprimir la parte que hace contacto con ella.
- El estriado del microservo tiene pasos de unos 17° (valor habitual, sin confirmar): el horn de la boca y los de los brazos pueden no quedar exactamente en la posición de 90°. Elige el diente más cercano; el ajuste fino se hace en el programa, en la fase 2.
- Calor: el Raspberry Pi queda cerrado dentro del cuerpo, que es de PLA y no tiene abertura de ventilación. El PLA se ablanda cerca de 60 °C y el Pi reduce la velocidad a partir de 80 °C. Pega los disipadores y mide con el comando `vcgencmd measure_temp`. Si supera los 70 °C, abre orificios de ventilación en la carcasa trasera.
<!-- /GERADO -->

## Cuánto cuesta

<!-- GERADO:custo -->
- Piezas de la fase 1 (sin filamento ni herramientas): **R$ 889–1953**.
- Desde cero (piezas, 2 rollos de filamento y todas las herramientas): **R$ 1273–2918**.
- Solo los 2 rollos de filamento (1 de PETG y 1 de PLA): R$ 170–290.
- Si ya tienes el Arduino Uno, descuenta: R$ 43–90.
- Si ya tienes todas las herramientas, descuenta: R$ 214–675.
<!-- /GERADO -->

## Fase 1: qué comprar

<!-- GERADO:compras -->
### Cerebro y movimiento

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | El cerebro del robot. Va en la bandeja de abajo, dentro del cuerpo. En la fase 1 solo se conecta y configura; si quieres aplazar esta compra, puedes montar todo sin él y dejar la bandeja vacía. El Pi 5 también sirve, con 1 cámara y sin accesorios USB: el convertidor entrega cerca de 2 A. | R$ 450–800 (cada uno) | no verificado |
| [Tarjeta microSD de 32 GB clase 10](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Sistema del Raspberry Pi. | R$ 25–50 (cada uno) | no verificado |
| [Kit de disipadores adhesivos para Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | El Raspberry Pi queda cerrado dentro del cuerpo, que es de PLA y no tiene abertura de ventilación. Los disipadores pegados a los chips bajan la temperatura. NC: altura del disipador: sobre el Raspberry Pi quedan cerca de 17 mm hasta la bandeja de arriba. | R$ 8–25 (kit) | no verificado |
| [Servo MG996R de 180° (de posición, no de rotación continua)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | Uno gira la cabeza hacia los lados (pan) y el otro la inclina (tilt). NC: grosor y orificios de las pestañas, diámetro y grosor del horn redondo. | R$ 30–75 (cada uno) | R$ 70,45 |
| [Microservo de 9 g, de 180°: MG90S o SG90 (de posición, no de rotación continua)](https://lista.mercadolivre.com.br/micro-servo-mg90s-180-graus) | 3 / 3 | Abre la boca (1) y mueve los brazos (2). Prefiere el MG90S, que tiene engranajes de metal. NC: grosor de la pestaña, distancia entre los orificios y tamaño del horn de 1 brazo. | R$ 15–45 (cada uno) | R$ 17,71 (SG90) a R$ 41,84 (MG90S) |
| [Extensión de servo de 30 cm (cable extensor de 3 hilos, macho-hembra)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 2 / 2 | Una lleva el cable del servo de la boca hasta el Arduino; la otra es para el servo de tilt, si su cable no alcanza. NC: longitud del cable de fábrica de cada servo (de 15 a 30 cm): mide el recorrido antes de cerrar. | R$ 5–15 (cada uno) | no verificado |
| [Motor DC de 3 a 6 V con caja reductora 1:48 (motor TT amarillo)](https://lista.mercadolivre.com.br/motor-dc-3-6v-caixa-de-reducao-48-1) | 2 / 2 | Tracción: uno en cada rueda. Si viene sin cables, suelda 2 cables a cada uno en el preparativo 1. NC: distancia entre los 2 agujeros traseros (la ranura acepta de 12,3 a 17,6 mm) y grosor de la caja (18,6 mm en el modelo). | R$ 7–20 (cada uno) | R$ 9,01 |
| [Rueda de 65 mm para motor TT](https://lista.mercadolivre.com.br/roda-65mm-motor-dc-arduino) | 2 / 2 | Encaja a presión en el eje del motor. Muchas tiendas venden el par motor + rueda. NC: diámetro (65 mm en el modelo; hay ruedas de 64 a 68 mm) y ancho (hasta 27 mm). | R$ 5–15 (cada uno) | R$ 20,54 el kit de 1 motor con 1 rueda de 64 mm |
| [Esfera de acero de 16 mm (o una canica, como medida)](https://lista.mercadolivre.com.br/esfera-de-aco-16mm) | 1 / 1 | Tercer punto de apoyo del robot, atrás, bajo la raíz de la cola. Gira libremente en un alojamiento, sujeta por una tapa. NC: diámetro: el alojamiento es para 16 mm; las canicas varían de 14 a 25 mm. | R$ 3–10 (cada uno) | no verificado |
| [Driver de motores L298N (puente H doble)](https://lista.mercadolivre.com.br/driver-ponte-h-l298n) | 1 / 1 | Activa e invierte los 2 motores de las ruedas, por orden del Arduino. NC: distancia entre los 4 agujeros (37 mm en el modelo); si no coincide, fíjalo con cinta de doble cara. | R$ 20–35 (cada uno) | R$ 21,51 a R$ 29,18 |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (quizás ya tienes) | 1 / 1 | Controla los 5 servos y los 2 motores. Va en la bandeja superior, dentro del cuerpo. | R$ 43–90 (cada uno) | R$ 43,28 a R$ 89,95 |
| [Sensor Shield V5.0 para Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Se coloca sobre el Uno y ofrece conectores de 3 pines para los servos, con alimentación separada a través del borne azul. El Arduino recibe los 5,1 V por el pin + del conector COM del shield. NC: Según la foto de la tienda, el conector COM tiene 4 pines verticales, marcados TX, RX, − y +; hay versiones del shield con los pines en otro lugar. Mide antes de conectar. | R$ 11–35 (cada uno) | R$ 18,13 |
| [Resistor de 1 kΩ, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 paquete de 10 | Divisor de tensión en la conexión serial: baja los 5 V del Arduino a los 3,3 V que acepta Raspberry Pi. Los 3 quedan sujetos a la barra de conexión. | R$ 1–5 (paquete) | no verificado |

### Energía

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Batería 18650 de ion de litio de 3,7 V (celda suelta)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | Pack 2S: 7,4 V nominales (8,4 V con carga completa). Compra dos iguales, nuevas y de una marca conocida. | R$ 13–45 (cada uno) | R$ 26,08 el kit con 2 |
| [Soporte para 2 baterías 18650 lado a lado, con cables](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Sujeta las 2 celdas en serie. Va en el piso del chasis y sale por atrás. NC: el compartimento del chasis acepta hasta 78 × 41 × 22 mm. | R$ 5–15 (cada uno) | R$ 6,22 |
| [Portafusible con cables para fusible de vidrio de 5 × 20 mm, con fusible retardado de 3 A (marcado T3A o T3,15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (y 1 fusible de repuesto) | En el cable positivo, justo después del soporte de las baterías. Es de 3 A porque el interruptor es de 3 A: ante una sobrecarga, el fusible se abre antes de que se caliente el interruptor. Es retardado porque el arranque de los servos y la carga del capacitor producen picos de una fracción de segundo, que quemarían un fusible rápido sin que haya una falla. No tiene un espacio modelado: queda suelto en el cable. | R$ 4–12 (conjunto) | no verificado |
| [Placa de protección BMS 2S 10 A (modelo 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Corta la descarga profunda, la sobrecarga y el cortocircuito. Va soldada a los cables de la batería y fijada con cinta doble faz. NC: nombre impreso de los pads de soldadura. En la placa de la tienda consultada, solo el reverso tiene nombres: B+, B1 (medio), B− y C−. Por la foto, C− es la salida negativa (la función de P− en otras placas) y la salida positiva es la propia B+; es una interpretación de la foto, compruébalo con el multímetro. | R$ 8–20 (cada uno) | no verificado |
| [Cargador USB-C 2S/3S con balanceo (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Carga las dos celdas sin abrir el robot. Va en una pequeña plataforma del chasis, atrás; el conector entra por una ranura bajo la raíz de la cola. NC: altura de la boca USB-C en la ranura de 13 × 7 mm bajo la raíz de la cola. | R$ 15–30 (cada uno) | R$ 17,90 |
| [Convertidor step-down LM2596 ajustable (placa azul, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Reduce el voltaje del pack a los 5 V del Raspberry Pi y del Arduino. Ajústalo a 5,1 V con el multímetro ANTES de conectar cualquier placa. La placa soporta cerca de 2 A continuos sin disipador. El XL4015 no sirve aquí: necesita al menos 8 V. NC: los 2 A continuos son el valor habitual de esta placa, sin ficha que lo confirme. | R$ 8–20 (cada uno) | R$ 10,22 |
| [UBEC 6 V 3 A (Hobbywing UBEC 3A 2-6S o equivalente)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Proporciona los 6 V de los 5 servos, separados de los 5 V de las placas. | R$ 25–60 (cada uno) | no verificado |
| [Capacitor electrolítico 1000 µF 16 V](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | En el borne de 6 V de los servos: soporta el pico de corriente del arranque. | R$ 1–4 (cada uno) | R$ 2,33 |
| [Interruptor basculante KCD11-101 de 3 A (recorte de 13,5 × 9 mm)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Enciende y apaga. Encaja por debajo del piso, entre las patas. NC: grosor de panel que admite el seguro. | R$ 3–8 (cada uno) | R$ 3,74 a R$ 5,40 (modelos KCD1; comprueba el recorte) |
| [Cable flexible de 22 AWG (0,33 mm²): rojo, negro y un tercer color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | unos 2 m de rojo, 2 m de negro y 30 cm de amarillo / 3 m de rojo, 3 m de negro, 1 m de amarillo | Toda la parte de alimentación y los cables de los 2 motores. El amarillo es el 3.er cable, del punto medio del paquete. | R$ 12–30 (total) | R$ 22,40 (5 m bicolor) |
| [Barra de conexión de 12 vías (tipo sindal), para cable fino](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 3 vías (bornes 1, 2 y 3) / 1 barra de conexión de 12 vías; corta un tramo de 3 | Va dentro del cuerpo y evita soldar con el robot montado. Borne 1: los 5,1 V. Borne 2: el negativo. Borne 3: el cable azul de la conexión serial y las resistencias del divisor. De un lado entran los cables que vienen del convertidor; del otro, los que van a Raspberry Pi, Arduino y al driver. No tiene un lugar modelado: queda suelta. | R$ 3–10 (barra) | no verificado |
| [Jumpers Dupont hembra-hembra de 20 cm (kit de 40)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-20cm) | 16 cables / 1 kit de 40 | Alimentación y conexión serial de Raspberry Pi, alimentación del Arduino y las 6 señales del driver de motores. | R$ 8–20 (el kit) | no verificado |

### Fijación

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Inserto de latón M3 para inserción en caliente (para orificio de 4,0 mm, hasta 5,7 mm de largo)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 13 / 1 paquete de 20 o más | La rosca metálica de las piezas. La ubicación de cada una está en la tabla de tornillos. | R$ 15–40 (paquete) | no verificado |
| [Tornillo M3 × 8 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 10 / 2 kits de 10 | Driver de motores, Arduino y tapa de la esfera. | R$ 3–8 (kit de 10) | R$ 6,14 el kit de 10 (tipo de cabeza no informado) |
| [Tornillo M3 × 10 mm, cabeza cilíndrica Allen](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 6 / 1 kit de 10 | Collar, placa de la cabeza y pasador de la cuna. | R$ 3–8 (kit de 10) | R$ 3,55 el kit de 10 (Phillips) |
| [Tornillo M3 × 12 mm](https://lista.mercadolivre.com.br/parafuso-m3x12) | 11 / 2 kits de 10 | 4 en cada servo MG996R, con tuerca, y 3 que sujetan la placa de la cabeza al cráneo. | R$ 3–8 (kit de 10) | no verificado |
| [Tornillo M3 × 16 mm](https://lista.mercadolivre.com.br/parafuso-m3x16) | 2 / 1 kit de 10 | Sujeta el cuerpo a los postes del chasis, detrás de los muslos. | R$ 3–8 (el kit de 10) | no verificado |
| [Tornillo M3 × 30 mm](https://lista.mercadolivre.com.br/parafuso-m3x30) | 4 / 1 kit de 10 | Fija los 2 motores de las ruedas. Con M3 × 25, la tuerca agarra solo 1,4 mm de rosca: son 18,6 mm de motor más 5 mm de pared. | R$ 3–10 (el kit de 10) | R$ 3,44 el kit de 10 unidades M3 × 25 (no se encontró el de 30 mm) |
| [Tuerca hexagonal M3](https://lista.mercadolivre.com.br/porca-sextavada-m3) | 12 / 1 kit de 20 o más | Para los tornillos de los 2 servos MG996R y los 2 motores. | R$ 3–10 (el kit) | no verificado |
| [Tornillo autorroscante M2,5 × 8 mm](https://lista.mercadolivre.com.br/parafuso-m2.5x8-auto-atarraxante) | 4 / 1 kit | Fija la Raspberry Pi a la bandeja. | R$ 5–15 (el kit) | no verificado |
| [Tornillo autorroscante M2 × 8 mm](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit de 10 | 4 en cada horn redondo: fijan la horquilla al servo de pan y la cuna al servo de tilt. NC: diámetro de los orificios del horn redondo. | R$ 3–8 (kit de 10) | R$ 3,31 el kit de 10 (comprueba si es autorroscante) |
| [Tornillo autorroscante de 3 × 8 mm para plástico, de cabeza redonda](https://lista.mercadolivre.com.br/parafuso-auto-atarraxante-3x8-cabeca-panela) | 2 / 1 kit de 10 | Fija la carcasa trasera por debajo, directamente al piso del chasis. | R$ 3–8 (el kit de 10) | no verificado |
| [Brida de nylon de 3,6 mm de ancho (150 a 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 paquete de 100 | Fijan el convertidor, el UBEC y la placa de protección a las cunas del chasis. | R$ 8–20 (paquete) | no verificado |
| [Cinta de espuma de doble cara](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | cerca de 15 cm / 1 rollo | Sujeta el portapilas al piso y el cargador a la mesita trasera. | R$ 8–20 (rollo) | no verificado |
| [Pegamento instantáneo (cianoacrilato)](https://lista.mercadolivre.com.br/cola-instantanea-cianoacrilato) | unas gotas / 1 tubo pequeño | Pega las piezas de color que no llevan tornillos ni encajan a presión. | R$ 5–20 (el tubo) | no verificado |

### Filamento

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Filamento PETG de 1,75 mm, rollo de 1 kg](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 271 g, en 2 colores sugeridos (grafito y amarillo) / 1 rollo de cualquier color (o un rollo de cada color sugerido) | Las piezas que soportan fuerza: chasis, bandejas, horquilla, cuna, placa de la cabeza y cubierta de la esfera. El color es solo una sugerencia; el material no: mantén el PETG. | R$ 90–150 (rollo) | no verificado |
| [Filamento PLA de 1,75 mm, rollo de 1 kg](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 739 g, en 7 colores sugeridos (verde, azul, crema, blanco, gris, verde oscuro y negro) / 1 rollo de 1 kg, si todo es de un solo color; para los colores sugeridos, 1 rollo del color del cuerpo y sobrantes o rollos pequeños de los demás | Las piezas que visten al robot: cuerpo, cabeza, ojos y piezas de color. El color es solo una sugerencia. | R$ 80–140 (rollo) | no verificado |

### Herramientas y materiales de soldadura (si no los tienes)

| Artículo (el nombre abre la búsqueda) | Usa / comprar | Para qué sirve | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Cautín de 30 a 60 W, de preferencia con ajuste de temperatura](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Suelda los cables de alimentación e instala los 13 insertos en caliente. | R$ 40–150 (cada uno) | no verificado |
| [Punta de cautín para inserto M3 (opcional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guía el inserto recto dentro del agujero. La punta cónica común también sirve: apoya la punta dentro del inserto y empuja despacio. | R$ 15–40 (cada uno) | no verificado |
| [Estaño para soldar con fundente, de 0,8 a 1 mm (tubo pequeño)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | menos de 1 m / 1 tubo | Todos los empalmes de cables y los pads de soldadura de la placa de protección. | R$ 8–25 (tubo) | no verificado |
| [Tubo termorretráctil de 2 a 3 mm y de 5 a 6 mm (o cinta aislante)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | alrededor de 30 cm de cada uno / 1 m de cada uno | Aísla cada empalme de cable. No puede quedar ningún metal expuesto cerca de la batería. | R$ 5–20 (total) | no verificado |
| [Multímetro](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Ajusta el convertidor a 5,1 V, comprueba los 6 V del UBEC y la polaridad antes de conectar las placas. | R$ 40–100 (cada uno) | no verificado |
| [Destornillador plano de precisión de 2 mm y destornillador Phillips pequeño (PH0 o PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | El destornillador plano gira el tornillo de ajuste del LM2596 y aprieta los bornes. El Phillips aprieta los tornillos M2 de los horns, el tornillo central de los servos y los tornillos Phillips. | R$ 10–35 (cada uno) | no verificado |
| [Alicates de corte pequeños](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Corta los cables, las patas de las resistencias y el sobrante de las bridas. | R$ 15–40 (cada uno) | no verificado |
| [Pelacables (o un cúter, con cuidado)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Pela las puntas de los cables sin cortar los hilitos de cobre. | R$ 15–45 (cada uno) | no verificado |
| [Pinzas de punta fina](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Sujeta las resistencias al soldar y permite alcanzar los conectores dentro del cuerpo. | R$ 5–20 (cada uno) | no verificado |
| [Llave Allen larga de 2,5 mm (vástago de 50 mm o más)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Aprieta los tornillos Allen M3, incluidos los 2 del cuerpo, detrás de los muslos. | R$ 8–25 (cada uno) | no verificado |
| [Calibrador](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Comprueba las medidas marcadas como NC antes de imprimir. | R$ 25–80 (cada uno) | no verificado |
| [Fuente USB-C de 5 V y 3 A (15 W), con cable USB-C](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Carga el paquete por el puerto USB-C del cargador y conecta la Raspberry Pi en la mesa de trabajo, en el preparativo 4. Para la Pi 4, debe entregar 5 V y 3 A: muchos cargadores de celular no alcanzan esa potencia (lee la etiqueta). La fuente oficial de la Raspberry Pi 4, de 5,1 V y 3 A, es la opción segura. | R$ 25–80 (cada uno) | no verificado |
| [Cable USB A-B (el de impresora) y una computadora con Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Graba el sketch en el Arduino Uno, con su bandeja fuera del robot. | R$ 8–25 (cada uno) | no verificado |
| [Lector de tarjetas microSD (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Graba el sistema del Raspberry Pi en la tarjeta desde tu computadora. Muchas laptops ya tienen una ranura. | R$ 10–30 (cada uno) | no verificado |
<!-- /GERADO -->

## Tornillos e insertos, contados

13 insertos M3 en caliente: 2 en los postes del chasis, 2 en el resalte de la esfera de apoyo, 3 en el borde superior del cuerpo, 3 en el cráneo, 2 en la parte superior de la cuna del tilt y 1 en la horquilla del cuello.

<!-- GERADO:parafusos -->
| Dónde está | Cant. | Tornillo | Dónde se enrosca |
|---|---|---|---|
| Motores de las ruedas en las paredes del chasis | 4 | M3 × 30 + tuerca | tuerca en el lado interior de la pared |
| Servo de pan en la plataforma | 4 | M3 × 12 + tuerca | tuerca por debajo de la plataforma |
| Servo de tilt en la cuna | 4 | M3 × 12 + tuerca | tuerca por dentro de la cuna |
| Pivote de la cuna, en el lado izquierdo de la horquilla | 1 | M3 × 10 | inserto en la horquilla |
| Driver L298N en el travesaño | 4 | M3 × 8 | directo en el plástico (orificio de 2,7 mm) |
| Cubierta de la esfera de apoyo (por debajo) | 2 | M3 × 8 | inserto roscado en el chasis |
| Cuerpo en los postes del chasis (detrás de los muslos) | 2 | M3 × 16 | inserto roscado en los postes del chasis |
| Collar en el cuerpo (por encima) | 3 | M3 × 10 | inserto roscado en el borde del cuerpo |
| Carcasa trasera (por debajo) | 2 | tornillo autorroscante de 3 × 8 mm, cabeza abombada | directamente en el piso del chasis (agujero de 2,7 mm) |
| Arduino Uno en la bandeja | 4 | M3 × 8 | directo en el plástico (orificio de 2,7 mm) |
| Raspberry Pi en la bandeja | 4 | M2,5 × 8 autorroscante | directo en el plástico (agujero de 2,2 mm) |
| Placa de la cabeza en el cráneo (por debajo) | 3 | M3 × 12 | inserto roscado en el cráneo |
| Placa de la cabeza en la columna de la cuna (por encima) | 2 | M3 × 10 | inserto roscado en la parte superior de la cuna |
| Horn redondo de los 2 servos MG996R | 8 | M2 × 8 autorroscante | en los orificios del horn |
| Microservos de la boca y de los 2 brazos | 6 | tornillo que viene con el servo | directo en el plástico (agujero de 1,7 mm) |
<!-- /GERADO -->

El tornillo central, los tornillos del horn y los anillos de goma vienen en el kit de cada servo. Las longitudes de los tornillos
M3 se calcularon a partir de las medidas del modelo y aún no se han comprobado con las piezas impresas.

## Filamento

Gramos por color, sumando las 34 piezas (estimación por volumen, sin laminador). El color es una sugerencia; el material no:
mantén PETG donde dice PETG. El mínimo son 2 rollos de 1 kg, uno de PETG y uno de PLA, de cualquier color. En los colores
sugeridos, el color del cuerpo consume la mayor parte de un rollo y los demás consumen pocos gramos cada uno: los restos de filamento
son suficientes. Las dos líneas de filamento están en la lista de arriba.

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

## Fase 2 (opcional por ahora)

Nada de esto es necesario para imprimir, montar y conectar. Los ojos ya están diseñados para los sensores: la pupila derecha tiene el
orificio para la lente de la cámara y la pupila izquierda tiene la ventana del sensor de distancia.

<!-- GERADO:fase2 -->
| Artículo (el nombre abre la búsqueda) | Cant. | Dónde está | Precio estimado | Visto en tienda |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide (placa de 25 × 24 mm)](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3-wide) | 1 | Detrás de la pupila del ojo derecho: la placa entra por detrás del ojo y toca el iris, en 4 orificios para tornillos M2. La lente mira a través del orificio de 8,5 mm de la pupila. NC: orificios de la placa y altura de la lente. | R$ 200–400 | no verificado |
| [Cable plano de cámara de 50 cm (para Raspberry Pi 5, el cable de 22 a 15 vías)](https://lista.mercadolivre.com.br/cabo-flat-camera-raspberry-pi-50cm) | 1 | Sale por la ventana trasera del ojo, baja por la cara plana de la columna del cuello y por la ranura de la horquilla, hasta Raspberry Pi. Deja una curva en S dentro del collar: la cabeza gira 60° hacia cada lado. NC: longitud: los 50 cm son una estimación según el modelo. | R$ 15–45 | no verificado |
| [Tornillo autorroscante M2 × 6 mm](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Sujeta la cámara en los 4 agujeros del iris derecho. | R$ 3–8 | R$ 5,98 el kit de 10 |
| [Sensor de distancia ToF VL53L1X (placa de aproximadamente 25 × 11 mm)](https://lista.mercadolivre.com.br/sensor-distancia-vl53l1x) | 3 | 1 detrás de la pupila del ojo izquierdo (ventana de 6 mm): mide la distancia de lo que mira la cabeza. 2 a los lados, detrás de las 2 manchas verde oscuro de los flancos (ventana de 6 mm en el centro de cada mancha). NC: tamaño de la placa y ubicación de la ventana: mide antes de imprimir el ojo izquierdo. | R$ 30–110 | R$ 102,32 (VL53L1X, hasta 4 m); R$ 31,81 (VL53L0X, hasta 2 m) |
| [Micrófono I2S INMP441](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Detrás de las 2 narinas: cada narina es un agujero de sonido de 2 mm y la placa redonda encaja por dentro. NC: placa redonda de 14 mm de diámetro: mide la tuya. | R$ 15–55 | R$ 54,26 |
| [Altavoz de 40 mm, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Encima de la placa de la cabeza, orientado hacia abajo. El sonido sale por la ranura de la boca y el espacio del cuello: no queda ninguna rejilla a la vista. NC: diámetro y profundidad. | R$ 7–20 | no verificado |
| [Amplificador de audio pequeño (PAM8403 o MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | Aún no tiene una ubicación modelada: va suelto dentro del cuerpo, con cinta de doble cara. | R$ 5–35 | R$ 5,47 a R$ 11,34 (PAM8403) |
| [Sensor de movimiento IMU MPU-6050](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | Este robot aún no tiene una ubicación modelada: cinta de doble cara en el piso del chasis, cerca del eje de las ruedas. | R$ 15–35 | R$ 34,09 |
<!-- /GERADO -->

El LiDAR no está en esta lista: en este robot, la cabeza cubre toda la vuelta que necesita.

## Glosario

<!-- GERADO:glossario -->
- **GPIO:** La fila de 40 pines del Raspberry Pi, donde se conectan los cables de alimentación y señal. En esta guía, «pin 32» es la posición del pin en la fila; «GPIO12» es el nombre de la señal que sale por él.
- **UBEC:** Convertidor pequeño, usado en aeromodelos, que reduce el voltaje de la batería a un valor fijo. Aquí, 6 V para los servos.
- **BMS:** Placa de protección de la batería de litio. Desconecta la batería antes de que se descargue demasiado, se sobrecargue o entre en cortocircuito.
- **2S:** Dos celdas de litio conectadas en serie, una después de la otra. Los voltajes se suman: de 6 V (vacía) a 8,4 V (cargada).
- **Horn:** La pieza de plástico que encaja en el eje del servo y gira con él. Los 2 servos grandes usan el horn redondo, en forma de disco; los microservos, el de 1 brazo.
- **Inserto en caliente:** Buje de latón con rosca interna. Se introduce en el orificio del plástico con el cautín y se convierte en una rosca metálica.
- **NC:** No confirmado: una medida tomada de un anuncio de una tienda que aún no se ha verificado con la pieza en mano.
- **Laminador:** El programa que convierte el archivo 3D en las capas que imprime la impresora. El de Bambu Lab se llama Bambu Studio.
- **SSH:** Forma de usar el Raspberry Pi por la red: escribes los comandos en la terminal de tu computadora y se ejecutan en el Pi, sin conectarle teclado ni monitor.
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
- **Puente H (L298N):** Placa que enciende, apaga e invierte los motores de las ruedas por orden del Arduino. También se llama driver de motores.
- **Microservo:** Servo pequeño, de 9 gramos (SG90 o MG90S). Aquí abre la boca y mueve los brazos.
- **Pan y tilt:** Los dos movimientos de la cabeza: pan es girar hacia los lados, tilt es inclinar hacia arriba y hacia abajo.
- **ToF:** Sensor que mide la distancia por el tiempo que tarda la luz en ir y volver. Es de la fase 2.
- **Soportes (de impresión):** Material adicional que el laminador imprime debajo de una parte de la pieza que se imprimiría en el aire. Lo retiras después de imprimir. Los soportes de árbol son los que se ramifican y se retiran más fácilmente.
<!-- /GERADO -->

Cómo conectar todo lo que aparece en esta lista: [LIGACAO.es.md](LIGACAO.es.md). Cómo imprimir: [IMPRIMIR.es.md](IMPRIMIR.es.md).
