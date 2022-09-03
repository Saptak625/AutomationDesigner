class Parser:
  def __init__(self, string):
    self.string = string
  
  def readByCharacter(self, startSetup = None, endSetup = None, checks = None):
    if startSetup:
      startSetup()
    for i, char in enumerate(self.string):
      if checks:
        checks(i, char)
    if endSetup:
      endSetup()

  def __str__(self):
    return self.string

  def __repr__(self):
    return self.string