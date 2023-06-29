"""
Computing the shortest paths between all pairs of vertices/nodes in a directed, weighted graph real-valued edges.

Includes are two algorithms for solving this problem:
1. The Floyd-Warshall algorithm, a dynamic programming approach running in O(n^3)
2. Johnson's algorithm, a reduction of the problem to 1 call of the Bellman-Ford algorithm followed by n calls of
   Dijkstra's algorithm, running in O(n^2log(n) + mn)
"""
import numpy as np
import cProfile
from data_structures import heap

def read_input(src: str):
    """
    Helper function to read input txt file. First line is the number of vertices and edges
    in the graph. Subsequent lines are edges given by tail vertex, head vertex, and edge length, in order
    Args:
        src: str, file path for the input

    Returns: inp, array of the inputs
    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append([int(i) for i in line.split()])
    return inp


class Vertex:
    """
    Vertex class for constructing graphs
    """
    def __init__(self, key):
        """
        Constructor
        Args:
            key: unique, hashable identifier for the Vertex
        """
        self.key = key
        self.out_edges = {}
        self.in_edges = {}

    def add_out_edge(self, dest, weight: float=0):
        """
        Add an out-going wegithed edge to the vertex
        Args:
            dest: identifier for the edge end Vertex 
            weight: float, weight for the edge to be added, optional 

        Returns:
            None
        """
        self.out_edges[dest] = cost
        return None

    def add_in_edge(self, start, weight: float=0):
        """
        Add an incoming weighted edge to the vertex
        Args:
            start: identifier for the start Vertex of the edge
            weight: float, weight for the edge to be added, optional

        Returns:
            None
        """
        self.in_edges[start] = cost
        return None

class Graph:
    """
    Class for directed, weighted graphs with real valued edges
    """
    def __init__(self):
        """
        Graph class constructor.
        """
        self.vertices = {}
        self.num_vertices = 0
        self.num_edges = 0
        self.re_weighted = False

    def add_vertex(self, key):
        """
        Add a vertex to the graph

        Args:
            key: unique, hashable identifier for the vertex

        Returns:
            None
        """
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)
            self.num_vertices += 1
        return None

    def add_edge(self, start, dest, weight: float = 0):
        """
        Add an edge to the graph. Adds start and end vertices if not already in the graph.

        Args:
            start: unique, hashable identifier of for the edge start vertex
            dest:  unique, hashable identifier of for the edge end vertex
            weight: float, weight for the edge to be added, optional

        Returns:
            None
        """
        if start not in self.vertices:
            self.add_vertex(start)
        if dest not in self.vertices:
            self.add_vertex(dest)

        self.vertices[start].add_out_edge(dest, cost)
        self.vertices[dest].add_in_edge(start, cost)
        self.num_edges += 1

        return None

    def re_weight(self, W):
        """
         Re-weights edges to ensure non-negative values using computed vertex weightings

        Args:
            W: array, vertex weights computed as the minimum path lengths from a dummy node with o cost connection
                  to all nodes.

        Returns:
            None
        """
        for u, u_vert in self.vertices.items():
            for v, c_uv in u_vert.out_edges.items():
                v_vert = self.vertices[v]
                u_vert.out_edges[v] = c_uv + W[u] - W[v]
                v_vert.in_edges[u] = c_uv + W[u] - W[v]

        self.re_weighted = True

        return None

    def floyd_warshall(self):
        """
        Compute the length of the shortest path for all pairs of vertices in the input graph using the
        Floyd-Warshall algorithm. This is dynamic programming approach that works by computing path lengths
        using a limited, expanding number of vertices.

        We exploit the fact that each time a vertex is added, the shortest path between every pair is
        either the existing path length, or the sum of two optimal sub-paths passing through the newly
        added vertex. Negative cycles are detected of the fly by checking for negative path lengths from
        any vertex to itself. Computation is terminated upon finding a negative cycle as shortest paths are undefined.
        Running time is O(V^3)

        Returns:
            A: np array of all pairs of minimum path lengths
        """

        print("Running Floyd-Warshall algo")

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
                    # Check for negative cycles
                    if A[i, i] < 0:
                        print("Graph contains negative cycles, shortest path matrix undefined")
                        return None
        print("Smallest minimum pair path:", A.min())

        return A

    def johnson(self):
        """
        Johnson's algo for the all-pairs shortest paths problem with negative edges.

        Invokes the Bellman-Ford algorithm once to compute vertex weights. These are used to re-weight the edges,
        removing any negative values.

        Having removed negative edges, we call Dijkstra from each node. The final path lengths are then adjusted to
        their true value by inverting the weighting operation

        Running time is O(n^2log(n) + mn), the n calls to Dijkstra (nlog(n)) plus the single call the Bellman-Ford

        Returns:
            A: np.array with the shortest path lengths
        """

        print("Running Johnson's algo")

        # If not done already, re-weight to remove any negative edges
        if not self.re_weighted:
            print("Computing weights for re-weighting")
            weights = self.bellman_ford(list(self.vertices.keys())[0], re_weight=True)
            self.re_weight(weights)

        # Initialize the output array with boundary conditions
        A = np.full((self.num_vertices, self.num_vertices), np.inf)

        # Having re-weighted, perform Dijkstra from each vertex
        print("Finding shortest paths")
        for u in self.vertices:
            A[u, :] = self.dijkstra(u)

            # Adjust to the true lengths using the weights
            A[u, :] = A[u, :] + weights - weights[u]

        print("Smallest minimum pair path:", A.min())
        return A

    def bellman_ford(self, start: int, check_negative: bool = True, re_weight: bool = False):
        """
        Bellman-Ford algorithm for computing the minimum path lengths from a single source.

        This is a dynamic programming alternative to Dijkstra that accepts graphs with negative edges weights. We limit
        the number of allowed edges and iteratively expand it, exploiting the fact that if adding another allowed
        edges creates a new optimum path, the edge must be appended to a previously computed optimal path.

        Running time is O(mn), number of edges times number of vertices

        :param start:
        :param check_negative:
        :param re_weight:
        :return:
        Args:
            start: int, identifies the starting node
            check_negative: bool, optional. Triggers an additional iteration (checking with n edges) to test for
               any negative cycles, in which case the shortest paths are not well-defined. Default is True.
            re_weight: bool, optional. Triggers the addition of dummy node which is used as the start. The returned
               array then contains the vertex weights that allow re-weighting to remove negative edges in Johnson's
               algo. Default is False.

        Returns:
            A: np array with the shortest path lengths. None if negative cycles detected.
        """

        # Set up array for storing path lengths. If we want to re-weight, IC is a path length of zero to all nodes
        # from the dummy node, max edges is n. Otherwise, IC is inf to all except the passed starting node, n-1.
        if re_weight:
            A = np.zeros(self.num_vertices)
            start = list(self.vertices.keys())[0]
        else:
            A = np.full(self.num_vertices, np.inf)
            A[start] = 0

        max_edges = self.num_vertices

        # Iterate over the number of allowed edges
        for i in range(1, max_edges):
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

    def dijkstra(self, start: int):
        """
        Min heap based implementation of Dijkstra's algorithm for an undirected graph. Runs in O(nlog(n)). The graph
        must contain no negative edges for the routine to yield a correct result. If negative edges are present, the
        graph must first be re-weighted.

        Running time is O(nlog(n))

        Args:
            start:  int, start vertex

        Returns:
            A: np array with the shortest path lengths
        """

        # Sets to keep track of what is explored and what isn't
        explored = set()
        explored.add(start)
        vert_set = set(self.vertices.keys())

        # Array for shortest paths, with appropriate ICs
        A = np.full(self.num_vertices, np.inf)
        A[start] = 0

        # Initial heap populated with Dijkstra greedy criterion (DGC) and vert numbers stemming from the start node
        H = heap.MinHeap()
        for v, c_sv in self.vertices[start].out_edges.items():
            H.insert(c_sv, v)

        # Continue until everything is explored
        while explored != vert_set:

            # Get the root from the heap and add it to the explored set
            min_dgc, add = H.pop_root()

            if add not in explored:
                A[add] = min_dgc
                explored.add(add)

            # Add new frontier DGCs to the heap
            for u, c_u in self.vertices[add].out_edges.items():
                # If we've already explored here, move on
                if u in explored:
                    continue

                # Insert the new path length
                H.insert(min_dgc + c_u, u)
        return A


if __name__ == "__main__":

    # Source files for the input graphs
    src_g1 = "g1.txt"
    src_g2 = "g2.txt"
    src_g3 = "g3.txt"
    """ 
    # ***** Both G1, G2 have negative cycles, so we'll skip these for comparing Johnson and Floyd-Warshall 
    
    
    # Build the graph, src 1
    graph_src1 = read_input(src_g1)
    G1 = Graph()
    for start, dest, cost in graph_src1:
        G1.add_edge(start-1, dest-1, cost)

    # Run Floyd-Warshall algorithm
    #cProfile.run('G1.floyd_warshall()')

    # Build the graph, src 2
    graph_src2 = read_input(src_g2)
    G2 = Graph()
    for start, dest, cost in graph_src2:
        G2.add_edge(start - 1, dest - 1, cost)

    # Run Floyd-Warshall algorithm
    #cProfile.run('G2.floyd_warshall()')
    """

    # Build the graph, src 3
    graph_src3 = read_input(src_g3)
    G3 = Graph()
    for start, dest, cost in graph_src3:
        G3.add_edge(start - 1, dest - 1, cost)

    # Run FW with profiling
    cProfile.run('G3.floyd_warshall()')

    # Run Johnson with profiling
    cProfile.run('G3.johnson()')



