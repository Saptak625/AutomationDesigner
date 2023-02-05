from decimal import Decimal, Context

class SigFig:
  """
  SigFig 
  A class for representing numbers with significant figures. SigFig objects are immutable.
  Internally, all numbers are stored as Decimal objects (fixed point numbers) for extra accuracy and precision.
  The central paradigm of this class is that the decimal value is the true value of the number, and the sigfigs and decimals are the precision of the number.
  The sigfigs and decimals are used to determine the precision of the number when it is printed.
  """
  def __init__(self, value, sigfigs=None, decimals=None, constant=False):
    """
    SigFig Constructor
    value: The value of the number as a string.
    sigfigs: The number of significant figures to use when printing the number. If None, the number of significant figures will be automatically determined.
    decimals: The number of decimal places to use when printing the number. If None, the number of decimal places will be automatically determined.
    constant: If True, the number will be assumed to be perfectly accurate for all calculations. If False, the number will be assumed to have some precision that must be followed.
    """
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
        self.decimals = exponent
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
    """
    changeSigFigs
    Changes the number of significant figures of a number.
    value: The value of the number as a string.
    sigfigs: The number of significant figures to use.
    """
    sign, digits, exponent = Context(prec=sigfigs).create_decimal(value).as_tuple()
    if len(digits) < sigfigs:
      missing = sigfigs - len(digits)
      digits = digits + (0,) * missing
      exponent -= missing
    return Decimal((sign, digits, exponent))

  def deepCopy(self):
    """
    deepCopy
    Returns a deep copy of the SigFig object.
    """
    new = SigFig('0')
    new.value = self.value
    new.decimalValue = self.decimalValue
    new.decimal = self.decimal
    new.sigfigs = self.sigfigs
    new.decimals = self.decimals
    return new
  
  def __str__(self):
    """
    __str__
    Returns the string representation of the SigFig object.
    """
    return str(self.decimal)

  def __repr__(self):
    """
    __repr__
    Returns the string representation of the SigFig object.
    """
    return str(self)

  def __eq__(self, other):
    """
    __eq__
    Returns True if the two SigFig objects are equal.
    """
    return self.decimal == other.decimal

  def __lt__(self, other):
    """
    __lt__
    Returns True if the SigFig object is less than the other SigFig object.
    """
    return self.decimal < other.decimal

  def __gt__(self, other):
    """
    __gt__
    Returns True if the SigFig object is greater than the other SigFig object.
    """
    return self.decimal > other.decimal

  def __le__(self, other):
    """
    __le__
    Returns True if the SigFig object is less than or equal to the other SigFig object.
    """
    return self < other or self == other

  def __ge__(self, other):
    """
    __ge__
    Returns True if the SigFig object is greater than or equal to the other SigFig object.
    """
    return self > other or self == other
  
  def __neg__(self):
    """
    __neg__
    Returns the negative of the SigFig object.
    """
    neg = self.deepCopy()
    neg.value = self.value.replace('-', '') if '-' in self.value else f'-{self.value}'
    neg.decimal = -self.decimal
    neg.decimalValue = -self.decimalValue
    return neg

  def __add__(self, other):
    """
    __add__
    Returns the sum of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    decimals = max(self.decimals, other.decimals)
    return SigFig(str(self.decimalValue + other.decimalValue), decimals=decimals, constant=decimals == float('-inf'))
  
  def __radd__(self, other):
    """
    __radd__
    Returns the sum of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    return self + other
  
  def __sub__(self, other):
    """
    __sub__
    Returns the difference of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    return -other + self

  def __rsub__(self, other):
    """
    __rsub__
    Returns the difference of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    return -self + other

  def __mul__(self, other):
    """
    __mul__
    Returns the product of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue * other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rmul__(self, other):
    """
    __rmul__
    Returns the product of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    return self * other

  def __truediv__(self, other):
    """
    __truediv__
    Returns the quotient of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    sigfigs = min(self.sigfigs, other.sigfigs)
    return SigFig(str(self.decimalValue / other.decimalValue), sigfigs=sigfigs, constant=sigfigs == float('inf'))

  def __rtruediv__(self, other):
    """
    __rtruediv__
    Returns the quotient of the two SigFig objects as a new SigFig object, following the rules of significant figures.
    """
    return other / self

  def abs(self):
    """
    abs
    Returns the absolute value of the SigFig object.
    """
    if self >= SigFig('0', constant=True):
      return self
    else:
      return -self