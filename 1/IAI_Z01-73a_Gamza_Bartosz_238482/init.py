import sys
import csv
import random
import numpy as np

ITERATIONS=10
POP_SIZE=100
TOURNAMENT_SIZE=4
CROSSOVER_RATE=0.6
MUTATION_RATE=0.02

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
      if bool(self.chromosome[index]):
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

class Population:
  def __init__(self, individuals = []):
    self.individuals = individuals

  def add(self, individual):
    self.individuals = np.append(self.individuals, individual)

  def size(self):
    return len(self.individuals)

  def best(self):
    best_individual = None
    best_score = 0
    for individual in self.individuals:
      individual_score = individual.evaluate()
      if individual_score >= best_score:
        best_score = individual_score
        best_individual = individual
    return best_individual

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
  population = Population()
  for _ in range(size):
    chromosome = []
    for _ in range(task.n_items):
      gene = random.randrange(0, 1, 1)
      chromosome.append(gene)
    individual = Individual(task, chromosome)
    population.add(individual)
  return population

def tournament(population, size = TOURNAMENT_SIZE):
  selected_for_battle = random.sample(range(0, population.size()), size)
  winner = None
  best_score = 0
  for index in selected_for_battle:
    player = population.individuals[index]
    player_score = player.evaluate()
    if int(player_score) >= int(best_score):
      best_score = player_score
      winner = player
  return winner

def crossover(parent1, parent2, crossover_rate = CROSSOVER_RATE):
  if random.uniform(0, 1) < crossover_rate:
    cut = int(len(parent1.chromosome) / 2)
    new_chromosome = parent1.chromosome[0:cut] + parent2.chromosome[cut:len(parent2.chromosome)]
    return Individual(parent1.task, new_chromosome)
  else:
    return parent1

def mutate(individual, mutation_rate = MUTATION_RATE):
  new_chromosome = individual.chromosome
  number_of_genes_to_mutate = int(individual.task.n_items * mutation_rate)
  selected_for_mutation = random.sample(range(0, len(new_chromosome)), number_of_genes_to_mutate)
  for index in selected_for_mutation:
    new_chromosome[index] = int(not new_chromosome[index])
  return Individual(individual.task, new_chromosome)


def genetic_algorithm(task, pop_size, iterations, tournament_size, crossover_rate, mutation_rate):
  pop = init_population(task, POP_SIZE)
  i = 0
  while i < iterations:
    j = 0
    new_pop = Population()
    while j < pop_size:
      parent1 = tournament(pop, tournament_size)
      parent2 = tournament(pop, tournament_size)
      child = crossover(parent1, parent2, crossover_rate)
      mutate(child, mutation_rate)
      new_pop.add(child)
      j += 1
    pop = new_pop
    i += 1
  return pop.best().evaluate()

def average(lst):
  return round((sum(lst) / len(lst)))

def crossover_analysis(task):
  values = [0.1, 0.5, 0.8]
  results = []
  for value in values:
    results_per_value = []
    i = 0
    while i < 5:
      result = genetic_algorithm(task, POP_SIZE, ITERATIONS, TOURNAMENT_SIZE, value, MUTATION_RATE)
      results_per_value.append(result)
      i += 1
    results.append(average(results_per_value))
  print("crossover", values, results)

def mutation_analysis(task):
  values = [0.01, 0.1, 0.003]
  results = []
  for value in values:
    results_per_value = []
    i = 0
    while i < 5:
      result = genetic_algorithm(task, POP_SIZE, ITERATIONS, TOURNAMENT_SIZE, CROSSOVER_RATE, value)
      results_per_value.append(result)
      i += 1
    results.append(average(results_per_value))
  print("mutation", values, results)

def tournament_analysis(task):
  values = [2, 10, 50]
  results = []
  for value in values:
    results_per_value = []
    i = 0
    while i < 5:
      result = genetic_algorithm(task, POP_SIZE, ITERATIONS, value, CROSSOVER_RATE, MUTATION_RATE)
      results_per_value.append(result)
      i += 1
    results.append(average(results_per_value))
  print("tournament", values, results)

def population_analysis(task):
  values = [100, 1000, 2000]
  results = []
  for value in values:
    results_per_value = []
    i = 0
    while i < 5:
      result = genetic_algorithm(task, value, ITERATIONS, TOURNAMENT_SIZE, CROSSOVER_RATE, MUTATION_RATE)
      results_per_value.append(result)
      i += 1
    results.append(average(results_per_value))
  print("population", values, results)

if __name__ == '__main__':
  task = read(*sys.argv[1:])

  # default:
  # best = genetic_algorithm(task, POP_SIZE, ITERATIONS, TOURNAMENT_SIZE, CROSSOVER_RATE, MUTATION_RATE)
  # print(best)

  #analysis
  crossover_analysis(task)
  mutation_analysis(task)
  tournament_analysis(task)
  population_analysis(task)



