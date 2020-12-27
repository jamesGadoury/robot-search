import pathgraph
import robotsearch

def main():
    pathgraph.vizualize_graph(pathgraph.dumb_graph())
    
    print("Shortest path from Start:", robotsearch.dijkstra_search(graph = pathgraph.dumb_graph(), start = "Start", target = "End"))

if __name__ == "__main__":
    main()