from includes.inputs import numericInput, choiceInput
from includes.matrix import Matrix
from includes.fraction import Fraction

import itertools

def two_event_solver():  
  regions = ['a', 'b', 'c', 'd']
  baseEvents = {"A": {'b', 'c'}, "A'": {'a', 'd'}, "B": {'c', 'd'}, "B'": {'a', 'b'}}
  combEvents = [i for i in itertools.permutations(baseEvents.keys(), r=2) if ("A" == i[0] or "A'" == i[0]) and not ("A" in i and "A'" in i)]
  permEvents = [i for i in itertools.permutations(baseEvents.keys(), r=2) if ("A" in i or "A'" in i) and ("B" in i or "B'" in i)]
  choices = sorted(baseEvents.keys()) + [f'{i[0]}&&{i[1]}' for i in combEvents] + [f'{i[0]}||{i[1]}' for i in combEvents] + [f'{i[0]}|{i[1]}' for i in permEvents]
  cinput = choiceInput(choices, 3, numericInput, float)
  def setToRow(s):
    return [1 if i in s else 0 for i in regions]
  matrixRows = [[1, 1, 1, 1, 1]]
  for k, v in cinput.items():
    if len(k) <= 2:
      matrixRows.append(setToRow(baseEvents[k])+[v])
    elif '||' in k:
      s1, s2 = [baseEvents[i] for i in k.split('||')]
      matrixRows.append(setToRow(s1.union(s2))+[v])
    elif '&&' in k:
      s1, s2 = [baseEvents[i] for i in k.split('&&')]
      matrixRows.append(setToRow(s1.intersection(s2))+[v])
    else:
      s1, s2 = [baseEvents[i] for i in k.split('|')]
      intersection = setToRow(s1.intersection(s2))
      given = setToRow(s2)
      matrixRows.append([v * given[ind] - i for ind, i in enumerate(intersection)]+[0])
  m = Matrix(matrixRows)
  m.gaussjordanElimination()
  solutions = [row[-1] for row in m.matrix]
  for ind, i in enumerate(regions):
    print(f'{i}: {solutions[ind]} or {float(solutions[ind]):.3f}')
  print('\nTherefore,')
  for k in choices:
    ans = None
    rowSum = None
    if len(k) <= 2:
      rowSum = setToRow(baseEvents[k])
    elif '||' in k:
      s1, s2 = [baseEvents[i] for i in k.split('||')]
      rowSum = setToRow(s1.union(s2))
    elif '&&' in k:
      s1, s2 = [baseEvents[i] for i in k.split('&&')]
      rowSum = setToRow(s1.intersection(s2))
    else:
      s1, s2 = [baseEvents[i] for i in k.split('|')]
      intersection = Fraction.sum([solutions[ind]*Fraction.fromInt(i) for ind, i in enumerate(setToRow(s1.intersection(s2)))])
      given = Fraction.sum([solutions[ind]*Fraction.fromInt(i) for ind, i in enumerate(setToRow(s2))])
      ans = intersection / given
    ans = Fraction.sum([solutions[ind]*Fraction.fromInt(i) for ind, i in enumerate(rowSum)]) if ans is None else ans
    print(f'P({k}): {ans} or {float(ans):.3f}')