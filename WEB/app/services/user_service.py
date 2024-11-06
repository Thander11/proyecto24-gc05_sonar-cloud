import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from app.config import Config
from functools import lru_cache
from datetime import datetime, timedelta

class UserService:
    _session = requests.Session()
    retries = Retry(
        total=1,                  # Reduce total retries
        backoff_factor=0.05,      # Reduce backoff time
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=['GET', 'POST', 'DELETE'],  # Allow retries for these methods
        raise_on_status=False
    )
    # Optimize session parameters
    _session.headers.update({
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Keep-Alive': 'timeout=5, max=1000'
    })


    adapter = HTTPAdapter(
        max_retries=retries,
        pool_connections=50,
        pool_maxsize=20,
        pool_block=False
    )

    _session.mount('http://', adapter)
    _session.mount('https://', adapter)
    
    TIMEOUT = (3.05, 5)  # (connect, read) timeout
    # Cache temporal para resultados
    _cache = {}
    CACHE_TTL = timedelta(minutes=5)

    @classmethod
    def _make_request(cls, method, url, **kwargs):
        kwargs.setdefault('timeout', cls.TIMEOUT)
        kwargs.setdefault('verify', False)
        try:
            response = cls._session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error in request {url}: {e}")
            return None

    @classmethod
    def buscar_usuario_por_correo(cls, correo):
        if not correo:
            return None
        response = cls._make_request('GET', 
                                   f'{Config.API_BASE_URL}/api/usuarios/buscar/',
                                   params={'q': correo})
        if response:
            usuarios = response.json()
            return next((u for u in usuarios if u.get('correoelectronico') == correo), None)
        return None

    @classmethod
    def verificar_credenciales(cls, email, password):
        response = cls._make_request('GET',
                                   f'{Config.API_BASE_URL}/api/usuarios/buscar/',
                                   params={'q': email})
        if response:
            usuarios = response.json()
            return next((u for u in usuarios 
                        if u.get('correoelectronico') == email 
                        and u.get('contrasena') == password), None)
        return None

    @classmethod
    def crear_usuario(cls, nuevo_usuario):
        response = cls._make_request('POST',
                                   f'{Config.API_BASE_URL}/api/usuarios/',
                                   json=nuevo_usuario)
        return response.json() if response else None

    @classmethod
    def crear_pago(cls, nuevo_pago):
        response = cls._make_request('POST',
                                   f'{Config.API_BASE_URL}/api/pagos/',
                                   json=nuevo_pago)
        return response.json() if response else None

    @classmethod
    def obtener_perfiles(cls, email):
        usuario = cls.buscar_usuario_por_correo(email)
        if usuario:
            response = cls._make_request('GET',
                                       f'{Config.API_BASE_URL}/api/perfiles/por_usuario/{usuario["id"]}/')
            return response.json() if response else []
        return []

    @classmethod
    def crear_perfil(cls, nuevo_perfil):
        response = cls._make_request('POST',
                                   f'{Config.API_BASE_URL}/api/perfiles/',
                                   json=nuevo_perfil)
        return response.json() if response else None

    @classmethod
    def eliminar_perfil(cls, perfil_id):
        response = cls._make_request('DELETE',
                                   f'{Config.API_BASE_URL}/api/perfiles/{perfil_id}/')
        return response.status_code == 204 if response else False

    @classmethod
    def obtener_perfil(cls, perfil_id):
        response = cls._make_request('GET',
                                   f'{Config.API_BASE_URL}/api/perfiles/{perfil_id}/')
        return response.json() if response else None

    @classmethod
    def actualizar_perfil(cls, perfil_id, perfil_actualizado):
        perfil_actual = cls.obtener_perfil(perfil_id)
        if not perfil_actual:
            return None
        perfil_actualizado['idusuario'] = perfil_actual['idusuario']
        response = cls._make_request('PUT',
                                   f'{Config.API_BASE_URL}/api/perfiles/{perfil_id}/',
                                   json=perfil_actualizado)
        return response.json() if response else None

    @classmethod
    def obtener_pago(cls, usuario_id):
        response = cls._make_request('GET',
                                   f'{Config.API_BASE_URL}/api/pagos/por_usuario/{usuario_id}/')
        if response:
            pagos = response.json()
            return pagos[0] if pagos else None
        return None

    @classmethod
    def actualizar_usuario(cls, usuario_id, usuario_actualizado):
        response = cls._make_request('PUT',
                                   f'{Config.API_BASE_URL}/api/usuarios/{usuario_id}/',
                                   json=usuario_actualizado)
        return response.json() if response else None

    @classmethod
    def actualizar_pago(cls, pago_id, pago_actualizado):
        response = cls._make_request('PUT',
                                   f'{Config.API_BASE_URL}/api/pagos/{pago_id}/',
                                   json=pago_actualizado)
        return response.json() if response else None

    @classmethod
    @lru_cache(maxsize=256)
    def obtener_tendencias(cls):
        start_time = time.time()
        url = 'http://127.0.0.1:5010/tendencias'
        
        kwargs = {
            'timeout': (1, 5),
            'verify': False,
            'allow_redirects': False,
            'headers': {
                'Connection': 'keep-alive',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'Host': '127.0.0.1:5010'
            }
        }

        try:
            conn_start = time.time()
            response = cls._session.get(url, **kwargs)
            print(f"Connection time: {time.time() - conn_start:.3f}s")
            
            if response.ok:
                parse_start = time.time()
                data = response.json()
                print(f"Parse time: {time.time() - parse_start:.3f}s")
                print(f"Total time: {time.time() - start_time:.3f}s")
                return data
            return []
        except Exception as e:
            print(f"Error fetching trends: {e}")
            return []

    @classmethod
    @lru_cache(maxsize=256)
    def obtener_favoritos(cls, id_perfil):
        start_time = time.time()
        url = f'http://127.0.0.1:5010/favoritos/{id_perfil}'
        
        kwargs = {
            'timeout': (0.5, 5),
            'verify': False,
            'allow_redirects': False,
            'headers': {
                'Host': '127.0.0.1:5010'
            }
        }

        try:
            with cls._session.get(url, **kwargs) as response:
                if response.ok:
                    data = response.json()
                    print(f"Total time: {time.time() - start_time:.3f}s")
                    return data
            return []
        except Exception as e:
            print(f"Error fetching favorites: {e}")
            return []

    @classmethod
    @lru_cache(maxsize=256)
    def obtener_visualizaciones_usuario(cls, id_perfil):
        start_time = time.time()
        url = f'http://127.0.0.1:5010/visualizaciones/{id_perfil}'
        
        kwargs = {
            'timeout': (0.5, 3),
            'verify': False,
            'allow_redirects': False,
            'headers': {
                'Host': '127.0.0.1:5010'
            }
        }

        try:
            conn_start = time.time()
            with cls._session.get(url, **kwargs) as response:
                if response.ok:
                    data = response.json()
                    print(f"Total time: {time.time() - start_time:.3f}s")
                    return data
            return []
        except Exception as e:
            print(f"Error fetching visualizations: {e}")
            return []

    @classmethod
    @lru_cache(maxsize=256)
    def obtener_detalles_pelicula(cls, contenido_id):
        response = cls._make_request('GET', f'http://127.0.0.1:5005/peliculas/{contenido_id}')
        return response.json() if response else None

    @classmethod
    @lru_cache(maxsize=256)
    def obtener_detalles_serie(cls, contenido_id):
        start_time = time.time()
        
        url = f'http://127.0.0.1:5005/series/{contenido_id}'
        
        kwargs = {
            'timeout': (1, 1),
            'verify': False,
            'allow_redirects': False,
            'headers': {
                'Connection': 'keep-alive',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'Host': '127.0.0.1:5005'
            }
        }

        try:
            conn_start = time.time()
            response = cls._session.get(url, **kwargs)
            conn_time = time.time() - conn_start
            
            print(f"Connection time: {conn_time:.3f}s")
            
            if response.ok:
                parse_start = time.time()
                data = response.json()
                parse_time = time.time() - parse_start
                
                print(f"Parse time: {parse_time:.3f}s")
                print(f"Total time: {time.time() - start_time:.3f}s")
                
                return data
                
        except Exception as e:
            print(f"Request error: {e}")
            
        return None

        # In UserService.py add method
    @classmethod
    def agregar_favorito(cls, usuario_id, content_id, tipo):
        try:
            response = cls._make_request(
                'POST',
                f'http://127.0.0.1:5010/favoritos/{usuario_id}/{content_id}/{tipo}'
            )
            if response and response.ok:
                # Invalidate cache after successful addition
                cls.invalidate_cache()
                return True
            return False
        except Exception as e:
            print(f"Error adding favorite: {e}")
            return False
    @classmethod
    def invalidate_cache(cls):
        cls.obtener_favoritos.cache_clear()
        cls.obtener_tendencias.cache_clear()
        cls.obtener_visualizaciones_usuario.cache_clear()
        cls.obtener_recomendaciones.cache_clear()  # Add this line to clear recommendations cache

