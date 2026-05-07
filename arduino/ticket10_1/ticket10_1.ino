/*
 * UART接続確認
 * Arduino -> Raspberry Pi
 *
 * 目的:
 * 1秒ごとに固定文字列をUARTで送信する
 */

const unsigned long SEND_INTERVAL_MS = 1000;
unsigned long previousSendTime = 0;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    unsigned long currentTime = millis();

    if (currentTime - previousSendTime >= SEND_INTERVAL_MS) {
        previousSendTime = currentTime;

        Serial.println("HELLO_FROM_ARDUINO");
    }
}
