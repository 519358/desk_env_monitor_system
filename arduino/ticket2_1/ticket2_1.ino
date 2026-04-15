const int LED_PIN = LED_BUILTIN; //LED_BUILTINは組み込まれたLEDのピン(13番)
const int SWITCH_PIN = 2;

void setup()
{
    pinMode(LED_PIN, OUTPUT);
    pinMode(SWITCH_PIN, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop()
{
    int sw = digitalRead(SWITCH_PIN);

    if (sw == LOW)
    {
        digitalWrite(LED_PIN, HIGH);
        Serial.println("SW: PUSHED, LED: ON");
    }
    else
    {
        digitalWrite(LED_PIN, LOW);
        Serial.println("SW: RELEASED, LED: OFF");
    }

    delay(100);
}
