# app/__init__.py
from flask import Flask, render_template, request, redirect, url_for, session
from app.config import Config
from app.services.user_service import UserService  # Importar UserService
from app.routes.auth import auth_bp  # Importar el blueprint aquí


def create_app():
    app = Flask(__name__, 
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object(Config)
    app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta segura

    @app.route('/')
    def index():
        return render_template('Index.html')

    @app.route('/verificar_correo', methods=['POST'])
    def verificar_correo_main():
        email = request.form.get('email')
        try:
            user = UserService.buscar_usuario_por_correo(email)
            if user:
                return redirect(url_for('login', email=email))
            else:
                return redirect(url_for('auth.register', email=email))
        except Exception as e:
            return str(e)

    # Importar y registrar los blueprints después de definir la instancia de Flask
    app.register_blueprint(auth_bp)

    @app.route('/login')
    def login():
        email = request.args.get('email', '')
        return render_template('login.html', email=email)

    @app.route('/register')
    def register():
        email = request.args.get('email', '')
        return render_template('Registrarse.html', email=email)

    @app.route('/verificar_login', methods=['POST'])
    def verificar_login():
        email = request.form.get('email')
        password = request.form.get('password')
        if UserService.verify_login(email, password):
            return redirect(url_for('perfiles'))
        return redirect(url_for('login'))

    @app.route('/perfiles')
    def perfiles():
        return render_template('Perfiles.html')

    return app