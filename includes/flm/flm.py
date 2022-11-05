from includes.measurement import Measurement
from includes.flm.factor import Factor

class FLM:
  def __init__(self, name, *args):
    self.name = name
    self.factors = tuple(Factor.fromStr(i) for i in args)
    if not self.factors:
      raise Exception("FLM Error: FLM must have at least one factor.")
    self.result = self.factors[0].value
    for i in self.factors[1:]:
      self.result *= i.value

  def __str__(self):
    return self.name + ' = ' + '*'.join([f'({i})' for i in self.factors])  + ' = ' + str(self.result)