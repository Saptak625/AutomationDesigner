from includes.chemistry.chemicalequation import ChemicalEquation
from includes.typecheck import typecheck

def chemical_equation_solver(eq = None):
  typecheck(eq, ChemicalEquation, None)
  if eq == None:
    eq = ChemicalEquation(input('Enter whole equation seperated by "=": '))
  eq.solve()
  print(eq)
  return eq