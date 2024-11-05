# In visualizaciones.py - Update imports at top
from flask import jsonify, request
from concurrent.futures import ThreadPoolExecutor  # Add this
import requests  # Add this
import time  # Add this
from config.database import (
    obtener_visualizaciones_usuario as get_db_visualizaciones,
    crear_visualizacion,
    actualizar_tendencia,
    obtener_visualizacion_especifica
)
from . import visualizaciones_bp


def fetch_data(url):
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    print(f"Time taken to fetch {url}: {elapsed_time:.3f}s")
    if response.status_code == 200:
        return response.json()
    return None
    
@visualizaciones_bp.route('/visualizaciones', methods=['POST'])
def registrar_visualizacion():
    try:
        data = request.get_json()
        
        # Add validation for required fields
        required_fields = ['usuarioId', 'contenidoId', 'duracion', 'tipo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        if crear_visualizacion(data['usuarioId'], data['contenidoId'], data['duracion'], data['tipo']):
            actualizar_tendencia(data['contenidoId'])
            return jsonify({'mensaje': 'Visualización registrada con éxito'}), 201
        return jsonify({'error': 'Error al registrar la visualización'}), 400
    except Exception as e:
        print(f"Error in registrar_visualizacion: {e}")
        return jsonify({'error': str(e)}), 400

@visualizaciones_bp.route('/visualizaciones/<int:usuarioId>', methods=['GET'])
def obtener_historial(usuarioId):
    try:
        visualizaciones_db = get_db_visualizaciones(usuarioId)
        if not visualizaciones_db:
            return jsonify([]), 200

        resultados = []
        urls = []

        for visualizacion in visualizaciones_db:
            contenido_id = visualizacion['contenidoId']
            tipo = visualizacion['tipo']

            if tipo == 'episodio':
                print("bbbbbbbbbbbbbbb")
                print(contenido_id)
                urls.append((f'http://127.0.0.1:5005/series/{contenido_id}/episodio', tipo, contenido_id, dict(visualizacion)))
            elif tipo == 'pelicula':
                print("cccccccccccccccc")

                urls.append((f'http://127.0.0.1:5005/peliculas/{contenido_id}', tipo, contenido_id, dict(visualizacion)))

        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(fetch_data, url): (url, tipo, contenido_id, visualizacion) 
                           for url, tipo, contenido_id, visualizacion in urls}
            
            for future in future_to_url:
                url, tipo, contenido_id, visualizacion = future_to_url[future]
                try:
                    data = future.result()
                    if data:
                        nombre = data.get('titulo')
                        if tipo == 'episodio' and nombre:
                            episode_info = None
                            season_number = 0
                            episode_number = 0

                            for temp_idx, temporada in enumerate(data.get('temporadas', []), 1):
                                for ep_idx, episodio in enumerate(temporada.get('episodios', []), 1):
                                    if episodio['id'] == contenido_id:
                                        episode_info = episodio
                                        season_number = temp_idx
                                        episode_number = ep_idx
                                        break
                                if episode_info:
                                    break

                            if episode_info:
                                resultados.append({
                                    'contenidoId': contenido_id,
                                    'serieId': data.get('id'),
                                    'tipo': tipo,
                                    'nombre': data.get('titulo'),
                                    'titulo_episodio': episode_info['titulo'],
                                    'temporada': season_number,
                                    'episodio': episode_number,
                                    'fechaVisualizacion': visualizacion['fechaVisualizacion'],
                                    'duracionTotal': episode_info['duracion'],
                                    'duracionVista': visualizacion['duracion']
                                })
                        elif tipo == 'pelicula' and nombre:
                            resultados.append({
                                'contenidoId': contenido_id,
                                'tipo': tipo,
                                'nombre': nombre,
                                'fechaVisualizacion': visualizacion['fechaVisualizacion'],
                                'duracionTotal': data.get('duracion', 0),
                                'duracionVista': visualizacion['duracion']
                            })
                except Exception as e:
                    print(f"Error fetching data from {url}: {e}")
                    continue

        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@visualizaciones_bp.route('/visualizaciones/<int:usuarioId>/<int:contenidoId>', methods=['GET'])
def obtener_visualizacion(usuarioId, contenidoId):
    try:
        visualizacion = obtener_visualizacion_especifica(usuarioId, contenidoId)
        
        if not visualizacion:
            return jsonify({'error': 'Visualización no encontrada'}), 404
            
        return jsonify(dict(visualizacion)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400