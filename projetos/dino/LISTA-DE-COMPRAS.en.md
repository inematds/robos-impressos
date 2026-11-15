# Dinosaur shopping list

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Everything you need to buy to assemble the dinosaur in phase 1: the body assembled and wired. The program comes later, in phase 2.

Page with the same list: https://inematds.github.io/robos-impressos/guia/en/dino/#comprar

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
- Nothing has been printed or assembled yet. The wiring has not been bench-tested: it was put together from the component datasheets.
- Six parts need supports: skull, body, rear shell, jaw, neck fork, and tilt cradle. The supports go inside or underneath, away from the face, but no one has removed them from a real part yet.
- The 3MF files for the build plates have never been opened in Bambu Studio. If one won’t open, use the STL files.
- The on/off switch is rated for 3 A, and based on the component specifications, normal use comes close to that (between 2.5 and 3 A with the wheels moving, the head and arms moving). The 3 A fuse protects the switch and may blow when the robot is working hard. A larger switch would require changing the part’s cutout: that’s a project item still to be addressed.
- The Raspberry Pi gets 5.1 V through the 5 V pins because its USB-C port sits against the rack wall in the tray. This is a common connection, but it has not been tested in this robot: swapped wires or the wrong voltage on these pins can burn out the Pi. Measure before connecting it.
- There is about 17 mm above the Raspberry Pi up to the tray above (model measurement, unconfirmed). A standard Dupont connector is about 16.5 mm tall and may not fit. Plan B: solder the wires to a low-profile female pin header, with the wires coming out the side.
- The test coupon does not check the MG996R servo window. Check the servo in the tilt cradle, which comes off one of the first build plates, before starting the long prints.
- The fuse holder, terminal block, and 3 serial resistors have no modeled place: they sit loose inside the body, insulated with heat-shrink tubing.
- Cable lengths (head servos, extensions, and jumpers) were estimated from the model. The head rotates and tilts, pulling these cables: leave slack and check both ends before closing it up.
- The micro servo horn for each arm is not in the 3D model: the assembly test does not prove the body lowers with it in place. Install the horn pointing back and up, and only rotate it afterward.
- The Arduino sits crosswise in the tray, with its USB port facing sideways: to reflash the program, you need to pull out the tray.
- Measurements marked NC come from store listings. Measure your part before printing the section that touches it.
- The micro servo spline has steps of about 17° (typical value, unconfirmed): the mouth horn and arm horns may not land exactly at the 90° position. Choose the closest tooth; fine-tune in the program during phase 2.
- Heat: the Raspberry Pi is enclosed in the body, which is made of PLA and has no ventilation openings. PLA softens near 60 °C, and the Pi slows down starting at 80 °C. Attach the heatsinks and measure with the `vcgencmd measure_temp` command. If it goes above 70 °C, make ventilation holes in the rear shell.
<!-- /GERADO -->

## How much it costs

<!-- GERADO:custo -->
- Phase 1 parts (excluding filament and tools): **R$ 889–1953**.
- Starting from scratch (parts, 2 rolls of filament, and all tools): **R$ 1273–2918**.
- Just the 2 rolls of filament (1 PETG and 1 PLA): R$ 170–290.
- If you already have the Arduino Uno, subtract: R$ 43–90.
- If you already have all the tools, subtract: R$ 214–675.
<!-- /GERADO -->

## Phase 1: what to buy

