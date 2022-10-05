from includes.parser import Parser
from includes.chemistry.element import Element
from includes.chemistry.compound import Compound
from includes.matrix import Matrix
from includes.fraction import Fraction
from includes.lcm import lcm

class ChemicalEquation(Parser):
  latexPrint = False

  def setLatexPrint(value):
    ChemicalEquation.latexPrint = value
    Compound.setLatexPrint(value)
    Matrix.setLatexPrint(value)
  
  def __init__(self, equationString):
    super().__init__(equationString)
    self.reactantsString = ""
    self.productsString = ""
    self.reactantCompounds = []
    self.productCompounds = []
    self.matrix = None
    self.coefficients = []
    self.splitString(self.string, checks = self.split)
    reactantsElements = set()
    for c in self.reactantCompounds:
      for e in c.composition:
        if e not in reactantsElements:
          reactantsElements.add(e)
    productsElements = set()
    for c in self.productCompounds:
      for e in c.composition:
        if e not in productsElements:
          productsElements.add(e)
    if reactantsElements != productsElements:
      raise Exception('Chemical Equation Exception: Same elements need to be on both sides of equation.')
    self.elements = {e : i for i, e in enumerate(reactantsElements)}
    matrix = [[Fraction(0, 1) for i in range(len(self.reactantCompounds) + len(self.productCompounds))] for j in range(len(self.elements))]
    for i, c in enumerate(self.reactantCompounds):
      for e in c.composition:
        matrix[self.elements[e]][i] = Fraction(c.composition[e], 1)
    for i, c in enumerate(self.productCompounds):
      for e in c.composition:
        matrix[self.elements[e]][i+len(self.reactantCompounds)] = Fraction(-c.composition[e], 1)
    for row in matrix:
      row[-1] = -row[-1]
    self.matrix = Matrix(matrix)

  def split(self, string):
    if string.count('=') != 1:
      raise Exception('Chemical Equation Exception: Equation needs to have reactant and product side seperated by a "=".')
    self.reactantsString, self.productsString = string.split('=')
    self.reactantCompounds = [Compound(i.strip()) for i in self.reactantsString.split('+')]
    self.productCompounds = [Compound(i.strip()) for i in self.productsString.split('+')]

  def solve(self):
    self.matrix.gaussjordanElimination()
    solutions = [row[-1] for row in self.matrix.matrix if row[-1] != Fraction(0, 1)] + [Fraction(1, 1)]
    multiple = 1
    for s in solutions:
      multiple = lcm(multiple, s.denominator)
    solutions = [(i * Fraction(multiple, 1)).numerator for i in solutions]
    self.coefficients.append(solutions[:len(self.reactantCompounds)])
    self.coefficients.append(solutions[len(self.reactantCompounds):])
    
  def formatSolution(coefficients, compounds, textOverride):
    return " + ".join([(str(coefficients[i]) if coefficients[i] != 1 else "")+compounds[i].__str__(textOverride = textOverride) for i in range(len(compounds))])

  def __str__(self, textOverride = False):
    solution = ChemicalEquation.formatSolution(self.coefficients[0], self.reactantCompounds, textOverride) + " = " + ChemicalEquation.formatSolution(self.coefficients[1], self.productCompounds, textOverride)
    if ChemicalEquation.latexPrint and not textOverride:
      return solution.replace('=', '\\rightarrow')
    return 'Balanced Equation:\n' + solution