import subprocess
import platform
import os
import webbrowser
import time

def open_new_terminal(command, title=None):
    """
    Abre un comando en una nueva terminal según el sistema operativo y ejecuta el script.
    """
    system = platform.system()
    try:
        if system == "Windows":
            full_command = f"start cmd.exe /k {' '.join(command)}"
            if title:
                full_command = f"start \"{title}\" cmd.exe /k {' '.join(command)}"
            subprocess.Popen(full_command, shell=True)
        elif system == "Darwin":  # macOS
            command_string = " ".join(command)
            osascript_command = f'tell application "Terminal" to do script "{command_string}"'
            subprocess.Popen(['osascript', '-e', osascript_command])
        elif system == "Linux":
            command_string = " ".join(command)
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'{command_string}; exec bash'])
        else:
            print(f"Plataforma no soportada: {system}")
    except Exception as e:
        print(f"\nError al intentar abrir el comando en una nueva terminal: {str(e)}")

def main():
    """
    Ejecuta los scripts en nuevas terminales y abre el navegador.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    run = "run.py"
    python = "python.exe"

    scripts = [
        ([python, os.path.join(current_dir, "CONTENT_API", run)], "CONTENT_API"),
        ([python, os.path.join(current_dir, "USERS_API", "manage.py"), "runserver"], "USERS_API"),
        ([python, os.path.join(current_dir, "RECOMENDACIONES_API", run)], "RECOMENDACIONES_API"),
        ([python, os.path.join(current_dir, "WEB", run)], "WEB"),
    ]

    for command, title in scripts:
        open_new_terminal(command, title)

    # Esperar 5 segundos
    print("Esperando 5 segundos para que los servicios inicien...")
    time.sleep(5)

    # Abrir con el navegador predeterminado
    try:
        webbrowser.open('http://127.0.0.1:5000/')
    except Exception as e:
        print(f"Error al abrir el navegador: {str(e)}")
        print("Intente abrir manualmente: http://127.0.0.1:5000/")

if __name__ == "__main__":
    main()