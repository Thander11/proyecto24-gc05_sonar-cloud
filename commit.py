import subprocess
import os
from datetime import datetime, timedelta


def change_commit_author(authors):
    # Mostrar los últimos commits para elegir
    print("\nÚltimos commits:")
    subprocess.run(['git', 'log', '--oneline', '-n', '5'])
    
    # Obtener el hash del commit a modificar
    commit_hash = input("\nIngresa el hash del commit a modificar: ").strip()
    
    # Mostrar opciones de autores
    print("\nSelecciona el nuevo autor:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")
    
    # Obtener selección del nuevo autor
    while True:
        selection = input("\nIngresa el número del nuevo autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")
    
    # Preparar el nuevo autor
    author_name, author_email = authors[selection]
    
    try:
        # Crear el comando de rebase con el nuevo autor
        env = os.environ.copy()
        filter_branch_cmd = f'''
        if [ $GIT_COMMIT = {commit_hash} ];
        then
            export GIT_AUTHOR_NAME="{author_name}";
            export GIT_AUTHOR_EMAIL="{author_email}";
            export GIT_COMMITTER_NAME="{author_name}";
            export GIT_COMMITTER_EMAIL="{author_email}";
        fi
        '''
        
        # Ejecutar el comando
        subprocess.run(['git', 'filter-branch', '-f', '--env-filter', filter_branch_cmd, f'{commit_hash}^..{commit_hash}'],
                      env=env, check=True)
        print("\n¡Autor del commit modificado exitosamente!")
    except subprocess.CalledProcessError as e:
        print(f"\nError al modificar el autor: {str(e)}")


def get_current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

def get_last_commit_message():
    return subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode('utf-8').strip()

def has_changes():
    status = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
    return bool(status.strip())

def do_merge(authors):
    # Obtener la rama actual
    current_branch = get_current_branch()
    print(f"\nVas a mergear la rama {current_branch} en develop")

    # Mostrar opciones de autores
    print("\nSelecciona el autor del merge:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")

    # Obtener selección del usuario
    while True:
        selection = input("\nIngresa el número del autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1 y 4.")

    # Preparar el autor
    author_name, author_email = authors[selection]

    try:
        # Configurar temporalmente el autor y committer
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = author_name
        env['GIT_AUTHOR_EMAIL'] = author_email
        env['GIT_COMMITTER_NAME'] = author_name
        env['GIT_COMMITTER_EMAIL'] = author_email

        # Cambiar a la rama develop
        subprocess.run(['git', 'checkout', 'develop'], check=True)

        # Realizar el merge
        print("\nRealizando merge...")
        merge_message = f"Merge branch '{current_branch}' into develop"
        
        # Hacer el merge sin fast-forward
        subprocess.run(['git', 'merge', '--no-ff', current_branch, '-m', merge_message], 
                      env=env, check=True)
        
        print("\nMerge realizado exitosamente!")
    except subprocess.CalledProcessError as e:
        print(f"\nError al realizar el merge: {str(e)}")
    finally:
        # Volver a la rama original
        subprocess.run(['git', 'checkout', current_branch], check=True)

