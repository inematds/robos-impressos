/*
  centrar_servos.ino — robô quadrado que roda (robos-impressos)

  O que faz: leva os 2 servos MG996R para o centro (90°), mantém os dois lá e deixa
  os 2 motores das rodas DESLIGADOS (todos os pinos do driver L298N em nível baixo).
  Para que serve: você prende a engrenagem e o garfo com os servos já no centro,
  e a cabeça fica olhando para a frente quando o robô liga. Enquanto este sketch
  estiver gravado, o robô não anda.

  NÃO TESTADO NA BANCADA: o sketch compila para o Arduino Uno (arduino-cli, core
  arduino:avr 1.8.8, biblioteca Servo 1.3.0), mas ainda não foi rodado num robô montado.

  Ligações (Sensor Shield V5.0 em cima do Arduino Uno):
    D9  -> servo de PAN  (gira o pescoço; fica no deck)
    D10 -> servo de TILT (inclina a cabeça; fica dentro da cabeça)
    Em cada conector de 3 pinos do shield: G = fio marrom ou preto, V = fio vermelho,
    S = fio laranja ou amarelo.
    D5 = ENA, D4 = IN1, D7 = IN2 (motor direito) e D6 = ENB, D8 = IN3, D12 = IN4
    (motor esquerdo): só o pino S de cada conector vai ao driver L298N.
    D2 e A0 = encoder direito; D3 e A1 = encoder esquerdo (este sketch não os lê).
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
  Grave ANTES de fechar o robô: depois, para chegar ao USB do Uno, é preciso
  soltar os 4 parafusos de baixo e levantar o tronco.

  O que você vê quando funciona: o LED "L" do Uno pisca 1 vez por segundo, os
  2 servos vão para o centro e seguram a posição, e as rodas ficam paradas.
*/

#include <Servo.h>

const uint8_t PINO_PAN = 9;    // servo que gira o pescoço
const uint8_t PINO_TILT = 10;  // servo que inclina a cabeça
const uint8_t CENTRO = 90;     // graus: meio do curso de um servo de 180°

// driver L298N: ENA, IN1, IN2 (motor direito), ENB, IN3, IN4 (motor esquerdo)
const uint8_t PINOS_DRIVER[] = {5, 4, 7, 6, 8, 12};

Servo servoPan;
Servo servoTilt;

void setup() {
  for (uint8_t i = 0; i < sizeof(PINOS_DRIVER); i++) {
    digitalWrite(PINOS_DRIVER[i], LOW);   // nível baixo antes de virar saída: o motor não dá tranco
    pinMode(PINOS_DRIVER[i], OUTPUT);
  }
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
