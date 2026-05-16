import tkinter as tk
import serial

# conectar a la báscula
puerto = serial.Serial('COM4', 9600, timeout=1)

peso_anterior = [""]  # usando lista para evitar global

# crear ventana primero
ventana = tk.Tk()
ventana.title("Sistema de peso actualizado")

tk.Label(ventana, text="Peso").pack()

entrada_peso = tk.Entry(ventana, font=("Arial", 16))
entrada_peso.pack(pady=10)

def leer_peso():
    try:
        dato = puerto.readline().decode('utf-8').strip()
        
        if dato and dato != peso_anterior[0]:
            peso_anterior[0] = dato
            entrada_peso.delete(0, tk.END)
            entrada_peso.insert(0, dato)

    except (serial.SerialException, UnicodeDecodeError) as e:
        print(f"Error al leer puerto: {e}")

    ventana.after(200, leer_peso)  # vuelve a leer cada 200 ms

leer_peso()

ventana.mainloop()