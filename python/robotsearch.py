from collections import deque
import pathgraph

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

def dijkstra_search(graph: pathgraph.Graph, start: str, target: str):
    queue = deque()
    vertexes = {}

    if start == target:
        return pathgraph.Path(steps=deque(), cost=0, possible=True)

    for key in graph.vertices():
        queue.append(key)
        vertexes[key] = initialized_vertex(key)

    if start not in vertexes.keys():
        raise KeyError("start node was not found in graph")
    if target not in vertexes.keys():
        raise KeyError("target node was not found in graph")
    
    vertexes[start].cost = 0
    
    # While queue is not empty
    while len(queue) != 0:
        current = lowest_cost_vertex(queue, vertexes)

        if current.key not in queue:
            # no more available neighbors 
            return pathgraph.impossible_path()

        queue.remove(current.key)

        if current.key == target:
            break

        if current.key not in graph.edges.keys():
            # dead end - if there are no more possible from keys then it is impossible to reach the destination:
            if len(queue) == 0:
                return pathgraph.impossible_path()
            continue

        for destination in graph.edges[current.key]:
            neighborCostFromCurrent = current.cost + destination.cost
            # vertexes[destination.key].cost will be infinite if we haven't reached the vertex in our search yet
            # otherwise, we have already seen it and should only update if this is the cheaper past
            if neighborCostFromCurrent < vertexes[destination.key].cost:
                vertexes[destination.key].cost = neighborCostFromCurrent
                vertexes[destination.key].previousKey = current.key

    # Now read shortest path from start to target by reverse iteration
    current = vertexes[target]

    shortestPath = deque()

    if current.previousKey is not None or current.key == start.key:
        while current.previousKey is not None:
            shortestPath.insert(0, current.key)
            current = vertexes[current.previousKey]
    
    return pathgraph.Path(steps=shortestPath, cost=vertexes[target].cost, possible=True)

def dijkstra_search_and_display_string(graph: pathgraph.Graph, start: str, target: str):
    return f"Shortest path from {start} to {target}:\n{dijkstra_search(graph, start, target)}"