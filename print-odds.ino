const int anode_pins[] = {12, 8, 5, 3, 2, 11, 6};    // アノードに接続するArduinoのピン
const int cathode_pins[] = {7, 9, 10, 13};  // カソードに接続するArduinoのピン
const int dot_pin= 4;
const int number_of_anode_pins = sizeof(anode_pins) / sizeof(anode_pins[0]);
const int number_of_cathode_pins = sizeof(cathode_pins) / sizeof(cathode_pins[0]);
const int PLAT_BUTTON = 1000;
int numbers_to_display = 0; // LEDに表示する数字を保持する変数
double number_to_display = 0.0;
bool enableToPrint = true;  //  ディスプレイに書き込み可不可を判定するフラグ
double input_nums[2] = {0.0, 0.0};  // リモコンからの入力を格納する配列
#define ERROR_NUM 999
#define INPUT_MODE 10000

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
  0b00000000,
  0b01111001, // E
};


// IC_number
#define IR_IN 14
#define IR_DATA_SIZE 100
byte ir_data[IR_DATA_SIZE];
byte ir_code[32];
int nums[2] = {0,0};


// 1桁の数字(n)を表示する
void display_number (int n) {
  for (int i = 0; i < number_of_anode_pins; i++) {
    digitalWrite(anode_pins[i], digits[n] & (1 << i) ? HIGH : LOW);

  }
  digitalWrite(4, LOW);
  //Serial.println(n);
}
// 1桁の数字(n)と小数点を表示する
void display_number_with_dot (int n) {
  for (int i = 0; i < number_of_anode_pins; i++) {
    digitalWrite(anode_pins[i], digits[n] & (1 << i) ? HIGH : LOW);
  }
  digitalWrite(4, LOW);



  //Serial.println(n);
}

void display_error () {
  digitalWrite(cathode_pins[0], LOW);
  for (int i = 0; i < number_of_anode_pins; i++) {
    digitalWrite(anode_pins[i], digits[11] & (1 << i) ? HIGH : LOW);
  }
  digitalWrite(4, LOW);
}


// アノードをすべてLOWにする
void clear_segments() {
  for (int j = 0; j < number_of_anode_pins; j++) {
    digitalWrite(anode_pins[j], LOW);
  }
}
/*
int find_dot_dot_position(double n) {
    return 1;
}
*/
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
   //int n = numbers_to_display;  // number_to_displayの値を書き換えないために変数にコピー
   if(number_to_display==ERROR_NUM) {
    display_error();
    clear_segments();
    digitalWrite(cathode_pins[0], HIGH);
    return;
   }
   else if(number_to_display<0) {
    return;
   }
  double origin_n = number_to_display;
  //int dot_position = find_dot_dot_position(origin_n);
  int n = to_int( origin_n, 1 );

  for (int i = 0; i < number_of_cathode_pins; i++) {
    digitalWrite(cathode_pins[i], LOW);
    if(i == 1) {
      digitalWrite(4, HIGH);
      display_number_with_dot(n % 10);
      //Serial.println(n);
    }
    else {
      display_number(n % 10); // 最後の一桁を表示する
    }
    //delayMicroseconds(100);
    clear_segments();
    digitalWrite(cathode_pins[i], HIGH);
    n = n / 10; // 10で割る
    if(n==0)break;
  }


}


void set_number(double n) {
  number_to_display = n;
}

// setup()　は、最初に一度だけ実行される
void setup() {
  Serial.begin(115200);
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

  // IC_NUMBER
  pinMode(14, INPUT);
  digitalWrite(14, HIGH);
}

void loop () {
    double inputchar;      //入力状態の読み取りに使う

  inputchar = Serial.parseFloat();  //シリアル通信で送信された値を読み取る


  if(inputchar == 0.00 ) {
    enableToPrint = false;
    ir_mode();
  }
  else {
     enableToPrint = true;
     display_mode(inputchar);
  }

}
void ir_mode() {
//  Serial.println("ir mode starts");
      ir_read(IR_IN);
//    ir_print_1();
    ir_print_2();

}
void display_mode(double inputchar) {
  if(inputchar==-1){
    clear_segments();
  }

  if(inputchar!=0.00){
    Serial.println(inputchar);
    if(inputchar==999.00) set_number(ERROR_NUM);
    else set_number(inputchar);
    delay(1000);
  }

}

ISR(TIMER2_COMPA_vect) {
  //  display_numbers();
  if (enableToPrint ) {
    print_number();
  }

}

//データ受信
void ir_read(byte ir_pin){
  for(int i = 0; i < IR_DATA_SIZE; i++){
    ir_data[i] = 0;
  }
  unsigned long now, last, start_at;
  boolean stat;
  start_at = micros();

  //2.5秒以上入力がなかったら終了
  while(stat = digitalRead(ir_pin)){
    if(micros() - start_at > 2500000) return;
  }

  start_at = last = micros();
  for(int i = 0; i < IR_DATA_SIZE; i++){
    //入力が反転するまで待ち（上限25ms）
    while(1){
      if(stat != digitalRead(ir_pin)) break;
      if(micros() - last > 25000) return;
    }
    now = micros();
    ir_data[i] = (now - last)/100;  //byteに格納するあため
    last = now;
    stat = !stat;
  }

}

//解析データ出力
void ir_print_2(){
  int j = 0;
  byte result = 0;

  //1or0判定
  for (int i = 3; i < 66; i+=2){
    if(ir_data[i] > 10){
      ir_code[j] = 1;
    }else{
      ir_code[j] = 0;
    }
    j++;
  }

  //データを数値化
  for (int i = 0; i < 8; i++){
    if(ir_code[i+16] == ir_code[i+24]){  //反転データチェック
      result = 0;
      break;
    }else{
      bitWrite(result,i,ir_code[i+16]);
    }
  }

  if(0 != result) {
//     Serial.println(result);
    translate(result);
  }
}

// 入力文字を変換
void translate(byte input_num) {
  double translated_num = 999;
  bool is_not_play_button = true;
  switch (input_num) {
    case 22:
      translated_num = 0;
      break;
    case 12:
      translated_num = 1;
      break;
    case 24:
      translated_num = 2;
      break;
    case 94:
      translated_num = 3;
      break;
    case 8:
      translated_num = 4;
      break;
    case 28:
      translated_num = 5;
      break;
    case 90:
      translated_num = 6;
      break;
    case 66:
      translated_num = 7;
      break;
    case 82:
      translated_num = 8;
      break;
    case 74:
      translated_num = 9;
      break;
    case 67:
      is_not_play_button = false;
      translated_num = PLAT_BUTTON;
      break;
    default:
      initialize_input_nums();
  }
  if (is_not_play_button) {
    // キューの構造体
    input_nums[1] = input_nums[0];
    input_nums[0] = translated_num;
    enableToPrint = true;
    set_number(calc_input_nums());
  }
  if(!is_not_play_button) {
    enableToPrint = true;
    double num = calc_input_nums();
//    Serial.println(num);
    set_number(num);
    get_odds(num);
    initialize_input_nums();
    /** ここでコンソールに出力して、値をもらう*/

  }
}
void initialize_input_nums() {
    input_nums[1] = 0.0;
    input_nums[0] = 0.0;  
}
double calc_input_nums() {
  return input_nums[1]*10 + input_nums[0];
}
void get_odds(double num) {
  // display at console and send number to pc
  if(0 < num) Serial.println(num);
  else Serial.println(PLAT_BUTTON);
}
