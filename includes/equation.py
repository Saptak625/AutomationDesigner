from sympy import var, Eq, solve, Symbol as Sy, Float

class Equation:
  def __init__(self, variables, left, right, verbose={}):
    self.variables = variables #Variables defined for use. Not necessarily present in equation
    var(' '.join(variables))
    self.equation = None
    self.equationLeft = None if verbose is None else left
    self.equationRight = None if verbose is None else right
    self.verbose = verbose
    left = self.equationLeft
    right = self.equationRight
    for key, val in verbose.items():
      left = left.replace(key, val)
      right = right.replace(key, val)
    if isinstance(left, Sy):
      self.equation = Eq(left, right)
    elif isinstance(left, str):
      self.equation = eval(f'Eq({left}, {right})')
    else:
      raise Exception("Please use string or sympy types to instantiate Equation.")

  def fromEq(variables, eq, verboseLeft=None, verboseRight=None, verbose={}):
    lhs = eq.lhs
    if verboseLeft is not None:
      if not isinstance(lhs, Float):
        lhs = verboseLeft
    rhs = eq.rhs
    if verboseRight is not None:
      if not isinstance(rhs, Float):
        rhs = verboseRight
    return Equation(variables, str(lhs), str(rhs), verbose=verbose)
  
  def rearrange(self, variable):
    if self.equation is not None:
      return [Equation(self.variables, Sy(variable), i) for i in solve(self.equation, Sy(variable))]

  def replace(self, dict):
    s = str(self)
    #Replace functions used here
    s = s.replace('sqrt', '&')
    for key in dict:
      s = s.replace(key, str(dict[key]))
    s = s.replace('&', 'sqrt')
    return s

  def substitute(self, dict):
    return Equation.fromEq(self.variables, self.equation.subs([(Sy(key), dict[key]) for key in dict]), verboseLeft=self.equationLeft, verboseRight=self.equationRight, verbose=self.verbose)

  def getVars(self):
    return self.equation.free_symbols
  
  def __str__(self):
    lhs = self.equation.lhs
    if self.equationLeft is not None:
      lhs = self.equationLeft
    rhs = (self.equationRight if self.equationRight is not None else self.equation.rhs) if not isinstance(self.equation.rhs, Float) else float(self.equation.rhs)
    return f'{lhs} = {rhs}'

  def __repr__(self):
    return str(self)