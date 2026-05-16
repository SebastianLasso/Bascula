# Sistema de Báscula Web - Pescadería

Una aplicación web moderna para gestionar pesos y precios de productos en una pescadería.

## Características

✅ Lectura en tiempo real de báscula (puerto COM4)
✅ Gestión de productos con precios por kg
✅ Registro automático de pesajes
✅ Historial completo de transacciones
✅ Interfaz responsiva (HTML5, CSS3, JavaScript)
✅ Base de datos SQLite
✅ API REST con Flask
✅ Cálculo automático de precios

## Requisitos

- Python 3.7+
- Báscula conectada al puerto COM4 (9600 baud)

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
cd app
python app.py
```

3. Abrir en navegador:
```
http://localhost:5000
```

## Estructura del Proyecto

```
bascula/
├── app/
│   ├── app.py                 # Backend Flask
│   ├── templates/
│   │   └── index.html         # Interfaz principal
│   └── static/
│       ├── css/
│       │   └── style.css      # Estilos
│       └── js/
│           └── script.js      # Lógica del frontend
├── bascula.db                 # Base de datos SQLite
├── bascula.py                 # Versión anterior (Tkinter)
└── requirements.txt           # Dependencias
```

## API Endpoints

### Peso
- `GET /api/peso` - Obtener peso actual

### Productos
- `GET /api/productos` - Listar todos
- `POST /api/productos` - Crear nuevo
- `DELETE /api/productos/<id>` - Eliminar

### Registros
- `GET /api/registros` - Listar historial
- `POST /api/registros` - Registrar pesaje
- `DELETE /api/registros/<id>` - Eliminar registro

## Uso

1. Agregar productos con sus precios por kg
2. Seleccionar producto y pesar en la báscula
3. El sistema calcula automáticamente el precio total
4. Ver historial de todas las transacciones
5. Eliminar registros si es necesario

## Notas

- La báscula debe estar conectada antes de iniciar la aplicación
- Los datos se guardan automáticamente en SQLite
- La interfaz se actualiza en tiempo real cada 500ms
- Compatible con celulares y tablets
