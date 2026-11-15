# Electrical wiring for the square desktop robot

<!-- GERADO:idiomas -->
[🇧🇷 Português](LIGACAO.md) · [🇺🇸 English](LIGACAO.en.md) · [🇪🇸 Español](LIGACAO.es.md)
<!-- /GERADO -->

**Not bench-tested.** This diagram is based on the component datasheets; no wires have been connected to an assembled robot yet.
Check every connection with a multimeter before turning on the switch. If your board has a different name printed on it than
the one shown here, use the name printed on the board.

![Wiring diagram for the square desktop robot: battery, fuse, protection board, charger, switch, converters, Arduino with Sensor Shield, servos, Raspberry Pi, and display](ligacao.en.svg)

Page with the same diagram: https://inematds.github.io/robos-impressos/guia/en/cubo/#energia

## Lithium Battery Safety

- **Polarity:** red to positive, black to negative. Check with the multimeter before each new connection. Reversed wiring burns out the board immediately.
- **Adjust before connecting the load:** LM2596 to 5.1 V and UBEC to 6 V, measured with the multimeter, with the Raspberry Pi, Arduino, and servos disconnected.
- **A short can start a fire:** solder with the cells OUT of the holder and insulate each splice with heat-shrink tubing. No metal can be exposed.
- **Fuse:** 3 A, on the positive wire, a few centimeters from the battery holder.
- **Matching cells:** use two new 18650 cells of the same brand and model. A dented, swollen, or hot cell goes to battery recycling, not in the robot.
- **First charge:** stay nearby, with the robot on a nonflammable surface.

## What Powers What

- **2S pack:** two 18650 cells in series, from 6 V (empty) to 8.4 V (full). It goes through the fuse and the protection board (BMS).
- **USB-C charger:** it connects to the protection board output, before the switch. The robot charges while off, using a USB-C power supply of 15 W or more.
- **Switch:** cuts the positive wire going to both converters.
- **LM2596, set to 5.1 V:** the output goes to a splice bar at the base. From there, one pair powers the Raspberry Pi (through the USB-C adapter with screw terminals) and another pair powers the Arduino (through the 5V pin on the Sensor Shield POWER connector).
- **UBEC at 6 V:** powers only the 2 servos, through the Sensor Shield’s blue screw terminal, with the SEL jumper removed.
- **Negative (GND):** there is just one for the entire robot.

Why the Arduino gets 5.1 V from the LM2596 instead of the battery voltage: the Arduino Uno VIN input requires 7 to 12 V
([Arduino Uno R3 datasheet](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)), and the pack stays below 7 V for a good
part of its discharge.

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
| Terminal block, screw terminal 1 (5.1 V) | 5V pin on the Sensor Shield POWER connector | red | Dupont jumper with one end cut and stripped | This is how the Arduino receives power. First, with the Uno powered only by USB and the SEL jumper removed, use a multimeter to confirm that this pin reads about 5 V and the D9 V pin reads 0 V. The wrong pin here sends the servos’ 6 V to the Raspberry Pi. |
| Terminal block, screw terminal 2 (negative) | GND pin on the Sensor Shield POWER connector | black | Dupont jumper with one end cut and stripped |  |

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
| Raspberry Pi: pin 32 (GPIO12, TX) | Through the neck to the S pin of D0 (RX) on the Sensor Shield | green | Dupont | Direct: the Pi's 3.3 V already counts as a high level for Arduino. |
| S pin of D1 (TX) on the Sensor Shield | 1 kΩ resistor, then through the neck to pin 33 (GPIO13, RX) on the Raspberry Pi | blue | Dupont | Never connect D1 directly to the Pi: that's 5 V on a 3.3 V pin. |
| Point between the 1 kΩ resistor and the blue wire | 2 1 kΩ resistors in series, then a G (GND) pin on the Sensor Shield | black | resistor leads | The 3 resistors form the voltage divider: 5 V becomes 3.3 V. |
| Raspberry Pi: pin 34 (GND) | Through the neck to a G (GND) pin on the Sensor Shield | black | Dupont |  |
| MPI3501 screen | Fitted onto Raspberry Pi pins 1 to 26 | no wire | the screen's own connector | Uses SPI and the 5 V from pins 2 and 4. |
<!-- /GERADO -->

