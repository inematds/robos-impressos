# Electrical wiring for the square desktop robot

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**Not bench-tested.** This diagram is based on the component datasheets; no wires have been connected to an assembled robot yet.
Check every connection with a multimeter before turning on the switch. If your board has a different name printed on it than
the one shown here, use the name printed on the board.

![Wiring diagram for the square desktop robot: battery, fuse, protection board, charger, switch, converters, Arduino with Sensor Shield, servos, Raspberry Pi, and display](ligacao.en.svg)

Page with the same diagram: https://inematds.github.io/robos-impressos/guia/en/cubo/#energia

All soldering for the robot is done on the workbench, in prep steps 1, 2, and 3. During assembly, you only use screw terminals and plug-in connections. The numbered steps in the 4 prep steps are the same as on the page.

## Lithium Battery Safety

- **Polarity:** red to positive, black to negative. Measure with the multimeter before each new connection. A reversed wire will burn out the board immediately.
- **Adjust before connecting the load:** set the LM2596 to 5.1 V and the UBEC to 6 V, measured with the multimeter, with no Raspberry Pi, Arduino, or servos connected.
- **A short circuit can start a fire:** solder with the cells OUT of the holder and insulate each splice with heat-shrink tubing. No metal can be exposed.
- **Fuse:** 3 A, slow-blow (marked T3A), on the positive wire, a few centimeters from the battery holder.
- **Matching cells:** use two new 18650 cells from the same brand and model. A dented, swollen, or hot cell goes to battery recycling, not into the robot.
- **First charge:** stay nearby, with the robot on a nonflammable surface.

## What Powers What

- **2S pack:** two 18650 cells in series, from 6 V (empty) to 8.4 V (full). It goes through the fuse and the protection board (BMS).
- **USB-C charger:** connected to the protection board output, before the switch. Charge the robot while it is off, using a USB-C power supply of 15 W or more.
- **Switch:** cuts the positive wire that goes to both converters.
- **LM2596, set to 5.1 V:** the output goes to a terminal block in the base. From there, one pair powers the Raspberry Pi (through the USB-C adapter with screw terminals), and another pair powers the Arduino (through the + and − pins of the Sensor Shield COM connector).
- **UBEC at 6 V:** powers only the 2 servos through the blue screw terminal on the Sensor Shield, with the SEL jumper removed.
- **Negative (GND):** one shared ground for the entire robot.

Why the Arduino gets 5.1 V from the LM2596 instead of the battery voltage: the Arduino Uno VIN input requires 7 to 12 V
([Arduino Uno R3 datasheet](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)), and the pack stays below 7 V for a good
part of its discharge.

## The terminal strip

It is a screw terminal strip (sindal type) that sits loose in the base. You use 3 of its terminals:

- **Terminal 1, the 5.1 V:** on one side, the red wire from the LM2596. On the other, the red wire going up to the Raspberry Pi and the jumper going to the + pin of the shield's COM connector.
- **Terminal 2, the negative:** on one side, the black wire from the LM2596 and one end of the resistor pair. On the other, the black wire going up to the Raspberry Pi and the jumper going to the − pin of the COM connector.
- **Terminal 3, the serial connection:** on one side, the voltage divider resistors. On the other, the blue wire coming down from the Raspberry Pi.

## Wiring Table, Wire by Wire

<!-- GERADO:ligacoes -->
### Battery, protection, and charging

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Battery holder: red wire (pack positive) | 3 A fuse holder and, after it, the protection board B+ solder pad | red | 22 AWG | The fuse goes a few centimeters from the holder. |
| Battery holder: black wire (pack negative) | B− solder pad on the protection board | black | 22 AWG |  |
| Battery holder: metal strip that joins the 2 cells (middle point) | Middle solder pad on the protection board (BM or B1) | yellow | 22 AWG | This is the 3rd wire. Solder it to the strip with the cells OUT of the holder. |
| Middle solder pad on the protection board (BM or B1) | BM solder pad on the USB-C charger | yellow | 22 AWG | Without this wire, the charger cannot balance the two cells. |
| B+ solder pad on the USB-C charger | Positive output of the protection board (P+; if the board has no P+, use the B+ solder pad itself) | red | 22 AWG | The charger goes before the switch: the robot charges while switched off. |
| B− solder pad on the USB-C charger | Negative output of the protection board (P−; on the board from the store checked, the C− solder pad) | black | 22 AWG | Do not connect to the B− solder pad on the protection board: charging must pass through the protection circuit. |

