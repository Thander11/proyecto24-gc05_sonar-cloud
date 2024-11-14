# StreamEx

StreamEx es una aplicación desarrollada para la transmisión de contenido multimedia por streaming. La aplicación se basa en el uso de tres microservicios, cada uno encargado de una funcionalidad específica:

1. **Microservicio de Usuarios**: Desarrollado en Django, este microservicio gestiona la autenticación y autorización de los usuarios, así como el manejo de perfiles y preferencias.

2. **Microservicio de Contenidos**: Desarrollado en Flask, este microservicio se encarga de la gestión y distribución del contenido multimedia, incluyendo la carga, almacenamiento y transmisión de videos.

3. **Microservicio de Recomendaciones**: También desarrollado en Flask, este microservicio proporciona recomendaciones personalizadas a los usuarios basadas en sus preferencias y comportamiento de visualización.

## Características
  
- **Interfaz de Usuario**: La interfaz de usuario de StreamEx es similar a la de Netflix en algunos aspectos, proporcionando una experiencia de usuario intuitiva y atractiva.
- **Autenticación y Autorización**: Gestión segura de usuarios con autenticación y autorización.
- **Gestión de Contenidos**: Carga, almacenamiento y transmisión eficiente de contenido multimedia.
- **Recomendaciones Personalizadas**: Algoritmos avanzados para ofrecer recomendaciones de contenido basadas en el comportamiento del usuario.

## Tecnologías Utilizadas

- **Django**: Utilizado para el microservicio de usuarios.
- **Flask**: Utilizado para los microservicios de contenidos y recomendaciones.
- **HTML/CSS/JavaScript**: Utilizados para la interfaz de usuario.

## Instalación y Configuración

1. **Clonar el repositorio**:
    ```
    git clone https://github.com/UExGPSASEE/proyecto24-gc05.git
    ```

2. **Instalar dependencias**:
    - Para el microservicio de usuarios (Django):
      ```
      cd usuarios
      pip install -r requirements.txt
      ```

    - Para el microservicio de contenidos (Flask):
      ```
      cd contenidos
      pip install -r requirements.txt
      ```

    - Para el microservicio de recomendaciones (Flask):
      ```
      cd recomendaciones
      pip install -r requirements.txt
      ```

3. **Configurar las bases de datos y variables de entorno** según las instrucciones específicas de cada microservicio.

4. **Ejecutar los microservicios**:
    - Microservicio de usuarios:
      ```
      cd USERS_API
      python manage.py runserver
      ```

    - Microservicio de contenidos:
      ```
      cd CONTENT_API
      flask run
      ```

    - Microservicio de recomendaciones:
      ```
      cd RECOMENDACIONES_API
      flask run
      ```

    - Alternativamente, puedes ejecutar todos los microservicios con un solo comando:
      ```
      python ./runAll.py
      ```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.


----

<br>

<br>
<br>

----

# Descripción General del proyecto y sus componentes
## Estructura del Proyecto

### API de Contenidos (Flask)
```plaintext

API_Contenidos_Flask/
├── app/
│   ├── __init__.py
│   ├── models.py 
│   ├── routes.py
│   └── templates/
│       └── Database
├── config.py
├── Guia de POSTS.md
└── run.py
```
### API de Recomendaciones (Flask) 
```plaintext
RECOMENDACIONES_API/
├── config/
│   ├── database.py
│   └── database
├── routes/
│   ├── __init__.py
│   ├── favoritos.py
│   ├── tendencias.py
│   └── visualizaciones.py
├── recomendaciones.yaml
└── run.py
```
### API de Usuarios (Django)
```plaintext
USERS_API/
├── api_usuarios/
│   ├── api_usuarios/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── usuarios/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── testAPI.py
├── backups/
│   └── ... (archivos de respaldo)
└── usuarios.yaml
```
### API Web (Flask)
```plaintext
WEB/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── ... (otras rutas)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── ... (otros servicios)
│   ├── static/
│   │   ├── css/
│   │   │   └── inicio.css
│   │   └── ... (otros archivos estáticos)
│   ├── templates/
│   │   ├── editar_personas.html
│   │   ├── modificar_serie.html
│   │   └── ... (otras plantillas HTML)
│   └── ... (otros archivos)
├── config.py
└── run.py
```

### Descripción General de la API de Contenidos

Esta API de contenidos está diseñada para gestionar una plataforma de streaming. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre diferentes tipos de contenido, como películas, series, temporadas y episodios. Además, gestiona información relacionada con personas (actores), personajes y géneros.

