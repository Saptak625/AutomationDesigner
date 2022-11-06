from includes.measurement import Measurement
from includes.chemistry.chemicalequation import ChemicalEquation
from includes.chemistry.stoichiometry import Stoichiometry
from includes.typecheck import typecheck

def limiting_reagent(eq = None):
  typecheck(eq, ChemicalEquation, None)
  if eq is None:
    eq = ChemicalEquation(input('Enter whole equation seperated by "=": '))
    print()
  s = Stoichiometry(eq) 
  mDict = {i.string: Measurement.fromStr(input(f'Enter Measurement for {i} with units: ')) for i in s.eq.reactantCompounds}
  lr = s.limitingReagent(mDict)
  print('\nInital Stoichiometry:')
  print('\n\n'.join([str(i) for i in lr[0]]))
  print()
  print(lr[1])
  print('\nReactant Stoichiometry:')
  print('\n\n'.join([f'{i[0]}\n{i[1]}\n{i[2]}' for i in lr[2]]))
  print('\n\nProduct Stoichiometry:')
  print('\n\n'.join([str(i) for i in lr[3]]))
  return lr