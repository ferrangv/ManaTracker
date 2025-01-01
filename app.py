from flask import Flask, render_template
from flask_migrate import Migrate
import os

from models import db
from routes.auth import auth_bp  # Asegúrate de importar el blueprint de auth
from routes.games import games_bp  # Otro blueprint de ejemplo
from flask_migrate import upgrade


app = Flask(__name__)

@app.before_first_request
def apply_migrations():
    upgrade()

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '644323233'

# Inicializar base de datos y migración
db.init_app(app)
migrate = Migrate(app, db)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(games_bp, url_prefix='/games')

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

