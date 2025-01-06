# routes/user.py
from flask import Blueprint, render_template
from flask import session
from models.game import Game
from collections import Counter

user_bp = Blueprint('user', __name__)

@user_bp.route('/statistics')
def statistics():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Obtener todas las partidas del usuario
    games = Game.query.filter_by(user_id=user_id).all()

    # Calcular total de partidas
    total_games = len(games)

    # Calcular total de victorias
    total_wins = sum(1 for game in games if game.result == '1st')

    # Calcular win rate
    win_rate = (total_wins / total_games * 100) if total_games > 0 else 0

    # Calcular promedio de posiciones
    placements = []
    for game in games:
        try:
            placement = int(game.result[0])  # Extraer el número de posición (1st -> 1)
            placements.append(placement)
        except ValueError:
            continue
    avg_placement = sum(placements) / len(placements) if placements else None

    # Calcular el deck más jugado
    deck_counter = {}
    for game in games:
        if game.name:
            deck_counter[game.name] = deck_counter.get(game.name, 0) + 1
    most_played_deck = max(deck_counter, key=deck_counter.get) if deck_counter else 'N/A'

    # Calcular promedio de turnos por partida
    turn_counts = [game.turns for game in games if game.turns is not None]
    total_turns = sum(turn_counts)
    avg_turns = total_turns / len(turn_counts) if turn_counts else 'N/A'


    # Calcular la condición de victoria más común en todas las partidas
    wincon_counter_all = {}
    for game in games:
        if game.end_condition:
            wincon_counter_all[game.end_condition] = wincon_counter_all.get(game.end_condition, 0) + 1
    most_common_wincon_all = max(wincon_counter_all, key=wincon_counter_all.get) if wincon_counter_all else 'N/A'

    # Calcular la condición de victoria más común en las partidas ganadas
    wincon_counter_wins = {}
    for game in games:
        if game.result == '1st' and game.end_condition:
            wincon_counter_wins[game.end_condition] = wincon_counter_wins.get(game.end_condition, 0) + 1
    most_common_wincon_user = max(wincon_counter_wins, key=wincon_counter_wins.get) if wincon_counter_wins else 'N/A'

    # Calcular la cantidad de partidas jugadas por cada deck
    deck_counts = Counter(game.name for game in games)

    # Separar nombres de decks y sus conteos para Chart.js
    deck_names = list(deck_counts.keys())
    deck_played_counts = list(deck_counts.values())

    # Calcular la distribución de las condiciones de fin
    end_conditions = [game.end_condition for game in games if game.end_condition]
    condition_counts = {}
    for condition in end_conditions:
        condition_counts[condition] = condition_counts.get(condition, 0) + 1

    return render_template(
        'statistics.html',
        total_games=total_games,
        total_wins=total_wins,
        win_rate=round(win_rate, 2),
        avg_placement=round(avg_placement, 2) if avg_placement else 'N/A',
        most_played_deck=most_played_deck,
        avg_turns=round(avg_turns, 2) if isinstance(avg_turns, (int, float)) else avg_turns,
        most_common_wincon_all=most_common_wincon_all,
        most_common_wincon_user=most_common_wincon_user,
        deck_names=deck_names,
        deck_played_counts=deck_played_counts,
        condition_labels=list(condition_counts.keys()),
        condition_values=list(condition_counts.values())
    )


@user_bp.route('/achievements')
def achievements():
    return render_template('achievements.html')

@user_bp.route('/leaderboards')
def leaderboards():
    return render_template('leaderboards.html')

@user_bp.route('/profile')
def profile():
    return render_template('profile.html')