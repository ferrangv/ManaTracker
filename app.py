from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
import os

from models import db
from routes.auth import auth_bp  # Importar el blueprint de auth
from routes.games import games_bp  # Importar el blueprint de games

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '644323233'

# Inicializar base de datos y migración
db.init_app(app)
migrate = Migrate(app, db)

# Ejecutar migraciones al iniciar la aplicación
with app.app_context():
    upgrade()

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(games_bp, url_prefix='/games')

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=5000)
