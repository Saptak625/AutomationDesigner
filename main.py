from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.equation import Equation
from includes.sigfig import SigFig
from includes.chemistry.compound import Compound
from includes.chemistry.element import Element

from includes.matrix_calculator import matrix_calculator
from includes.physics_solver import physics_solver

from autop import AutoP

# physics_solver()
# s=SigFig('423')
# print(s.roundToSigFigs(1))
# matrix_calculator()
# m=Matrix([[1, 0, 5, 6], [9, 0, 2, 0], [18, 0, 4, 0]])
# m.gaussjordanElimination()
# print(m)

print(Compound('[Cr(N2H4CO)6]4[Cr(CN)6]3').composition)
# print(Element('Xe').mass)