import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"  # La URL base del servidor Django

def print_response(response):
    """Imprime el status y el contenido completo de la respuesta."""
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=4))

def test_buscar_usuarios():
    """Prueba la búsqueda de usuarios."""
    print("\nProbando búsqueda de usuarios:")
    params = {'q': 'usuario'}
    response = requests.get(BASE_URL + 'usuarios/buscar/', params=params)
    print_response(response)

def test_get_usuarios():
    """Prueba la obtención de la lista de usuarios."""
    print("\nProbando obtención de lista de usuarios:")
    response = requests.get(BASE_URL + 'usuarios/')
    print_response(response)

def test_post_usuario():
    """Prueba la creación de un nuevo usuario."""
    print("\nProbando creación de un nuevo usuario:")
    nuevo_usuario = {
        "correo_electronico": "test@example.com",
        "contrasena": "contraseña123",
        "nombre_usuario": "testuser"
    }
    response = requests.post(BASE_URL + 'usuarios/', json=nuevo_usuario)
    print_response(response)
    return response.json().get("id")

def test_get_usuario(usuario_id):
    """Prueba la obtención de un usuario por su ID."""
    print(f"\nProbando obtención del usuario con ID {usuario_id}:")
    response = requests.get(f"{BASE_URL}usuarios/{usuario_id}/")
    print_response(response)

def test_put_usuario(usuario_id):
    """Prueba la actualización de un usuario."""
    print(f"\nProbando actualización del usuario con ID {usuario_id}:")
    usuario_actualizado = {
        "correo_electronico": "updated@example.com",
        "contrasena": "nueva_contraseña123",
        "nombre_usuario": "updateduser"
    }
    response = requests.put(f"{BASE_URL}usuarios/{usuario_id}/", json=usuario_actualizado)
    print_response(response)

def test_delete_usuario(usuario_id):
    """Prueba la eliminación de un usuario."""
    print(f"\nProbando eliminación del usuario con ID {usuario_id}:")
    response = requests.delete(f"{BASE_URL}usuarios/{usuario_id}/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Usuario eliminado correctamente.")

def test_perfiles_usuario(usuario_id):
    """Prueba la obtención y creación de perfiles para un usuario."""
    print(f"\nProbando obtención de perfiles del usuario con ID {usuario_id}:")
    response = requests.get(f"{BASE_URL}usuarios/{usuario_id}/perfiles/")
    print_response(response)

    print(f"\nProbando creación de un perfil para el usuario con ID {usuario_id}:")
    nuevo_perfil = {
        "nombre": "Perfil de prueba",
        "lista_visualizacion_reciente": [1, 2],
        "mi_lista": [3, 4],
        "foto_perfil": 1
    }
    response = requests.post(f"{BASE_URL}usuarios/{usuario_id}/perfiles/", json=nuevo_perfil)
    print_response(response)
    return response.json().get("id")

def test_metodo_pago(usuario_id):
    """Prueba la obtención y actualización del método de pago de un usuario."""
    print(f"\nProbando obtención del método de pago del usuario con ID {usuario_id}:")
    response = requests.get(f"{BASE_URL}usuarios/{usuario_id}/pago/")
    print_response(response)

    print(f"\nProbando actualización del método de pago del usuario con ID {usuario_id}:")
    metodo_pago = {
        "numero_tarjeta": "1234567890123456",
        "fecha_caducidad": "12/25",
        "cvc": 123
    }
    response = requests.put(f"{BASE_URL}usuarios/{usuario_id}/pago/", json=metodo_pago)
    print_response(response)

def main():
    # Realizamos las pruebas
    test_buscar_usuarios()
    test_get_usuarios()
    
    # Prueba de creación de usuario y luego operación con el usuario creado
    usuario_id = test_post_usuario()

    if usuario_id:
        test_get_usuario(usuario_id)
        test_put_usuario(usuario_id)
        test_perfiles_usuario(usuario_id)
        test_metodo_pago(usuario_id)
        test_delete_usuario(usuario_id)

if __name__ == "__main__":
    main()
