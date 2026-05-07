	import serial
	import time
	
	SERIAL_PORT = "/dev/serial0"
	BAUD_RATE = 9600
	
	
	def main():
	    try:
	        ser = serial.Serial(
	            port=SERIAL_PORT,
	            baudrate=BAUD_RATE,
	            bytesize=serial.EIGHTBITS,
	            parity=serial.PARITY_NONE,
	            stopbits=serial.STOPBITS_ONE,
	            timeout=1.0,
	        )
	
	        print("UART receive start")
	
	        while True:
	            line = ser.readline()
	
	            if line:
	                text = line.decode("utf-8", errors="replace").strip()
	                print(text)
	
	            time.sleep(0.01)
	
	    except serial.SerialException as e:
	        print(f"Serial error: {e}")
	
	    except KeyboardInterrupt:
	        print("Stopped by user")
	
	    finally:
	        try:
	            ser.close()
	        except NameError:
	            pass
	
	
	if __name__ == "__main__":
    main()