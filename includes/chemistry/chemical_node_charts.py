from includes.chemistry.chemicalequation import ChemicalEquation
from includes.fraction import Fraction as F
from includes.inputs import booleanInput as bInput, numericInput as nInput

def chemical_node_charts():
  equation = ChemicalEquation(input('Enter whole equation seperated by "=": '))
  variableSpace = None
  if bInput("Specify Variable Space"):
    variableSpace = nInput("Variable Space: ", int)
  idealPaths = bInput("Allow only ideal paths")
  connections = {e: [i != F(0, 1) for i in equation.matrix.matrix[equation.elements[e]]] for e in equation.elements}
  connectionsMade = [False for i in range(len(equation.matrix.matrix[0]))]
  splitIndex = len(equation.reactantCompounds)

  def calculateRelationships(currentConnections, currentConnectionsMade, split):
    currentRelationships = {}
    for e in currentConnections:
      unfilledLeft = 0
      unfilledRight = 0
      for ind, i in enumerate(currentConnections[e]):
        if i:
          if not currentConnectionsMade[ind]:
            if ind < split:
              unfilledLeft += 1
            else:
              unfilledRight += 1
      relationship = "multiple"
      if unfilledLeft + unfilledRight == 1:
        relationship = 'oneleft'
      elif unfilledLeft == 1 and unfilledRight == 1:
        relationship = 'onetoone'
      elif unfilledLeft + unfilledRight == 0:
        relationship = 'zero'
      currentRelationships[e] = relationship
    return currentRelationships

  def applyElement(currentConnections, currentConnectionsMade, element):
    return [(currentConnections[element][ind] or currentConnectionsMade[ind]) for ind in range(len(currentConnectionsMade))]

  relationships = calculateRelationships(connections, connectionsMade, splitIndex)
  layers = [[ChemicalEquationStateNode([i], applyElement(connections, connectionsMade, i), variablesUsed = 1) for i in relationships if relationships[i] == 'onetoone']]
  print(len(equation.matrix.matrix[0])-1)
  for i in range(len(equation.matrix.matrix[0])-1):
    newLayer = []
    currentLayer = layers[-1]
    for node in currentLayer:
      if variableSpace != None:
        if node.variablesUsed > variableSpace:
          print('Failed')
          node.fail = True
          continue
      if all(node.connections):
        node.success = True
        print('Success')
        continue
      newRelationships = calculateRelationships(connections, node.connections, splitIndex)
      print(newRelationships)
      allowableSteps = {i: newRelationships[i] for i in newRelationships if newRelationships[i] in ['oneleft', 'onetoone']}
      print(allowableSteps)
      hasOneLeft = False
      for s in allowableSteps:
        if allowableSteps[s] == 'oneLeft':
          hasOneLeft = True
        else:
          if idealPaths and hasOneLeft:
            break
        newNode = ChemicalEquationStateNode(node.state + [s], applyElement(connections, node.connections, s), variablesUsed = node.variablesUsed + (1 if allowableSteps[s] == 'onetoone' else 0))
        if newNode not in newLayer:
          newLayer.append(newNode)
        else:
          newNode = newLayer.index(newNode)
        node.addSubNode(newNode)
      if not len(allowableSteps):
        print('Failed')
        node.fail = True
      print('New Node')
    if newLayer:
      layers.append(newLayer)
    else:
      break
    print('Next Iter')
  print(layers)

class ChemicalEquationStateNode:
  def __init__(self, state, connections, subNodes = None, variablesUsed = 0):
    self.state = state
    self.connections = connections
    self.subNodes = [] if not subNodes else subNodes
    self.variablesUsed = variablesUsed
    self.success = False
    self.fail = False

  def addSubNode(self, sub):
    self.subNodes.append(sub)

  def __eq__(self, other):
    return set(self.state) == set(other.state) and self.variablesUsed == other.variablesUsed

  def __str__(self):
    return str(self.state) + ": " + str(self.connections)

  def __repr__(self):
    return str(self)