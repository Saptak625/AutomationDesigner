from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.equation import Equation
from includes.sigfig import SigFig
from includes.measurement import Measurement
from includes.flm.factor import Factor
from includes.flm.flm import FLM
from includes.chemistry.compound import Compound
from includes.chemistry.element import Element
from includes.chemistry.chemicalequation import ChemicalEquation

from includes.matrix_calculator import matrix_calculator
from includes.physics.physics_solver import physics_solver
from includes.chemistry.chemical_equation_solver import chemical_equation_solver


from autop import AutoP
from packager import Packager

print(Measurement.fromStr('5.50 g H/mol H')*Measurement.fromStr('3.34 mol H'))
# print(Factor.fromStr('(2.0 +- 0.1 m/s) // (1c)').value)
# print(Factor.fromStr('(2.0d m/s) // (0.04 +- 4% kg)'))
# print(FLM('v', '(2.0d g H) // 1c', '(2.0d m/s) // 1c')
# physics_solver()
# e=Equation(['s', 'u', 'v', 'a', 't', 'F', 'm', 'p', 'deltav', 'J', 'W', 'K', 'U', 'g', 'h'], 'v', 'u+a*t')
# print(e)
# equation = e.replace({'u': "M('5.50', U='2')", 'a': "M('1.38', U='2')", 't': "M('5.9', U='1')"})
# exec('from includes.measurement import Measurement as M')
# value=eval('='.join(equation.split('=')[1:]))
# print(value)

# a=Measurement('5.50', uncertainty="2")
# b=Measurement('10.0', uncertainty="1")
# m = a ** 2 
# print(m, a, b)
# s = ((SigFig('3') / SigFig('1.87')) + SigFig('5.87')) * SigFig('3.14', constant=True)
# print(s, s.sigfigs, s.decimals)
# print(-SigFig('6.02E23', constant=True))
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