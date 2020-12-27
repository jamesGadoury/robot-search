import pathgraph
import robotsearch

def main():
    print("Shortest path from Start:", ",".join(robotsearch.dijkstra_search(graph = pathgraph.dumb_graph("directed"), start = "Start", target = "End")))

if __name__ == "__main__":
    main()