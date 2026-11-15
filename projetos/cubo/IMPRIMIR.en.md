# How to print the square desktop robot

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Reference printer: Bambu Lab A1 (256 × 256 × 256 mm build plate), 0.4 mm nozzle, 0.2 mm layer height.

Suggested settings, not yet tested with these parts:

- Textured PEI plate for both materials.
- In Bambu Studio, use the Generic PLA profile for PLA and Generic PETG for PETG, with the temperatures included in each profile.
- Typical values to check: PLA with the nozzle at 220 °C and the build plate at 55–65 °C; PETG with the nozzle at 250–255 °C and the build plate at 70–80 °C. The [Bambu filament guide](https://wiki.bambulab.com/en/general/filament-guide-material-table) gives a nozzle range of 240 to 270 °C for PETG.

Page with the same tables: https://inematds.github.io/robos-impressos/guia/en/cubo/#imprimir

## The files are already in print orientation

- Each STL in `pecas/cubo/stl/` is laid out as it should be printed: the bed-contact face is at Z = 0. Open it in your slicer and
  print without rotating it.
- Each 3MF in `pecas/cubo/mesas/` contains the parts for one color, already arranged on a 256 mm build plate.
- Everything at once: [cubo-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/cubo/cubo-stl.zip)
  (the STL files, the 3MF build plates, the Arduino program, and the guides).
- How it was checked (14/11/2026): for each STL, the part bounding box matches the "on build plate" size in the table below,
  the lowest point is at Z = 0, and the flat area touching the build plate is the same one measured by the project checker.
  No part needs supports.
- The 3MF files are generic: geometry and position only, with no profile or color. They were reread by script, but have not yet been
  opened in Bambu Studio. If one does not open, use the STL files.

## 1. Print the test coupon first

**Nothing in this project has been printed yet.** The test coupon (`pecas/comum/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
less than 1 hour) is on build plate 06, with the 4 Raspberry Pi spacers. On the square robot, test these on it:

- one M3 threaded insert in each of the 3 holes (3.9, 4.0, and 4.1 mm);
- one M3 screw in the through-hole (3.4 mm) and another in the hole for threading directly into the plastic (2.7 mm).

The small dimple marks the measurement used by the design. If a different hole works better on your printer, you don’t need to remake the
parts: in Bambu Studio, the X-Y hole compensation option (X-Y hole compensation; Quality tab, Precision group, with
advanced mode enabled) opens or closes every hole in the part: a positive value opens them, a negative value closes them
([source: Bambu Studio code](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
The source doesn’t say whether the value applies per side or to the diameter: start with 0.05 mm and print the test coupon again. The coupon decides.

If you work with the code, you can change the value in the `FOLGA` block in `cad/parametros.py` and generate the parts again
(`.venv/bin/python cad/gerar.py cubo`).

Three notes:

- The test coupon is shared with the other robots in the project. Its servo window is for the micro servo (SG90/MG90S), and its pin sockets and TT motor hole are for the other robots: the square desktop robot uses none of the three. The coupon’s M2.5 and M2 holes are for threading into plastic; on the square desktop robot, the Raspberry Pi uses a clearance hole with a nut.
- The MG996R servo fit and the M5 screw thread are not included in the coupon. Check the servo in the head frame (plate 01, the third in the order below). The M5 thread is in the fork arm (plate 03, the fourth). Both are checked before the long prints.
- The coupon prints in PLA, but 12 of the 16 inserts go into PETG parts. Print a second coupon in PETG. It is not included on any plate or in the totals: load the file `comum-teste-encaixe.stl` separately, with PETG, and allow about 15 g and 38 minutes extra.

## 2. Suggested build plate order

First, the small parts that fit together; last, the two long prints.

<!-- GERADO:mesas -->
| Order | Build plate file | Material and color | Parts | Filament (g) | Time (h) | Why this order |
|---|---|---|---|---|---|---|
| 1 | [cubo-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-06-pla-cinza.3mf) | PLA gray | Test coupon (teste-encaixe), 4 × Raspberry Pi spacer (espacador-pi) | 15 | 0.9 | Start here. The test coupon shows whether the inserts and M3 screws fit with the right clearance on YOUR printer. Less than 1 hour. |
| 2 | [cubo-mesa-04-petg-prata.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-04-petg-prata.3mf) | PETG silver | Neck tube (tubo-pescoco), Neck gear (engrenagem-pescoco) | 24 | 1.1 | Neck tube and gear: small parts that already test the fit with the tie rods. |
| 3 | [cubo-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-01-petg-amarelo.3mf) | PETG yellow | Head frame (quadro-cabeca), Servo gear (engrenagem-servo) | 88 | 3.3 | Head frame and servo gear: check whether the servo fits in the slot and whether the two gears turn together without binding. |
| 4 | [cubo-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-03-petg-grafite.3mf) | PETG graphite | Base cover (tampa-base), Rear door (porta-traseira), Fork (garfo) | 129 | 5.0 | Lid, door, and fork. On the fork, check that the M5 screw threads into the hole in the fork arm; with the previous frame on the workbench, check that the head tilts without getting stuck. |
| 5 | [cubo-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-02-petg-grafite.3mf) | PETG graphite | Base (base) | 222 | 8.2 | Base: the longest print in PETG. |
| 6 | [cubo-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-07-pla-preto.3mf) | PLA black | Face panel (cabeca-face) | 53 | 2.0 | Face panel: the visible side goes on the build plate, so clean the build plate well first. |
| 7 | [cubo-mesa-05-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/mesas/cubo-mesa-05-pla-branco.3mf) | PLA white | Head shell (cabeca-corpo) | 204 | 7.7 | Head cup: the longest print in PLA. Leave it for last, once the printer is dialed in. |
| **Total** |  |  |  | **735** | **28.2** |  |
<!-- /GERADO -->

## 3. Part by part

"Walls" is the number of perimeters. No part needs supports in the orientation provided in the file. The name in
parentheses is the file name.

<!-- GERADO:pecas -->
| Part | File | Qty | Material and color | Size on the build plate (mm) | How it sits on the build plate | Support | Walls | Infill | Filament (g) | Time (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base (base) | [cubo-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-base.stl) | 1 | PETG graphite | 158 × 146 × 56.5 | base on the build plate | no | 4 | 20 % | 222 | 8.2 |
| Base cover (tampa-base) | [cubo-tampa-base.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tampa-base.stl) | 1 | PETG graphite | 158 × 146 × 18 | upside down: the top face on the build plate | no | 4 | 25 % | 101 | 3.8 |
| Rear door (porta-traseira) | [cubo-porta-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-porta-traseira.stl) | 1 | PETG graphite | 45.4 × 52.6 × 5 | outside face on the build plate | no | 3 | 20 % | 9 | 0.4 |
| Neck tube (tubo-pescoco) | [cubo-tubo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-tubo-pescoco.stl) | 1 | PETG silver | 40 × 40 × 32.6 | upside down: top (fork side) on the build plate, conical flange opens at 45° | no | 5 | 40 % | 16 | 0.7 |
| Neck gear (engrenagem-pescoco) | [cubo-engrenagem-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-pescoco.stl) | 1 | PETG silver | 36 × 36 × 8 | lying flat | no | 5 | 60 % | 8 | 0.4 |
| Servo gear (engrenagem-servo) | [cubo-engrenagem-servo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-engrenagem-servo.stl) | 1 | PETG yellow | 69 × 69 × 8 | upside down: top face on the build plate, horn recess facing up | no | 5 | 60 % | 23 | 0.9 |
| Fork (garfo) | [cubo-garfo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-garfo.stl) | 1 | PETG graphite | 44 × 41.9 × 24 | lying down, back on the build plate: the layers run from the block toward the arms | no | 5 | 40 % | 19 | 0.8 |
| Head frame (quadro-cabeca) | [cubo-quadro-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-quadro-cabeca.stl) | 1 | PETG yellow | 129.2 × 74.6 × 63.7 | front of the crossbar on the build plate, sides facing up | no | 4 | 30 % | 65 | 2.4 |
| Head shell (cabeca-corpo) | [cubo-cabeca-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-corpo.stl) | 1 | PLA white | 136 × 118 × 102 | back on the build plate, opening (front) facing up, like a cup | no | 3 | 15 % | 204 | 7.7 |
| Face panel (cabeca-face) | [cubo-cabeca-face.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-cabeca-face.stl) | 1 | PLA black | 129.9 × 111.9 × 34.2 | front face (the visible one) on the build plate, pillars facing up | no | 3 | 20 % | 53 | 2.0 |
| Raspberry Pi spacer (espacador-pi) | [cubo-espacador-pi.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/cubo/stl/cubo-espacador-pi.stl) | 4 | PLA gray | 6 × 6 × 5 | upright | no | 3 | 15 % | <1 | 0.3 |
| Test coupon (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/pecas/comum/stl/comum-teste-encaixe.stl) | 1 | PLA gray | 70 × 34 × 8 | lying flat | no | 3 | 15 % | 15 | 0.6 |
| **Total** |  | **15** |  |  |  |  |  |  | **735** | **28.2** |
<!-- /GERADO -->

Filament and time are volume estimates, without a slicer. The slicer will give you the actual numbers.

## 4. Filament by color

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

## Where Each Part Is Reinforced

<!-- GERADO:reforcos -->
| Part | Reinforcement | What it is |
|---|---|---|
| Base (base) | 45° chamfer on the bottom edge; Ø12 lid posts fused into the corners; servo posts with gussets; ribbed Uno bosses; vertical slots in the grille | tub: floor, walls, pan servo posts, Uno posts and lid posts, power module cradles (zip tie), speaker rails; switch, USB-C, and grille at the back |
| Base cover (tampa-base) | 4 insert bosses with 3 ribs at 45°; 45° chamfer on the edge that touches the build plate | held by 4 M3x10 screws inserted FROM UNDER the base; the neck flange rotates on it; door screw tab |
| Rear door (porta-traseira) | — | battery door (back); 1 M3 screw in the lid tab, foot against 2 floor stops |
| Neck tube (tubo-pescoco) | 3 steel M3 tie rods run through the entire tube: the layers work only in compression; conical flange at 45° | hollow neck (cables inside); 3 M3x45 screws go in from below, through the gear, and thread into the fork's inserts |
| Neck gear (engrenagem-pescoco) | module 1.5 teeth with 5 perimeters (nearly solid tooth); held by the 3 tie rods | 22 teeth; sits under the lid and, with the tube flange above it, keeps the neck from wobbling |
| Servo gear (engrenagem-servo) | module 1.5 teeth with 5 perimeters; 4 screws on the round horn | 44 teeth, attached to the round horn of the pan servo (the neck rotates 2x the servo) |
| Fork (garfo) | layers along the arms (bending); solid block with 3 tie rod inserts; teardrop holes | internal tilt fork: sits inside the head, at the top of the tube; servo horn on one arm, M5 pin (threads into the plastic) on the other; wrench access holes on the left arm |
| Head frame (quadro-cabeca) | full sides down to the bottom with Ø10 columns at the 4 inserts and 45° gussets on the crossbar; tilt servo in a U-shaped slot (no bridge), 4 screws | head skeleton: Raspberry Pi (4 M2.5), tilt servo, pin bearing; holds the panel (4 M3 screws from behind) and the cup (4 M3 screws through the back wall) |
| Head shell (cabeca-corpo) | long edges with a 20 mm radius (vertical in the print) and a 45° chamfer on the back edge; teardrop neck slot; no bridges or ceiling | head shell (5 sides); insert from the back, 4 M3 screws in the back wall; neck slot and microphone holes underneath |
| Face panel (cabeca-face) | 4 Ø10 pillars with 2 ribs at 45° each (M3 threaded inserts at the tip); camera posts | dark face panel: screen window, 8 mm camera hole above it; no screws on the front |
| Raspberry Pi spacer (espacador-pi) | — | 4 Raspberry Pi spacers, 5 mm |
| Test coupon (teste-encaixe) | — | clearance coupon: servo window, 3 insert holes (3.9/4.0/4.1), TT motor shaft, M3 through hole/M3 pilot/M2.5/M2, 3 pin sockets (0.20/0.25/0.30); dimple = design dimension |
<!-- /GERADO -->

After printing: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md) and [LIGACAO.en.md](LIGACAO.en.md).
