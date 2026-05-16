import serial

puerto = serial.Serial('COM4', 9600, timeout=1)

while True:
    dato = puerto.readline().decode('utf-8').strip()
    if dato:
        print("Peso:", dato)