### Funcionalidades Principales

1. **Gestión de Películas**:
   - **Creación**: Permite agregar nuevas películas a la base de datos.
   - **Lectura**: Permite obtener información detallada de todas las películas o de una película específica.
   - **Actualización**: Permite modificar la información de una película existente, incluyendo su título, duración, sinopsis, lanzamiento, géneros y elenco.
   - **Eliminación**: Permite eliminar una película de la base de datos.

2. **Gestión de Series**:
   - **Creación**: Permite agregar nuevas series, incluyendo su primera temporada y episodio.
   - **Lectura**: Permite obtener información detallada de todas las series o de una serie específica.
   - **Actualización**: Permite modificar la información de una serie existente, incluyendo su título, sinopsis, lanzamiento, géneros y elenco.
   - **Eliminación**: Permite eliminar una serie de la base de datos.

3. **Gestión de Temporadas y Episodios**:
   - **Temporadas**:
     - **Creación**: Permite agregar nuevas temporadas a una serie existente.
     - **Lectura**: Permite obtener información detallada de todas las temporadas de una serie o de una temporada específica.
     - **Actualización**: Permite modificar la información de una temporada existente.
     - **Eliminación**: Permite eliminar una temporada de la base de datos.
   - **Episodios**:
     - **Creación**: Permite agregar nuevos episodios a una temporada existente.
     - **Lectura**: Permite obtener información detallada de un episodio específico.
     - **Actualización**: Permite modificar la información de un episodio existente.
     - **Eliminación**: Permite eliminar un episodio de la base de datos.

4. **Gestión de Personas y Personajes**:
   - **Personas**:
     - **Creación**: Permite agregar nuevas personas (actores) a la base de datos.
     - **Lectura**: Permite obtener información detallada de todas las personas o de una persona específica.
     - **Actualización**: Permite modificar la información de una persona existente.
     - **Eliminación**: Permite eliminar una persona de la base de datos.
   - **Personajes**:
     - **Creación**: Permite agregar nuevos personajes a la base de datos.
     - **Lectura**: Permite obtener información detallada de todos los personajes o de un personaje específico.
     - **Actualización**: Permite modificar la información de un personaje existente.
     - **Eliminación**: Permite eliminar un personaje de la base de datos.

5. **Gestión de Géneros**:
   - **Creación**: Permite agregar nuevos géneros a la base de datos.
   - **Lectura**: Permite obtener información detallada de todos los géneros o de un género específico.
   - **Actualización**: Permite modificar la información de un género existente.
   - **Eliminación**: Permite eliminar un género de la base de datos.

### Características Adicionales

- **Relaciones Complejas**: La API maneja relaciones complejas entre los diferentes modelos, como la relación muchos a muchos entre películas y géneros, y entre episodios y personajes. Esto permite una gestión eficiente y flexible de los datos.
- **Serialización**: Los modelos tienen métodos `to_dict` para convertir las instancias en diccionarios JSON serializables, facilitando la comunicación entre el cliente y el servidor.
- **Búsqueda y Filtrado**: La API incluye funcionalidades para buscar y filtrar contenido basado en diferentes criterios, como texto de búsqueda. Esto permite a los usuarios encontrar rápidamente el contenido que están buscando.
- **Blueprints en Flask**: La API utiliza el patrón Blueprint de Flask para organizar las rutas de la aplicación en módulos separados. Esto facilita la gestión y escalabilidad del proyecto.
- **Documentación y Especificaciones**: La API está documentada utilizando archivos YAML y Markdown, proporcionando una referencia clara y detallada de los endpoints disponibles y sus funcionalidades.

### Ejemplo de Uso

#### Actualización del Elenco de una Película

La API permite actualizar el elenco de una película específica. Esto se realiza mediante una solicitud `PUT` a la ruta `/peliculas/<int:pelicula_id>/cast`. En esta operación, se obtiene la película por su ID, se limpia el elenco actual y se agrega el nuevo elenco proporcionado en el cuerpo de la solicitud.

```python
@routes_bp.route('/peliculas/<int:pelicula_id>/cast', methods=['PUT'])
def update_cast_pelicula(pelicula_id):
    data = request.get_json()
    pelicula = Pelicula.query.get_or_404(pelicula_id)
    
    # Limpiar el cast actual
    pelicula.cast = []
    
    # Agregar el nuevo cast
    for personaje_id in data['cast']:
        personaje = Personaje.query.get_or_404(personaje_id)
        pelicula.cast.append(personaje)
    
    db.session.commit()
    
    return jsonify({'message': 'Cast actualizado exitosamente'}), 200
```

