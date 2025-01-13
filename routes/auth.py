from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

# Inicializar el blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('signup.html')

        # Verificar si el username o email ya existe
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template('signup.html')

        # Crear nuevo usuario
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("An error occurred. Please try again.", "error")
            return render_template('signup.html')

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('games.dashboard'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
