import subprocess
import sys
import os

def instalar_dependencias():
    """Instalar todas las dependencias necesarias"""
    print("=" * 50)
    print("Instalador - Sistema de Báscula Web")
    print("=" * 50)
    print()
    
    print("📦 Instalando dependencias...")
    print()
    
    intentos = 0
    while intentos < 3:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print()
            print("✓ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            intentos += 1
            if intentos < 3:
                print(f"⚠ Reintentando... ({intentos}/2)")
            else:
                print("✗ Error al instalar dependencias")
                return False

def main():
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('requirements.txt'):
        print("✗ Error: Este script debe ejecutarse desde la carpeta raíz del proyecto")
        print("   (donde está el archivo requirements.txt)")
        input("Presiona Enter para salir...")
        return
    
    # Instalar dependencias
    if instalar_dependencias():
        print()
        print("=" * 50)
        print("✓ Instalación completada exitosamente!")
        print("=" * 50)
        print()
        print("Para iniciar la aplicación, ejecuta:")
        print()
        print("  cd app")
        print("  python app.py")
        print()
        print("Luego abre en tu navegador:")
        print("  http://localhost:5000")
        print()
    else:
        print()
        print("✗ No se pudo completar la instalación")
        print("Intenta ejecutar manualmente:")
        print("  pip install -r requirements.txt")
    
    input("Presiona Enter para salir...")

if __name__ == '__main__':
    main()
