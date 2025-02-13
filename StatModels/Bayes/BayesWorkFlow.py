import numpy as np
import pandas as pd
import requests
import scipy
from scipy.integrate import simpson
import GenerateBNNModel as generate

def get_moving_averages_for_player(stat, first_name, last_name, middle_name=None, days=5):
    
    #Creates dataframe of moving averages to be used as features
    df_MA = generate.create_df_for_player(first_name, last_name, middle_name, days=days)

    df_features = df_MA[['Game Date', f'Average {stat}', f'Opponent {stat}']]

    return df_features

def get_prior_dataframe(stat, first_name, last_name, middle_name, season):

    #Get player stats from previous season
    if middle_name == None:
            apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/season={season}')
    else:
            apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/middle_name={middle_name}/season={season}')
    data = apiinfo.json()
    df_1 = pd.DataFrame.from_dict(data, orient='index')

    #Get player stats for this season
    if middle_name == None:
            apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/season={season+1}')
    else:
            apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/middle_name={middle_name}/season={season+1}')
    data = apiinfo.json()
    df_2 = pd.DataFrame.from_dict(data, orient='index')

    df = pd.concat([df_1, df_2])
    df = df.reset_index().rename(columns={'index': 'Game Date'})

    df = df[['Game Date', f'{stat}']]

    return df

def create_prior_distribution_for_stat(prior_dataframe, stat='Points'):
    
    data = prior_dataframe[stat].values
    params = scipy.stats.skewnorm.fit(data)
    prior = scipy.stats.skewnorm(*params)

    return prior

def merge_dataframes(df_features, df_prior):
      
      return df_prior.merge(df_features, on='Game Date')

def generate_joint_distributions(df, PMA, OMA, stat):
      
      stat_bins = np.arange(0, df[f'{stat}'].max()+2, 1)
      avg_stat_bins = np.arange(0, int(PMA)+3, 1)
      avg_opponent_bins = np.arange(0, int(OMA)+3, 1)

      df[f'{stat} Bin'] = pd.cut(df[f'{stat}'], bins=stat_bins, labels=False, right=False)
      df[f'Average {stat} Bin'] = pd.cut(df[f'Average {stat}'], bins=avg_stat_bins, labels=False, right=False)
      df[f'Opponent {stat} Bin'] = pd.cut(df[f'Opponent {stat}'], bins=avg_opponent_bins, labels=False, right=False)

          # Define all possible values for rows and columns
      all_stat_bins = np.arange(len(stat_bins) - 1)  # Bins are 0-based indices
      all_avg_bins = np.arange(len(avg_stat_bins) - 1)
      all_opp_bins = np.arange(len(avg_opponent_bins) - 1)

        # Generate joint distributions with all possible bins as indices
      avg_stat_joint_distribution = pd.crosstab(
          df[f'{stat} Bin'], 
          df[f'Average {stat} Bin'], 
          dropna=False
      ).reindex(index=all_stat_bins, columns=all_avg_bins, fill_value=0)

      opp_stat_joint_distribution = pd.crosstab(
          df[f'{stat} Bin'], 
          df[f'Opponent {stat} Bin'], 
          dropna=False
      ).reindex(index=all_stat_bins, columns=all_opp_bins, fill_value=0)

      return avg_stat_joint_distribution, opp_stat_joint_distribution

def solve_probability_stat(PMA, OMA, prior, avg_stat_distribution, opponent_stat_distribution, max_stat=50):

    stat_range = np.arange(0,max_stat, 1)
    final_dist = np.zeros(len(stat_range))

    for i in range(len(final_dist)):
        stat_normalization_constant = sum(avg_stat_distribution.sum())
        opponent_normalization_constant = sum(opponent_stat_distribution.sum())
        p_A = prior.pdf(i)
        p_PMA = sum(avg_stat_distribution.loc[:i, round(PMA)])/stat_normalization_constant
        p_OMA = sum(opponent_stat_distribution.loc[:i, round(OMA)])/opponent_normalization_constant

        final_dist[i] = p_A * p_PMA * p_OMA

    final_dist = final_dist

    if sum(final_dist) == 0.0:
          return None
    
    fitted_dist = scipy.stats.gaussian_kde(stat_range, weights=final_dist)
    smoothed_dist = fitted_dist(stat_range)

    return smoothed_dist

def run_bayes(stat, season, PMA, OMA, max_stat, first_name, last_name, middle_name=None, days=5):
      
    df_MA = get_moving_averages_for_player(stat, first_name, last_name, middle_name, days=days)
    df_prior = get_prior_dataframe(stat, first_name, last_name, middle_name, season)
    prior_distribution = create_prior_distribution_for_stat(df_prior, stat=stat)
    final_df = merge_dataframes(df_MA, df_prior)
    avg_stat, opp_stat = generate_joint_distributions(final_df, PMA, OMA, stat)
    final_distribution = solve_probability_stat(PMA, OMA, prior_distribution, avg_stat, opp_stat, max_stat)


    if final_distribution is not None:
        return final_distribution
    else:
        #Switch to a different model?
        print("Input data is outside the scope of the model!")

#Retrieve players features
def retrieve_player_features(stat, days, first_name, last_name, middle_name=None, season=2025):

    if middle_name == None:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/season={season}')
    else:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/middle_name={middle_name}/season={season}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    features = df[f'{stat}'].iloc[-days:].mean()

    return features

#Retrieve team features
def retrieve_team_features(stat, days, team_name, season=2025):

    apiinfo = requests.get(f'http://127.0.0.1:5000/get_team_stats_for_season/team_name={team_name}/season={season}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    features = df[f'{stat}'].iloc[-days:].mean()

    return features