class Vertex:
    """
    Vertex class for undirected wegithed graph construction
    """
    def __init__(self, key):
        """
        Constructor
        :param key: unique, hashable identifier for Vertex
        """
        self.id = key
        self.explored = False
        self.neighbors = {}

    def add_neighbor(self, key, weight=0):
        """
        Add a neighbor
        :param key: nique, hashable identifier for the neighbour Vertex
        :param weight: weight of the edge, optional
        :return: None
        """
        self.neighbors[key] = weight
        return None

#Graph class
class Graph:
    """
    Graph class. Equipped for running Dijkstra's algo
    """
    def __init__(self):
        """
        Constructor
        """
        # Dict for Vertex objects in graph
        self.verts = {}
        # Numver of Vertex objects in the graph
        self.num_verts = 0

    def get_vertices(self):
        """
        Get the keys of all Vertex objects in the graph
        :return: keys of all Vertex objects
        """
        return self.verts.keys()

    def add_vert(self, key):
        """
        Add a Vertex to the graph
        :param key: unique, hashable identifier for the Vertex object to create and add
        :return: None
        """
        if key not in self.verts:
            self.verts[key] = Vertex(key)
            self.num_verts += 1
        return None
    def add_edge(self, start : int, end :  int, weight=0):
        """
        Add a weighted edge connecting two Vertex objects in the graph. Start and/or end are created and added
        if not in the graph already
        :param start: unique, hashable identifier for the edge start Vertex object
        :param end: unique, hashable identifier for the edge end Vertex object
        :param weight: weight of the edge, optional
        :return: None
        """

        if start not in self.verts:
            self.add_vert(start)
        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_neighbor(end, weight)
        self.verts[end].add_neighbor(start, weight)

        return None



