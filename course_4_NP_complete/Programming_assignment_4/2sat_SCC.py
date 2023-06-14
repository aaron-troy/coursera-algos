import time
import glob

def read_2sat_input(src: str):
    """
    Helper function to read txt file input for the 2-sat problem. Input first line contains the number of clauses.
    Following lines have identifiers for the booleans, negative indicates not.
    Args:
        src: str, file path for the input

    Returns: inp, array of the input constraints
    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append([int(i) for i in line.split()])
    return inp


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
        return {n:self.verts[n].leader for n in self.verts}

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

def build_implication_graphs(edg_list: list, reverse=False):
    """
    Build an implication graph from a list of input constraints for 2sat problem. For each constraint, two edges are
    added. One for A' -> B, another for B' -> A
    :param edg_list: list of lists. Each entry is a list with the two boolean values for the constraint
    :param reverse: Boolean flag for produce a graph with reversed edges. Optional, default False
    :return: Graph object
    """
    G = Graph()

    if reverse:
        for e in edg_list:
            G.add_edge(e[1], -e[0])
            G.add_edge(e[0], -e[1])
    else:
        for e in edg_list:
            G.add_edge(-e[0], e[1])
            G.add_edge(-e[1], e[0])
    return G


def kosaraju(G : Graph, G_rev: Graph):
    """
    Run Kosaraju's algorithm to compute the strongly connected components in a direct graph.

    First run a DFS on the reversed graph, retaining the finishing order for each vertex. Then complete a second
    DFS on the forward graph using the reversed finishing order (i.e. vertices that finished last start). During
    the second DFS, keep track of the DFS source, assigning this as the leader to each node explored. Vertices in a
    SCC will have the same leader

    :param G: Graph object, forward edges
    :param G_rev: Graph object, reverse edges
    :return: None
    """
    # Run the DFS loop over the graph
    print('DFS reverse graph')
    DFS_loop(G_rev)

    # Get the finishing order from the first DFS pass. Use this in descending
    # order as the search order for the second DFS pass
    search_order = [-1] * G_rev.num_verts
    for n in G_rev.verts:
        search_order[G_rev.verts[n].order] = n
    search_order.reverse()

    # Run DFS again on the forward graph, using the finishing time as the start vertex order
    print('DFS forward graph')
    DFS_loop(G, order=search_order)

    return None

def DFS_loop(G : Graph, order : list = []):
    """

    :param G: Graph object to perform DFS on
    :param order: Order of vertices to initiate DFS from. Used during 2nd pass of Kosaraju's algo
    :return: None
    """

    # Global variables for the explored vertices count and the current source vertex
    global exp_cnt, source

    # Explored count. Used to define the search order for the second DFS pass
    exp_cnt = 0

    # Current source vertex from which the DFS was initiated. Useful only during the second DFS pass
    source = None

    # If no search order was passed, just get the vertices
    if not order:
        order = G.get_vertices()

    # Try DFS from all vertices to ensure everything gets explored
    for n in order:
        # If a vertex is not explored, begin DFS
        if not G.verts[n].explored:

            source = n
            # DFS
            _ = DFS(G.verts[n])
    return None

def DFS(start: Vertex):
    """
    Perform DFS on directed graph from a starting Vertex object. Implemented using stack.
    :param start: Vertex object to start the DFS from
    :return: None
    """
    # Global variables for the explored vertices count and the current source vertex
    global exp_cnt, source

    # Initialize the stack with only the start vertex
    stack = [start]

    while stack:
        # Get the home vertex
        home = stack[-1]

        # Explore the vertex we are starting from
        if not home.explored:
            home.explore()

        # Set the leader for this vertex as the current source
        home.set_leader(source)

        # Check all neighbors. If they are unexplored add them to the stack
        for n in home.get_connections():

            # If not explored, add to the stack
            if not n.explored:
                stack.append(n)

        # If there are no neighbours to explore, we're done with this node.
        # Remove from the stack and assign a finishing order.
        if home == stack[-1]:
            if home.order == None:
                home.order = exp_cnt
                exp_cnt += 1
            stack.pop()
    return None

def check_2sat(G: Graph):
    """
    Check whether a 2 sat instance represented as an implication graph is satisfiable. A graph is unsatisfiable, iff
    X and X` are contained in the same strongly connected component of the implication graph.
    :param G: Graph object, implication graph of 2 sat instance. Must have leaders identified for each vertex.
    :return: None
    """
    leaders = G.get_leaders()
    vert_list = list(G.verts.keys())

    if None in leaders.values():
        print('Missing leaders in graph! SCCs undefined.')
        return None

    while vert_list:
        x = vert_list.pop()
        if leaders[x] == leaders[-x]:
            print('Unsatisfiable!')
            return None
    print('Satisfiable')
    print('\n')
    return None


if __name__ == "__main__":

    for file in glob.glob("*.txt"):

        print("Checking", file)

        two_sat_in = read_2sat_input(file)

        begin = time.time()
        print("Construct implication graphs")
        im_graph = build_implication_graphs(two_sat_in)
        im_graph_rev = build_implication_graphs(two_sat_in, reverse=True)
        print("Graph construction ran in", time.time() - begin, "seconds")

        begin = time.time()
        kosaraju(im_graph, im_graph_rev)
        print("Kosaraju ran in", time.time() - begin, "seconds")

        check_2sat(im_graph)





