import graphviz
from numpy.random import randint
from collections import deque

class DestinationNode:
    def __init__(self, key, cost):
        self.key  = key
        self.cost = cost

class Graph:
    def __init__(self):
        self.edges = {}
    
    def key_path_pair_in_edges(self, fromKey: str, destination: DestinationNode):
        fromToPair = f"{fromKey}{destination.key}" 

        for key, edges in self.edges.items():
            for destination in edges:
                if f"{key}{destination.key}" == fromToPair:
                    return True
        
        return False
    
    def add_edge(self, fromKey: str, destination: DestinationNode):
        # Check if this path already exists
        if self.key_path_pair_in_edges(fromKey, destination):
            return False

        # Check if from key is equal to to key
        if fromKey == destination.key:
            return False

        if fromKey not in self.edges.keys():
            self.edges[fromKey] = [destination]
        else:
            self.edges[fromKey].append(destination)
        
        return True
    
    def vertices(self):
        """ the state of vertices is captured in edges - do not store it separately """
        vertices = []
        for key, destinations in self.edges.items():
            if key not in vertices:
                vertices.append(key)
            for destination in destinations:
                if destination.key not in vertices:
                    vertices.append(destination.key)
        
        return vertices

class UndirectedGraph(Graph):
    def add_edge(self, fromKey: str, destination: DestinationNode):
        return Graph.add_edge(self, fromKey, destination) and Graph.add_edge(self, fromKey=destination.key, destination=DestinationNode(key=fromKey, cost=destination.cost))
    
    def as_graphviz(self, name: str):
        g = graphviz.Graph(name)
        g.attr('node', shape='circle')

        seenPairs = []
        for fromKey in self.edges.keys():
            # f.node(key)
            for destination in self.edges[fromKey]:
                if f"{destination.key}{fromKey}" not in seenPairs:
                    g.edge(fromKey, destination.key, label=str(destination.cost))
                    seenPairs.append(f"{fromKey}{destination.key}")
        return g
    
    def save_vizualization(self, name: str):
        self.as_graphviz(name).render()

class DirectedGraph(Graph):
    def add_edge(self, fromKey: str, destination: DestinationNode):
        return Graph.add_edge(self, fromKey, destination)
    
    def as_graphviz(self, name: str):
        g = graphviz.Digraph(name)
        g.attr('node', shape='circle')

        for fromKey in self.edges.keys():
            # f.node(key)
            for destination in self.edges[fromKey]:
                g.edge(fromKey, destination.key, label=str(destination.cost))

        return g
    
    def save_vizualization(self, name: str):
        self.as_graphviz(name).render()

class Vertex:
    def __init__(self, key: str, cost, previousKey: str):
        self.key         = key
        self.cost        = cost
        self.previousKey = previousKey
    
    def __str__(self):
        return f"key: {self.key}, cost: {self.cost}, previousKey: {self.previousKey}"

class Path:
    def __init__(self, steps: deque, cost: int, possible: True):
        self.steps    = steps
        self.cost     = cost
        self.possible = possible
    
    def __str__(self):
        return f"Steps: {','.join(self.steps)}\nCost: {self.cost}"
    

def graph_by_type(type: str):
    if type == "undirected":
        return UndirectedGraph()
    elif type == "directed":
        return DirectedGraph()
    else:
        raise TypeError("graph_by_type called with wrong type argument")

def dumb_graph(type: str="undirected"):
    graph = graph_by_type(type)

    graph.add_edge( fromKey="Start", destination=DestinationNode(key="A", cost=4) )
    graph.add_edge( fromKey="A", destination=DestinationNode(key="B", cost=8) )
    graph.add_edge( fromKey="B", destination=DestinationNode(key="End", cost=9) )

    graph.add_edge( fromKey="Start", destination=DestinationNode(key="C", cost=3) )
    graph.add_edge( fromKey="C", destination=DestinationNode(key="D", cost=2))
    graph.add_edge( fromKey="D", destination=DestinationNode(key="End", cost=7))

    return graph

def random_graph(vertexCount: int, pathCount: int, minCost: int=1, maxCost: int=10, type: str="undirected"):
    graph = graph_by_type(type)

    vertices = []

    for i in range(vertexCount):
        vertices.append(str(i))

    addedCount = 0
    while addedCount != pathCount:
        # Don't bother w/ ensuring from key doesn't match to key, Graph will not add path if from key and to key match
        fromKey = vertices[int(randint(0, vertexCount))]
        toKey   = vertices[int(randint(0, vertexCount))]
        cost    = randint(minCost, maxCost+1)
        
        if graph.add_edge( fromKey=fromKey, destination=DestinationNode(key=toKey, cost=cost) ):
            addedCount += 1
    return graph

def undefined_vertex():
    return Vertex(key = "", cost = float("infinity"), previousKey = None)

def initialized_vertex(key: str):
    vertex = undefined_vertex()
    vertex.key = key
    return vertex

def lowest_cost_vertex(queue: set, vertexes: dict):
    lowestCostVertex = undefined_vertex()

    for key in queue:
        vertex = vertexes[key]
        if lowestCostVertex.cost > vertex.cost:
            lowestCostVertex = vertex
    
    return lowestCostVertex

def impossible_path():
    return Path(steps=deque(), cost=float("infinity"), possible=False)