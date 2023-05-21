import numpy as np
import cProfile


def read_input(src: str):
    """
    Helper function to read input txt file. First line is the number of vertices and edges
    in the graph. Subsequent lines are edges given by tail vertex, head vertex, and edge length, in order
    Args:
        src: str, file path for the input

    Returns:

    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append([int(i) for i in line.split()])
    return inp


class Vertex:
    def __init__(self, key):
        self.key = key
        self.out_edges = {}
        self.in_edges = {}

    def add_out_edge(self, dest, cost):
        self.out_edges[dest] = cost

    def add_in_edge(self, start, cost):
        self.in_edges[start] = cost

class Graph:
    def __init__(self):
        """
        Graph class constructor.

        self.vertices - hash table for Vertex objects
        Self.num_vertices - int, current number of vertices
        """
        self.vertices = {}
        self.num_vertices = 0
        self.num_edges = 0

    def add_vertex(self, key):
        """
        Add a vertex to the graph
        :param key: key, a unique, hashable identifier for the vertex
        """
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)
            self.num_vertices += 1

    def add_edge(self, start, dest, cost):
        """
        Add an edge to the graph. Adds start and end vertices if not already in the graph.
        :param start: unique, hashable identifier of for the edge start vertex
        :param dest: unique, hashable identifier of for the edge end vertex
        :param cost: cost for the edge
        """
        if start not in self.vertices:
            self.add_vertex(start)
        if dest not in self.vertices:
            self.add_vertex(dest)

        self.vertices[start].add_out_edge(dest, cost)
        self.vertices[dest].add_in_edge(start, cost)
        self.num_edges += 1

    def floyd_warshall(self):
        """
        Compute the length of the shortest path for all pairs of vertices in the input graph using the
        Floyd-Warshall algorithm. This is dynamic programming approach that works by computing path lengths
        using a limited, expanding number of vertices.

        We exploit the fact that each time a vertex is added, the shortest path between every pair is
        either the existing path length, or the sum of two optimal sub-paths passing through the newly
        added vertex. Running time is O(V^3)
        :return: A, np array of all pairs of minimum path lengths
        """

        # Initialize the output array with boundary conditions
        A = np.array([[np.inf] * self.num_vertices] * self.num_vertices)

        # Set up initial conditions
        for tail_key, tail in self.vertices.items():
            # Distance to self should be 0
            A[tail_key, tail_key] = 0
            # One-hop distances
            for head_key, head_cost in tail.out_edges.items():
                A[tail_key, head_key] = head_cost

        vert_range = range(self.num_vertices)

        # Recurrence
        for k in vert_range:
            for j in vert_range:
                for i in vert_range:
                    # Update the best path length only if we do better be passing through the new vertex
                    if (A[j, k] + A[k, i]) < A[j, i]:
                        A[j, i] = (A[j, k] + A[k, i])
                    if A[i, i] < 0:
                        print("Graph contains negative cycles, shortest path matrix undefined")
                        return None
        print("Smallest minimum pair path:", A.min())
        return A

    def bellman_ford(self, start, check_negative: bool = True):
        """
        Bellman-Ford algorithm for computing the minimum path lengths from a single source.

        This is a dynamic programming alternative to Dijkstra that accepts graphs with negative edges weights. We limit
        the number of allowed edges and iteratively expand it, exploiting the fact that if adding another allowed
        edges creates a new optimum path, the edge must be appended to a previously computed optimal path.

        Running time is O(mn), number of edges times number of vertices

        :param start: int, identifies the starting node
        :param check_negative: bool, optional. Triggers an additional iteration (checking with n edges) to test for
               any negative cycles, in which case the shortest paths are not well-defined. Default is True.
        :return: None if negative cycles detected. Array with the shortest path lengths otherwise.
        """

        # Set up array for storing path lengths
        A = np.full(self.num_vertices, np.inf)
        A[start] = 0

        # Iterate over the number of allowed edges, stopping at n-1
        for i in range(1, self.num_vertices-1):
            # Check each vertex to see if there is a shorter path
            for v, v_vert in self.vertices.items():
                min_in_edge = min([A[w] + cw for w, cw in v_vert.in_edges.items()])
                if min_in_edge < A[v]:
                    A[v] = min_in_edge

        # Check for negative cycles, if desired.
        if check_negative:
            for v, v_vert in self.vertices.items():
                min_in_edge = min([A[w] + cw for w, cw in v_vert.in_edges.items()])
                if min_in_edge < A[v]:
                    print("Graph contains negative cycles, shortest path matrix undefined")
                    return None

        return A




if __name__ == "__main__":

    # Source files for the input graphs
    src_g1 = "g1.txt"
    src_g2 = "g2.txt"
    src_g3 = "g3.txt"

    # Build the graph, src 1
    graph_src1 = read_input(src_g1)
    G1 = Graph()
    for start, dest, cost in graph_src1:
        G1.add_edge(start-1, dest-1, cost)

    # Run Floyd-Warshall algorithm
    #cProfile.run('G1.floyd_warshall()')

    cProfile.run('G1.bellman_ford(1)')

    """
    # Build the graph, src 2
    graph_src2 = read_input(src_g2)
    G2 = Graph()
    for start, dest, cost in graph_src2:
        G2.add_edge(start - 1, dest - 1, cost)

    # Run Floyd-Warshall algorithm
    cProfile.run('G2.floyd_warshall()')

    # Build the graph, src 3
    graph_src3 = read_input(src_g3)
    G3 = Graph()
    for start, dest, cost in graph_src3:
        G3.add_edge(start - 1, dest - 1, cost)

    # Run Floyd-Warshall algorithm
    cProfile.run('G3.floyd_warshall()')"""