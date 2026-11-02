import random
from bots.bot_util import getAvailableMoves

class RandomBot:
  def __init__(self, colour, width, height):
    self.name = "Random"
    self.width = width
    self.height = height
    self.colour = colour

  def play(self, board):
    availableMoves = getAvailableMoves(board, self.height, self.width)
    randomTopMoveCol = random.choice([i for i in range(self.width) if availableMoves[i] < self.height])
    return (availableMoves[randomTopMoveCol], randomTopMoveCol)