import graphviz

class Path:
    def __init__(self, key, cost):
        self.key  = key
        self.cost = cost

class Graph:
    def __init__(self):
        self.paths = {}
    
    def add_path(self, key: str, path: Path):
        if key not in self.paths.keys():
            self.paths[key] = [path]
        else:
            self.paths[key].append(path)
    
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
        Graph.add_path(self, key=key, path=path)
        Graph.add_path(self, key=path.key, path=Path(key=key, cost=path.cost))
    
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
        Graph.add_path(self, key=key, path=path)
    
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

def dumb_graph(type: str):
    if type == "undirected":
        graph = UndirectedGraph()
    elif type == "directed":
        graph = DirectedGraph()
    else:
        raise TypeError("dumb_graph called with wrong type argument")

    graph.add_path( key="Start", path=Path(key="A", cost=4) )
    graph.add_path( key="A", path=Path(key="B", cost=8) )
    graph.add_path( key="B", path=Path(key="End", cost=9) )

    graph.add_path( key="Start", path=Path(key="C", cost=3) )
    graph.add_path( key="C", path=Path(key="D", cost=2))
    graph.add_path( key="D", path=Path(key="End", cost=7))

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
