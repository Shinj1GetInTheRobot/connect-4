RED = 1
YELLOW = -1
import json
from util import isWon, printBoard
from bots.bot_random import RandomBot
from bots.bot_always_center import AlwaysCenterBot
from bots.bot_always_left import AlwaysLeftBot
from bots.bot_always_right import AlwaysRightBot
from bots.bot_always_low import AlwaysLowBot
from bots.bot_always_high import AlwaysHighBot
from bots.bot_make4from3 import MakeFourFromThreeBot
from bots.bot_minmax import MinimaxBot
import bots.heuristic_functions as h
import argparse
# Pls don't change above ---------------------------------------------

BOT_CLASSES = {
  "random": RandomBot,
  "always_center": AlwaysCenterBot,
  "always_left": AlwaysLeftBot,
  "always_right": AlwaysRightBot,
  "always_low": AlwaysLowBot,
  "always_high": AlwaysHighBot,
  "make4from3": MakeFourFromThreeBot,
}

HEURISTICS = {
  "none": h.heuristicNone,
  "near_center": h.heuristicNearCenter,
  "far_right": h.heuristicFarRight,
  "far_left": h.heuristicFarLeft,
  "far_up": h.heuristicFarUp,
  "far_down": h.heuristicFarDown,
}

BOT_CONFIGS = {
  name: ("regular", name)
  for name in BOT_CLASSES
}

for heuristic_name in HEURISTICS:
  BOT_CONFIGS[f"minimax_{heuristic_name}"] = ("minimax", heuristic_name)

BOT_CHOICES = [*BOT_CONFIGS, "all"]

# SELECT A MINIMAX BOT BY USING minimax_HEURISTIC_NAME e.g. minimax_none

def parse_args():
  parser = argparse.ArgumentParser(description="Command line for running games")
  parser.add_argument("player1", choices=BOT_CHOICES)
  parser.add_argument("player2", choices=BOT_CHOICES)
  parser.add_argument("game_data_name", type=str, help="Name of the game data file")
  parser.add_argument("-n", "--num_games", type=int, default=100, help="Number of games to play")
  parser.add_argument("-r", "--rows", type=int, default=6, help="Number of rows")
  parser.add_argument("-c", "--cols", type=int, default=7, help="Number of columns")
  parser.add_argument("-d1", "--depth", type=int, default=2, help="Depth for minimax bot1")
  parser.add_argument("-d2", "--depth2", type=int, default=2, help="Depth for minimax bot2")
  return parser.parse_args()

args = parse_args()

player1_names = list(BOT_CONFIGS) if args.player1 == "all" else [args.player1]
player2_names = list(BOT_CONFIGS) if args.player2 == "all" else [args.player2]

# Pls don't change below ---------------------------------------------
def playNewGame():
  moves = []
  result = 0
  winningMove = 0
  board = [[0 for _ in range(args.cols)] for _ in range(args.rows)]
  currentPlayer = RED
  lastMoveRow = -1
  lastMoveCol = -1
  while len(moves) < args.rows * args.cols:
    if currentPlayer == RED:
      lastMoveRow, lastMoveCol = player1.play(board) 
    else:
      lastMoveRow, lastMoveCol = player2.play(board) 

    moves.append(lastMoveCol)
    board[lastMoveRow][lastMoveCol] = currentPlayer
    winningMoveType = isWon(board, lastMoveRow, lastMoveCol, args.rows, args.cols)
    if winningMoveType != 0:
      result = currentPlayer
      break
    currentPlayer *= -1 
    
  return moves, result, winningMoveType

# Custom JSON encoder to print the moves array on one line
# Use this instead of json.dumps()
def pretty_arrays_json(data, indent=2):
    def format_value(value, level):
        if isinstance(value, dict):
            if not value:
                return "{}"
            pad = " " * (indent * level)
            child_pad = " " * (indent * (level + 1))
            items = [
                child_pad + json.dumps(k) + ": " + format_value(v, level + 1)
                for k, v in value.items()
            ]
            return "{\n" + ",\n".join(items) + "\n" + pad + "}"
        if isinstance(value, list):
            # Keep the entire array on one line
            return json.dumps(value)
        return json.dumps(value)
    return format_value(data, 0)

# Creates a bot based on name colour and other args
def create_bot(name, colour, depth):
  bot_type, option = BOT_CONFIGS[name]

  if bot_type == "minimax":

    return MinimaxBot(
      colour, args.cols, args.rows,
      depth, HEURISTICS[option]
    )
  return BOT_CLASSES[option](colour, args.cols, args.rows)

def convertMTStr(moveType):
  mtStr = ""
  if (moveType & 0b1) == 0b1:
    mtStr += 'h'
  if (moveType & 0b10) == 0b10:
    mtStr += ('v' if mtStr == "" else '+v')
  if (moveType & 0b100) == 0b100:
    mtStr += ('d1' if mtStr == "" else '+d1')
  if (moveType & 0b1000) == 0b1000:
    mtStr += ('d2' if mtStr == "" else '+d2')
  return mtStr


# Plays a bunch of games and saves the data to a prompted file name
game_data = {}
for player1_name in player1_names:
  for player2_name in player2_names:
    player1 = create_bot(player1_name, RED, args.depth)
    player2 = create_bot(player2_name, YELLOW, args.depth2)

    for i in range(args.num_games):
      moves, result, winningMoveType = playNewGame()
      game_data[str(i + 1)] = {
        "rows": args.rows,
        "columns": args.cols,
        "players": {
          "1": player1.name,
          "2": player2.name
        },
        "moves": moves,
        "num_moves": len(moves),
        "result": result,
        "winning_move_type": convertMTStr(winningMoveType)
      }

filename = f"{args.game_data_name}.json"
with open(f"./game_data/{filename}", "w", encoding="utf-8") as file:
  file.write(pretty_arrays_json(game_data))