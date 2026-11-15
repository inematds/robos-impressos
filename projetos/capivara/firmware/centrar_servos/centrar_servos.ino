/*
  centrar_servos.ino — a capivara (robos-impressos)

  O que faz: leva os 3 servos para o centro (90°) e os mantém lá, com os 2 motores das rodas desligados.
  Para que serve: você prende os horns, o garfo com os servos já no centro,
  e a cabeça fica olhando para a frente, de boca fechada, quando o robô liga.

  NÃO TESTADO NA BANCADA: o sketch compila para o Arduino Uno (arduino-cli, core arduino:avr,
  biblioteca Servo), mas ainda não foi rodado num robô montado.

  Ligações (Sensor Shield V5.0 em cima do Arduino Uno):
    D9  -> servo PAN: gira a cabeça (no deck do chassi)
    D10 -> servo TILT: inclina a cabeça (no berço do pescoço)
    D11 -> servo BOCA: abre a boca (micro servo, dentro da cabeça)
    Em cada conector de 3 pinos do shield: G = fio marrom ou preto, V = fio vermelho,
    S = fio laranja ou amarelo.
    Driver L298N dos motores (só o pino S de cada conector): ENA = D5, IN1 = D4, IN2 = D7,
    IN3 = D8, IN4 = D12, ENB = D6. Este sketch deixa os 6 em nível baixo: as rodas não giram.
    Os pinos D0 e D1 ficam livres: são a serial que vai para o Raspberry Pi.

  Energia dos servos: os 6 V do UBEC entram no borne azul do shield (VCC e GND),
  com o jumper SEL do shield RETIRADO. Não alimente os servos pelos 5 V da USB:
  a porta USB dá 0,5 A e um servo MG996R pede mais do que isso quando parte.

  Como gravar (Arduino IDE 2):
    1. Ligue o Uno ao computador pelo cabo USB, sem o shield e sem bateria.
    2. Ferramentas > Placa > Arduino AVR Boards > Arduino Uno.
    3. Ferramentas > Porta > a porta em que o Uno apareceu.
    4. Clique em Carregar (seta para a direita). Espere "Carregado".
    5. Tire o cabo USB antes de ligar a bateria.
  Para regravar depois de montado: puxe a bandeja do Arduino e tire os fios do D0 e do D1.

  O que você vê quando funciona: o LED "L" do Uno pisca 1 vez por segundo e os
  3 servos vão para o centro e seguram a posição.
*/

#include <Servo.h>

const uint8_t PINO_PAN = 9;          // gira a cabeça (no deck do chassi)
const uint8_t PINO_TILT = 10;        // inclina a cabeça (no berço do pescoço)
const uint8_t PINO_BOCA = 11;        // abre a boca (micro servo, dentro da cabeça)
const uint8_t PINOS_DRIVER[] = {5, 4, 7, 8, 12, 6};  // ENA, IN1, IN2, IN3, IN4, ENB do L298N
const uint8_t CENTRO = 90;      // graus: meio do curso de um servo de 180°

const uint8_t PINOS_SERVO[] = {PINO_PAN, PINO_TILT, PINO_BOCA};
const uint8_t N_SERVOS = sizeof(PINOS_SERVO);
Servo servos[N_SERVOS];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  for (uint8_t i = 0; i < sizeof(PINOS_DRIVER); i++) {   // motores desligados
    pinMode(PINOS_DRIVER[i], OUTPUT);
    digitalWrite(PINOS_DRIVER[i], LOW);
  }
  for (uint8_t i = 0; i < N_SERVOS; i++) {
    servos[i].write(CENTRO);     // define a posição antes de ligar o sinal: o servo não dá tranco
    servos[i].attach(PINOS_SERVO[i]);
    delay(300);                  // um servo de cada vez: o pico de partida não soma
  }
}

void loop() {
  // os servos continuam recebendo o sinal de 90°; o LED só mostra que o sketch está rodando
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(900);
}
