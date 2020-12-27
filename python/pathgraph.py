import graphviz
from numpy.random import randint

class Path:
    def __init__(self, key, cost):
        self.key  = key
        self.cost = cost

class Graph:
    def __init__(self):
        self.paths = {}
    
    def key_path_pair_in_paths(self, key: str, path: Path):
        fromToPair = f"{key}{path.key}" 

        for fromKey, paths in self.paths.items():
            for toPath in paths:
                if f"{fromKey}{toPath.key}" == fromToPair:
                    return True
        
        return False
    
    def add_path(self, key: str, path: Path):
        # Check if this path already exists
        if self.key_path_pair_in_paths(key=key, path=path):
            return False

        # Check if from key is equal to to key
        if key == path.key:
            return False

        if key not in self.paths.keys():
            self.paths[key] = [path]
        else:
            self.paths[key].append(path)
        
        return True
    
    def path_keys(self):
        """ oh no - this is oh so confusing... how can I be better? """
        keys = []
        for key, paths in self.paths.items():
            if key not in keys:
                keys.append(key)
            for path in paths:
                if path.key not in keys:
                    keys.append(path.key)
        
        return keys

class UndirectedGraph(Graph):
    """ Very poorly implemented graph """
    def add_path(self, key: str, path: Path):
        return Graph.add_path(self, key=key, path=path) and Graph.add_path(self, key=path.key, path=Path(key=key, cost=path.cost))
    
    def as_graphviz(self, name: str):
        g = graphviz.Graph(name)
        g.attr('node', shape='circle')

        seenPairs = []
        for key in self.paths.keys():
            # f.node(key)
            for path in self.paths[key]:
                if f"{path.key}{key}" not in seenPairs:
                    g.edge(key, path.key, label=str(path.cost))
                    seenPairs.append(f"{key}{path.key}")
        return g
    
    def save_vizualization(self, name: str):
        self.as_graphviz(name).render()

class DirectedGraph(Graph):
    def add_path(self, key: str, path: Path):
        return Graph.add_path(self, key=key, path=path)
    
    def as_graphviz(self, name: str):
        g = graphviz.Digraph(name)
        g.attr('node', shape='circle')

        for key in self.paths.keys():
            # f.node(key)
            for path in self.paths[key]:
                g.edge(key, path.key, label=str(path.cost))

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

def graph_by_type(type: str):
    if type == "undirected":
        return UndirectedGraph()
    elif type == "directed":
        return DirectedGraph()
    else:
        raise TypeError("graph_by_type called with wrong type argument")

def dumb_graph(type: str="undirected"):
    graph = graph_by_type(type)

    graph.add_path( key="Start", path=Path(key="A", cost=4) )
    graph.add_path( key="A", path=Path(key="B", cost=8) )
    graph.add_path( key="B", path=Path(key="End", cost=9) )

    graph.add_path( key="Start", path=Path(key="C", cost=3) )
    graph.add_path( key="C", path=Path(key="D", cost=2))
    graph.add_path( key="D", path=Path(key="End", cost=7))

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
        
        if graph.add_path( key=fromKey, path=Path(key=toKey, cost=cost) ):
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
