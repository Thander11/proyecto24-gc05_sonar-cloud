import requests
import json
from time import sleep

BASE_URL = 'http://localhost:5000'

def test_favoritos():
    usuario_id = 1
    contenido_id = 100
    
    print("\n=== Probando endpoints de favoritos ===")
    
    # 1. Agregar favorito
    print("\nProbando agregar favorito...")
    response = requests.post(f'{BASE_URL}/favoritos/{usuario_id}/{contenido_id}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'No content'}")
    
    # 2. Obtener favoritos
    print("\nProbando obtener favoritos...")
    response = requests.get(f'{BASE_URL}/favoritos/{usuario_id}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'No content'}")
    
    # 3. Intentar agregar el mismo favorito (debe fallar)
    print("\nProbando agregar favorito duplicado...")
    response = requests.post(f'{BASE_URL}/favoritos/{usuario_id}/{contenido_id}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'No content'}")
    
    # 4. Eliminar favorito
    print("\nProbando eliminar favorito...")
    response = requests.delete(f'{BASE_URL}/favoritos/{usuario_id}/{contenido_id}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'No content'}")
    
    # 5. Verificar que se eliminó correctamente
    print("\nVerificando que se eliminó...")
    response = requests.get(f'{BASE_URL}/favoritos/{usuario_id}')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'No content'}")

if __name__ == '__main__':
    # Asegúrate de que el servidor esté corriendo antes de ejecutar las pruebas
    try:
        test_favoritos()
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que está corriendo en localhost:5000")