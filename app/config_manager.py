import json
import os

CONFIG_FILE = 'config.json'

def cargar_config():
    """Cargar configuración desde archivo o crear valores por defecto"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        config_default = {
            'puerto_bascula': 'COM4',
            'baudrate': 9600,
            'timeout': 1,
            'intervalo_lectura': 200,
            'nombre_negocio': 'Pescadería',
            'puerto_servidor': 5000,
            'debug': True
        }
        guardar_config(config_default)
        return config_default

def guardar_config(config):
    """Guardar configuración en archivo"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def obtener_config(clave):
    """Obtener un valor específico de la configuración"""
    config = cargar_config()
    return config.get(clave)

def actualizar_config(clave, valor):
    """Actualizar un valor en la configuración"""
    config = cargar_config()
    config[clave] = valor
    guardar_config(config)
