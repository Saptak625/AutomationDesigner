from decimal import Decimal, Context

class SigFig:
  def __init__(self, value, sigfigs=None, decimals=None, constant=False):
    self.value = value
    try:
      self.decimalValue = Decimal(value) #True Value of Decimal including extra calculation precision.
    except:
      raise Exception(f'Sig Fig Error: Could not convert "{self.value}" into sig fig.')
    sign, digits, exponent = self.decimalValue.as_tuple()
    self.sigfigs = len(digits)
    self.decimal = Decimal((sign, digits, exponent)) #Sig Fig Decimal Representation
    if constant:
      #Constants are assumed to be perfectly accurate for all calculations.
      self.sigfigs = float('inf')
      self.decimals = float('-inf')
    else:
      #Value has some precision that must be followed.
      #Automatic Override
      if '.' in self.value: #Decimal Value
        #Force override to maintain sig fig precision
        self.decimal = SigFig.changeSigFigs(value, self.sigfigs)
        self.decimals = (exponent + self.sigfigs - 1) if -exponent >= self.sigfigs else exponent
      else:
        newSigfigs = len([int(i) for i in ''.join([str(i) for i in digits]).rstrip('0')])
        if newSigfigs != self.sigfigs and newSigfigs > 0:
          self.decimal = SigFig.changeSigFigs(value, newSigfigs)
          self.sigfigs = newSigfigs
        self.decimals = len(digits) - self.sigfigs
  
      #Manual override for sigfig or decimal precision.
      if sigfigs != None and sigfigs != float("inf"):
        self.sigfigs = sigfigs
        self.decimal = SigFig.changeSigFigs(value, sigfigs)
        sign, digits, exponent = self.decimal.as_tuple()
        if exponent < 0: #Decimal Value
          self.decimals = exponent
        else:
          self.decimals = len(digits) - self.sigfigs
      elif decimals != None:
        self.decimals = decimals
        self.decimal = self.decimal.quantize(Decimal(f"1E{self.decimals}"))
        sign, digits, exponent = self.decimal.as_tuple()
        self.sigfigs = len(digits) - self.decimals + exponent

  def changeSigFigs(value, sigfigs):
    sign, digits, exponent = Context(prec=sigfigs).create_decimal(value).as_tuple()
    if len(digits) < sigfigs:
      missing = sigfigs - len(digits)
      digits = digits + (0,) * missing
      exponent -= missing
    return Decimal((sign, digits, exponent))

  def deepCopy(self):
    new = SigFig('0')
    new.value = self.value
    new.decimalValue = self.decimalValue
    new.decimal = self.decimal
    new.sigfigs = self.sigfigs
    new.decimals = self.decimals
    return new
  
  def __str__(self):
    return str(self.decimal)

  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    return self.value == other.value

  def __lt__(self, other):
    return self.value < other.value

  def __gt__(self, other):
    return self.value > other.value

  def __le__(self, other):
    return self < other or self == other

  def __ge__(self, other):
    return self > other or self == other
  
  def __neg__(self):
    neg = self.deepCopy()
    neg.value = self.value.replace('-', '') if '-' in self.value else f'-{self.value}'
    neg.decimal = -self.decimal
    neg.decimalValue = -self.decimalValue
    return neg

  def __add__(self, other):
    decimals = max(self.decimals, other.decimals)
    return SigFig(str(self.decimalValue + other.decimalValue), decimals=decimals, constant=decimals == float('-inf'))
  
  def __radd__(self, other):
    return self + other
  
  def __sub__(self, other):
    return -other + self

  def __rsub__(self, other):
    return -self + other

  def __mul__(self, other):
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue * other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue / other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rtruediv__(self, other):
    return other / self

  def abs(self):
    if self >= SigFig('0', constant=True):
      return self
    else:
      return -self