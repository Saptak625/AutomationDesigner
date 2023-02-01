from includes.chemistry.compound import Compound
from includes.chemistry.chemicalequation import ChemicalEquation
from includes.typecheck import typecheck, typecheckArray
from includes.measurement import Measurement

class HessLaw:
  latexPrint = False

  def setLatexPrint(value):
    ChemicalEquation.setLatexPrint(value)
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

  def solve(self):
    targetCompounds = ch