### Switch and converters

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Positive output of the protection board (P+ or B+) | On/off switch and, after it, LM2596 IN+ input and UBEC red input wire | red | 22 AWG | The switch cuts only the positive. |
| Negative output of the protection board (P−; on the board from the store checked, the C− solder pad) | LM2596 IN− input and UBEC black input wire | black | 22 AWG | This is the common negative (GND) for the entire robot. |

### 5 V: Raspberry Pi and Arduino

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| LM2596 OUT+ output (5.1 V) | Terminal block, screw terminal 1 | red | 20 AWG, short | Adjust the 5.1 V BEFORE connecting anything on the other side of the terminal block. |
| LM2596 OUT− output | Terminal block, screw terminal 2 | black | 20 AWG, short |  |
| Terminal block, screw terminal 1 (5.1 V) | Up through the neck, to the + screw terminal on the USB-C adapter, which plugs into the Raspberry Pi's USB-C port | red | 20 AWG | Use the thickest, shortest wire you can: a thin wire will make the Pi report undervoltage. |
| Terminal block, screw terminal 2 (negative) | Up through the neck, to the − screw terminal on the USB-C adapter | black | 20 AWG |  |
| Terminal block, screw terminal 1 (5.1 V) | Sensor Shield COM connector + pin | red | Dupont jumper with one end cut and stripped | This is how the Arduino receives power. First, with the Uno powered only by USB and the SEL jumper removed, use a multimeter to confirm that this pin reads about 5 V and the D9 V pin reads 0 V. The wrong pin here sends the servos’ 6 V to the Raspberry Pi. |
| Terminal block, screw terminal 2 (negative) | Sensor Shield COM connector − pin | black | Dupont jumper with one end cut and stripped |  |

### 6 V: servos

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| UBEC red output wire (6 V) | Sensor Shield blue VCC screw terminal | red | UBEC wire | Shield SEL jumper REMOVED and UBEC jumper set to 6 V. |
| UBEC black output wire | Sensor Shield blue GND screw terminal | black | UBEC wire |  |
| 1000 µF capacitor: long leg (+) | Blue VCC screw terminal; the striped leg (−) goes to the blue GND screw terminal | no wire | capacitor leads | The capacitor will explode if connected backwards. |
| Pan servo (at the base) | Sensor Shield D9 connector | servo cable | 3-wire servo cable | G = brown or black, V = red, S = orange or yellow. |
| Tilt servo (in the head) | Through the neck, using the 30 cm extension, to the Sensor Shield D10 connector | servo cable | 3-wire servo cable | Same color order as D9. |

### Serial connection between the Raspberry Pi and Arduino

