#include <Arduino.h>

//センサ感度が悪くスムーズに動かないことに注意
const uint8_t PIR_PIN = 2;  // Arduino Uno の外部割込み対応ピン(D2)。Passive Infrared Ray sensor(人感センサ)ピン。

volatile bool motionDetected = false;
volatile unsigned long interruptCount = 0;

void onMotionDetected(void)
{
    //割り込み発生時に実行される関数
    //動作検知のフラグをオンにし、回数のカウントを増やす
    motionDetected = true;
    interruptCount++;
}

void setup(void)
{
    Serial.begin(9600);

    pinMode(PIR_PIN, INPUT);

    //attachInterrupt()は割り込み発生時の動作を設定する関数。
    //attachInterrupt(割り込みピン,実行する関数,割り込み発生条件)
    attachInterrupt(digitalPinToInterrupt(PIR_PIN), onMotionDetected,RISING);

    Serial.println("PIR interrupt monitoring start");
    Serial.println("Waiting for motion...");
}

void loop(void)
{
    if(motionDetected == true)
    {
        unsigned long countCopy = 0;

        //noInterrupts();とinterrupts();で囲った間は割り込みが発生しない。
        //→検出回数とフラグの状態とかに矛盾が生じない
        noInterrupts();
        motionDetected = false;
        countCopy = interruptCount;
        interrupts();

        Serial.print("Interrupt detected. count = ");
        Serial.println(countCopy);
    }
}
