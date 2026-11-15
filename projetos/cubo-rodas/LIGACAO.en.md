# Wiring the square robot on wheels

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**Not bench-tested.** This diagram is based on the component datasheets; no wires have been connected to an assembled robot yet.
Check every connection with a multimeter before turning on the switch. If your board has a different name printed on it than
the one shown here, use the name printed on the board.

![Wiring diagram for the square robot on wheels, in two drawings. Power: batteries, fuse, protection board, charger, switch, terminal block, converters, and motor driver. Signals: Arduino with Sensor Shield, motor driver, motors with encoders, servos, and Raspberry Pi](ligacao.en.svg)

Robot page: https://inematds.github.io/robos-impressos/guia/en/cubo-rodas/

All soldering for the robot is done at the workbench, in prep steps 1, 2, and 3. Assembly only involves screw terminals and plug-in connections.

## Lithium Battery Safety

- **Polarity:** red to positive, black to negative. Measure with a multimeter before each new connection. A reversed wire burns out the board immediately.
- **Adjust before connecting the load:** XL4015 to 5.1 V and UBEC to 6 V, measured with a multimeter, with the Raspberry Pi, Arduino, and servos disconnected.
- **Short circuits can cause fires:** solder with the cells OUT of the holder and insulate each splice with heat-shrink tubing. No metal can be exposed. A 3-cell pack releases much more energy than a regular battery when shorted.
- **Fuse:** 3 A, slow-blow (marked T3A), on the positive wire, a few centimeters from the battery holder.
- **Matching cells:** all three 18650 cells must be the same brand and model, and new. A dented, swollen, or hot cell goes to battery recycling, not in the robot.
- **First charge:** stay nearby, with the robot on a nonflammable surface.

## What Powers What

- **3S pack:** three 18650 cells in series, from 9 V (empty) to 12.6 V (full). It goes through the fuse and the protection board (BMS).
- **USB-C charger:** connected to the protection board output, before the switch. Charge the robot while it is off, using a USB-C power supply of 15 W or more. It needs to be set up for 3 cells (prep step 1).
- **Switch:** cuts the positive wire going to both converters and the motor driver.
- **XL4015, set to 5.1 V:** the output goes to the terminal block on the deck. From there, one pair powers the Raspberry Pi (through pins 2, 4, 6, and 9), another pair powers the Arduino (through the + and − pins on the Sensor Shield COM connector), and a wire carries 5 V to the motor driver and encoders.
- **UBEC at 6 V:** powers only the 2 servos through the blue screw terminal on the Sensor Shield, with the SEL jumper removed.
- **L298N motor driver:** receives the pack voltage and supplies it to the 2 motors. It drops about 2 V along the way.
- **Negative (GND):** there is only one for the entire robot.

Why the Arduino receives 5.1 V from the converter, not the battery voltage: the Arduino Uno VIN input requires 7 to 12 V
([Arduino Uno R3 datasheet](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)), and the fully charged pack exceeds
12 V.

Why the Raspberry Pi gets power through the pins instead of the USB-C port: the USB-C port is on the bottom edge of the
board, where there is about 22 mm of clearance to the bottom of the head (model measurement, not confirmed), and a straight plug
will not fit there. Pins 2 and 4 accept 5 V input
([Raspberry Pi documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc)).
Power through those pins does not go through the USB-C port protection: measure the 5.1 V before connecting. If you prefer the USB-C port,
use a USB-C adapter with angled screw terminals and check the clearance.

## The terminal block

It is a screw terminal block (the type known as “sindal”) that sits loose on the deck. Use 5 of its terminals, numbered 1 to 5:

- **Terminal 1, the 5.1 V:** on one side, the red wire from the XL4015. On the other, the red wire going up to the Raspberry Pi, the jumper going to the + pin on the shield’s COM connector, and the wire going to the driver’s +5V terminal.
- **Terminal 2, the negative:** on one side, the black wire from the XL4015 and one end of the resistor pair. On the other, the black wire going up to the Raspberry Pi and the jumper going to the − pin on the COM connector.
- **Terminal 3, the serial connection:** on one side, the divider resistors. On the other, the blue wire coming down from the Raspberry Pi.
- **Terminal 4, the pack positive:** on one side, the red wire coming up from the switch. On the other, the XL4015 input, the UBEC input, and the driver’s +12V terminal.
- **Terminal 5, the pack negative:** on one side, the black wire coming up from the protection board. On the other, the negative connections for the XL4015, UBEC, and motor driver.

Terminals 4 and 5 let you separate the deck from the base without desoldering anything: the 2 wires coming up from the base pass
through a slot in the deck and are secured in the terminal block.

