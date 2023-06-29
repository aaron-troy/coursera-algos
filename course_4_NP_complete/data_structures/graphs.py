class Vertex:
    """
    Vertex class for graph construction. Equipped for running Kosaraju's algorithm.
    """

    def __init__(self, node):
        """
        Constructor for vertex.
        Args:
            node: unique, hashable identifier for the vertex.
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

    def add_downstream(self, neighbor, weight: float = 0):
        """
        Add a weighted link to a downstream vertex

        Args:
            neighbor: hashable identifier for the downstream vertex
            weight: float, optional weight for the link, default to 0

        Returns:
            None
        """
        self.downstream[neighbor] = weight
        return None

    def get_connections(self):
        """
        Return the keys for downstream neighbour vertices

        Returns:
            self.downstream.keys(): dict keys for linked downstream vertices
        """
        return self.downstream.keys()

    def explore(self):
        """
        Update explored flag to true
        Returns:
            None
        """
        self.explored = True
        return None

    def set_leader(self, leader):
        """
        Set the leader for a vertex, indicating its SCC membership

        Args:
            leader: Hashable identifier for the leader

        Returns:
            None
        """
        self.leader = leader
        return None

    def set_order(self, order: int):
        """
        Set place in the search order for the 2nd pass of Kosaraju's algo

        Args:
            order: int, index in search order

        Returns:
            None
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

        Args:
            node: Hashable identifier for the vertex to add.

        Returns:
            None
        """
        if node not in self.verts:
            self.verts[node] = Vertex(node)
            self.num_verts += 1
        return None

    def remove_vert(self, node):
        """
        Remove a vertex from the graph.

        Args:
            node: Unique identifier for the vertex to remove. Must be in the graph.

        Returns:
            None
        """
        if node in self.verts:
            self.verts.pop(node)
        return None

    def get_vertices(self):
        """
        Get keys for all vertices in the graph

        Returns:
            self.verts.keys: keys for vertices in the graph
        """
        return self.verts.keys()

    def get_vert(self, node):
        """
        Get Vertex object by identifier

        Args:
            node: Unique, hashable identifier for the vertex

        Returns:
            self.verts[node]: Vertex object corresponding the passed identifier. None if desired vertex not in graph
        """
        if node in self.verts:
            return self.verts[node]
        else:
            return None

    def get_leaders(self):
        """
            Get a dict of the leaders for all vertices in the graph
        Returns:
            dict: n : self.verts[].leader
        """
        return {n: self.verts[n].leader for n in self.verts}

    def add_edge(self, start, end, weight: float =0):
        """
        Add a weighted, directed edge to the graph. Add Vertex instances for the start and end if not already in the graph

        Args:
            start: unique, hashable identifier for the start Vertex
            end: unique, hashable identifier for the end Vertex
            weight: float, weight for the edge, optional, default 0

        Returns:
            None
        """
        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], weight)

        return None
