
# Heuristic Functions
# Evaluates a relativistic heuristic winning value (from the perspective the given player's colour)
# Note: Can assume the game has not been won yet

def heuristicNone(board, width, height, colour):
  return 0

def heuristicNearCenter(board, width, height, colour):
  h = 0
  orderedCols =  [min(i, width - 1 - i) for i in range(width)]
  for j in range(height):
    for i in range(width):
      h += board[j][i] * orderedCols[i]
  return h * colour

def heuristicFarRight(board, width, height, colour):
  h = 0
  orderedCols = [i for i in range(width)]
  for j in range(height):
    for i in range(width):
      h += board[j][i] * orderedCols[i]
  return h * colour

def heuristicFarLeft(board, width, height, colour):
  h = 0
  orderedCols = [(width - i - 1) for i in range(width)]
  for j in range(height):
    for i in range(width):
      h += board[j][i] * orderedCols[i]
  return h * colour

def heuristicFarUp(board, width, height, colour):
  h = 0
  orderedRows = [j for j in range(height)]
  for j in range(height):
    for i in range(width):
      h += board[j][i] * orderedRows[j]
  return h * colour

def heuristicFarDown(board, width, height, colour):
  h = 0
  orderedRows = [(height - j - 1) for j in range(height)]
  for j in range(height):
    for i in range(width):
      h += board[j][i] * orderedRows[j]
  return h * colour