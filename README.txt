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