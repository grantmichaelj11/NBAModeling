
from flask import Flask, request, jsonify
import db_connection as connector
import update
import pickle
import sys
import os
# Add the folder containing StatsModels to sys.path
sys.path.append(os.path.abspath('StatModels'))
import NeuralNetwork as NN
app = Flask(__name__)

@app.route('/player_stats_for_career_listed/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>/birthday=<birthday>', methods=['GET'])
@app.route('/player_stats_for_career_listed/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>', methods=['GET'])
@app.route('/player_stats_for_career_listed/first_name=<first_name>/last_name=<last_name>', methods=['GET'])
def player_stats_for_career_listed(first_name=None, middle_name=None, last_name=None, birthday=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_stats_career_listed', [first_name, last_name, middle_name, birthday])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

            player_stats = {}

            for row in data:
                player_stats[row[2].strftime("%Y-%m-%d")] = {
                'Name': row[0],
                'Season': row[1],
                'Game Date': row[2].strftime("%Y-%m-%d"),
                'Team': row[3],
                'Opponent': row[4],
                'Minutes': row[5],
                'Field Goals': row[6],
                'Field Goal Attempts': row[7],
                'Three Pointers': row[8],
                'Three Point Attempts': row[9],
                'Free Throws': row[10],
                'Free Throw Attempts': row[11],
                'Offensive Rebounds': row[12],
                'Defensive Rebounds': row[13],
                'Total Rebounds': row[14],
                'Assists': row[15],
                'Steals': row[16],
                'Blocks': row[17],
                'Turnovers': row[18],
                'Fouls': row[19],
                'Points': row[20]}


            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/player_stats_for_season/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>/season=<season>', methods=['GET'])
@app.route('/player_stats_for_season/first_name=<first_name>/last_name=<last_name>/season=<season>', methods=['GET'])
def player_stats_for_season(season=None, first_name=None, middle_name=None, last_name=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_stats_for_season', [first_name, last_name, middle_name, season])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

            player_stats = {}

            for row in data:
                player_stats[row[2].strftime("%Y-%m-%d")] = {
                'Name': row[0],
                'Season': row[1],
                'Team': row[3],
                'Opponent': row[4],
                'Minutes': row[5],
                'Field Goals': row[6],
                'Field Goal Attempts': row[7],
                'Three Pointers': row[8],
                'Three Point Attempts': row[9],
                'Free Throws': row[10],
                'Free Throw Attempts': row[11],
                'Offensive Rebounds': row[12],
                'Defensive Rebounds': row[13],
                'Total Rebounds': row[14],
                'Assists': row[15],
                'Steals': row[16],
                'Blocks': row[17],
                'Turnovers': row[18],
                'Fouls': row[19],
                'Points': row[20]}


            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/player_stats_for_date/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>/date=<date>', methods=['GET'])
@app.route('/player_stats_for_date/first_name=<first_name>/last_name=<last_name>/date=<date>', methods=['GET'])
def player_stats_for_date(date=None, first_name=None, middle_name=None, last_name=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_stats_for_date', [first_name, last_name, middle_name, date])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

            player_stats = {}

            for row in data:
                player_stats[row[2].strftime("%Y-%m-%d")] = {
                'Name': row[0],
                'Season': row[1],
                'Team': row[3],
                'Opponent': row[4],
                'Minutes': row[5],
                'Field Goals': row[6],
                'Field Goal Attemtps': row[7],
                'Three Pointers': row[8],
                'Three Point Attempts': row[9],
                'Free Throws': row[10],
                'Free Throw Attempts': row[11],
                'Offensive Rebounds': row[12],
                'Defensive Rebounds': row[13],
                'Total Rebounds': row[14],
                'Assists': row[15],
                'Steals': row[16],
                'Blocks': row[17],
                'Turnovers': row[18],
                'Fouls': row[19],
                'Points': row[20]}


            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/player_stats_vs_team/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>/team=<team>', methods=['GET'])
@app.route('/player_stats_vs_team/first_name=<first_name>/last_name=<last_name>/team=<team>', methods=['GET'])
def player_stats_vs_team(team=None, first_name=None, middle_name=None, last_name=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_stats_vs_team', [first_name, last_name, middle_name, team])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

            player_stats = {}

            for row in data:
                player_stats[row[2].strftime("%Y-%m-%d")] = {
                'Name': row[0],
                'Season': row[1],
                'Team': row[3],
                'Opponent': row[4],
                'Minutes': row[5],
                'Field Goals': row[6],
                'Field Goal Attemtps': row[7],
                'Three Pointers': row[8],
                'Three Point Attempts': row[9],
                'Free Throws': row[10],
                'Free Throw Attempts': row[11],
                'Offensive Rebounds': row[12],
                'Defensive Rebounds': row[13],
                'Total Rebounds': row[14],
                'Assists': row[15],
                'Steals': row[16],
                'Blocks': row[17],
                'Turnovers': row[18],
                'Fouls': row[19],
                'Points': row[20]}


            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/player_stats_career/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>', methods=['GET'])
@app.route('/player_stats_career/first_name=<first_name>/last_name=<last_name>', methods=['GET'])
def player_stats_career(first_name=None, middle_name=None, last_name=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            result = cursor.callproc('get_player_stats_career', [first_name, last_name, middle_name])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()][0]

            player_stats = {'Name': data[0],
                            'Minutes': data[1],
                           'Field Goals': data[2],
                           'Field Goal Attemtps': data[3],
                           'Three Pointers': data[4],
                           'Three Point Attempts': data[5],
                           'Free Throws': data[6],
                           'Free Throw Attempts': data[7],
                           'Offensive Rebounds': data[8],
                           'Defensive Rebounds': data[9],
                           'Total Rebounds': data[10],
                           'Assists': data[11],
                           'Steals': data[12],
                           'Blocks': data[13],
                           'Turnovers': data[14],
                           'Fouls': data[15],
                           'Points': data[16]}


            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/all_teams/', methods=['GET'])
def all_teams():
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            result = cursor.callproc('get_all_teams', [])

            conferences = {'Western': {'Pacific': [],
                                       'Northwest': [],
                                       'Southwest': []},
                           'Eastern': {'Atlantic': [],
                                       'Central': [],
                                       'Southeast': []}}



            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

                for row in data:
                    if row[1] == 'Atlantic':
                        conferences['Eastern']['Atlantic'].append(row[0])
                    elif row[1] == 'Northwest':
                        conferences['Western']['Northwest'].append(row[0])
                    elif row[1] == 'Central':
                        conferences['Eastern']['Central'].append(row[0])
                    elif row[1] == 'Pacific':
                        conferences['Western']['Pacific'].append(row[0])
                    elif row[1] == 'Southeast':
                        conferences['Eastern']['Southeast'].append(row[0])
                    elif row[1] == 'Southwest':
                        conferences['Western']['Southwest'].append(row[0])

            return jsonify(conferences)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_team_stats_for_season/team_name=<team_name>/season=<season>', methods=['GET'])
def get_team_stats_for_season(team_name, season):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            result = cursor.callproc('get_team_stats_for_season', [team_name, season])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]

            team_stats = {}

            for row in data:

                team_stats[row[0].strftime("%Y-%m-%d")] = {
                'Season': row[1],
                'Team': row[2],
                'Field Goals': row[3],
                'Field Goal Attemtps': row[4],
                'Three Pointers': row[5],
                'Three Point Attempts': row[6],
                'Free Throws': row[7],
                'Free Throw Attempts': row[8],
                'Offensive Rebounds': row[9],
                'Defensive Rebounds': row[10],
                'Total Rebounds': row[11],
                'Assists': row[12],
                'Steals': row[13],
                'Blocks': row[14],
                'Turnovers': row[15],
                'Fouls': row[16],
                'Points': row[17],
                'Opponent': row[18],
                'Opponent Field Goals': row[19],
                'Opponent Field Goal Attemtps': row[20],
                'Opponent Three Pointers': row[21],
                'Opponent Three Point Attempts': row[22],
                'Opponent Free Throws': row[23],
                'Opponent Free Throw Attempts': row[24],
                'Opponent Offensive Rebounds': row[25],
                'Opponent Defensive Rebounds': row[26],
                'Opponent Total Rebounds': row[27],
                'Opponent Assists': row[28],
                'Opponent Steals': row[29],
                'Opponent Blocks': row[30],
                'Opponent Turnovers': row[31],
                'Opponent Fouls': row[32],
                'Opponent Points': row[33]}

            return jsonify(team_stats)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_previous_n_team_stats/team_name=<team_name>/date=<date>/days=<days>', methods=['GET'])
def get_previous_n_team_stats(team_name, date, days):
    
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            result = cursor.callproc('get_previous_n_team_stats', [team_name, date, days])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()]


            team_stats = {}

            for row in data:

                team_stats[row[0].strftime("%Y-%m-%d")] = {
                'Season': row[1],
                'Team': row[2],
                'Field Goals': row[3],
                'Field Goal Attemtps': row[4],
                'Three Pointers': row[5],
                'Three Point Attempts': row[6],
                'Free Throws': row[7],
                'Free Throw Attempts': row[8],
                'Offensive Rebounds': row[9],
                'Defensive Rebounds': row[10],
                'Total Rebounds': row[11],
                'Assists': row[12],
                'Steals': row[13],
                'Blocks': row[14],
                'Turnovers': row[15],
                'Fouls': row[16],
                'Points': row[17],
                'Opponent': row[18],
                'Opponent Field Goals': row[19],
                'Opponent Field Goal Attempts': row[20],
                'Opponent Three Pointers': row[21],
                'Opponent Three Point Attempts': row[22],
                'Opponent Free Throws': row[23],
                'Opponent Free Throw Attempts': row[24],
                'Opponent Offensive Rebounds': row[25],
                'Opponent Defensive Rebounds': row[26],
                'Opponent Total Rebounds': row[27],
                'Opponent Assists': row[28],
                'Opponent Steals': row[29],
                'Opponent Blocks': row[30],
                'Opponent Turnovers': row[31],
                'Opponent Fouls': row[32],
                'Opponent Points': row[33]}

            return jsonify(team_stats)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_player_id/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>/birthday=<birthday>', methods=['GET'])
@app.route('/get_player_id/first_name=<first_name>/last_name=<last_name>/middle_name=<middle_name>', methods=['GET'])
@app.route('/get_player_id/first_name=<first_name>/last_name=<last_name>', methods=['GET'])
def get_player_id(first_name=None, middle_name=None, last_name=None, birthday=None):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_id', [first_name, last_name, middle_name, birthday])

            for result in cursor.stored_results():
                data = [list(row) for row in result.fetchall()][0]

            player_stats = {'Name': data[0],
                            'id': data[1]}

            
            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_player_model/player_id=<player_id>', methods=['GET'])
def get_player_model(player_id):
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            cursor.callproc('get_player_model', [player_id])

            for result in cursor.stored_results():
                data = result.fetchall()

            if not data:
                return jsonify({'ERROR': 'NO MODEL FOR PLAYER'}), 500

            data = data[0]

            unserialized = pickle.loads(data[3])

            print(type(unserialized))

            with open('StatModels/model.pkl', 'wb') as file:
                pickle.dump(unserialized, file)

            player_stats = {'id': data[0],
                            'player_id': data[1],
                            'creation_date': data[2],
                            'skewness': data[4],
                            'mean': data[5],
                            'scale': data[6]}

            return jsonify(player_stats)
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/input_player_model/player_id=<player_id>/skewness=<skewness>/mean=<mean>/scale=<scale>', methods=['POST'])  
def input_player_model(player_id, skewness, mean, scale):
    
    try:
        with connector.connect_to_database() as conn:

            cursor = conn.cursor()

            model_file = request.files['model']
            model_data = model_file.read()

            cursor.callproc('input_player_model', [player_id, model_data, skewness, mean, scale])

            conn.commit()

            return jsonify({"message": "Player model inserted successfully!"}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_games/year=<year>/month=<month>/day=<day>/update_seasons=<update_seasons>/start_year=<start_year>/end_year=<end_year>', methods=['GET'])
def update_games(year, month, day, update_seasons, start_year=2024, end_year=2024):

    if update_seasons.lower() == 'true':
        update_seasons = True
    else:
        update_seasons=False

    start_year = int(start_year)
    end_year = int(end_year)

    update.run(year, month, day, update_seasons, start_year, end_year)

    return "DATABASE UPDATED"

if __name__ == '__main__':
    app.run(debug=False)