from includes.parser import Parser
from includes.scripting.logger import Logger

class Scripting(Parser):
    def __init__(self, string, imports = []):
        super().__init__(string)
        self.imports = imports
        self.imports.append('from includes.scripting.logger import log as print')
        self.splitString(self.string, checks = self.split)
        self.output = ''

    def split(self, string):
        self.scripts = [i.strip() for i in string.split('\n')]

    def execute(self):
        Logger.target(self)
        if self.imports:
            for i in self.imports:
                exec(i)
        for i in self.scripts:
            out = exec(i)
            if out is not None:
                self.output += f'{out}\n'

    def __str__(self):
        return f'Script:\n{self.string}' + (f'\n\nOutput:\n{self.output}' if self.output else '')

    def __repr__(self):
        return str(self)
            