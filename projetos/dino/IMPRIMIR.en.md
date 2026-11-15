# How to print the dinosaur

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Reference printer: Bambu Lab A1 (256 × 256 × 256 mm build plate), 0.4 mm nozzle, 0.2 mm layer height.

Suggested settings, not yet tested with these parts:

- Textured PEI plate for both materials.
- In Bambu Studio, use the Generic PLA profile for PLA and Generic PETG for PETG, with the temperatures included in each profile.
- Typical values to check: PLA with the nozzle at 220 °C and the build plate at 55–65 °C; PETG with the nozzle at 250–255 °C and the build plate at 70–80 °C. The [Bambu filament guide](https://wiki.bambulab.com/en/general/filament-guide-material-table) gives a nozzle range of 240 to 270 °C for PETG.

Page with the same tables: https://inematds.github.io/robos-impressos/guia/en/dino/#imprimir

## The files are already in print orientation

- Each STL in `projetos/dino/stl/` is already oriented as it should be printed: the support face at Z = 0. Open it in the slicer and
  print without rotating it.
- Each 3MF in `projetos/dino/mesas/` contains the parts for one color, arranged on a 256 mm build plate.
- Everything at once: [dino-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/dino-stl.zip)
  (the STL files, the build plate 3MF files, the Arduino program and the guides).
- How it was checked (14/11/2026): for each STL, the part's bounding box matches the "on build plate" size in the table below, and its
  lowest point is at Z = 0.
- The 3MF files are generic: geometry and position only, with no profile or color. They were reread by script, but have not yet been
  opened in Bambu Studio. If one does not open, use the STL files.

## Six parts need supports

The others print without supports. For these six, enable supports in the slicer (tree supports, unless the table says otherwise).
For none of them do the supports touch the face or a fit.

| Part | Where supports go | Visible? |
|---|---|---|
| Skull | Inside: skull ceiling, bottoms of the eye cups and crest rib. Underneath: edge of the roof of the mouth. | No. Nothing on the face. |
| Body | Inside: ceiling of both thighs, above the wheels, and steps of the flat seats (2.3 % of the area). | No. |
| Rear shell | Inside: ceiling at the top of the hip and rib of the crest slot (2.4 % of the area). | No. |
| Jaw | Under the round cutout at the back, facing the neck. | No. |
| Neck fork | 1.8 mm under the base, around the horn ring. Normal supports. | No: it is inside the collar. |
| Tilt cradle | A little, under the bridge between the two servo walls. | No: it is inside the collar. |

The project checker measures each part's unsupported area and rejects parts declared support-free that would need them.
No one has removed supports from any of these printed parts yet: start with a small part, such as the jaw.

## 1. Print the test coupon first

**Nothing in this project has been printed yet.** The test coupon (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
less than 1 hour) is on build plate 05. Test on it:

- an M3 insert in each of the 3 holes (3.9, 4.0 and 4.1 mm);
- an M3 screw in the through-hole (3.4 mm) and another in the hole for threading directly into the plastic (2.7 mm);
- the micro servo in its window and the wheel motor shaft in its hole;
- the M2.5 (Raspberry Pi) and M2 (micro servo screws) holes, for threading directly into the plastic.

The small dimple marks the measurement used by the design. If a different hole works better on your printer, you don’t need to remake the
parts: in Bambu Studio, the X-Y hole compensation option (X-Y hole compensation; Quality tab, Precision group, with
advanced mode enabled) opens or closes every hole in the part: a positive value opens them, a negative value closes them
([source: Bambu Studio code](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
The source doesn’t say whether the value applies per side or to the diameter: start with 0.05 mm and print the test coupon again. The coupon decides.

Anyone editing the code can change the value in the `FOLGA` block of `comum/cad/parametros.py` and regenerate the parts
(`.venv/bin/python comum/cad/gerar.py dino`).

Three notes:

- The test coupon is shared with the project's other robots. Its 3 pin sockets are not used in this robot.
- The MG996R servo fit is not included on the test coupon. Check the servo in the tilt cradle (plate 02, the third one in the order below),
  before starting the long prints.
- The test coupon is printed in PLA, but 7 of the 13 threaded inserts go into PETG parts (chassis, cradle, and fork). Print a second test coupon in PETG. It is not included on any plate or in the totals: load the file `comum-teste-encaixe.stl` separately with PETG, and add about 15 g and 38 minutes.

## 2. Suggested build plate order

Print the small parts and skeleton first; the long prints last: the skull, rear shell and body.

<!-- GERADO:mesas -->
| Order | Build plate file | Material and color | Parts | Filament (g) | Time (h) | Why this order |
|---|---|---|---|---|---|---|
| 1 | [dino-mesa-05-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-05-pla-cinza.3mf) | PLA gray | Test coupon (teste-encaixe) | 15 | 0.6 | Start here. The test coupon shows whether the threaded inserts, M3 screws, micro servo, and motor shaft fit with the right clearance on YOUR printer. Less than 1 hour. |
| 2 | [dino-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-01-petg-amarelo.3mf) | PETG yellow | Raspberry Pi tray (bandeja-pi), Arduino tray (bandeja-uno) | 28 | 1.2 | The 2 trays: small parts that test the Raspberry Pi and Arduino holes. |
| 3 | [dino-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-02-petg-grafite.3mf) | PETG graphite | Chassis (chassi), Head plate (mesa-cabeca), Neck fork (garfo-pescoco), Sphere cover (capa-esfera), Tilt cradle (berco-tilt), 2 × Arm hub (cubo-braco) | 243 | 9.4 | The entire skeleton in PETG: chassis, head plate, fork, cradle, ball shell, and the 2 arm cubes. The fork and cradle need supports. Check that the MG996R servo fits in the cradle before the long prints. |
| 4 | [dino-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-04-pla-branco.3mf) | PLA white | Right eye (olho), Left eye (olho-esq) | 28 | 1.2 | The 2 eyes. |
| 5 | [dino-mesa-03-pla-azul.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-03-pla-azul.3mf) | PLA blue | Head crest (crista-cabeca), Back crest (crista-costas), Right iris (iris), Left iris (iris-esq) | 42 | 1.9 | Crests and irises, in blue. |
| 6 | [dino-mesa-07-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-07-pla-preto.3mf) | PLA black | Right pupil (pupila), Left pupil (pupila-esq) | 4 | 0.3 | The 2 pupils. |
| 7 | [dino-mesa-12-pla-verde-escuro.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-12-pla-verde-escuro.3mf) | PLA dark green | Right flank spot (mancha-dir), Left flank spot (mancha-esq) | 4 | 0.4 | The 2 flank spots. |
| 8 | [dino-mesa-06-pla-creme.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-06-pla-creme.3mf) | PLA cream | Belly (barriga), Right toe 3 (dedo-dir-3), Left toe 3 (dedo-esq-3), Right toe 1 (dedo-dir-1), Right toe 2 (dedo-dir-2), Left toe 1 (dedo-esq-1), Left toe 2 (dedo-esq-2) | 28 | 1.5 | Belly and the 6 toes: the glue face goes on the build plate. |
| 9 | [dino-mesa-11-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-11-pla-verde.3mf) | PLA green | Jaw (mandibula) | 34 | 1.4 | Jaw: upright, with a little support at the back. |
| 10 | [dino-mesa-09-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-09-pla-verde.3mf) | PLA green | Rear shell (hip and tail) (traseira) | 102 | 3.9 | Rear shell: upright on the seam, with tree supports only on the inside. |
| 11 | [dino-mesa-08-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-08-pla-verde.3mf) | PLA green | Skull (cranio) | 179 | 6.8 | Skull: tree supports on the inside and under the roof of the mouth. No supports on the face. |
| 12 | [dino-mesa-10-pla-verde.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/mesas/dino-mesa-10-pla-verde.3mf) | PLA green | Body (corpo), Neck collar (gola), Right arm (braco-dir), Left arm (braco-esq) | 295 | 11.3 | Body shell, collar, and the 2 arms: the longest print. Leave these for last, once your printer is tuned. The body shell needs tree supports only on the inside. |
| **Total** |  |  |  | **1002** | **39.9** |  |
<!-- /GERADO -->

## 3. Part by part

"Walls" is the number of perimeters. The "Supports" column says whether the part needs supports and where. The name in parentheses is the
filename.

<!-- GERADO:pecas -->
| Part | File | Qty | Material and color | Size on the build plate (mm) | How it sits on the build plate | Support | Walls | Infill | Filament (g) | Time (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Belly (barriga) | [dino-barriga.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-barriga.stl) | 1 | PLA cream | 63.4 × 79.4 × 13.3 | flat base (collar face) on the build plate | no | 3 | 15 % | 22 | 0.9 |
| Right toe 1 (dedo-dir-1) | [dino-dedo-dir-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-1.stl) | 1 | PLA cream | 17.2 × 12.7 × 8.5 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Right toe 2 (dedo-dir-2) | [dino-dedo-dir-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-2.stl) | 1 | PLA cream | 17 × 12.7 × 7.4 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Right toe 3 (dedo-dir-3) | [dino-dedo-dir-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-dir-3.stl) | 1 | PLA cream | 12.7 × 17.4 × 6.9 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Left toe 1 (dedo-esq-1) | [dino-dedo-esq-1.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-1.stl) | 1 | PLA cream | 17.2 × 12.7 × 8.5 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Left toe 2 (dedo-esq-2) | [dino-dedo-esq-2.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-2.stl) | 1 | PLA cream | 17 × 12.7 × 7.4 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Left toe 3 (dedo-esq-3) | [dino-dedo-esq-3.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-dedo-esq-3.stl) | 1 | PLA cream | 12.7 × 17.4 × 6.9 | flat base (collar face) on the build plate | no | 3 | 15 % | 1 | 0.1 |
| Right flank spot (mancha-dir) | [dino-mancha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-dir.stl) | 1 | PLA dark green | 21.3 × 26.4 × 7.6 | flat base (collar face) on the build plate | no | 3 | 15 % | 2 | 0.2 |
| Left flank spot (mancha-esq) | [dino-mancha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mancha-esq.stl) | 1 | PLA dark green | 21.3 × 26.4 × 7.6 | flat base (collar face) on the build plate | no | 3 | 15 % | 2 | 0.2 |
| Right arm (braco-dir) | [dino-braco-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-dir.stl) | 1 | PLA green | 27.5 × 59 × 16 | inner face (flat) on the build plate | no | 3 | 20 % | 8 | 0.4 |
| Left arm (braco-esq) | [dino-braco-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-braco-esq.stl) | 1 | PLA green | 27.5 × 59 × 16 | inner face (flat) on the build plate | no | 3 | 20 % | 8 | 0.4 |
| Arm hub (cubo-braco) | [dino-cubo-braco.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cubo-braco.stl) | 2 | PETG graphite | 17 × 17 × 12.8 | outer tip (2 flat faces) on the build plate, horn recess facing up | no | 4 | 60 % | 6 | 0.4 |
| Body (corpo) | [dino-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-corpo.stl) | 1 | PLA green | 194.1 × 113.7 × 129.4 | bottom edge (z=5) on the build plate, upright like a vase; opening (z=134) facing up | yes (supports INSIDE: tops of both thighs, above the wheels; inner steps of the flat seats (belly, arms, spots); none on the outside) | 4 | 15 % | 200 | 7.5 |
| Rear shell (hip and tail) (traseira) | [dino-traseira.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-traseira.stl) | 1 | PLA green | 126.1 × 131 × 131.9 | front edge (seam plane) on the build plate, tail pointing up | yes (supports INSIDE: top of the hip (53° from vertical) and ridge of the crest slot; none on the outside) | 4 | 15 % | 102 | 3.9 |
| Neck collar (gola) | [dino-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-gola.stl) | 1 | PLA green | 112.3 × 100.5 × 56.1 | base (z=134) on the build plate; sphere facing up, open at the top | no | 4 | 20 % | 79 | 3.0 |
| Back crest (crista-costas) | [dino-crista-costas.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-costas.stl) | 1 | PLA blue | 46.4 × 67.3 × 6 | lying flat (6 mm blade) | no | 3 | 15 % | 10 | 0.4 |
| Skull (cranio) | [dino-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-cranio.stl) | 1 | PLA green | 134.2 × 174.5 × 118.2 | bottom edge on the build plate, upright | yes (supports INSIDE: top of the skull, bottoms of the eye cups, and crest ridge; also underneath, outside the face: edge of the palate, which is 40 mm above the build plate) | 3 | 15 % | 179 | 6.8 |
| Jaw (mandibula) | [dino-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mandibula.stl) | 1 | PLA green | 91.4 × 37 × 35.6 | rear face (cut plane) on the build plate, chin tip pointing up | yes (slight: under the rear spherical cutout, which starts 2 to 10 mm above the build plate; hidden face, toward the neck) | 4 | 20 % | 34 | 1.4 |
| Head plate (mesa-cabeca) | [dino-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-mesa-cabeca.stl) | 1 | PETG graphite | 75.1 × 122.3 × 45.8 | upside down: top face on the build plate | no | 4 | 30 % | 29 | 1.1 |
| Head crest (crista-cabeca) | [dino-crista-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-crista-cabeca.stl) | 1 | PLA blue | 104.9 × 128.3 × 6 | lying flat (6 mm blade) | no | 3 | 15 % | 22 | 0.9 |
| Right eye (olho) | [dino-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho.stl) | 1 | PLA white | 44 × 44 × 22.6 | flat back face on the build plate | no | 3 | 15 % | 13 | 0.6 |
| Left eye (olho-esq) | [dino-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-olho-esq.stl) | 1 | PLA white | 44 × 44 × 22.6 | flat back face on the build plate | no | 3 | 15 % | 15 | 0.6 |
| Right iris (iris) | [dino-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris.stl) | 1 | PLA blue | 30 × 30 × 9.9 | back face on the build plate | no | 3 | 15 % | 5 | 0.3 |
| Left iris (iris-esq) | [dino-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-iris-esq.stl) | 1 | PLA blue | 30 × 30 × 9.9 | back face on the build plate | no | 3 | 15 % | 5 | 0.3 |
| Right pupil (pupila) | [dino-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila.stl) | 1 | PLA black | 19 × 19 × 7.9 | back face on the build plate | no | 3 | 15 % | 2 | 0.1 |
| Left pupil (pupila-esq) | [dino-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-pupila-esq.stl) | 1 | PLA black | 19 × 19 × 8.2 | back face on the build plate | no | 3 | 15 % | 2 | 0.2 |
| Chassis (chassi) | [dino-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-chassi.stl) | 1 | PETG graphite | 105.9 × 179.2 × 121 | floor on the build plate (standing upright) | no | 4 | 25 % | 173 | 6.4 |
| Sphere cover (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 1 | PETG graphite | 29 × 29 × 5.6 | lying flat | no | 3 | 15 % | 3 | 0.2 |
| Raspberry Pi tray (bandeja-pi) | [dino-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-pi.stl) | 1 | PETG yellow | 61.4 × 89 × 8 | plate on the build plate, pillars facing up | no | 4 | 25 % | 16 | 0.7 |
| Arduino tray (bandeja-uno) | [dino-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/dino/stl/dino-bandeja-uno.stl) | 1 | PETG yellow | 67.7 × 58.8 × 6 | plate on the build plate, pillars facing up | no | 4 | 25 % | 12 | 0.5 |
| Neck fork (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG graphite | 65 × 48 × 50.8 | base on the build plate, uprights facing up | yes (1.8 mm under the base, around the servo horn centring ring; normal supports, out of sight) | 5 | 40 % | 17 | 0.7 |
| Tilt cradle (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG graphite | 38.5 × 23 × 77 | upside down: top of the column on the build plate | yes (a little, under the bridge) | 5 | 40 % | 15 | 0.6 |
| Test coupon (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gray | 70 × 34 × 8 | lying flat | no | 3 | 15 % | 15 | 0.6 |
| **Total** |  | **34** |  |  |  |  |  |  | **1002** | **39.9** |
<!-- /GERADO -->

Filament and time are volume estimates, without a slicer. The slicer will give you the actual numbers.

## 4. Filament by color

<!-- GERADO:filamento -->
| Material and color | Filament (g) | Time (h) |
|---|---|---|
| PETG yellow | 28 | 1.2 |
| PETG graphite | 243 | 9.4 |
| PLA blue | 42 | 1.9 |
| PLA white | 28 | 1.2 |
| PLA gray | 15 | 0.6 |
| PLA cream | 28 | 1.5 |
| PLA black | 4 | 0.3 |
| PLA green | 610 | 23.4 |
| PLA dark green | 4 | 0.4 |
| **Total** | **1002** | **39.9** |
<!-- /GERADO -->

## Where Each Part Is Reinforced

<!-- GERADO:reforcos -->
| Part | Reinforcement | What it is |
|---|---|---|
| Belly (barriga) | — | cream belly; glue to the body's flat seat |
| Right toe 1 (dedo-dir-1) | — | toe; glue |
| Right toe 2 (dedo-dir-2) | — | toe; glue |
| Right toe 3 (dedo-dir-3) | — | toe; glue |
| Left toe 1 (dedo-esq-1) | — | toe; glue |
| Left toe 2 (dedo-esq-2) | — | toe; glue |
| Left toe 3 (dedo-esq-3) | — | toe; glue |
| Right flank spot (mancha-dir) | — | flank patch, with an organic outline and flush with the surrounding skin: the side distance sensor window (phase 2) is the small, off-centre hole; glue it to the body's flat seat |
| Left flank spot (mancha-esq) | — | flank patch, with an organic outline and flush with the surrounding skin: the side distance sensor window (phase 2) is the small, off-centre hole; glue it to the body's flat seat |
| Right arm (braco-dir) | — | right arm; press-fits onto the hub (2 flat faces), no outer screw |
| Left arm (braco-esq) | — | left arm |
| Arm hub (cubo-braco) | solid around the horn recess | arm hub: passes through the shoulder hole, fits around the micro servo horn, and is secured by the servo’s centre screw (hidden by the arm) |
| Body (corpo) | 2 solid tabs at the back (horizontal M3 screws in the chassis posts); lip inside the rear edge; solid collar at the back and 3 raised pads with inserts at the top edge; 4 perimeters because the body is open at the back | legs, belly, and chest; lowers over the chassis; 2 M3 screws from the back (covered by the rear shell); the rear edge fits into the rear shell |
| Rear shell (hip and tail) (traseira) | inner ridge along the crest slot; 2 pads at the lower screws; solid tail tip in a cone shape | hip + tail: swings back and gives access to the battery and trays without removing the head; 2 self-tapping M3 screws underneath |
| Neck collar (gola) | solid between the sphere and the outer shell (no overhanging roof); 3 M3 holes with deep recesses | collar: sphere that the head rotates on; rests on the body's edge; 3 M3 screws from above, in the body's raised pads (inside, before the head) |
| Back crest (crista-costas) | — | back and tail-root crest; press-fit or glue into the rear shell slot |
| Skull (cranio) | 3 internal ears with M3 inserts for the head plate; eye cups closed at the back (only the cable window) | 3 M3x12 screws underneath, through the head plate (on the workbench); 2 holes at the top, under the crest, provide access to the column screws |
| Jaw (mandibula) | solid pads on both sides of the shaft; 2 ribs that fit around the horn; solid chin tip in front of a 45° plane | no outer screw: the horn fits between 2 ribs (right), and the head plate pin fits into the blind socket (left) |
| Head plate (mesa-cabeca) | 4 mm plate; mouth servo window with chamfered corners | head plate: 2 M3x10 in the cradle column (from above, through the holes under the crest); holds the mouth servo and the jaw pivot pin |
| Head crest (crista-cabeca) | — | head crest; press-fit (no glue): covers the 2 access holes for the plate screws |
| Right eye (olho) | — | right eye: camera pocket (Camera Module 3) open at the back; press-fit or glue into the skull shell |
| Left eye (olho-esq) | — | left eye: ToF sensor pocket open at the back |
| Right iris (iris) | — | iris ring: the camera board rests behind it (4 M2 pilot holes) |
| Left iris (iris-esq) | — |  |
| Right pupil (pupila) | — | DARK HOLLOW pupil in the centre (the camera lens looks through the hole); press-fit, no glue (keeps the lens accessible) |
| Left pupil (pupila-esq) | — | hollow dark pupil (ToF window) |
| Chassis (chassi) | 45° gussets and a V-shaped wall under the pan deck; full-height crosspiece from the floor to the deck; rack walls widened at 45° from the floor; solid posts at the inserts | cut-out floor of the body shell section + tray rack (behind) + pan servo tower and deck + arm servo ears + rear support ball boss |
| Sphere cover (capa-esfera) | — | ring that holds the support ball; 2 M3x8 |
| Raspberry Pi tray (bandeja-pi) | 3 mm plate resting on both rails along the full length of the rack | Raspberry Pi 4/5 sliding tray (bottom level); slides out at the back through the door; 4 M2.5x8 self-tapping screws |
| Arduino tray (bandeja-uno) | 3 mm plate; rail on the left wall and support on top of the right wall | Arduino Uno + shield tray, mounted sideways (top level); slides out at the back, with the rear shell removed; 4 M3x8 self-tapping screws |
| Neck fork (garfo-pescoco) | NO layers along the uprights: the tilt load bends the uprights in the layer plane, so use 5 perimeters and 40% infill | rotates with the pan servo (round horn) and holds the tilt axle |
| Tilt cradle (berco-tilt) | solid D-shaped column (5 perimeters) and 4 mm bridge between the two servo walls | holds the tilt servo (MG996R upright) and rises through the collar opening to the head plate; cables along the flat face of the column |
| Test coupon (teste-encaixe) | — | clearance coupon: servo window, 3 insert holes (3.9/4.0/4.1), TT motor shaft, M3 through hole/M3 pilot/M2.5/M2, 3 pin sockets (0.20/0.25/0.30); dimple = design dimension |
<!-- /GERADO -->

After printing: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md) and [LIGACAO.en.md](LIGACAO.en.md).