| From | To | Color | Wire | Attention |
|---|---|---|---|---|
| Raspberry Pi: pin 32 (GPIO12, TX), on the lower 2 × 2 connector | Through the neck to the S pin of D0 (RX) on the Sensor Shield | green | 40 cm jumper: one end soldered to the 2 × 2 connector, the other with the female connector | Direct: the Pi's 3.3 V already counts as a high level for Arduino. |
| Raspberry Pi: pin 34 (GND), on the lower 2 × 2 connector | Through the neck, to the G pin on D0 of the Sensor Shield | black | 40 cm jumper: one end soldered to the 2 × 2 connector, the other with the female connector |  |
| Raspberry Pi: pin 33 (GPIO13, RX), on the lower 2 × 2 connector | Through the neck, to terminal 3 on the terminal strip | blue | 40 cm jumper: one end soldered to the 2 × 2 connector, the other cut and stripped | This wire never goes straight to D1: that’s 5 V on a 3.3 V pin. |
| Terminal strip, terminal 3 | 1 kΩ resistor and, after it, the S pin on D1 (TX) of the Sensor Shield | blue | Half a jumper, soldered to the resistor lead, with the female connector on the shield | Assembled on the workbench, in prep step 3. |
| Terminal strip, terminal 3 | 2 1 kΩ resistors in series and, after them, terminal 2 on the terminal strip (negative) | no wire | resistor leads | The 3 resistors form the voltage divider: 5 V becomes 3.3 V. |
| MPI3501 screen | Fitted onto Raspberry Pi pins 1 to 26 | no wire | the screen's own connector | Uses SPI and the 5 V from pins 2 and 4. |
<!-- /GERADO -->

## Prep Step 1: Solder the Power Circuit and Set Both Voltages

Do this on the workbench, with the printed base beside you. The switch is the first part to go into the base, and it goes in before being soldered
to the rest. Solder pad names vary from board to board. On the charger, they are B+, BM, and B−. On the protection board from the store
we checked, only the back has labels: B+, B1 (middle), B−, and C−. From the photo, C− appears to be the negative output and B+ itself the positive output; this is a reading of the photo, not confirmed: check with a multimeter. On the Sensor Shield from the same store, the photo shows
the COM connector with 4 upright pins (TX, RX, −, and +) and the SEL jumper beside the blue screw terminal.

<!-- GERADO:prep1 -->
1. Solder the 3rd wire (yellow) to the metal strip joining the two cells, with the cells out of the holder.
2. Solder 2 red 10 cm wires to the 2 switch terminals. Pass the free ends through the cutout in the base, from the outside in, and fit the switch into the cutout. Do this BEFORE soldering the switch to the rest of the wiring: once connected to the wiring harness, it won’t fit through the 13.5 × 9 mm cutout.
3. With the base beside you as a guide for wire lengths, connect the support, fuse, protection board, and charger according to the wiring table.
4. Solder one end of the switch to the protection board’s positive output. Solder the other end to the LM2596 IN+ input and the UBEC red input wire. Connect the negatives of both inputs to the protection board’s negative output.
5. At the LM2596 output, solder 2 short 20 AWG wires and tighten their other ends in the terminal block: red in screw terminal 1, black in screw terminal 2. Do not connect anything else to the outputs.
6. Put the cells in the holder, checking which side is positive, and turn on the switch.
7. With the multimeter connected to the terminal block, turn the LM2596 adjustment screw with the screwdriver until it reads 5.1 V. It takes several turns.
8. Measure the UBEC output: it should read 6 V. If it reads 5 V, move its jumper to 6 V.
9. Turn off the switch.
<!-- /GERADO -->

## Prep Step 2: Upload the Program and Set Both Servos to 90°

The program is the sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). It moves both servos to
the center and holds them there.

<!-- GERADO:prep2 -->
1. Open the `centrar_servos.ino` sketch in Arduino IDE. Connect the Arduino Uno to the computer with the USB cable, without the shield or battery.
2. From the Tools menu, select the Arduino Uno board and the port it appeared on. Click Upload.
3. Unplug the USB cable, fit the Sensor Shield onto the Uno, and remove the shield’s SEL jumper: it is the small plastic cap over 2 pins, next to the blue screw terminal.
4. Reconnect the USB cable just to take a measurement with the multimeter. The shield's COM connector has 4 upright pins labeled TX, RX, −, and +. You should get about 5 V between + and −. On the D9 connector, you should get 0 V between the V pin and the G pin.
5. If the D9 V pin reads 5 V, the SEL jumper is still in place. If the COM + pin does not read 5 V, your shield differs from the store photo: look for another pin labeled + or 5V that reads 5 V with SEL removed. A wrong pin here sends the servos' 6 V to the Raspberry Pi.
6. Unplug the USB cable.
7. Connect the UBEC’s 6 V to the blue screw terminal (VCC and GND) and the 1000 µF capacitor to the same terminal, with its long lead in VCC.
8. Take 2 40 cm jumper wires, cut the connector off one end of each, and strip the wires. Tighten one into terminal 1 on the terminal block, opposite the converter, and plug its connector into the + pin of the COM connector. The other goes from terminal 2 to the − pin of the same connector.
9. Connect the pan servo to D9 and the tilt servo to D10: brown or black wire to G, red to V, orange or yellow to S.
10. Turn on the switch: both servos move to the center (90°) and the Uno LED blinks once per second.
11. Turn off the switch. From now on, do not turn the servo shafts by hand.
12. Disconnect the test setup because the Uno is screwed onto the base without the shield: unplug the 2 servos from D9 and D10, remove the UBEC wires and capacitor from the blue screw terminal, remove the 2 jumpers from the COM connector, and unplug the shield. Everything goes back in place during assembly.
<!-- /GERADO -->

