from flask import Blueprint, render_template, request, redirect, url_for, session
import threading
import time  # Add at top of file
from datetime import datetime
from app.services import UserService
import random

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/debug_routes')
def debug_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append(f"{rule.endpoint}: {rule.rule}")
    return "<br>".join(routes)


@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/verificar_correo', methods=['POST'])
def verificar_correo():
    correo = request.form.get('email')
    print(f"Verificando correo: {correo}")
    
    usuario = UserService.buscar_usuario_por_correo(correo)
    if usuario:
        return redirect(url_for('auth.login', email=correo))
    return redirect(url_for('auth.register', email=correo))

@auth_bp.route('/login')
def login():
    email = request.args.get('email', '')
    return render_template('login.html', email=email)

@auth_bp.route('/verificar_login', methods=['POST'])
def verificar_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    usuario = UserService.verificar_credenciales(email, password)
    if usuario:
        session['usuario'] = usuario  # Almacena los datos del usuario en la sesión
        return redirect(url_for('auth.perfiles'))
    return redirect(url_for('auth.login', email=email))

@auth_bp.route('/register')
def register():
    email = request.args.get('email', '')
    return render_template('register.html', email=email)

@auth_bp.route('/verificar_registro', methods=['POST'])
def verificar_registro():
    email = request.form.get('email')
    password = request.form.get('password')
    nombre_usuario = request.form.get('nombre_usuario')
    numero_tarjeta = request.form.get('numero_tarjeta')
    fecha_caducidad = request.form.get('fecha_caducidad')
    cvc = request.form.get('cvc')
    
    nuevo_usuario = {
        "correoelectronico": email,
        "contrasena": password,
        "nombreusuario": nombre_usuario
    }
    
    response_usuario = UserService.crear_usuario(nuevo_usuario)
    if response_usuario:
        usuario_id = response_usuario.get('id')
        nuevo_pago = {
            "numerotarjeta": numero_tarjeta,
            "fechacaducidad": fecha_caducidad,
            "cvc": cvc,
            "idusuario": usuario_id
        }
        response_pago = UserService.crear_pago(nuevo_pago)
        if response_pago:
            return redirect(url_for('auth.login', email=email))
    return redirect(url_for('auth.register', email=email))

@auth_bp.route('/perfiles')
def perfiles():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    email = usuario.get('correoelectronico')
    perfiles = UserService.obtener_perfiles(email)
    return render_template('perfiles.html', perfiles=perfiles)

@auth_bp.route('/crear_perfil')
def crear_perfil():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    email = usuario.get('correoelectronico')
    return render_template('crear_perfil.html', email=email)

@auth_bp.route('/verificar_crear_perfil', methods=['POST'])
def verificar_crear_perfil():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    
    email = usuario.get('correoelectronico')
    nombre_perfil = request.form.get('nombreperfil')
    foto_perfil = request.form.get('fotoperfil')
    
    usuario_id = usuario.get('id')
    nuevo_perfil = {
        "nombreperfil": nombre_perfil,
        "fotoperfil": foto_perfil,
        "idusuario": usuario_id
    }
    print(f"Creando perfil: {nuevo_perfil}")
    response_perfil = UserService.crear_perfil(nuevo_perfil)
    if response_perfil:
        print(f"Perfil creado: {response_perfil}")
        return redirect(url_for('auth.perfiles'))
    else:
        print("Error al crear el perfil.")
    return redirect(url_for('auth.crear_perfil'))

@auth_bp.route('/eliminar_perfil', methods=['POST'])
def eliminar_perfil():
    perfil_id = request.form.get('id')
    if not perfil_id:
        return redirect(url_for('auth.perfiles'))
    
    response = UserService.eliminar_perfil(perfil_id)
    if response:
        print(f"Perfil eliminado: {perfil_id}")
    else:
        print("Error al eliminar el perfil.")
    return redirect(url_for('auth.perfiles'))

@auth_bp.route('/editar_perfil')
def editar_perfil():
    perfil_id = request.args.get('id')
    if not perfil_id:
        return redirect(url_for('auth.perfiles'))
    
    perfil = UserService.obtener_perfil(perfil_id)
    if not perfil:
        return redirect(url_for('auth.perfiles'))
    
    return render_template('editar_perfil.html', perfil=perfil)