## Prep Step 1: Solder the Power Circuit and Set Both Voltages

Do this at the workbench, before assembling the robot, with the printed base beside you as a guide for wire lengths.

1. Solder the 3rd wire (yellow) to the metal strip connecting the two cells, with the cells out of the holder.
2. Connect the holder, fuse, protection board, and charger as shown in the table. The solder pad names vary from board to board. On the charger, they are B+, BM, and B−. On the protection board from the store we checked, only the back has labels: B+, B1 (middle), B−, and C−. Based on the photo, C− is the negative output and B+ itself is the positive output; this is a reading of the photo, not confirmed: check with a multimeter.
3. Fit the switch into the cutout in the base from the outside, with the wires passing through the cutout, and solder it to the positive wire.
4. Connect the LM2596 and UBEC inputs. At the LM2596 output, solder 2 short wires (20 AWG) that end at the splice bar. Don’t connect anything else to the outputs.
5. Put the cells in the holder, checking which side is positive, and turn on the switch.
6. With the multimeter at the LM2596 output, turn the adjustment screw with the screwdriver until it reads 5.1 V. It takes several turns.
7. Measure the UBEC output: it should read 6 V. If it reads 5 V, move its jumper to 6 V.
8. Turn off the switch.

## Prep Step 2: Upload the Program and Set Both Servos to 90°

The program is the sketch [centrar_servos.ino](firmware/centrar_servos/centrar_servos.ino). It moves both servos to
the center and holds them there.

1. Open the sketch in Arduino IDE. Connect the Arduino Uno to the computer with the USB cable, without the shield or battery.
2. Under Tools, select the Arduino Uno board and the port it appeared on. Click Upload.
3. Unplug the USB cable, fit the Sensor Shield onto the Uno, and remove the shield’s SEL jumper: it is the small plastic cap over 2 pins, next to the blue screw terminal.
4. Reconnect the USB cable just to measure with the multimeter: the 5V pin on the shield’s POWER connector should read about 5 V, and the V pin on D9 should read 0 V.
5. If D9’s V pin reads 5 V, the SEL jumper is still in place. If your shield doesn’t have a POWER connector, use the + pin on the COM connector and measure the same way. A wrong pin here sends the servos’ 6 V to the Raspberry Pi.
6. Unplug the USB cable.
7. Connect the UBEC’s 6 V to the blue screw terminal (VCC and GND) and the 1000 µF capacitor to the same terminal.
8. Connect the splice bar’s 5.1 V to the 5V pin on the shield’s POWER connector, and the negative wire to the GND pin on the same connector. Use 2 Dupont jumpers: cut one end off each, strip the wire, and clamp it in the bar; the female end fits onto the pin.
9. Connect the pan servo to D9 and the tilt servo to D10.
10. Turn on the switch: both servos move to the center (90°) and the Uno’s LED flashes once per second.
11. Turn it off. From here on, don’t turn the servo shafts by hand.

Three notes:

- Do not power the MG996R servo from USB 5 V. The USB port supplies 0.5 A, and the servo needs more than that when it starts.
- Never connect the computer's USB cable while the battery is on: the two power sources would be in parallel.
- Upload the sketch before screwing the Uno onto the base. Once it is in place, only about 10 mm remains between the USB connector and the wall, so the cable will not fit.

The sketch compiles for the Arduino Uno (arduino-cli, core arduino:avr 1.8.8, Servo library 1.3.0). It has not yet been
run on an assembled robot.

## Prep Step 3: Flash the microSD Card and Install the Screen Driver

You write the card on your computer using a microSD card reader. Then you connect to the Raspberry Pi over the network,
using SSH: you type commands on your computer, and they run on the Pi.

