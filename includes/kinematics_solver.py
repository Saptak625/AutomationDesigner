from includes.fraction import Fraction
from includes.inputs import choiceInput as cInput, numericInput
from includes.equation import Equation

def kinematics_solver():
  print('---------------------------------Kinematics Solver---------------------------------')
  vars = ['s', 'u', 'v', 'a', 't']
  print('Enter givens.')
  inputs = cInput(vars, 3, numericInput, float, Fraction)
  print('Enter unknown.')
  unknown = list(cInput([i for i in vars if i not in inputs], 1, None).keys())[0]

  print('\nG:')
  for key in inputs:
    print(f'--> {key}={inputs[key]}')

  print('\nU:')
  print(f'--> {unknown}=?')

  print('\nE:')
  eqs = {'suat': Equation(vars, 's', 'u*t+(a*t**2)/2'), 'vuat': Equation(vars, 'v', 'u+a*t'), 'vuas': Equation(vars, 'v**2', 'u**2+2*a*s'), 'suvt': Equation(vars, 's', 't*(u+v)/2'), 'savt': Equation(vars, 's', 'v*t-(a*t**2)/2')}
  equation = eqs[[i for i in eqs if all([j in inputs or j == unknown for j in i])][0]]
  print(f'Equation: {equation}')
  print(f'Rearranging equation in terms of {unknown}.')
  newEquations = equation.rearrange(unknown)
  print(f'Rearranged Equation: {" and ".join([str(i) for i in newEquations])}')

  print('\nS:')
  print(f'Substituted Equation: {" and ".join([i.replace(inputs) for i in newEquations])}')

  print('\nS:')
  answers = [str(i.substitute(inputs)) for i in newEquations]
  print(f'Answer: {" and ".join(answers)}')
  if len(answers) > 1:
    print('One answer may be an extraneous solution.')