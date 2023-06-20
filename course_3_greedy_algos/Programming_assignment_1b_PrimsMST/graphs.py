
# Vertex class for constructing graphs
class Vertex:
    def __init__(self, node):
        """
        Constructor
        Args:
            node: unique, hashable identifier for the vertex
        """
        self.id = node
        self.explored = False
        self.neighbors = {}

    def add_neighbor(self, key, weight=0):
        """
        Add a neighbour to the Vertex via a weighted edge
        Args:
            key: key of vertex to make a neighbour
            weight: optional, weight of the edge

        Returns: None
        """
        self.neighbors[key] = weight
        return None

#Graph class
class Graph:
    def __init__(self):
        self.verts = {}
        self.explored = {}
        self.edges = []
        self.num_verts = 0
        self.edge_sum = 0

    def get_vertices(self):
        """
        Get the keys of all vertices in the graph
        Returns: keys of all vertices in the graph
        """
        return self.verts.keys()

    def add_vert(self, key):
        """
        Add a Vertex object to graph
        Args:
            key: unique, hashable identifier for the Vertex

        Returns: None
        """
        if key not in self.verts:
            self.verts[key] = Vertex(key)
            self.num_verts += 1
        return None

    def add_edge(self, start: int, end:  int, weight: int):
        """
        Add a weighted edge to the graph
        Args:
            start: key for the start Vertex of the edge to edd
            end: key for the end Vertex of the edge to edd
            weight: optional, weight of the edge

        Returns: None
        """

        if start not in self.verts:
            self.add_vert(start)
        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_neighbor(end, weight)
        self.verts[end].add_neighbor(start, weight)
        self.edge_sum += weight
        self.edges.append([start,end,weight])

        return None


