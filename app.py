from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import sqlite3
import base64
from src import Info, Visualization
import numpy as np
app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)
def get_db_connection():
    conn = sqlite3.connect('SoccerStatsHub.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/players', methods=['GET'])
def get_players():
    conn = get_db_connection()
    players = conn.execute('SELECT DISTINCT "Player Name" FROM player_seasons_data').fetchall()
    conn.close()
    return jsonify([player[0] for player in players])

@app.route('/api/managers', methods=['GET'])
def get_managers():
    conn = get_db_connection()
    managers = conn.execute('SELECT DISTINCT "Name" FROM manager_seasons_data').fetchall()
    conn.close()
    return jsonify([manager[0] for manager in managers])

@app.route('/api/seasons', methods=['GET'])
def get_seasons():
    player_name = request.args.get('player_name')
    conn = get_db_connection()
    seasons = conn.execute('SELECT DISTINCT Season FROM player_seasons_data WHERE "Player Name" = "' + player_name + '"').fetchall()
    conn.close()
    return jsonify([season[0] for season in seasons])

@app.route('/api/manager_seasons', methods=['GET'])
def get_manager_seasons():
    manager_name = request.args.get('manager_name')
    conn = get_db_connection()
    seasons = conn.execute('SELECT DISTINCT Season FROM manager_seasons_data WHERE "Name" = "' + manager_name + '"').fetchall()
    conn.close()
    return jsonify([season[0] for season in seasons])

@app.route('/api/competitions', methods=['GET'])
def get_competitions():
    player_name = request.args.get('player_name')
    conn = get_db_connection()
    competitions = conn.execute('SELECT DISTINCT Tournament FROM player_seasons_data WHERE "Player Name" = "' + player_name + '"').fetchall()
    conn.close()
    return jsonify([competition[0] for competition in competitions])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    stats = conn.execute('PRAGMA table_info(player_seasons_data)').fetchall()
    conn.close()
    stats = [col[1] for col in stats]
    exc = ['Player Name', 'Team', 'Tournament', 'Season', 'Unnamed: 0', 'Key Passes Per Game.1']
    stats = [thing for thing in stats if thing not in exc]
    return jsonify(stats)

@app.route('/api/manager_stats', methods=['GET'])
def get_manager_stats():
    conn = get_db_connection()
    stats = conn.execute('PRAGMA table_info(manager_seasons_data)').fetchall()
    conn.close()
    stats = [col[1] for col in stats]
    exc = ['Name', 'Season', 'Unnamed: 0']
    stats = [thing for thing in stats if thing not in exc]
    return jsonify(stats)


@app.route('/api/visualize', methods=['POST'])
def visualize():
    import matplotlib
    matplotlib.use('Agg')
    img_base64 = ""
    conn = get_db_connection()
    data = request.json['player_info']
    llm = None
    images = []
    for player in data:
        global colors, viz_options
        global player_name, player_seasons, player_competitions, player_stats
        player_name = player['name']
        player_seasons = player['seasons']
        player_competitions = player['competitions']
        player_stats = player['stats']
        viz_options = player['viz']
        colors = viz_options['colors']
        info = Info.Info(player_name, player_seasons, player_competitions, player_stats)
        result = info.get_player_data(conn)
        if 'Apps' in result.columns:
            result['Apps'] = result['Apps'].str.split('(').str[0].str.strip()
        result = result.applymap(lambda x: '0' if x == '-' else x)
        if len(result.index) == 0:
            error_image = np.zeros((200, 200, 3), dtype=np.uint8)
            text1 = "No data for " + player_name
            text2 = "in " + ', '.join(player_competitions)
            text3 = "across selected seasons"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255, 255, 255)  # White color (BGR format)
            thickness = 2

            text_size = cv2.getTextSize(text1, font, font_scale, thickness)[0]
            text_x = (error_image.shape[1] - text_size[0]) // 2
            text_y = 25
            cv2.putText(error_image, text1, (text_x, text_y), font, font_scale, color, thickness)

            text_size = cv2.getTextSize(text2, font, font_scale, thickness)[0]
            text_x = (error_image.shape[1] - text_size[0]) // 2
            text_y = 55
            cv2.putText(error_image, text2, (text_x, text_y), font, font_scale, color, thickness)

            text_size = cv2.getTextSize(text3, font, font_scale, thickness)[0]
            text_x = (error_image.shape[1] - text_size[0]) // 2
            text_y = 85
            cv2.putText(error_image, text3, (text_x, text_y), font, font_scale, color, thickness)

            _, img_png = cv2.imencode('.png', error_image)
            img_base64 = base64.b64encode(img_png).decode('utf-8')
            images.append(img_base64)
            continue
        visualizer = Visualization.Visualization(llm, info)
        code_block = visualizer.generate_non_llm(viz_options)
        if code_block:
            #print(code_block)
            exec(code_block)
        else:
            print("Failed to execute LLM code")
    conn.close()
    return jsonify({'visualizations': images})

@app.route('/api/visualize_manager', methods=['POST'])
def visualize_manager():
    import matplotlib
    matplotlib.use('Agg')
    img_base64 = ""
    llm = None
    conn = get_db_connection()
    data = request.json['manager_info']
    images = []
    for manager in data:
        global manager_colors, manager_viz_options
        global manager_name, manager_seasons, manager_stats
        manager_name = manager['name']
        manager_seasons = manager['seasons']
        manager_stats = manager['stats']
        manager_viz_options = manager['viz']
        manager_colors = manager_viz_options['colors']
        info = Info.Info(manager_name, manager_seasons, [], manager_stats)
        result = info.get_manager_data(conn)
        result.drop_duplicates(inplace=True)
        if 'Goals' in result.columns:
            result['Goals'] = result['Goals'].str.split(':').str[0].str.strip()
        if len(result.index) == 0:
            error_image = np.zeros((200, 200, 3), dtype=np.uint8)
            text1 = "No data for " + manager_name
            text2 = "across selected seasons"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255, 255, 255)  # White color (BGR format)
            thickness = 2

            text_size = cv2.getTextSize(text1, font, font_scale, thickness)[0]
            text_x = (error_image.shape[1] - text_size[0]) // 2
            text_y = 25
            cv2.putText(error_image, text1, (text_x, text_y), font, font_scale, color, thickness)

            text_size = cv2.getTextSize(text2, font, font_scale, thickness)[0]
            text_x = (error_image.shape[1] - text_size[0]) // 2
            text_y = 55
            cv2.putText(error_image, text2, (text_x, text_y), font, font_scale, color, thickness)

            _, img_png = cv2.imencode('.png', error_image)
            img_base64 = base64.b64encode(img_png).decode('utf-8')
            images.append(img_base64)
            continue
        visualizer = Visualization.Visualization(llm, info)
        code_block = visualizer.generate_manager(manager_viz_options)
        if code_block:
            exec(code_block)
        else:
            print("Failed to execute LLM code")
    conn.close()
    return jsonify({'visualizations': images})
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)