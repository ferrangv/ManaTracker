from flask import render_template, request, redirect, url_for, session, abort, flash
from models import db
from models.game import Game
from . import games_bp

@games_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    search = request.args.get('search')  # Obtener parámetro de búsqueda
    
    if search:
        # Filtras por el nombre de la partida que contenga la cadena "search"
        # Usar ilike (o like), para ignorar mayúsculas/minúsculas en PostgreSQL
        games = Game.query.filter(
            Game.user_id == user_id,
            Game.name.ilike(f'%{search}%')  # o .like(...) si tu DB no soporta ilike
        ).all()
    else:
        # Si no hay búsqueda, traes todas las partidas
        games = Game.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', games=games, search=search)


@games_bp.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        colors = ','.join(request.form.getlist('colors'))
        sr_turn1 = request.form.get('sr_turn1') == 'on'
        result = request.form['result']
        turns = int(request.form['turns']) if request.form.get('turns') else None
        turn_order = request.form['turn_order']  # Nuevo campo
        notes = request.form['notes']  # Nuevo campo
        end_condition = request.form.get('end_condition', '')

        new_game = Game(
            name=name,
            colors=colors,
            sr_turn1=sr_turn1,
            result=result,
            turns=turns,
            turn_order=turn_order,
            notes=notes,
            end_condition=end_condition,
            user_id=session['user_id']
        )
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('games.dashboard'))

    return render_template('new_game.html')


@games_bp.route('/detail/<int:game_id>', methods=['GET'])
def game_detail(game_id):
    game = Game.query.get(game_id)
    if not game:
        abort(404)  # Si la partida no existe, retorna un error 404
    return render_template('game_detail.html', game=game)


@games_bp.route('/delete/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    game = Game.query.get_or_404(game_id)
    if game.user_id != session['user_id']:
        flash("You are not authorized to delete this game.")
        return redirect(url_for('games.dashboard'))

    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully.")
    return redirect(url_for('games.dashboard'))


@games_bp.route('/edit/<int:game_id>', methods=['POST'])
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)

    # Actualizar los campos del juego
    game.name = request.form['name']
    game.colors = request.form['colors']
    game.result = request.form['result']
    game.turns = request.form.get('turns', type=int)
    game.turn_order = request.form['turn_order']
    game.end_condition = request.form['end_condition']
    game.sr_turn1 = 'sr_turn1' in request.form
    game.notes = request.form['notes']

    db.session.commit()
    flash('Game updated successfully!', 'success')
    return redirect(url_for('games.game_detail', game_id=game.id))

