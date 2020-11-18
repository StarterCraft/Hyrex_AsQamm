void setup() {
  Serial.begin(115200); // open serial port, set the baud rate as 9600 bps
}
void loop() {
  Serial.println(analogRead(0)); //print the value to serial port
  delay(200);
}
