from graphviz import Graph as GraphVizGraph

class Path:
    def __init__(self, key, cost):
        self.key  = key
        self.cost = cost

class Graph:
    """ Very poorly implemented graph """
    def __init__(self):
        self.paths = {}

    def addPath(self, key: str, path: Path):
        if key not in self.paths.keys():
            self.paths[key] = [path]
        else:
            self.paths[key].append(path)
        
        # now that path is added to key node - add reverse path
        pathBack = Path(key=key, cost=path.cost)
        if path.key not in self.paths.keys():
            self.paths[path.key] = [pathBack]
        else:
            self.paths[path.key].append(pathBack)

class Vertex:
    def __init__(self, key: str, cost, previousKey: str):
        self.key         = key
        self.cost        = cost
        self.previousKey = previousKey
    
    def __str__(self):
        return f"key: {self.key}, cost: {self.cost}, previousKey: {self.previousKey}"

def dumb_graph():
    graph = Graph()
    graph.addPath( key="Start", path=Path(key="A", cost=4) )
    graph.addPath( key="A", path=Path(key="B", cost=8) )
    graph.addPath( key="B", path=Path(key="End", cost=9) )

    graph.addPath( key="Start", path=Path(key="C", cost=3) )
    graph.addPath( key="C", path=Path(key="D", cost=2))
    graph.addPath( key="D", path=Path(key="End", cost=7))

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

def vizualize_graph(graph):
    g = GraphVizGraph('graph')
    g.attr('node', shape='circle', size='2,2')

    seenPairs = []
    for key in graph.paths.keys():
        # f.node(key)
        for path in graph.paths[key]:
            if f"{path.key}{key}" not in seenPairs:
                g.edge(key, path.key, label=str(path.cost))
                seenPairs.append(f"{key}{path.key}")
    g.render()