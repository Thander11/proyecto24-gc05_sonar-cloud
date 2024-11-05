# tendencias.py - Handle API logic
from flask import jsonify, request
import requests
from concurrent.futures import ThreadPoolExecutor
from config.database import obtener_tendencias_db, obtener_favoritos_usuario, obtener_visualizaciones_usuario
from . import tendencias_bp
import time

def fetch_data(url):
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    print(f"Time taken to fetch {url}: {elapsed_time:.3f}s")
    if response.status_code == 200:
        return response.json()
    return None

@tendencias_bp.route('/tendencias', methods=['GET'])
def obtener_tendencias_route():
    try:
        tendencias_db = obtener_tendencias_db()
        print(tendencias_db)
        tendencias_dict = {t['contenidoId']: dict(t) for t in tendencias_db}

        resultados = []
        series_ids = set()
        urls = []

        for contenido_id, tendencia in tendencias_dict.items():
            tipo = tendencia['tipo']
            if tipo == 'serie':
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
                        if tipo == 'serie' and nombre:
                            if contenido_id not in series_ids:
                                series_ids.add(contenido_id)
                                resultados.append({
                                    'contenidoId': contenido_id,
                                    'serieId': data.get('id'),
                                    'popularidad': tendencias_dict[contenido_id]['popularidad'],
                                    'tipo': tipo,
                                    'nombre': nombre,
                                    'num_temporadas': len(data.get('temporadas', []))
                                })
                        elif nombre:
                            resultados.append({
                                'contenidoId': contenido_id,
                                'popularidad': tendencias_dict[contenido_id]['popularidad'],
                                'tipo': tipo,
                                'nombre': nombre
                            })
                except Exception as e:
                    print(f"Error fetching data from {url}: {e}")
                    continue

        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@tendencias_bp.route('/recomendaciones/<int:usuarioId>', methods=['GET'])
def obtener_recomendaciones(usuarioId):
    try:
        favoritos = obtener_favoritos_usuario(usuarioId)
        visualizaciones = obtener_visualizaciones_usuario(usuarioId)

        generos = {}
        actores = {}

        def contar_elementos(lista, diccionario):
            for item in lista:
                if item in diccionario:
                    diccionario[item] += 1
                else:
                    diccionario[item] = 1

        favoritos_ids = {favorito['contenidoId'] for favorito in favoritos}

        for favorito in favoritos:
            contenido_id = favorito['contenidoId']
            tipo = favorito['tipo']
            url = f'http://127.0.0.1:5005/{tipo}s/{contenido_id}'
            data = fetch_data(url)
            if data:
                contar_elementos(data.get('generos', []), generos)
                for cast in data.get('cast', []):
                    actor = cast['actor']['nombre'] + " " + cast['actor']['apellidos']
                    contar_elementos([actor], actores)

        for visualizacion in visualizaciones:
            contenido_id = visualizacion['contenidoId']
            tipo = visualizacion['tipo']
            if tipo == 'episodio':
                url = f'http://127.0.0.1:5005/series/{contenido_id}/episodio'
            else:
                url = f'http://127.0.0.1:5005/{tipo}s/{contenido_id}'
            data = fetch_data(url)
            if data:
                if tipo == 'episodio':
                    # Obtener la serie a la que pertenece el episodio
                    serie_id = data.get('id')
                    url_serie = f'http://127.0.0.1:5005/series/{serie_id}'
                    data_serie = fetch_data(url_serie)
                    if data_serie:
                        contar_elementos(data_serie.get('generos', []), generos)
                        for cast in data_serie.get('cast', []):
                            actor = cast['actor']['nombre'] + " " + cast['actor']['apellidos']
                            contar_elementos([actor], actores)
                else:
                    contar_elementos(data.get('generos', []), generos)
                    for cast in data.get('cast', []):
                        actor = cast['actor']['nombre'] + " " + cast['actor']['apellidos']
                        contar_elementos([actor], actores)

        generos_frecuentes = sorted(generos.items(), key=lambda x: x[1], reverse=True)
        actores_frecuentes = sorted(actores.items(), key=lambda x: x[1], reverse=True)

        recomendaciones = []

        for genero, _ in generos_frecuentes[:5]:
            for tipo in ['series', 'peliculas']:
                url = f'http://127.0.0.1:5005/{tipo}/buscar/{genero}'
                data = fetch_data(url)
                if data:
                    for item in data:
                        if 'id' in item and item['id'] not in favoritos_ids:
                            print(f"Añadiendo {item['id']} ({tipo[:-1]}) a las recomendaciones")
                            recomendaciones.append({
                                'contenidoId': item['id'],
                                'popularidad': item.get('popularidad', 0),
                                'tipo': tipo[:-1],
                                'nombre': item.get('titulo'),
                                'num_temporadas': len(item.get('temporadas', [])) if tipo == 'series' else None
                            })

        for actor, _ in actores_frecuentes[:5]:
            for tipo in ['series', 'peliculas']:
                url = f'http://127.0.0.1:5005/{tipo}/buscar/{actor}'
                data = fetch_data(url)
                if data:
                    for item in data:
                        if 'id' in item and item['id'] not in favoritos_ids:
                            print(f"Añadiendo {item['id']} ({tipo[:-1]}) a las recomendaciones")
                            recomendaciones.append({
                                'contenidoId': item['id'],
                                'popularidad': item.get('popularidad', 0),
                                'tipo': tipo[:-1],
                                'nombre': item.get('titulo'),
                                'num_temporadas': len(item.get('temporadas', [])) if tipo == 'series' else None
                            })

        print("termine")
        return jsonify(recomendaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400