@auth_bp.route('/verificar_editar_perfil', methods=['POST'])
def verificar_editar_perfil():
    perfil_id = request.form.get('id')
    nombre_perfil = request.form.get('nombreperfil')
    foto_perfil = request.form.get('fotoperfil')
    
    perfil_actualizado = {
        "nombreperfil": nombre_perfil,
        "fotoperfil": foto_perfil
    }
    
    response = UserService.actualizar_perfil(perfil_id, perfil_actualizado)
    if response:
        print(f"Perfil actualizado: {perfil_id}")
    else:
        print("Error al actualizar el perfil.")
    return redirect(url_for('auth.perfiles'))



@auth_bp.route('/display_videos')
def display_videos():
    perfil_id = request.args.get('id')
    
    if perfil_id:
        perfil = UserService.obtener_perfil(perfil_id)
        if not perfil:
            return redirect(url_for('auth.perfiles'))
        session['perfil'] = perfil  # Almacena el perfil en la sesión
    else:
        perfil = session.get('perfil')
        if not perfil:
            return redirect(url_for('auth.perfiles'))
        perfil_id = perfil.get('idperfil')

    usuario = session.get('usuario')
    email = usuario.get('correoelectronico')
    perfiles = UserService.obtener_perfiles(email)
    
    results = {
        'tendencias': None,
        'favoritos': None,
        'visualizaciones': None,
        'recomendaciones': None,
        'allFilms': None,
        'allSeries': None
    }

    # Functions for each operation
    def get_tendencias():
        results['tendencias'] = UserService.obtener_tendencias()
    print("he llamado a las funciones1")

    def get_favoritos(perfil_id):
        results['favoritos'] = UserService.obtener_favoritos(perfil_id)
    print("he llamado a las funciones2")

    def get_visualizaciones(perfil_id):
        results['visualizaciones'] = UserService.obtener_visualizaciones_usuario(perfil_id)
    print("he llamado a las funciones3")
    def get_recomendaciones(perfil_id):
        results['recomendaciones'] = UserService.obtener_recomendaciones(perfil_id)
    print("he llamado a las funciones4")
    def get_allFilms():
        results['allFilms'] = UserService.obtener_peliculas()
        print("he llamado a las funciones5")
    def get_allSeries():
        results['allSeries'] = UserService.obtener_series()
        print("he llamado a las funciones6")
    # Create threads
    t1 = threading.Thread(target=get_tendencias)
    t2 = threading.Thread(target=get_favoritos, args=(perfil_id,))
    t3 = threading.Thread(target=get_visualizaciones, args=(perfil_id,))
    t4 = threading.Thread(target=get_recomendaciones, args=(perfil_id,))
    t5 = threading.Thread(target=get_allFilms)
    t6 = threading.Thread(target=get_allSeries)


    # Start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    # Wait for all threads to complete
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    # Obtener resultados
    tendencias = results['tendencias']
    favoritos = results['favoritos']
    visualizaciones = results['visualizaciones']
    recomendaciones = results['recomendaciones']
    allFilms = results['allFilms']
    allSeries = results['allSeries']
    
    # Limpiar las visualizaciones
    visualizaciones_clean = filtrarVisualizaciones(visualizaciones)
    print("Visualizaciones limpias: ", visualizaciones_clean)

    allFilms = randomizarLista(allFilms)
    allSeries = randomizarLista(allSeries)

    print("All Films: ", allSeries)
    
    return render_template('display_videos.html', perfil=perfil, perfiles=perfiles, 
                          tendencias=tendencias, favoritos=favoritos, visualizaciones=visualizaciones_clean, recomendaciones=recomendaciones,
                          allFilms=allFilms, allSeries=allSeries)

@auth_bp.route('/usuario')
def usuario():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    pago = UserService.obtener_pago(usuario['id'])
    # Si pago es None, poner uno de copia
    if not pago:
        pago = {"numerotarjeta": "0000 0000 0000 0000", "fechacaducidad": "00/00", "cvc": "000"}
    return render_template('usuario.html', usuario=usuario, pago=pago)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))


