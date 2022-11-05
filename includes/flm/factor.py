from includes.measurement import Measurement

class Factor:
  def __init__(self, numeratorM, denominatorM=Measurement('1', precision=float('inf')), numeratorU="", denominatorU=""):
    #Measurements
    self.numeratorM = numeratorM
    self.denominatorM = denominatorM
    #Units
    self.numeratorU = numeratorU
    self.denominatorU = denominatorU
    self.value = numeratorM / denominatorM

  def fromStr(string):
    try:
      numerator, denominator = string.split('//')

      numeratorSplit = numerator.strip('() ').split()
      numeratorM = numeratorSplit[0]
      numeratorU = ' '.join(numeratorSplit[1:])
      if '+/-' in numerator or '+-' in numerator:
        numeratorM = ' '.join(numeratorSplit[0:3])
        numeratorU = ' '.join(numeratorSplit[3:]) 
        
      denominatorSplit = denominator.strip('() ').split()
      denominatorM = denominatorSplit[0]
      denominatorU = ' '.join(denominatorSplit[1:])
      if '+/-' in numerator or '+-' in numerator:
        denominatorM = ' '.join(denominatorSplit[0:3])
        denominatorU = ' '.join(denominatorSplit[3:])            
    except ValueError:
      raise Exception("FLM Factor Error: Factor must have Numerator and Denominator.")
    return Factor(Measurement.fromStr(numeratorM), Measurement.fromStr(denominatorM), numeratorU, denominatorU)
      
  def __str__(self):
    numerator = str(self.numeratorM) + ('' if self.numeratorU=="" else f' {self.numeratorU}')
    denominator = str(self.denominatorM) + ('' if self.denominatorU=="" else f' {self.denominatorU}')
    return f'({numerator})/({denominator})'

  def __repr__(self):
    return str(self)