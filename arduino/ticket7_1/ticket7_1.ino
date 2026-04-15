#include <DHT.h>
#include <math.h>

// ===== 設定 =====
#define DHTPIN 2

// 使用センサに合わせてどちらかを選ぶ
// #define DHTTYPE DHT11
#define DHTTYPE DHT22

// 読み取り周期[ms]
const unsigned long READ_INTERVAL_MS = 2000;

// ===== DHTオブジェクト生成 =====
DHT dht(DHTPIN, DHTTYPE);

// ===== 前回読み取り時刻 =====
unsigned long lastReadTime = 0;

// ===== 前回正常値（必要なら保持） =====
float lastValidTemperature = 0.0f;
float lastValidHumidity = 0.0f;
bool hasValidData = false;

void setup()
{
    Serial.begin(9600);
    dht.begin();

    Serial.println("DHT sensor start");
}

void loop()
{
    unsigned long currentTime = millis();

    if ((currentTime - lastReadTime) >= READ_INTERVAL_MS)
    {
        lastReadTime = currentTime;

        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        // 読み取り失敗判定
        if (isnan(humidity) || isnan(temperature))
        {
            Serial.println("[ERROR] Failed to read from DHT sensor");

            if (hasValidData)
            {
                Serial.print("[LAST VALID] Temperature: ");
                Serial.print(lastValidTemperature, 1);
                Serial.print(" C, Humidity: ");
                Serial.print(lastValidHumidity, 1);
                Serial.println(" %");
            }

            return;
        }

        // 正常値保存
        lastValidTemperature = temperature;
        lastValidHumidity = humidity;
        hasValidData = true;

        // 出力
        Serial.print("Temperature: ");
        Serial.print(temperature, 1);
        Serial.print(" C, Humidity: ");
        Serial.print(humidity, 1);
        Serial.println(" %");
    }
}