from includes.measurement import Measurement
from includes.flm.factor import Factor

class FLM:
  def __init__(self, name, factor_list):
    self.name = name
    self.factor_list = factor_list
    self.value