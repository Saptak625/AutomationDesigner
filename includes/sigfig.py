from math import floor, log10

class SigFig:
  def __init__(self, stringValue):
    #Check if valid number
    try:
      self.value = float(stringValue)
    except:
      raise Exception(f'Could not convert "{stringValue}" to a float.')
    #String Version of Value
    sign = '-' if '-' in stringValue else ''
    self.stringValue = stringValue.replace('-', '').lstrip('0')
    if self.stringValue[0] == '.':
      self.stringValue = '0'+self.stringValue
    self.unsignedStringValue = self.stringValue
    self.stringValue = sign+self.stringValue
    #Determine number of sig figs for number
    if '.' in self.stringValue:
      if self.stringValue[-1] == '.':
        self.sigfigs = len(self.unsignedStringValue) - 1
      else:
        if self.unsignedStringValue[0] == '0':
          self.sigfigs = len(self.unsignedStringValue.replace('0.', '').lstrip('0'))
        else:
          self.sigfigs = len(self.unsignedStringValue) - 1
    else:
      self.sigfigs = len(self.unsignedStringValue.rstrip('0'))

  def roundToSigFigs(self, sigfigs):
    if self.sigfigs > sigfigs:
      lastDigitBefore = self.stringValue[self.sigfigs - sigfigs]
      if lastDigitBefore != '.':
        if round(float(lastDigitBefore)/10): #Rounds up
          pass
        else: #Round down
          print('hello')
          firstString = self.stringValue[:self.sigfigs - sigfigs - 1]
        #Add 0 and . after getting only front of string.
        return SigFig()
    elif self.sigfigs < sigfigs:
      if '.' in self.stringValue:
        return SigFig(self.stringValue + ('0'*(sigfigs-self.sigfigs)))
      else:
        #Bit broken for numbers like 400 where sig figs are meant to be tens place, but cannot be representated properly.
        return SigFig(self.stringValue + '.' + ('0'*(sigfigs-self.sigfigs+(-1 if self.stringValue[-1] == '0' else 0))))
    return self.deepCopy()

  def deepCopy(self):
    return SigFig(self.stringValue)

  def __eq__(self, other):
    return self.sigfigs == other.sigfigs and self.value == other.value

  def __str__(self):
    return self.stringValue

  def __repr__(self):
    return self.stringValue