import subprocess
import os
from datetime import datetime, timedelta
import sys
 
# Permite cambiar el autor de un commit específico
def change_commit_author(authors):
    print("\nÚltimos commits:")
    subprocess.run(['git', 'log', '--oneline', '-n', '5'])
    
    commit_hash = input("\nIngresa el hash del commit a modificar: ").strip()
    
    print("\nSelecciona el nuevo autor:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")
    
    while True:
        selection = input("\nIngresa el número del nuevo autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")
    
    author_name, author_email = authors[selection]
    
    try:
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
        
        subprocess.run(['git', 'filter-branch', '-f', '--env-filter', filter_branch_cmd, f'{commit_hash}^..{commit_hash}'],
                       env=env, check=True)
        print("\n¡Autor del commit modificado exitosamente!")
    except subprocess.CalledProcessError as e:
        print(f"\nError al modificar el autor: {str(e)}")

# Obtiene la rama actual
def get_current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

# Obtiene el mensaje del último commit
def get_last_commit_message():
    return subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode('utf-8').strip()

# Comprueba si hay cambios en el repositorio
def has_changes():
    status = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
    return bool(status.strip())

# Obtiene la fecha del último commit de una rama específica
def get_latest_commit_date(branch_name):
    """Obtiene la fecha del último commit de una rama específica."""
    try:
        last_commit_date_str = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=iso', branch_name]
        ).decode('utf-8').strip()
        return datetime.strptime(last_commit_date_str, "%Y-%m-%d %H:%M:%S %z")
    except subprocess.CalledProcessError as e:
        print(f"\nError al obtener la fecha del último commit de la rama '{branch_name}': {str(e)}")
        return None

# Ajusta la fecha del merge para que sea posterior al último commit de ambas ramas
def adjust_merge_date(branch1, branch2):
    """Ajusta la fecha del merge para que sea posterior al último commit de ambas ramas."""
    last_commit_branch1 = get_latest_commit_date(branch1)
    last_commit_branch2 = get_latest_commit_date(branch2)

    if last_commit_branch1 and last_commit_branch2:
        # Obtener la fecha más reciente entre las dos ramas
        latest_commit_date = max(last_commit_branch1, last_commit_branch2)
        # Incrementar en 5 minutos para garantizar sincronización
        adjusted_date = latest_commit_date + timedelta(minutes=5)
        return adjusted_date
    else:
        print("\nNo se pudo obtener la fecha del último commit en una o ambas ramas.")
        return None

# Realiza un merge de la rama actual en la rama 'develop' con el autor seleccionado
def do_merge_to_develop(authors):
    current_branch = get_current_branch()
    if current_branch == "develop":
        print("Ya estás en la rama 'develop'. No puedes hacer merge de 'develop' en sí misma.")
        return

    print(f"\nVas a mergear la rama '{current_branch}' en 'develop'.")

    # Seleccionar autor
    print("\nSelecciona el autor del merge:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")

    while True:
        selection = input("\nIngresa el número del autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")

    author_name, author_email = authors[selection]

    # Ajustar la fecha del merge
    new_commit_date = adjust_merge_date(current_branch, "develop")
    if not new_commit_date:
        print("Error al calcular la fecha del merge. Operación cancelada.")
        return

    formatted_date = new_commit_date.strftime("%Y-%m-%d %H:%M:%S %z")

    try:
        subprocess.run(['git', 'checkout', 'develop'], check=True)

        # Realizar el merge con no-ff
        merge_message = f"Merge branch '{current_branch}' into develop"
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = author_name
        env['GIT_AUTHOR_EMAIL'] = author_email
        env['GIT_COMMITTER_NAME'] = author_name
        env['GIT_COMMITTER_EMAIL'] = author_email
        env['GIT_AUTHOR_DATE'] = formatted_date
        env['GIT_COMMITTER_DATE'] = formatted_date

        subprocess.run(['git', 'merge', '--no-ff', current_branch, '-m', merge_message], env=env, check=True)
        print("\nMerge realizado exitosamente en 'develop'.")
    except subprocess.CalledProcessError as e:
        print(f"\nError al realizar el merge: {str(e)}")
    finally:
        # Volver a la rama original
        subprocess.run(['git', 'checkout', current_branch], check=True)

