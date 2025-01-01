from datetime import datetime
from flask import session
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os


app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '644323233'  
db = SQLAlchemy(app)

# Configuración de Flask-Migrate
migrate = Migrate(app, db)

# Modelo de usuario
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Modelo de games
class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    colors = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    sr_turn1 = db.Column(db.Boolean)
    result = db.Column(db.String(50))
    turns = db.Column(db.Integer)
    end_condition = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='games')

User.games = db.relationship('Game', back_populates='user')

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Username or email already exists", 400

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Variable para almacenar el mensaje de error
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar el usuario por correo
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Almacenar información de sesión
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    # Filtrar juegos por el usuario autenticado
    games = Game.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', games=games)




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        colors = ','.join(request.form.getlist('colors'))  # Recibe los colores seleccionados
        sr_turn1 = request.form.get('sr_turn1') == 'on'  # Checkbox
        result = request.form['result']
        turns = int(request.form['turns']) if request.form.get('turns') else None
        end_condition = request.form.get('end_condition', '')  # Usa .get() para evitar errores

        # Crear una nueva partida
        new_game = Game(
            name=name,
            colors=colors,
            sr_turn1=sr_turn1,
            result=result,
            turns=turns,
            end_condition=end_condition,
            user_id=session['user_id']
        )
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('new_game.html')




if __name__ == '__main__':
    app.run(debug=True)




