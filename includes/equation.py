from sympy import var, Eq, solve, Symbol as Sy, Float

class Equation:
  def __init__(self, variables, left, right):
    self.variables = variables #Variables defined for use. Not necessarily present in equation
    var(' '.join(variables))
    self.equation = None
    if isinstance(left, Sy):
      self.equation = Eq(left, right)
    elif isinstance(left, str):
      self.equation = eval(f'Eq({left}, {right})')
    else:
      raise Exception("Please use string or sympy types to instantiate Equation.")

  def fromEq(variables, eq):
    return Equation(variables, eq.lhs, eq.rhs)
  
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
    return Equation.fromEq(self.variables, self.equation.subs([(Sy(key), dict[key]) for key in dict]))

  def getVars(self):
    return self.equation.free_symbols
  
  def __str__(self):
    rhs = self.equation.rhs if not isinstance(self.equation.rhs, Float) else float(self.equation.rhs)
    return f'{self.equation.lhs}={rhs}'

  def __repr__(self):
    return str(self)