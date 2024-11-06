from flask import jsonify, request
import requests
from concurrent.futures import ThreadPoolExecutor
from config.database import crear_favorito, eliminar_favorito, obtener_favoritos_usuario
from . import favoritos_bp
import time

def fetch_data(url):
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    print(f"Time taken to fetch {url}: {elapsed_time:.3f}s")
    if response.status_code == 200:
        return response.json()
    return None

@favoritos_bp.route('/favoritos/<int:usuarioId>/<int:contenidoId>/<string:tipo>', methods=['POST'])
def agregar_favorito(usuarioId, contenidoId, tipo):
    try:
        if crear_favorito(usuarioId, contenidoId, tipo):
            return jsonify({'mensaje': 'Favorito agregado con éxito'}), 201
        return jsonify({'error': 'Error al agregar favorito'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@favoritos_bp.route('/favoritos/<int:usuarioId>/<int:contenidoId>/<string:tipo>', methods=['DELETE'])
def eliminar_favorito_route(usuarioId, contenidoId, tipo):
    try:
        if eliminar_favorito(usuarioId, contenidoId,tipo):
            return '', 204
        return jsonify({'error': 'Favorito no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@favoritos_bp.route('/favoritos/<int:usuarioId>', methods=['GET'])
def obtener_favoritos(usuarioId):
    try:
        favoritos_db = obtener_favoritos_usuario(usuarioId)
        if not favoritos_db:
            return jsonify({'error': 'Usuario no encontrado o sin favoritos'}), 404

        resultados = []
        urls = []

        for favorito in favoritos_db:
            contenido_id = favorito['contenidoId']
            tipo = favorito['tipo']

            if tipo == 'serie': 
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                print(contenido_id)
                urls.append((f'http://127.0.0.1:5005/series/{contenido_id}', tipo, contenido_id))
            elif tipo == 'pelicula':
                urls.append((f'http://127.0.0.1:5005/peliculas/{contenido_id}', tipo, contenido_id))

        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(fetch_data, url): (url, tipo, contenido_id) 
                           for url, tipo, contenido_id in urls}
            
            for future in future_to_url:
                url, tipo, contenido_id = future_to_url[future]
                try:
                    data = future.result()
                    if data:
                        nombre = data.get('titulo')
                        generos = data.get('generos')
                        if tipo == 'serie':
                            num_temporadas = len(data.get('temporadas', []))
                            if nombre:
                                resultados.append({
                                    'usuarioId': usuarioId,
                                    'serieId': data.get('id'),
                                    'contenidoId': contenido_id,
                                    'fechaAgregado': favorito['fechaAgregado'],
                                    'tipo': tipo,
                                    'nombre': nombre,
                                    'generos': generos,
                                    'num_temporadas': num_temporadas
                                })
                        elif nombre:
                            resultados.append({
                                'usuarioId': usuarioId,
                                'contenidoId': contenido_id,
                                'fechaAgregado': favorito['fechaAgregado'],
                                'tipo': tipo,
                                'nombre': nombre,
                                'generos': generos
                            })
                except Exception as e:
                    print(f"Error fetching data from {url}: {e}")

        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400