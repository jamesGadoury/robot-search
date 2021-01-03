import pathgraph
import robotsearch
import unittest

class TestGraphMethods(unittest.TestCase):

    def test_create_undirected_graph(self):
        self.assertTrue(isinstance(pathgraph.graph_by_type("undirected"), pathgraph.UndirectedGraph))
    
    def test_create_directed_graph(self):
        self.assertTrue(isinstance(pathgraph.graph_by_type("directed"), pathgraph.DirectedGraph))

    def test_add_duplicate_edge_undirected(self):
        graph      = pathgraph.graph_by_type("undirected")
        destination = pathgraph.DestinationNode("B", 1)
        self.assertTrue(graph.add_edge(fromKey="A", destination=destination))
        self.assertFalse(graph.add_edge(fromKey="A", destination=destination))
    
    def test_add_duplicate_edge_directed(self):
        graph=pathgraph.graph_by_type("directed")
        destination = pathgraph.DestinationNode("B", 1)
        self.assertTrue(graph.add_edge(fromKey="A", destination=destination))
        self.assertFalse(graph.add_edge(fromKey="A", destination=destination))

def main():
    unittest.main()

if __name__ == "__main__":
    main()