# Computes the strongly connected components of a directed graph using Kosaraju's two-pass
# depth first search algorithm. Completed for Programming assignment 1 from the Graph Search,
# Shortest Paths, and Data Structures Coursera course from Stanford University
import time
import cProfile
class Vertex:
    """
    Vertex class for graph construction
    """
    def __init__(self, node):
        """
        Constructor
        :param node: unique, hashbaled identifier
        """
        self.id = node
        self.explored = False
        self.leader = None
        self.order = None
        self.downstream = {}

    def add_downstream(self, neighbor, weight=0):
        """
        Add a weighted, directed edge to a neighbour
        :param neighbor: identifier for donwstream vertex
        :param weight: weight of edge, optional
        :return: None
        """
        self.downstream[neighbor] = weight
        return None

    def get_connections(self):
        """
        Get keys of all connected vertices
        :return: keys of connected vertices
        """
        return self.downstream.keys()

    def explore(self):
        """
        Mark as explored
        :return: None
        """
        self.explored = True
        return None

    def set_leader(self, leader):
        """
        Set the leader, denoting the strongly connected component (SCC), for the vertex
        :param leader: identifier for the leader vertex of the SCC
        :return: None
        """
        self.leader = leader
        return None

    def set_order(self, order: int):
        """
        Set place in a search order for a node. Used for 2nd pass of Kosaraju's algorithm
        :param order: int >= 0, place search order.
        :return: None
        """
        self.order = order
        return None

# Graph class
class Graph:
    """
    Graph class. Equipped for Kosaraju's algorithm for computing strongly connected components
    """
    def __init__(self):
        """
        Constructor
        """
        self.verts = {}
        self.num_verts = 0

    def add_vert(self, node):
        """
        Add a vertex to the graph
        :param node: unique, hashable identifier for the node
        :return: None
        """
        if node in self.verts:
            return None
        else:
            self.verts[node] = Vertex(node)
            self.num_verts += 1
            return None

    def remove_vert(self, node):
        """
        Remove a vertex form the graph
        :param node: identifier for the vertex
        :return: None
        """
        if node in self.verts:
            self.verts.pop(node)
        else:
            print("Vertex not found in graph!")
        return None

    def get_vert(self, node):
        """
        Get the vertex object by identifier
        :param node: Idenfitifer for the vertex
        :return: Vertex, None if not in graph
        """
        if node in self.verts:
            return self.verts[node]
        else:
            print("Vertex not found in graph!")
            return None

    def get_vertices(self):
        """
        Get dict of Vertex objects in the graph
        :return: dict of Vertex objects
        """
        return self.verts.keys()

    def get_leaders(self):
        """
        Get a dict of leaders, denoting SCC membership, for all vertices in the graph
        :return: dict, vertex keys : leader keys
        """
        return {n: self.verts[n].leader for n in self.verts}

    def add_edge(self, start, end, weight=0):
        """
        Add a directed, weighted edge to the graph. Start and/or end vertices are add if not already in
        graph
        :param start: key for the start vertex of the edge
        :param end: key for the end vertex of the edge
        :param weight: weight of the edge, optional
        :return: None
        """
        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], weight)
        return None

def kosaraju(forward_graph: Graph, reverse_graph: Graph, top_n : int = 5):
    """
    Kosaraju's algorithm for computing strongly connected components (SCCs). The algorithm exploits
    the fact that the graph with all edges reversed will have the same SCCs.

    Operates through a 2-stepdepth first search process. DFS is first performed on the graph with edges
    reversed, trying a start from all vertices until everything is explored. During this process we keep
    track of the finishing order, keeping track of the order in which vertices have all downstream
    vertices explored

    DFS is then performed again on the forward graph, starting the search from vertices in the reverse
    finishing order. This starting vertex is assigned as the leader for all vertices reached during
    the instance of DFS. Vertices with the same leader are in the same SCC.

    Runs in linear time!

    :param forward_graph: graph to compute SCCs on, with edges forward
    :param reverse_graph: graph to compute SCCs on, with edges reversed
    :param top_n: int, optional. Number of n largest SCCs to find
    :return: leader keys for the top_n largest SCCs
    """
    # Run the DFS loop over the graph
    dfs_loop(reverse_graph)

    # Get the finishing order from the first DFS pass. Use this in descending
    # order as the search order for the second DFS pass
    search_order = [-1] * reverse_graph.num_verts
    for n in reverse_graph.verts:
        search_order[reverse_graph.verts[n].order] = n
    search_order.reverse()

    # Run DFS again on the forward graph, using the finishing time as the start vertex order
    dfs_loop(forward_graph, order=search_order)

    # Get the most common leaders
    leaders = most_common(forward_graph.get_leaders().values(), n=top_n)

    return leaders

def dfs_loop(g: Graph, order: list = []):
    """
    DFS loop. Ensures DFS is attempted from all vertices, to ensure everything is explored.
    :param g: Graph object to perform DFS
    :param order: list denoting order of vertices to start DFS from. Optional
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
        order = g.get_vertices()

    # Try DFS from all vertices to ensure everything gets explored
    for n in order:
        # If a vertex is not explored, begin DFS
        if not g.verts[n].explored:
            source = n
            # DFS
            dfs(g, g.verts[n])
    return None

def dfs(g: Graph, start: Vertex):
    """
    Perform DFS on graph
    :param start: Vertex object from which to start the DFS
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
            if home.order is None:
                home.order = exp_cnt
                exp_cnt += 1
            stack.pop()
    return None

def most_common(arr: list, n: int = 5):
    """
    Find the most common entries in list
    :param arr: arr to inspect
    :param n: top n most common entries to identify
    :return: list of tuples, (entry, number of occurences)
    """

    # Use the collection library. Nice pythonic way to retrieve most common.
    from collections import Counter
    cnt = Counter(arr)
    return cnt.most_common(n)

def construct_graphs(input_file : str):

    # Initialize graph objects for both the forward and reverse graphs
    graph = Graph()
    graph_rev = Graph()

    # Read in the input and construct the forward and reverse graphs
    with open(input_file) as file:
        for l in file.readlines():
            s, e = [int(n) for n in l.split()]
            graph.add_edge(s, e)
            graph_rev.add_edge(e, s)

    return graph, graph_rev

if __name__ =="__main__":

    begin = time.time()

    # Read the input and construct graphs
    graph, graph_rev = construct_graphs("SCC_adjList.txt")

    print("Graph construction ran in:", time.time() - begin, "seconds")

    # Run Kosaraju's algorithm using the forward and reverse graphs
    begin = time.time()
    top_leaders = kosaraju(graph, graph_rev)

     # Print time required
    print("Kosaraju ran in:", time.time() - begin, "seconds")
    print("Most common leaders:", top_leaders)