# import sys
import csv
import random
import math
import numpy as np
import time

class Puzzle:
  def __init__(self, raw_data, difficulity, id):
    self.grid = np.reshape(list(raw_data), (-1, 9))
    self.difficulity = difficulity
    self.id = id

  def grid_column (self, index):
     return [row[index] for row in self.grid]

  def grid_block (self, index):
    row = math.floor(index[0] / 3)
    col = math.floor(index[1] / 3)
    block_index = int((row * 3)  + col)
    chunked_array = chunk_array(self.grid, 3, 3)
    return chunked_array[block_index]

  def get_empty_cell_indexes (self):
    indexes = []
    grid = self.grid
    for row in range(len(grid)):
      for cell in range(len(grid[1])):
        if grid[row][cell] == '.':
          indexes.append([row, cell])
    return indexes

  def is_present_in_row (self, row, value):
    grid = self.grid
    row = list(grid[row])
    return bool(row.count(str(value)))

  def is_present_in_column (self, index, value):
    column = self.grid_column(index)
    return bool(column.count(str(value)))

  def is_present_in_block (self, index, value):
    block = self.grid_block(index).flatten().tolist()
    return bool(block.count(str(value)))

  def insert_value (self, index, value):
    self.grid[index[0]][index[1]] = str(value)

  def get_possible_values (self):
    empty_cells = self.get_empty_cell_indexes()
    possible_values = { tuple(index): [] for index in empty_cells }
    for index in empty_cells:
      for possible_value in range (1, 10):
        if not self.is_present_in_block(index, possible_value):
          if not self.is_present_in_row(index[0], possible_value):
            if not self.is_present_in_column(index[1], possible_value):
              possible_values[tuple(index)].append(possible_value)
    return possible_values


def chunk_array (arr, nrows, ncols):
  h = arr.shape[0]
  return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

def read(filename):
  with open(filename) as input_file:
    input_reader = csv.reader(input_file, delimiter=';')
    next(input_reader)
    row = next(input_reader)
    return Puzzle(row[2], row[1], row[0])

def backtrack (puzzle):
  remaining = puzzle.get_empty_cell_indexes()

  if len(remaining) == 0:
    print(puzzle.grid)
    return 1

  index = remaining[0]

  for value in range(1, 10):
    if not puzzle.is_present_in_block(index, value):
      if not puzzle.is_present_in_row(index[0], value):
        if not puzzle.is_present_in_column(index[1], value):
          puzzle.insert_value(index, value)
          if backtrack(puzzle):
            return 1
          else:
            puzzle.insert_value(index, '.')
  return 0


def backTrackFC (puzzle):
  remaining = puzzle.get_empty_cell_indexes()

  if len(remaining) == 0:
    print(puzzle.grid)
    return 1

  possible_values = puzzle.get_possible_values()

  for index in remaining:
    for value in possible_values[tuple(index)]:
      if not puzzle.is_present_in_block(index, value):
        if not puzzle.is_present_in_row(index[0], value):
          if not puzzle.is_present_in_column(index[1], value):
            puzzle.insert_value(index, value)
            if backtrack(puzzle):
              return 1
            else:
              puzzle.insert_value(index, '.')
  return 0




if __name__ == '__main__':
  sample = read('Sudoku.csv')
  start_backtrack = time.time()
  result = backtrack(sample)
  if result:
    end_backtrack = time.time()
    print('backtrack: ', end_backtrack - start_backtrack)

  sample_fc = read('Sudoku.csv')
  start_backtrack_fc = time.time()
  result_fc = backTrackFC(sample_fc)
  if result_fc:
    end_backtrack_fc = time.time()
    print('backtrack fc: ', end_backtrack_fc - start_backtrack_fc)




