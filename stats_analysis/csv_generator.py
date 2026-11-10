import json
import pandas as pd


game_data_file = "./random_v_random/random_d0_v_random_d0"


# Pls don't change below ---------------------------------------------
def parseGame(game):
  rows, cols, players, _, numMoves, result, winningMoveType = game.values()
  return [rows, cols, players["1"], players["2"], numMoves, (3 - result)// 2, winningMoveType]

# Read the json file
game_data = None
with open(f"./game_data/{game_data_file}.json", "r") as file:
  game_data = json.load(file)

# Write the csv file
COLS = ["Rows", "Cols", "Player1", "Player2", "Moves", "Winner", "WinningMoveType"]
game_data = { k: parseGame(v) for k, v in game_data.items() }
df = pd.DataFrame.from_dict(game_data, orient='index', columns=COLS)
with open(f"./game_data/{game_data_file}.csv", "w", newline='') as file:
  df.to_csv(file, index_label="Game")