Este ejemplo muestra cómo se maneja la actualización de relaciones muchos a muchos entre `Pelicula` y `Personaje` utilizando SQLAlchemy.



### Descripción General de la API de Recomendaciones

Esta API de recomendaciones está diseñada para gestionar las visualizaciones y favoritos de los usuarios en una plataforma de streaming. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre las visualizaciones y favoritos, así como obtener tendencias y recomendaciones personalizadas para los usuarios.

### Funcionalidades Principales

1. **Gestión de Visualizaciones**:
   - **Creación**: Permite registrar nuevas visualizaciones de contenido por parte de los usuarios.
   - **Lectura**: Permite obtener el historial de visualizaciones de un usuario específico o una visualización específica.
   - **Actualización**: Permite actualizar la información de una visualización existente, como la fecha de visualización y la duración vista.
   - **Eliminación**: No se especifica eliminación directa de visualizaciones, pero se pueden actualizar los registros existentes.

2. **Gestión de Favoritos**:
   - **Creación**: Permite agregar contenido a la lista de favoritos de un usuario.
   - **Lectura**: Permite obtener la lista de favoritos de un usuario específico.
   - **Eliminación**: Permite eliminar contenido de la lista de favoritos de un usuario.

3. **Gestión de Tendencias**:
   - **Lectura**: Permite obtener las tendencias actuales en la plataforma, basadas en la popularidad del contenido.

4. **Gestión de Recomendaciones**:
   - **Lectura**: Permite obtener recomendaciones personalizadas para un usuario, basadas en sus favoritos y visualizaciones previas.

### Características Adicionales

- **Relaciones Complejas**: La API maneja relaciones complejas entre los diferentes modelos, como la relación entre usuarios y sus visualizaciones o favoritos. Esto permite una gestión eficiente y flexible de los datos.
- **Serialización**: Los modelos tienen métodos para convertir las instancias en diccionarios JSON serializables, facilitando la comunicación entre el cliente y el servidor.
- **Búsqueda y Filtrado**: La API incluye funcionalidades para buscar y filtrar contenido basado en diferentes criterios, como texto de búsqueda. Esto permite a los usuarios encontrar rápidamente el contenido que están buscando.
- **Blueprints en Flask**: La API utiliza el patrón Blueprint de Flask para organizar las rutas de la aplicación en módulos separados. Esto facilita la gestión y escalabilidad del proyecto.
- **Documentación y Especificaciones**: La API está documentada utilizando archivos YAML y Markdown, proporcionando una referencia clara y detallada de los endpoints disponibles y sus funcionalidades.

### Ejemplo de Uso

#### Registro de una Visualización

La API permite registrar una nueva visualización de contenido por parte de un usuario. Esto se realiza mediante una solicitud `POST` a la ruta `/visualizaciones`. En esta operación, se valida la presencia de los campos requeridos y se registra la visualización en la base de datos.

```python
@visualizaciones_bp.route('/visualizaciones', methods=['POST'])
def registrar_visualizacion():
    try:
        data = request.get_json()
        
        # Validación de campos requeridos
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
```

Este ejemplo muestra cómo se maneja la creación de una nueva visualización, incluyendo la validación de los datos de entrada y la actualización de las tendencias.





### Descripción General de la API de Usuarios

Esta API de usuarios está diseñada para gestionar usuarios, perfiles y métodos de pago en una plataforma de streaming. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre usuarios, perfiles y métodos de pago, así como realizar búsquedas y obtener información detallada de cada entidad.

### Funcionalidades Principales

1. **Gestión de Usuarios**:
   - **Creación**: Permite agregar nuevos usuarios a la base de datos.
   - **Lectura**: Permite obtener información detallada de todos los usuarios o de un usuario específico.
   - **Actualización**: Permite modificar la información de un usuario existente, incluyendo su correo electrónico, contraseña y nombre de usuario.
   - **Eliminación**: Permite eliminar un usuario de la base de datos.
   - **Búsqueda**: Permite buscar usuarios por correo electrónico o nombre de usuario.

2. **Gestión de Perfiles**:
   - **Creación**: Permite agregar nuevos perfiles asociados a un usuario.
   - **Lectura**: Permite obtener información detallada de todos los perfiles o de un perfil específico.
   - **Actualización**: Permite modificar la información de un perfil existente.
   - **Eliminación**: Permite eliminar un perfil de la base de datos.
   - **Perfiles por Usuario**: Permite obtener todos los perfiles asociados a un usuario específico.

