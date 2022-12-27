from includes.fraction import Fraction
from includes.inputs import choiceInput as cInput, numericInput
from includes.equation import Equation
from includes.title import title

class PhysicsSolver: #Single-Step
  def __init__(self, name, variables, equations):
    self.name = name
    self.variables = variables
    self.equations = equations
    #Index Equations
    self.keys = {}
    for i in self.equations:
      eq = Equation(self.variables, i[0], i[1])
      self.keys[tuple([str(i) for i in tuple(eq.getVars())])] = eq

  def solve(self):
    title(self.name)
    #Enter as many givens as wanted.
    print('Enter givens.')
    inputs = cInput(self.variables, len(self.variables)-1, numericInput, float, Fraction, ask=True)
    #Enter Unknown
    print('Enter unknown.')
    unknown = list(cInput([i for i in self.variables if i not in inputs], 1, None).keys())[0]
    print('\nG:')
    for key in inputs:
      print(f'--> {key}={inputs[key]}')
  
    print('\nU:')
    print(f'--> {unknown}=?')

    print('\nE:')
    key = [i for i in self.keys if all([j in inputs or j == unknown for j in i])]
    if not key:
      raise Exception(f"No equation to find {unknown}")
    equation = self.keys[key[0]]
    print(f'Equation: {equation}')
    print(f'Rearranging equation in terms of {unknown}.')
    newEquations = equation.rearrange(unknown)
    print(f'Rearranged Equation: {" and ".join([str(i) for i in newEquations])}')
  
    print('\nS:')
    print(f'Substituted Equation: {" and ".join([i.replace(inputs) for i in newEquations])}')
  
    print('\nS:')
    print(inputs)
    answers = [str(i.substitute(inputs)) for i in newEquations]
    print(f'Answer: {" and ".join(answers)}')
    if len(answers) > 1:
      print('One answer may be an extraneous solution.')