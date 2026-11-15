# Shopping list for the square desktop robot

<!-- GERADO:idiomas -->
[🇧🇷 Português](LISTA-DE-COMPRAS.md) · [🇺🇸 English](LISTA-DE-COMPRAS.en.md) · [🇪🇸 Español](LISTA-DE-COMPRAS.es.md)
<!-- /GERADO -->

Everything you need to buy to build the square desktop robot in phase 1: the body assembled and wired. The program
comes later, in phase 2.

Page with the same list: https://inematds.github.io/robos-impressos/guia/en/cubo/#comprar

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
- The USB-C plug that powers the Raspberry Pi is not in the 3D model. There may not be room for it next to the Pi inside the head.
- Raspberry Pi pins 31 to 34 are under the screen board. The clearance there (17.5 mm in the model) is unconfirmed: if the low-profile connector doesn't fit, the 3 serial wires will have to be soldered.
- The test coupon does not check the MG996R servo window or the M5 screw thread. Check the servo window in the head frame (build plate 01). The M5 thread is in the fork arm (build plate 03). Both are printed before the long print jobs.
- With the Arduino screwed to the base, the USB cable won't fit: there is about 10 mm of clearance to the wall. To reprogram it, you need to remove its 4 screws.
- The fuse holder, terminal block, and 3 serial resistors have no modeled mounting spot: they hang loose on the wires, insulated with heat-shrink tubing.
- Measurements marked NC come from store listings. Measure your part before printing the section that touches it.
- The path for the 8 wires through the fork hole and the slot in the bottom of the head shell has never been tested with printed parts.
- Heat: the Raspberry Pi 4 is enclosed in the head, which is made of PLA and has no ventilation opening. PLA softens near 60 °C, and the Pi throttles starting at 80 °C. Attach the heatsinks and measure with the `vcgencmd measure_temp` command. If it goes above 70 °C, print the head shell in PETG or open ventilation holes at the back.
<!-- /GERADO -->

## How much it costs

<!-- GERADO:custo -->
- Phase 1 parts (excluding filament and tools): **R$ 886–1891**.
- Starting from scratch (parts, 2 rolls of filament, and all tools): **R$ 1270–2856**.
- Just the 2 rolls of filament (1 PETG and 1 PLA): R$ 170–290.
- If you already have the Arduino Uno, subtract: R$ 43–90.
- If you already have all the tools, subtract: R$ 214–675.
<!-- /GERADO -->

## Phase 1: what to buy

