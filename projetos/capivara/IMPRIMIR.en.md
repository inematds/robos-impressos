# How to print the capybara

<!-- GERADO:idiomas -->
[🇧🇷 Português](IMPRIMIR.md) · [🇺🇸 English](IMPRIMIR.en.md) · [🇪🇸 Español](IMPRIMIR.es.md)
<!-- /GERADO -->

Reference printer: Bambu Lab A1 (256 × 256 × 256 mm build plate), 0.4 mm nozzle, 0.2 mm layer height.

Suggested settings, not yet tested with these parts:

- Textured PEI plate for both materials.
- In Bambu Studio, use the Generic PLA profile for PLA and Generic PETG for PETG, with the temperatures included in each profile.
- Typical values to check: PLA with the nozzle at 220 °C and the build plate at 55–65 °C; PETG with the nozzle at 250–255 °C and the build plate at 70–80 °C. The [Bambu filament guide](https://wiki.bambulab.com/en/general/filament-guide-material-table) gives a nozzle range of 240 to 270 °C for PETG.

Page with the same tables: https://inematds.github.io/robos-impressos/guia/en/capivara/#imprimir

## The files are already in print orientation

- Each STL in `projetos/capivara/stl/` is in the position it should be printed in: the support face is at Z = 0. Open it in the slicer and
  print without rotating it.
- Each 3MF in `projetos/capivara/mesas/` contains the parts of one color, already arranged on a 256 mm build plate.
- Everything at once: [capivara-stl.zip](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/capivara-stl.zip)
  (the STL files, the build plate 3MF files, the Arduino program, and the guides).
- How it was checked (14/11/2026): for each STL, the part's bounding box matches the "on the build plate" size in the table below, and the
  lowest point is at Z = 0.
- The 3MF files are generic: geometry and position only, with no profile or color. They were reread by script, but have not yet been
  opened in Bambu Studio. If any file won't open, use the STL files.

## Six parts need supports

The others print without supports. For these six, enable supports in the slicer (tree supports, unless the table says otherwise).
For none of them do the supports touch the face or a fit.

| Part | Where to put supports | Will they show? |
|---|---|---|
| Skull | Inside: skull ceiling and bottoms of the eye cups. Underneath: roof of the mouth and lower curves of the cheeks. | No. None on the face. |
| Body | Inside: ceilings of the 2 legs, above the support ball bosses; lower corners of the arm relief (1.0 % of the area). | No. |
| Rear door | About 110 mm² on the lower curve, on the outside and underneath. | No: it faces the floor. |
| Jaw | Under the round relief at the back, inside. | No. |
| Neck fork | 1.8 mm under the base, around the horn ring. Normal supports. | No: it stays inside the collar. |
| Tilt cradle | A little, under the bridge between the 2 servo walls. | No: it stays inside the collar. |

The project checker measures each part's unsupported area and rejects parts declared support-free that would need them.
No one has removed supports from any of these printed parts yet: start with a small part, such as the jaw.

## 1. Print the test coupon first

**Nothing in this project has been printed yet.** The test coupon (`comum/pecas/stl/comum-teste-encaixe.stl`, 70 × 34 × 8 mm,
less than 1 hour) is on build plate 06. Test on it:

- an M3 insert in each of the 3 holes (3.9, 4.0 and 4.1 mm);
- an M3 screw in the through-hole (3.4 mm) and another in the hole for threading directly into the plastic (2.7 mm);
- the micro servo in its window and the wheel motor shaft in its hole;
- the M2.5 (Raspberry Pi) and M2 (micro servo screws) holes, for threading directly into the plastic.

The small dimple marks the measurement used by the design. If a different hole works better on your printer, you don’t need to remake the
parts: in Bambu Studio, the X-Y hole compensation option (X-Y hole compensation; Quality tab, Precision group, with
advanced mode enabled) opens or closes every hole in the part: a positive value opens them, a negative value closes them
([source: Bambu Studio code](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp)).
The source doesn’t say whether the value applies per side or to the diameter: start with 0.05 mm and print the test coupon again. The coupon decides.

Anyone editing the code can change the value in the `FOLGA` block in `comum/cad/parametros.py` and generate the parts again
(`.venv/bin/python comum/cad/gerar.py capivara`).

Three notes:

- The coupon is shared with the project's other robots. Its 3 pin sockets aren't used in this robot.
- The MG996R servo fit isn't included on the coupon. Check the servo in the tilt cradle (build plate 03, the fourth in the order below),
  before the long prints.
- The coupon is printed in PLA, but 13 of the 18 inserts go into PETG parts (chassis, cradle, and fork). Print a second coupon in PETG. It isn't on any build plate or included in the totals: load the `comum-teste-encaixe.stl` file separately with PETG, and allow about 15 g and 38 extra minutes.

## 2. Suggested build plate order

Print the small parts and skeleton first; save the long prints for last: the collar, skull, and body.

<!-- GERADO:mesas -->
| Order | Build plate file | Material and color | Parts | Filament (g) | Time (h) | Why this order |
|---|---|---|---|---|---|---|
| 1 | [capivara-mesa-06-pla-cinza.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-06-pla-cinza.3mf) | PLA gray | Test coupon (teste-encaixe) | 15 | 0.6 | Start here. The test coupon shows whether the threaded inserts, M3 screws, micro servo, and motor shaft fit with the right clearance on YOUR printer. Less than 1 hour. |
| 2 | [capivara-mesa-01-petg-amarelo.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-01-petg-amarelo.3mf) | PETG yellow | Raspberry Pi tray (bandeja-pi), Arduino tray (bandeja-uno) | 33 | 1.3 | The 2 trays: small parts that test the Raspberry Pi and Arduino holes. |
| 3 | [capivara-mesa-02-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-02-petg-grafite.3mf) | PETG graphite | Head plate (mesa-cabeca) | 36 | 1.4 | Head plate: check that the mouth micro servo fits through the opening. |
| 4 | [capivara-mesa-03-petg-grafite.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-03-petg-grafite.3mf) | PETG graphite | Chassis (chassi), Neck fork (garfo-pescoco), 2 × Sphere cover (capa-esfera), Tilt cradle (berco-tilt) | 212 | 8.1 | The skeleton in PETG: chassis, fork, cradle, and the 2 ball covers. The fork and cradle need supports. Check that the MG996R servo fits in the cradle before starting the long prints. |
| 5 | [capivara-mesa-04-pla-branco.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-04-pla-branco.3mf) | PLA white | Right eye (olho), Left eye (olho-esq) | 34 | 1.5 | The 2 eyes. |
| 6 | [capivara-mesa-09-pla-marrom.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-09-pla-marrom.3mf) | PLA brown | Snout (focinho), Tail (rabo), Right hand (mao-dir), Left hand (mao-esq), Right iris (iris), Left iris (iris-esq), Right ear (orelha-dir), Left ear (orelha-esq) | 84 | 3.8 | The brown parts: snout, tail, hands, ears, and irises. Place the gluing face on the build plate. |
| 7 | [capivara-mesa-10-pla-preto.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-10-pla-preto.3mf) | PLA black | 2 × Ring centre disc (miolo), Right pupil (pupila), Left pupil (pupila-esq) | 9 | 0.7 | Ring centre discs and pupils. |
| 8 | [capivara-mesa-05-pla-ciano.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-05-pla-ciano.3mf) | PLA cyan | 2 × Hip ring (aro) | 4 | 0.3 | The 2 hip rings. Use translucent filament if you want to put lights behind them in phase 2. |
| 9 | [capivara-mesa-11-pla-verde-bandana.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-11-pla-verde-bandana.3mf) | PLA green bandana | Bandana collar (gola), Tip of the bandana (avental) | 182 | 6.9 | Collar-bandana and the tip of the bandana. |
| 10 | [capivara-mesa-07-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-07-pla-laranja.3mf) | PLA orange | Skull (cranio) | 251 | 9.5 | Skull: the longest head part. Use tree supports inside and under the roof of the mouth. No supports on the face. |
| 11 | [capivara-mesa-08-pla-laranja.3mf](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/mesas/capivara-mesa-08-pla-laranja.3mf) | PLA orange | Body shell (corpo), Tuft (topete), Rear door (porta), Jaw (mandibula) | 269 | 10.3 | Body, rear door, jaw, and tuft: the longest print. Leave it for last, once the printer is adjusted. The body needs a little tree support inside. |
| **Total** |  |  |  | **1129** | **44.4** |  |
<!-- /GERADO -->

## 3. Part by part

"Walls" is the number of perimeters. The "Supports" column says whether the part needs supports and where. The name in parentheses is the
filename.

<!-- GERADO:pecas -->
| Part | File | Qty | Material and color | Size on the build plate (mm) | How it sits on the build plate | Support | Walls | Infill | Filament (g) | Time (h) |
|---|---|---|---|---|---|---|---|---|---|---|
| Tail (rabo) | [capivara-rabo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-rabo.stl) | 1 | PLA brown | 52.8 × 58.8 × 29.3 | flat base (collar face) on the build plate | no | 3 | 15 % | 21 | 0.9 |
| Right hand (mao-dir) | [capivara-mao-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-dir.stl) | 1 | PLA brown | 48.6 × 48.1 × 19.7 | flat base (collar face) on the build plate | no | 3 | 15 % | 11 | 0.5 |
| Left hand (mao-esq) | [capivara-mao-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mao-esq.stl) | 1 | PLA brown | 48.6 × 48.1 × 19.7 | flat base (collar face) on the build plate | no | 3 | 15 % | 11 | 0.5 |
| Tip of the bandana (avental) | [capivara-avental.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-avental.stl) | 1 | PLA green bandana | 68.9 × 38.4 × 12.1 | flat base (collar face) on the build plate | no | 3 | 15 % | 9 | 0.4 |
| Hip ring (aro) | [capivara-aro.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-aro.stl) | 2 | PLA cyan | 40 × 40 × 3 | flat face on the build plate | no | 3 | 15 % | 4 | 0.3 |
| Ring centre disc (miolo) | [capivara-miolo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-miolo.stl) | 2 | PLA black | 28 × 28 × 2.4 | flat face on the build plate | no | 3 | 15 % | 3 | 0.3 |
| Body shell (corpo) | [capivara-corpo.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-corpo.stl) | 1 | PLA orange | 197 × 179.9 × 119 | bottom edge (z=5) on the build plate, upright like a vase; opening (z=124) facing up | yes (a little, fine tree: ceiling inside the 2 paws, over the support ball bumps; bottom corners of the arm relief; bottom tip of the 2 rear blocks; ~1.0 % of the area) | 4 | 15 % | 196 | 7.4 |
| Rear door (porta) | [capivara-porta.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-porta.stl) | 1 | PLA orange | 76.1 × 36.7 × 119 | bottom edge on the build plate, upright | yes (a little: ~110 mm² on the lower curve, outside and underneath; not visible) | 4 | 15 % | 38 | 1.5 |
| Bandana collar (gola) | [capivara-gola.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-gola.stl) | 1 | PLA green bandana | 159.4 × 155.7 × 68.6 | base (z=124) on the build plate; the ball rises to 45° and stays open at the top | no | 4 | 20 % | 173 | 6.5 |
| Skull (cranio) | [capivara-cranio.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-cranio.stl) | 1 | PLA orange | 181.2 × 187.1 × 134.7 | bottom edge (z=152) on the build plate, upright | yes (supports INSIDE: skull ceiling and bottoms of the eye sockets; and underneath, outside the face: roof of the mouth and lower curve of the cheeks) | 3 | 15 % | 251 | 9.5 |
| Jaw (mandibula) | [capivara-mandibula.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mandibula.stl) | 1 | PLA orange | 130.4 × 30.8 × 44.3 | rear face (cut plane) on the build plate, chin tip pointing up | yes (a little: ~190 mm² in the rear spherical relief, inside) | 4 | 20 % | 20 | 0.8 |
| Head plate (mesa-cabeca) | [capivara-mesa-cabeca.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-mesa-cabeca.stl) | 1 | PETG graphite | 97.2 × 146.5 × 50.3 | upside down: top face on the build plate | no | 4 | 30 % | 36 | 1.4 |
| Right eye (olho) | [capivara-olho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho.stl) | 1 | PLA white | 48 × 48 × 24 | flat back face on the build plate | no | 3 | 15 % | 16 | 0.7 |
| Left eye (olho-esq) | [capivara-olho-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-olho-esq.stl) | 1 | PLA white | 48 × 48 × 24 | flat back face on the build plate | no | 3 | 15 % | 18 | 0.8 |
| Right iris (iris) | [capivara-iris.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris.stl) | 1 | PLA brown | 34 × 34 × 10.5 | back face on the build plate | no | 3 | 15 % | 6 | 0.3 |
| Left iris (iris-esq) | [capivara-iris-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-iris-esq.stl) | 1 | PLA brown | 34 × 34 × 10.5 | back face on the build plate | no | 3 | 15 % | 6 | 0.3 |
| Right pupil (pupila) | [capivara-pupila.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila.stl) | 1 | PLA black | 22 × 22 × 8.7 | back face on the build plate | no | 3 | 15 % | 3 | 0.2 |
| Left pupil (pupila-esq) | [capivara-pupila-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-pupila-esq.stl) | 1 | PLA black | 22 × 22 × 8.9 | back face on the build plate | no | 3 | 15 % | 3 | 0.2 |
| Snout (focinho) | [capivara-focinho.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-focinho.stl) | 1 | PLA brown | 77.9 × 59.9 × 18.2 | flat base (collar face) on the build plate | no | 3 | 15 % | 25 | 1.0 |
| Right ear (orelha-dir) | [capivara-orelha-dir.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-dir.stl) | 1 | PLA brown | 26.3 × 26.8 × 5.4 | flat base (collar face) on the build plate | no | 3 | 15 % | 2 | 0.2 |
| Left ear (orelha-esq) | [capivara-orelha-esq.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-orelha-esq.stl) | 1 | PLA brown | 26.3 × 26.8 × 5.4 | flat base (collar face) on the build plate | no | 3 | 15 % | 2 | 0.1 |
| Tuft (topete) | [capivara-topete.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-topete.stl) | 1 | PLA orange | 43.1 × 51.4 × 24.4 | flat base on the build plate | no | 3 | 15 % | 15 | 0.6 |
| Chassis (chassi) | [capivara-chassi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-chassi.stl) | 1 | PETG graphite | 149 × 135.8 × 115 | floor on the build plate (standing upright) | no | 4 | 25 % | 174 | 6.4 |
| Sphere cover (capa-esfera) | [comum-capa-esfera.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-capa-esfera.stl) | 2 | PETG graphite | 29 × 29 × 5.6 | lying flat | no | 3 | 15 % | 6 | 0.4 |
| Raspberry Pi tray (bandeja-pi) | [capivara-bandeja-pi.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-pi.stl) | 1 | PETG yellow | 61.4 × 93 × 8 | plate on the build plate, pillars facing up | no | 4 | 25 % | 17 | 0.7 |
| Arduino tray (bandeja-uno) | [capivara-bandeja-uno.stl](https://github.com/inematds/robos-impressos/raw/main/projetos/capivara/stl/capivara-bandeja-uno.stl) | 1 | PETG yellow | 61.4 × 77.5 × 8 | plate on the build plate, pillars facing up | no | 4 | 25 % | 16 | 0.6 |
| Neck fork (garfo-pescoco) | [comum-garfo-pescoco.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-garfo-pescoco.stl) | 1 | PETG graphite | 65 × 48 × 50.8 | base on the build plate, uprights facing up | yes (1.8 mm under the base, around the servo horn centring ring; normal supports, out of sight) | 5 | 40 % | 17 | 0.7 |
| Tilt cradle (berco-tilt) | [comum-berco-tilt.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-berco-tilt.stl) | 1 | PETG graphite | 38.5 × 23 × 77 | upside down: top of the column on the build plate | yes (a little, under the bridge) | 5 | 40 % | 15 | 0.6 |
| Test coupon (teste-encaixe) | [comum-teste-encaixe.stl](https://github.com/inematds/robos-impressos/raw/main/comum/pecas/stl/comum-teste-encaixe.stl) | 1 | PLA gray | 70 × 34 × 8 | lying flat | no | 3 | 15 % | 15 | 0.6 |
| **Total** |  | **32** |  |  |  |  |  |  | **1129** | **44.4** |
<!-- /GERADO -->

Filament and time are volume estimates, without a slicer. The slicer will give you the actual numbers.

## 4. Filament by color

<!-- GERADO:filamento -->
| Material and color | Filament (g) | Time (h) |
|---|---|---|
| PETG yellow | 33 | 1.3 |
| PETG graphite | 248 | 9.5 |
| PLA white | 34 | 1.5 |
| PLA cyan | 4 | 0.3 |
| PLA gray | 15 | 0.6 |
| PLA orange | 520 | 19.8 |
| PLA brown | 84 | 3.8 |
| PLA black | 9 | 0.7 |
| PLA green bandana | 182 | 6.9 |
| **Total** | **1129** | **44.4** |
<!-- /GERADO -->

## Where Each Part Is Reinforced

<!-- GERADO:reforcos -->
| Part | Reinforcement | What it is |
|---|---|---|
| Tail (rabo) | — | tail; glue to the door's flat seat |
| Right hand (mao-dir) | — | right hand; glue |
| Left hand (mao-esq) | — | left hand; glue |
| Tip of the bandana (avental) | — | bandana tip on the chest; glue into the flat-bottomed recess |
| Hip ring (aro) | — | haunch ring (translucent filament for the phase 2 LED); glue |
| Ring centre disc (miolo) | — | dark disc in the centre of the ring: side distance sensor window (phase 2); glue |
| Body shell (corpo) | 2 solid blocks at the back (one per M3 screw, from the skin to the chassis post; the bottom tip of each starts ~2 mm above the build plate and extends into the declared support); front belly and rear bottom thickened underneath; 4 perimeters because the body shell is open at the back (door) | entire body shell; goes down over the chassis; 2 M3 screws at the back (underneath) + secured at the top by the collar; wraps around the support ball bosses at the front |
| Rear door (porta) | 2 solid blocks (one per M3 screw, from the build plate to the post); flat tail seat with a wall behind it | rear door: the battery and trays come out here without removing the head; 2 M3 screws at the back (underneath); carries the tail and USB-C charger |
| Bandana collar (gola) | solid between the ball and the outer roller (no overhanging ceiling); 2 tabs at the base for the M3 screws in the tower ears | collar-bandana: ball that the head rotates on; rests on the edge of the body shell and holds it in place; 2 M3 screws from above, in the tower ears (inside, before the head) |
| Skull (cranio) | 3 internal ears with M3 inserts for the head plate; eye cups closed at the back (only the cable window) | 3 M3x12 screws from below, through the build plate (on the workbench); 2 holes at the top give access to the column screws |
| Jaw (mandibula) | solid pads on both sides of the shaft; 2 ribs that wrap around the horn | no screws on the outside: the horn fits between 2 ribs (right) and the build plate pin goes into the blind socket (left); opens and snaps into place |
| Head plate (mesa-cabeca) | 4 mm plate; mouth servo window with chamfered corners (19.6 mm bridge); conical speaker seat | head plate: 2 M3x10 screws in the cradle column (from above, through the holes under the tuft); holds the mouth servo, jaw pivot pin and speaker |
| Right eye (olho) | — | right eye: camera pocket (Camera Module 3) open at the back; press-fit or glue into the skull shell |
| Left eye (olho-esq) | — | left eye: ToF sensor pocket open at the back |
| Right iris (iris) | — | iris ring: the camera board rests behind it (4 M2 pilot holes) |
| Left iris (iris-esq) | — |  |
| Right pupil (pupila) | — | DARK HOLLOW pupil in the centre (the camera lens looks through the hole); press-fit, no glue (keeps the lens accessible) |
| Left pupil (pupila-esq) | — | hollow dark pupil (ToF window) |
| Snout (focinho) | — | brown snout cover; glue |
| Right ear (orelha-dir) | — | right ear; glue |
| Left ear (orelha-esq) | — | left ear; glue |
| Tuft (topete) | — | tuft; press-fit (no glue): covers the 2 access holes for the head plate screws |
| Chassis (chassi) | gussets and arch at 45° under the pan deck; full brace from the floor to the deck; thickened rear posts (10 mm wall around the inserts); gusseted collar ears; rails with chamfered ceilings | cutout floor of the skin section + tray rack (rear) + tower and pan servo deck (front) + bosses for the 2 support balls |
| Sphere cover (capa-esfera) | — | ring that holds the support ball; 2 M3x8 |
| Raspberry Pi tray (bandeja-pi) | 3 mm plate resting on both rails along the full length of the rack | Raspberry Pi 4/5 sliding tray (bottom level); slides out at the back through the door; 4 M2.5x8 self-tapping screws |
| Arduino tray (bandeja-uno) | 3 mm plate resting on both rails along the full length of the rack | sliding Arduino Uno + shield tray (upper level); comes out at the back through the door; 4 M3x8 self-tapping screws |
| Neck fork (garfo-pescoco) | NO layers along the uprights: the tilt load bends the uprights in the layer plane, so use 5 perimeters and 40% infill | rotates with the pan servo (round horn) and holds the tilt axle |
| Tilt cradle (berco-tilt) | solid D-shaped column (5 perimeters) and 4 mm bridge between the two servo walls | holds the tilt servo (MG996R upright) and rises through the collar opening to the head plate; cables along the flat face of the column |
| Test coupon (teste-encaixe) | — | clearance coupon: servo window, 3 insert holes (3.9/4.0/4.1), TT motor shaft, M3 through hole/M3 pilot/M2.5/M2, 3 pin sockets (0.20/0.25/0.30); dimple = design dimension |
<!-- /GERADO -->

After printing: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md) and [LIGACAO.en.md](LIGACAO.en.md).
