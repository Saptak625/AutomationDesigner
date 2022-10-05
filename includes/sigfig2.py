from decimal import Decimal, Context

class SigFig:
  def __init__(self, value, sigfigs=None, decimals=None, constant=False):
    self.value = value
    d = Decimal(value).as_tuple()
    sign, digits, exponent = d
    self.sigfigs = len(digits)
    self.decimal = Decimal((sign, digits, exponent))

    if constant:
      #Constants are assumed to be perfectly accurate for all calculations.
      self.sigfigs = float('inf')
      self.decimals = float('-inf')
    else:
      #Value has some precision that must be followed.
      #Automatic Override
      if exponent < 0: #Decimal Value
        #Force override to maintain sig fig precision
        self.decimal = SigFig.changeSigFigs(value, self.sigfigs)
        self.decimals = (exponent + self.sigfigs - 1) if -exponent >= self.sigfigs else exponent
      else:
        newSigfigs = len([int(i) for i in ''.join([str(i) for i in digits]).rstrip('0')])
        if newSigfigs != self.sigfigs:
          self.decimal = SigFig.changeSigFigs(value, newSigfigs)
          self.sigfigs = newSigfigs
        self.decimals = len(digits) - self.sigfigs
  
      #Manual override for sigfig or decimal precision.
      if sigfigs != None:
        self.sigfigs = sigfigs
        self.decimal = SigFig.changeSigFigs(value, sigfigs)
        if exponent < 0: #Decimal Value
          self.decimals = exponent + self.sigfigs - 1
        else:
          self.decimals = len(digits) - self.sigfigs
      elif decimals != None:
        self.decimals = decimals
        self.decimal = self.decimal.quantize(Decimal(f"1E{self.decimals}"))
        self.sigfigs = len(digits) - self.decimals + exponent

  def changeSigFigs(value, sigfigs):
    sign, digits, exponent = Context(prec=sigfigs).create_decimal(value).as_tuple()
    if len(digits) < sigfigs:
      missing = sigfigs - len(digits)
      digits = digits + (0,) * missing
      exponent -= missing
    return Decimal((sign, digits, exponent))

  def __str__(self):
    return str(self.decimal)

  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    return self.decimal == other.decimal

  def __lt__(self, other):
    return self.decimal < other.decimal

  def __gt__(self, other):
    return self.decimal > other.decimal

  def __le__(self, other):
    return self < other or self == other

  def __ge__(self, other):
    return self > other or self == other
  
  def __add__(self, other):
    print(self.decimal + other.decimal)
    return SigFig(self.decimal + other.decimal, decimals=max(self.decimals, other.decimals))

  def __neg__(self):
    return SigFig(str(-self.decimal), sigfigs = self.sigfigs, constant=(self.sigfigs == float("inf")))