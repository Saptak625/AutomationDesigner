class Graph:
  def __init__(self):
    self.nodes = {}

  def addNode(self, name, edges=[]):
    if name in self.nodes:
      raise Exception(f'Graph Node "{name} must be uniquely named."')
    self.nodes[name]=Node(name, edges=edges)

  def removeNode(self, name):
    self.nodes.pop(name)

  def addEdge(self, start, end, weight = 1, bidirectional=False):
    if start not in self.nodes or end not in self.nodes:
      raise Exception("Start and End Nodes must be defined to create Edge.")
    startNode = self.nodes[start]
    endNode = self.nodes[end]
    startNode.addEdge(endNode, weight=weight)
    if bidirectional:
      endNode.addEdge(startNode, weight=weight)

  def removeEdge(self, start, end, bidirectional=False):
    if start not in self.nodes or end not in self.nodes:
      raise Exception("Start and End Nodes must be defined to remove Edge.")
    startNode = self.nodes[start]
    endNode = self.nodes[end]
    startNode.removeEdge(endNode)
    if bidirectional:
      endNode.removeEdge(startNode)

class Node:
  def __init__(self, name, edges={}):
    self.name = name
    self.edges = edges

  def addEdge(self, node, weight = 1):
    self.edges[node.name] = Edge(self, node, weight=weight)

  def removeEdge(self, node):
    self.edges.pop(node.name)

class Edge:
  def __init__(self, start, end, weight = 1):
    self.start = start
    self.end = end
    self.weight = weight