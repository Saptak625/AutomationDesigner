from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.equation import Equation
from includes.sigfig2 import SigFig
# from includes.scientificnotation import ScientificNotation as SN
from includes.chemistry.compound import Compound
from includes.chemistry.element import Element
from includes.chemistry.chemicalequation import ChemicalEquation

from includes.matrix_calculator import matrix_calculator
from includes.physics.physics_solver import physics_solver
from includes.chemistry.chemical_equation_solver import chemical_equation_solver


from autop import AutoP
from packager import Packager


# physics_solver()
print((SigFig('200.30') + SigFig('1000')))
print(SigFig('1200.30', decimals=3).sigfigs)
print(-SigFig('6.02E23', constant=True))
# print(SigFig.changeSigFigs("0.02000", 3))
# print(s.roundToSigFigs(1))
# matrix_calculator()
# m=Matrix([[1, 0, 5, 6], [9, 0, 2, 0], [18, 0, 4, 0]])
# m.gaussjordanElimination()
# print(m)

# Compound.setLatexPrint(True)
# print(Compound('3[Cr(N2H4CO)6]4[Cr(CN)6]3 (s)'))
# print(Compound('2H2O').composition)
# print(Element('Xe').mass)

# p=AutoP('chemistry/chemical_node_charts')
# p.new()
# p.generate()
# SN('6.7')

# from includes.chemistry.chemical_node_charts import chemical_node_charts
# print(chemical_node_charts())

# ChemicalEquation.setLatexPrint(True)
# c = ChemicalEquation('H2 + O2 = H2O')
# c.solve()
# print(c)

# print(Compound("Pb2(PO4)3").molePercentComposition())

# chemical_equation_solver()

# Packager('Chemistry Bundle',['includes/chemistry/chemical_equation_solver.py', 'includes/chemistry/chemical_node_charts.py']).package()
# F.setLatexPrint(True)
# print(F(-1, 2))
# Matrix.setLatexPrint(True)
# print(Matrix([[F(1,1), F(2, 1)], [F(3, 1), F(-5,7)], [F(6, 1), F(-10,7)]]))