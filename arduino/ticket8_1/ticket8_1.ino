const int LIGHT_SENSOR_PIN = A0;

int lightValue = 0;

void setup()
{
    pinMode(LIGHT_SENSOR_PIN, INPUT);
    Serial.begin(9600);
}

void loop()
{
    lightValue = analogRead(LIGHT_SENSOR_PIN);

    Serial.print("Light Value: ");
    Serial.println(lightValue);

    delay(500);
}
