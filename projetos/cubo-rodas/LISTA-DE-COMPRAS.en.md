# Shopping list for the square robot on wheels

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Everything you need to buy to assemble the square robot on wheels in phase 1: the body assembled and wired. The program
comes later, in phase 2.

Robot page: https://inematds.github.io/robos-impressos/guia/en/cubo-rodas/

## How to read the list

- **Uses / buy:** the first number is what the robot uses; the second is what you buy, because screws and threaded inserts
  come in kits.
- **Prices are in reais (R$)** and the links open Mercado Livre Brazil search results. The name of each item is the link.
- **Estimated price** is a range, not a quote. It gives you a rough idea of the cost.
- **Seen at store** is the price listed on 14/11/2026 on the public pages of usinainfo.com.br. Where it says
  "not checked," the range is only a reference. Mercado Livre prices were not checked.
- **NC** = unconfirmed measurement. The model uses the most common value for that component. Measure your part with calipers
  before printing the part that touches it.

## Risks before buying

What has not been tested yet. Read before spending.

<!-- GERADO:riscos -->
- Nothing has been printed or assembled yet. The electrical section of this page has not been bench-tested: it was based on the component datasheets.
- The 3MF files for the build plates have never been opened in Bambu Studio. If one won’t open, use the STL files.
- The 3 A switch is the weakest point in the electrical system. Based on the component specs, the robot draws about 2 A during normal use and about 6.5 A in the worst case (both wheels stalled, both servos pushing, and the Raspberry Pi at full load). The 3 A fuse protects the switch, but it may blow if the robot pushes against an obstacle. Replacing it with a larger switch means changing the 13.5 × 9 mm cutout in the base.
- The screen’s 2 cables, HDMI and USB, are not included in the 3D model. The model leaves about 22 mm below the Raspberry Pi and about 30 mm beside its USB ports: the straight cables that come with the screen will not fit. This is the main fit risk for this robot. Check with the parts in hand before closing the head.
- The charger comes set up for 2 cells. Converting it to 3 requires removing a tiny resistor and closing a solder jumper. If that doesn’t work, the 3 cells can be removed through the battery hatch and charged in a standard 18650 charger.
- The labels printed on the solder pads of the 3-cell protection board and on the charger’s 2 middle solder pads could not be read. Check each cell junction with a multimeter (about 4 V and about 8 V) before soldering.
- The position of the motor’s 6 holes around the shaft is an unconfirmed measurement. If they don’t line up, the part to reprint is the flange, a small disk. Check with the motor in hand before printing the base.
- The Raspberry Pi gets 5.1 V through pins 2 and 4, bypassing the USB-C input protection. The wrong voltage or a reversed wire there will burn out the Pi. Measure at the terminal block before connecting it.
- The test coupon does not check the MG996R servo window or the M5 screw thread. Check the servo window on the head frame (plate 01). The M5 thread is on the fork arm (plate 04). Check both before starting the long prints.
- To reprogram the Arduino after assembling the robot, loosen the 4 bottom screws and lift the torso with the neck and head.
- The fuse holder, terminal block, and 3 serial resistors have no modeled location: they stay loose and insulated with heat-shrink tubing. Each motor cable is about 14 cm long and may not reach the motor driver; if it falls short, splice it.
- The Sensor Shield’s A0 and A1 connectors, used by the second wire from each encoder, are not clearly visible in the store photo. If your board doesn’t have these pins, leave the 2 green wires insulated: the phase 2 program can count rotations using only the yellow wire.
- Measurements marked NC come from store listings. Measure your part before printing the section that touches it.
- The path for the 8 wires through the fork hole and the slot in the bottom of the head shell has never been tested with printed parts.
- Balance: the checker shows that the robot does not tip over when stationary, with the head in any position. While moving, the calculation is an estimate: it can brake at up to about 3 m/s² without tipping forward, and the phase 2 program should use no more than half that. The highest step it can climb is about 8 mm.
- Heat: the Raspberry Pi 4 is enclosed in the head, which is made of PLA and has no ventilation opening. PLA softens near 60 °C, and the Pi throttles starting at 80 °C. Attach the heatsinks and measure with the `vcgencmd measure_temp` command. If it goes above 70 °C, print the head shell in PETG or open ventilation holes at the back.
<!-- /GERADO -->