@auth_bp.route('/verificar_editar_usuario', methods=['POST'])
def verificar_editar_usuario():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))

    usuario_id = usuario.get('id')
    pago = UserService.obtener_pago(usuario_id)

    # Actualizar solo los campos que no están vacíos
    usuario_actualizado = {
        "correoelectronico": request.form.get('correoelectronico') or usuario['correoelectronico'],
        "contrasena": request.form.get('contrasena') or usuario['contrasena'],
        "nombreusuario": request.form.get('nombreusuario') or usuario['nombreusuario']
    }

    # Combinar los campos de mes y año en un solo campo de fecha de caducidad
    mes = request.form.get('mes')
    anio = request.form.get('anio')
    fechacaducidad = f"{mes}/{anio}" if mes and anio else pago['fechacaducidad']

    pago_actualizado = {
        "numerotarjeta": request.form.get('numerotarjeta') or pago['numerotarjeta'],
        "fechacaducidad": fechacaducidad,
        "cvc": request.form.get('cvc') or pago['cvc'],
        "idusuario": usuario_id
    }

    response_usuario = UserService.actualizar_usuario(usuario_id, usuario_actualizado)
    response_pago = UserService.actualizar_pago(pago['id'], pago_actualizado)

    if response_usuario and response_pago:
        # Actualizar la sesión con los nuevos datos del usuario
        session['usuario'] = response_usuario
        print(f"Usuario y pago actualizados: {usuario_id}")
    else:
        print("Error al actualizar el usuario o el pago.")
    
    return redirect(url_for('auth.usuario'))

# In auth.py - Update the route

@auth_bp.route('/content')
def content_details():
    tipo = request.args.get('tipo')
    content_id = request.args.get('id', type=int)
    serie_id = request.args.get('idserie', type=int)

    if not tipo:
        return "Missing parameters", 400

    print(f"Accessing content_details with tipo={tipo}, id={content_id}, idserie={serie_id}")
    start_time = time.time()

    if tipo == 'pelicula':
        content = UserService.obtener_detalles_pelicula(content_id)
    elif tipo == 'serie':
        # Obtener el primer episodio de la serie
        serie = UserService.obtener_detalles_serie(content_id)
        if serie and 'temporadas' in serie:
            for temporada in serie['temporadas']:
                if 'episodios' in temporada and len(temporada['episodios']) > 0:
                    primer_episodio_id = temporada['episodios'][0]['id']
                    return redirect(url_for('auth.content_details', tipo='episodio', id=primer_episodio_id, idserie=content_id))
        return "No episodes found for this series", 404
    elif tipo == 'episodio':
        serie = UserService.obtener_detalles_serie(serie_id)
        if serie and 'temporadas' in serie:
            for temporada in serie['temporadas']:
                for episodio in temporada['episodios']:
                    if episodio['id'] == content_id:
                        content = episodio
                        content['titulo_serie'] = serie['titulo']
                        content['generos'] = serie['generos']
                        content['cast'] = serie['cast']
                        content['temporadas'] = serie['temporadas']
                        break
    else:
        return "Invalid content type", 400

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time}")
    if not content:
        print(f"Content not found for {tipo} - {content_id}")
        return "Content not found", 404
    
    return render_template('content_details.html', content=content, tipo=tipo, serie_id=serie_id)



@auth_bp.route('/agregar_favorito', methods=['POST'])
def agregar_favorito():
    try:
        perfil = session.get('perfil')
        if not perfil:
            return redirect(url_for('auth.perfiles'))
        
        content_id = request.form.get('contentId')
        tipo = request.form.get('tipo')
        usuario_id = perfil.get('idperfil')

        # Add debug logging
        print(f"Adding favorite - User: {usuario_id}, Content: {content_id}, Type: {tipo}")

        response = UserService.agregar_favorito(usuario_id, content_id, tipo)
        if not response:
            print("Error al agregar favorito")
            
        return redirect(url_for('auth.display_videos', id=usuario_id))
    except Exception as e:
        print(f"Error in agregar_favorito: {e}")
        return redirect(url_for('auth.display_videos', id=usuario_id))
