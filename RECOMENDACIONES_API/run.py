from flask import Flask
from waitress import serve
from config.database import init_app
from routes import favoritos_bp, tendencias_bp, visualizaciones_bp

def create_app():
    app = Flask(__name__)
    
    # Inicializar la base de datos
    init_app(app)
    
    # Registrar los blueprints
    app.register_blueprint(favoritos_bp)
    app.register_blueprint(tendencias_bp)
    app.register_blueprint(visualizaciones_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5010)