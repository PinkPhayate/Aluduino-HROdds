const int anode_pins[] = {12, 8, 5, 3, 2, 11, 6};    // アノードに接続するArduinoのピン
const int cathode_pins[] = {7, 9, 10, 13};  // カソードに接続するArduinoのピン
const int dot_pin= 4;
const int number_of_anode_pins = sizeof(anode_pins) / sizeof(anode_pins[0]);
const int number_of_cathode_pins = sizeof(cathode_pins) / sizeof(cathode_pins[0]);
int numbers_to_display = 0; // LEDに表示する数字を保持する変数
double number_to_display = 0.0;

const int digits[] = {
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111101, // 6
  0b00100111, // 7
  0b01111111, // 8
  0b01101111, // 9
};

// 1桁の数字(n)を表示する
void display_number (int n) {
  for (int i = 0; i < number_of_anode_pins; i++) {
    digitalWrite(anode_pins[i], digits[n] & (1 << i) ? HIGH : LOW);
    digitalWrite(4, LOW);
  }
  Serial.println(n);
}
// 1桁の数字(n)と小数点を表示する
void display_number_with_dot (int n) {
  for (int i = 0; i < number_of_anode_pins; i++) {
    digitalWrite(anode_pins[i], digits[n] & (1 << i) ? HIGH : LOW);
    
  }
  digitalWrite(4, HIGH);
  Serial.println(n);
}

// アノードをすべてLOWにする
void clear_segments() {
  for (int j = 0; j < number_of_anode_pins; j++) {
    digitalWrite(anode_pins[j], LOW);
  }
}
int find_dot_dot_position(double n) {
  if(n > 1000) {
    return 0;
  }
  if(n > 100) {
    return 1;
  }
  if(n > 10) {
    return 2;
  }
    return 3;
}
int to_int(double n, int dot_position) {
  int i = 0;
  int num = 1;
  while(i < dot_position) {
    i ++;
    num *= 10;
  }
  return num * n;
}
void print_number() {
  // int n = numbers_to_display;  // number_to_displayの値を書き換えないために変数にコピー
  double origin_n = number_to_display;
  int dot_position = find_dot_dot_position(origin_n);
  int n = to_int( origin_n, dot_position );
  for (int i = 0; i < number_of_cathode_pins; i++) {
    digitalWrite(cathode_pins[i], LOW);
    if(i == dot_position) {
      display_number_with_dot(n % 10);
    }
    else {
      display_number(n % 10); // 最後の一桁を表示する
    }
    delayMicroseconds(100);
    clear_segments();
    digitalWrite(cathode_pins[i], HIGH);
    n = n / 10; // 10で割る
  }


}


void set_number(double n) {
  number_to_display = n;
}

// setup()　は、最初に一度だけ実行される
void setup() {
  Serial.begin(9800);
  for (int i = 0; i < number_of_anode_pins; i++) {
    pinMode(anode_pins[i], OUTPUT);  // anode_pinsを出力モードに設定する
  }
  for (int i = 0; i < number_of_cathode_pins; i++) {
    pinMode(cathode_pins[i], OUTPUT);  // cathode_pinを出力モードに設定する
    digitalWrite(cathode_pins[i], HIGH);
  }
  pinMode(dot_pin, OUTPUT);  // cathode_pinを出力モードに設定する

  // f = クロック周波数 / ( 2 * 分周比　*　( 1 + 比較レジスタの値))
  // 分周比=32, 比較レジスタの1値=255 -> f = 16000000 / (2 * 32 * 256) = 976 Hz
  OCR2A = 255; // 255クロックごとに割り込みをかける
  TCCR2B = 0b100; // 分周比を32に設定する
  bitWrite(TIMSK2, OCIE2A, 1); // TIMER2を許可する
}

void loop () {

   for (int i = 0; i < 10000; i++) {
    set_number(543.2);
    delay(1000);
   }
}

ISR(TIMER2_COMPA_vect) {
//  display_numbers();
  print_number();
}

