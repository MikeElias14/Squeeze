void setup() {
  // Setup pins
  pinMode(LED_BUILTIN, OUTPUT);

  // Button Inputs
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);

  Serial.begin(115200); // baud rate for the wifi module
  Serial.println("All set!!");
}

void loop() {
  /*
   * Send the combination of vales and do all the work 'server side' (on the laptop)
   */

  if(digitalRead(2) == LOW && digitalRead(3) == LOW && digitalRead(4) == LOW)
    Serial.println("000");

  if(digitalRead(2) == HIGH && digitalRead(3) == LOW && digitalRead(4) == LOW)
    Serial.println("100");

  if(digitalRead(2) == LOW && digitalRead(3) == HIGH && digitalRead(4) == LOW)
    Serial.println("010");

  if(digitalRead(2) == HIGH && digitalRead(3) == HIGH && digitalRead(4) == LOW)
    Serial.println("110");

  if(digitalRead(2) == LOW && digitalRead(3) == LOW && digitalRead(4) == HIGH)
    Serial.println("001");

  if(digitalRead(2) == HIGH && digitalRead(3) == LOW && digitalRead(4) == HIGH)
    Serial.println("101");

  if(digitalRead(2) == LOW && digitalRead(3) == HIGH && digitalRead(4) == HIGH)
    Serial.println("011");

  if(digitalRead(2) == HIGH && digitalRead(3) == HIGH && digitalRead(4) == HIGH)
    Serial.println("111");

  delay(100);

}
