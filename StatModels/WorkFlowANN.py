import numpy as np
import requests
import pandas as pd
import torch
import scipy
from scipy.integrate import simpson
import GenerateBNNModel as generate
import NeuralNetwork as NN

#Retrieve stats required for player -> this generates the three CSVs
def obtain_required_data(first_name, last_name, middle_name=None):
    df_3 = generate.create_df_for_player(first_name, last_name, middle_name, days=3)
    df_7 = generate.create_df_for_player(first_name, last_name, middle_name, days=7)
    df_14 = generate.create_df_for_player(first_name, last_name, middle_name, days=14)

    df_3 = df_3[['Average Points', 'Opponent Points', 'Points']].iloc[11:].reset_index(drop=True)
    df_7 = df_7[['Average Points', 'Opponent Points', 'Points']].iloc[7:].reset_index(drop=True)
    df_14 = df_14[['Average Points', 'Opponent Points', 'Points']]

    master_df = pd.DataFrame()

    master_df['Points'] = df_3['Points'].copy()
    master_df['Average Points 3-day'] = df_3['Average Points'].copy()
    master_df['Average Points 7-day'] = df_7['Average Points'].copy()
    master_df['Average Points 14-day'] = df_14['Average Points'].copy()
    master_df['Opponent Points 3-day'] = df_3['Opponent Points'].copy()
    master_df['Opponent Points 7-day'] = df_7['Opponent Points'].copy()
    master_df['Opponent Points 14-day'] = df_14['Opponent Points'].copy()

    master_df = master_df.dropna()

    #Shuffle the NN
    master_df = master_df.sample(frac=1).reset_index(drop=True)

    #Split into training and test sets
    training_df = master_df.iloc[:int(len(master_df)*0.5)]
    test_df = master_df.iloc[int(len(master_df)*0.5):]

    #Convert to torch arrays
    training_features = training_df[['Average Points 3-day', 'Average Points 7-day', 'Average Points 14-day','Opponent Points 3-day','Opponent Points 7-day','Opponent Points 14-day']].values
    training_labels = training_df[['Points']].values

    test_features = test_df[['Average Points 3-day', 'Average Points 7-day', 'Average Points 14-day','Opponent Points 3-day','Opponent Points 7-day','Opponent Points 14-day']].values
    test_labels = test_df[['Points']].values

    return training_features, training_labels, test_features, test_labels

#Train the Neural Network
def train_model(x_train, y_train, model, epochs=100, learning_rate=0.01, batch_size=20):

  # We must turn our x_train and y_train into tensors and define our dataset using "torch.utils.data.TensorDataset"
  dataset = torch.utils.data.TensorDataset(torch.tensor(x_train).float(), torch.tensor(y_train).float())

  # Define our loss function
  L = torch.nn.MSELoss()

  # Define our optimization technique
  # Typically the best optimizer we can use is a momentum based optimizer. This will allow for faster convergence
  optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0.05)

  # We will keep track of our loss function at each epoch so we can monitor how our training is going
  loss_list = np.zeros(epochs)

  for epoch in range(epochs):

    # Since we are iterating in batches we must keep a running count of our loss function
    epoch_loss = 0.0

    # PyTorch will automatically connect features to targets and seperate them into batches
    # We want to randomize our batches so that the NN doesn't learn the order it was fed information
    # and to avoid overfitting
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # We then loop through every batch and conduct our forward and backward passes
    for inputs, labels in dataloader:
      optimizer.zero_grad()

      # Unsqueeze changes the dimensions in a form readable by PyTroch
      # For example, if we have a tensor, [1,2,3,4], where each element is a different input
      # the model might fail to read it due to it containing one row (PyTorch will read it as 1 input, with four features)
      # Therefore, we unsqueeze it so that it becomes a (4,1) tensor, four rows, one column
      y_hat = model(inputs.unsqueeze(1)) # Forward Pass

      # Evaluate Batch Loss
      loss = L(y_hat, labels.unsqueeze(1))

      # Backpropogation
      loss.backward()

      # Update our weights
      optimizer.step()

      # Update the epochs total loss!
      epoch_loss += loss.item()

    loss_list[epoch] = epoch_loss

  return model, loss_list

#Acquire skewed distribution
def retrieve_skewness_params(data):
    
    a, loc, scale = scipy.stats.skewnorm.fit(data)

    return a, loc, scale

#Retrieve players features
def retrieve_player_features(first_name, last_name, middle_name=None, season=2025):

    if middle_name == None:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/season={season}')
    else:
        apiinfo = requests.get(f'http://127.0.0.1:5000/player_stats_for_season/first_name={first_name}/last_name={last_name}/middle_name={middle_name}/season={season}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    points_3_day = df['Points'].iloc[-3:].mean()
    points_7_day = df['Points'].iloc[-7:].mean()
    points_14_day = df['Points'].iloc[-14:].mean()

    return np.array([points_3_day, points_7_day, points_14_day])

#Retrieve team features
def retrieve_team_features(team_name, season=2025):

    apiinfo = requests.get(f'http://127.0.0.1:5000/get_team_stats_for_season/team_name={team_name}/season={season}')

    data = apiinfo.json()

    df = pd.DataFrame.from_dict(data, orient='index')

    points_3_day = df['Points'].iloc[-3:].mean()
    points_7_day = df['Points'].iloc[-7:].mean()
    points_14_day = df['Points'].iloc[-14:].mean()

    return np.array([points_3_day, points_7_day, points_14_day])

#Calculate Probability
def calculate_probability(params, model, features, stat):
    prediction = model(torch.tensor(features).float()).detach().numpy()
    n = np.round(prediction-stat)[0]
    if n > 0:  # We would bet the over since our prediction is greater than the total
        n = np.floor(n)
        x = np.linspace(-100, n, 20000)
        
        p = scipy.stats.skewnorm.pdf(x, params[0], params[1], params[2])
        probability = simpson(y=p, x=x)
        bet = 'OVER'
        

    if n <= 0: #We would bet the Under, since our prediction is less than the total
        n = np.ceil(n)
        x = np.linspace(n, 100, 20000)
        p = scipy.stats.skewnorm.pdf(x, params[0], params[1], params[2])
        probability = simpson(y=p, x=x)
        bet = 'UNDER'
        
    return n, probability, bet

#Determine expected return on bet
def expected_winnings(P_winning, line, bet):

    if line < 0:
        winnings = ((P_winning * (100*bet) / np.abs(line)) - ((1-P_winning) * bet))
    elif line > 0:
        winnings = ((P_winning * np.abs(line) / (100*bet)) - ((1-P_winning) * bet))

    return winnings
