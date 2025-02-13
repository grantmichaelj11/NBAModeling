import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd


def retrieve_stat_from_player(stat, season, first_name, last_name, middle_name=None):

    if middle_name == None:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/season={season}')
    else:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/middle_name={middle_name}/season={season}')

    data = apiinfo.json()

            
    df = pd.DataFrame.from_dict(data, orient='index')

    return df[stat]

def retrieve_stat_from_team(stat, team, season):
    
    apiinfo = requests.get(f'http://127.0.0.1:5000/get_team_stats_for_season/team_name={team}/season={season}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    return df[stat]

def retrieve_skewness_params(data):
    
    a, loc, scale = scipy.stats.skewnorm.fit(data)

    return a, loc, scale

def plot_stat_distribution(a, loc, scale, x_min, x_max):
    
    x = np.linspace(x_min,x_max, 500)
    p = scipy.stats.skewnorm.pdf(x, a, loc, scale)
    plt.plot(x, p,c='black')
    plt.xlabel('Points', fontsize=16)
    plt.ylabel(r'$P(points)$', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

# We need to get players rank scoring wise on team for a specific game and then get the averages of desired stat
# Then we need to iterate through the opponents team  and see the averages of stat for players 1-N
# Finally we can compare each player to the opponents usual allowed stat.

def main():

    stats = retrieve_stat_from_player('Points', 2012, 'Lebron', 'James')
    #team_stats = retrieve_stat_from_team('Points', 'New York Knicks', 2015)
    params = retrieve_skewness_params(stats)
    plot_stat_distribution(*params, 0, 200)

    

#apiinfo = requests.get(f'http://127.0.0.1:5000/update_games/year={2024}/month={12}/day=04/update_seasons={False}/start_year={2024}/end_year={2025}')

#main()
#plt.show()