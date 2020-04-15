import StringIO
import numpy as np


class Grid:
    def __init__(self, matrix=[]):
        self.matrix = matrix

    def fillGrid(self, puzzle):
        self.matrix = list(puzzle)


def readGrid(ID):
    # matrix = open("puzzle" + str(ID)).read()
    with open("puzzle" + str(ID), "rt") as infile:

        # lenght = len(infile.readline())
        matrix = np.matrix([list(line.strip()) for line in infile.readlines()])
        # print(matrix.size)
        # print(len(matrix))
        matrixWidth = len(matrix)
        matrixHeight = matrix.size/len(matrix)
        # print matrixHeight

        # print len(matrix)
        grid = Grid(matrix)
        grid.fillGrid(matrix)
        res = np.reshape(grid.matrix, (-1, matrixHeight))

        print res
        return res, matrixWidth, matrixHeight


def readWordList(ID):
    words = []
    wordlist = open("words" + str(ID), "r")
    for word in wordlist:
        words.append(word.strip('\n'))

    print(words)
    return words


def checkHorizontal(row_index, column_index, matrix, currentWord):
    wordLen = len(currentWord)
    for i in range(wordLen):
        if matrix[row_index][column_index + i] == '#' or matrix[row_index][column_index + i] == currentWord[i]:
            matrix[row_index][column_index + i] = currentWord[i]
        else:
            matrix[0][0] = '@'
            return matrix
    return matrix


def checkVerical(row_index, column_index, matrix, currentWord):
    wordLen = len(currentWord)
    for i in range(wordLen):
        if matrix[row_index+i][column_index] == '_' or matrix[row_index+i][column_index] == currentWord[i]:
            matrix[row_index+i][column_index] = currentWord[i]
        else:
            matrix[0][0] = '@'
            return matrix
    return matrix


def solvePuzzle(grid, gridW, gridH, wordlist, index):
    if (index < len(wordlist)):
        currentWord = wordlist[index]
        if (gridH > gridW):
            n = gridH
            maxLen = gridH - len(currentWord)

        else:
            n = gridW
            maxLen = gridW - len(currentWord)
        for i in range(0, n):
            print("1")
            for j in range(0, maxLen):
                print("2")
                temp = checkVerical(j, i, grid, currentWord)
                if (temp[0][0] != '@'):
                    solvePuzzle(grid, gridW, gridH, wordlist, index+1)

        for i in range(gridW):
            for j in range(maxLen):
                temp = checkHorizontal(i, j, grid, currentWord)
                if (temp[0][0] != '@'):
                    solvePuzzle(grid, gridW, gridH, wordlist, index+1)
    else:
        print("RESULT:", grid)


ID = input("Enter puzzle's id ")
wordlist = readWordList(ID)
grid, gridW, gridH = readGrid(ID)
solvePuzzle(grid, gridW, gridH, wordlist, 0)
