from includes.typecheck import typecheck

class Parser:
  def __init__(self, string):
    typecheck(string, str)
    self.string = string
  
  def readByCharacter(self, string, startSetup = None, endSetup = None, checks = None):
    if startSetup:
      startSetup()
    for i, char in enumerate(string):
      if checks:
        checks(i, char)
    if endSetup:
      endSetup()

  def splitString(self, string, checks = None):
    if checks:
      checks(string)
  
  def __str__(self):
    return self.string

  def __repr__(self):
    return str(self)