<!-- GERADO:compras -->
### Brain, screen, and movement

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi 4 Model B, 4 GB](https://lista.mercadolivre.com.br/raspberry-pi-4-model-b-4gb) | 1 / 1 | The robot’s brain. It sits inside the head, behind the screen. The Pi 5 also works, but only without USB accessories: the converter supplies about 2 A. | R$ 450–800 (each) | not verified |
| [32 GB class 10 microSD card](https://lista.mercadolivre.com.br/cartao-micro-sd-32gb-classe-10) | 1 / 1 | Raspberry Pi operating system. | R$ 25–50 (each) | not verified |
| [3.5" 480 × 320 TFT screen for Raspberry Pi (MPI3501, fits the GPIO)](https://lista.mercadolivre.com.br/display-lcd-tft-3.5-raspberry-pi-mpi3501) | 1 / 1 | The robot's face. Fits directly onto Pi pins 1 to 26, with no screws. NC: assembly thickness (7 mm) and height above the Pi (24.5 mm). | R$ 90–200 (each) | R$ 193.57 |
| [180° MG996R servo (positional, not continuous rotation)](https://lista.mercadolivre.com.br/servo-mg996r-180-graus) | 2 / 2 | One rotates the neck (pan), the other tilts the head (tilt). The servo kit must include the round horn (disk). NC: thickness and holes in the tabs, diameter and thickness of the round horn. | R$ 30–75 (each) | R$ 70.45 |
| [30 cm servo extension (3-wire male-to-female extension cable)](https://lista.mercadolivre.com.br/extensao-servo-30cm) | 1 / 1 | Runs the tilt servo cable from the head, through the neck to the shield in the base, with enough slack for the head to turn. NC: factory servo cable length (usually 30 cm). | R$ 5–15 (each) | not verified |
| [Arduino Uno R3](https://lista.mercadolivre.com.br/arduino-uno-r3) (you may already have) | 1 / 1 | Controls the 2 servos. It sits on the base floor, on 4 raised bosses. | R$ 43–90 (each) | R$ 43.28 to R$ 89.95 |
| [Sensor Shield V5.0 for Arduino](https://lista.mercadolivre.com.br/sensor-shield-v5-arduino) | 1 / 1 | It fits on top of the Uno and provides the servos' 3-pin connectors, with power supplied separately through the blue screw terminal. The Arduino receives 5.1 V through the + pin of the shield's COM connector. NC: According to the store photo, the COM connector has 4 upright pins labeled TX, RX, −, and +; some shield versions have the pins in a different place. Measure before connecting.. | R$ 11–35 (each) | R$ 18.13 |
| [1 kΩ resistor, 1/4 W](https://lista.mercadolivre.com.br/resistor-1k-1-4w) | 3 / 1 pack of 10 | Serial voltage divider: lowers the Arduino’s 5 V to the 3.3 V the Raspberry Pi accepts. The 3 resistors are secured to the terminal block in the base. | R$ 1–5 (pack) | not verified |
| [2-row female pin header, 2.54 mm pitch (2 × 20)](https://lista.mercadolivre.com.br/barra-pinos-femea-2x20-2.54mm) | 1 piece of 2 × 2 / 1 strip | Low-profile connector for Raspberry Pi pins 31 to 34, which are under the display. A regular Dupont wire will not fit upright there. Cut the piece and solder the 3 serial wires to it during prep step 3. NC: clearance between the Pi and the screen board (17.5 mm in the model). | R$ 3–10 (each) | not verified |
| [Adhesive heatsink kit for Raspberry Pi 4](https://lista.mercadolivre.com.br/dissipador-raspberry-pi-4-kit) | 1 kit / 1 kit | The Raspberry Pi is enclosed inside the head, which is made of PLA and has no ventilation opening. The heatsinks attached to the chips lower the temperature. NC: heatsink height: it must fit in the 17.5 mm between the Pi and the display. | R$ 8–25 (kit) | not verified |

### Power

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [3.7 V lithium-ion 18650 battery (loose cell)](https://lista.mercadolivre.com.br/bateria-18650-3.7v) | 2 / 2 | 2S pack: 7.4 V nominal (8.4 V fully charged). Buy two identical, new batteries from a reputable brand. | R$ 13–45 (each) | R$ 26.08 for the kit with 2 |
| [Holder for 2 side-by-side 18650 batteries, with wires](https://lista.mercadolivre.com.br/suporte-2-baterias-18650) | 1 / 1 | Holds the 2 cells in series. Slides into the base cradle and exits through the rear door. NC: the cradle accepts up to 78 × 41 × 22 mm. | R$ 5–15 (each) | R$ 6.22 |
| [Inline fuse holder for a 5 × 20 mm glass fuse, with a 3 A slow-blow fuse (marked T3A or T3.15A)](https://lista.mercadolivre.com.br/porta-fusivel-5x20-fio) | 1 / 1 (and 1 spare fuse) | On the positive wire, just after the battery holder. It is 3 A because the switch is rated for 3 A: during an overload, the fuse blows before the switch heats up. It is slow-blow because servo startup and capacitor charging cause peaks lasting a fraction of a second, which would blow a fast fuse without a fault. No modeled spot for it: it hangs loose on the wire. | R$ 4–12 (set) | not verified |
| [2S 10 A BMS protection board (model 10A2S, ~24 × 11 mm)](https://lista.mercadolivre.com.br/bms-2s-10a-18650) | 1 / 1 | Cuts off deep discharge, overcharging, and short circuits. Solder it to the battery wires and secure it with double-sided tape. NC: printed names of the solder pads. On the board from the store checked, only the back has labels: B+, B1 (middle), B−, and C−. From the photo, C− is the negative output (the role of P− on other boards), and the positive output is B+ itself; this is based on reading the photo, so check with a multimeter. | R$ 8–20 (each) | not verified |
| [USB-C 2S/3S balance charger (LX-USC-V2)](https://lista.mercadolivre.com.br/carregador-usb-c-2s-18650-balanceamento) | 1 / 1 | Charges the pack without opening the robot. The solder pads are B+, BM and B−. BM needs a 3rd wire, soldered to the pack’s middle point (between the two cells). NC: size of the USB-C opening in the rear window (9.2 × 3.4 mm). | R$ 15–30 (each) | R$ 17.90 |
| [Adjustable LM2596 step-down converter (blue board, 3 A)](https://lista.mercadolivre.com.br/modulo-step-down-lm2596) | 1 / 1 | Steps the pack voltage down to 5 V for the Raspberry Pi and Arduino. Adjust it to 5.1 V with a multimeter BEFORE connecting any board. The board handles about 2 A continuously without a heatsink. The XL4015 will not work here: it needs at least 8 V. NC: 2 A continuous is the usual rating for this board; we have no datasheet to confirm it. | R$ 8–20 (each) | R$ 10.22 |
| [6 V 3 A UBEC (Hobbywing UBEC 3A 2-6S or equivalent)](https://lista.mercadolivre.com.br/ubec-3a-5v-6v-hobbywing) | 1 / 1 | Powers the 2 servos at 6 V, separate from the Pi. Set its jumper to 6 V. | R$ 25–60 (each) | not verified |
| [1000 µF 16 V electrolytic capacitor](https://lista.mercadolivre.com.br/capacitor-eletrolitico-1000uf-16v) | 1 / 1 | On the servos' 6 V screw terminal: handles the startup current spike. | R$ 1–4 (each) | R$ 2.33 |
| [KCD11-101 3 A rocker switch (13.5 × 9 mm cutout)](https://lista.mercadolivre.com.br/chave-gangorra-kcd11) | 1 / 1 | Turns the power on and off. Press-fits into the rear wall from the outside. The datasheet rates it at 3 A at 250 V~ and 6 A at 125 V~, with no DC rating: that is why the fuse is 3 A. NC: panel thickness accepted by the latch. | R$ 3–8 (each) | R$ 3.74 to R$ 5.40 (KCD1 models; check the cutout) |
| [USB-C male adapter with screw terminals (2 pins)](https://lista.mercadolivre.com.br/adaptador-usb-c-macho-borne) | 1 / 1 | It carries 5 V from the converter to the Raspberry Pi’s USB-C input (the GPIO 5 V pins are under the screen). The plug isn’t in the 3D model: check that it fits beside the Pi, inside the head. | R$ 8–20 (each) | R$ 13.11 |
| [Flexible 22 AWG wire (0.33 mm²): red, black, and a third color](https://lista.mercadolivre.com.br/fio-flexivel-22awg-vermelho-preto) | about 1 m of red, 1 m of black and 30 cm of yellow / 2 m of red, 2 m of black, 1 m of yellow | The power wiring that stays in the base. The yellow wire is the 3rd wire from the pack’s middle point. | R$ 12–30 (total) | R$ 22.40 (5 m two-color) |
| [Flexible 20 AWG wire (0.5 mm²), red and black](https://lista.mercadolivre.com.br/fio-flexivel-20awg-vermelho-preto) | about 50 cm of each color / 1 m of each color | Only the 5.1 V pair that runs up the neck to the Raspberry Pi. Thicker wire loses less voltage along the way; with thin wire, the Pi reports undervoltage. | R$ 5–15 (total) | not verified |
| [2-way screw terminal block (barrier strip type), for thin wire](https://lista.mercadolivre.com.br/barra-bornes-sindal-12-vias) | 3 terminals / 1 12-way terminal block | It sits in the base and keeps you from soldering with the robot assembled. Terminal 1: the 5.1 V. Terminal 2: the negative. Terminal 3: the blue serial wire and the voltage divider resistors. The wires from the converter go in on one side; on the other side, the wires going up to the Raspberry Pi and the ones going to the Arduino. There’s no modeled spot for it: it sits loose. | R$ 3–10 (block) | not verified |
| [40 cm female-to-female Dupont jumpers (40-piece kit)](https://lista.mercadolivre.com.br/jumper-dupont-femea-femea-40cm) | 6 wires / 1 kit of 40 | There are 6: 3 for serial (green, blue, and black, from the Raspberry Pi to the base), 2 carrying 5.1 V and the negative wire from the terminal block to the Arduino, and 1 cut in half for the divider. The 20 cm wires are too short. The 40 cm wires are a tight fit: according to the model, the pins on the Pi are about 21 cm in a straight line from the shield, plus 15 cm of slack (estimate). If you run short, splice a piece of jumper wire onto the base end with solder and heat-shrink tubing, during prep step 3. | R$ 10–25 (kit) | not verified |

### Fasteners

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [M3 brass threaded insert (for 4.0 mm hole, up to 5.7 mm long)](https://lista.mercadolivre.com.br/inserto-latao-m3-impressao-3d) | 16 / 1 pack of 20 or more | The metal threads in the parts: 4 in the lid, 1 in the door tab, 4 in the face panel pillars, 4 in the frame columns, 3 in the fork. | R$ 15–40 (pack) | not verified |
| [M3 × 8 mm screw, Allen cylindrical head](https://lista.mercadolivre.com.br/parafuso-allen-m3x8) | 13 / 2 kits of 10 | 4 for the Arduino, 4 for the face panel, 4 for the head cup, 1 for the door. | R$ 3–8 (kit of 10) | R$ 6.14 for a kit of 10 (head type not specified) |
| [M3 × 10 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x10) | 4 / 1 kit of 10 | Bottom cover. Must be an Allen socket head screw: the head sits at the bottom of a 44 mm hole. | R$ 3–8 (kit of 10) | R$ 3.55 for a kit of 10 (Phillips) |
| [M3 × 12 mm screw](https://lista.mercadolivre.com.br/parafuso-m3x12) | 8 / 1 kit of 10 | 4 per MG996R servo, threaded directly into the plastic (2.7 mm hole). | R$ 3–8 (kit of 10) | not verified |
| [M3 × 45 mm Allen socket head screw](https://lista.mercadolivre.com.br/parafuso-allen-m3x45) | 3 / 3 (sold individually) | Neck tie rods: they go in under the gear, pass through the tube, and thread into the fork's inserts. | R$ 1–3 (each) | not verified |
| [M5 × 16 mm screw](https://lista.mercadolivre.com.br/parafuso-m5x16) | 1 / 1 kit of 10 (or 1 loose piece) | Tilt pin: passes through the side of the frame and threads into the fork arm. The head tilts around it. | R$ 3–8 (kit of 10) | R$ 6.04 for a kit of 10 (Phillips) |
| [M2.5 × 12 mm screw with M2.5 nut](https://lista.mercadolivre.com.br/parafuso-m2.5x12-porca) | 4 screws and 4 nuts / 1 kit | Secures the Raspberry Pi to the frame, with the 4 printed spacers in between. | R$ 5–15 (kit) | not verified |
| [M2 × 8 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x8-auto-atarraxante) | 8 / 1 kit of 10 | 4 on each round horn: attach the gear to the pan servo and the fork to the tilt servo. NC: diameter of the round horn holes. | R$ 3–8 (kit of 10) | R$ 3.31 for a kit of 10 (check whether they are self-tapping) |
| [3.6 mm wide nylon cable tie (150 to 200 mm)](https://lista.mercadolivre.com.br/abracadeira-nylon-3.6x200) | 3 / 1 pack of 100 | One in each cradle: 5 V converter, UBEC, and charger. | R$ 8–20 (pack) | not verified |
| [Double-sided foam tape](https://lista.mercadolivre.com.br/fita-dupla-face-espuma) | about 5 cm / 1 roll | Secures the protection board (BMS) in the shallow floor pocket. | R$ 8–20 (roll) | not verified |

### Filament

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [1.75 mm PETG filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-petg-1.75mm-1kg) | 463 g, in 3 suggested colors (yellow, graphite and silver) / 1 spool in any color (or 3 spools, one in each suggested color) | The parts that bear loads: base, cover, neck, gears, fork and head frame. The color is just a suggestion; the material is not: use PETG. | R$ 90–150 (roll) | not verified |
| [1.75 mm PLA filament, 1 kg spool](https://lista.mercadolivre.com.br/filamento-pla-1.75mm-1kg) | 272 g, in 3 suggested colors (white, gray and black) / 1 spool in any color (or 3 spools, one in each suggested color) | The parts that only cover the robot: head shell, face panel, spacers and test coupon. The color is just a suggestion. | R$ 80–140 (roll) | not verified |

### Tools and soldering supplies (if you don’t have them)

| Item (the name opens a search) | Uses / buy | What it's for | Estimated price | Seen in store |
|---|---|---|---|---|
| [30 to 60 W soldering iron, preferably with temperature control](https://lista.mercadolivre.com.br/ferro-de-solda-60w-temperatura-ajustavel) | 1 / 1 | Solder the power wires and seat the 16 inserts using heat. | R$ 40–150 (each) | not verified |
| [Soldering iron tip for M3 inserts (optional)](https://lista.mercadolivre.com.br/ponta-ferro-de-solda-inserto-m3) | 1 / 1 | Guides the insert straight into the hole. The standard conical tip also works: place it inside the insert and push slowly. | R$ 15–40 (each) | not verified |
| [Rosin-core solder, 0.8 to 1 mm (small spool)](https://lista.mercadolivre.com.br/estanho-solda-1mm-tubo) | less than 1 m / 1 spool | All wire splices and solder pads on the protection board. | R$ 8–25 (spool) | not verified |
| [2 to 3 mm and 5 to 6 mm heat-shrink tubing (or electrical tape)](https://lista.mercadolivre.com.br/tubo-termo-retratil-3mm) | about 30 cm of each / 1 m of each | Insulate every wire splice. No metal should be exposed near the battery. | R$ 5–20 (total) | not verified |
| [Multimeter](https://lista.mercadolivre.com.br/multimetro-digital) | 1 / 1 | Set the converter to 5.1 V, check the UBEC’s 6 V output and the polarity before connecting the boards. | R$ 40–100 (each) | not verified |
| [2 mm precision flathead screwdriver and small Phillips screwdriver (PH0 or PH1)](https://lista.mercadolivre.com.br/jogo-chaves-precisao-fenda-phillips) | 1 / 1 | Use the flathead to turn the LM2596 adjustment screw and tighten the screw terminals. Use the Phillips to tighten the M2 servo horn screws, the central servo screws, and the Phillips-head M3 and M5 screws. | R$ 10–35 (each) | not verified |
| [Small wire cutters](https://lista.mercadolivre.com.br/alicate-de-corte-eletronica) | 1 / 1 | Cuts wires, resistor leads, excess zip ties, and the pin header. | R$ 15–40 (each) | not verified |
| [Wire stripper (or a utility knife, carefully)](https://lista.mercadolivre.com.br/descascador-de-fios) | 1 / 1 | Removes the insulation from the ends of 20 and 22 AWG wires without cutting the copper strands. | R$ 15–45 (each) | not verified |
| [Fine-tip tweezers](https://lista.mercadolivre.com.br/pinca-ponta-fina-eletronica) | 1 / 1 | Pulls wire ends through the slot in the bottom of the head and holds resistors while you solder. | R$ 5–20 (each) | not verified |
| [Long 2.5 mm Allen key (shaft 50 mm or longer)](https://lista.mercadolivre.com.br/chave-allen-2.5mm-longa) | 1 / 1 | Tightens the 4 cover screws through the bottoms of the base holes and the 3 neck braces. | R$ 8–25 (each) | not verified |
| [Caliper](https://lista.mercadolivre.com.br/paquimetro-digital-150mm) | 1 / 1 | Checks the dimensions marked NC before printing. | R$ 25–80 (each) | not verified |
| [15 W or higher USB-C power supply (5 V 3 A; a phone charger works) with a USB-C cable](https://lista.mercadolivre.com.br/carregador-usb-c-20w) | 1 / 1 | Charge the pack through the rear USB-C port. The charger accepts up to 15 W. | R$ 25–80 (each) | not verified |
| [USB A-B cable (the printer cable) and a computer with the Arduino IDE](https://lista.mercadolivre.com.br/cabo-usb-a-b-arduino-uno) | 1 / 1 | Upload the sketch to the Arduino Uno before screwing it onto the base. | R$ 8–25 (each) | not verified |
| [microSD card reader (USB)](https://lista.mercadolivre.com.br/leitor-cartao-micro-sd-usb) | 1 / 1 | Writes the Raspberry Pi system to the card from your computer. Many laptops already have a slot. | R$ 10–30 (each) | not verified |
<!-- /GERADO -->

Optional: 4 adhesive rubber feet under the base. They do not change any fit.

## Counted screws and threaded inserts

16 M3 heat-set threaded inserts: 4 in the base lid, 1 in the door tab, 4 in the face panel pillars, 4 in the
head frame columns, and 3 in the fork.

<!-- GERADO:parafusos -->
| Where it goes | Qty | Screw | What it screws into |
|---|---|---|---|
| Base cover (underside) | 4 | M3 × 10 Allen | threaded insert in the cover |
| Rear door | 1 | M3 × 8 | threaded insert in the cover ear |
| Arduino Uno | 4 | M3 × 8 | directly into the plastic (2.7 mm hole) |
| Pan servo (base) | 4 | M3 × 12 | directly into the plastic (2.7 mm hole) |
| Tilt servo (head frame) | 4 | M3 × 12 | directly into the plastic (2.7 mm hole) |
| Face panel (behind the frame) | 4 | M3 × 8 | threaded insert in the panel posts |
| Head cup (back wall) | 4 | M3 × 8 | threaded insert in the frame columns |
| Neck braces | 3 | M3 × 45 Allen | insert in the fork |
| Tilt pin | 1 | M5 × 16 | directly into the fork's plastic (4.4 mm hole) |
| Raspberry Pi | 4 | M2.5 × 12 + nut | nut behind the crossbar |
| Round horn for the 2 servos | 8 | M2 × 8 self-tapping screw | in the horn holes |
<!-- /GERADO -->

The center horn screws and the servo rubber rings come in the MG996R kit.

## Filament

Grams per color, adding up the 15 parts (volume estimate, without a slicer). Color is a suggestion; material is not:
keep PETG wherever PETG is specified. The minimum is 2 rolls of 1 kg each, one PETG and one PLA, in any colors. With the 6
suggested colors, you need 6 rolls, 3 PETG and 3 PLA, and a lot of filament will be left over. Both filament options are in the list above.

<!-- GERADO:filamento -->
| Material and color | Filament (g) | Time (h) |
|---|---|---|
| PETG yellow | 88 | 3.3 |
| PETG graphite | 351 | 13.2 |
| PETG silver | 24 | 1.1 |
| PLA white | 204 | 7.7 |
| PLA gray | 15 | 0.9 |
| PLA black | 53 | 2.0 |
| **Total** | **735** | **28.2** |
<!-- /GERADO -->

## Phase 2 (optional for now)

None of this is needed to print, assemble, and wire the robot. The parts already have the space, holes, and cable routing.

<!-- GERADO:fase2 -->
| Item (the name opens a search) | Qty | Where it goes | Estimated price | Seen in store |
|---|---|---|---|---|
| [Raspberry Pi Camera Module 3 (25 × 24 mm board) with ribbon cable](https://lista.mercadolivre.com.br/raspberry-pi-camera-module-3) | 1 | Behind the face panel, in the 8 mm hole above the screen. 4 posts with holes for M2 screws. NC: lens holes and height. | R$ 180–350 | not verified |
| [M2 × 6 mm self-tapping screw](https://lista.mercadolivre.com.br/parafuso-m2x6-auto-atarraxante) | 4 | Secures the camera to the 4 posts. | R$ 3–8 | R$ 5.98 for a kit of 10 |
| [I2S INMP441 microphone](https://lista.mercadolivre.com.br/microfone-inmp441-i2s) | 2 | Inside the head, over the 2 holes of 2 mm underneath it. NC: microphone mount not modeled yet. | R$ 15–55 | R$ 54.26 |
| [40 mm speaker, 3 W](https://lista.mercadolivre.com.br/alto-falante-40mm-3w-4-ohms) | 1 | Slides along the 2 rails on the back wall of the base, against the vertical slot grille. NC: diameter and depth. | R$ 7–20 | not verified |
| [Small audio amplifier (PAM8403 or MAX98357A)](https://lista.mercadolivre.com.br/amplificador-pam8403) | 1 | No modeled spot yet: it sits loose in the base, secured with double-sided tape. | R$ 5–35 | R$ 5.47 to R$ 11.34 (PAM8403) |
| [MPU-6050 IMU motion sensor](https://lista.mercadolivre.com.br/mpu-6050-gy-521) | 1 | At the universal point on the base floor (pair of M3 holes, 20 mm apart). | R$ 15–35 | R$ 34.09 |
| [LD19 or LD06 LiDAR](https://lista.mercadolivre.com.br/lidar-ld19) | 1 | At the top of the head: 2 blind holes on the inside; the 0.8 mm skin is drilled only when the sensor is installed. NC: sensor hole pattern. | R$ 400–900 | not verified |
<!-- /GERADO -->

## Glossary

<!-- GERADO:glossario -->
- **GPIO:** The row of 40 pins on the Raspberry Pi, where the screen and signal wires connect. In this guide, "pin 32" is the pin’s position in the row; "GPIO12" is the name of the signal that comes out of it.
- **UBEC:** A small converter used in model aircraft that lowers the battery voltage to a fixed value. Here, 6 V for the servos.
- **BMS:** Lithium battery protection board. It disconnects the battery before it discharges too much, overcharges, or shorts out.
- **2S:** Two lithium cells connected in series, one after the other. Their voltages add up: from 6 V (empty) to 8.4 V (full).
- **Horn:** The plastic part that fits onto the servo shaft and turns with it. This robot uses the round, disk-shaped horn.
- **Heat-set threaded insert:** A brass bushing with an internal thread. It goes into the hole in the plastic when pushed in with a soldering iron, creating a metal thread.
- **NC:** Unconfirmed: a measurement from a store listing that has not yet been checked against the part in hand.
- **Slicer:** The software that turns the 3D file into the layers the printer prints. Bambu Lab's slicer is called Bambu Studio.
- **SSH:** A way to use the Raspberry Pi over the network: you type commands in your computer's terminal, and they run on the Pi without connecting a keyboard or monitor to it.
- **SPI:** A data connection that uses a few wires and a clock to keep things in step. The Raspberry Pi sends the image to the screen through it.
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
<!-- /GERADO -->

How to wire everything on this list: [LIGACAO.en.md](LIGACAO.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
