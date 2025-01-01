from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
games_bp = Blueprint('games', __name__)

# Importar las rutas desde los módulos
from .auth import *
from .games import *
