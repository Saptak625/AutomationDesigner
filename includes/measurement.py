from includes.sigfig import SigFig

class Measurement:
  def __init__(self, sample, precision=None, uncertainty=None, uncertaintyPercent=False, digital=False, analog=False, P=None, U=None, UP=False, D=False, A=False):
    if P is not None:
      precision = P
    if U is not None:
      uncertainty = U
    if UP is not False:
      uncertaintyPercent = UP
    if D is not False:
      digital = D
    if A is not False:
      analog = A
    
    if not isinstance(sample, SigFig):
      if '(' in sample or '[' in sample:
        sample, precision = sample.split()
        try:
          precision = int(precision[1:-1]) #Precision in Sig Figs
        except ValueError:
          raise Exception('Measurement Error: Invalid Literal for Sig Fig Precision.')
    if not isinstance(sample, SigFig):
      if precision == float('inf'):
        self.sample = SigFig(sample, constant=True)
      else:
        self.sample = SigFig(sample, sigfigs=precision) 
    else:
      self.sample = sample

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

  def fromStr(string):
    sample = string
    uncertainty = None
    if '+/-' in string:
      sample, uncertainty = string.split('+/-')
    elif '+-' in string:
      sample, uncertainty = string.split('+-')
    return Measurement(sample.strip(), uncertainty=(uncertainty.strip() if isinstance(uncertainty, str) else uncertainty))
  
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
    return Measurement(self.sample.deepCopy(), uncertainty = self.uncertainty.deepCopy() if self.uncertainty is not None else None, uncertaintyPercent = self.uncertaintyPercent)
  
  def __str__(self):
    return str(self.sample) + (f' +/- {self.uncertainty}' + ('%' if self.uncertaintyPercent else '') if isinstance(self.uncertainty, SigFig) else '')

  def __repr__(self):
    return str(self)

  def __neg__(self):
    neg = self.deepCopy()
    neg.sample = -self.sample
    return neg

  def __add__(self, other):
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.absolute(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    return Measurement(self.sample + other.sample, uncertainty=uSum)
  
  def __radd__(self, other):
    return self + other
  
  def __sub__(self, other):
    return -other + self

  def __rsub__(self, other):
    return -self + other

  def __mul__(self, other):
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    return Measurement(self.sample * other.sample, uncertainty=uSum, uncertaintyPercent=True)
  
  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    return Measurement(self.sample / other.sample, uncertainty=uSum, uncertaintyPercent=True)
    
  def __rtruediv__(self, other):
    return other / self

  def __pow__(self, integer):
    product = Measurement('1', precision=float('inf'))
    for i in range(integer):
      product *= self
    return product