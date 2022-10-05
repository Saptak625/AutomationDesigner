from includes.typecheck import typecheckArray
from includes.lengthcheck import lengthcheckArray
from includes.fraction import Fraction

class Matrix:
  latexPrint = False

  def setLatexPrint(value):
    Fraction.latexPrint = value
    Matrix.latexPrint = value
  
  def __init__(self, matrix):
    processedMatrix = matrix
    typecheckArray(matrix, Fraction, int, dimension=2)
    if len(matrix):
      lengthcheckArray(matrix, len(matrix[0]))
      if len(matrix[0]):
        #Non-Empty Matrix
        try:
          typecheckArray(matrix, Fraction, dimension=2)
        except:
          #Normalize int elements
          for i in range(len(processedMatrix)):
            for j in range(len(processedMatrix[0])):
              if isinstance(processedMatrix[i][j], int):
                processedMatrix[i][j] = Fraction(processedMatrix[i][j], 1)
    self.matrix = processedMatrix
    self.printWork = False

  def showWork(self):
    self.printWork = True

  def hideWork(self):
    self.printWork = False

  def dimensions(self):
    return (len(self.matrix), len(self.matrix[0]))

  def rowSwap(self, row1, row2):
    temp = self.matrix[row1]
    self.matrix[row1] = self.matrix[row2]
    self.matrix[row2] = temp

  def rowAddition(self, row1, row2):
    self.matrix[row2] = [
      self.matrix[row1][i] + self.matrix[row2][i]
      for i in range(len(self.matrix[row1]))
    ]

  def rowMultiplication(self, scalar, row):
    for i in range(len(self.matrix[row])):
      self.matrix[row][i] = self.matrix[row][i] * scalar

  def gaussianElimination(self):
    if self.isEmpty():
      raise Exception("Matrix Exception: Cannot solve empty matrix.")
    rowIndex = 0
    for columnIndex in range(len(self.matrix[0])):
      nonZero = None
      one = None
      for i in range(rowIndex, len(self.matrix)):
        if nonZero == None and self.matrix[i][columnIndex] != Fraction(
            0, 1):
          nonZero = i
        if one == None and self.matrix[i][columnIndex] == Fraction(
            1, 1):
          one = i
      if nonZero != None:
        if one != None:
          self.rowSwap(rowIndex, one)
        else:
          self.rowMultiplication(
            Fraction.inverse(self.matrix[nonZero][columnIndex]),
            nonZero)
          self.rowSwap(rowIndex, nonZero)
        if self.printWork: print(self)
        for i in range(rowIndex + 1, len(self.matrix)):
          if self.matrix[i][columnIndex] != Fraction(0, 1):
            self.rowMultiplication(-self.matrix[i][columnIndex], rowIndex)
            self.rowAddition(rowIndex, i)
            self.rowMultiplication(Fraction.inverse(self.matrix[rowIndex][columnIndex]), rowIndex)
            if self.printWork: print(self)
        rowIndex += 1
        if rowIndex >= len(self.matrix):
          break

  def gaussjordanElimination(self):
    self.gaussianElimination()
    rowIndex = 0
    for columnIndex in range(len(self.matrix[0])):
      if self.matrix[rowIndex][columnIndex] == Fraction(1, 1):
        for i in range(0, rowIndex):
          if self.matrix[i][columnIndex] != Fraction(0, 1):
            self.rowMultiplication(-self.matrix[i][columnIndex], rowIndex)
            self.rowAddition(rowIndex, i)
            self.rowMultiplication(Fraction.inverse(self.matrix[rowIndex][columnIndex]), rowIndex)
            if self.printWork: print(self)
        rowIndex += 1
        if rowIndex >= len(self.matrix):
          break

  def determinant(self):
    if not self.isSquare():
      raise Exception("Non-square Matrix has no determinant.")
    if len(self.matrix) == 0:
      return 1
    elif len(self.matrix) == 1:
      return self.matrix[0][0]
    elif len(self.matrix) == 2:
      return (self.matrix[0][0] * self.matrix[1][1]) - (
        self.matrix[0][1] * self.matrix[1][0])
    else:
      det = Fraction(0, 1)
      sign = Fraction(1, 1)
      for i in range(len(self.matrix[0])):
        submatrix = [[] for j in range(len(self.matrix) - 1)]
        for j in range(len(self.matrix[0])):
          if j != i:
            for k in range(1, len(self.matrix)):
              submatrix[k - 1].append(self.matrix[k][j])
        det += sign * self.matrix[0][i] * Matrix(
          submatrix).determinant()
        sign = -sign
      return det

  def inverse(matrix):
    if not matrix.isSquare():
      raise Exception("Non-square matrix has no inverse.")
    if not matrix.determinant():
      raise Exception("Singular Matrix has no inverse.")
    matrix.augment(Matrix.identity(len(matrix.matrix)))
    matrix.gaussjordanElimination()
    inverse = matrix.unaugment(rows=len(matrix.matrix))
    return inverse

  def unaugment(self, rows=1):
    other = Matrix([i[-rows:] for i in self.matrix])
    self.matrix = [i[:-rows] for i in self.matrix]
    return other

  def augment(self, other):
    if len(self.matrix) != len(other.matrix):
      raise Exception(
        "Can't augment matrices with different numbers of rows.")
    self.matrix = [
      self.matrix[i] + other.matrix[i] for i in range(len(self.matrix))
    ]

  def identity(size):
    return Matrix([[
      Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(size)
    ] for i in range(size)])

  def isSquare(self):
    return len(self.matrix) == len(self.matrix[0])

  def isEmpty(self):
    if not len(self.matrix):
      return True
    else:
      if not len(self.matrix[0]):
        return True
    return False

  def scale(self, fraction):
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[0])):
        self.matrix[i][j] *= fraction

  def __neg__(self):
    self.scale(Fraction(-1, 1))

  def __add__(matrix1, matrix2):
    if len(matrix1.matrix) != len(matrix2.matrix) or len(
        matrix1.matrix) != len(matrix2.matrix):
      raise Exception("Can't add matrices of different sizes.")
    else:
      return Matrix([[
        matrix1.matrix[i][j] + matrix2.matrix[i][j]
        for j in range(len(matrix1.matrix))
      ] for i in range(len(matrix1.matrix))])

  def __mul__(matrix1, matrix2):
    if len(matrix1.matrix[0]) != len(matrix2.matrix):
      raise Exception("Can't multiply incorrectly sized matrices.")
    product = [[Fraction(0, 1) for i in range(len(matrix2.matrix[0]))]
           for j in range(len(matrix1.matrix))]
    for i in range(len(product)):
      for j in range(len(product[0])):
        res = Fraction(0, 1)
        for k in range(len(matrix2.matrix)):
          res += matrix1.matrix[i][k] * matrix2.matrix[k][j]
        product[i][j] = res
    return Matrix(product)

  def __str__(self):
    if Matrix.latexPrint:
      contents = ' \\\\ '.join([' & '.join([str(j) for j in i]) for i in self.matrix])
      return f'\\begin{{bmatrix}}{contents}\\end{{bmatrix}}'
    return '\n'.join(
      [str(self.matrix[i]) for i in range(len(self.matrix))]) + '\n'

  def __repr__(self):
    return str(self)

  def deepCopy(self):
    return Matrix([[
      self.matrix[i][j].deepCopy() for j in range(len(self.matrix[0]))
    ] for i in range(len(self.matrix))])
