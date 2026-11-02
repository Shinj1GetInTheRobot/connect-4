# Returns true if a game was just won
def isWon(board, lastMoveRow, lastMoveCol, rows, cols):
  if lastMoveRow == -1 or lastMoveCol == -1:
    return False
  currentPlayer = board[lastMoveRow][lastMoveCol]
  # Check horizontally
  lineCountA = 0
  lineCountB = 0
  row = board[lastMoveRow]
  i = lastMoveCol - 1
  while i > -1 and row[i] == currentPlayer:
    lineCountA += 1
    i -= 1
  i = lastMoveCol + 1
  while i < cols and row[i] == currentPlayer:
    lineCountB += 1
    i += 1
  if lineCountA + lineCountB + 1 >= 4:
    return True
  # Check vertically
  lineCountA = 0
  lineCountB = 0
  i = lastMoveRow - 1
  while i > -1 and board[i][lastMoveCol] == currentPlayer:
    lineCountA += 1
    i -= 1
  i = lastMoveRow + 1
  while i < rows and board[i][lastMoveCol] == currentPlayer:
    lineCountB += 1
    i += 1
  if lineCountA + lineCountB + 1 >= 4:
    return True
  # Check diagonally bottom-left -> top-right
  lineCountA = 0
  lineCountB = 0
  i = 1
  while lastMoveCol - i > -1 and lastMoveRow - i > -1 and board[lastMoveRow - i][lastMoveCol - i] == currentPlayer:
    lineCountA += 1
    i += 1
  i = 1
  while lastMoveCol + i < cols and lastMoveRow + i < rows and board[lastMoveRow + i][lastMoveCol + i] == currentPlayer:
    lineCountB += 1
    i += 1
  if lineCountA + lineCountB + 1 >= 4:
    return True
  # Check diagonally top-left -> bottom-right
  lineCountA = 0
  lineCountB = 0
  i = 1
  while lastMoveCol - i > -1 and lastMoveRow + i < rows and board[lastMoveRow + i][lastMoveCol - i] == currentPlayer:
    lineCountA += 1
    i += 1
  i = 1
  while lastMoveCol + i < cols and lastMoveRow - i > -1 and board[lastMoveRow - i][lastMoveCol + i] == currentPlayer:
    lineCountB += 1
    i += 1
  if lineCountA + lineCountB + 1 >= 4:
    return True
  # No line of 4 found -> game is not won yet
  return False


# Returns an array representing the available moves in the current board
# E.g. [3, 2, 1, 1, 6, 4, 2] -> board might look like this:
#     O O O O R O O
#     O O O O Y O O
#     O O O O Y R O
#     R O O O Y R O
#     R Y O O R R Y
#     R Y Y R R Y Y
def getAvailableMoves(board, rows, cols):
  topRow = board[-1]
  availableMoves = []
  for i in range(cols):
    if topRow[i] != 0:
      availableMoves.append(rows)
    else:
      j = 0
      while board[j][i] != 0:
        j += 1
      availableMoves.append(j)
  return availableMoves


def isDraw(board):
  topRow = board[-1]
  for i in topRow:
    if i == 0:
      return False
  return True