void setup() {
  // initialize serial ports
  Serial.begin(19200);    // USB serial port 0
  Serial1.begin(19200, SERIAL_8N1);   // serial port 1
}

byte rx_byte = 0;        // stores received byte

void loop() {
  // check for data byte on USB serial port
  if (Serial.available()) {
    // get byte from USB serial port
    rx_byte = Serial.read();
    Serial.write(rx_byte);
    // send byte to serial port 3
    Serial1.write(rx_byte);
  }
  // check for data byte on serial port 3
  if (Serial3.available()) {
    // get a byte from serial port 3
    rx_byte = Serial3.read();
    // send the byte to the USB serial port
    Serial.write(rx_byte);
  }
}
