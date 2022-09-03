from includes.parser import Parser
from includes.chemistry.element import Element

class Compound(Parser):
  def __init__(self, string):
    super().__init__(string);
    self.composition = {}
    self.element = ""
    self.number = ""
    self.parenthesesOn = False
    self.parentheses = ')'
    self.subString = ""
    self.readByCharacter(checks = self.checks, endSetup = self.save)
    self.composition = {Element(i): self.composition[i] for i in self.composition}

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
    if element not in self.composition:
      self.composition[element] = (int(number) if number else 1) * multiple
    else:
      self.composition[element] += (int(number) if number else 1) * multiple

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