## Wiring Table, Wire by Wire

<!-- GERADO:ligacoes -->
### Battery, protection, and charging

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Battery holder: red wire (pack positive) | 3 A fuse holder and, after it, the cell positive solder pad on the protection board (B+ or 12.6V) | red | 22 AWG | The fuse goes a few centimeters from the holder. |
| Battery holder: black wire (pack negative) | Cell negative solder pad on the protection board (B− or 0V) | black | 22 AWG |  |
| Battery holder: upper junction tab (the one on the red wire side) | Upper junction solder pad on the protection board (usually 8.4V) | yellow, marked with tape | 22 AWG | From the battery holder’s black wire to this wire, the multimeter reads about 8 V. Solder to the tab with the cells OUT of the holder. |
| Battery holder: lower junction tab (the one on the black wire side) | Lower junction solder pad on the protection board (usually 4.2V) | yellow | 22 AWG | From the battery holder’s black wire to this wire, the multimeter reads about 4 V. |
| Upper junction tab (a second wire on the same tab) | USB-C charger: the middle solder pad closest to B+ | yellow, marked with tape | 22 AWG | Without the 2 junction wires, the charger won’t balance the three cells. |
| Lower junction tab (a second wire on the same tab) | USB-C charger: the middle solder pad closest to B− | yellow | 22 AWG | The order of the 2 middle solder pads comes from the store listing; the printed labels can’t be read in the photo. |
| B+ solder pad on the USB-C charger | Protection board positive output (P+) | red | 22 AWG | The charger goes before the switch: the robot charges while switched off. |
| B− solder pad on the USB-C charger | Protection board negative output (P−) | black | 22 AWG | Don’t connect to the cell negative solder pad: the load must go through the protection board. |

### Pack switch and distribution

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Protection board positive output (P+) | On/off switch and, after it, terminal 4 on the terminal block | red | 20 AWG | The switch cuts only the positive lead. This wire goes up from the base to the deck through the rear slot. |
| Protection board negative output (P−) | Terminal 5 on the terminal block | black | 20 AWG | This is the common negative (GND) for the entire robot. |
| Terminal block, terminal 4 (pack positive, from 9 to 12.6 V) | XL4015 IN+ input, UBEC red input wire, and L298N motor driver +12V terminal | red | 20 AWG | There are 3 wires in the same terminal. |
| Terminal block, terminal 5 (pack negative) | XL4015 IN− input, UBEC black input wire, and L298N motor driver GND terminal | black | 20 AWG |  |

### 5.1 V: Raspberry Pi, Arduino, driver, and encoders

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| XL4015 OUT+ output (5.1 V) | Terminal block, screw terminal 1 | red | 20 AWG, short | Adjust the 5.1 V BEFORE connecting anything on the other side of the terminal block. |
| XL4015 OUT− output | Terminal block, screw terminal 2 | black | 20 AWG, short |  |
| Terminal block, screw terminal 1 (5.1 V) | Through the neck, to Raspberry Pi pins 2 and 4 | red | 20 AWG, with 2 jumper halves soldered to the end | Pins 2 and 4 are the Pi’s 5 V input. Power through them bypasses the USB-C input protection: measure the 5.1 V and polarity at the terminal block before connecting. |
| Terminal block, screw terminal 2 (negative) | Along the neck, to pins 6 and 9 on the Raspberry Pi | black | 20 AWG, with 2 jumper halves soldered to the end |  |
| Terminal block, screw terminal 1 (5.1 V) | Sensor Shield COM connector + pin | red | Dupont jumper with one end cut and stripped | This is how the Arduino receives power. First, with the Uno powered only by USB and the SEL jumper removed, use a multimeter to confirm that this pin reads about 5 V and the D9 V pin reads 0 V. The wrong pin here sends the servos’ 6 V to the Raspberry Pi. |
| Terminal block, screw terminal 2 (negative) | Sensor Shield COM connector − pin | black | Dupont jumper with one end cut and stripped |  |
| Terminal block, screw terminal 1 (5.1 V) | L298N driver +5V screw terminal | red | 22 AWG | Only with the driver's 5 V regulator jumper REMOVED. If it is installed, the driver's regulator and the XL4015 will be connected against each other. |
| Blue wire from each motor cable (encoder power) | L298N driver +5V screw terminal, together with the wire from terminal 1 | blue | 6-wire motor cable | The encoder accepts 3.3 to 5 V. Never connect this wire to the motor voltage or to the shield's V pin, which has 6 V. |
| Black wire from each motor cable (encoder negative) | L298N driver GND screw terminal | black | 6-wire motor cable |  |