# In auth.py add new route
@auth_bp.route('/eliminar_favorito', methods=['POST'])
def eliminar_favorito():
    try:
        perfil = session.get('perfil')
        if not perfil:
            return redirect(url_for('auth.perfiles'))
        
        content_id = request.form.get('contentId')
        usuario_id = perfil.get('idperfil')
        tipo = request.form.get('tipo')

        print(f"Removing favorite - User: {usuario_id}, Content: {content_id}")

        response = UserService.eliminar_favorito_api(usuario_id, content_id,tipo)
        if not response:
            print("Error al eliminar favorito")
            
        return redirect(url_for('auth.display_videos', id=usuario_id))
    except Exception as e:
        print(f"Error in eliminar_favorito: {e}")
        return redirect(url_for('auth.display_videos', id=usuario_id))

# In auth.py add new route
@auth_bp.route('/ver_video', methods=['POST'])
def ver_video():
    try:
        perfil = session.get('perfil')
        if not perfil:
            return redirect(url_for('auth.perfiles'))
        
        content_id = request.form.get('contentId')
        tipo = request.form.get('tipo')
        duracion = random.randint(10, 30)
        usuario_id = perfil.get('idperfil')

        print(f"Adding visualization - User: {usuario_id}, Content: {content_id}, Type: {tipo}, Duration: {duracion}")

        # Register visualization
        UserService.registrar_visualizacion(usuario_id, content_id, duracion, tipo)
        video_url = "https://www.youtube.com/embed/UiOYxLrKYYc?si=H8_LXlTiWjllAymV"
        return render_template('video_player.html', video_url=video_url)

    except Exception as e:
        print(f"Error in ver_video: {e}")
        return redirect(url_for('auth.display_videos', id=usuario_id))


@auth_bp.route('/buscar_contenido', methods=['GET'])
def buscar_contenido():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('auth.display_videos', id=session.get('perfil', {}).get('id')))
    
    # Realizar las búsquedas en los endpoints correspondientes
    peliculas = UserService.buscar_peliculas(query)
    series = UserService.buscar_series(query)
    
    return render_template('resultados_busqueda.html', query=query, peliculas=peliculas, series=series)

@auth_bp.route('/gestion')
def gestion():
    usuario = session.get('usuario')
    if not usuario or usuario.get('id') != 0:
        return redirect(url_for('auth.index'))
    return render_template('gestion.html')


@auth_bp.route('/gestion_peliculas')
def gestion_peliculas():
    peliculas = UserService.obtener_peliculas()
    return render_template('gestion_peliculas.html', peliculas=peliculas)

@auth_bp.route('/modificar_pelicula/<int:pelicula_id>')
def modificar_pelicula(pelicula_id):
    pelicula = UserService.obtener_detalles_pelicula(pelicula_id)
    generos = UserService.obtener_generos()
    return render_template('modificar_pelicula.html', pelicula=pelicula, generos=generos)

@auth_bp.route('/gestion_series')
def gestion_series():
    series = UserService.obtener_series()
    return render_template('gestion_series.html', series=series)

@auth_bp.route('/anadir_pelicula')
def anadir_pelicula():
    generos = UserService.obtener_generos()
    return render_template('anadir_pelicula.html', generos=generos)


@auth_bp.route('/modificar_serie/<int:serie_id>')
def modificar_serie(serie_id):
    serie = UserService.obtener_detalles_serie(serie_id)
    generos = UserService.obtener_generos()
    return render_template('modificar_serie.html', serie=serie, generos=generos)

@auth_bp.route('/anadir_serie')
def anadir_serie():
    generos = UserService.obtener_generos()
    return render_template('anadir_serie.html', generos=generos)
@auth_bp.route('/editar_personas')

@auth_bp.route('/editar_personas')
def editar_personas():
    personas = UserService.obtener_personas()
    # Sort personas by nombre and apellidos
    personas_sorted = sorted(personas, key=lambda x: f"{x['nombre']} {x['apellidos']}")
    return render_template('editar_personas.html', personas=personas_sorted)


@auth_bp.route('/verificar_modificar_pelicula', methods=['POST'])
def verificar_modificar_pelicula():
    pelicula_id = request.form.get('id')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    duracion = request.form.get('duracion')
    lanzamiento = request.form.get('lanzamiento')
    generos = [int(id) for id in request.form.get('generos').strip('[]').split(',') if id]

    pelicula_actualizada = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento,
        "generos": generos
    }

    response = UserService.actualizar_pelicula(pelicula_id, pelicula_actualizada)
    if response:
        print(f"Película actualizada: {pelicula_id}")
    else:
        print("Error al actualizar la película.")
    return redirect(url_for('auth.gestion_peliculas'))

