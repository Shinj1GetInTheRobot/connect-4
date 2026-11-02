import random
from bots.bot_util import isWon, isDraw, getAvailableMoves

WIN = 999999

class MinimaxBot:
  def __init__(self, colour, width, height, depth, heuristic_func):
    self.name = f"minimax_{heuristic_func.__name__.strip('heuristic')}_d{depth}"
    self.width = width
    self.height = height
    self.colour = colour
    self.depth = depth
    self.heuristic = heuristic_func
    self.lastMoveRow = -1
    self.lastMoveCol = -1

  def play(self, board):
    availableMoves = getAvailableMoves(board, self.height, self.width)
    heuristic_vals = [float('-inf') for i in range(self.width)]
    for i in range(self.width):
      if availableMoves[i] != self.height:
      
        j = availableMoves[i]

        # Play the move
        board[j][i] = self.colour
        availableMoves[i] += 1

        # Evaluate this move's heuristic
        heuristic_vals[i] = -self.negamax(board, availableMoves, j, i, -self.colour, self.depth - 1)

        # Undo the move
        board[j][i] = 0
        availableMoves[i] = j
    
    max_h = max(heuristic_vals)
    randomTopMoveCol = random.choice([i for i in range(self.width) if heuristic_vals[i] == max_h and availableMoves[i] < self.height])
    return (availableMoves[randomTopMoveCol], randomTopMoveCol)
    

  def negamax(self, board, availableMoves, lastMoveRow, lastMoveCol, currColour, currDepth):
    if isWon(board, lastMoveRow, lastMoveCol, self.height, self.width):
      return -(WIN + currDepth)   # Can change this?
    elif currDepth == 0:
      return -self.heuristic(board, self.width, self.height, -currColour)
    elif isDraw(board):
      return 0                    # Can change this?

    eval = float('-inf')
    for i in range(self.width):
      if availableMoves[i] != self.height:

        j = availableMoves[i]

        # Play the move
        lastMoveCol = i
        lastMoveRow = j
        board[j][i] = currColour
        availableMoves[i] += 1

        # Evaluate the heuristic
        eval = max(eval, -self.negamax(board, availableMoves, lastMoveRow, lastMoveCol, -currColour, currDepth - 1))

        # Undo the move
        board[j][i] = 0
        availableMoves[i] = j
        
    return eval