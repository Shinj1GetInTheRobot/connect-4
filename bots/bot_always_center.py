import random
from bots.bot_util import getAvailableMoves

class AlwaysCenterBot:
  def __init__(self, colour, width, height):
    self.name = "Always Center"
    self.width = width
    self.height = height
    self.colour = colour

  def play(self, board):
    availableMoves = getAvailableMoves(board, self.height, self.width)
    # Find the nearest available move from the center on the left-side
    i = (self.width - 1) // 2
    while i >= 0 and availableMoves[i] == self.height:
      i -= 1
    # Find the nearest available move from the center on the right-side
    j = self.width // 2
    while j < self.width and availableMoves[j] == self.height:
      j += 1
    # If one side has no available column, use the other side
    if i < 0:
      return availableMoves[j], j
    if j >= self.width:
      return availableMoves[i], i
    # Return whichever is closest
    if ((self.width - 1) // 2) - i < j - (self.width // 2):
      return availableMoves[i], i
    elif j - (self.width // 2) < ((self.width - 1) // 2) - i:
      return availableMoves[j], j
    else:
      r = random.choice([i, j])
      return availableMoves[r], r