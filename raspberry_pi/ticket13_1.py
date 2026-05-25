def parse_sensor_line(line: str) -> dict | None:
    """
    Arduinoから受信した1行の文字列をdictへ変換する。

    想定フォーマット:
        temp=25.3,hum=48.2,light=612,motion=1

    戻り値:
        正常時:
            {
                "temp": 25.3,
                "hum": 48.2,
                "light": 612,
                "motion": 1
            }

        異常時:
            None
    """

    # 改行コードや前後の空白を削除する
    line = line.strip()

    # 空行なら異常データとして扱う
    if line == "":
        return None

    raw_data = {}

    # カンマで項目ごとに分割する
    items = line.split(",")

    for item in items:
        # "=" が含まれていない項目は異常
        if "=" not in item:
            return None

        # 最初の "=" だけで key と value に分ける
        key, value = item.split("=", 1)

        # 前後の空白を削除する
        key = key.strip()
        value = value.strip()

        # key または value が空なら異常
        if key == "" or value == "":
            return None

        raw_data[key] = value

    # 必須キーが存在するか確認する
    required_keys = ["temp", "hum", "light", "motion"]

    for key in required_keys:
        if key not in raw_data:
            return None

    try:
        parsed_data = {
            "temp": float(raw_data["temp"]),
            "hum": float(raw_data["hum"]),
            "light": int(raw_data["light"]),
            "motion": int(raw_data["motion"]),
        }
    except ValueError:
        # 数値変換できない値があれば異常
        return None

    return parsed_data


def main() -> None:
    # 動作確認用の受信文字列
    line = "temp=25.3,hum=48.2,light=612,motion=1"

    data = parse_sensor_line(line)

    if data is None:
        print("[ERROR] parse failed")
        return

    # dictから個別変数へ取り出す
    temperature = data["temp"]
    humidity = data["hum"]
    light = data["light"]
    motion = data["motion"]

    print("parsed dict:")
    print(data)

    print("individual variables:")
    print(f"temperature = {temperature}")
    print(f"humidity    = {humidity}")
    print(f"light       = {light}")
    print(f"motion      = {motion}")

    # 個別変数として制御判定に使える
    if light < 300:
        print("Light level: dark")
    else:
        print("Light level: bright")

    if motion == 1:
        print("Motion: detected")
    else:
        print("Motion: none")


if __name__ == "__main__":
    main()