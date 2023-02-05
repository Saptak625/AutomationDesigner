from includes.chemistry.chemicalequation import ChemicalEquation
from includes.typecheck import typecheck
from includes.scripting.logger import log as print

def chemical_equation_solver(eq = None):
  typecheck(eq, ChemicalEquation, str, None)
  if isinstance(eq, str):
    eq = ChemicalEquation(eq)
  if eq == None:
    eq = ChemicalEquation(input('Enter whole equation seperated by "=": '))
  eq.solve()
  print(eq)
  return eq