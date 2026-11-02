import random

class AlwaysLowBot:
  def __init__(self, colour, width, height):
    self.name = "Always Low"
    self.width = width
    self.height = height
    self.colour = colour

  def play(self, board):
    legal_moves = []
    for j in range(self.height):
      row = board[j]
      for i in range(self.width):
        if (row[i] == 0):
          legal_moves.append((j, i))
      if len(legal_moves) != 0:
        break
    return random.choice(legal_moves)