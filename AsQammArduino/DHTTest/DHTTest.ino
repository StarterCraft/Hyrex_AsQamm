#include <DHTLifo.h>

void setup() {
  Serial.begin(115200);
  Serial.println("begin");
}


void loop() {
  DHTt(7);
  delay(60000);
}
