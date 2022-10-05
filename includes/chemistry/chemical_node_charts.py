from includes.chemistry.chemicalequation import ChemicalEquation
from includes.fraction import Fraction as F
from includes.inputs import booleanInput as bInput, numericInput as nInput
from includes.typecheck import typecheck

def chemical_node_charts(equation = None, variableSpace = None, idealPaths = True):
  typecheck(equation, ChemicalEquation)
  typecheck(variableSpace, int, None)
  typecheck(idealPaths, bool)
  if equation == None:
    equation = ChemicalEquation(input('Enter whole equation seperated by "=": '))
    variableSpace = None
    if bInput("Specify Variable Space"):
      variableSpace = nInput("Variable Space: ", int)
    idealPaths = bInput("Allow only ideal paths")
    chemical_node_charts(equation, variableSpace, idealPaths)

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
      allowableSteps1 = {i: newRelationships[i] for i in newRelationships if newRelationships[i] == 'oneleft'}
      allowableSteps2 = {i: newRelationships[i] for i in newRelationships if newRelationships[i] == 'onetoone'}
      hasOneLeft = False
      for s in allowableSteps1:
        hasOneLeft = True
        newNode = ChemicalEquationStateNode(node.state + [s], applyElement(connections, node.connections, s), variablesUsed = node.variablesUsed)
        if newNode not in newLayer:
          newLayer.append(newNode)
        else:
          newNode = newLayer[newLayer.index(newNode)]
        node.addSubNode(newNode)
      if not idealPaths or not hasOneLeft:
        for s in allowableSteps2:
          newNode = ChemicalEquationStateNode(node.state + [s], applyElement(connections, node.connections, s), variablesUsed = node.variablesUsed + 1)
          if newNode not in newLayer:
            newLayer.append(newNode)
          else:
            newNode = newLayer[newLayer.index(newNode)]
          node.addSubNode(newNode)
      if not len(allowableSteps1)+len(allowableSteps2):
        print('Failed')
        node.fail = True
      print('New Node')
    if newLayer:
      layers.append(newLayer)
    else:
      break
    print('Next Iter')
  print(layers)
  output = []
  index = 0
  for i, layer in enumerate(layers):
    for n in layer:
      index+=1
      n.jsonifyNode(index, i+1)
      output.append(n)
  edges = []
  for node in output:
    edges += node.jsonifyEdges()
  return {'nodes': output, 'edges': edges}

class ChemicalEquationStateNode:
  def __init__(self, state, connections, subNodes = None, variablesUsed = 0):
    self.state = state
    self.connections = connections
    self.subNodes = [] if not subNodes else subNodes
    self.variablesUsed = variablesUsed
    self.success = False
    self.fail = False
    self.id = None
    self.level = None
    self.label = None
    self.color = "#97C2FC"

  def addSubNode(self, sub):
    self.subNodes.append(sub)

  def jsonifyNode(self, id, level):
    self.id = id
    self.level = level
    self.label = str(self)
    if self.success:
      self.color = "#057a1c"
    elif self.fail:
      self.color = "#fc0303"

  def jsonifyEdges(self):
    edges = []
    print(self)
    print("hello", self.subNodes)
    for i in self.subNodes:
      print(type(i), i)
      edges.append({'from': self.id, 'to': i.id, 'color': ("#fc0303" if i.variablesUsed > self.variablesUsed else "#ccc")})
    return edges
  
  def __eq__(self, other):
    return set(self.state) == set(other.state) and self.variablesUsed == other.variablesUsed

  def __str__(self):
    return str(self.state) + "-" + str(self.variablesUsed)

  def __repr__(self):
    return str(self)