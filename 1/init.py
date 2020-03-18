import sys
import csv
import random
import numpy as np

POP_SIZE=1000
TOUR_SIZE=100

class Task:
  def __init__(self, w, s, c, config):
    self.w_i = w
    self.s_i = s
    self.c_i = c
    self.n_items = int(config[0])
    self.max_weight = int(config[1])
    self.max_size = int(config[2])

class Individual:
  def __init__(self, task, chromosome):
    self.task = task
    self.chromosome = chromosome

  def total_of_parameter(self, parameter):
    total = 0
    for index in range(len(self.chromosome)):
      if self.chromosome[index]:
        total += int(parameter[index])
    return total

  def validate_parameter(self, parameter, limit):
    return self.total_of_parameter(parameter) < limit

  def is_valid(self):
    is_not_overweight = self.validate_parameter(self.task.w_i, self.task.max_weight)
    is_not_oversized = self.validate_parameter(self.task.s_i, self.task.max_size)
    return is_not_oversized and is_not_overweight

  def evaluate(self):
    if(self.is_valid()):
      return self.total_of_parameter(self.task.c_i)
    else:
      return 0

def read(filename):
  w = []
  s = []
  c = []
  with open(filename) as input_file:
    input_reader = csv.reader(input_file)
    config = next(input_reader)
    for row in input_reader:
      w.append(int(row[0]))
      s.append(int(row[1]))
      c.append(int(row[2]))

  return Task(w, s, c, config)

def init_population(task, size):
  population = []
  for _ in range(size):
    chromosome = []
    for _ in range(task.n_items):
      gene = int(random.getrandbits(1))
      chromosome.append(gene)
    individual = Individual(task, chromosome)
    score = individual.evaluate()
    if score > 0:
      print(score, chromosome)
    population.append(individual)
  return population

def tournament(population, size):
  selected_for_battle = random.sample(range(0, len(population)), size)
  print(selected_for_battle)
  winner = None
  best_score = 0
  for index in selected_for_battle:
    player = population[index]
    player_score = player.evaluate()
    print(player_score)
    if int(player_score) > int(best_score):
      best_score = player_score
      winner = player
  return winner



if __name__ == '__main__':
  task = read(*sys.argv[1:])
  population = init_population(task, POP_SIZE)
  winner = tournament(population, TOUR_SIZE)
  print(winner.evaluate())