## How much it costs

<!-- GERADO:custo -->
- Phase 1 parts (excluding filament and tools): **R$ 1353–2944**.
- Starting from scratch (parts, 2 rolls of filament, and all tools): **R$ 1737–3909**.
- Just the 2 rolls of filament (1 PETG and 1 PLA): R$ 170–290.
- If you already have the Arduino Uno, subtract: R$ 43–90.
- If you already have all the tools, subtract: R$ 214–675.
<!-- /GERADO -->

The most expensive items are the Raspberry Pi, the 5-inch screen, and the 2 motors with encoders. None of their prices
were checked at a store: the price ranges are only estimates.

## Phase 1: what to buy

<!-- GERADO:compras -->
### Brain, screen, and servos

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | The robot’s brain. It sits inside the head, behind the screen. The Pi 5 also works. | R$ 450–800 (each) | not verified |
| [32 GB class 10 microSD card](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Raspberry Pi operating system. | R$ 25–50 (each) | not verified |
| [5" HDMI screen, 800 × 480 (Waveshare 5inch HDMI LCD (B), 121 × 89.5 mm board)](https://lista.mercadolivre.com.br/display-5-polegadas-hdmi-800x480-raspberry-pi-waveshare) | 1 / 1 | The robot’s face. It does not plug into the Raspberry Pi pins: it is fastened with 4 screws to the face panel posts and connects to the Pi with an HDMI cable and a USB cable. The posts are designed for the 121 × 89.5 mm board, with 4 holes spaced 115 × 84 mm apart. NC: assembly thickness (14 mm in the model), diameter of the 4 holes, and position of the HDMI and USB ports on the board. | R$ 250–480 (each) | not verified |
| [Short flat HDMI cable (10 to 20 cm): angled micro-HDMI on one end, standard HDMI on the other](https://lista.mercadolivre.com.br/cabo-hdmi-flat-fpv-micro-hdmi-angulo-20cm) | 1 / 1 | Connects the screen to the Raspberry Pi 4, which has a micro-HDMI output. The cable included with the screen is straight and long: the model leaves about 22 mm below the Pi, so it will not fit. NC: The screen cables are not included in the 3D model: check the space with the parts in hand before closing the head. | R$ 25–70 (each) | not verified |
| [Short USB cable (15 to 20 cm): angled USB-A on one end, micro-USB on the other](https://lista.mercadolivre.com.br/cabo-usb-a-angulo-90-micro-usb-20cm) | 1 / 1 | Carries power from the Raspberry Pi to the screen. The model leaves about 30 mm between the Pi’s USB ports and the head wall: a standard straight plug will not fit. NC: screen USB port type (micro-USB in the manufacturer’s kit); the cables are not included in the 3D model. | R$ 10–30 (each) | not verified |
| [180° MG996R servo (positional, not continuous rotation)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | One rotates the neck (pan), the other tilts the head (tilt). The servo kit must include the round horn (disk). NC: thickness and holes in the tabs, diameter and thickness of the round horn. | R$ 30–75 (each) | R$ 70.45 |
| [30 cm servo extension (3-wire male-to-female extension cable)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Carries the tilt servo cable from the head through the neck to the shield on the deck, with enough slack for the head to turn. NC: factory servo cable length (usually 30 cm). | R$ 5–15 (each) | not verified |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (you may already have) | 1 / 1 | Controls the 2 servos and 2 motors and reads the encoders. It sits on the deck, on 4 raised mounts. | R$ 43–90 (each) | R$ 43.28 to R$ 89.95 |
| [Sensor Shield V5.0 for Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | Fits on top of the Uno and provides 3-pin connectors for the servos, motor driver, and encoders, with separate power through the blue screw terminal. The Arduino gets 5.1 V through the + pin of the shield’s COM connector. NC: Based on the store photo, the COM connector has 4 upright pins labeled TX, RX, −, and +, and the digital connectors have 3 pins (G, V, S). The A0 and A1 connectors, used by the encoders, are not clearly visible in the photo. Some shield versions have the pins in different places. Measure before connecting. | R$ 11–35 (each) | R$ 18.13 |
| [1 kΩ resistor, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pack of 10 | Serial voltage divider: lowers the Arduino’s 5 V to the 3.3 V accepted by the Raspberry Pi. The 3 resistors are secured to the terminal block on the deck. | R$ 1–5 (pack) | not verified |
| [Adhesive heatsink kit for Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | The Raspberry Pi is enclosed inside the head, which is made of PLA and has no ventilation opening. The heatsinks attached to the chips lower the temperature. NC: heatsink height: it must fit in the about 20 mm between the Pi and the screen. | R$ 8–25 (kit) | not verified |

### Wheels and motors

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [12 V JGB37-520 motor with encoder, 107 rpm (1:56 reduction), 6 mm D-shaped shaft](https://lista.mercadolivre.com.br/motor-jgb37-520-12v-encoder-107rpm) | 2 / 2 | Drive: one motor per wheel. Each motor comes with a 6-wire cable: 2 for the motor and 4 for the encoder, the sensor that counts wheel rotations. Choose the 12 V, 107 rpm version. NC: position of the 6 M3 holes around the shaft, which is 7 mm off-center, and thread depth (3.5 to 4 mm). | R$ 60–150 (each) | not verified |
| [85 × 38 mm wheel with a 12 mm hex socket](https://lista.mercadolivre.com.br/roda-85mm-sextavado-12mm-robo) | 2 / 2 | The 2 front wheels. The 42.5 mm radius lets the robot cross low door thresholds. | R$ 30–60 (each) | R$ 38.87 each |
| [12 mm hex adapter for a 6 mm shaft (wheel coupling, with set screw)](https://lista.mercadolivre.com.br/adaptador-sextavado-12mm-eixo-6mm-roda) | 2 / 2 | Attaches the wheel to the motor shaft. NC: length (20 mm in the model; the common brass one is about 18 mm). | R$ 10–30 (each) | not verified |
| [40 mm table tennis ball](https://lista.mercadolivre.com.br/bola-tenis-de-mesa-40mm) | 1 / 1 pack | Rear support: it rolls freely in a well in the base, held in place by the cover. It limits the step the robot can cross: about 8 mm. NC: balls marked 40+ measure 40.0 to 40.6 mm; the well is 41.2 mm. | R$ 5–20 (pack) | not verified |
| [L298N motor driver (dual H-bridge module, 2 A per channel)](https://lista.mercadolivre.com.br/driver-motor-l298n-ponte-h) | 1 / 1 | Turns the 2 motors on and off and reverses them. It sits on the deck, on 4 raised mounts. It drops about 2 V across the motors: with the pack at 11 V, they get about 9 V, which this robot can handle. NC: distance between the 4 holes (37 mm in the model) and the printed names of the pins and jumpers. | R$ 18–35 (each) | R$ 21.51 to R$ 29.18 |

### Power

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [3.7 V lithium-ion 18650 battery (loose cell)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 3 / 3 | 3S pack: 11.1 V nominal (12.6 V fully charged). Buy three identical, new batteries from a known brand. | R$ 13–45 (each) | R$ 26.08 for the kit with 2 |
| [Holder for 3 side-by-side 18650 batteries, with wires](https://lista.mercadolivre.com.br/suporte-3-baterias-18650) | 1 / 1 | Holds the 3 cells in series. It is attached to the battery hatch, which comes out from underneath the robot with 4 screws. NC: the battery hatch cradle was designed for 75 × 61 × 20 mm. | R$ 6–18 (each) | R$ 7.80 |
| [Inline fuse holder for a 5 × 20 mm glass fuse, with a 3 A slow-blow fuse (marked T3A or T3.15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (and 1 spare fuse) | On the positive wire, right after the battery holder. It is 3 A because the switch is rated for 3 A: in an overload, the fuse opens before the switch heats up. It is slow-blow because motor and servo startup and the capacitor charging cause spikes lasting a fraction of a second, which would blow a fast-acting fuse even when there is no fault. No mount was modeled: it hangs loose on the wire. | R$ 4–12 (set) | not verified |
| [3S 10 A BMS protection board (HX-3S-FL10 model, 50 × 15 mm)](https://lista.mercadolivre.com.br/bms-3s-10a-18650-hx-3s-fl10) | 1 / 1 | Cuts off deep discharge, overcharge, and short circuits. It is soldered to the battery wires and held to the base floor with double-sided tape. This board does not balance the cells: the charger does that. NC: printed names of the solder pads (not shown on the store page). They are usually 0V, 4.2V, 8.4V, and 12.6V on the cell side and P+ and P− on the output side. Check with a multimeter. | R$ 15–30 (each) | R$ 21.60 |
| [USB-C 2S/3S balance charger (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Charges the pack without opening the robot. It comes ready for 2 cells. For 3 cells, you need to remove a tiny resistor from the board and close a jumper with solder, as shown in the figure on the store page. In 3-cell mode, it uses 4 wires: positive, negative, and the 2 cell junctions. NC: printed names of the 2 cell-junction pads (not legible in the store photo) and size of the USB-C opening in the rear window (9.2 × 3.4 mm). | R$ 15–30 (each) | R$ 17.90 |
| [Adjustable XL4015 step-down converter (5 A)](https://lista.mercadolivre.com.br/modulo-step-down-xl4015-5a) | 1 / 1 | Lowers the pack voltage to the 5.1 V for the Raspberry Pi, Arduino, motor driver, and encoders. Adjust it to 5.1 V with a multimeter BEFORE connecting any board. It requires at least 8 V input, and the 3-cell pack always stays above that. | R$ 12–30 (each) | R$ 17.82 |
| [6 V 3 A UBEC (Hobbywing UBEC 3A 2-6S or equivalent)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Powers the 2 servos at 6 V, separate from the Pi. Set its jumper to 6 V. | R$ 25–60 (each) | not verified |
| [1000 µF 16 V electrolytic capacitor](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | On the servos' 6 V screw terminal: handles the startup current spike. | R$ 1–4 (each) | R$ 2.33 |
| [KCD11-101 3 A rocker switch (13.5 × 9 mm cutout)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Turns the power on and off. It press-fits into the rear wall of the base, from the outside. The datasheet rates it at 3 A at 250 V~ and 6 A at 125 V~, with no DC rating: that is why the fuse is 3 A. It is the weakest point in this robot's electrical system (see the risks). NC: panel thickness accepted by the latch. | R$ 3–8 (each) | R$ 3.74 to R$ 5.40 (KCD1 models; check the cutout) |
| [Flexible 22 AWG wire (0.33 mm²): red, black, and a third color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | about 50 cm of red, 30 cm of black, and 80 cm of yellow wire / 2 m of red, 2 m of black, 1 m of yellow | The thin power wires: the 4 cell-junction wires (yellow), the charger connections, and the driver's 5.1 V supply. | R$ 12–30 (total) | R$ 22.40 (5 m two-color) |
| [Flexible 20 AWG wire (0.5 mm²), red and black](https://lista.mercadolivre.com.br/fio-flexivel-20awg-vermelho-preto) | about 1.1 m of each color / 2 m of each color | The wires that carry more current: from the switch and protection board to the terminal block, from the block to the converter and motor driver, and the pair of 5.1 V wires that goes up the neck to the Raspberry Pi. Thicker wire loses less voltage along the way; with thin wire, the Pi reports undervoltage. | R$ 8–25 (total) | not verified |
| [12-way terminal block, for thin wire](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 5 terminals (terminals 1 to 5) / 1 12-terminal block; cut off a piece with 5 terminals | It sits on the deck and keeps you from having to solder with the robot assembled. Terminal 1: 5.1 V. Terminal 2: negative. Terminal 3: the blue serial wire and the voltage divider resistors. Terminal 4: pack positive, after the switch. Terminal 5: pack negative. There is no modeled spot for it: it stays loose. | R$ 3–10 (block) | not verified |
| [40 cm female-to-female Dupont jumpers (40-piece kit)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-40cm) | 16 wires / 1 kit of 40 | There are 16: 3 for serial (green, blue, and black, from the Raspberry Pi to the deck), 2 that carry 5.1 V and negative from the terminal block to the Arduino, 1 cut in half for the divider, 2 cut in half for Raspberry Pi power, 6 for the motor driver, and 2 cut in half for the encoders. The serial wires fit tightly: if you run short, splice a jumper segment onto the end at the deck, with solder and heat-shrink tubing, during prep step 3. | R$ 10–25 (kit) | not verified |

### Fasteners

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [M3 brass threaded insert (for 4.0 mm hole, up to 5.7 mm long)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 31 / 2 packs of 20 (or 1 of 50) | The metal threads for the parts: 8 in the motor walls, 4 for the battery hatch, and 4 for the ball cover (all in the base), 4 in the torso columns, 4 in the face panel posts, 4 in the frame columns, and 3 in the fork. | R$ 15–40 (pack) | not verified |
| [M3 × 6 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x6) | 12 / 2 kits of 10 | 6 for each motor: they attach the motor to the flange, with the head in the recess. NC: bottom of the motor thread: 3.5 to 4 mm. After the flange, 4 mm of screw remains. If it hits the bottom before tightening, switch to M3 × 5. | R$ 3–8 (kit of 10) | not verified |
| [M3 × 8 mm screw, Allen cylindrical head](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 24 / 3 packs of 10 | 4 for the battery hatch, 4 for the ball cover, 4 for the Arduino, 4 for the motor driver, 4 for the face panel, and 4 for the head shell. | R$ 3–8 (kit of 10) | R$ 6.14 for a kit of 10 (head type not specified) |
| [M3 × 10 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 8 / 1 kit of 10 | 4 for each motor flange, in the base wall inserts. They are hidden behind the wheel. | R$ 3–8 (kit of 10) | R$ 3.55 for a kit of 10 (Phillips) |
| [M3 × 12 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x12) | 12 / 2 kits of 10 | 4 for each MG996R servo, screwed directly into the plastic (2.7 mm hole), and 4 that go in from under the base, pass through the deck, and thread into the torso inserts. These 4 must be Allen socket head screws: the head sits at the bottom of a 68 mm hole. | R$ 3–8 (kit of 10) | not verified |
| [M3 × 50 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x50) | 3 / 3 (sold individually) | Neck tie rods: they go inside the torso, through the gear, pass through the tube, and thread into the fork inserts. | R$ 1–4 (each) | not verified |
| [M5 × 16 mm screw](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit of 10 (or 1 loose piece) | Tilt pin: passes through the side of the frame and threads into the fork arm. The head tilts around it. | R$ 3–8 (kit of 10) | R$ 6.04 for a kit of 10 (Phillips) |
| [M2.5 × 12 mm screw with M2.5 nut](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 screws and 4 nuts / 1 kit | Secures the Raspberry Pi to the frame, with the 4 printed spacers in between. | R$ 5–15 (kit) | not verified |
| [M2.5 × 6 mm screw](https://lista.mercadolivre.com.br/parafuso-m2.5x6) | 4 / 1 kit | Attaches the 5-inch screen to the 4 posts on the face panel, screwed directly into the plastic. NC: diameter of the holes in the screen board. | R$ 5–15 (kit) | not verified |
| [M2 × 8 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit of 10 | 4 on each round horn: attach the gear to the pan servo and the fork to the tilt servo. NC: diameter of the round horn holes. | R$ 3–8 (kit of 10) | R$ 3.31 for a kit of 10 (check whether they are self-tapping) |
| [3.6 mm wide nylon cable tie (150 to 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 4 / 1 pack of 100 | One in each cradle: 5 V converter, UBEC, charger, and battery holder, in the battery hatch. | R$ 8–20 (pack) | not verified |
| [Double-sided foam tape](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | about 5 cm / 1 roll | Attaches the protection board (BMS) to the base floor. | R$ 8–20 (roll) | not verified |

### Filament

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [1.75 mm PETG filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 823 g, in 4 suggested colors (yellow, white, graphite, and silver) / 1 spool in any color (or 4 spools, one in each suggested color) | The parts that take the load: base, battery hatch, ball cover, flanges, deck, torso, neck, gears, fork, and head frame. The color is only a suggestion; the material is not: keep PETG. One 1 kg spool is enough with little to spare: this is an estimate without a slicer, and if a large part fails partway through, you may run out of filament. | R$ 90–150 (roll) | not verified |
| [1.75 mm PLA filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 320 g, in 3 suggested colors (white, gray, and black) / 1 spool in any color (or 3 spools, one in each suggested color) | The parts that only cover the robot: head shell, face panel, spacers and test coupon. The color is just a suggestion. | R$ 80–140 (roll) | not verified |

### Tools and soldering supplies (if you don’t have them)

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [30 to 60 W soldering iron, preferably with temperature control](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solders the power wires and seats the 31 inserts with heat. With a fine tip, it also closes the charger's solder jumper. | R$ 40–150 (each) | not verified |
| [Soldering iron tip for M3 inserts (optional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guides the insert straight into the hole. The standard conical tip also works: place it inside the insert and push slowly. | R$ 15–40 (each) | not verified |
| [Rosin-core solder, 0.8 to 1 mm (small spool)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | less than 1 m / 1 spool | All wire splices and solder pads on the protection board. | R$ 8–25 (spool) | not verified |
| [2 to 3 mm and 5 to 6 mm heat-shrink tubing (or electrical tape)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | about 30 cm of each / 1 m of each | Insulate every wire splice. No metal should be exposed near the battery. | R$ 5–20 (total) | not verified |
| [Multimeter](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Set the converter to 5.1 V, check the UBEC's 6 V, the cell junctions (about 4 V and 8 V), and polarity before connecting the boards. | R$ 40–100 (each) | not verified |
| [2 mm precision flathead screwdriver and small Phillips screwdriver (PH0 or PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | The flathead turns the XL4015 adjustment screw and tightens the terminals. The Phillips tightens the M2 horn screws, the servos' center screw, and the Phillips head screws. | R$ 10–35 (each) | not verified |
| [Small wire cutters](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Cuts the wires, resistor leads, and excess cable ties. | R$ 15–40 (each) | not verified |
| [Wire stripper (or a utility knife, carefully)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Removes the insulation from the ends of 20 and 22 AWG wires without cutting the copper strands. | R$ 15–45 (each) | not verified |
| [Fine-tip tweezers](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Pulls the wire ends through the slot at the bottom of the head, holds the resistors while soldering, and removes the charger's tiny resistor. | R$ 5–20 (each) | not verified |
| [Long 2.5 mm Allen key (shaft 80 mm or longer)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa-haste-100mm) | 1 / 1 | Tightens the 4 screws that go in from under the base, at the bottom of 68 mm holes, and the 3 neck tie rods. | R$ 8–25 (each) | not verified |
| [Caliper](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Checks the dimensions marked NC before printing. | R$ 25–80 (each) | not verified |
| [5 V, 3 A (15 W) USB-C power supply with USB-C cable](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Charges the pack through the rear USB-C port and powers the Raspberry Pi in prep step 4. For the Pi 4, it must deliver 5 V and 3 A: many phone chargers can’t supply that much (check the label). The official Raspberry Pi 4 power supply, rated at 5.1 V and 3 A, is the safe option. | R$ 25–80 (each) | not verified |
| [USB A-B cable (the printer cable) and a computer with the Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Upload the sketch to the Arduino Uno before closing the robot. | R$ 8–25 (each) | not verified |
| [microSD card reader (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Writes the Raspberry Pi system to the card from your computer. Many laptops already have a slot. | R$ 10–30 (each) | not verified |
<!-- /GERADO -->

## Counted screws and threaded inserts

31 hot M3 threaded inserts: 8 in the motor walls, 4 for the battery hatch and 4 for the ball cover (all 16 are in the base), 4 in
the torso columns, 4 in the face panel pillars, 4 in the head frame columns, and 3 in the fork.

<!-- GERADO:parafusos -->
| Where it goes | Qty | Screw | What it screws into |
|---|---|---|---|
| Motor on the flange (6 per motor) | 12 | M3 × 6 Allen | motor's own threads |
| Flange on the base wall (4 per side) | 8 | M3 × 10 Allen | threaded insert in the base wall |
| Battery hatch (underneath) | 4 | M3 × 8 | threaded insert in the base floor |
| Ball cover (underneath) | 4 | M3 × 8 | threaded insert in the base floor, around the well |
| Arduino Uno (deck) | 4 | M3 × 8 | directly into the plastic (2.7 mm hole) |
| L298N driver (deck) | 4 | M3 × 8 | directly into the plastic (2.7 mm hole) |
| Pan servo (deck) | 4 | M3 × 12 | directly into the plastic (2.7 mm hole) |
| Base + deck + torso (underneath, at the bottom of the 4 posts) | 4 | M3 × 12 Allen | threaded insert in the torso column |
| Tilt servo (head frame) | 4 | M3 × 12 | directly into the plastic (2.7 mm hole) |
| 5-inch screen (face panel pillars) | 4 | M2.5 × 6 | directly into the plastic (2.2 mm hole) |
| Face panel (behind the frame) | 4 | M3 × 8 | threaded insert in the panel posts |
| Head cup (back wall) | 4 | M3 × 8 | threaded insert in the frame columns |
| Neck tie rods (inside the torso) | 3 | M3 × 50 Allen | insert in the fork |
| Tilt pin | 1 | M5 × 16 | directly into the fork's plastic (4.4 mm hole) |
| Raspberry Pi | 4 | M2.5 × 12 + nut | nut behind the crossbar |
| Round horn for the 2 servos | 8 | M2 × 8 self-tapping screw | in the horn holes |
<!-- /GERADO -->

The center horn screws and the servos' rubber rings come in the MG996R kit. The lock screw and the screw at the end of
the hex adapter come with the adapter.

## Filament

Grams per color, adding up the 19 parts (volume estimate, without a slicer). The color is a suggestion; the material is not:
keep PETG where it says PETG. The minimum is 2 rolls of 1 kg each, one PETG and one PLA, any color. Almost all the PETG
will be used in the robot: if a long print fails, you may run short. With the 7 suggested colors, you need 7 rolls, 4 PETG and 3
PLA, and a lot of filament will be left over. The two filament lines are in the list above.

<!-- GERADO:filamento -->
| Material and color | Filament (g) | Time (h) |
|---|---|---|
| PETG yellow | 108 | 4.1 |
| PETG white | 236 | 8.7 |
| PETG graphite | 454 | 17.1 |
| PETG silver | 25 | 1.1 |
| PLA white | 248 | 9.3 |
| PLA gray | 15 | 0.9 |
| PLA black | 57 | 2.2 |
| **Total** | **1143** | **43.4** |
<!-- /GERADO -->

## Phase 2 (optional for now)

None of this is needed for printing, assembling, and wiring. The parts already have spaces, holes, and cable routes, and
none of these holes are visible from the front: the “Where it goes” column says where each one is hidden.

<!-- GERADO:fase2 -->
| Item (the name opens a search) | Qty | Where it goes | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (25 × 24 mm board) with ribbon cable](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Behind the face panel, in the 8 mm hole above the screen. 4 posts with holes for M2 screws. NC: lens holes and height. | R$ 180–350 | not verified |
| [M2 × 6 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Secures the camera to the 4 posts. | R$ 3–8 | R$ 5.98 for a kit of 10 |
| [I2S INMP441 microphone](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Inside the head, over the 2 mm holes underneath it. They are not visible from the front or side. NC: microphone mount not modeled yet. | R$ 15–55 | R$ 54.26 |
| [40 mm speaker, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Slides into the 2 rails on the back wall of the torso, against the row of vertical slots. Visible only from behind. NC: diameter and depth. | R$ 7–20 | not verified |
| [Small audio amplifier (PAM8403 or MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | No modeled spot yet: it sits loose on the deck, held with double-sided tape. | R$ 5–35 | R$ 5.47 to R$ 11.34 (PAM8403) |
| [MPU-6050 IMU motion sensor](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | At the universal spot on the deck (pair of M3 holes 20 mm apart), near the wheel axle. | R$ 15–35 | R$ 34.09 |
| [LiDAR LD19](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | At the top of the head, the only spot with 360° of clearance: 3 blind holes inside and a blind recess for the cable. The 0.8 mm shell is drilled only when the sensor is installed; until then, nothing is visible from the outside. With it, the robot is 341 mm tall. NC: position of the 3 holes in the sensor body. | R$ 400–900 | not verified |
| [VL53L1X ToF distance sensor (small board)](https://lista.mercadolivre.com.br/sensor-vl53l1x-tof) | 3 | On the inside of the base wall, 10 mm below the top edge: one at the front and one on each side. Each point has 2 blind holes for an M2.5 screw and, between them, a blind window: the outside wall is smooth, with 0.8 mm of plastic in front of the window. During installation, pierce this skin from the inside, in the center of the window, with a nail or a hot needle: the drill won’t fit inside the base. The small hole marks the center on the outside; widen it from the outside with a 6 mm drill bit. After that, 3 visible 6 mm holes remain in the base. NC: board size (25 × 10.7 mm) and distance between the holes. | R$ 40–110 | R$ 102.32 |
| [Drop sensor (infrared reflective, such as TCRT5000)](https://lista.mercadolivre.com.br/sensor-reflexivo-infravermelho-tcrt5000) | 1 | In a 14 × 6 mm window in the base floor, at the front, facing the ground, with a pair of M3 holes 20 mm apart. Visible only from underneath. | R$ 5–15 | R$ 7.92 |
<!-- /GERADO -->

## Glossary

<!-- GERADO:glossario -->
- **GPIO:** The Raspberry Pi’s 40-pin row, where the power and signal wires connect. In this guide, "pin 32" is the pin’s position in the row; "GPIO12" is the name of the signal that comes out through it.
- **UBEC:** A small converter used in model aircraft that lowers the battery voltage to a fixed value. Here, 6 V for the servos.
- **BMS:** Lithium battery protection board. It disconnects the battery before it discharges too much, overcharges, or shorts out.
- **3S:** Three lithium cells connected in series, one after another. Their voltages add up: from 9 V (empty) to 12.6 V (full).
- **Cell junction (battery pack):** The point where one cell connects to the next. A 3-cell pack has 2 junctions. The protection board and charger measure each cell through them.
- **Horn:** The plastic part that fits onto the servo shaft and turns with it. This robot uses the round, disk-shaped horn.
- **Heat-set threaded insert:** A brass bushing with an internal thread. It goes into the hole in the plastic when pushed in with a soldering iron, creating a metal thread.
- **NC:** Unconfirmed: a measurement from a store listing that has not yet been checked against the part in hand.
- **Slicer:** The software that turns the 3D file into the layers the printer prints. Bambu Lab's slicer is called Bambu Studio.
- **SSH:** A way to use the Raspberry Pi over the network: you type commands in your computer's terminal, and they run on the Pi without connecting a keyboard or monitor to it.
- **UART (serial):** A simple data connection: one wire to send (TX) and one to receive (RX). The Raspberry Pi sends commands to the Arduino through it.
- **Motor driver (H-bridge):** Board that connects the motors to the battery and reverses their direction when the Arduino sends a command. Here, it’s the L298N.
- **Encoder:** Sensor attached to the back of the motor that counts rotations. The program uses it to know how far each wheel has moved.
- **SEL jumper:** A small plastic cap over 2 Sensor Shield pins, next to the blue screw terminal, marked SEL. When installed, it connects the Arduino's 5 V to the servo connectors. When removed, the servos receive only the power supplied through the blue screw terminal.
- **Screw terminal:** A screw connector: the wire goes into the hole and the screw tightens it. On the Sensor Shield, it is the blue block marked GND and VCC.
- **Sketch:** The name Arduino gives to a program. You open the file in Arduino IDE and upload it to the board with the USB cable.
- **Shield:** Board that plugs into the Arduino’s pins and adds connectors. Here, the Sensor Shield provides connectors for the servos, motor driver, and encoders.
- **AWG:** A measure of wire thickness. The lower the number, the thicker the wire: 20 AWG is thicker than 22 AWG.
- **GND:** The circuit’s negative, also called ground. All the robot’s negative connections are connected to each other.
- **Dupont:** A thin wire that comes with a plug-in connector on each end, sized to fit the pins on the boards. Also called a jumper.
- **Step-down:** Converter that lowers the voltage. Here, the XL4015 lowers the battery voltage to 5.1 V.
- **Heat-shrink tubing:** A small plastic tube that shrinks with heat. Slip it over the solder joint and heat it: it tightens and insulates.
- **Battery hatch:** The cover underneath the base. It holds the battery holder and comes off with 4 screws, without opening the rest of the robot.
- **Flange:** The disk that secures each motor to the base wall. It’s hidden behind the wheel.
- **Deck:** The tray between the base and the torso. It holds the Arduino, motor driver, converters, and the servo that turns the neck.
<!-- /GERADO -->

How to wire everything on this list: [LIGACAO.en.md](LIGACAO.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
