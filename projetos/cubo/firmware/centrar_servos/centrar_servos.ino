/*
  centrar_servos.ino — robô quadrado de mesa (robos-impressos)

  O que faz: leva os 2 servos MG996R para o centro (90°) e os mantém lá.
  Para que serve: você prende a engrenagem e o garfo com os servos já no centro,
  e a cabeça fica olhando para a frente quando o robô liga.

  NÃO TESTADO NA BANCADA: o sketch compila para o Arduino Uno (arduino-cli, core
  arduino:avr 1.8.8, biblioteca Servo 1.3.0), mas ainda não foi rodado num robô montado.

  Ligações (Sensor Shield V5.0 em cima do Arduino Uno):
    D9  -> servo de PAN  (gira o pescoço; fica na base)
    D10 -> servo de TILT (inclina a cabeça; fica dentro da cabeça)
    Em cada conector de 3 pinos do shield: G = fio marrom ou preto, V = fio vermelho,
    S = fio laranja ou amarelo.
    Os pinos D0 e D1 ficam livres: são a serial que vai para o Raspberry Pi.

  Energia dos servos: os 6 V do UBEC entram no borne azul do shield (VCC e GND),
  com o jumper SEL do shield RETIRADO. Não alimente o MG996R pelos 5 V da USB:
  a porta USB dá 0,5 A e o servo pede mais do que isso quando parte.

  Como gravar (Arduino IDE 2):
    1. Ligue o Uno ao computador pelo cabo USB, sem o shield e sem bateria.
    2. Ferramentas > Placa > Arduino AVR Boards > Arduino Uno.
    3. Ferramentas > Porta > a porta em que o Uno apareceu.
    4. Clique em Carregar (seta para a direita). Espere "Carregado".
    5. Tire o cabo USB antes de ligar a bateria.
  Grave ANTES de parafusar o Uno na base: com ele no lugar, o cabo USB não entra.

  O que você vê quando funciona: o LED "L" do Uno pisca 1 vez por segundo e os
  2 servos vão para o centro e seguram a posição.
*/

#include <Servo.h>

const uint8_t PINO_PAN = 9;    // servo que gira o pescoço
const uint8_t PINO_TILT = 10;  // servo que inclina a cabeça
const uint8_t CENTRO = 90;     // graus: meio do curso de um servo de 180°

Servo servoPan;
Servo servoTilt;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  servoPan.write(CENTRO);      // define a posição antes de ligar o sinal: o servo não dá tranco
  servoTilt.write(CENTRO);
  servoPan.attach(PINO_PAN);
  servoTilt.attach(PINO_TILT);
}

void loop() {
  // os servos continuam recebendo o sinal de 90°; o LED só mostra que o sketch está rodando
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(900);
}
