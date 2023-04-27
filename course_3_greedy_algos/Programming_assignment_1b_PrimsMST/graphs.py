
# Vertex class for constructing graphs
class Vertex:
    def __init__(self, node):
        self.id = node
        self.explored = False
        self.neighbors = {}
    def add_neighbor(self, key, weight):
        self.neighbors[key] = weight

#Graph class
class Graph:
    def __init__(self):
        self.verts = {}
        self.explored = {}
        self.num_verts = 0
        self.edge_sum = 0
    def get_vertices(self):
        return self.verts.keys()

    def add_vert(self, key):
        if key not in self.verts:
            self.verts[key] = Vertex(key)
            self.num_verts += 1
    def add_edge(self, start : int, end :  int, weight : int):

        if start not in self.verts:
            self.add_vert(start)
        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_neighbor(end, weight)
        self.verts[end].add_neighbor(start, weight)
        self.edge_sum += weight


