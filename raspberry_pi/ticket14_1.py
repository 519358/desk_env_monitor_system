#!/usr/bin/env python3

import csv
import os
from datetime import datetime

import serial


SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600
LOG_FILE = "sensor_log.csv"


# line: str         関数の引数lineはstr型
# -> dict | None    関数の返り値はdictかNone
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

    # line(Serial通信で送られてきた文字列)の空白を削除する
    line = line.strip()

    if line == "":
        return None

    raw_data = {}

    # lineを,で分割し、list　itemsに格納する
    items = line.split(",")

    for item in items:
        if "=" not in item:
            return None

        key, value = item.split("=", 1)

        key = key.strip()
        value = value.strip()

        if key == "" or value == "":
            return None

        raw_data[key] = value

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
        return None

    if parsed_data["motion"] not in (0, 1):
        return None

    return parsed_data


def create_csv_writer(log_file: str):
    """
    CSVファイルを追記モードで開き、writerを返す。

    ファイルが存在しない場合、または空ファイルの場合はヘッダを書き込む。
    """

    # 指定ファイルが存在するか確認
    file_exists = os.path.exists(log_file)
    file_is_empty = (not file_exists) or os.path.getsize(log_file) == 0


    csv_file = open(log_file, mode="a", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)

    if file_is_empty:
        writer.writerow(["timestamp", "temp", "hum", "light", "motion"])
        # バッファの内容を実行しきる
        csv_file.flush()

    return csv_file, writer


def display_current_value(timestamp: str, data: dict) -> None:
    """
    現在値をCLIに表示する。
    """

    print(
        f"[{timestamp}] "
        f"Temp: {data['temp']:.1f} C, "
        f"Hum: {data['hum']:.1f} %, "
        f"Light: {data['light']}, "
        f"Motion: {data['motion']}"
    )


def write_csv_row(writer, csv_file, timestamp: str, data: dict) -> None:
    """
    センサ値をCSVへ1行追記する。
    """

    writer.writerow([
        timestamp,
        data["temp"],
        data["hum"],
        data["light"],
        data["motion"],
    ])

    csv_file.flush()


def main() -> None:
    """
    UARTから継続受信し、現在値表示とCSV保存を行う。
    """

    print("CLI display and CSV logging started.")
    print(f"Serial port: {SERIAL_PORT}")
    print(f"Baud rate  : {BAUD_RATE}")
    print(f"Log file   : {LOG_FILE}")
    print("Press Ctrl+C to stop.")
    print()

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print("Failed to open serial port.")
        print(e)
        return

    csv_file, writer = create_csv_writer(LOG_FILE)

    try:
        while True:
            received_bytes = ser.readline()

            if received_bytes == b"":
                continue

            try:
                line = received_bytes.decode("utf-8").strip()
            except UnicodeDecodeError:
                print("Invalid byte sequence received. Skipped.")
                continue

            data = parse_sensor_line(line)

            if data is None:
                print(f"Invalid data skipped: {line}")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            display_current_value(timestamp, data)
            write_csv_row(writer, csv_file, timestamp, data)

    except KeyboardInterrupt:
        print()
        print("Stopped by user.")

    except serial.SerialException as e:
        print()
        print("Serial communication error.")
        print(e)

    finally:
        csv_file.close()
        ser.close()
        print("Serial port and CSV file closed.")


if __name__ == "__main__":
    main()