<!-- GERADO:compras -->
### Brain and movement

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | The robot's brain. It goes in the bottom tray, inside the body. In phase 1, you only connect and configure it; if you want to delay this purchase, you can assemble everything without it and leave the tray empty. The Pi 5 also works, with 1 camera and no USB accessories: the converter delivers about 2 A. | R$ 450–800 (each) | not verified |
| [32 GB class 10 microSD card](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Raspberry Pi operating system. | R$ 25–50 (each) | not verified |
| [Adhesive heatsink kit for Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | The Raspberry Pi is enclosed inside the body, which is made of PLA and has no ventilation openings. The heatsinks attached to the chips lower the temperature. NC: heatsink height: there is about 17 mm above the Raspberry Pi up to the tray above. | R$ 8–25 (kit) | not verified |
| [180° MG996R servo (positional, not continuous rotation)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | One turns the head from side to side (pan), and the other tilts it (tilt). NC: thickness and holes in the tabs, diameter and thickness of the round horn. | R$ 30–75 (each) | R$ 70.45 |
| [9 g, 180° micro servo: MG90S or SG90 (position control, not continuous rotation)](https://lista.mercadolivre.com.br/micro-servo-mg90s-180-graus) | 3 / 3 | Opens the mouth (1) and moves the arms (2). Choose the MG90S if you can; it has metal gears. NC: flange thickness, distance between the holes, and size of 1 arm's horn. | R$ 15–45 (each) | R$ 17.71 (SG90) to R$ 41.84 (MG90S) |
| [30 cm servo extension (3-wire male-to-female extension cable)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 2 / 2 | One carries the mouth servo cable to the Arduino; the other is for the tilt servo if its cable does not reach. NC: factory cable length for each servo (15 to 30 cm): measure the route before closing it up. | R$ 5–15 (each) | not verified |
| [3 to 6 V DC motor with a 1:48 reduction gearbox (yellow TT motor)](https://lista.mercadolivre.com.br/motor-dc-3-6v-caixa-de-reducao-48-1) | 2 / 2 | Drive: one for each wheel. If it comes without wires, solder 2 wires to each one in prep step 1. NC: distance between the 2 rear holes (the slot accepts 12.3 to 17.6 mm) and case thickness (18.6 mm in the model). | R$ 7–20 (each) | R$ 9.01 |
| [65 mm wheel for TT motor](https://lista.mercadolivre.com.br/roda-65mm-motor-dc-arduino) | 2 / 2 | Press-fits onto the motor shaft. Many stores sell the motor + wheel as a pair. NC: diameter (65 mm in the model; wheels range from 64 to 68 mm) and width (up to 27 mm). | R$ 5–15 (each) | R$ 20.54 for a kit with 1 motor and 1 64 mm wheel |
| [16 mm steel ball (or a measured marble)](https://lista.mercadolivre.com.br/esfera-de-aco-16mm) | 1 / 1 | Third support for the robot, at the back, under the root of the tail. It spins freely in a socket, held in place by a cover. NC: diameter: the socket is for 16 mm; marbles range from 14 to 25 mm. | R$ 3–10 (each) | not verified |
| [L298N motor driver (dual H-bridge)](https://lista.mercadolivre.com.br/driver-ponte-h-l298n) | 1 / 1 | Powers and reverses the 2 wheel motors at the Arduino's command. NC: distance between the 4 holes (37 mm in the model); if they don't line up, secure it with double-sided tape. | R$ 20–35 (each) | R$ 21.51 to R$ 29.18 |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (you may already have) | 1 / 1 | Controls the 5 servos and 2 motors. It goes on the upper tray, inside the body. | R$ 43–90 (each) | R$ 43.28 to R$ 89.95 |
| [Sensor Shield V5.0 for Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | It fits on top of the Uno and provides the servos' 3-pin connectors, with power supplied separately through the blue screw terminal. The Arduino receives 5.1 V through the + pin of the shield's COM connector. NC: According to the store photo, the COM connector has 4 upright pins labeled TX, RX, −, and +; some shield versions have the pins in a different place. Measure before connecting. | R$ 11–35 (each) | R$ 18.13 |
| [1 kΩ resistor, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pack of 10 | Serial voltage divider: lowers the Arduino's 5 V to the 3.3 V the Raspberry Pi accepts. All 3 are secured to the terminal block. | R$ 1–5 (pack) | not verified |

### Power

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [3.7 V lithium-ion 18650 battery (loose cell)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | 2S pack: 7.4 V nominal (8.4 V fully charged). Buy two identical, new batteries from a reputable brand. | R$ 13–45 (each) | R$ 26.08 for the kit with 2 |
| [Holder for 2 side-by-side 18650 batteries, with wires](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Holds the 2 cells in series. It sits on the chassis floor and comes out at the rear. NC: the chassis bay accepts up to 78 × 41 × 22 mm. | R$ 5–15 (each) | R$ 6.22 |
| [Inline fuse holder for a 5 × 20 mm glass fuse, with a 3 A slow-blow fuse (marked T3A or T3.15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (and 1 spare fuse) | On the positive wire, just after the battery holder. It is 3 A because the switch is rated for 3 A: during an overload, the fuse blows before the switch heats up. It is slow-blow because servo startup and capacitor charging cause peaks lasting a fraction of a second, which would blow a fast fuse without a fault. No modeled spot for it: it hangs loose on the wire. | R$ 4–12 (set) | not verified |
| [2S 10 A BMS protection board (model 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Cuts off deep discharge, overcharging, and short circuits. Solder it to the battery wires and secure it with double-sided tape. NC: printed names of the solder pads. On the board from the store checked, only the back has labels: B+, B1 (middle), B−, and C−. From the photo, C− is the negative output (the role of P− on other boards), and the positive output is B+ itself; this is based on reading the photo, so check with a multimeter. | R$ 8–20 (each) | not verified |
| [USB-C 2S/3S balance charger (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Charges both cells without opening the robot. It sits on a small platform in the chassis, at the back; the plug goes through a slot under the root of the tail. NC: height of the USB-C port at the 13 × 7 mm slot under the root of the tail. | R$ 15–30 (each) | R$ 17.90 |
| [Adjustable LM2596 step-down converter (blue board, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Steps the pack voltage down to 5 V for the Raspberry Pi and Arduino. Adjust it to 5.1 V with a multimeter BEFORE connecting any board. The board handles about 2 A continuously without a heatsink. The XL4015 will not work here: it needs at least 8 V. NC: 2 A continuous is the usual rating for this board; we have no datasheet to confirm it. | R$ 8–20 (each) | R$ 10.22 |
| [6 V 3 A UBEC (Hobbywing UBEC 3A 2-6S or equivalent)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Supplies 6 V to the 5 servos, separate from the boards' 5 V. | R$ 25–60 (each) | not verified |
| [1000 µF 16 V electrolytic capacitor](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | On the servos' 6 V screw terminal: handles the startup current spike. | R$ 1–4 (each) | R$ 2.33 |
| [KCD11-101 3 A rocker switch (13.5 × 9 mm cutout)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Turns the power on and off. It fits underneath the floor, between the legs. NC: panel thickness accepted by the latch. | R$ 3–8 (each) | R$ 3.74 to R$ 5.40 (KCD1 models; check the cutout) |
| [Flexible 22 AWG wire (0.33 mm²): red, black, and a third color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | about 2 m of red, 2 m of black, and 30 cm of yellow wire / 3 m of red, 3 m of black, 1 m of yellow wire | All the power wiring and the wires for the 2 motors. The yellow wire is the 3rd wire, from the middle point of the pack. | R$ 12–30 (total) | R$ 22.40 (5 m two-color) |
| [12-way terminal block, for thin wire](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 3 ways (terminals 1, 2, and 3) / 1 12-way terminal block; cut off a piece with 3 ways | It stays inside the body and avoids soldering with the robot assembled. Terminal 1: the 5.1 V. Terminal 2: the negative. Terminal 3: the blue serial wire and the divider resistors. The wires from the converter go in one side; the wires to the Raspberry Pi, Arduino, and driver go out the other. There is no modeled spot for it: it sits loose. | R$ 3–10 (block) | not verified |
| [20 cm female-to-female Dupont jumper wires (40-piece kit)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-20cm) | 16 wires / 1 kit of 40 | Raspberry Pi power and serial, Arduino power, and the 6 motor driver signals. | R$ 8–20 (the kit) | not verified |

### Fasteners

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [M3 brass threaded insert (for 4.0 mm hole, up to 5.7 mm long)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 13 / 1 pack of 20 or more | The metal threads in the parts. The screw table shows where each one goes. | R$ 15–40 (pack) | not verified |
| [M3 × 8 mm screw, Allen cylindrical head](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 10 / 2 kits of 10 | Motor driver, Arduino, and support ball cover. | R$ 3–8 (kit of 10) | R$ 6.14 for a kit of 10 (head type not specified) |
| [M3 × 10 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 6 / 1 kit of 10 | Collar, head plate, and cradle pin. | R$ 3–8 (kit of 10) | R$ 3.55 for a kit of 10 (Phillips) |
| [M3 × 12 mm screw](https://lista.mercadolivre.com.br/parafuso-m3x12) | 11 / 2 kits of 10 | 4 for each MG996R servo, with nuts, and 3 that secure the head plate to the skull. | R$ 3–8 (kit of 10) | not verified |
| [M3 × 16 mm screw](https://lista.mercadolivre.com.br/parafuso-m3x16) | 2 / 1 kit of 10 | Secures the body to the chassis posts, behind the thighs. | R$ 3–8 (the 10-piece kit) | not verified |
| [M3 × 30 mm screw](https://lista.mercadolivre.com.br/parafuso-m3x30) | 4 / 1 kit of 10 | Secures the 2 wheel motors. With M3 × 25, the nut catches only 1.4 mm of thread: the motor is 18.6 mm plus a 5 mm wall. | R$ 3–10 (the 10-piece kit) | R$ 3.44 for a kit of 10 M3 × 25 screws (the 30 mm one wasn’t found) |
| [M3 hex nut](https://lista.mercadolivre.com.br/porca-sextavada-m3) | 12 / 1 kit of 20 or more | For the screws on the 2 MG996R servos and the 2 motors. | R$ 3–10 (the kit) | not verified |
| [M2.5 × 8 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2.5x8-auto-atarraxante) | 4 / 1 kit | Secures the Raspberry Pi to the tray. | R$ 5–15 (the kit) | not verified |
| [M2 × 8 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit of 10 | 4 for each round horn: secure the fork to the pan servo and the cradle to the tilt servo. NC: diameter of the round horn holes. | R$ 3–8 (kit of 10) | R$ 3.31 for a kit of 10 (check whether they are self-tapping) |
| [3 × 8 mm self-tapping screw for plastic, pan head](https://lista.mercadolivre.com.br/parafuso-auto-atarraxante-3x8-cabeca-panela) | 2 / 1 kit of 10 | Secures the rear shell from underneath, directly to the chassis floor. | R$ 3–8 (the 10-piece kit) | not verified |
| [3.6 mm wide nylon cable tie (150 to 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 pack of 100 | Secure the converter, UBEC, and protection board to the chassis cradles. | R$ 8–20 (pack) | not verified |
| [Double-sided foam tape](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | about 15 cm / 1 roll | Secures the battery holder to the floor and the charger to the rear tray. | R$ 8–20 (roll) | not verified |
| [Instant glue (cyanoacrylate)](https://lista.mercadolivre.com.br/cola-instantanea-cianoacrilato) | a few drops / 1 small tube | Glues the colored parts that have no screws or press fit. | R$ 5–20 (the tube) | not verified |

### Filament

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [1.75 mm PETG filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 271 g, in 2 suggested colors (graphite and yellow) / 1 spool in any color (or one spool in each suggested color) | The parts that bear loads: chassis, trays, fork, cradle, head plate, and support ball cover. The color is only a suggestion; the material isn’t: use PETG. | R$ 90–150 (roll) | not verified |
| [1.75 mm PLA filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 739 g, in 7 suggested colors (green, blue, cream, white, gray, dark green, and black) / 1 kg spool if everything is one color; for the suggested colors, 1 spool in the body color plus leftovers or small spools of the others | The parts that dress the robot: body, head, eyes, and colored parts. The color is only a suggestion. | R$ 80–140 (roll) | not verified |

### Tools and soldering supplies (if you don’t have them)

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [30 to 60 W soldering iron, preferably with temperature control](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solder the power wires and heat-set the 13 inserts. | R$ 40–150 (each) | not verified |
| [Soldering iron tip for M3 inserts (optional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guides the insert straight into the hole. The standard conical tip also works: place it inside the insert and push slowly. | R$ 15–40 (each) | not verified |
| [Rosin-core solder, 0.8 to 1 mm (small spool)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | less than 1 m / 1 spool | All wire splices and solder pads on the protection board. | R$ 8–25 (spool) | not verified |
| [2 to 3 mm and 5 to 6 mm heat-shrink tubing (or electrical tape)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | about 30 cm of each / 1 m of each | Insulate every wire splice. No metal should be exposed near the battery. | R$ 5–20 (total) | not verified |
| [Multimeter](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Set the converter to 5.1 V, check the UBEC’s 6 V output and the polarity before connecting the boards. | R$ 40–100 (each) | not verified |
| [2 mm precision flathead screwdriver and small Phillips screwdriver (PH0 or PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | Use the flathead to turn the LM2596 adjustment screw and tighten the screw terminals. Use the Phillips to tighten the M2 horn screws, the servos’ centre screws, and the Phillips-head screws. | R$ 10–35 (each) | not verified |
| [Small wire cutters](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Cuts the wires, resistor leads, and excess from the cable ties. | R$ 15–40 (each) | not verified |
| [Wire stripper (or a utility knife, carefully)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Strips the insulation from the wire ends without cutting the copper strands. | R$ 15–45 (each) | not verified |
| [Fine-tip tweezers](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Holds resistors while you solder and reaches the connectors inside the body. | R$ 5–20 (each) | not verified |
| [Long 2.5 mm Allen key (shaft 50 mm or longer)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Tightens the M3 Allen screws, including the 2 on the body behind the thighs. | R$ 8–25 (each) | not verified |
| [Caliper](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Checks the dimensions marked NC before printing. | R$ 25–80 (each) | not verified |
| [5 V, 3 A (15 W) USB-C power supply with USB-C cable](https://lista.mercadolivre.com.br/fonte-usb-c-5v-3a-raspberry-pi-4) | 1 / 1 | Charge the pack through the charger’s USB-C port and power the Raspberry Pi on the workbench in prep step 4. For the Pi 4, it must provide 5 V and 3 A: many phone chargers fall short (check the label). The official 5.1 V, 3 A Raspberry Pi 4 power supply is the safe choice. | R$ 25–80 (each) | not verified |
| [USB A-B cable (the printer cable) and a computer with the Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Upload the sketch to the Arduino Uno with its tray outside the robot. | R$ 8–25 (each) | not verified |
| [microSD card reader (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Writes the Raspberry Pi system to the card from your computer. Many laptops already have a slot. | R$ 10–30 (each) | not verified |
<!-- /GERADO -->

## Counted screws and threaded inserts

13 M3 heat-set inserts: 2 in the chassis posts, 2 in the support ball boss, 3 along the top edge of the body, 3 in the skull, 2 on top of the tilt cradle and 1 in the neck fork.

<!-- GERADO:parafusos -->
| Where it goes | Qty | Screw | What it screws into |
|---|---|---|---|
| Wheel motors on the chassis walls | 4 | M3 × 30 + nut | nut on the inside of the wall |
| Pan servo on the deck | 4 | M3 × 12 + nut | nut underneath the deck |
| Tilt servo in the cradle | 4 | M3 × 12 + nut | nut inside the cradle |
| Cradle pin, on the left side of the fork | 1 | M3 × 10 | insert in the fork |
| L298N motor driver on the crossbar | 4 | M3 × 8 | directly into the plastic (2.7 mm hole) |
| Support ball cover (underneath) | 2 | M3 × 8 | threaded insert in the chassis |
| Body on the chassis posts (behind the thighs) | 2 | M3 × 16 | threaded insert in the chassis posts |
| Collar on the body (on top) | 3 | M3 × 10 | threaded insert at the edge of the body |
| Rear shell (underneath) | 2 | 3 × 8 mm self-tapping screw, pan head | directly into the chassis floor (2.7 mm hole) |
| Arduino Uno on the tray | 4 | M3 × 8 | directly into the plastic (2.7 mm hole) |
| Raspberry Pi on the tray | 4 | M2.5 × 8 self-tapping screw | directly into the plastic (2.2 mm hole) |
| Head plate on the skull (underneath) | 3 | M3 × 12 | threaded insert in the skull |
| Head plate on the cradle column (on top) | 2 | M3 × 10 | threaded insert at the top of the cradle |
| Round servo horn for the 2 MG996R servos | 8 | M2 × 8 self-tapping screw | in the horn holes |
| Micro servos for the mouth and the 2 arms | 6 | screw included with the servo | directly into the plastic (1.7 mm hole) |
<!-- /GERADO -->

The centre screw, servo horn screws and rubber rings come in each servo kit. The M3 screw lengths
were taken from the model dimensions and have not yet been checked against the printed parts.

## Filament

Grams per color, totaling the 34 parts (volume estimate, without a slicer). Color is a suggestion; material is not:
keep PETG where PETG is specified. The minimum is 2 rolls of 1 kg, one PETG and one PLA, in any color. With the
suggested colors, the body color uses most of one roll and the other colors use only a few grams each: filament
leftovers will do. The two filament lines are in the list above.

<!-- GERADO:filamento -->
| Material and color | Filament (g) | Time (h) |
|---|---|---|
| PETG yellow | 28 | 1.2 |
| PETG graphite | 243 | 9.4 |
| PLA blue | 42 | 1.9 |
| PLA white | 28 | 1.2 |
| PLA gray | 15 | 0.6 |
| PLA cream | 28 | 1.5 |
| PLA black | 4 | 0.4 |
| PLA green | 618 | 23.8 |
| PLA dark green | 4 | 0.2 |
| **Total** | **1010** | **40.2** |
<!-- /GERADO -->

## Phase 2 (optional for now)

None of this is needed to print, assemble and wire the robot. The eyes are already made for the sensors: the right pupil has the
camera lens hole and the left pupil has the distance sensor window.

<!-- GERADO:fase2 -->
| Item (the name opens a search) | Qty | Where it goes | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 Wide (25 × 24 mm board)](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3-wide) | 1 | Behind the right eye’s pupil: the board fits behind the eye and touches the iris, using 4 holes for M2 screws. The lens looks through the pupil’s 8.5 mm hole. NC: board holes and lens height. | R$ 200–400 | not verified |
| [50 cm camera ribbon cable (for Raspberry Pi 5, the 22-to-15-pin cable)](https://lista.mercadolivre.com.br/cabo-flat-camera-raspberry-pi-50cm) | 1 | It exits through the rear window of the eye, runs down the flat face of the neck column and through the fork slot, to the Raspberry Pi. Leave an S-shaped loop inside the collar: the head turns 60° to each side. NC: length: 50 cm is an estimate based on the model. | R$ 15–45 | not verified |
| [M2 × 6 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Attach the camera to the 4 holes in the right iris. | R$ 3–8 | R$ 5.98 for a kit of 10 |
| [VL53L1X ToF distance sensor (board about 25 × 11 mm)](https://lista.mercadolivre.com.br/sensor-distancia-vl53l1x) | 3 | 1 behind the left eye pupil (6 mm window): measures the distance to what the head is looking at. 2 on the sides, behind the 2 dark green flank spots (6 mm window in the centre of each spot). NC: board size and window location: measure before printing the left eye. | R$ 30–110 | R$ 102.32 (VL53L1X, up to 4 m); R$ 31.81 (VL53L0X, up to 2 m) |
| [I2S INMP441 microphone](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Behind the 2 nostrils: each nostril is a 2 mm sound hole, and the round board fits inside. NC: 14 mm diameter round board: measure yours. | R$ 15–55 | R$ 54.26 |
| [40 mm speaker, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | On top of the head plate, facing down. Sound comes out through the mouth gap and the neck opening: no grille is visible. NC: diameter and depth. | R$ 7–20 | not verified |
| [Small audio amplifier (PAM8403 or MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | No modeled location yet: it sits loose inside the body, held with double-sided tape. | R$ 5–35 | R$ 5.47 to R$ 11.34 (PAM8403) |
| [MPU-6050 IMU motion sensor](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | No modeled location on this robot: use double-sided tape on the chassis floor, near the wheel axle. | R$ 15–35 | R$ 34.09 |
<!-- /GERADO -->

The LiDAR is not on this list: on this robot, the head covers the entire area it needs.

## Glossary

<!-- GERADO:glossario -->
- **GPIO:** The Raspberry Pi's 40-pin row, where the power and signal wires connect. In this guide, "pin 32" is the pin's position in the row; "GPIO12" is the name of the signal that comes out of it.
- **UBEC:** A small converter used in model aircraft that lowers the battery voltage to a fixed value. Here, 6 V for the servos.
- **BMS:** Lithium battery protection board. It disconnects the battery before it discharges too much, overcharges, or shorts out.
- **2S:** Two lithium cells connected in series, one after the other. Their voltages add up: from 6 V (empty) to 8.4 V (full).
- **Horn:** The plastic piece that fits onto the servo shaft and turns with it. The 2 large servos use the round, disc-shaped horn; the micro servos use the 1-arm horn.
- **Heat-set threaded insert:** A brass bushing with an internal thread. It goes into the hole in the plastic when pushed in with a soldering iron, creating a metal thread.
- **NC:** Unconfirmed: a measurement from a store listing that has not yet been checked against the part in hand.
- **Slicer:** The software that turns the 3D file into the layers the printer prints. Bambu Lab's slicer is called Bambu Studio.
- **SSH:** A way to use the Raspberry Pi over the network: you type commands in your computer's terminal, and they run on the Pi without connecting a keyboard or monitor to it.
- **UART (serial):** A simple data connection: one wire to send (TX) and one to receive (RX). The Raspberry Pi sends commands to the Arduino through it.
- **SEL jumper:** A small plastic cap over 2 Sensor Shield pins, next to the blue screw terminal, marked SEL. When installed, it connects the Arduino's 5 V to the servo connectors. When removed, the servos receive only the power supplied through the blue screw terminal.
- **Screw terminal:** A screw connector: the wire goes into the hole and the screw tightens it. On the Sensor Shield, it is the blue block marked GND and VCC.
- **Sketch:** The name Arduino gives to a program. You open the file in Arduino IDE and upload it to the board with the USB cable.
- **Shield:** A board that fits on top of the Arduino, onto its pins, and adds connectors. Here, the Sensor Shield provides the servo connectors.
- **AWG:** A measure of wire thickness. The lower the number, the thicker the wire: 20 AWG is thicker than 22 AWG.
- **GND:** The circuit’s negative, also called ground. All the robot’s negative connections are connected to each other.
- **Dupont:** A thin wire that comes with a plug-in connector on each end, sized to fit the pins on the boards. Also called a jumper.
- **Step-down:** A converter that lowers the voltage. Here, the LM2596 lowers the battery voltage to 5.1 V.
- **Heat-shrink tubing:** A small plastic tube that shrinks with heat. Slip it over the solder joint and heat it: it tightens and insulates.
- **H-bridge (L298N):** Board that turns the wheel motors on and off and reverses them at the Arduino's command. It's also called a motor driver.
- **Micro servo:** Small, 9-gram servo (SG90 or MG90S). Here, it opens the mouth and moves the arms.
- **Pan and tilt:** The head's two movements: pan means turning side to side; tilt means angling up and down.
- **ToF:** Sensor that measures distance by timing how long light takes to travel out and back. It's part of phase 2.
- **Supports (for printing):** Extra material the slicer prints under a part that would otherwise start in midair. You remove it after printing. Tree supports grow like thin branches and are easier to remove.
<!-- /GERADO -->

How to wire everything on this list: [LIGACAO.en.md](LIGACAO.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