Three notes:

- Do not power the MG996R servo from USB 5 V. The USB port supplies 0.5 A, and the servo needs more than that when it starts.
- Never connect the computer's USB cable while the battery is on: the two power sources would be in parallel.
- Upload the sketch before screwing the Uno onto the base. Once it is in place, only about 10 mm remains between the USB connector and the wall, so the cable will not fit.

The sketch compiles for the Arduino Uno (arduino-cli, core arduino:avr 1.8.8, Servo library 1.3.0). It has not yet been
run on an assembled robot.

## Prep step 3: make the serial cable and resistor divider

The Raspberry Pi goes in the head and the Arduino in the base. They communicate over 3 wires that run down through the neck: green, blue,
and black. In this prep step, you solder these 3 wires to a low-profile connector that plugs into the Pi pins, and build the 3-resistor
divider on the terminal strip. The whole robot uses 6 40 cm jumpers: 3 in this cable, 1 cut in half for the
divider, and 2 that carry power to the Arduino (prep step 2). One 40 cm jumper will be left over from a kit.

<!-- GERADO:prep3 -->
1. With the wire cutters, cut a 2 × 2 piece from the female pin header: 2 rows with 2 holes each. This is the low-profile connector that goes on Raspberry Pi pins 31 to 34.
2. Set aside 3 40 cm jumpers: one green, one blue, and one black (or mark 3 jumpers of another color with tape). Cut the connector off ONE end of each and strip 3 mm.
3. Find the pins on the Raspberry Pi: pin 1 is at the corner next to the microSD card, on the inner row; pin 40 is at the opposite corner, on the outer row. Odd-numbered pins are on the inner row and even-numbered pins are on the outer row. Pins 31 and 32 are the 16th pair; pins 33 and 34 are the 17th.
4. Solder the 3 wire ends to the terminals of the 2 × 2 connector, with the wires lying flat and pointing to the side: green to the hole that will go on pin 32, blue to pin 33, black to pin 34. Leave the pin 31 terminal empty. Slide a piece of thin heat-shrink tubing over each solder joint.
5. Mark with a pen the corner of the connector where the empty terminal is, the one for pin 31. When you plug it in, the mark goes on the inner row, facing the microSD card. To check: there are 2 pairs of empty pins (27 to 30) between the connector and the display, and 3 pairs (35 to 40) on the other side. If the connector is reversed, it swaps the wires around.
6. On the blue wire, also cut off the connector at the other end and strip 6 mm: this end goes into a screw terminal. Leave the green and black wires with their female connectors, which fit onto the shield.
7. Now make the divider. Solder 2 1 kΩ resistors together, leg to leg, and cover the joint with heat-shrink tubing. This pair adds up to 2 kΩ.
8. Cut a jumper in half. Solder the cut end of one half to a leg of the 3rd resistor and cover it with heat-shrink tubing. The female connector on this half goes to D1.
9. On the terminal block, on the converter side, tighten the free leg of the 3rd resistor together with one end of the 2 kΩ pair in terminal 3. Tighten the other end of the pair in terminal 2, together with the black wire already there. Bend the end of each leg before tightening, so the screw grips it.
10. Check with the multimeter in ohms: between the D1 jumper’s female connector and terminal 3, about 1 kΩ; between terminal 3 and terminal 2, about 2 kΩ.
11. Set the cable aside: the 2 × 2 connector plugs into the Raspberry Pi during assembly, before the display. At the base, the blue wire goes to terminal 3 on the terminal block, the green wire to the S pin of D0, and the black wire to the G pin of D0; use screw terminals or plug-in connections, no soldering. Attention: on the 3-pin connectors for D0 and D1, always leave the middle point (V) empty. With the SEL jumper removed, it carries the servos' 6 V, and 6 V on a serial wire will burn out the Raspberry Pi.
<!-- /GERADO -->