### 6 V: servos

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| UBEC red output wire (6 V) | Sensor Shield blue VCC screw terminal | red | UBEC wire, with the 3-pin plug cut off | Sensor Shield SEL jumper REMOVED and UBEC jumper set to 6 V. The UBEC output has a servo plug: cut it off and strip the wires. Red is positive. |
| Black or brown UBEC output wire | Sensor Shield blue GND screw terminal | black | UBEC wire, with the 3-pin plug cut off | If the plug has a third wire, white or orange, insulate its end with heat-shrink tubing: it isn’t connected. |
| 1000 µF capacitor: long leg (+) | Blue VCC screw terminal; the striped leg (−) goes to the blue GND screw terminal | no wire | capacitor leads | The capacitor will explode if connected backwards. |
| Pan servo (on the deck) | Sensor Shield D9 connector | servo cable | 3-wire servo cable | G = brown or black, V = red, S = orange or yellow. |
| Tilt servo (in the head) | Through the neck, using the 30 cm extension, to the Sensor Shield D10 connector | servo cable | 3-wire servo cable | Same color order as D9. |

### Motors and encoders

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Right motor: red and white wires | L298N driver OUT1 and OUT2 screw terminals | red and white | 6-wire motor cable | If the wheel turns the wrong way when the phase 2 program tells it to move forward, switch these two wires. |
| Left motor: red and white wires | L298N driver OUT3 and OUT4 screw terminals | red and white | 6-wire motor cable |  |
| L298N driver: ENA pin | S pin of D5 on the Sensor Shield | any, marked ENA | 40 cm Dupont jumper, intact | With the ENA jumper removed. The wire goes to the input pin, not the 5 V pin next to it (prep step 3). D5 and D6 control the speed. |
| L298N driver: IN1 and IN2 pins | S pin of D4 (IN1) and S pin of D7 (IN2) | any, marked | 40 cm Dupont jumper, intact | Right motor direction. |
| L298N driver: IN3 and IN4 pins | S pin of D8 (IN3) and S pin of D12 (IN4) | any, marked | 40 cm Dupont jumper, intact | Left motor direction. |
| L298N driver: ENB pin | S pin of D6 on the Sensor Shield | any, marked ENB | 40 cm Dupont jumper, intact | With the ENB jumper removed; the same caution as for ENA applies. |
| Right encoder: yellow wire | S pin of D2 on the Sensor Shield | yellow | half of a jumper soldered to the cable wire | The motor label doesn’t say which of the 2 wires, yellow or green, is channel A. If the count goes the wrong way, you can correct that in the program. |
| Right encoder: green wire | S pin on the Sensor Shield A0 connector | green | half of a jumper soldered to the cable wire | The A0 and A1 connectors are in the shield’s ANALOG IN row; check that your board has the pins standing upright there. |
| Left encoder: yellow wire | S pin on Sensor Shield D3 | yellow | half of a jumper soldered to the cable wire |  |
| Left encoder: green wire | S pin on the Sensor Shield A1 connector | green | half of a jumper soldered to the cable wire |  |

### Serial connection between the Raspberry Pi and Arduino

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Raspberry Pi: pin 32 (GPIO12, TX) | Through the neck to the S pin of D0 (RX) on the Sensor Shield | green | 40 cm Dupont jumper, intact | Direct: the Pi's 3.3 V already counts as a high level for Arduino. |
| Raspberry Pi: pin 34 (GND) | Through the neck, to the G pin on D0 of the Sensor Shield | black | 40 cm Dupont jumper, intact |  |
| Raspberry Pi: pin 33 (GPIO13, RX) | Through the neck, to terminal 3 on the terminal block | blue | 40 cm jumper wire with one end cut and stripped | This wire never goes straight to D1: that’s 5 V on a 3.3 V pin. |
| Terminal block, terminal 3 | 1 kΩ resistor and, after it, the S pin on D1 (TX) of the Sensor Shield | blue | Half a jumper, soldered to the resistor lead, with the female connector on the shield | Assembled on the workbench, in prep step 3. |
| Terminal block, terminal 3 | 2 1 kΩ resistors in series and, after them, terminal 2 on the block (negative) | no wire | resistor leads | The 3 resistors form the voltage divider: 5 V becomes 3.3 V. |
| 5-inch screen | Raspberry Pi: micro-HDMI output (the one closest to the USB-C port) and a USB port | no wire | short flat HDMI cable and short USB cable | The screen doesn’t use the Pi’s pins. The 2 cables stay inside the head and aren’t in the 3D model. |
<!-- /GERADO -->

## Prep Step 1: Solder the Power Circuit and Set Both Voltages