def do_commit(authors):
    if not has_changes():
        print("No hay cambios para hacer commit.")
        return

    # Mostrar opciones de autores
    print("\nSelecciona el autor del commit:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")

    # Obtener selección del usuario
    while True:
        selection = input("\nIngresa el número del autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")

    # Obtener mensaje del commit
    commit_message = input("\nIngresa el mensaje del commit: ")

    # Obtener ID de JIRA y formatear como SCRUM-XX
    while True:
        scrum_id = input("\nIngresa solo el número de la subtarea (ej. 52): ")
        if scrum_id.isdigit():
            scrum_id = f"SCRUM-{scrum_id}"
            break
        print("Por favor, ingresa solo el número.")

    # Formar el mensaje completo
    full_message = f"{scrum_id} {commit_message}"

    # Preparar el autor
    author_name, author_email = authors[selection]

    # Consultar la fecha del último commit
    try:
        last_commit_date_str = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=iso']
        ).decode('utf-8').strip()
        last_commit_date = datetime.strptime(last_commit_date_str, "%Y-%m-%d %H:%M:%S %z")
        print(f"\nLa fecha del último commit fue: {last_commit_date.strftime('%Y-%m-%d %H:%M:%S %z')}")
    except subprocess.CalledProcessError as e:
        print(f"\nError al obtener la fecha del último commit: {str(e)}")
        return

    # Preguntar cuántos días u horas sumar
    while True:
        try:
            days_to_add = int(input("\n¿Cuántos días deseas sumar? (0 si es el mismo día): "))
            break
        except ValueError:
            print("Por favor, ingresa un número válido.")

    if days_to_add == 0:  # Mismo día
        while True:
            try:
                hours_to_add = int(input("\n¿Cuántas horas deseas sumar al último commit?: "))
                break
            except ValueError:
                print("Por favor, ingresa un número válido.")
        if hours_to_add == 0:
            # Sumamos 5 minutos al last_commit_date
            new_commit_date = last_commit_date + timedelta(minutes=5)
        else:
            new_commit_date = last_commit_date + timedelta(hours=hours_to_add)
    else:  # Días adicionales
        same_time = input("\n¿Mantener la misma hora que el último commit? (s/n): ").lower() == 's'
        if same_time:
            new_commit_date = last_commit_date + timedelta(days=days_to_add)
        else:
            while True:
                custom_time = input("\nIngresa la nueva hora (HH:MM:SS): ")
                try:
                    custom_time_parsed = datetime.strptime(custom_time, "%H:%M:%S").time()
                    new_commit_date = (last_commit_date + timedelta(days=days_to_add)).replace(
                        hour=custom_time_parsed.hour,
                        minute=custom_time_parsed.minute,
                        second=custom_time_parsed.second
                    )
                    break
                except ValueError:
                    print("Hora inválida. Por favor, usa el formato HH:MM:SS.")

    # Convertir la fecha final a cadena
    formatted_date = new_commit_date.strftime("%Y-%m-%d %H:%M:%S %z")

    try:
        # Añadir todos los cambios al staging area
        print("\nAñadiendo cambios al staging area...")
        subprocess.run(['git', 'add', '.'], check=True)

        # Configurar temporalmente el autor, committer y fecha
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = author_name
        env['GIT_AUTHOR_EMAIL'] = author_email
        env['GIT_COMMITTER_NAME'] = author_name
        env['GIT_COMMITTER_EMAIL'] = author_email
        env['GIT_AUTHOR_DATE'] = formatted_date
        env['GIT_COMMITTER_DATE'] = formatted_date

        # Realizar el commit
        print("Realizando commit...")
        subprocess.run(['git', 'commit', '-m', full_message], env=env, check=True)
        print("\nCommit realizado exitosamente!")
    except subprocess.CalledProcessError as e:
        print(f"\nError al realizar el commit: {str(e)}")


def main():
    # Verificar que estamos en un repositorio git
    if not os.path.exists('.git'):
        print("Error: No estás en un repositorio Git")
        return

    # Mostrar la rama actual
    current_branch = get_current_branch()
    print(f"Rama actual: {current_branch}")

    # Mostrar el último commit
    last_commit = get_last_commit_message()
    print(f"Último commit: {last_commit}")

    # Lista de autores
    authors = {
        '1': ("Pablo Natera Muñoz", "pnateram@alumnos.unex.es"),
        '2': ("Alejandro Barrena Millán", "abarrenaq@alumnos.unex.es"),
        '3': ("Raúl Martín-Romo Sánchez", "rmartinrw@alumnos.unex.es"),
        '4': ("Pedro Moreno Calderón", "pmorenoj@alumnos.unex.es")
    }

    
    # Modificar el menú principal
    while True:
        print("\nOpciones disponibles:")
        print("1: Commit")
        print("2: Merge")
        print("3: Cambiar autor de commit")
        action = input("\n¿Qué deseas hacer? (1-3): ")
        if action in ['1', '2', '3']:
            break
        print("Selección inválida. Por favor, elige un número entre 1 y 3.")

    if action == '1':
        do_commit(authors)
    elif action == '2':
        do_merge(authors)
    else:
        change_commit_author(authors)

if __name__ == "__main__":
    main()