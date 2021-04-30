import serial
import time

ser = serial.Serial('/dev/ttyS9', baudrate=9600, timeout=1000)

while True:
    print("write")
    ser.write(b'hello\r\n')
    time.sleep(5)
