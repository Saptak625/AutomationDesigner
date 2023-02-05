from includes.scripting.scripting import Scripting

class ChemScripting(Scripting):
    def __init__(self, string, imports = []):
        imports += ['from includes.chemistry.chemicalequation import ChemicalEquation as CE', 'from includes.chemistry.compound import Compound as C', 'from includes.chemistry.element import Element as E', '', 'from includes.chemistry.chemical_equation_solver import chemical_equation_solver', 'from includes.chemistry.limiting_reagent import limiting_reagent', 'from includes.chemistry.stoichiometry import Stoichiometry as S, stoichiometry', '', 'from includes.measurement import Measurement as M']
        super().__init__(string, imports = imports)