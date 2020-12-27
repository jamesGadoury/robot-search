from collections import deque
import pathgraph

def dijkstra_search(graph, start: str, target: str):
    queue = deque()
    vertexes = {}

    for key in graph.paths.keys():
        queue.append(key)
        vertexes[key] =  pathgraph.initialized_vertex(key)
    
    if start not in vertexes.keys():
        raise KeyError("start node was not found in graph")
    if target not in vertexes.keys():
        raise KeyError("target node was not found in graph")
    
    vertexes[start].cost = 0
    
    # While queue is not empty
    while len(queue) != 0:

        current = pathgraph.lowest_cost_vertex(queue, vertexes)
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