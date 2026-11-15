# How to print the square robot on wheels

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Reference printer: Bambu Lab A1 (256 × 256 × 256 mm build plate), 0.4 mm nozzle, 0.2 mm layer height.

Suggested settings, not yet tested with these parts:

- Textured PEI plate for both materials.
- In Bambu Studio, use the Generic PLA profile for PLA and Generic PETG for PETG, with the temperatures included in each profile.
- Typical values to check: PLA with the nozzle at 220 °C and the build plate at 55–65 °C; PETG with the nozzle at 250–255 °C and the build plate at 70–80 °C. The [Bambu filament guide](https://wiki.bambulab.com/en/general/filament-guide-material-table) gives a nozzle range of 240 to 270 °C for PETG.

Robot page: https://inematds.github.io/robos-impressos/guia/en/cubo-rodas/

## The files are already in print orientation

- Each STL in `projetos/cubo-rodas/stl/` is laid out as it should be printed: the support face at Z = 0. Open it in the slicer and
  print without rotating it.
- Each 3MF in `projetos/cubo-rodas/mesas/` contains the parts for one color, already arranged on a 256 mm build plate.
- Everything at once: [cubo-rodas-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/cubo-rodas-stl.zip)
  (the STL files, the build plate 3MF files, the Arduino program, and the guides).
- How it was checked (14/11/2026): for each of the 15 STL files, the part’s bounding box matches the “on the build plate” size in the table
  below, its lowest point is at Z = 0, and it has a flat face against the build plate. No part needs supports.
- The 3MF files are generic: geometry and position only, with no profile or color. They were checked again with a script, but have not yet been
  opened in Bambu Studio. If one does not open, use the STL files.

## 1. Print the test coupon first

**Nothing in this project has been printed yet.** The test coupon (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
less than 1 hour) is on build plate 07, with the 4 Raspberry Pi spacers. For this robot, test these on it:

- one M3 threaded insert in each of the 3 holes (3.9, 4.0, and 4.1 mm);
- one M3 screw in the clearance hole (3.4 mm) and another in the hole for threading directly into the plastic (2.7 mm);
- one M2.5 screw in the hole for threading directly into the plastic: this is how the screen is attached to the face panel.

The small dimple marks the measurement used by the design. If a different hole works better on your printer, you don’t need to remake the
parts: in Bambu Studio, the X-Y hole compensation option (X-Y hole compensation; Quality tab, Precision group, with
advanced mode enabled) opens or closes every hole in the part: a positive value opens them, a negative value closes them
([source: Bambu Studio code](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
The source doesn’t say whether the value applies per side or to the diameter: start with 0.05 mm and print the test coupon again. The coupon decides.

Anyone who works with the code can change the value in the `FOLGA` block in `comum/cad/parametros.py` and generate the parts again
(`.venv/bin/python comum/cad/gerar.py cubo_rodas`).

Four notes:

- The coupon is shared with the project's other robots. Its servo window is for the micro servo (SG90/MG90S), and the pin sockets and TT motor hole are for the other robots: this robot uses none of these three. The Raspberry Pi here uses a clearance hole with a nut.
- The MG996R servo fit and the M5 screw thread are not on the coupon. Check the servo on the head frame (build plate 01, the third in the order below). The M5 thread is on the fork arm (build plate 04, the fourth). Both are ready before the long prints.
- The motor fit is not on the coupon either. The flange is on build plate 04: with the motor in hand, check the 6 holes around the shaft before printing the base, which is the longest print. If the holes do not line up, correct the measurement and reprint only the flange.
- The coupon is printed in PLA, but 27 of the 31 inserts go in PETG parts. Print a second coupon in PETG. It is not on any build plate or included in the totals: load the `comum-teste-encaixe.stl` file separately, with PETG, and allow about 15 g and 38 minutes extra.

## 2. Suggested build plate order

Print the small parts that fit together first; do the long prints last.

<!-- GERADO:mesas -->
| Order | Build plate file | Material and color | Parts | Filament (g) | Time (h) | Why this order |
|---|---|---|---|---|---|---|
| 1 | [cubo_rodas-mesa-07-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-07-pla-cinza.3mf) | PLA gray | Test coupon (teste-encaixe), 4 × Raspberry Pi spacer (espacador-pi) | 15 | 0.9 | Start here. The test coupon shows whether threaded inserts and M3 screws fit with the right clearance on YOUR printer. Less than 1 hour, with the 4 Raspberry Pi spacers. |
| 2 | [cubo_rodas-mesa-05-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-05-petg-prata.3mf) | PETG silver | Neck tube (tubo-pescoco), Neck gear (engrenagem-pescoco) | 25 | 1.1 | Neck tube and gear: small parts that already test the fit with the tie rods. |
| 3 | [cubo_rodas-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-01-petg-amarelo.3mf) | PETG yellow | Head frame (quadro-cabeca), Servo gear (engrenagem-servo) | 108 | 4.1 | Head frame and servo gear: check whether the servo fits in the slot and whether the two gears turn together without binding. |
| 4 | [cubo_rodas-mesa-04-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-04-petg-grafite.3mf) | PETG graphite | Deck (board tray) (deck), Battery hatch (tampa-bateria), 2 × Motor flange (flange-motor), Ball cover (capa-esfera), Fork (garfo) | 187 | 7.3 | Deck, battery hatch, the 2 flanges, ball cover, and fork. Check now: the flange’s 6 holes against the motor, the M5 screw in the fork arm, and the plates on the deck’s raised areas. |
| 5 | [cubo_rodas-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-03-petg-grafite.3mf) | PETG graphite | Wheeled base (base-rodas) | 267 | 9.8 | Base with wheels: the longest print. Before printing it, check with the previous build plate flange that the motor fits through a 40.6 mm hole. |
| 6 | [cubo_rodas-mesa-02-petg-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-02-petg-branco.3mf) | PETG white | Torso (tronco) | 236 | 8.7 | Torso: print upside down, with the top on the build plate. |
| 7 | [cubo_rodas-mesa-08-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-08-pla-preto.3mf) | PLA black | Face panel (cabeca-face) | 57 | 2.2 | Face panel: the visible side goes on the build plate, so clean the build plate well first. |
| 8 | [cubo_rodas-mesa-06-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/mesas/cubo_rodas-mesa-06-pla-branco.3mf) | PLA white | Head shell (cabeca-corpo) | 248 | 9.3 | Head cup: the longest print in PLA. Leave it for last, once the printer is dialed in. |
| **Total** |  |  |  | **1143** | **43.4** |  |
<!-- /GERADO -->

## 3. Part by part

"Walls" is the number of perimeters. No part needs supports in the orientation provided in the file. The name in
parentheses is the file name.

<!-- GERADO:pecas -->
| Part | File | Qty | Material and color | Size on the build plate (mm) | How it sits on the build plate | Support | Walls | Infill | Filament (g) | Time (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Wheeled base (base-rodas) | [cubo_rodas-base-rodas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-base-rodas.stl) | 1 | PETG graphite | 130 × 182 × 72 | base on the build plate | no | 5 | 25 % | 267 | 9.8 |
| Battery hatch (tampa-bateria) | [cubo_rodas-tampa-bateria.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tampa-bateria.stl) | 1 | PETG graphite | 108 × 84 × 7 | bottom face on the build plate, brackets facing up | no | 4 | 25 % | 34 | 1.3 |
| Ball cover (capa-esfera) | [cubo_rodas-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-capa-esfera.stl) | 1 | PETG graphite | 56.9 × 47.2 × 12 | upside down: the face that touches the floor on the build plate; the opening closes at 45° | no | 4 | 40 % | 9 | 0.4 |
| Motor flange (flange-motor) | [cubo_rodas-flange-motor.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-flange-motor.stl) | 2 | PETG graphite | 62 × 62 × 4 | lying down, the face that touches the wall on the build plate | no | 5 | 60 % | 28 | 1.2 |
| Deck (board tray) (deck) | [cubo_rodas-deck.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-deck.stl) | 1 | PETG graphite | 127 × 179 × 29.8 | bottom face on the build plate | no | 4 | 25 % | 97 | 3.6 |
| Torso (tronco) | [cubo_rodas-tronco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tronco.stl) | 1 | PETG white | 130 × 182 × 57.5 | upside down: top on the build plate | no | 4 | 15 % | 236 | 8.7 |
| Neck tube (tubo-pescoco) | [cubo_rodas-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-tubo-pescoco.stl) | 1 | PETG silver | 40 × 40 × 36.6 | upside down: top (fork side) on the build plate, conical flange opens at 45° | no | 5 | 40 % | 17 | 0.7 |
| Neck gear (engrenagem-pescoco) | [cubo_rodas-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-pescoco.stl) | 1 | PETG silver | 35.8 × 36 × 8 | lying flat | no | 5 | 60 % | 8 | 0.4 |
| Servo gear (engrenagem-servo) | [cubo_rodas-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-engrenagem-servo.stl) | 1 | PETG yellow | 68.9 × 68.9 × 8 | upside down: top face on the build plate, horn recess facing up | no | 5 | 60 % | 23 | 0.9 |
| Fork (garfo) | [cubo_rodas-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-garfo.stl) | 1 | PETG graphite | 44 × 41.9 × 24 | lying down, back on the build plate: the layers run from the block toward the arms | no | 5 | 40 % | 19 | 0.8 |
| Head frame (quadro-cabeca) | [cubo_rodas-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-quadro-cabeca.stl) | 1 | PETG yellow | 145.2 × 93.5 × 62.7 | front of the crossbar on the build plate, sides facing up | no | 4 | 30 % | 85 | 3.2 |
| Head shell (cabeca-corpo) | [cubo_rodas-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-corpo.stl) | 1 | PLA white | 152 × 128 × 110 | back on the build plate, opening (front) facing up, like a cup | no | 3 | 15 % | 248 | 9.3 |
| Face panel (cabeca-face) | [cubo_rodas-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-cabeca-face.stl) | 1 | PLA black | 145.9 × 121.9 × 43.2 | front face (the visible one) on the build plate, pillars facing up | no | 3 | 20 % | 57 | 2.2 |
| Raspberry Pi spacer (espacador-pi) | [cubo_rodas-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo-rodas/stl/cubo_rodas-espacador-pi.stl) | 4 | PLA gray | 6 × 6 × 4 | upright | no | 3 | 15 % | <1 | 0.3 |
| Test coupon (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gray | 70 × 34 × 8 | lying flat | no | 3 | 15 % | 15 | 0.6 |
| **Total** |  | **19** |  |  |  |  |  |  | **1143** | **43.4** |
<!-- /GERADO -->

Filament and time are volume estimates, without a slicer. The slicer will give you the actual numbers.

## 4. Filament by color

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

## Where Each Part Is Reinforced

<!-- GERADO:reforcos -->
| Part | Reinforcement | What it is |
|---|---|---|
| Wheeled base (base-rodas) | motor walls with 4 mm reinforcement and teardrop holes; 4 Ø12 posts at the corners; ribbed bosses for the battery hatch and cover; 45° conical ball seat; 45° chamfer underneath | mobile base tub: motors enter from the side (flange behind the wheel), battery in a hatch underneath, USB-C charger and switch at the back, drop sensor window in the floor; inside, 3 blind windows for the phase 2 distance sensors (front and sides): the outside wall is smooth |
| Battery hatch (tampa-bateria) | 4 brackets + zip tie hold the 3x18650 holder | battery hatch: 4 M3x8 screws underneath; the battery comes down with it |
| Ball cover (capa-esfera) | 4 ears; 45° conical opening | holds the 40 mm ball in the well; 4 M3x8 screws underneath; 8 mm off the ground |
| Motor flange (flange-motor) | nearly solid disk (5 perimeters, 60%): carries the motor's weight and torque | holds the JGB37 motor (6 M3x6) and closes the base side hole (4 M3x10); hidden behind the wheel |
| Deck (board tray) (deck) | pan servo posts with gussets; ribbed bosses for the Uno and L298N; cradles with zip ties | electronics tray: pan servo, Arduino Uno, L298N, Pi step-down converter, and UBEC; 1.5 mm inward (shadow gap between the base and torso) |
| Torso (tronco) | 4 Ø12 columns integrated into the walls (insert at the tip); 6 mm 45° chamfer at the top; speaker rails start at the top | top shell: 4 M3x12 screws go in FROM UNDER the base, pass through the deck, and thread into here; speaker grille at the back |
| Neck tube (tubo-pescoco) | 3 steel M3 tie rods run through the entire tube: the layers work only in compression; conical flange at 45° | hollow neck (cables inside); 3 M3x50 screws go in from underneath, through the gear, and thread into the fork inserts |
| Neck gear (engrenagem-pescoco) | module 1.5 teeth with 5 perimeters (nearly solid tooth); held by the 3 tie rods | 22 teeth; sits under the lid and, with the tube flange above it, keeps the neck from wobbling |
| Servo gear (engrenagem-servo) | module 1.5 teeth with 5 perimeters; 4 screws on the round horn | 44 teeth, attached to the round horn of the pan servo (the neck rotates 2x the servo) |
| Fork (garfo) | layers along the arms (bending); solid block with 3 tie rod inserts; teardrop holes | internal tilt fork: sits inside the head, at the top of the tube; servo horn on one arm, M5 pin (threads into the plastic) on the other; wrench access holes on the left arm |
| Head frame (quadro-cabeca) | full sides down to the bottom with Ø10 columns at the 4 inserts and 45° gussets on the crossbar; tilt servo in a U-shaped slot (no bridge), 4 screws | head skeleton: Raspberry Pi (4 M2.5), tilt servo, pin bearing; holds the panel (4 M3 screws from behind) and the cup (4 M3 screws through the back wall) |
| Head shell (cabeca-corpo) | long edges with a 20 mm radius (vertical in the print) and a 45° chamfer on the back edge; teardrop neck slot; no bridges or ceiling | head shell (5 sides); insert from the back, 4 M3 screws in the back wall; neck slot and microphone holes underneath |
| Face panel (cabeca-face) | 4 Ø10 pillars with 2 ribs at 45° each (M3 threaded inserts at the tip); camera posts | dark face panel: screen window, 8 mm camera hole above it; no screws on the front |
| Raspberry Pi spacer (espacador-pi) | — | 4 Raspberry Pi spacers, 4 mm |
| Test coupon (teste-encaixe) | — | clearance coupon: servo window, 3 insert holes (3.9/4.0/4.1), TT motor shaft, M3 through hole/M3 pilot/M2.5/M2, 3 pin sockets (0.20/0.25/0.30); dimple = design dimension |
<!-- /GERADO -->

After printing: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md) and [LIGACAO.en.md](LIGACAO.en.md).
