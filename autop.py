from os.path import exists
import re

class AutoP:
  def __init__(self, name):
    self.name = name
  
  def new(self):
    if not exists(f'auto/{self.name}.autop'):
      with open(f'auto/{self.name}.autop', 'w') as f:
        f.write('import ${\n\n}$\n\nfunction ${\n\n}$')

  def generate(self):
    program = None
    with open(f'auto/{self.name}.autop', 'r') as f:
      program = f.read()
    matches = re.finditer(r'\$\{(.*?)\}\$', program, re.MULTILINE | re.DOTALL)
    code = [i.group(1)[1:-1] for i in matches]

    generatedCode = ''
    #Imports Section
    for i in code[0].split('\n'):
      filename, imports = i.split(': ')
      generatedCode += f'from includes.{filename} import {imports}\n'

    #Function Section
    generatedCode += f'\ndef {self.name}():\n' + code[1]

    #Generate File
    with open(f'includes/{self.name}.py', 'w') as f:
      f.write(generatedCode)