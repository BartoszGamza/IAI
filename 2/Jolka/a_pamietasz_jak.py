import numpy as np
import time

class Board:
  def __init__(self, matrix):
    self.matrix = matrix
    self.height = np.shape(matrix)[0]
    self.width = np.shape(matrix)[1]

  def get_real_row_length (self, row_index):
    row = self.matrix[row_index]
    filter(lambda a: a != '#', row)
    return len(row)

  def word_fits_row (self, row_index, word):
    rowLen = self.get_real_row_length(row_index)
    return rowLen == len(word)

  def fill_row (self, row_index, word):
    for char in range(len(self.matrix[row_index])):
      self.matrix[row_index][char] = word[char]

def read_board (filename):
  with open(filename) as input_file:
    board = [[char for char in line.strip()] for line in input_file.readlines()]
    # board = np.matrix([list(line.strip()) for line in input_file.readlines()])
    return Board(board)

def read_words (filename):
  words = []
  with open(filename) as input_file:
    for word in input_file.readlines():
      words.append(word.strip('\n'))
  return words

def backtrack (board, words, current_word_index):
  if (current_word_index < len(words)):
    word = words[current_word_index]
    for row in range(len(board.matrix)):
      if board.word_fits_row(row, word):
        board.fill_row(row, word)
        print(board.matrix)
        current_word_index = current_word_index + 1
        backtrack(board, words, current_word_index)
      else:
        current_word_index = current_word_index + 1
        backtrack(board, words, current_word_index)

if __name__ == '__main__':
  board = read_board('puzzle0')
  words = read_words('words0')
  backtrack(board, words, 0)