Why use a low-profile connector: pins 31 to 34 sit under the display board, where about 17.5 mm of clearance remains (measurement not
confirmed). A standard 14 mm Dupont connector does not fit upright.

Where pin 1 is and why the pin number is not the GPIO number:
[Raspberry Pi documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/gpio-on-raspberry-pi.adoc).
On a powered-on Pi, the `pinout` command draws the pin map.

## Prep step 4: flash the microSD card, install the display driver, and connect the serial line

You write the card on your computer using a microSD card reader. Then you connect to the Raspberry Pi over the network,
using SSH: you type commands on your computer, and they run on the Pi.

<!-- GERADO:prep4 -->
1. Install Raspberry Pi Imager, the free Raspberry Pi program, on your computer, and put the card in the reader.
2. In Imager, choose your Pi model, the Raspberry Pi OS (64-bit) operating system, and the card.
3. Before flashing, open Imager’s settings: give the Pi a name (for example, `robo`), create a username and password, enter your Wi-Fi name and password, and enable SSH. Flash the card.
4. Put the card in the Pi, fit the screen onto pins 1 to 26 just for this test, and power on the Pi with a 5 V, 3 A USB-C power supply. Wait about 2 minutes.
5. On your computer, open the terminal: on Windows, use the PowerShell program; on Mac and Linux, use Terminal.
6. Type `ssh usuario@robo.local`, replacing `usuario` and `robo` with the names you created. Answer `yes` the first time and enter the password.
7. If `robo.local` doesn’t respond, open your router’s page, find the Pi in the list of connected devices, and use its number (the IP address), for example `ssh usuario@192.168.0.50`.
8. When the terminal shows the Pi’s name, you’re inside it. Type the three driver commands, one per line, pressing Enter after each: `git clone https://github.com/goodtft/LCD-show.git`, then `cd LCD-show`, then `sudo ./LCD35-show`. The Pi needs internet access. It restarts on its own and the screen turns on.
9. Connect again over SSH and enable the serial port AFTER the screen script, because it rewrites the configuration file. Type `sudo nano /boot/firmware/config.txt`, go to the end of the file, and add a line: `dtoverlay=uart5` on Raspberry Pi 4, or `dtoverlay=uart4-pi5` on Raspberry Pi 5. Save with Ctrl+O and Enter, then exit with Ctrl+X.
10. Type `sudo poweroff`, wait for the Pi’s green LED to stop blinking, unplug the power supply, and detach the screen: you’ll put it back during assembly.
<!-- /GERADO -->

The screen is the MPI3501: 3.5 inches, 480 × 320, ILI9486 controller, connected over SPI to pins 1 to 26. Sources:
[the MPI3501 page on lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display) (model, pins, and driver) and
Raspberry Pi documentation on GitHub: [SSH](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/ssh.adoc) and [how to find the Pi’s address](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/find-your-ip-address.adoc).
Not bench-tested: the manufacturer lists tests up to the Raspberry Pi 3B+, and the script replaces the Pi’s configuration file.

