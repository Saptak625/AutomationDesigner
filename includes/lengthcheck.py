def lengthcheck(check, lengthWanted):
  if not len(check) == lengthWanted:
    raise Exception(f'Check length {len(check)} did not match length {lengthWanted}.')

def lengthcheckArray(checkArray, elementTypeWanted, dimension = 2):
  for check in checkArray:
    if dimension == 2:
      lengthcheck(check, elementTypeWanted)
    else:
      lengthcheckArray(check, elementTypeWanted, dimension = dimension - 1)