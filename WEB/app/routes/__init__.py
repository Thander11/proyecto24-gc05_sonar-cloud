from flask import Blueprint
from app.routes.auth import auth_bp

# Lista de todos los blueprints disponibles
blueprints = [auth_bp]

def init_app(app):
    """Registra todos los blueprints en la aplicación"""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)