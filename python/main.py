import pathgraph
import robotsearch
import unittest

class TestGraphMethods(unittest.TestCase):

    def test_create_undirected_graph(self):
        self.assertTrue(isinstance(pathgraph.graph_by_type("undirected"), pathgraph.UndirectedGraph))
    
    def test_create_directed_graph(self):
        self.assertTrue(isinstance(pathgraph.graph_by_type("directed"), pathgraph.DirectedGraph))

    def test_add_duplicate_path_undirected(self):
        graph = pathgraph.graph_by_type("undirected")
        path  = pathgraph.Path("B", 1)
        self.assertTrue(graph.add_path(key="A", path=path))
        self.assertFalse(graph.add_path(key="A", path=path))
    
    def test_add_duplicate_path_directed(self):
        graph=pathgraph.graph_by_type("directed")
        path  = pathgraph.Path("B", 1)
        self.assertTrue(graph.add_path(key="A", path=path))
        self.assertFalse(graph.add_path(key="A", path=path))

def main():
    unittest.main()

if __name__ == "__main__":
    main()