1. Install Raspberry Pi Imager, the free Raspberry Pi program, on your computer, and put the card in the reader.
2. In Imager, choose your Pi model, the Raspberry Pi OS (64-bit) system, and the card.
3. Before writing the image, open Imager’s settings: give your Pi a name (for example, `robo`), create a username and password, enter your Wi-Fi name and password, and enable SSH. Write the image.
4. Put the card in the Pi, fit the screen onto pins 1 to 26 just for this test, and power on the Pi with a 5 V, 3 A USB-C power supply. Wait about 2 minutes.
5. On your computer, open the terminal: on Windows, use PowerShell; on Mac and Linux, use Terminal.
6. Type `ssh usuario@robo.local`, replacing `usuario` and `robo` with the names you created. Type `yes` the first time, then enter the password.
7. If `robo.local` doesn’t respond, open your router’s page, find the Pi in the list of connected devices, and use its number (the IP address), for example, `ssh usuario@192.168.0.50`.
8. When the terminal shows the Pi’s name, you’re in. Type the three commands below, one per line, pressing Enter after each one. The Pi needs an internet connection.

```
git clone https://github.com/goodtft/LCD-show.git
cd LCD-show
sudo ./LCD35-show
```

The Pi restarts on its own and the screen turns on. Then shut down the Pi with `sudo poweroff`, wait for the green LED to stop, and remove the screen for assembly.

