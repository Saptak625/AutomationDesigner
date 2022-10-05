def typecheck(check, *args):
  if not any([isinstance(check, a) for a in args if a is not None]) and (None in args and check is not None):
    raise TypeError(f'Check type "{type(check)}" did not match type "{args}."')

def typecheckArray(checkArray, *args, dimension = 1):
  for check in checkArray:
    if dimension == 1:
      typecheck(check, args)
    else:
      typecheckArray(check, args, dimension = dimension - 1)