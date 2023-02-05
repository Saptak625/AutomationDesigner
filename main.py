from includes.matrix import Matrix
from includes.fraction import Fraction as F
from includes.inputs import numericInput, choiceInput
from includes.equation import Equation
from includes.sigfig import SigFig
from includes.measurement import Measurement
from includes.scripting.scripting import Scripting
from includes.flm.factor import Factor
from includes.flm.flm import FLM
from includes.chemistry.compound import Compound
from includes.chemistry.element import Element
from includes.chemistry.chemicalequation import ChemicalEquation
from includes.chemistry.thermodynamics.hesslaw import HessLaw
from includes.chemistry.chemscripting import ChemScripting

from includes.matrix_calculator import matrix_calculator
from includes.physics.physics_solver import physics_solver
from includes.chemistry.chemical_equation_solver import chemical_equation_solver
from includes.chemistry.stoichiometry import Stoichiometry, stoichiometry
from includes.chemistry.limiting_reagent import limiting_reagent

from includes.scripting.logger import Logger, log as print


from autop import AutoP
from packager import Packager

import pandas as pd


# Measurement Testing
# deltaT = Measurement.fromStr('0.55 +/- 0.01 degC')
# m = Measurement.fromStr('3.42 g H2O')
# c = Measurement.fromStr('4.18c J/(g H2O * degC)')
# conv = Measurement.fromStr('0.0001c kJ/J')
# q = deltaT * m * c * conv
# print(q)

m = Measurement.fromStr('1.22d kg')
p = Measurement.fromStr('2.35a kg * m/s')
ke = p**2 / (m * 2)
print(ke)

# ce = chemical_equation_solver('H2O = H2 + O2')
# hl = HessLaw([ChemicalEquation('H2+F2=2HF'), ChemicalEquation('C+2F2=CF4'), ChemicalEquation('2C+2H2=C2H4')], [Measurement.fromStr('-537 kJ/mol'), Measurement.fromStr('-680 kJ/mol'), Measurement.fromStr('52.3 kJ/mol')], ChemicalEquation('C2H4+6F2=2CF4+4HF'))
# hl.solve()
# print(hl)

# tempChange = Measurement.fromStr('11.6d')
# mass = Measurement.fromStr('2.016d')
# q = tempChange * Measurement.fromStr('100.0a') * Measurement.fromStr('4.18')
# moles = mass / Compound('NaOH').mass

# h = -q/moles

# print('Q',q)
# print('moles', moles)
# print('H', h)

# df = pd.DataFrame()

# df['m_water'] = [Measurement.fromStr('78.701d'), Measurement.fromStr('78.701d')]
# df['init_m'] = [Measurement.fromStr('110.759d'), Measurement.fromStr('110.759d')] 
# df['end_m'] = [Measurement.fromStr('109.689d'), Measurement.fromStr('109.689d')] 
# df['init_t'] = [Measurement.fromStr('21.7d'), Measurement.fromStr('21.7d')]
# df['end_t'] = [Measurement.fromStr('70.9d'), Measurement.fromStr('70.9d')]
# df['molar'] = [Measurement.fromStr('46.08c'), Measurement.fromStr('46.08c')]

# df['q'] = df['m_water'] * Measurement.fromStr('4.18c') * (df['end_t']-df['init_t'])
# df['m_alcohol'] = df['init_m'] - df['end_m']
# df['mol_alcohol'] = df['m_alcohol'] / df['molar']
# df['enthalpy'] = -df['q'] / df['mol_alcohol']
# print(q, m_alcohol, mol_alcohol, enthalpy, sep='\n')
# print(df.head())

# with open('script.txt', 'r') as f:
#   code = f.read()
#   s=Scripting(code)
#   s.execute()
#   print(s)

# a = Measurement.fromStr('3 +- 2% mol H2O')
# stoichiometry(ChemicalEquation('H2O = H2 + O2'), Compound('H2O'), Compound('O2'), a)

