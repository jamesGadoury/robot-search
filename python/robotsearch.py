from collections import deque
import pathgraph

def dijkstra_search(graph: pathgraph.Graph, start: str, target: str):
    queue = deque()
    vertexes = {}

    if start == target:
        return []

    for key in graph.vertices():
        queue.append(key)
        vertexes[key] = pathgraph.initialized_vertex(key)

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

        if current.key not in graph.edges.keys():
            # dead end - if there are no more possible from keys then it is impossible to reach the destination:
            if len(queue) == 0:
                return pathgraph.impossible_path()

            continue

        for destination in graph.edges[current.key]:
            alt = current.cost + destination.cost
            if alt < vertexes[destination.key].cost:
                vertexes[destination.key].cost = alt
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