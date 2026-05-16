@echo off
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando servidor Flask...
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
echo La aplicacion estara disponible en: http://localhost:5000
echo.
cd app
python app.py
pause
