from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.equation import Equation
from includes.sigfig import SigFig
from includes.chemistry.compound import Compound
from includes.chemistry.element import Element
from includes.chemistry.chemicalequation import ChemicalEquation

from includes.matrix_calculator import matrix_calculator
from includes.physics.physics_solver import physics_solver
from includes.chemistry.chemical_equation_solver import chemical_equation_solver


from autop import AutoP
from packager import Packager

# physics_solver()
# s=SigFig('423')
# print(s.roundToSigFigs(1))
# matrix_calculator()
# m=Matrix([[1, 0, 5, 6], [9, 0, 2, 0], [18, 0, 4, 0]])
# m.gaussjordanElimination()
# print(m)

# print(Compound('3[Cr(N2H4CO)6]4[Cr(CN)6]3 (s)'))
# print(Compound('2H2O').composition)
# print(Element('Xe').mass)

p=AutoP('chemistry/chemical_node_charts')
p.new()
p.generate()

from includes.chemistry.chemical_node_charts import chemical_node_charts
chemical_node_charts()

# c = ChemicalEquation('3NaOH + 1H3PO4 = 1Na3PO4 + 3H2O')
# c.solve()
# print(c)

# chemical_equation_solver()

# Packager('Chemistry Bundle',['includes/chemistry/chemical_equation_solver.py']).package()