# In UserService.py add new method
    @classmethod
    def eliminar_favorito_api(cls, usuario_id, content_id,tipo):
        try:
            response = cls._make_request(
                'DELETE',
                f'http://127.0.0.1:5010/favoritos/{usuario_id}/{content_id}/{tipo}'
            )
            if response and response.status_code == 204:
                # Invalidate cache after successful deletion
                cls.invalidate_cache()
                return True
            return False
        except Exception as e:
            print(f"Error deleting favorite: {e}")
            return False

# In UserService.py add method
    @classmethod
    def registrar_visualizacion(cls, usuario_id, content_id, duracion, tipo):
        try:
            print(f"Sending visualization request - User: {usuario_id}, Content: {content_id}, Type: {tipo}, Duration: {duracion}")
            response = cls._make_request(
                'POST',
                'http://127.0.0.1:5010/visualizaciones',
                json={
                    'usuarioId': usuario_id,
                    'contenidoId': content_id,
                    'duracion': duracion,
                    'tipo': tipo
                }
            )
            if response:
                print("Visualization registered successfully")
                cls.invalidate_cache()
                return True
            print("Failed to register visualization")
            return False
        except Exception as e:
            print(f"Error registering visualization: {e}")
            return False

    @classmethod
    def buscar_peliculas(cls, query):
        response = cls._make_request('GET', f'http://127.0.0.1:5005/peliculas/buscar/{query}')
        return response.json() if response else []

    @classmethod
    def buscar_series(cls, query):
        response = cls._make_request('GET', f'http://127.0.0.1:5005/series/buscar/{query}')
        return response.json() if response else []
    
    @classmethod
    @lru_cache(maxsize=256)
    def obtener_recomendaciones(cls, id_perfil):
        start_time = time.time()
        url = f'http://127.0.0.1:5010/recomendaciones/{id_perfil}'
        
        kwargs = {
            'timeout': (0.5, 5),
            'verify': False,
            'allow_redirects': False,
            'headers': {
                'Host': '127.0.0.1:5010'
            }
        }

        try:
            with cls._session.get(url, **kwargs) as response:
                if response.ok:
                    data = response.json()
                    print(f"Total time: {time.time() - start_time:.3f}s")
                    return data
            return []
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
            return []

    @classmethod
    def obtener_peliculas(cls):
        response = cls._make_request('GET', 'http://127.0.0.1:5005/peliculas')
        return response.json() if response else []

    @classmethod
    def obtener_detalles_pelicula(cls, pelicula_id):
        response = cls._make_request('GET', f'http://127.0.0.1:5005/peliculas/{pelicula_id}')
        return response.json() if response else None

    @classmethod
    def obtener_generos(cls):
        response = cls._make_request('GET', 'http://127.0.0.1:5005/generos')
        return response.json() if response else []
    @classmethod
    def obtener_series(cls):
        response = cls._make_request('GET', 'http://127.0.0.1:5005/series')
        return response.json() if response else []

    @classmethod
    def obtener_personas(cls):
        response = cls._make_request('GET', 'http://127.0.0.1:5005/personas')
        return response.json() if response else []

    @classmethod
    def actualizar_pelicula(cls, pelicula_id, pelicula_actualizada):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/peliculas/{pelicula_id}', json=pelicula_actualizada)
        return response.json() if response else None

    @classmethod
    def crear_pelicula(cls, pelicula_nueva):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/peliculas', json=pelicula_nueva)
        return response.json() if response else None
    
    @classmethod
    def eliminar_pelicula(cls, pelicula_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/peliculas/{pelicula_id}')
        return response.status_code == 204 if response else False


# En UserService.py

    @classmethod
    def actualizar_serie(cls, serie_id, serie_actualizada):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/series/{serie_id}', json=serie_actualizada)
        if response:
            # Limpiar caché específico
            cls.obtener_detalles_serie.cache_clear()
            return response.json()
        return None

    @classmethod
    def actualizar_temporada(cls, temporada_id, temporada_actualizada):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/temporadas/{temporada_id}', json=temporada_actualizada)
        if response:
            # Limpiar caché específico
            cls.obtener_detalles_serie.cache_clear()
            return response.json()
        return None

    @classmethod
    def crear_temporada(cls, temporada_nueva):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/temporadas', json=temporada_nueva)
        if response:
            # Limpiar caché específico
            cls.obtener_detalles_serie.cache_clear()
            return response.json()
        return None

    @classmethod
    def actualizar_episodio(cls, episodio_id, episodio_actualizado):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/episodios/{episodio_id}', json=episodio_actualizado)
        if response:
            # Limpiar caché específico
            cls.obtener_detalles_serie.cache_clear()
            return response.json()
        return None

    @classmethod
    def crear_episodio(cls, episodio_nuevo):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/episodios', json=episodio_nuevo)
        if response:
            # Limpiar caché específico
            cls.obtener_detalles_serie.cache_clear()
            return response.json()
        return None

    @classmethod
    def crear_serie(cls, serie_nueva):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/series', json=serie_nueva)
        return response.json() if response else None

    @classmethod
    def eliminar_temporada(cls, temporada_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/temporadas/{temporada_id}')
        if response:
            cls.obtener_detalles_serie.cache_clear()
            return True
        return False

    @classmethod
    def eliminar_episodio(cls, episodio_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/episodios/{episodio_id}')
        if response:
            cls.obtener_detalles_serie.cache_clear()
            return True
        return False

    @classmethod
    def eliminar_serie(cls, serie_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/series/{serie_id}')
        if response:
            cls.obtener_detalles_serie.cache_clear()
            return True
        return False

    @classmethod
    def eliminar_persona(cls, persona_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/personas/{persona_id}')
        return response is not None

    @classmethod
    def eliminar_personaje(cls, personaje_id):
        response = cls._make_request('DELETE', f'http://127.0.0.1:5005/personajes/{personaje_id}')
        return response is not None

    @classmethod
    def crear_persona(cls, persona_nueva):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/personas', json=persona_nueva)
        return response.json() if response else None

    @classmethod
    def crear_personaje(cls, personaje_nuevo):
        response = cls._make_request('POST', 'http://127.0.0.1:5005/personajes', json=personaje_nuevo)
        return response.json() if response else None

    @classmethod
    def actualizar_persona(cls, persona_id, persona_actualizada):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/personas/{persona_id}', json=persona_actualizada)
        return response.json() if response else None

    @classmethod
    def actualizar_personaje(cls, personaje_id, personaje_actualizado):
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/personajes/{personaje_id}', json=personaje_actualizado)
        return response.json() if response else None
    
    @classmethod
    def obtener_personajes(cls):
        # Remove caching for personajes list
        response = cls._make_request('GET', 'http://127.0.0.1:5005/personajes')
        return response.json() if response else []

    @classmethod 
    def actualizar_cast_serie(cls, serie_id, cast_ids):
        data = {
            "cast": cast_ids  
        }
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/series/{serie_id}/cast', json=data)
        # Clear the series cache after updating cast
        if response:
            cls.obtener_detalles_serie.cache_clear()
        return response.json() if response else None

    @classmethod 
    def actualizar_cast_pelicula(cls, pelicula_id, cast_ids):
        data = {
            "cast": cast_ids  
        }
        response = cls._make_request('PUT', f'http://127.0.0.1:5005/peliculas/{pelicula_id}/cast', json=data)
        return response.json() if response else None