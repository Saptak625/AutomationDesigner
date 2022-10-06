from includes.sigfig import SigFig

class Measurement:
  def __init__(self, sample, precision=None, uncertainty=None, uncertaintyPercent=False, digital=False, analog=False):
    if not isinstance(sample, SigFig):
      if '(' in sample or '[' in sample:
        sample, precision = sample.split()
        try:
          precision = int(precision[1:-1]) #Precision in Sig Figs
        except ValueError:
          raise Exception('Measurement Error: Invalid Literal for Sig Fig Precision.')
    self.sample = SigFig(sample, sigfigs=precision) if not isinstance(sample, SigFig) else sample

    #Automatic Determination of Uncertainty based on Device
    self.uncertainty = None
    if analog:
      self.uncertainty = SigFig(f"5e{self.sample.decimals}", decimals=self.sample.decimals)
    elif digital:
      self.uncertainty = SigFig(f"1e{self.sample.decimals}", decimals=self.sample.decimals)
    
    #Main Override
    if uncertainty is not None:
      if not isinstance(uncertainty, SigFig):
        if '%' in uncertainty:
          uncertaintyPercent = True
          uncertainty = uncertainty.replace('%', '')
      self.uncertainty = SigFig(uncertainty, decimals=self.sample.decimals) if not isinstance(uncertainty, SigFig) else uncertainty
    self.uncertaintyPercent = uncertaintyPercent

    #Chemistry Percent Rules(if <2%, 2 sig figs. Else 1 sig fig)
    if self.uncertaintyPercent:
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))

  def toAbsolute(self):
    if self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = False
      self.uncertainty *= (self.sample / SigFig('100', constant=True)).abs()
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), decimals=self.sample.decimals)
    return self

  def toPercent(self):
    if not self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = True
      self.uncertainty *= (SigFig('100', constant=True) / self.sample).abs()
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))
    return self

  def absolute(m):
    return m.deepCopy().toAbsolute()

  def percent(m):
    return m.deepCopy().toPercent()
  
  def deepCopy(self):
    return Measurement(self.sample.deepCopy(), uncertainty = self.uncertainty.deepCopy(), uncertaintyPercent = self.uncertaintyPercent)
  
  def __str__(self):
    return str(self.sample) + (f' +/- {self.uncertainty}' + ('%' if self.uncertaintyPercent else '') if isinstance(self.uncertainty, SigFig) else '')

  def __repr__(self):
    return str(self)

  def __neg__(self):
    neg = self.deepCopy()
    neg.sample = -self.sample
    return neg

  def __add__(self, other):
    return Measurement(self.sample + other.sample, uncertainty=Measurement.absolute(self).uncertainty + Measurement.absolute(other).uncertainty)
  
  def __radd__(self, other):
    return self + other
  
  def __sub__(self, other):
    return -other + self

  def __rsub__(self, other):
    return -self + other

  def __mul__(self, other):
    return SigFig(self.decimalValue * other.decimalValue, sigfigs=min(self.sigfigs, other.sigfigs))

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    return SigFig(self.decimalValue / other.decimalValue, sigfigs=min(self.sigfigs, other.sigfigs))

  def __rtruediv__(self, other):
    return other / self