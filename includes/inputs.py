from includes.fraction import Fraction
from includes.matrix import Matrix

def stringInput(prompt):
  i = input(prompt)
  print()
  return i

def numericInput(prompt, *args, output = None):
  while True:
    i = input(prompt)
    if not i.replace('.', '').replace('/', '').isnumeric() or i.count('.') > 1 or i.count('/') > 1:
      print('Input was not numeric. Please try again.\n')
    else:
      val = None
      if '/' not in i:
        if float in args:
          val = float(i)
        if int in args:
          if float(i).is_integer():
            val = int(float(i))
      else:
        if '.' not in i:
          if Fraction in args:
            val = Fraction.fromStr(i)
      if val is None:
        print(f'Input did not match types of {args}. Please try again.\n')
      else:
        print()
        if output is Fraction and isinstance(val, int):
          val = Fraction.fromInt(val)
        return val

def menu(prompt, options):
  while True:
    print(prompt)
    for i, opt in enumerate(options):
      print(f'{i+1}: {opt}')
    choice = numericInput('Choice: ', int)
    if choice < 1 or choice > len(options):
      print(f'Please enter choice between 1 and {len(options)}.\n')
    else:
      return choice

def matrixInput():
  print('Enter Size of Matrix')
  columns = numericInput('Columns: ', int, Fraction)
  rows = numericInput('Rows: ', int, Fraction)
  return Matrix([[numericInput(f'Position ({i}, {j})\nElement(Fraction or integer): ', int, Fraction) for j in range(rows)] for i in range(columns)])

def choiceInput(choices, select, inputType, *args):
  print(f'Choose {select} from {", ".join(choices)}.')
  results = {}
  for i in range(select):
    while True:
      s=input("Field Name: ")
      if s not in choices or s in results:
        print("Please choose a field listed above that you have not entered.\n")
      else:
        inArgs = [f'{s}: ']+list(args)
        results[s] = inputType(*inArgs)
        break
  return results