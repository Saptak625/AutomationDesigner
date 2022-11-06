from includes.measurement import Measurement
from includes.equation import Equation
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
    eq = ChemicalEquation(input('Enter whole equation seperated by "=": '))
    start = Compound(input('Starting Compound: '))
    end = Compound(input('Ending Compound: '))
    measurement = Compound(input('Ending Compound: '))
  s = Stoichiometry(eq)
  print(s.eq)
  flm = s.stoichiometry(start, end, measurement, endMols = endMols)
  print()
  print(flm)
  return flm

class Stoichiometry:
  def __init__(self, eq):
    typecheck(eq, ChemicalEquation)
    self.eq = eq
    self.eq.solve()

  def stoichiometry(self, start, end, measurement, endMols = False, title=None):
    if start not in self.eq.reactantCompounds and start not in self.eq.productCompounds:
      raise Exception(f'Stoichiometry Error: Compound {start} not in equation {self.eq}.')
    if end not in self.eq.reactantCompounds and end not in self.eq.productCompounds:
      raise Exception(f'Stoichiometry Error: Compound {end} not in equation {self.eq}.')
    startsWithMoles = 'mol' in measurement.units
    startCoefficient = None
    if start in self.eq.reactantCompounds:
      startCoefficient = self.eq.coefficients[0][self.eq.reactantCompounds.index(start)]
    else:
      startCoefficient = self.eq.coefficients[1][self.eq.productCompounds.index(start)]
    endCoefficient = None
    if end in self.eq.reactantCompounds:
      endCoefficient = self.eq.coefficients[0][self.eq.reactantCompounds.index(end)]
    else:
      endCoefficient = self.eq.coefficients[1][self.eq.productCompounds.index(end)]
    factors = tuple([f'({measurement}) // (1c)'] + ([f"(1c mol {start}) // ({start.mass}c g {start})"] if not startsWithMoles else []) + [f"({endCoefficient}c mol {end}) // ({startCoefficient}c mol {start})"] + ([f"({end.mass}c g {end}) // (1c mol {end})"] if not endMols else []))
    flm = FLM(f'Stoichiometry for '+('moles' if endMols else 'grams')+f' of {end}' if title is None else title, *factors)
    return flm

  def limitingReagent(self, mDict):
    if not all(i.string in mDict for i in self.eq.reactantCompounds):
      raise Exception('Stoichiometry Error: Limiting Reagent requires Measurements for each reagent.')
    for key, val in mDict.items():
      typecheck(val, Measurement)
    measurements = [mDict[i.string] for i in self.eq.reactantCompounds]

    #Reagents
    reagentFLMs = [self.stoichiometry(self.eq.reactantCompounds[i], self.eq.reactantCompounds[0], measurements[i], endMols = True, title = f"{self.eq.reactantCompounds[i]} to {self.eq.reactantCompounds[0]}") for i in range(len(self.eq.reactantCompounds))]
    minMeasurement = sorted(reagentFLMs, key=lambda x: x.result)[0].result
    limitingReagentIndex = [i.result for i in reagentFLMs].index(minMeasurement)
    limitingReagent = self.eq.reactantCompounds[limitingReagentIndex]

    #Excess Reactants
    reactantCalcs = []
    for c in self.eq.reactantCompounds:
      if c != limitingReagent:
        s = self.stoichiometry(self.eq.reactantCompounds[0], c, minMeasurement)
        e = Equation(['r', 'a', 'e'], f'Excess {c}', 'Amount Provided - Amount Expected', verbose={f'Excess {c}': 'r', 'Amount Provided': 'a', 'Amount Expected': 'e'})
        actual = mDict[c.string] * Measurement.fromStr(f'{c.mass} g {c}/mol {c}') if 'mol' in mDict[c.string].units else mDict[c.string]
        ans = e.substitute({'a': f'M.fromStr("{actual}")', 'e': f'M.fromStr("{s.result}")'})
        reactantCalcs.append((s, e, ans))

    #Products
    productFLMs = [self.stoichiometry(self.eq.reactantCompounds[0], c, minMeasurement) for c in self.eq.productCompounds]
    return (reagentFLMs, f'Limiting Reagent is {limitingReagent}.', reactantCalcs, productFLMs)