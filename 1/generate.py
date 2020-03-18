import sys
import csv
import random

def getRandom(n, w, s):
  w_i = random.randrange(0, 10*w/n, 1)
  s_i = random.randrange(0, 10*s/n, 1)
  c_i = random.randrange(0, n, 1)
  return [w_i, s_i, c_i]

def generate(n, w, s, filename):
  n = int(n)
  w = int(w)
  s = int(s)
  with open(filename, "w") as output_file:
    output_writer = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow([n, w, s])
    for _ in range(n):
      output_row = getRandom(n, w, s)
      output_writer.writerow(output_row)

if __name__ == '__main__':
  generate(*sys.argv[1:])

