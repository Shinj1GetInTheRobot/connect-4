import random

class AlwaysHighBot:
  def __init__(self, colour, width, height):
    self.name = "Always High"
    self.width = width
    self.height = height
    self.colour = colour

  def play(self, board):
    topRow = board[-1]

    max_height = -1
    for i in range(self.width):
      if topRow[i] != 0:
        continue
      for j in range(self.height):
        if board[j][i] == 0:
          max_height = max(max_height, j - 1)
          break

    legal_moves = []
    for i in range(self.width):
      if board[max_height + 1][i] == 0 and (max_height == -1 or board[max_height][i] != 0):
        legal_moves.append((max_height + 1, i))
        
    return random.choice(legal_moves)