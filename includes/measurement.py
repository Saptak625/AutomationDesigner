from includes.sigfig import SigFig

class Measurement:
  def __init__(self, sample, precision=None, uncertainty=None, uncertaintyPercent=False, digital=False, analog=False, units=None, P=None, U=None, UP=False, D=False, A=False, UN=None):
    if P is not None:
      precision = P
    if U is not None:
      uncertainty = U
    if UP:
      uncertaintyPercent = UP
    if D:
      digital = D
    if A:
      analog = A
    if UN is not None:
      units = UN
    
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
      self.uncertainty = SigFig(f"5e{self.sample.decimals-1}", decimals=self.sample.decimals-1)
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

    #Determine Units
    #Will use units class to allow for conversions later.
    self.units = units
    self.nUnits = self.units.replace(' ', '').split('*') if self.units is not None else []
    self.dUnits = []
    if self.units is not None:
      if '/' in units:
        nUnitsStr, dUnitsStr = self.units.split('/')
        nUnitsStr = nUnitsStr.strip('() ').replace(' ', '')
        dUnitsStr = dUnitsStr.strip('() ').replace(' ', '')
        self.nUnits = nUnitsStr.split('*')
        self.dUnits = dUnitsStr.split('*')
        if '^' in nUnitsStr:
          newNUnits = []
          for i in self.nUnits:
            if '^' in i:
              i, repeat = i.split('^')
              for n in range(int(repeat)-1):
                newNUnits.append(i)
            newNUnits.append(i)
          self.nUnits = newNUnits
        if '^' in dUnitsStr:
          newDUnits = []
          for i in self.dUnits:
            if '^' in i:
              i, repeat = i.split('^')
              for n in range(int(repeat)-1):
                newDUnits.append(i)
            newDUnits.append(i)
          self.dUnits = newDUnits

  def fromStr(string):
    sample = string.strip()
    uncertainty = None
    units = None
    values = sample.split()
    if '+/-' in sample or '+-' in sample:
      if len(values) == 3:
        if '+/-' in sample:
          sample, uncertainty = string.split('+/-')
        elif '+-' in sample:
          sample, uncertainty = string.split('+-')
      elif len(values) == 4:
        sample, _, uncertainty, units = values
    else:
      if len(values) == 2:
        sample, units = values
    precision = None
    digital = False
    analog = False
    if uncertainty is None:
      if 'c' in sample:
        precision = float('inf')
        sample = sample.replace('c', '')
      elif 'd' in sample:
        digital = True
        sample = sample.replace('d', '')
      elif 'a' in sample:
        analog = True
        sample = sample.replace('a', '')
    return Measurement(sample.strip(), precision=precision, uncertainty=(uncertainty.strip() if isinstance(uncertainty, str) else uncertainty), digital=digital, analog=analog, units=units)
  
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
    return str(self.sample) + (f' +/- {self.uncertainty}' + ('%' if self.uncertaintyPercent else '') if isinstance(self.uncertainty, SigFig) else '') + (f' {self.units}' if self.units is not None else '')

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