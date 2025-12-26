Paso 1: Activar el Entorno Virtual (.venv)
    Asegúrate de que el entorno virtual esté activo para usar las librerías correctas.

    Linux/macOS	source              --->    .venv/bin/activate
    Windows (CMD o PowerShell)      --->    .\.venv\Scripts\activate

Paso 2: Instalar Dependencias
    Instala todas las librerías necesarias (solo si no lo has hecho antes):
    Bash    --->    pip install -r requirements.txt

Paso 3: Iniciar la Aplicación Streamlit
    Ejecuta el punto de entrada principal del paquete:
    Bash    --->    streamlit run gcti_analysis/main.py