from includes.measurement import Measurement
from includes.chemistry.compound import Compound
from includes.chemistry.chemicalequation import ChemicalEquation
from includes.flm.flm import FLM
from includes.typecheck import typecheck

def stoichiometry(eq = None, s = None, e = None, m = None, eMols = False):
  start = s
  end = e
  measurement = m
  endMols = eMols
  typecheck(eq, ChemicalEquation, None)
  typecheck(start, Compound, None)
  typecheck(end, Compound, None)
  typecheck(measurement, Measurement, None)
  if eq is None:
    eq = ChemicalEquation(input('Enter whole eq seperated by "=": '))
    start = Compound(input('Starting Compound: '))
    end = Compound(input('Ending Compound: '))
    measurement = Compound(input('Ending Compound: '))
  eq.solve()
  if start not in eq.reactantCompounds and start not in eq.productCompounds:
    raise Exception(f'Stoichiometry Error: Compound {start} not in eq {eq}.')
  if end not in eq.reactantCompounds and end not in eq.productCompounds:
    raise Exception(f'Stoichiometry Error: Compound {end} not in eq {eq}.')
  print(eq)
  startsWithMoles = 'mol' in measurement.units
  startCoefficient = None
  if start in eq.reactantCompounds:
    startCoefficient = eq.coefficients[0][eq.reactantCompounds.index(start)]
  else:
    startCoefficient = eq.coefficients[1][eq.productCompounds.index(start)]
  endCoefficient = None
  if end in eq.reactantCompounds:
    endCoefficient = eq.coefficients[0][eq.reactantCompounds.index(end)]
  else:
    endCoefficient = eq.coefficients[1][eq.productCompounds.index(end)]
  factors = tuple([f'({measurement}) // (1c)'] + ([f"(1c mol {start}) // ({start.mass}c g {start})"] if not startsWithMoles else []) + [f"({endCoefficient}c mol {end}) // ({startCoefficient}c mol {start})"] + ([f"({end.mass}c g {end}) // (1c mol {end})"] if not endMols else []))
  flm = FLM(f'Stoichiometry for '+('moles' if endMols else 'grams')+f' of {end}', *factors)
  print()
  print(flm)
  return flm