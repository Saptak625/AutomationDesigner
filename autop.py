import os
from os.path import exists
import re

class AutoP:
  def __init__(self, name):
    self.name = name
  
  def new(self):
    directory = 'auto/'+'/'.join(self.name.split('/')[:-1])
    if not os.path.exists(directory):
      os.makedirs(directory)
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
      if ': ' in i:
        filename, imports = i.split(': ')
        generatedCode += f'from includes.{filename} import {imports}\n'

    #Function Section
    functionName = self.name.split('/')[-1]
    generatedCode += f'\ndef {functionName}():\n' + code[1]

    #Generate File
    directory = 'includes/'+'/'.join(self.name.split('/')[:-1])
    if not os.path.exists(directory):
      os.makedirs(directory)
    with open(f'includes/{self.name}.py', 'w') as f:
      f.write(generatedCode)