The screen is the MPI3501: 3.5 inches, 480 × 320, ILI9486 controller, connected over SPI to pins 1 to 26. Sources:
[the MPI3501 page on lcdwiki](http://www.lcdwiki.com/3.5inch_RPi_Display) (model, pins, and driver) and
Raspberry Pi documentation on GitHub: [SSH](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/ssh.adoc) and [how to find the Pi’s address](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/remote-access/find-your-ip-address.adoc).
Not bench-tested: the manufacturer lists tests up to the Raspberry Pi 3B+, and the script replaces the Pi’s configuration file.

Plan B, also not tested, if the screen stays white or blank:

- Instead of the script, add the line `dtoverlay=piscreen,drm` to the end of the `/boot/firmware/config.txt` file and restart. This is the official overlay for a 3.5-inch screen with the same ILI9486 controller ([overlay list](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README)); the source doesn’t guarantee that it works with the MPI3501.
- If it still doesn’t turn on, write the Raspberry Pi OS (Legacy) image to the card again and repeat the manufacturer’s script.

## How the Raspberry Pi Communicates with the Arduino

The Raspberry Pi is in the head and the Arduino is in the base. The neck cable hole is 9 mm wide, and a USB plug will not fit
through it. So they communicate over a 3-wire serial connection (UART), with loose wires that pass through the hole.

- **On the Arduino:** pins D0 (RX) and D1 (TX), the board’s actual serial connection. It doesn’t interfere with the servo signal.
- **On the Raspberry Pi:** pin 32 (GPIO12, TX), pin 33 (GPIO13, RX), and pin 34 (GND). The screen uses pins 1 to 26; these three are free.
- **Voltage:** the Arduino runs at 5 V and the Pi at 3.3 V. The wire from the Arduino to the Pi passes through a divider with 3 1 kΩ resistors, which lowers 5 V to 3.3 V. The wire from the Pi to the Arduino connects directly.
- **Why use resistors instead of a level shifter module:** the divider takes 3 resistors on the wire, without another loose board in the base. The module also works: its 3.3 V side (LV) connects to the 3V3 pin on the shield’s POWER connector, and its 5 V side (HV) connects to the 5V pin.

How to assemble the divider: solder a 1 kΩ resistor to the wire from D1. On its other leg, solder the blue wire that goes up
to Pi pin 33 and two more 1 kΩ resistors in series, ending at a G pin on the shield. Cover everything with
heat-shrink tubing.

How to connect to the Pi: pins 31 to 34 are underneath the screen board, where about 17.5 mm of clearance is available (measurement not
confirmed). A standard 14 mm Dupont connector will not fit upright. Cut a 2 × 2 piece from the female pin header strip,
solder the 3 wires sideways to its terminals, and fit it onto pins 31 to 34 before installing the screen.

To enable serial on the Pi system, add a line at the end of the `/boot/firmware/config.txt` file, AFTER
installing the screen driver, because the driver script rewrites this file:

- Raspberry Pi 4: `dtoverlay=uart5`
- Raspberry Pi 5: `dtoverlay=uart4-pi5`

Source: [Raspberry Pi firmware overlay list](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README).
After restarting, check the port name with `ls /dev/ttyAMA*`. Not bench-tested. The program that uses this
serial connection is part of phase 2.

## The 8 Wires That Pass Through the Neck

There are 8 wires: 2 power wires (5.1 V from the Raspberry Pi, 20 AWG), 3 serial wires, and the 3 wires from the tilt servo cable. They must be
connected inside the head BEFORE the head shell, because the Raspberry Pi is enclosed afterward. They also can’t hang down
under the fork at this point, because the bottom of the head shell passes beneath it. Follow this order:

1. With the head still open (frame, screen, tilt servo, and fork in place), screw the 2 wires carrying 5.1 V into the USB-C adapter and plug it into the Raspberry Pi.
2. Check the low-profile serial connector on pins 31 to 34. It goes in before the screen, with the 3 wires already soldered.
3. Connect the 30 cm extension to the tilt servo cable.
4. Feed the 8 wires down through the 9 mm hole in the fork, from top to bottom. Feed the extension connector first; it’s 7.6 mm wide and fits snugly.
5. Stop when the ends are flush with the underside of the fork. Leave about 5 cm of extra wire inside the head: it tilts around the fork.
6. Close the head with the head shell. Use tweezers to pull the ends of all 8 wires out through the slot in the bottom of the head shell.
7. Feed the wires through the neck tube and seat the head on it.
8. At the base, with the switch off: connect the 2 wires carrying 5.1 V to the splice bar, the extension to D10, and the 3 serial wires as shown in the table.

Leave about 10 cm of slack inside the base: the neck turns almost one full rotation and twists the wires. This routing has never been
tested with the printed parts.

## Current, Wire, and Fuse

The values below are calculated from the specifications, not measured.

- Normal use: about 2 A from the pack. The Raspberry Pi draws about 1 A at 5.1 V, and the servos draw less than 1 A at 6 V.
- Peak: about 5 A, with the LM2596 at 2 A, the UBEC at its 3 A limit, and the pack at 6.5 V.
- KCD11-101 switch: 3 A at 250 V~ and 6 A at 125 V~ ([store listing](https://eletronicamaker.com.br/produto/mini-chave-gangorra-kcd11-101-liga-desliga-3a-250v-vm-c)). The listing gives no value for DC current.
- 3 A fuse: the lowest rating for the switch. Normal use stays below it. A peak lasting a few seconds won’t blow it; a sustained overload blows the fuse before the switch heats up (typical glass-fuse behavior; not confirmed by measurement).
- If the fuse blows during normal robot use, don’t install a larger one: measure the current and find what is drawing too much.
- 22 AWG wire (0.33 mm²) for power in the base. 20 AWG wire (0.5 mm²) for the 5.1 V pair running up to the Raspberry Pi: at 2 A, the calculated voltage drop along this section is 0.06 V.
- The LM2596 can handle about 2 A continuously without a heatsink (typical value; not confirmed by measurement). Use the Raspberry Pi 4, or the Pi 5 without USB accessories.
- If the Raspberry Pi reports undervoltage, shorten the 5.1 V pair and check the setting. To check, type `vcgencmd get_throttled` on the Pi: the expected response is `throttled=0x0`.
- The phase 2 program must not let both servos strain against their end stops at the same time.

## First time you turn on the assembled robot

1. Switch off. With the multimeter set to continuity, check that the pack’s positive and negative terminals aren’t shorted.
2. Before joining the 2 wires coming down from the Raspberry Pi, turn on the switch and measure at the splice bar, on the converter side: 5.1 V, with the red probe on positive. Measure 6 V at the blue screw terminal. Turn it off.
3. Join the Pi wires at the bar, red to red and black to black, and turn the switch on again.
4. The Arduino LED blinks, both servos hold the middle point, the Raspberry Pi power LED turns on, and in about 1 minute the screen shows the system.
5. If nothing turns on, switch off and check the fuse.

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
<!-- /GERADO -->

## Glossary

<!-- GERADO:glossario -->
- **GPIO:** The Raspberry Pi's 40-pin header, where the screen and signal wires connect.
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
<!-- /GERADO -->

What to buy: [LISTA-DE-COMPRAS.en.md](LISTA-DE-COMPRAS.en.md). How to print: [IMPRIMIR.en.md](IMPRIMIR.en.md).
