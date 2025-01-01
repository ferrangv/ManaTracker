from flask import render_template, request, redirect, url_for, session
from models import db
from models.game import Game
from . import games_bp

@games_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    games = Game.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', games=games)


@games_bp.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        colors = ','.join(request.form.getlist('colors'))
        sr_turn1 = request.form.get('sr_turn1') == 'on'
        result = request.form['result']
        turns = int(request.form.get('turns', 0)) if request.form.get('turns') else None
        end_condition = request.form.get('end_condition', '')

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

        return redirect(url_for('games.dashboard'))

    return render_template('new_game.html')
