import time, sys

# Max recursion depth for DFS
MAX_DEPTH = 2000

# Vertex class for constructing graphs
class Vertex:

    def __init__(self, node):
        self.id = node
        self.explored = False
        self.order = None
        self.downstream = {}

    def add_downstream(self, neighbor, weight=0):
        self.downstream[neighbor] = weight

    def get_connections(self):
        return self.downstream.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.downstream[neighbor]

    def explore(self):
        self.explored = True

    def set_order(self, order):
        self.order = order

# Graph class
class Graph:

    def __init__(self):
        self.verts = {}
        self.edges = []
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

    def add_edge(self, start, end, cost=0):

        if start not in self.verts:
            self.add_vert(start)

        if end not in self.verts:
            self.add_vert(end)

        self.verts[start].add_downstream(self.verts[end], cost)


def DFS(G: Graph, start: Vertex, current_label: int, depth: int):

    # Explore the vertex we are starting from
    start.explore()

    # Check all neighbors. Call DFS recursively on any that are unexplored
    for n in start.get_connections():
        # Stop recursion if maximum depth reached
        if depth > MAX_DEPTH:
            break

        # If not explored, DFS using a recursive call
        if not n.explored:
            depth += 1
            current_label, depth = DFS(G, n, current_label, depth)

    # Assign the current label to the start vertex
    start.set_order(current_label)
    return current_label - 1, depth - 1

def DFS_loop(G : Graph):

    # Label for ordering is initially the total number of vertices
    current_label = G.num_verts

    # Try DFS from all vertices to ensure everything get's explored
    for n in G.get_vertices():

        # If a vertex is not explored, begin DFS
        if not G.verts[n].explored:

            # Keep track of the recursion depth to avoid stack overflow
            depth = 0

            # DFS
            current_label, _ = DFS(G, G.verts[n], current_label, depth)

    return

if __name__ =="__main__":

    # Increase recursion limit
    sys.setrecursionlimit(2 ** 20)

    graph = Graph()

    # Read in the input graph
    with open("SCC_adjList.txt") as file:
        for l in file.readlines():
            s, e = [int(n) for n in l.split()]
            graph.add_edge(s, e)

    begin = time.time()

    # Run the DFS loop over the graph
    DFS_loop(graph)

    # Print time required
    print("Topological sorting completed in:", time.time() - begin, "seconds")