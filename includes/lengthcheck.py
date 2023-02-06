def lengthcheck(check, lengthWanted):
  if not len(check) == lengthWanted:
    raise Exception(f'Check length {len(check)} did not match length {lengthWanted}.')

def lengthcheckArray(checkArray, lengthWanted, dimension = 2):
  for check in checkArray:
    if dimension == 2:
      lengthcheck(check, lengthWanted)
    else:
      lengthcheckArray(check, lengthWanted, dimension = dimension - 1)