The serial line comes from the [Raspberry Pi firmware overlays list](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
After restarting, the port name appears with `ls /dev/ttyAMA*`. The program that uses this serial connection is part of phase 2.

Plan B, also not tested, if the screen stays white or blank:

- Instead of the script, add the line `dtoverlay=piscreen,drm` to the end of the `/boot/firmware/config.txt` file and restart. This is the official overlay for a 3.5-inch screen with the same ILI9486 controller ([overlay list](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README)); the source doesn’t guarantee that it works with the MPI3501.
- If it still doesn’t turn on, write the Raspberry Pi OS (Legacy) image to the card again and repeat the manufacturer’s script.

## How the Raspberry Pi Communicates with the Arduino

The neck cable hole is 9 mm wide, and a USB plug will not fit through it. That is why the two boards communicate over a 3-wire
serial connection (UART).

- **On the Arduino:** D0 (RX) and D1 (TX) pins, which are the board's actual serial connection. They do not interfere with the servo signal.
- **On the Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX), and pin 34 (GND). The screen uses pins 1 to 26; these three are free.
- **Pin number and GPIO number:** "pin 32" is the position in the row of 40 pins, counted from the microSD card corner. "GPIO12" is the name of the signal that comes out of that pin. The two numbers are not the same.
- **Voltage:** the Arduino runs at 5 V and the Pi at 3.3 V. The wire from the Arduino to the Pi passes through a 3-resistor 1 kΩ divider, which drops 5 V to 3.3 V. The wire from the Pi to the Arduino is direct.
- **Why resistors instead of a level converter module:** the divider does the job with 3 resistors attached to the terminal block, without another loose board in the base. The module would also work, but it needs a 3.3 V pin: the shield photo shows the 3V3 label, but it's not possible to confirm whether there is an upright pin there.

## The 8 Wires That Pass Through the Neck

There are 8 wires: 2 power wires (5.1 V from the Raspberry Pi, 20 AWG), 3 serial wires, and the 3 wires from the tilt servo cable. They must be
connected inside the head BEFORE the head shell, because the Raspberry Pi is enclosed afterward. They also can’t hang down
under the fork at this point, because the bottom of the head shell passes beneath it. Follow this order:

1. When assembling the Raspberry Pi, before installing the display, plug the serial cable's low-profile connector into pins 31 to 34.
2. With the head still open (frame, display, tilt servo, and fork in place), screw the 2 5.1 V wires into the USB-C adapter and plug it into the Raspberry Pi.
3. Connect the 30 cm extension to the tilt servo cable.
4. Feed the 8 wires through the fork's 9 mm hole, from top to bottom. Feed the extension connector first; it is 7.6 mm wide and fits snugly.
5. Stop when the wire ends are flush with the underside of the fork. Leave about 5 cm of extra wire inside the head: it tilts around the fork.
6. Close the head with the head shell. Use tweezers to pull the ends of the 8 wires out through the opening in the bottom of the shell.
7. Feed the wires through the neck tube and seat the head on top of it.
8. In the base, with the switch off and no soldering: connect the 2 5.1 V wires to terminals 1 and 2 of the terminal strip; the blue wire to terminal 3; the green connector to the S pin on D0 and the black connector to the G pin on D0; the divider jumper to the S pin on D1; and the servo extension to D10.

Leave about 10 cm of slack inside the base: the neck turns almost one full rotation and twists the wires. This routing has never been
tested with the printed parts.

## Current, Wire, and Fuse

The values below are calculated from the specifications, not measured.