@auth_bp.route('/verificar_anadir_pelicula', methods=['POST'])
def verificar_anadir_pelicula():
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    duracion = int(request.form.get('duracion'))
    lanzamiento = int(request.form.get('lanzamiento'))
    generos = [int(id) for id in request.form.get('generos').strip('[]').split(',') if id]

    pelicula_nueva = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento,
        "generos": generos
    }

    response = UserService.crear_pelicula(pelicula_nueva)
    if response:
        print(f"Película creada: {response}")
    else:
        print("Error al crear la película.")
    return redirect(url_for('auth.gestion_peliculas'))
    
@auth_bp.route('/eliminar_pelicula/<int:pelicula_id>', methods=['POST'])
def eliminar_pelicula(pelicula_id):
    response = UserService.eliminar_pelicula(pelicula_id)
    if response:
        print(f"Película eliminada: {pelicula_id}")
    else:
        print("Error al eliminar la película.")
    return redirect(url_for('auth.gestion_peliculas'))


# Series routes
@auth_bp.route('/verificar_modificar_serie', methods=['POST'])
def verificar_modificar_serie():
    serie_id = request.form.get('id')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    lanzamiento = int(request.form.get('lanzamiento'))
    generos = [int(id) for id in request.form.get('generos').strip('[]').split(',') if id]

    serie_actualizada = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "lanzamiento": lanzamiento,
        "generos": generos
    }

    response = UserService.actualizar_serie(serie_id, serie_actualizada)
    if response:
        print(f"Serie actualizada: {serie_id}")
    else:
        print("Error al actualizar la serie.")
    return redirect(url_for('auth.gestion_series'))

# Temporadas routes
@auth_bp.route('/verificar_modificar_temporada', methods=['POST'])
def verificar_modificar_temporada():
    temporada_id = request.form.get('id')
    nombre = request.form.get('nombre')
    lanzamiento = int(request.form.get('lanzamiento'))

    temporada_actualizada = {
        "nombre": nombre,
        "lanzamiento": lanzamiento
    }

    response = UserService.actualizar_temporada(temporada_id, temporada_actualizada)
    if response:
        print(f"Temporada actualizada: {temporada_id}")
    else:
        print("Error al actualizar la temporada.")
    return redirect(url_for('auth.modificar_serie', serie_id=request.form.get('serie_id')))

@auth_bp.route('/verificar_crear_temporada', methods=['POST'])
def verificar_crear_temporada():
    serie_id = request.form.get('serie_id')
    nombre = request.form.get('nombre')
    lanzamiento = int(request.form.get('lanzamiento'))

    nueva_temporada = {
        "nombre": nombre,
        "lanzamiento": lanzamiento,
        "serie_id": serie_id
    }

    response = UserService.crear_temporada(nueva_temporada)
    if response:
        print(f"Temporada creada para serie: {serie_id}")
    else:
        print("Error al crear la temporada.")
    return redirect(url_for('auth.modificar_serie', serie_id=serie_id))

# Episodios routes
@auth_bp.route('/verificar_modificar_episodio', methods=['POST'])
def verificar_modificar_episodio():
    episodio_id = request.form.get('id')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    duracion = int(request.form.get('duracion'))
    lanzamiento = int(request.form.get('lanzamiento'))

    episodio_actualizado = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento
    }

    response = UserService.actualizar_episodio(episodio_id, episodio_actualizado)
    if response:
        print(f"Episodio actualizado: {episodio_id}")
    else:
        print("Error al actualizar el episodio.")
    return redirect(url_for('auth.modificar_serie', serie_id=request.form.get('serie_id')))

@auth_bp.route('/verificar_crear_episodio', methods=['POST'])
def verificar_crear_episodio():
    temporada_id = request.form.get('idTemporada')  # Cambiado de temporada_id
    serie_id = request.form.get('serie_id')
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    duracion = int(request.form.get('duracion'))
    lanzamiento = int(request.form.get('lanzamiento'))

    nuevo_episodio = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento,
        "idTemporada": int(temporada_id)  # Asegúrate de que sea un entero
    }

    response = UserService.crear_episodio(nuevo_episodio)
    if response:
        print(f"Episodio creado para temporada: {temporada_id}")
    else:
        print("Error al crear el episodio.")
    return redirect(url_for('auth.modificar_serie', serie_id=serie_id))