# Realiza un merge de la rama 'develop' en la rama actual con el autor seleccionado
def do_merge_from_develop(authors):
    current_branch = get_current_branch()
    if current_branch == "develop":
        print("Ya estás en la rama 'develop'. No puedes hacer merge desde 'develop' en sí misma.")
        return

    print(f"\nVas a mergear la rama 'develop' en '{current_branch}'.")

    # Seleccionar autor
    print("\nSelecciona el autor del merge:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")

    while True:
        selection = input("\nIngresa el número del autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")

    author_name, author_email = authors[selection]

    # Ajustar la fecha del merge
    new_commit_date = adjust_merge_date("develop", current_branch)
    if not new_commit_date:
        print("Error al calcular la fecha del merge. Operación cancelada.")
        return

    formatted_date = new_commit_date.strftime("%Y-%m-%d %H:%M:%S %z")

    try:
        # Realizar el merge desde develop
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = author_name
        env['GIT_AUTHOR_EMAIL'] = author_email
        env['GIT_COMMITTER_NAME'] = author_name
        env['GIT_COMMITTER_EMAIL'] = author_email
        env['GIT_AUTHOR_DATE'] = formatted_date
        env['GIT_COMMITTER_DATE'] = formatted_date

        subprocess.run(['git', 'checkout', 'develop'], check=True)
        subprocess.run(['git', 'checkout', current_branch], check=True)
        
        merge_message = f"Merge branch 'develop' into {current_branch}"
        subprocess.run(['git', 'merge', '--no-ff', 'develop', '-m', merge_message], env=env, check=True)
        print(f"\nMerge de 'develop' realizado exitosamente en '{current_branch}'.")
    except subprocess.CalledProcessError as e:
        print(f"\nError al realizar el merge: {str(e)}")
    finally:
        subprocess.run(['git', 'checkout', current_branch], check=True)


def do_commit(authors):
    if not has_changes():
        print("No hay cambios para hacer commit.")
        return

    print("\nSelecciona el autor del commit:")
    for key, (name, _) in authors.items():
        print(f"{key}. {name}")

    while True:
        selection = input("\nIngresa el número del autor (1-4): ")
        if selection in authors:
            break
        print("Selección inválida. Por favor, elige un número entre 1-4.")

    commit_message = input("\nIngresa el mensaje del commit: ")

    while True:
        scrum_id = input("\nIngresa solo el número de la subtarea (ej. 52): ")
        if scrum_id.isdigit():
            scrum_id = f"SCRUM-{scrum_id}"
            break
        print("Por favor, ingresa solo el número.")

    full_message = f"{scrum_id} {commit_message}"

    author_name, author_email = authors[selection]

    try:
        last_commit_date_str = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=iso']
        ).decode('utf-8').strip()
        last_commit_date = datetime.strptime(last_commit_date_str, "%Y-%m-%d %H:%M:%S %z")
        print(f"\nLa fecha del último commit fue: {last_commit_date.strftime('%Y-%m-%d %H:%M:%S %z')}")
    except subprocess.CalledProcessError as e:
        print(f"\nError al obtener la fecha del último commit: {str(e)}")
        return

    while True:
        try:
            days_to_add = int(input("\n¿Cuántos días deseas sumar? (0 si es el mismo día): "))
            break
        except ValueError:
            print("Por favor, ingresa un número válido.")

    if days_to_add == 0:
        while True:
            try:
                hours_to_add = int(input("\n¿Cuántas horas deseas sumar al último commit?: "))
                break
            except ValueError:
                print("Por favor, ingresa un número válido.")
        if hours_to_add == 0:
            new_commit_date = last_commit_date + timedelta(minutes=3)
        else:
            new_commit_date = last_commit_date + timedelta(hours=hours_to_add)
    else:
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

    formatted_date = new_commit_date.strftime("%Y-%m-%d %H:%M:%S %z")

    try:
        print("\nAñadiendo cambios al staging area...")
        subprocess.run(['git', 'add', '.'], check=True)

        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = author_name
        env['GIT_AUTHOR_EMAIL'] = author_email
        env['GIT_COMMITTER_NAME'] = author_name
        env['GIT_COMMITTER_EMAIL'] = author_email
        env['GIT_AUTHOR_DATE'] = formatted_date
        env['GIT_COMMITTER_DATE'] = formatted_date

        print("Realizando commit...")
        subprocess.run(['git', 'commit', '-m', full_message], env=env, check=True)
        print("\nCommit realizado exitosamente!")
    except subprocess.CalledProcessError as e:
        print(f"\nError al realizar el commit: {str(e)}")


def main():
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
        if os.path.isdir(project_path):
            os.chdir(project_path)
        else:
            print(f"Error: La ruta '{project_path}' no existe.")
            return

    if not os.path.exists('.git'):
        print("Error: No estás en un repositorio Git")
        return

    current_branch = get_current_branch()
    print(f"Rama actual: {current_branch}")

    last_commit = get_last_commit_message()
    print(f"Último commit: {last_commit}")

    authors = {
        '1': ("Pablo Natera Muñoz", "pnateram@alumnos.unex.es"),
        '2': ("Alejandro Barrena Millán", "abarrenaq@alumnos.unex.es"),
        '3': ("Raúl Martín-Romo Sánchez", "rmartinrw@alumnos.unex.es"),
        '4': ("Pedro Moreno Calderón", "pmorenoj@alumnos.unex.es")
    }

    while True:
        print("\nOpciones disponibles:")
        print("1: Commit")
        print("2: Merge to develop")
        print("3: Merge from develop")
        print("4: Cambiar autor de commit")
        action = input("\n¿Qué deseas hacer? (1-4): ")
        if action in ['1', '2', '3', '4']:
            break
        print("Selección inválida. Por favor, elige un número entre 1 y 4.")

    if action == '1':
        do_commit(authors)
    elif action == '2':
        do_merge_to_develop(authors)
    elif action == '3':
        do_merge_from_develop(authors)
    else:
        change_commit_author(authors)


if __name__ == "__main__":
    main()