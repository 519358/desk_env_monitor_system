unsigned long counter = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Serial monitor test start");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("count = ");
  Serial.println(counter);
  counter++;
  delay(1000);
}