@auth_bp.route('/verificar_anadir_serie', methods=['POST'])
def verificar_anadir_serie():
    titulo = request.form.get('titulo')
    sinopsis = request.form.get('sinopsis')
    duracion = int(request.form.get('duracion'))
    lanzamiento = int(request.form.get('lanzamiento'))
    generos = [int(id) for id in request.form.get('generos').strip('[]').split(',') if id]

    serie_nueva = {
        "titulo": titulo,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento,
        "generos": generos
    }

    response = UserService.crear_serie(serie_nueva)
    if response:
        print(f"Serie creada: {response}")
    else:
        print("Error al crear la serie.")
    return redirect(url_for('auth.gestion_series'))

@auth_bp.route('/eliminar_temporada/<int:temporada_id>', methods=['POST'])
def eliminar_temporada(temporada_id):
    serie_id = request.form.get('serie_id')
    response = UserService.eliminar_temporada(temporada_id)
    if response:
        print(f"Temporada eliminada: {temporada_id}")
    else:
        print("Error al eliminar la temporada.")
    return redirect(url_for('auth.modificar_serie', serie_id=serie_id))

@auth_bp.route('/eliminar_episodio/<int:episodio_id>', methods=['POST'])
def eliminar_episodio(episodio_id):
    serie_id = request.form.get('serie_id')
    response = UserService.eliminar_episodio(episodio_id)
    if response:
        print(f"Episodio eliminado: {episodio_id}")
    else:
        print("Error al eliminar el episodio.")
    return redirect(url_for('auth.modificar_serie', serie_id=serie_id))

@auth_bp.route('/eliminar_serie/<int:serie_id>', methods=['POST'])
def eliminar_serie(serie_id):
    response = UserService.eliminar_serie(serie_id)
    if response:
        print(f"Serie eliminada: {serie_id}")
    else:
        print("Error al eliminar la serie.")
    return redirect(url_for('auth.gestion_series'))


@auth_bp.route('/eliminar_persona/<int:persona_id>', methods=['POST'])
def eliminar_persona(persona_id):
    response = UserService.eliminar_persona(persona_id)
    if response:
        print(f"Persona eliminada: {persona_id}")
    else:
        print("Error al eliminar la persona")
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/eliminar_personaje/<int:personaje_id>', methods=['POST'])
def eliminar_personaje(personaje_id):
    response = UserService.eliminar_personaje(personaje_id)
    if response:
        print(f"Personaje eliminado: {personaje_id}")
    else:
        print("Error al eliminar el personaje")
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/verificar_crear_persona', methods=['POST'])
def verificar_crear_persona():
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    edad = int(request.form.get('edad'))
    
    nueva_persona = {
        "nombre": nombre,
        "apellidos": apellidos,
        "edad": edad
    }
    
    response = UserService.crear_persona(nueva_persona)
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/verificar_crear_personaje', methods=['POST'])
def verificar_crear_personaje():
    nombre = request.form.get('nombre')
    actor_id = request.form.get('actor_id')  # Changed from persona_id to actor_id
    
    nuevo_personaje = {
        "nombre": nombre,
        "actor_id": int(actor_id)  # Changed from idPersona to actor_id
    }
    
    response = UserService.crear_personaje(nuevo_personaje)
    if response:
        print(f"Personaje creado: {response}")
    else:
        print("Error al crear el personaje.")
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/verificar_modificar_persona', methods=['POST'])
def verificar_modificar_persona():
    persona_id = request.form.get('id')
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    edad = int(request.form.get('edad'))

    persona_actualizada = {
        "nombre": nombre,
        "apellidos": apellidos,
        "edad": edad
    }

    response = UserService.actualizar_persona(persona_id, persona_actualizada)
    if response:
        print(f"Persona actualizada: {persona_id}")
    else:
        print("Error al actualizar la persona")
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/verificar_modificar_personaje', methods=['POST'])
def verificar_modificar_personaje():
    personaje_id = request.form.get('id')
    nombre = request.form.get('nombre')
    actor_id = request.form.get('actor_id')

    personaje_actualizado = {
        "nombre": nombre,
        "actor_id": int(actor_id)
    }

    response = UserService.actualizar_personaje(personaje_id, personaje_actualizado)
    if response:
        print(f"Personaje actualizado: {personaje_id}")
    else:
        print("Error al actualizar el personaje")
    return redirect(url_for('auth.editar_personas'))

