import time
import glob

def read_input(src: str):
    """
    Helper function to read input txt file.
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
        if node not in self.verts:
            self.verts[node] = Vertex(node)
            self.num_verts += 1

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
        return {n:self.verts[n].leader for n in self.verts}

    def add_edge(self, start, end, cost=0):

        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], cost)

def build_implication_graphs(edg_list: list):
    print("Construct implication graph")
    G = Graph()
    G_rev = Graph()
    i = 1
    for e in edg_list:
        G.add_edge(-e[0], e[1])
        G.add_edge(-e[1], e[0])

        G_rev.add_edge(e[1], -e[0])
        G_rev.add_edge(e[0], -e[1])

    return G, G_rev


def kosaraju(G : Graph, G_rev: Graph):

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
    DFS_loop(G, order = search_order)

    return None

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
    return None

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
    return None

def check_2sat(G: Graph):

    leaders = G.get_leaders()
    vert_list = list(G.verts.keys())

    while vert_list:
        x = vert_list.pop()
        if leaders[x] == leaders[-x]:
            print('Unsatisfiable!')
            return None
    print('Satisfiable')
    return None


if __name__ == "__main__":

    for file in glob.glob("*.txt"):

        print("Checking", file)

        two_sat_in = read_input(file)

        begin = time.time()
        im_graph, im_graph_rev = build_implication_graphs(two_sat_in)
        print("Graph construction ran in", time.time() - begin, "seconds")

        begin = time.time()
        kosaraju(im_graph, im_graph_rev)
        print("Kosaraju ran in", time.time() - begin, "seconds")

        check_2sat(im_graph)





