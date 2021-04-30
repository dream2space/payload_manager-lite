import serial

ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=10)

while True:
    print(ser.readline())
