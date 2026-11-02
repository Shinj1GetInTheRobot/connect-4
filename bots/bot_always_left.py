class AlwaysLeftBot:
  def __init__(self, colour, width, height):
    self.name = "Always Left"
    self.width = width
    self.height = height
    self.colour = colour

  def play(self, board):
    topRow = board[-1]
    for i in range(self.width):
      if (topRow[i] == 0):
        j = self.height - 1
        while (j > 0 and board[j - 1][i] == 0):
          j -= 1
        return (j, i)