- Normal use: about 2 A from the pack. The Raspberry Pi draws about 1 A at 5.1 V and the servos draw less than 1 A at 6 V.
- Peak: about 5 A, with the LM2596 at 2 A, the UBEC at its 3 A limit, and the pack at 6.5 V.
- KCD11-101 switch: 3 A at 250 V~ and 6 A at 125 V~ ([store specification](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). The specification does not list a continuous-current rating.
- 3 A fuse: this is the switch's lowest rating. Normal use stays below it, and a sustained overload blows the fuse before the switch overheats.
- Slow-blow fuse (marked T3A or T3.15A): starting the servos and charging the 1000 µF capacitor create peaks lasting a fraction of a second. A fast-acting fuse may blow during these peaks even when there is no fault; a slow-blow fuse tolerates the brief peak and blows during a sustained overload (typical behavior for this fuse type; measurement not confirmed).
- If the fuse blows during normal robot use, do not install a larger one: measure the current and find what is drawing too much.
- 22 AWG wire (0.33 mm²) for power in the base. 20 AWG wire (0.5 mm²) for the 5.1 V pair that runs up to the Raspberry Pi: at 2 A, the calculated voltage drop along this section is 0.06 V.
- The LM2596 can handle about 2 A continuously without a heatsink (typical value; measurement not confirmed). Use the Raspberry Pi 4, or the Pi 5 without USB accessories.
- If the Raspberry Pi reports undervoltage, shorten the 5.1 V pair and check the setting. To check, type `vcgencmd get_throttled` on the Pi: the expected response is `throttled=0x0`.
- The phase 2 program must not let both servos push against their end stops at the same time.

## Heat inside the head

The Raspberry Pi 4 is enclosed in the head, which is made of PLA and has no ventilation openings. This is an unmeasured risk.

- PLA softens near 60 °C (typical value; measurement not confirmed).
- The Pi reduces processor speed when its temperature is between 80 and 85 °C ([Raspberry Pi documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/frequency-management.adoc)).
- Stick the adhesive heatsinks onto the Pi chips before assembly.
- With the robot powered on for half an hour, type `vcgencmd measure_temp` on the Pi. If it goes above 70 °C, print the head shell in PETG or add ventilation holes in the back wall.

## First time you turn on the assembled robot

1. Switch off. Set the multimeter to continuity and check that the pack's positive and negative terminals are not shorted.
2. Before tightening the 2 wires coming down from the Raspberry Pi into the terminal strip, switch on and measure at the terminal strip, on the converter side: 5.1 V between terminals 1 and 2, with red on positive. Measure 6 V at the blue wire. Switch off.
3. Tighten the Pi wires into the terminal strip, red to terminal 1 and black to terminal 2, then switch on again.
4. The Arduino LED blinks, both servos hold the middle point, the Raspberry Pi power LED lights up, and in about 1 minute the display shows the system.
5. If nothing lights up, switch off and check the fuse.

## What has not been tested yet

<!-- GERADO:riscos -->
- Nothing has been printed or assembled yet. The electrical section of this page has not been bench-tested: it was based on the component datasheets.
- The 3MF files for the build plates have never been opened in Bambu Studio. If one won’t open, use the STL files.
- The USB-C plug that powers the Raspberry Pi is not in the 3D model. There may not be room for it next to the Pi inside the head.
- Raspberry Pi pins 31 to 34 are under the screen board. The clearance there (17.5 mm in the model) is unconfirmed: if the low-profile connector doesn't fit, the 3 serial wires will have to be soldered.
- The test coupon does not check the MG996R servo window or the M5 screw thread. Check the servo window in the head frame (build plate 01). The M5 thread is in the fork arm (build plate 03). Both are printed before the long print jobs.
- With the Arduino screwed to the base, the USB cable won't fit: there is about 10 mm of clearance to the wall. To reprogram it, you need to remove its 4 screws.
- The fuse holder, splice bar, and 3 serial resistors don’t have modeled locations: they sit loose among the wires, insulated with heat-shrink tubing.
- Measurements marked NC come from store listings. Measure your part before printing the section that touches it.
- The path for the 8 wires through the fork hole and the slot in the bottom of the head shell has never been tested with printed parts.
- Heat: the Raspberry Pi 4 is enclosed in the head, which is made of PLA and has no ventilation opening. PLA softens near 60 °C, and the Pi throttles starting at 80 °C. Attach the heatsinks and measure with the `vcgencmd measure_temp` command. If it goes above 70 °C, print the head shell in PETG or open ventilation holes at the back.
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

What to buy: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
