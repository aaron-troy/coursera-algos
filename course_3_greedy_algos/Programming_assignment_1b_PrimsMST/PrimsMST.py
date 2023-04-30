"""
Computing the minimum spanning tree (MST) from an undirected weight graph. Input is a text file
adjacency list with weights, output the cost of the MST (sum of weights). Computation is performed twice,
using two different greedy algorithms. The first is Prim's algorithm, implemented using a heap data structure.
The second is Kruskal's algorithm, which deploys a lazy union-find by rank data structure. Both approaches
achieve O(mlog(n)) running time.
"""

import time
import graphs
import heap
import union_find

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

def Prim_MST(G : graphs.Graph):
    """
    Compute the minimum spanning tree (MST) for an input undirected graph using Prim's greedy algo.
    Implemented using min-heap data structure. At each step, edges crossing the frontier from explored
    to  unexplored territory are added. The minimum cost edge is maintained at the root. We continuosly pop
    the root and see if it goes somewhere unexplored. If yes, add it to the MST and update the heap with
    new frontier edges.

    This implementation avoids having to delete arbitrary elements from the heap, but the heap will
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

def Kruskal_MST(G : graphs.Graph):
    """
    Compute the minimum spanning tree (MST) for an input undirected graph using Kruskal's greedy algo
    -- an alternative to Prim's above. Implemented using union-find data structure. In this approach,
    we traverse a sorted list of edges increasing in cost. We greedily add each successive edge to the
    MST if its addition does not result in a directed cycle.

    Deploying the UF data structure allows for "blazingly fast" checks for these cycles, speeding things
    up from an O(n^2) running time to O(mlog(n)).
    """

    # Get a list of edges and sort
    edges = sorted(G.edges, key= lambda x: x[2])

    # Use a graph object for the MST
    T = graphs.Graph()

    # Union-find object to accelerate Kruskal
    U = union_find.UnionFind()
    for m1, m2, _ in edges:
        U.add_member(m1)
        U.add_member(m2)

    # Continue merging parents until we span the graph
    while len(set(U.parents.values())) > 1:
        # Take the cheapest edge
        if len(edges) < 1:
            print('Graph is not connected. MST not possible')
            break
        start, end, cost = edges.pop(0)
        # If the edge connects distinct subtrees, and thus doesn't induce a cycle, add it to the MST
        if U.find(start) != U.find(end):
            T.add_edge(start, end, cost)
            # Update the union-find
            U.union(start, end)

    return T



if __name__ == "__main__":

    # Source file for the input graph
    source = "Prims_input.txt"
    # Build the graph
    G = build_graph(read_file(source))

    # Timing
    begin = time.time()

    # Compute MST, first using Prim's algorithm
    MST_Prims = Prim_MST(G)

    print("Prim's MST ran in", time.time() - begin, "seconds")
    print("MST cost:", MST_Prims.edge_sum)

    # Re-build the graph to recompute the MST using Kruskal's algorithm
    G = build_graph(read_file(source))

    # Timing
    begin = time.time()

    # Compute MST again, this time using Kruskal's algorithm
    MST_Kruskal = Kruskal_MST(G)

    print("Kruskal's MST ran in", time.time() - begin, "seconds")
    print("MST cost:", MST_Kruskal.edge_sum)