3. **Gestión de Métodos de Pago**:
   - **Creación**: Permite agregar nuevos métodos de pago asociados a un usuario.
   - **Lectura**: Permite obtener información detallada de todos los métodos de pago o de un método de pago específico.
   - **Actualización**: Permite modificar la información de un método de pago existente.
   - **Eliminación**: Permite eliminar un método de pago de la base de datos.
   - **Pagos por Usuario**: Permite obtener todos los métodos de pago asociados a un usuario específico.

### Características Adicionales

- **Relaciones Complejas**: La API maneja relaciones complejas entre los diferentes modelos, como la relación entre usuarios y sus perfiles o métodos de pago. Esto permite una gestión eficiente y flexible de los datos.
- **Serialización**: Los modelos tienen serializers para convertir las instancias en diccionarios JSON serializables, facilitando la comunicación entre el cliente y el servidor.
- **Búsqueda y Filtrado**: La API incluye funcionalidades para buscar y filtrar usuarios basado en diferentes criterios, como texto de búsqueda. Esto permite a los usuarios encontrar rápidamente el contenido que están buscando.
- **ViewSets y Routers en Django REST Framework**: La API utiliza ViewSets y Routers de Django REST Framework para organizar las rutas de la aplicación en módulos separados. Esto facilita la gestión y escalabilidad del proyecto.
- **Documentación y Especificaciones**: La API está documentada utilizando archivos YAML y Markdown, proporcionando una referencia clara y detallada de los endpoints disponibles y sus funcionalidades.

### Ejemplo de Uso

#### Creación de un Nuevo Usuario

La API permite crear un nuevo usuario en la plataforma. Esto se realiza mediante una solicitud `POST` a la ruta `/usuarios`. En esta operación, se valida la presencia de los campos requeridos y se registra el usuario en la base de datos.

```python
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
```

Este ejemplo muestra cómo se maneja la creación de un nuevo usuario, incluyendo la validación de los datos de entrada y la respuesta del servidor.



### Descripción General de la API Web

La API Web es la principal interfaz de la plataforma de streaming, encargada de orquestar las llamadas a las diferentes APIs de contenidos, recomendaciones y usuarios. Esta API actúa como un intermediario, gestionando las solicitudes de los usuarios y coordinando las respuestas de las otras APIs para proporcionar una experiencia de usuario coherente y eficiente.

### Funcionalidades Principales

1. **Gestión de Contenidos**:
   - **Películas**: Permite obtener la lista de películas, detalles de una película específica, y realizar búsquedas de películas.
   - **Series**: Permite obtener la lista de series, detalles de una serie específica, y realizar búsquedas de series.
   - **Géneros**: Permite obtener la lista de géneros disponibles en la plataforma.

2. **Gestión de Usuarios**:
   - **Usuarios**: Permite crear, leer, actualizar y eliminar usuarios. También permite buscar usuarios por correo electrónico o nombre de usuario.
   - **Perfiles**: Permite gestionar los perfiles asociados a un usuario, incluyendo la creación, lectura, actualización y eliminación de perfiles.
   - **Métodos de Pago**: Permite gestionar los métodos de pago asociados a un usuario, incluyendo la creación, lectura, actualización y eliminación de métodos de pago.

3. **Gestión de Visualizaciones y Favoritos**:
   - **Visualizaciones**: Permite registrar nuevas visualizaciones, obtener el historial de visualizaciones de un usuario y obtener detalles de una visualización específica.
   - **Favoritos**: Permite agregar contenido a la lista de favoritos de un usuario, obtener la lista de favoritos de un usuario y eliminar contenido de la lista de favoritos.

4. **Tendencias y Recomendaciones**:
   - **Tendencias**: Permite obtener las tendencias actuales en la plataforma, basadas en la popularidad del contenido.
   - **Recomendaciones**: Permite obtener recomendaciones personalizadas para un usuario, basadas en sus favoritos y visualizaciones previas.

### Características Adicionales

