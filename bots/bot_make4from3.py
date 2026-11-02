from bots.bot_random import RandomBot

class MakeFourFromThreeBot(RandomBot):
  def __init__(self, colour, width, height):
    super().__init__(colour, width, height)
    self.name = "Make 4 from 3"

  def play(self, board):
    for i in range(self.width):
      j = self.height - 1
      if board[j][i] != 0:
        continue
      while (j > 0 and board[j - 1][i] == 0):
        j -= 1
      board[j][i] = self.colour
      if self.isWon(board, j, i):
        board[j][i] = 0
        return (j, i)
      else:
        board[j][i] = 0
    return super().play(board)

  def isWon(self, board, lastMoveRow, lastMoveCol):
    # Check horizontally
    lineCountA = 0
    lineCountB = 0
    row = board[lastMoveRow]
    i = lastMoveCol - 1
    while i > -1 and row[i] == self.colour:
      lineCountA += 1
      i -= 1
    i = lastMoveCol + 1
    while i < self.width and row[i] == self.colour:
      lineCountB += 1
      i += 1
    if lineCountA + lineCountB + 1 >= 4:
      return True

    # Check vertically
    lineCountA = 0
    lineCountB = 0
    i = lastMoveRow - 1
    while i > -1 and board[i][lastMoveCol] == self.colour:
      lineCountA += 1
      i -= 1
    i = lastMoveRow + 1
    while i < self.height and board[i][lastMoveCol] == self.colour:
      lineCountB += 1
      i += 1
    if lineCountA + lineCountB + 1 >= 4:
      return True

    # Check diagonally bottom-left -> top-right
    lineCountA = 0
    lineCountB = 0
    i = 1
    while lastMoveCol - i > -1 and lastMoveRow - i > -1 and board[lastMoveRow - i][lastMoveCol - i] == self.colour:
      lineCountA += 1
      i += 1
    i = 1
    while lastMoveCol + i < self.width and lastMoveRow + i < self.height and board[lastMoveRow + i][lastMoveCol + i] == self.colour:
      lineCountB += 1
      i += 1
    if lineCountA + lineCountB + 1 >= 4:
      return True

    # Check diagonally top-left -> bottom-right
    lineCountA = 0
    lineCountB = 0
    i = 1
    while lastMoveCol - i > -1 and lastMoveRow + i < self.height and board[lastMoveRow + i][lastMoveCol - i] == self.colour:
      lineCountA += 1
      i += 1
    i = 1
    while lastMoveCol + i < self.width and lastMoveRow - i > -1 and board[lastMoveRow - i][lastMoveCol + i] == self.colour:
      lineCountB += 1
      i += 1
    if lineCountA + lineCountB + 1 >= 4:
      return True

    # No line of 4 found -> game is not won yet
    return False