Do this at the workbench, with the printed base and deck side by side. The switch is the first part to go into the base, and it goes in before
being soldered to the rest. The solder pad names vary from board to board, and the names on the boards used in this robot were not read:
the store page for the 3-cell protection board does not show the names, and the 2 middle solder pads in the charger photo
are unreadable. So this guide describes the connections by what they are (positive, negative, upper junction,
lower junction) and tells you to check each one with a multimeter.

The charger comes set up for 2 cells. The store page shows, in one figure, what changes for 3 cells: one resistor
removed and one jumper closed with solder, beside the ROV marking
([charger page](https://www.usinainfo.com.br/fonte-de-alimentacao/carregador-de-baterias-18650-litio-2s3s-com-balanceamento-usb-c-lx-usc-v2-8996.html)).
It is a very small solder joint. Plan B, without modifying the charger: remove the 3 cells through the battery hatch and charge them in a
regular 18650 charger.

<!-- GERADO:prep1 -->
1. With the 3 cells out of the holder, solder 2 yellow 20 cm wires to each of the 2 metal strips joining the cells: these are the pack’s 2 junctions, and each one has one wire going to the protection board and another to the charger. Mark the 2 wires from the junction on the red-wire side of the holder with tape: this is the upper junction.
2. Set up the charger for 3 cells, following the picture on the store page: remove the tiny resistor shown and bridge the jumper next to the ROV label with a small drop of solder. Without this, it only charges up to 8.4 V. If you’re not used to working with such small solder joints, don’t use this charger: remove the 3 cells through the battery hatch and charge them in a regular 18650 charger.
3. Solder 2 red 20 AWG wires, 15 cm long, to the switch’s 2 terminals. Feed the free ends through the cutout at the back of the base, from outside in, and fit the switch into the cutout. Do this BEFORE soldering the switch to the rest: once connected to the wiring harness, it won’t fit through the 13.5 × 9 mm cutout.
4. With the base beside you as a guide for wire length, connect the holder, fuse, protection board, and charger according to the wiring table. Leave about 15 cm of slack in the holder’s 4 wires: it moves down with the battery hatch when you replace the cells.
5. Solder one end of the switch to the protection board’s positive output (P+). Strip 6 mm from the other end: it goes to terminal 4. Solder a 20 cm black 20 AWG wire to the negative output (P−) and strip its free end: it goes to terminal 5.
6. Now prepare the deck, still outside the robot. Cut a piece with 5 terminals from the terminal block and number them 1 to 5. Solder 2 short 20 AWG wires to the XL4015 input and tighten the other ends in the terminal block: IN+ to terminal 4, IN− to terminal 5. Connect the UBEC’s red input wire to terminal 4 and its black wire to terminal 5.
7. Remove the 3 jumpers (the plastic caps) from the L298N motor driver: the 2 marked ENA and ENB and the 5 V regulator jumper next to the power screw terminal. Then, on the same side of the terminal block, tighten a red 20 AWG wire from terminal 4 to the driver's +12V terminal and a black wire from terminal 5 to the driver's GND terminal.
8. At the XL4015 output, solder 2 short 20 AWG wires and tighten the other ends in the terminal block: OUT+ to terminal 1, OUT− to terminal 2. Do not connect anything else to the outputs.
9. Place the base and deck side by side. On the other side of the terminal block, tighten the red wire from the switch into terminal 4 and the black wire from the protection board into terminal 5.
10. Put the 3 cells in the holder, checking which way the positive ends face. With the multimeter, measure from the holder’s black wire to each yellow wire: about 4 V at the lower junction and about 8 V at the upper junction (the one marked with tape). Turn on the switch.
11. Measure between terminals 4 and 5: it should read 9 to 12.6 V, with red on positive.
12. With the multimeter across terminals 1 and 2, turn the XL4015 adjustment screw with the screwdriver until it reads 5.1 V. It takes several turns.
13. Measure the UBEC output: it should read 6 V. If it reads 5 V, move its jumper to 6 V.
14. Turn off the switch.
<!-- /GERADO -->

## Prep Step 2: Upload the Program and Set Both Servos to 90°

The program is the sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). It moves both servos to
the center, keeps them there, and leaves the wheel motors off.

<!-- GERADO:prep2 -->
1. Open the `centrar_servos.ino` sketch in Arduino IDE. Connect the Arduino Uno to the computer with the USB cable, without the shield or battery.
2. From the Tools menu, select the Arduino Uno board and the port it appeared on. Click Upload.
3. Unplug the USB cable, fit the Sensor Shield onto the Uno, and remove the shield’s SEL jumper: it is the small plastic cap over 2 pins, next to the blue screw terminal.
4. Reconnect the USB cable just to take a measurement with the multimeter. The shield's COM connector has 4 upright pins labeled TX, RX, −, and +. You should get about 5 V between + and −. On the D9 connector, you should get 0 V between the V pin and the G pin.
5. If the D9 V pin reads 5 V, the SEL jumper is still in place. If the COM + pin does not read 5 V, your shield differs from the store photo: look for another pin labeled + or 5V that reads 5 V with SEL removed. A wrong pin here sends the servos' 6 V to the Raspberry Pi.
6. Unplug the USB cable.
7. The UBEC output has a 3-pin servo plug: cut it off and strip the wires. Red is positive and black (or brown) is negative. If there’s a third wire, white or orange, insulate its end with heat-shrink tubing. Clamp the red wire into VCC and the black wire into GND on the blue screw terminal. The 1000 µF capacitor goes into the same terminal, with its longer lead in VCC.
8. Take 2 40 cm jumper wires, cut the connector off one end of each, and strip the wires. Clamp one in terminal 1 of the terminal block, opposite the converter, and plug its connector into the + pin on the COM connector. Connect the other from terminal 2 to the − pin on the same connector. Leave the TX and RX pins beside it empty: 5 V on one of them reaches the Raspberry Pi through the serial wire.
9. Connect the pan servo to D9 and the tilt servo to D10: brown or black wire to G, red to V, orange or yellow to S.
10. Turn on the switch: both servos move to the center (90°) and the Uno LED blinks once per second. The motor driver is not connected to the Arduino yet: the wheels will not move.
11. Turn off the switch. From now on, do not turn the servo shafts by hand.
12. Disconnect the test setup for assembly: remove the 2 servos from D9 and D10, disconnect the UBEC wires and capacitor from the blue terminal, and remove the 2 jumpers from the COM connector. Disconnect the 2 wires from the base from terminals 4 and 5: you will reconnect them during assembly, after passing them through the slot in the deck. If the shield covers the Uno mounting holes, remove it too. Take the 3 cells out of the holder: they go back in during assembly, in the battery step.
<!-- /GERADO -->

Three notes:

- Do not power the MG996R servo from the USB 5 V. The USB port supplies 0.5 A, and the servo needs more than that when starting.
- Never connect the computer's USB cable while the battery is on: the two power sources would be in parallel.
- Upload the sketch before closing the robot. Afterward, to reach the Arduino USB port, you must remove the 4 bottom screws and lift the torso.

The sketch compiles for the Arduino Uno (arduino-cli, core arduino:avr 1.8.8, Servo library 1.3.0). It has not yet been
run on an assembled robot.

## Prep step 3: make the serial, Raspberry Pi, motor driver, and encoder cables

The Raspberry Pi is in the head and the Arduino is on the deck. They communicate over 3 wires running down the neck: green, blue,
and black. The pair of wires that powers the Pi runs up through the same neck. On the deck, the Arduino controls the motor driver with 6 wires and reads
the 2 encoders with 4. There are 16 40 cm jumpers in the whole robot; a 40-piece kit leaves some over. Do this prep step with the cells
out of the holder.

<!-- GERADO:prep3 -->
1. Serial. Set aside 3 40 cm jumpers: one green, one blue, and one black (or mark 3 jumpers of another color with tape). Leave the green and black ones intact, with both female connectors. On the blue one, cut off ONE connector and strip 6 mm: this end goes into a terminal.
2. Find the pins on the Raspberry Pi: pin 1 is at the corner beside the microSD card, in the inner row; pin 40 is at the opposite corner, in the outer row. Odd-numbered pins are in the inner row and even-numbered pins are in the outer row. Pins 2, 4, and 6 are the first 3 in the outer row; pin 9 is the 5th in the inner row. Pins 32 and 34 are the 16th and 17th in the outer row; pin 33 is the 17th in the inner row.
3. Mark the end of each serial jumper that goes to the Pi with tape: green = pin 32, blue = pin 33, black = pin 34.
4. Divider. Solder 2 1 kΩ resistors together, leg to leg, and cover the splice with heat-shrink tubing. This pair is 2 kΩ.
5. Cut a jumper in half. Solder the cut end of one half to a leg of the 3rd resistor and cover it with heat-shrink tubing. The female connector on this half goes to D1.
6. On the terminal block, on the converter side, tighten the free leg of the 3rd resistor together with one end of the 2 kΩ pair in terminal 3. Tighten the other end of the pair in terminal 2, together with the black wire already there. Bend the end of each leg before tightening, so the screw grips it.
7. Check with the multimeter in ohms: between the D1 jumper’s female connector and terminal 3, about 1 kΩ; between terminal 3 and terminal 2, about 2 kΩ.
8. Raspberry Pi power. Cut 2 jumpers in half: you’ll have 4 halves with female connectors. Cut 45 cm of red wire and 45 cm of black 20 AWG wire. Solder 2 halves to the end of the red wire and 2 to the end of the black wire, and cover each splice with heat-shrink tubing. Mark the 2 red ones with tape: they go to pins 2 and 4 (5 V). The 2 black ones go to pins 6 and 9 (GND). Strip 6 mm from the other end of each wire: they go to terminals 1 and 2.
9. Motor driver. Its 3 jumpers were already removed in prep step 1. Where the ENA and ENB jumpers were, there are 2 pins in each spot: one is the input (ENA or ENB) and the other is connected to the board's 5 V. With the multimeter set to continuity and the switch off, find the pin in each pair that beeps with the driver's +5V terminal: leave that one empty. Mark the other with a pen: that's where the Arduino wire goes. A wire from the Arduino to a 5 V pin can burn out the Arduino output.
10. Set aside 6 intact jumpers for the motor driver signals and label each one with tape: ENA, IN1, IN2, IN3, IN4, and ENB.
11. Tighten a 15 cm red 22 AWG wire into terminal 1 of the terminal block, on the side opposite the converter. The other end goes to the driver’s +5V terminal during assembly, along with the encoders’ blue wires.
12. Encoders. Each motor comes with a 6-wire cable. Plug the cable into the motor and cut off the connector at the other end. Strip 6 mm from the red, white, blue, and black wires: they go into terminals. On the yellow and green wires, solder a half jumper with a female connector to each one (that’s 2 more jumpers cut in half) and cover with heat-shrink tubing. Mark the cables: right and left.
13. Set the cables aside. During assembly, everything connects through a terminal or plug, with no soldering. Note: on the shield’s 3-pin connectors, only pin S (signal) gets a signal wire. The middle pin (V) always stays empty: with the SEL jumper removed, it carries the servos’ 6 V, and 6 V on a signal wire will burn out the Raspberry Pi or encoder.
<!-- /GERADO -->

Why a standard Dupont connector works here: this robot’s screen does not plug into the Raspberry Pi pins. There is about 20 mm between the Pi and the
screen (model measurement, not confirmed), and the Dupont connector is 14 mm long. If it does not fit in your screen, bend the wires just above
the connector or solder the wires to a piece of female pin header, with the wires coming out to the side.

Where pin 1 is and why the pin number is not the GPIO number:
[Raspberry Pi documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc).
On a powered-on Pi, the `pinout` command draws the pin map.

Each motor cable is about 14 cm long
([motor table at a store](https://rcdrone.top/products/jgb37-520-dc-gear-motor-with-encoder)). If any wire does not
reach the motor driver or shield, splice on a piece of 22 AWG wire with solder and heat-shrink tubing during this prep step.

## Prep step 4: flash the microSD card, test the screen, and connect the serial link

You write the card on your computer using a microSD card reader. Then you connect to the Raspberry Pi over the network,
using SSH: you type commands on your computer, and they run on the Pi.

<!-- GERADO:prep4 -->
1. Install Raspberry Pi Imager, the free Raspberry Pi program, on your computer, and put the card in the reader.
2. In Imager, choose your Pi model, the Raspberry Pi OS (64-bit) operating system, and the card.
3. Before flashing, open Imager’s settings: give the Pi a name (for example, `robo`), create a username and password, enter your Wi-Fi name and password, and enable SSH. Flash the card.
4. Put the card in the Pi. For this test only, connect the screen to it with the HDMI cable and USB cable, and power the Pi with a 5 V, 3 A USB-C supply. Wait about 2 minutes: the screen should show the system. The manufacturer says it works with Raspberry Pi OS without installing a driver.
5. On your computer, open the terminal: on Windows, use the PowerShell program; on Mac and Linux, use Terminal.
6. Type `ssh usuario@robo.local`, replacing `usuario` and `robo` with the names you created. Answer `yes` the first time and enter the password.
7. If `robo.local` doesn’t respond, open your router’s page, find the Pi in the list of connected devices, and use its number (the IP address), for example `ssh usuario@192.168.0.50`.
8. When the terminal shows the Pi’s name, you’re in. Connect the serial: type `sudo nano /boot/firmware/config.txt`, go to the end of the file, and add a line: `dtoverlay=uart5` on Raspberry Pi 4, or `dtoverlay=uart4-pi5` on Raspberry Pi 5. Save with Ctrl+O and Enter, then exit with Ctrl+X.
9. Type `sudo poweroff`, wait for the Pi’s green LED to stop blinking, unplug the power supply, and disconnect the 2 screen cables: you’ll reconnect them during assembly.
<!-- /GERADO -->

The screen is the Waveshare 5inch HDMI LCD (B): 5 inches, 800 × 480, connected through HDMI, with a USB cable for power. The
manufacturer says it works with Raspberry Pi OS without a driver
([manufacturer page](https://www.waveshare.com/5inch-hdmi-lcd-b.htm)). If the image does not fill the screen, see the
[manufacturer wiki](https://www.waveshare.com/wiki/5inch_HDMI_LCD_%28B%29). Not bench-tested. Raspberry Pi documentation on
GitHub: [SSH](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/ssh.adoc) and [how to find the Pi's address](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/find-your-ip-address.adoc).

The serial line comes from the [Raspberry Pi firmware overlays list](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
After restarting, the port name appears with `ls /dev/ttyAMA*`. The program that uses this serial connection is part of phase 2.

## The Screen Cables

The screen connects to the Raspberry Pi with 2 cables inside the head: an HDMI cable and a USB cable. They are not part of the 3D model.

- The Raspberry Pi 4 has a micro-HDMI port on the bottom edge of the board. According to the model, there is about 22 mm from there to the bottom of the head.
- The Pi's USB ports face right. According to the model, there is about 30 mm to the wall of the head.
- The cables that come with the screen are straight and long, and they don't fit in these spaces. That's why the parts list calls for a short flat HDMI cable with an angled micro-HDMI plug and a short USB cable with an angled USB-A plug.
- Check both cables with the parts in hand before closing the head. This is the main fit risk for this robot.

## How the Raspberry Pi Communicates with the Arduino

The neck cable hole is 9 mm wide, and a USB plug will not fit through it. That is why the two boards communicate over a 3-wire
serial connection (UART).

- **On the Arduino:** pins D0 (RX) and D1 (TX), the board's actual serial port. It doesn't interfere with the servo signal.
- **On the Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX), and pin 34 (GND).
- **Pin number and GPIO number:** "pin 32" is the position in the row of 40 pins, counted from the microSD card corner. "GPIO12" is the name of the signal that comes out of that pin. The two numbers are different.
- **Voltage:** the Arduino runs at 5 V and the Pi at 3.3 V. The wire from the Arduino to the Pi passes through a divider made of 3 1 kΩ resistors, which lowers 5 V to 3.3 V. The wire from the Pi to the Arduino is direct.
- **Why resistors instead of a level converter module:** the divider uses 3 resistors attached to the terminal block, without another loose board on the deck.

## How the Arduino Controls the Motors

The L298N motor driver has 6 control pins. The Arduino uses 6 Sensor Shield connectors, always only the S pin.

- **Speed:** ENA on D5 (right motor) and ENB on D6 (left motor). These two Arduino pins can vary the motor power, and the servo library doesn't use them. Remove the driver's ENA and ENB jumpers: with them in place, the motor is always at full power.
- **Direction:** IN1 on D4 and IN2 on D7 (right motor); IN3 on D8 and IN4 on D12 (left motor).
- **The driver's 5 V:** remove the driver's 5 V regulator jumper, and connect its +5V screw terminal to the 5.1 V from the terminal block. This way, the driver's control section doesn't depend on the pack voltage.
- **Encoders:** each motor has a sensor that outputs 2 signals. The yellow wire goes to D2 (right) and D3 (left), the two Arduino pins that notify the program at every pulse. The green wire goes to A0 (right) and A1 (left). The encoder outputs 11 pulses per motor revolution, before the 1:56 reduction (store table cited above).
- **Encoder power:** 3.3 to 5 V, through the blue (positive) and black (negative) wires. They go to the driver's +5V and GND screw terminals. Never connect them to the shield's V pin, which has the servos' 6 V.

While the `centrar_servos.ino` sketch is uploaded, the driver's 6 pins stay low and the wheels don't turn.
The program that makes the robot move is for phase 2.

## The 8 Wires That Pass Through the Neck

There are 8 wires: 2 power wires (5.1 V from the Raspberry Pi, 20 AWG), 3 serial wires, and the 3 wires from the tilt servo cable. They must be
connected inside the head BEFORE the head shell, because the Raspberry Pi is enclosed afterward. They also can’t hang down
under the fork at this point, because the bottom of the head shell passes beneath it. Follow this order:

1. When assembling the Raspberry Pi, before installing the panel with the screen, connect the 3 serial jumpers to pins 32, 33, and 34, and the 4 power cable connectors to pins 2, 4, 6, and 9.
2. With the head still open (frame, screen, tilt servo, and fork in place), check these 7 connectors and the 2 screen cables.
3. Connect the 30 cm extension to the tilt servo cable.
4. Feed the 8 wires through the 9 mm hole in the fork, from top to bottom. Feed the extension connector first; it is 7.6 mm wide and fits snugly.
5. Stop when the ends are flush with the bottom face of the fork. Leave about 5 cm of extra wire inside the head: it tilts around the fork.
6. Close the head with the head shell. Use tweezers to pull the ends of the 8 wires out through the slot at the bottom of the shell.
7. Feed the wires through the neck tube and seat the head on it.
8. On the deck, with the switch off and before soldering: connect the 2 wires carrying 5.1 V to terminals 1 and 2 on the terminal block; the blue wire to terminal 3; the green connector to the S pin on D0 and the black one to the G pin on D0; the divider jumper to the S pin on D1; the servo extension to D10.

Leave about 10 cm of slack inside the torso: the neck turns almost a full rotation and twists the wires. This routing has never been
tried with the printed parts.

## Current, Wire, and Fuse

The values below are calculated from the specifications, not measured.

- Normal use: about 2 A from the pack. The Raspberry Pi with the screen draws about 1.5 A at 5.1 V, the servos draw less than 1 A at 6 V, and each motor draws about 0.2 A while moving.
- Worst case: about 6.5 A, with both wheels stalled (1.2 A each, according to the motor table), the UBEC at its 3 A limit, the XL4015 at 3 A, and the pack at 9 V.
- KCD11-101 switch: 3 A at 250 V~ and 6 A at 125 V~ ([store spec sheet](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). The spec sheet doesn't list a continuous current rating.
- 3 A fuse: this is the switch's lowest rating. Normal use stays below it, and a sustained overload blows the fuse before the switch heats up.
- **The switch is this robot's weakest point.** If it pushes against an obstacle while the servos are under strain, the current exceeds 3 A and the fuse may blow. Replacing it with a higher-rated switch requires changing the 13.5 × 9 mm cutout in the base, so this remains an open project item.
- Time-delay fuse (marked T3A or T3.15A): the motors and servos starting up and the 1000 µF capacitor charging create spikes lasting a fraction of a second. A fast-acting fuse may blow during these spikes even if there is no fault; the time-delay fuse tolerates the brief spike and blows during a sustained overload (typical behavior for this type of fuse; not confirmed by measurement).
- If the fuse blows during normal use, don't install a higher-rated one: measure the current and find what is causing the strain.
- L298N motor driver: 2 A per channel (value from the store listing). A stalled motor draws 1.2 A, within this limit.
- 20 AWG wire (0.5 mm²) from the pack to the terminal block, from the block to the converter and driver, and in the 5.1 V pair going up to the Raspberry Pi: at 1.5 A, the calculated voltage drop in this pair is about 0.05 V. The combined voltage drop across the Dupont connector contacts has not been measured. Use 22 AWG wire (0.33 mm²) for the rest of the power wiring.
- If the Raspberry Pi reports undervoltage, shorten the 5.1 V pair and check the adjustment. To check, type `vcgencmd get_throttled` on the Pi: the good response is `throttled=0x0`.
- The phase 2 program must accelerate and brake gradually and must not make the motors and servos strain at the same time.

## Heat inside the head

The Raspberry Pi 4 is enclosed in the head, which is made of PLA and has no ventilation openings. This is an unmeasured risk.

- PLA softens near 60 °C (typical value; measurement not confirmed).
- The Pi reduces processor speed when its temperature is between 80 and 85 °C ([Raspberry Pi documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)).
- Stick the adhesive heatsinks onto the Pi chips before assembly.
- With the robot powered on for half an hour, type `vcgencmd measure_temp` on the Pi. If it goes above 70 °C, print the head shell in PETG or add ventilation holes in the back wall.

## First time you turn on the assembled robot

1. Switch off. Set the multimeter to continuity mode and check that the pack's positive and negative wires are not shorted.
2. Place the robot on a block, with both wheels in the air.
3. Before tightening the 2 wires coming down from the Raspberry Pi onto the terminal block, turn on the switch and measure at the block: 5.1 V between terminals 1 and 2, with the red lead on positive, and 9 to 12.6 V between terminals 4 and 5. Measure 6 V at the blue terminal. Switch off.
4. Tighten the Pi wires onto the block, red to terminal 1 and black to terminal 2, and turn the switch back on.
5. The Arduino LED blinks, both servos hold center, the wheels stay still, the Raspberry Pi power LED turns on, and the screen shows the system after about 1 minute.
6. If nothing lights up, switch off and check the fuse.

## What has not been tested yet

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

What to buy: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
