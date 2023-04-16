# Computes the strongly connected components of a directed graph using Kosaraju's two-pass
# depth first search algorithm. Completed for Programming assignment 1 from the Graph Search,
# Shortest Paths, and Data Structures Coursera course from Stanford University
import time

# Vertex class for constructing graphs
class Vertex:

    def __init__(self, node):
        self.id = node
        self.explored = False
        self.leader = None
        self.order = None
        self.downstream = {}

    def add_downstream(self, neighbor, weight=0):
        self.downstream[neighbor] = weight

    def get_connections(self):
        return self.downstream.keys()

    def get_id(self):
        return self.id

    def explore(self):
        self.explored = True

    def set_leader(self, leader):
        self.leader = leader

    def set_order(self, order):
        self.order = order

# Graph class
class Graph:

    def __init__(self):
        self.verts = {}
        self.num_verts = 0

    def add_vert(self, node):
        new_vert = Vertex(node)
        self.verts[node] = new_vert
        self.num_verts += 1
        return new_vert

    def remove_vert(self, node):
        if node in self.verts:
            return self.verts.pop(node)

    def get_vertices(self):
        return self.verts.keys()

    def get_vert(self, node):
        if node in self.verts:
            return self.verts[node]
        else:
            return None

    def get_leaders(self):
        return [self.verts[n].leader for n in self.verts]

    def add_edge(self, start, end, cost=0):

        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], cost)


def kosaraju(G : Graph, G_rev: Graph, top_n : int = 5):

    # Run the DFS loop over the graph
    DFS_loop(graph_rev)

    # Get the finishing order from the first DFS pass. Use this in descending
    # order as the search order for the second DFS pass
    search_order = [-1] * graph_rev.num_verts
    for n in graph_rev.verts:
        search_order[graph_rev.verts[n].order] = n
    search_order.reverse()

    # Run DFS again on the forward graph, using the finishing time as the start vertex order
    DFS_loop(graph, order = search_order)

    # Get the most common leaders
    top_leaders = most_common(graph.get_leaders(), n = top_n)

    return top_leaders

def DFS_loop(G : Graph, order : list = []):

    # Global variables for the explored vertices count and the current source vertex
    global exp_cnt, source

    # Explored count. Used to define the search order for the second DFS pass
    exp_cnt = 0

    # Current source vertex from which the DFS was initiated. Useful only during the second DFS pass
    source = None

    # If no search order was passed, just get the vertices
    if len(order) == 0:
        order = G.get_vertices()

    # Try DFS from all vertices to ensure everything gets explored
    for n in order:
        # If a vertex is not explored, begin DFS
        if not G.verts[n].explored:

            source = n
            # DFS
            _ = DFS(G, G.verts[n])
    return

def DFS(G: Graph, start: Vertex):

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
    return

def most_common(arr : list, n : int = 5):

    # Use the collection library. Nice pythonic way to retrieve most common.
    from collections import Counter
    cnt = Counter(arr)
    return cnt.most_common(n)

def construct_graphs(input_file : str):

    # Initialize graph obejects for both the forward and reverse graphs
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