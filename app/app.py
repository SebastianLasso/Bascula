from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import serial
import threading
from datetime import datetime
from config_manager import cargar_config, obtener_config

app = Flask(__name__)
CORS(app)

# Cargar configuración
config = cargar_config()

# Variables globales
puerto_bascula = None
peso_actual = {"valor": 0}
port_abierto = False

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect('bascula.db')
    c = conn.cursor()
    
    # Tabla de productos
    c.execute('''CREATE TABLE IF NOT EXISTS productos
                 (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)''')
    
    # Tabla de registros de pesos
    c.execute('''CREATE TABLE IF NOT EXISTS registros
                 (id INTEGER PRIMARY KEY, producto_id INTEGER, peso REAL, 
                  precio_total REAL, fecha TEXT, FOREIGN KEY(producto_id) REFERENCES productos(id))''')
    
    conn.commit()
    conn.close()

init_db()

def conectar_bascula():
    global puerto_bascula, port_abierto
    try:
        puerto_com = obtener_config('puerto_bascula')
        baudrate = obtener_config('baudrate')
        timeout = obtener_config('timeout')
        
        puerto_bascula = serial.Serial(puerto_com, baudrate, timeout=timeout)
        port_abierto = True
        print(f"✓ Báscula conectada en {puerto_com}")
        leer_bascula()
    except (serial.SerialException, OSError) as e:
        print(f"✗ Error conectando báscula: {e}")
        port_abierto = False

def leer_bascula():
    while port_abierto:
        try:
            if puerto_bascula and puerto_bascula.is_open:
                dato = puerto_bascula.readline().decode('utf-8').strip()
                if dato:
                    try:
                        peso_actual["valor"] = float(dato)
                    except ValueError:
                        pass
        except (serial.SerialException, UnicodeDecodeError):
            pass

# Iniciar lectura de bascula en thread
thread_bascula = threading.Thread(target=conectar_bascula, daemon=True)
thread_bascula.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/peso', methods=['GET'])
def get_peso():
    return jsonify(peso_actual)

@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = sqlite3.connect('bascula.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM productos')
    productos = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(productos)

@app.route('/api/productos', methods=['POST'])
def add_producto():
    data = request.json
    conn = sqlite3.connect('bascula.db')
    c = conn.cursor()
    c.execute('INSERT INTO productos (nombre, precio) VALUES (?, ?)',
              (data['nombre'], data['precio']))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    conn = sqlite3.connect('bascula.db')
    c = conn.cursor()
    c.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/registros', methods=['POST'])
def add_registro():
    data = request.json
    conn = sqlite3.connect('bascula.db')
    c = conn.cursor()
    precio_total = data['peso'] * data['precio']
    c.execute('INSERT INTO registros (producto_id, peso, precio_total, fecha) VALUES (?, ?, ?, ?)',
              (data['producto_id'], data['peso'], precio_total, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "precio_total": precio_total})

@app.route('/api/registros', methods=['GET'])
def get_registros():
    conn = sqlite3.connect('bascula.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT r.*, p.nombre, p.precio FROM registros r 
                 JOIN productos p ON r.producto_id = p.id 
                 ORDER BY r.fecha DESC LIMIT 50''')
    registros = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(registros)

@app.route('/api/registros/<int:registro_id>', methods=['DELETE'])
def delete_registro(registro_id):
    conn = sqlite3.connect('bascula.db')
    c = conn.cursor()
    c.execute('DELETE FROM registros WHERE id = ?', (registro_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    puerto = obtener_config('puerto_servidor')
    debug = obtener_config('debug')
    app.run(debug=debug, port=puerto, host='0.0.0.0')
