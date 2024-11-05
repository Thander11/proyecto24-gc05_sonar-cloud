from flask import Blueprint

favoritos_bp = Blueprint('favoritos', __name__)
tendencias_bp = Blueprint('tendencias', __name__)
visualizaciones_bp = Blueprint('visualizaciones', __name__)

from . import favoritos, tendencias, visualizaciones