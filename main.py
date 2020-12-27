from collections import deque
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

    

def dumb_graph():
    graph = Graph()
    graph.addPath( key="Start", path=Path(key="A", cost=4) )
    graph.addPath( key="A", path=Path(key="B", cost=8) )
    graph.addPath( key="B", path=Path(key="End", cost=9) )

    graph.addPath( key="Start", path=Path(key="C", cost=3) )
    graph.addPath( key="C", path=Path(key="D", cost=2))
    graph.addPath( key="D", path=Path(key="End", cost=7))

    return graph

class Vertex:
    def __init__(self, key: str, cost, previousKey: str):
        self.key         = key
        self.cost        = cost
        self.previousKey = previousKey
    
    def __str__(self):
        return f"key: {self.key}, cost: {self.cost}, previousKey: {self.previousKey}"

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

def dijkstra_search(graph, start: str, target: str):
    queue = deque()
    vertexes = {}

    for key in graph.paths.keys():
        queue.append(key)
        vertexes[key] =  initialized_vertex(key)
    
    if start not in vertexes.keys():
        raise KeyError("start node was not found in graph")
    if target not in vertexes.keys():
        raise KeyError("target node was not found in graph")
    
    vertexes[start].cost = 0
    
    # While queue is not empty
    while len(queue) != 0:

        current = lowest_cost_vertex(queue, vertexes)
        queue.remove(current.key)
        if current.key == target:
            break

        for path in graph.paths[current.key]:
            alt = current.cost + path.cost
            if alt < vertexes[path.key].cost:
                vertexes[path.key].cost = alt
                vertexes[path.key].previousKey = current.key

    # Now read shortest path from start to target by reverse iteration
    current = vertexes[target]

    shortestPath = deque()

    if current.previousKey is not None or current.key == start.key:
        while current.previousKey is not None:
            shortestPath.insert(0, current.key)
            current = vertexes[current.previousKey]
    
    return ",".join(shortestPath)

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

def main():
    vizualize_graph(dumb_graph())
    
    print("Shortest path from Start:", dijkstra_search(graph = dumb_graph(), start = "Start", target = "End"))

if __name__ == "__main__":
    main()