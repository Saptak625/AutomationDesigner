from includes.chemistry.chemicalequation import ChemicalEquation

def chemical_equation_solver():
  eq = ChemicalEquation(input('Enter whole equation seperated by "=": '))
  eq.solve()
  print(eq)
  return eq