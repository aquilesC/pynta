String tempValue;
byte rx_byte = 0;        // stores received byte
String serialString = "";
bool is_data;
int val;
int i;

void setup() {
  // initialize serial ports
  Serial.begin(19200);    // USB serial port 0
  Serial1.begin(19200);   // serial port 1
  Serial2.begin(19200);   // serial port 2
  Serial.flush();
  Serial1.flush();
  Serial2.flush();
  analogWriteResolution(12);
  analogWrite(DAC0, 0);

}

void loop() {
  while (Serial.available() > 0 ) {
    char c = Serial.read();
    serialString += c;
    if (c == '\n') {
      is_data = true;
    }
  }
  if (is_data) {
    is_data = false;
    if (serialString.startsWith("mot1")) {
      Serial.println("Waiting for input mot 1");
      while (Serial.available() <= 0) {
        delay(1);
      }
      rx_byte = Serial.read();
      Serial1.write(rx_byte);
      Serial.println("OK");
    }
    else if (serialString.startsWith("mot2")) {
      Serial.println("Waiting for input mot 2");
      while (Serial.available() <= 0) {
        delay(1);
      }
      rx_byte = Serial.read();
      Serial2.write(rx_byte);
      Serial.println("OK");
    }
    else if(serialString.startsWith("OUT")){
      for (i = 4; i < serialString.length(); i++) {
        tempValue += serialString[i];
      }
      val = tempValue.toInt();
      analogWrite(DAC0, val);
      Serial.println(val);
      }
    else {
      Serial.println("wrong command");
      Serial.flush();
      Serial1.flush();
      Serial2.flush();
      }
    serialString = "";
  }
  

}