# Stoichiometry.setLatexPrint(True)

# s = Stoichiometry(ChemicalEquation('CO2 + H2O = C6H12O6 + O2'))
# flms = s.limitingReagent({'CO2': Measurement.fromStr('37d g CO2'), 'H2O': Measurement.fromStr('13.2d g H2O')})
# print(flms)
# print('\n\n'.join([str(i) for i in flms[0]]))
# print(Measurement.fromStr('5.50 g H/mol H')*Measurement.fromStr('3.34 mol H'))
# print(Factor.fromStr('(2.0 +- 0.1 m/s) // (1c)').value)
# print(Factor.fromStr('(2.0d m/s) // (0.04 +- 4% kg)'))
# print(FLM('Stoichiometry for H2O', '143.4d g O2 // 1c', '1 mol O2 // 32.00 g O2', '2 mol H2O // 1 mol O2', '18.02 g H2O // 1 mol H2O'))
# print(FLM.fromStr('Stoichiometry for H2O = 143.4d g O2 // 1c * 1 mol O2 // 32.00 g O2 * 2 mol H2O // 1 mol O2 * 18.02 g H2O // 1 mol H2O'))
# Equation.latexPrint = True
# physics_solver()
# e=Equation(['s', 'u', 'v', 'a', 't', 'F', 'm', 'p', 'deltav', 'J', 'W', 'K', 'U', 'g', 'h'], 'v', 'u+a*t')
# e=Equation(['r', 'a', 'e'], 'Excess', 'Amount Provided - Amount Expected', verbose={'Excess': 'r', 'Amount Provided': 'a', 'Amount Expected': 'e'})
# print(e)
# print(e.substitute({'a': 4, 'e': 3}))
# print(e.substitute({'a': "M.fromStr('5.65d')", 'e': "M.fromStr('2.322d')"}))
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
# m=Matrix([[2, 0, 3], [1, 3, 0], [0, -2, 1], [-2, 0, -3]])
# m.gaussjordanElimination()
# print(m)

# Compound.setLatexPrint(True)
# print(Compound('3[Cr(N2H4CO)6]4[Cr(CN)6]3 (s)'))
# print(Compound('2H2O').composition)
# print(Element('Xe').mass)

# print(max(Measurement.fromStr('5.50d'), Measurement('4.43', uncertainty="2")))
# print(Measurement.fromStr(f'2.97 +/- 0.43% g H2'))
# exec('from includes.measurement import Measurement as M')
# print(eval("""M.fromStr("5.6 +/- 0.1 g H2") - M.fromStr("2.99 +/- 0.42% g H2")"""))
# p=AutoP('chemistry/stoichiometry')
# p.new()
# p.generate()

# p=AutoP('chemistry/stoichiometry')
# p.generate()


# print(Equation(['v', 'u', 'a', 't'], 'v', 'u+a**t'))

# limiting_reagent()
# print()
# print(flms[1])
# print()
# print('\n\n'.join([str(i) for i in flms[2]]))
# SN('6.7')

# from includes.chemistry.chemical_node_charts import chemical_node_charts
# print(chemical_node_charts())

# ChemicalEquation.setLatexPrint(True)
# c = ChemicalEquation('H2 + O2 = H2O')
# c.solve()
# print(c)

# print(Compound("Pb2(PO4)3").molePercentComposition())

# chemical_equation_solver()

# Packager('Measurement Bundle',['includes/measurement.py']).package()
# F.setLatexPrint(True)
# print(F(-1, 2))
# Matrix.setLatexPrint(True)
# print(Matrix([[F(1,1), F(2, 1)], [F(3, 1), F(-5,7)], [F(6, 1), F(-10,7)]]))

# Packager('Chemistry Bundle V2',
#          ['includes/chemistry/chemical_equation_solver.py',
#           'includes/chemistry/chemical_node_charts.py',
#           'includes/chemistry/stoichiometry.py',
#           'includes/chemistry/limiting_reagent.py'
#          ]).package()