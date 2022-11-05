from includes.typecheck import typecheck
from includes.measurement import Measurement

class Element:
  latexPrint = False

  def setLatexPrint(value):
    Element.latexPrint = value
  
  def __init__(self, string, protons = None, neutrons = None, mass = None):
    typecheck(string, str)
    typecheck(protons, int, None)
    typecheck(neutrons, int, None)
    typecheck(mass, int, None)
    if not (len(string) > 0 and len(string) <= 2 and string.isalpha()):
      raise Exception("Element Exception: Element Name must be 1 or 2 letters long.")
    self.string = string
    #Protons will only override if element does not exist.
    self.protons = Element.elements().index(self.string) + 1 if self.string in Element.elements() else None
    if self.protons == None:
      self.protons = protons
    self.neutrons = neutrons
    self.mass = mass
    total = (1 if self.protons != None else 0) + (1 if self.neutrons != None else 0) + (1 if self.mass != None else 0)
    if total == 2:
      if self.protons == None:
        self.protons = self.mass - self.neutrons
      elif self.neutrons == None:
        self.neutrons = self.mass - self.protons
      else:
        self.mass = self.protons + self.neutrons

    if self.mass == None:
      self.mass = Measurement.fromStr(f'{Element.atomicWeights()[self.protons]}c') if self.protons in Element.atomicWeights() else None

  def fromAtomicNumber(num):
    if num < 1 or num > 118:
      raise Exception("Element Exception: Atomic Number must be from 1-118.")
    return Element(Element.elements[num-1])

  def elements():
    return ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

  def atomicWeights():
    return {1: '1.01', 2: '4.00', 3: '6.94', 4: '9.01', 5: '10.81', 6: '12.01', 7: '14.01', 8: '16.00', 9: '19.00', 10: '20.18', 11: '22.99', 12: '24.31', 13: '26.98', 14: '28.09', 15: '30.97', 16: '32.07', 17: '35.45', 18: '39.95', 19: '39.1', 20: '40.08', 21: '44.96', 22: '47.87', 23: '50.94', 24: '52.00', 25: '54.94', 26: '55.85', 27: '58.93', 28: '58.69', 29: '63.55', 30: '65.41', 31: '69.72', 32: '72.64', 33: '74.92', 34: '78.96', 35: '79.90', 36: '83.80', 37: '85.47', 38: '87.62', 39: '88.91', 40: '91.22', 41: '92.91', 42: '95.94', 43: '98.00', 44: '101.07', 45: '102.91', 46: '106.42', 47: '107.87', 48: '112.41', 49: '114.82', 50: '118.71', 51: '121.76', 52: '127.6', 53: '126.9', 54: '131.29', 55: '132.91', 56: '137.33', 57: '138.91', 58: '140.12', 59: '140.91', 60: '144.24', 61: '145.0', 62: '150.36', 63: '151.97', 64: '157.25', 65: '158.93', 66: '162.5', 67: '164.93', 68: '167.26', 69: '168.93', 70: '173.04', 71: '174.97', 72: '178.49', 73: '180.95', 74: '183.84', 75: '186.21', 76: '190.23', 77: '192.22', 78: '195.08', 79: '196.97', 80: '200.59', 81: '204.38', 82: '207.2', 83: '208.98', 84: '209.0', 85: '210.00', 86: '222.0', 87: '223.0', 88: '226.0', 89: '227.0', 90: '232.04', 91: '231.04', 92: '238.03', 93: '237.0', 94: '244.0', 95: '243.0', 96: '247.0', 97: '247.0', 98: '251.0', 99: '252.0', 100: '257.0', 101: '258.0', 102: '259.0', 103: '262.0', 104: '261.0', 105: '262.0', 106: '266.00', 107: '264.00', 108: '277.00', 109: '268.0', 110: '269.0', 111: '272.0', 112: '285.00', 113: '286.00', 114: '289.00', 115: '289.00', 116: '293.00', 117: '293.00', 118: '294.00'}
    
  def __str__(self): #Add Latex String for Elements
    return self.string

  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    return self.string == other.string

  def __hash__(self):
    return hash(self.string)