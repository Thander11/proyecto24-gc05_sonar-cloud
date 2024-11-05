from flask import Blueprint, render_template, request, redirect, url_for, session
import threading
import time  # Add at top of file

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
        'recomendaciones': None
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
    # Create threads
    t1 = threading.Thread(target=get_tendencias)
    t2 = threading.Thread(target=get_favoritos, args=(perfil_id,))
    t3 = threading.Thread(target=get_visualizaciones, args=(perfil_id,))
    t4 = threading.Thread(target=get_recomendaciones, args=(perfil_id,))

    # Start threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # Wait for all threads to complete
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # Get results
    tendencias = results['tendencias']
    favoritos = results['favoritos']
    visualizaciones = results['visualizaciones']
    recomendaciones = results['recomendaciones']

    return render_template('display_videos.html', perfil=perfil, perfiles=perfiles, 
                         tendencias=tendencias, favoritos=favoritos, visualizaciones=visualizaciones, recomendaciones=recomendaciones)


@auth_bp.route('/usuario')
def usuario():
    usuario = session.get('usuario')
    if not usuario:
        return redirect(url_for('auth.login'))
    
    pago = UserService.obtener_pago(usuario['id'])
    
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
        response = UserService.registrar_visualizacion(usuario_id, content_id, duracion, tipo)
        if response:
            # Only redirect to video player if visualization was registered successfully
            video_url = "https://www.youtube.com/embed/HwxZR0uQa0A"
            return render_template('video_player.html', video_url=video_url)
        else:
            print("Failed to register visualization, redirecting to videos")
            return redirect(url_for('auth.display_videos', id=usuario_id))

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