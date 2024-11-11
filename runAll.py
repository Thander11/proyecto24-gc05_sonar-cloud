import subprocess
import platform
import os

def open_new_terminal(command, title=None):
    """
    Abre un comando en una nueva terminal según el sistema operativo y ejecuta el script.
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Construir el comando para cmd.exe
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
    Ejecuta los scripts en nuevas terminales.
    """
    # Obtener el directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Lista de scripts a ejecutar
    scripts = [
        (["python.exe", os.path.join(current_dir, "CONTENT_API", "run.py")], "CONTENT_API"),
        (["python.exe", os.path.join(current_dir, "USERS_API", "manage.py"), "runserver"], "USERS_API"),
        (["python.exe", os.path.join(current_dir, "RECOMENDACIONES_API", "run.py")], "RECOMENDACIONES_API"),
        (["python.exe", os.path.join(current_dir, "WEB", "run.py")], "WEB"),
    ]

    for command, title in scripts:
        open_new_terminal(command, title)

if __name__ == "__main__":
    main()
