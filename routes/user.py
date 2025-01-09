# routes/user.py
from flask import Blueprint, render_template
from flask import session
from models.game import Game
from collections import Counter, defaultdict

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

    # Contar combinaciones de colores
    color_combinations = [game.colors for game in games if game.colors]
    color_counts = Counter(color_combinations)

    # Convertir a formato legible (p.ej., "Mono Red", "Rakdos")
    color_names = {
    # Mono Colors
    "white": "Mono White",
    "blue": "Mono Blue",
    "black": "Mono Black",
    "red": "Mono Red",
    "green": "Mono Green",

    # Two-Color Combinations (Guilds)
    "white,blue": "Azorius",
    "white,black": "Orzhov",
    "white,red": "Boros",
    "white,green": "Selesnya",
    "blue,black": "Dimir",
    "blue,red": "Izzet",
    "blue,green": "Simic",
    "black,red": "Rakdos",
    "black,green": "Golgari",
    "red,green": "Gruul",

    # Three-Color Combinations (Shards and Wedges)
    "white,blue,black": "Esper",
    "white,blue,red": "Jeskai",
    "white,blue,green": "Bant",
    "white,black,red": "Mardu",
    "white,black,green": "Abzan",
    "blue,black,red": "Grixis",
    "blue,black,green": "Sultai",
    "blue,red,green": "Temur",
    "black,red,green": "Jund",
    "red,green,white": "Naya",

    # Four-Color Combinations (Nephilim)
    "white,blue,black,red": "Non-Green",
    "white,blue,black,green": "Non-Red",
    "white,blue,red,green": "Non-Black",
    "white,black,red,green": "Non-Blue",
    "blue,black,red,green": "Non-White",

    # Five-Color
    "white,blue,black,red,green": "Five-Color",

    # Colorless
    "": "Colorless",
}

    color_labels = [color_names.get(combo, combo) for combo in color_counts.keys()]
    color_played_counts = list(color_counts.values())

    # Contar la cantidad de juegos para cada color
    color_count = Counter()
    for game in games:
        if game.colors:
            colors = game.colors.split(',')
            color_count.update(colors)

    # Datos para el gráfico
    color_labels_pie = ['White', 'Blue', 'Black', 'Red', 'Green', 'Colorless']
    color_counts_pie = [
        color_count.get('white', 0),
        color_count.get('blue', 0),
        color_count.get('black', 0),
        color_count.get('red', 0),
        color_count.get('green', 0),
        color_count.get('colorless', 0)
    ]

    # Calcular la distribución de las condiciones de fin
    end_conditions = [game.end_condition for game in games if game.end_condition]
    condition_counts = {}
    for condition in end_conditions:
        condition_counts[condition] = condition_counts.get(condition, 0) + 1

    # Contar posiciones
    position_counts = Counter(game.result for game in games if game.result)

    # Preparar datos para la tabla
    positions = ['1st', '2nd', '3rd', '4th', '5th+']
    position_data = []
    for position in positions:
        count = position_counts.get(position, 0)
        percentage = (count / total_games * 100) if total_games > 0 else 0
        position_data.append({
            'position': position,
            'percentage': f"{percentage:.2f}%",
            'count': count
        })

    # Datos para el gráfico de posiciones
    position_labels = positions
    position_values = [position_counts.get(pos, 0) for pos in positions]

    # Datos para la tabla de rendimiento por Turn Order
    turn_order_data = defaultdict(lambda: {'wins': 0, 'games': 0, 'placement_sum': 0})

    for game in games:
        turn_order = game.turn_order
        if turn_order and turn_order[:-2].isdigit():  # Extrae el número antes de 'st', 'nd', etc.
            numeric_turn_order = int(turn_order[:-2])  # Convierte a número (ej.: '1st' -> 1)
            turn_order_data[numeric_turn_order]['games'] += 1
            turn_order_data[numeric_turn_order]['placement_sum'] += int(game.result[0]) if game.result and game.result[0].isdigit() else 0
            if game.result == '1st':
                turn_order_data[numeric_turn_order]['wins'] += 1

    turn_order_table = []
    for turn_order, data in turn_order_data.items():
        games_count = data['games']
        wins = data['wins']
        placement_sum = data['placement_sum']
        win_rate = round((wins / games_count) * 100, 2) if games_count > 0 else 0
        avg_placement = round((placement_sum / games_count), 2) if games_count > 0 else 0
        turn_order_table.append({
            'turn_order': f"{turn_order}st" if turn_order == 1 else f"{turn_order}nd" if turn_order == 2 else f"{turn_order}rd" if turn_order == 3 else f"{turn_order}th",
            'win_rate': f"{win_rate}%",
            'games': games_count,
            'avg_placement': avg_placement
        })

    # Ordenar turn_order_table por turn_order numérico
    turn_order_table = sorted(
        turn_order_table,
        key=lambda x: int(x['turn_order'][:-2])  # Extraer el número para ordenar
    )

     # Contar las wincons y las victorias
    wincon_data = defaultdict(lambda: {'total': 0, 'wins': 0})

    for game in games:
        if game.end_condition:  # Solo considerar partidas con una condición de victoria registrada
            wincon_data[game.end_condition]['total'] += 1
            if game.result == '1st':  # Verificar si el usuario ganó con esta wincon
                wincon_data[game.end_condition]['wins'] += 1

    # Formatear los datos para la tabla
    wincon_table = []
    for wincon, counts in wincon_data.items():
        wincon_table.append({
            'wincon': wincon,
            'total': counts['total'],
            'wins': counts['wins']
        })

    # Agrupar partidas por deck
    decks_data = defaultdict(lambda: {
        'games': 0,
        'placements': [],
        'wins': 0,
        'top2': 0,
        'top3': 0,
        'top4': 0,
        'top5plus': 0,
        'turns': [],
        'wincons': defaultdict(int)
    })

    for game in games:
        if game.name:  # Asegurar que el deck tiene un nombre
            deck_data = decks_data[game.name]
            deck_data['games'] += 1
            if game.result:
                placement = int(game.result[0]) if game.result[0].isdigit() else None
                if placement:
                    deck_data['placements'].append(placement)
                    if placement == 1:
                        deck_data['wins'] += 1
                    elif placement == 2:
                        deck_data['top2'] += 1
                    elif placement == 3:
                        deck_data['top3'] += 1
                    elif placement == 4:
                        deck_data['top4'] += 1
                    else:
                        deck_data['top5plus'] += 1
            if game.turns is not None:
                deck_data['turns'].append(game.turns)
            if game.end_condition:
                deck_data['wincons'][game.end_condition] += 1

    # Construir los datos para la tabla
    decks_table = []
    for deck, data in decks_data.items():
        games_count = data['games']
        avg_placement = (
            sum(data['placements']) / len(data['placements']) if data['placements'] else 'N/A'
        )
        winrate = (data['wins'] / games_count * 100) if games_count > 0 else 0
        top2_rate = (data['top2'] / games_count * 100) if games_count > 0 else 0
        top3_rate = (data['top3'] / games_count * 100) if games_count > 0 else 0
        top4_rate = (data['top4'] / games_count * 100) if games_count > 0 else 0
        top5plus_rate = (data['top5plus'] / games_count * 100) if games_count > 0 else 0
        avg_turns = (
            sum(data['turns']) / len(data['turns']) if data['turns'] else 'N/A'
        )
        most_common_wincon = max(data['wincons'], key=data['wincons'].get, default='N/A')

        decks_table.append({
            'deck': deck,
            'games': games_count,
            'avg_placement': avg_placement,
            'winrate': f"{winrate:.2f}%",
            'top2': f"{top2_rate:.2f}%",
            'top3': f"{top3_rate:.2f}%",
            'top4': f"{top4_rate:.2f}%",
            'top5plus': f"{top5plus_rate:.2f}%",
            'avg_turns': avg_turns,
            'wincon': most_common_wincon
        })

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
        condition_values=list(condition_counts.values()),
        color_labels=color_labels,
        color_played_counts=color_played_counts,
        color_labels_pie=color_labels_pie,
        color_counts_pie=color_counts_pie,
        position_data=position_data,
        position_labels=position_labels,
        position_values=position_values,
        turn_order_table=turn_order_table,
        decks_table=decks_table,
        wincon_table=wincon_table,
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