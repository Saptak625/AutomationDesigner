from includes.typecheck import typecheck
from includes.gcd import gcd
from includes.lcm import lcm

class Fraction:
  latexPrint = False

  def setLatexPrint(value):
    Fraction.latexPrint = value
  
  def __init__(self, numerator, denominator):
    typecheck(numerator, int)
    typecheck(denominator, int)
    self.numerator = numerator
    if denominator == 0:
      raise ZeroDivisionError('Fraction with denominator 0 is undefined.')
    self.denominator = denominator

  def fromInt(intNumerator):
    return Fraction(intNumerator, 1)

  def fromStr(string):
    if '/' not in string:
      return Fraction.fromInt(int(string))
    else:
      splitString = string.split('/')
      return Fraction(int(splitString[0]), int(splitString[1]))
  
  def simplify(self):
    if self.denominator < 0:
      self.numerator *= -1
      self.denominator *= -1
    if self.numerator == 0:
      self.denominator = 1
    else:
      greatestCommonDivisor = gcd(self.numerator, self.denominator)
      self.numerator, self.denominator = self.numerator//greatestCommonDivisor, self.denominator//greatestCommonDivisor

  def simplified(fraction):
    newFraction = fraction.deepCopy()
    newFraction.simplify()
    return newFraction

  def deepCopy(self):
    return Fraction(self.numerator, self.denominator)

  def __eq__(self, other):
    f1 = Fraction.simplified(self)
    f2 = Fraction.simplified(other)
    return f1.numerator == f2.numerator and f1.denominator == f2.denominator

  def __lt__(self, other):
    return float(self) < float(other)

  def __gt__(self, other):
    return float(self) > float(other)

  def __le__(self, other):
    return self < other or self == other

  def __ge__(self, other):
    return self > other or self == other
  
  def __float__(self):
    return self.numerator/self.denominator

  def __str__(self):
    if Fraction.latexPrint:
      sign = "-" if self.numerator < 0 else ""
      unsignedNumerator = abs(self.numerator)
      return f'{sign}\\frac{{{unsignedNumerator}}}{{{self.denominator}}}'
    return f'{self.numerator}/{self.denominator}'

  def __repr__(self):
    return str(self)

  def __neg__(self):
    newFraction = self.deepCopy()
    newFraction.numerator = -newFraction.numerator
    return newFraction

  def __add__(self, other):
    if isinstance(other, int) or isinstance(other, float):
      return float(self) + other
    elif isinstance(other, Fraction):
      leastCommonFactor = lcm(self.denominator, other.denominator)
      f1 = Fraction.scaled(self, leastCommonFactor//self.denominator)
      f2 = Fraction.scaled(other, leastCommonFactor//other.denominator)
      return Fraction.simplified(Fraction(f1.numerator + f2.numerator, leastCommonFactor))
    else:
      raise Exception(f"Can't add {type(self)} and {type(other)}.")

  def __radd__(self, other):
    return self + other
  
  def __sub__(self, other):
    return -other + self

  def __rsub__(self, other):
    return -self + other

  def __mul__(self, other):
    if isinstance(other, int) or isinstance(other, float):
      return float(self) * other
    elif isinstance(other, Fraction):
      return Fraction.simplified(Fraction(self.numerator * other.numerator, self.denominator * other.denominator))
    else:
      raise Exception(f"Can't multiply {type(self)} and {type(other)}.")

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    return self * Fraction.inverse(other)

  def __rtruediv__(self, other):
    return other * Fraction.inverse(self)
  
  def inverse(fraction):
    if isinstance(fraction, int) or isinstance(fraction, float):
      return 1 / float(fraction)
    elif isinstance(fraction, Fraction):
      return Fraction.simplified(Fraction(fraction.denominator, fraction.numerator))
    else:
      raise Exception(f"Fraction Inverse of type {type(fraction)} is non-numeric.")

  def scale(self, factor):
    typecheck(factor, int)
    self.numerator *= factor
    self.denominator *= factor

  def scaled(fraction, factor):
    newFraction = fraction.deepCopy()
    newFraction.scale(factor)
    return newFraction