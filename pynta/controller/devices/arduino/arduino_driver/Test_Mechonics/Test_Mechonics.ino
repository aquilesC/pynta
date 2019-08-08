byte rx_byte = 0;        // stores received byte
String serialString;

void setup() {
  // initialize serial ports
  Serial.begin(19200);    // USB serial port 0
  Serial1.begin(19200);   // serial port 1
  Serial.flush();
}



void loop() {
  serialString = "";
  while (Serial.available()) {
      char c = Serial.read();
      serialString += c;
  }
  if (serialString.length() > 0) {
    if (serialString.startsWith("mot")) {
      Serial.println("Waiting for input");
      rx_byte = Serial.read();
      Serial1.write(rx_byte);
      Serial.println("OK\n");
    }
    Serial.flush();
  }
//  // check for data byte on USB serial port
//  if (Serial.available()) {
//    // get byte from USB serial port
//    rx_byte = Serial.read();
//    // send byte to serial port 3
//    Serial1.write(rx_byte);
//    Serial.print("OK");
//  }
//  // check for data byte on serial port 3
//  if (Serial3.available()) {
//    // get a byte from serial port 3
//    rx_byte = Serial3.read();
//    // send the byte to the USB serial port
//    Serial.write(rx_byte);
//  }
}
