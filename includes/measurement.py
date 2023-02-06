from pymeasurement.sigfig import SigFig

class Measurement:
  """
  Measurement
  A class to represent a SigFig sample with a SigFig uncertainty and corresponding units.
  This class can be used to perform calculations with uncertainty propagation.
  Units are also automatically derived through operations with other measurements.
  """
  def __init__(self, sample, precision=None, uncertainty=None, uncertaintyPercent=False, digital=False, analog=False, units=None, P=None, U=None, UP=False, D=False, A=False, UN=None):
    """
    __init__
    sample: The sample value as a SigFig object or a string.
    precision: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
    uncertainty: The uncertainty of the sample as a SigFig object or a string.
    uncertaintyPercent: If True, the uncertainty will be interpreted as a percentage of the sample value.
    digital: If True, the uncertainty will be automatically determined based on the precision of the device.
    analog: If True, the uncertainty will be automatically determined based on the precision of the device.
    units: The units of the measurement as a string.
    P: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
    U: The uncertainty of the sample as a SigFig object or a string.
    UP: If True, the uncertainty will be interpreted as a percentage of the sample value.
    D: If True, the uncertainty will be automatically determined based on the precision of the device.
    A: If True, the uncertainty will be automatically determined based on the precision of the device.
    UN: The units of the measurement as a string.
    """
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
    if self.uncertainty is not None and self.uncertaintyPercent:
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))

    #Determine Units
    #Will use units class to allow for conversions later.
    self.units = units
    self.nUnits = [i.strip('() ') for i in self.units.split('*')] if self.units is not None else []
    self.dUnits = []
    if self.units is not None:
      if '/' in units:
        nUnitsStr, dUnitsStr = self.units.split('/')
        nUnitsStr = nUnitsStr.strip('() ')
        dUnitsStr = dUnitsStr.strip('() ')
        self.nUnits = [i.strip('() ') for i in nUnitsStr.split('*')]
        self.dUnits = [i.strip('() ') for i in dUnitsStr.split('*')]
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
    newNUnits = self.nUnits
    newDUnits = self.dUnits
    for i in self.nUnits:
      if i in newDUnits:
        newNUnits.remove(i)
        newDUnits.remove(i)
    #Sort units alphabetically
    self.nUnits=sorted(newNUnits)
    self.dUnits=sorted(newDUnits)
    #Reformat units string
    self.units = Measurement.formatUnits(self.nUnits, self.dUnits)

  def fromStr(string):
    """
    Creates a Measurement object from a string.
    The string must be in the form of a number, uncertainty, and units.
    The uncertainty can be in the form of a percentage or a number.
    A 'a' or 'd' can be used to indicate an analog or digital device for automatic uncertainty determination.
    """
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
      elif len(values) >= 4:
        sample, _, uncertainty, *units = values
        if len(units) == 2: # Assuming form will mol H2O
          if '_' not in units[1]:
            from includes.chemistry.compound import Compound
            units[1] = str(Compound(units[1])) # Format Compound String
        units = ' '.join(units)
    else:
      if len(values) >= 2:
        sample, *units = values
        if len(units) == 2: # Assuming form will mol H2O
          if '_' not in units[1]:
            from includes.chemistry.compound import Compound
            units[1] = str(Compound(units[1])) # Format Compound String
        units = ' '.join(units)
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

  def fromFloat(f, units=''): #Assume float is a constant with infinite precision and no uncertainty.
    """
    Creates a Measurement constant from a float.
    """
    return Measurement.fromStr(f'{f}c {units}')
  
  def toAbsolute(self):
    """
    Converts the uncertainty to an absolute value. Note that this mutates the object.
    """
    if self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = False
      self.uncertainty *= (self.sample / SigFig('100', constant=True)).abs()
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), decimals=self.sample.decimals)
    return self

  def toPercent(self):
    """
    Converts the uncertainty to a percentage. Note that this mutates the object.
    """
    if not self.uncertaintyPercent and isinstance(self.uncertainty, SigFig):
      self.uncertaintyPercent = True
      self.uncertainty *= (SigFig('100', constant=True) / self.sample).abs()
      self.uncertainty = SigFig(str(self.uncertainty.decimalValue), sigfigs=(2 if self.uncertainty < SigFig('2', constant=True) else 1))
    return self

  def absolute(m):
    """
    Returns a copy of the Measurement with the uncertainty converted to an absolute value.
    """
    return m.deepCopy().toAbsolute()

  def percent(m):
    """
    Returns a copy of the Measurement with the uncertainty converted to a percentage.
    """
    return m.deepCopy().toPercent()
  
  def deepCopy(self):
    """
    Returns a deep copy of the Measurement object.
    """
    return Measurement(self.sample.deepCopy(), uncertainty = self.uncertainty.deepCopy() if self.uncertainty is not None else None, uncertaintyPercent = self.uncertaintyPercent, units=self.units)
  
  def __str__(self):
    """
    Returns a string representation of the Measurement object.
    """
    return str(self.sample) + (f' +/- {self.uncertainty}' + ('%' if self.uncertaintyPercent else '') if isinstance(self.uncertainty, SigFig) else '') + (f' {Measurement.formatUnits(self.nUnits, self.dUnits)}' if self.units is not None else '')

  def __repr__(self):
    """
    Returns a string representation of the Measurement object.
    """
    return str(self)

  def multUnits(nUnits1, dUnits1, nUnits2, dUnits2):
    """
    Multiplies two sets of units.
    """
    nUnits = nUnits1 + nUnits2
    dUnits = dUnits1 + dUnits2
    newNUnits = nUnits
    newDUnits = dUnits
    for i in nUnits:
      if i in newDUnits:
        newNUnits.remove(i)
        newDUnits.remove(i)
    return (sorted(newNUnits), sorted(newDUnits))

  def formatUnits(nUnits, dUnits):
    """
    Formats a set of units into a string.
    """
    combinedNUnits = sorted([i if nUnits.count(i) == 1 else f'{i}^{nUnits.count(i)}' for i in set(nUnits)])
    combinedDUnits = sorted([i if dUnits.count(i) == 1 else f'{i}^{dUnits.count(i)}' for i in set(dUnits)])
    nUnitsStr = '1' if not nUnits else '*'.join(combinedNUnits)
    dUnitsStr = '' if not dUnits else '*'.join(combinedDUnits)
    if len(combinedNUnits) > 1:
      nUnitsStr = '(' + nUnitsStr + ')'
    if len(combinedDUnits) > 1:
      dUnitsStr = '(' + dUnitsStr + ')'
    return None if nUnitsStr == '1' and dUnitsStr == '' else nUnitsStr + (f'/{dUnitsStr}' if dUnitsStr else '')

  def __eq__(self, other):
    """
    Returns True if the two Measurement objects are equal.
    """
    return self.sample == other.sample

  def __lt__(self, other):
    """
    Returns True if the first Measurement object is less than the second.
    """
    return self.sample < other.sample

  def __gt__(self, other):
    """
    Returns True if the first Measurement object is greater than the second.
    """
    return self.sample > other.sample

  def __le__(self, other):
    """
    Returns True if the first Measurement object is less than or equal to the second.
    """
    return self < other or self == other

  def __ge__(self, other):
    """
    Returns True if the first Measurement object is greater than or equal to the second.
    """
    return self > other or self == other
  
  def __neg__(self):
    """
    Returns the negation of the Measurement object.
    """
    neg = self.deepCopy()
    neg.sample = -self.sample
    return neg

  def __add__(self, other):
    """
    Returns the sum of the two Measurement objects.
    """
    if self.nUnits != other.nUnits or self.dUnits != other.dUnits:
      raise Exception(f'Measurement Error: Cannot add {self} and {other} with different units.')
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.absolute(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    return Measurement(self.sample + other.sample, uncertainty=uSum if uncertainties else None, units=self.units)
  
  def __radd__(self, other):
    """
    Returns the sum of the two Measurement objects.
    """
    return self + other
  
  def __sub__(self, other):
    """
    Returns the difference of the two Measurement objects.
    """
    return -other + self

  def __rsub__(self, other):
    """
    Returns the difference of the two Measurement objects.
    """
    return -self + other

  def __mul__(self, other):
    """
    Returns the product of the two Measurement objects.
    """
    if isinstance(other, float) or isinstance(other, int):
      other = Measurement.fromFloat(other)
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    nUnits, dUnits = Measurement.multUnits(self.nUnits, self.dUnits, other.nUnits, other.dUnits)
    return Measurement(self.sample * other.sample, uncertainty=uSum if uncertainties else None, uncertaintyPercent=True, units=Measurement.formatUnits(nUnits, dUnits))
  
  def __rmul__(self, other):
    """
    Returns the product of the two Measurement objects.
    """
    return self * other

  def __truediv__(self, other):
    """
    Returns the quotient of the two Measurement objects.
    """
    if isinstance(other, float) or isinstance(other, int):
      other = Measurement.fromFloat(other)
    uSum = SigFig('0', constant=True)
    uncertainties = [Measurement.percent(i).uncertainty for i in [self, other] if i.uncertainty is not None]
    for u in uncertainties:
      uSum += u
    nUnits, dUnits = Measurement.multUnits(self.nUnits, self.dUnits, other.dUnits, other.nUnits)
    return Measurement(self.sample / other.sample, uncertainty=uSum if uncertainties else None, uncertaintyPercent=True, units=Measurement.formatUnits(nUnits, dUnits))
    
  def __rtruediv__(self, other):
    """
    Returns the quotient of the two Measurement objects.
    """
    return other / self

  def __pow__(self, integer):
    """
    Returns the Measurement object raised to the given integer power.
    """
    product = Measurement('1', precision=float('inf'))
    for i in range(integer):
      product *= self
    return product

  def sum(measurements):
    """
    Returns the sum of the given list of Measurement objects.
    """
    s = measurements[0]
    for i in measurements[1:]:
      s += i
    return s

  def max(measurements):
    """
    Returns the maximum of the given list of Measurement objects.
    """
    m = measurements[0]
    for i in measurements[1:]:
      if m < i:
        m = i
    return m

  def min(measurements):
    """
    Returns the minimum of the given list of Measurement objects.
    """
    m = measurements[0]
    for i in measurements[1:]:
      if m > i:
        m = i
    return m