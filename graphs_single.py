import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import json

fileName = "always_low_v_random"
folder = fileName

# _____________ Single Graph W/D/L Black and White _____________

histogram_background_color = "#888"
bin_colours = ["white", "black"]

minMoves = 7
maxMoves = -1
gamesAll = []
with open(f"./game_data/{folder}/{fileName}.json", "r") as file:
  data = json.load(file)
  maxMoves = data["1"]["columns"] * data["1"]["rows"]
  for game in data.values():
      gamesAll.append(game["num_moves"])

fig, ax = plt.subplots(figsize=(8,4))
ax.set_facecolor(histogram_background_color)
ax.set_title(fileName)
ax.set_xlabel("# of moves")
ax.set_ylabel("Games")
counts, edges, patches = ax.hist(gamesAll, bins=maxMoves - minMoves + 1, range=(minMoves, maxMoves))

for i, patch in enumerate(patches):
    patch.set_facecolor(bin_colours[i % 2])
    patch.set_edgecolor(histogram_background_color)
    
# plt.show()
plt.savefig(f"./histograms/{fileName}_1.png")


# ________________ Single Graph V/H/D Coloured ________________

bin_colours = ["green", "blue", "red", "orange", "#ff5ccb"]
histogram_background_color = "#888"

# games = [Horizontal, Vertical, D1, D2]
games = [[], [], [], [], []]
with open(f"./game_data/{folder}/{fileName}.json", "r") as file:
  data = json.load(file)
  minMoves = 7
  maxMoves = data["1"]["columns"] * data["1"]["rows"]
  for game in data.values():
    wMT = game["winning_move_type"]
    if not wMT: # Draws
      games[4].append(game["num_moves"])
      continue
    if 'h' in wMT:
      games[0].append(game["num_moves"])
    if 'v' in wMT:
      games[1].append(game["num_moves"])
    if 'd1' in wMT:
      games[2].append(game["num_moves"])
    if 'd2' in wMT:
      games[3].append(game["num_moves"])

games = np.array(games, dtype=object)

fig, ax = plt.subplots(figsize=(8,4))
ax.set_facecolor(histogram_background_color)
ax.set_title(fileName)
ax.set_xlabel("# of moves")

# Percentage based histogram
weights = [np.ones(len(games)) / len(data) for games in games]
counts, edges, patches = ax.hist(
    games,
    weights=weights,
    bins=maxMoves - minMoves + 1,
    range=(minMoves, maxMoves),
    stacked=True,
    color=bin_colours,
    edgecolor="black",
    label=["Horizontal", "Vertical", "D1", "D2", "Draw"]
)

ax.set_ylabel(f"% Games")
ax.legend()
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
plt.tight_layout()
# plt.show()
plt.savefig(f"./histograms/{fileName}_2.png")