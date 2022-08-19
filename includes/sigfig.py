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
    print(self.stringValue)
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
    print(self.sigfigs)
    
  def roundToSigFigs(number, sigfigs):
    roundedNumber =  round(number, sigfigs - int(floor(log10(abs(number)))) - 1)
    return SigFig(str(roundedNumber))

  def __str__(self):
    return self.stringValue

  def __repr__(self):
    return self.stringValue