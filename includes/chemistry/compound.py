from includes.parser import Parser
from includes.chemistry.element import Element
from includes.measurement import Measurement
import re

class Compound(Parser):
  latexPrint = False

  def setLatexPrint(value):
    Compound.latexPrint = value
    Element.setLatexPrint(value)
  
  def __init__(self, string):
    super().__init__(string)
    self.composition = {}
    self.element = ""
    self.number = ""
    self.parenthesesOn = False
    self.parentheses = ')'
    self.subString = ""
    self.compoundString = self.string
    self.stateString = ""
    self.splitString(self.string, checks = self.split)
    for i in range(len(self.compoundString)):
      if not self.compoundString[i].isdigit():
        self.compoundString = self.compoundString[i:].strip()
        break
    self.readByCharacter(self.compoundString, checks = self.checks, endSetup = self.save)
    self.mass = Measurement.fromStr('0c')
    for e in self.composition:
      self.mass += (e.mass * Measurement(str(self.composition[e]), precision=float('inf')))
  
  def split(self, string):
    if '(s)' in string or '(l)' in string or '(g)' in string or '(aq)' in string:
      if '(s)' in string:
        self.stateString = '(s)'
      elif '(l)' in string:
        self.stateString = '(l)'
      elif '(g)' in string:
        self.stateString = '(g)'
      else:
        self.stateString = '(aq)'
      self.compoundString = self.string.replace(self.stateString, '').strip()
  
  def checks(self, i, char):
    if char.isalpha():
      if self.parenthesesOn:
          self.subString += char
      else:
        if char.isupper():
          self.save()
          self.element += char
        else:
          self.element += char
    elif char.isdigit():
      if self.parenthesesOn:
        self.subString += char
      else:
        self.number += char
    else:
      if char == '(' or char == '[':
        if not self.parenthesesOn:
          self.save()
          self.parenthesesOn = True
          self.parentheses = ')' if char == '(' else ']'
        else:
          self.subString += char
      elif char == ')' or char == ']':
        if char == self.parentheses:
          self.parenthesesOn = False
        else:
          self.subString += char
      else:
        raise Exception(f"Compound Parser Exception: Unknown character '{char}'")

  def saveElement(self, element, number, multiple = 1):
    if Element(element) not in self.composition:
      self.composition[Element(element)] = (int(number) if number else 1) * multiple
    else:
      self.composition[Element(element)] += (int(number) if number else 1) * multiple

  def saveSubcompound(self):
    subCompound = Compound(self.subString)
    for element in subCompound.composition:
      self.saveElement(element.string, self.number, multiple = subCompound.composition[element])

  def save(self):
    if self.element or self.subString:
      if self.element:
        self.saveElement(self.element, self.number)
      if self.subString:
        self.saveSubcompound()
    self.element = ""
    self.number = ""
    self.subString = ""

  def __str__(self, textOverride = False):
    if Compound.latexPrint and not textOverride:
      allCoefficients = re.findall("\d+", self.compoundString)
      finalString = ''
      currentIndex = 0
      for i in allCoefficients:
        ind = self.compoundString[currentIndex:].index(i)
        finalString += self.compoundString[currentIndex:currentIndex + ind]+f'_{{{i}}}'
        currentIndex = currentIndex + ind + len(i)
      if currentIndex < len(self.compoundString):
        finalString += self.compoundString[currentIndex:]
      return finalString + (self.stateString if self.stateString else '')
    return self.compoundString + (self.stateString if self.stateString else '')

  def __eq__(self, other):
    return self.composition == other.composition

  def __ne__(self, other):
    return self.composition != other.composition
  
  def massPercentComposition(self):
    return [['Element', 'Mass']]+[[str(i), self.composition[i]*i.mass] for i in self.composition]

  def molePercentComposition(self):
    return [['Element', 'Moles']]+[[str(i), self.composition[i]] for i in self.composition]