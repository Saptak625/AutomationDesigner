from includes.chemistry.compound import Compound
from includes.chemistry.chemicalequation import ChemicalEquation
from includes.typecheck import typecheck, typecheckArray
from includes.measurement import Measurement
from includes.matrix import Matrix

class HessLaw:
  latexPrint = False

  def setLatexPrint(value):
    ChemicalEquation.setLatexPrint(value)
    Matrix.setLatexPrint(value)
    HessLaw.latexPrint = value

  def __init__(self, eqs, enthalpies, targetEq):
    typecheckArray(eqs, ChemicalEquation)
    typecheckArray(enthalpies, Measurement, float, int)
    typecheck(targetEq, ChemicalEquation)
    self.eqs = eqs
    self.enthalpies = enthalpies
    self.targetEq = targetEq
    for eq in self.eqs:
      eq.solve()
    self.targetEq.solve()
    targetCompounds = (self.targetEq.reactantCompounds + self.targetEq.productCompounds)[:len(self.eqs)]
    targetCoefficients = (self.targetEq.coefficients[0] + [-i for i in self.targetEq.coefficients[1]])[:len(self.eqs)]
    matrixList = []
    for ind, c in enumerate(targetCompounds):
      eqRelation = []
      for eq in self.eqs:
        coefficient = 0
        for index, i in enumerate(eq.reactantCompounds):
          if c == i:
            coefficient += eq.coefficients[0][index]
        for index, i in enumerate(eq.productCompounds):
          if c == i:
            coefficient -= eq.coefficients[1][index]
        eqRelation.append(coefficient)
      eqRelation.append(targetCoefficients[ind])
      matrixList.append(eqRelation)
    self.matrix = Matrix(matrixList)
    self.coefficients = []
    self.enthalpyChange = None

  def solve(self):
    self.matrix.gaussjordanElimination()
    self.coefficients = [row[-1] for row in self.matrix.matrix]
    self.enthalpyChange = Measurement.sum([i*self.enthalpies[ind] for ind, i in enumerate(self.coefficients)])    

  def __str__(self, textOverride = False):
    out = ''
    for i, eq in enumerate(self.eqs):
        out += f'    {self.coefficients[i]} x ( {eq}  H_change={self.enthalpies[i]} )\n'
    out += '-----------------------------------------------------------------------------\n'
    out += f'   {self.targetEq}  H_change={self.enthalpyChange}'
    return "Hess's Law:\n" + out