- **Orquestación de APIs**: La API Web actúa como un intermediario, coordinando las llamadas a las diferentes APIs de contenidos, recomendaciones y usuarios para proporcionar una experiencia de usuario coherente y eficiente.
- **Serialización**: Los datos obtenidos de las diferentes APIs se serializan en formatos JSON para facilitar la comunicación entre el cliente y el servidor.
- **Búsqueda y Filtrado**: La API incluye funcionalidades para buscar y filtrar contenido basado en diferentes criterios, como texto de búsqueda. Esto permite a los usuarios encontrar rápidamente el contenido que están buscando.
- **Gestión de Sesiones y Autenticación**: La API gestiona las sesiones de los usuarios y proporciona mecanismos de autenticación para asegurar que solo los usuarios autorizados puedan acceder a ciertas funcionalidades.
- **Documentación y Especificaciones**: La API está documentada utilizando archivos YAML y Markdown, proporcionando una referencia clara y detallada de los endpoints disponibles y sus funcionalidades.

### Ejemplo de Uso

#### Visualización de Videos

La API permite a los usuarios visualizar videos en la plataforma. Esto se realiza mediante una solicitud a la ruta `/display_videos`, que coordina las llamadas a las APIs de tendencias, favoritos, visualizaciones y recomendaciones para obtener la información necesaria.

```python
@auth_bp.route('/display_videos')
def display_videos():
    def get_visualizaciones(perfil_id):
        # Lógica para obtener visualizaciones
    def get_recomendaciones(perfil_id):
        # Lógica para obtener recomendaciones

    # Crear hilos para llamadas concurrentes
    t1 = threading.Thread(target=get_tendencias)
    t2 = threading.Thread(target=get_favoritos, args=(perfil_id,))
    t3 = threading.Thread(target=get_visualizaciones, args=(perfil_id,))
    t4 = threading.Thread(target=get_recomendaciones, args=(perfil_id,))

    # Iniciar hilos
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # Esperar a que todos los hilos terminen
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # Obtener resultados
    tendencias = results['tendencias']
    favoritos = results['favoritos']
    visualizaciones = results['visualizaciones']
    recomendaciones = results['recomendaciones']

    # Renderizar la página con los resultados obtenidos
    return render_template('display_videos.html', tendencias=tendencias, favoritos=favoritos, visualizaciones=visualizaciones, recomendaciones=recomendaciones)
```

Este ejemplo muestra cómo la API Web coordina las llamadas a las diferentes APIs para obtener la información necesaria y renderizar la página de visualización de videos.

### Conclusión


En conjunto, las APIs de Contenidos, Recomendaciones, Usuarios y Web proporcionan una solución integral para la gestión de una plataforma de streaming. Cada API desempeña un papel crucial en la funcionalidad general del sistema, permitiendo una gestión eficiente y flexible de los datos, así como una experiencia de usuario coherente y personalizada.

1. **API de Contenidos**: Facilita la gestión de películas, series, temporadas, episodios, personas, personajes y géneros. Permite realizar operaciones CRUD y maneja relaciones complejas entre los diferentes modelos, asegurando una administración eficiente del contenido disponible en la plataforma.

2. **API de Recomendaciones**: Gestiona las visualizaciones y favoritos de los usuarios, proporcionando tendencias y recomendaciones personalizadas. Utiliza relaciones complejas entre los modelos para ofrecer una experiencia de usuario adaptada a los intereses individuales.

3. **API de Usuarios**: Administra usuarios, perfiles y métodos de pago. Permite realizar operaciones CRUD y buscar usuarios por diferentes criterios, facilitando la gestión de la base de usuarios y sus preferencias de pago.

4. **API Web**: Actúa como la principal interfaz de la plataforma, orquestando las llamadas a las diferentes APIs de contenidos, recomendaciones y usuarios. Coordina las solicitudes de los usuarios y proporciona una experiencia de usuario coherente y eficiente mediante la gestión de sesiones y autenticación.

### Características Adicionales

- **Relaciones Complejas**: Todas las APIs manejan relaciones complejas entre los diferentes modelos, permitiendo una gestión eficiente y flexible de los datos.
- **Serialización**: Los modelos tienen métodos para convertir las instancias en diccionarios JSON serializables, facilitando la comunicación entre el cliente y el servidor.
- **Búsqueda y Filtrado**: Las APIs incluyen funcionalidades para buscar y filtrar contenido basado en diferentes criterios, permitiendo a los usuarios encontrar rápidamente lo que están buscando.
- **Blueprints y ViewSets**: La organización mediante Blueprints en Flask y ViewSets en Django REST Framework facilita la gestión y escalabilidad del proyecto.
- **Documentación y Especificaciones**: Las APIs están documentadas utilizando archivos YAML y Markdown, proporcionando una referencia clara y detallada de los endpoints disponibles y sus funcionalidades.


