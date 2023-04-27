"""
Computing the minimum spanning tree (MST) from an undirected weight graph. Input is a text file
adjacency list with weights, output the cost of the MST (sum of weights) compute using Prim's greedy
algorithm.
"""

import time
import graphs
import heap

def read_file(source : str):
    """
    Helper function for reading the input file, returned as an array
    """
    arr = []
    with open(source) as file:
        arr = []
        for line in file.readlines()[1:]:
            arr.append([int(i) for i in line.split()])
    return arr


def build_graph(adj_list: list):
    """
    Helper function that builds a graph object from an adjacency list
    """
    G = graphs.Graph()
    for x,y,w in adj_list:
        G.add_edge(x,y,w)
    return G

def Prims_MST(G : graphs.Graph):
    """
    Compute the minimum spanning tree (MST) for an input undirected graph using Prim's greedy algo.
    Implemented using min-heap data structure. At each step, edges crossing the frontier from explored
    to  unexplored territory are added. The minimum cost edge is maintained at the root. We continuosly pop
    the root and see if it goes somewhere unexplored. If yes, add it to the MST and update the heap with
    new frontier edges.

    This implementation avoid having to delete arbitrary elements from the heap, but the heap will
    contain redundant edges as a consequence.
    """
    # Initialize heap for frontier edges and get the start vertex
    H = heap.MinHeap()
    current = next(iter(G.get_vertices()))
    # Use a graph object for the output
    T = graphs.Graph()

    # Add edges from the start to the heap
    for vert, weight in G.verts[current].neighbors.items():
        H.insert(weight, (current, vert))

    # Continue while T does not span G
    while T.get_vertices() != G.get_vertices():

        # Get the next minimum cost edge from the heap
        weight, (start, nxt) = H.pop_root()

        # If the edge goes somewhere unexplored, add it to the MST
        if nxt not in T.verts:
            T.add_edge(start, nxt, weight)
            # Add new frontier edges to the heap.
            for add, add_weight in G.verts[nxt].neighbors.items():
                if add not in T.verts:
                    H.insert(add_weight, (nxt, add))
    return T


if __name__ == "__main__":

    # Source file for the input graph
    source = "Prims_input.txt"
    # Build the graph
    G = build_graph(read_file(source))

    # Timing
    begin = time.time()

    # Compute MST
    MST = Prims_MST(G)

    print("Prim's MST ran in", time.time() - begin, "seconds")
    print("MST cost:", MST.edge_sum)