@auth_bp.route('/gestionar_cast_serie/<int:serie_id>')
def gestionar_cast_serie(serie_id):
    serie = UserService.obtener_detalles_serie(serie_id)
    todos_personajes = UserService.obtener_personajes()
    
    # Get current cast ids
    cast_actual = []
    if serie and 'cast' in serie:
        cast_actual = [personaje['id'] for personaje in serie['cast']]
    
    return render_template('gestionar_cast_serie.html', 
                         serie=serie, 
                         todos_personajes=todos_personajes,
                         cast_actual=cast_actual)

@auth_bp.route('/actualizar_cast_serie/<int:serie_id>', methods=['POST'])
def actualizar_cast_serie(serie_id):
    personajes = request.form.get('personajes[]', '')
    personajes_ids = [int(id) for id in personajes.split(',') if id]
    
    response = UserService.actualizar_cast_serie(serie_id, personajes_ids)
    if response:
        print(f"Cast actualizado para serie: {serie_id}")
    else:
        print("Error al actualizar el cast")
    return redirect(url_for('auth.gestion_series'))

@auth_bp.route('/gestionar_cast_pelicula/<int:pelicula_id>')
def gestionar_cast_pelicula(pelicula_id):
    pelicula = UserService.obtener_detalles_pelicula(pelicula_id)
    todos_personajes = UserService.obtener_personajes()
    
    # Get current cast ids
    cast_actual = []
    if pelicula and 'cast' in pelicula:
        cast_actual = [personaje['id'] for personaje in pelicula['cast']]
    
    return render_template('gestionar_cast_pelicula.html', 
                         pelicula=pelicula, 
                         todos_personajes=todos_personajes,
                         cast_actual=cast_actual)

@auth_bp.route('/actualizar_cast_pelicula/<int:pelicula_id>', methods=['POST'])
def actualizar_cast_pelicula(pelicula_id):
    personajes = request.form.get('personajes[]', '')
    personajes_ids = [int(id) for id in personajes.split(',') if id]
    
    response = UserService.actualizar_cast_pelicula(pelicula_id, personajes_ids)
    if response:
        print(f"Cast actualizado para película: {pelicula_id}")
    else:
        print("Error al actualizar el cast")
    return redirect(url_for('auth.gestion_peliculas'))


def filtrarVisualizaciones(visualizaciones):
    # Convertir las fechas de visualización a objetos datetime para facilitar la comparación
    for visualizacion in visualizaciones:
        visualizacion['fechaVisualizacion'] = datetime.fromisoformat(visualizacion['fechaVisualizacion'])

    # Crear un diccionario para almacenar la visualización más reciente por serieId
    visualizaciones_dict = {}
    visualizaciones_clean = []

    for visualizacion in visualizaciones:
        if visualizacion['tipo'] == 'episodio':
            serie_id = visualizacion['serieId']
            if serie_id not in visualizaciones_dict or visualizacion['fechaVisualizacion'] > visualizaciones_dict[serie_id]['fechaVisualizacion']:
                visualizaciones_dict[serie_id] = visualizacion
        else:
            visualizaciones_clean.append(visualizacion)

    # Agregar las visualizaciones más recientes al resultado limpio
    visualizaciones_clean.extend(visualizaciones_dict.values())

    # Convertir las fechas de vuelta a cadenas ISO 8601
    for visualizacion in visualizaciones_clean:
        if isinstance(visualizacion['fechaVisualizacion'], datetime):
            visualizacion['fechaVisualizacion'] = visualizacion['fechaVisualizacion'].isoformat()
    # Reordenamos la lista por fecha de visualización
    visualizaciones_clean = sorted(visualizaciones_clean, key=lambda x: x['fechaVisualizacion'], reverse=True)

    return visualizaciones_clean


def randomizarLista(lista):
    return random.sample(lista, len(lista))
