import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
import numpy as np
import json

folder = "always_center_v_random"
bot1 = ("always_center", "minimax_near_center")
bot2 = ("random", "minimax_none")
depth = 4
figSize = (14, 7)

depth += 1
files = [[] for i in range(depth)]
for i in range(depth):
  bot1Name = bot1[0] if i == 0 else f"{bot1[1]}_d{i}"
  for j in range(depth):
    bot2Name = bot2[0] if j == 0 else f"{bot2[1]}_d{j}"
    files[i].append(f"{bot1Name}_v_{bot2Name}")

# __________________ Without Winning Move Type ___________________

histogram_background_color = "#888"
bin_colours = ["white", "black"]

fig, axs = plt.subplots(nrows=depth, ncols=depth, figsize=figSize)

minMoves = 7
maxMoves = -1
games = [[[] for j in range(depth)] for i in range(depth)]

for i in range(depth):
  for j in range(depth):

    axs[i][j].set_facecolor(histogram_background_color)
    axs[i][j].yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    if i == 0:
      axs[i][j].set_title(f"D-{j}", fontweight="bold")
    if j == 0:
      axs[i][j].set_ylabel(f"D-{i}", fontweight="bold")

    with open(f"./game_data/{folder}/{files[i][j]}.json", "r") as file:
      data = json.load(file)
      maxMoves = data["1"]["columns"] * data["1"]["rows"]
      for game in data.values():
        games[i][j].append(game["num_moves"])

    # Percentage based
    counts, edges, patches = axs[i][j].hist(
      games[i][j], 
      weights=np.ones(len(games[i][j])) / len(games[i][j]), 
      bins=maxMoves - minMoves + 1, 
      range=(minMoves, maxMoves)
    )
    for k, patch in enumerate(patches):
        patch.set_facecolor(bin_colours[k % 2])
        patch.set_edgecolor(histogram_background_color)

fig.suptitle(f"{bot2[0]}", fontsize=24, fontweight="bold")
fig.supylabel(f"{bot1[0]}", fontsize=24, fontweight="bold")

handles = [
    Patch(facecolor="white", edgecolor="black", label="Player 1"),
    Patch(facecolor="black", edgecolor="black", label="Player 2"),
]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1.0))
plt.tight_layout(rect=(0.05, 0.0, 1.0, 1.0))
# plt.show()
plt.savefig(f"./histograms/{folder}_3.png")

# __________________ With Winning Move Type ___________________

bin_colours = ["green", "blue", "red", "orange", "#ff5ccb"]
histogram_background_color = "#888"
fig, axs = plt.subplots(nrows=depth, ncols=depth, figsize=figSize)


# games = [Horizontal, Vertical, D1, D2]
games = [[[[] for i in bin_colours] for j in range(depth)] for i in range(depth)]
minMoves = 7
maxMoves = -1

for i in range(depth):
  for j in range(depth):
    with open(f"./game_data/{folder}/{files[i][j]}.json", "r") as file:
      data = json.load(file)
      maxMoves = data["1"]["columns"] * data["1"]["rows"]
      for game in data.values():
        wMT = game["winning_move_type"]
        if not wMT: # Draws
          games[i][j][4].append(game["num_moves"])
          continue
        if 'h' in wMT:
          games[i][j][0].append(game["num_moves"])
        if 'v' in wMT:
          games[i][j][1].append(game["num_moves"])
        if 'd1' in wMT:
          games[i][j][2].append(game["num_moves"])
        if 'd2' in wMT:
          games[i][j][3].append(game["num_moves"])

    games[i][j] = np.array(games[i][j], dtype=object)

    # Percentage based histogram
    weights = [np.ones(len(g)) / len(data) for g in games[i][j]]
    counts, edges, patches = axs[i][j].hist(
        games[i][j],
        weights=weights,
        bins=maxMoves - minMoves + 1,
        range=(minMoves, maxMoves),
        stacked=True,
        color=bin_colours,
        edgecolor="black",
        label=["Horizontal", "Vertical", "D1", "D2", "Draw"]
    )

    axs[i][j].set_facecolor(histogram_background_color)
    if i == 0:
      axs[i][j].set_title(f"D-{j}", fontweight="bold")
    if j == 0:
      axs[i][j].set_ylabel(f"D-{i}", fontweight="bold")
    axs[i][j].yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))

fig.suptitle(f"{bot2[0]}", fontsize=24, fontweight="bold")
fig.supylabel(f"{bot1[0]}", fontsize=24, fontweight="bold")

handles, labels = axs[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.0, 1.0))

plt.tight_layout(rect=(0.05, 0.0, 1.0, 1.0))
# plt.show()
plt.savefig(f"./histograms/{folder}_4.png")