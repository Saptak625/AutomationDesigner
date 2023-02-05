from includes.parser import Parser
from includes.scripting.logger import Logger, log

import sys
import traceback

class Scripting(Parser):
    def __init__(self, string, imports = []):
        super().__init__(string)
        self.coreImports = ['from includes.scripting.logger import log as print']
        self.imports = imports
        self.splitString(self.string, checks = self.split)
        self.output = ''

    def split(self, string):
        self.scripts = [i.strip() for i in string.split('\n')]

    def execute(self):
        Logger.target(self)
        if self.coreImports:
            exec('\n'.join(self.coreImports))
        try:
            exec(('\n'.join(self.imports)+'\n\n' if self.imports else '')+self.string)
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            log(''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
        Logger.reset()

    def __str__(self):
        code = ("\n".join(self.imports)+"\n\n" if self.imports else "")+self.string
        return f'Script:\n{code}' + (f'\n\nOutput:\n{self.output}' if self.output else '')

    def __repr__(self):
        return str(self)
            