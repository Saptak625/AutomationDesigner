from includes.measurement import Measurement

class Factor:
  def __init__(self, numeratorM, denominatorM=Measurement('1', precision=float('inf'))):
    #Measurements
    self.numeratorM = numeratorM
    self.denominatorM = denominatorM
    print('Factor', self.numeratorM.sample.sigfigs, self.denominatorM.sample.sigfigs)
    self.value = numeratorM / denominatorM
    print('Value', self.value.sample.sigfigs)

  def fromStr(string):
    try:
      numerator, denominator = string.split('//')          
    except ValueError:
      raise Exception("FLM Factor Error: Factor must have Numerator and Denominator.")
    return Factor(Measurement.fromStr(numerator.strip('() ')), Measurement.fromStr(denominator.strip('() ')))
      
  def __str__(self):
    return f'({self.numeratorM})/({self.denominatorM})'

  def __repr__(self):
    return str(self)