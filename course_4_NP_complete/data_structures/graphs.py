class Vertex:
    """
    Vertex class for graph construction. Equipped for running Kosaraju's algorithm.
    """

    def __init__(self, node):
        """
        Constructor for vertex.
        :param node: unique, hashable identifier for the vertex.
        """
        # Unique hashable identifier
        self.id = node
        # Boolean flag for explored status
        self.explored = False
        # Leader, identifies a strongly connected component
        self.leader = None
        # Order, identifies place in search order for second DFS pass in Kosaraju's algo
        self.order = None
        # Dict for downstream neighbour vertices
        self.downstream = {}

    def add_downstream(self, neighbor, weight=0):
        """
        Add a weighted link to a downstream vertex
        :param neighbor: hashable identifier for the downstream vertex
        :param weight: optional weight for the link, default to 0
        :return: None
        """
        self.downstream[neighbor] = weight
        return None

    def get_connections(self):
        """
        Return the keys for downstream neighbour vertices
        :return: self.downstream.keys(), dict keys for linked downstream vertices
        """
        return self.downstream.keys()

    def explore(self):
        """
        Update explored flag to true
        :return:None
        """
        self.explored = True
        return None

    def set_leader(self, leader):
        """
        Set the leader for a vertex, indicating its SCC membership
        :param leader: Hashable identifier for the leader
        :return: None
        """
        self.leader = leader
        return None

    def set_order(self, order):
        """
        Set place in the search order for the 2nd pass of Kosaraju's algo
        :param order: Place in search order
        :return: None
        """
        self.order = order
        return None


# Graph class
class Graph:
    """
    Graph class. Equipped for running Kosaraju's algorithm for computing strongly connected components.
    """

    def __init__(self):
        """
        Constructor
        """
        self.verts = {}
        self.num_verts = 0

    def add_vert(self, node):
        """
        Add a vertex to the graph. Generates a new vertex instance.
        :param node: Hashable identifier for the vertex to add.
        :return: None
        """
        if node not in self.verts:
            self.verts[node] = Vertex(node)
            self.num_verts += 1
        return None

    def remove_vert(self, node):
        """
        Remove a vertex from the graph.
        :param node: Unique identifier for the vertex to remove. Must be in the graph.
        :return: None
        """
        if node in self.verts:
            self.verts.pop(node)
        return None

    def get_vertices(self):
        """
        Get keys for all vertices in the graph
        :return: self.verts.keys, keys for vertices in the graph
        """
        return self.verts.keys()

    def get_vert(self, node):
        """
        Get Vertex object by identifier
        :param node: Unique, hashable identifier for the vertex
        :return: self.verts[node], Vertex object corresponding the passsed identifier.
                None if desired vertex not in graph
        """
        if node in self.verts:
            return self.verts[node]
        else:
            return None

    def get_leaders(self):
        """
        Get a dict of the leaders for all vertices in the graph
        :return:
        """
        return {n: self.verts[n].leader for n in self.verts}

    def add_edge(self, start, end, weight=0):
        """
        Add a weighted, directed edge to the graph. Add Vertex instances for the start and end if not already in the graph
        :param start: unique, hashable identifier for the start Vertex
        :param end: unique, hashable identifier for the end Vertex
        :param weight: weight for the edge, optional, default 0
        :return: None
        """
        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], weight)

        return None