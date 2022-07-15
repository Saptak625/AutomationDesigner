from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.matrix_calculator import matrix_calculator

from autop import AutoP

from sympy import *

# m1=Matrix([[F(1,1) for i in range(5)] for j in range(5)])
# m2=Matrix([[F(1,1) for i in range(5)] for j in range(5)])
# print(m1 + m2)

# m = Matrix([
#   [F.fromInt(3), F.fromInt(1), F.fromInt(-1), F.fromInt(9)],
#   [F.fromInt(2), F.fromInt(-2), F.fromInt(1), F.fromInt(-3)],
#   [F.fromInt(1), F.fromInt(1), F.fromInt(1), F.fromInt(7)]
# ])
# m.gaussjordanElimination()
# print(m)

# m1 = Matrix([[F(3, 1), F(0, 1), F(2, 1)], [F(2, 1), F(0, 1), F(-2, 1)], [F(0, 1), F(1, 1), F(1, 1)]])

# print(numericInput("Enter numeric here: ", float, int, F))

# m1 = Matrix([[F(3, 1), F(0, 1), F(2, 1)], [F(2, 1), F(0, 1), F(-2, 1)], [F(0, 1), F(1, 1), F(1, 1)]])

# a=None
# def store(m1, a):
#   eval(f'{a}=m1')

# # store(m1, 'a')
# exec('m1 * m')
# print(a)
# matrix_calculator()

print(choiceInput(['s', 'u', 'v', 'a', 't'], 3, numericInput, float))