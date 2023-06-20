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

def read_file(src: str):
    """
    Helper function for reading the input file, returned as an array
    Args:
        src: file path for input

    Returns: list, adjacency list from the input

    """
    arr = []
    with open(src) as file:
        arr = []
        for line in file.readlines()[1:]:
            arr.append([int(i) for i in line.split()])
    return arr


def build_graph(adj_list: list):
    """
    Helper function that builds a graph object from an adjacency list
    Args:
        adj_list:

    Returns: Graph object constructed from adjacency list
    """
    graph_out = graphs.Graph()
    for x, y, w in adj_list:
        graph_out.add_edge(x, y, w)
    return graph_out

def prims_mst(graph_in: graphs.Graph):
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
    h = heap.MinHeap()
    current = next(iter(graph_in.get_vertices()))
    # Use a graph object for the output
    tree_out = graphs.Graph()

    # Add edges from the start to the heap
    for vert, weight in graph_in.verts[current].neighbors.items():
        h.insert(weight, (current, vert))

    # Continue while T does not span G
    while tree_out.get_vertices() != graph_in.get_vertices():

        # Get the next minimum cost edge from the heap
        weight, (start, nxt) = h.pop_root()

        # If the edge goes somewhere unexplored, add it to the MST
        if nxt not in tree_out.verts:
            tree_out.add_edge(start, nxt, weight)
            # Add new frontier edges to the heap.
            for add, add_weight in graph_in.verts[nxt].neighbors.items():
                if add not in tree_out.verts:
                    h.insert(add_weight, (nxt, add))
    return tree_out

def kruskal_mst(graph_in: graphs.Graph):
    """
    Compute the minimum spanning tree (MST) for an input undirected graph using Kruskal's greedy algo
    -- an alternative to Prim's above. Implemented using union-find data structure. In this approach,
    we traverse a sorted list of edges increasing in cost. We greedily add each successive edge to the
    MST if its addition does not result in a directed cycle.

    Deploying the UF data structure allows for "blazingly fast" checks for these cycles, speeding things
    up from an O(n^2) running time to O(mlog(n)).
    """

    # Get a list of edges and sort
    edges = sorted(graph_in.edges, key= lambda x: x[2])

    # Use a graph object for the MST
    tree_out = graphs.Graph()

    # Union-find object to accelerate Kruskal
    mst_uf = union_find.UnionFind()
    for m1, m2, _ in edges:
        mst_uf.add_member(m1)
        mst_uf.add_member(m2)

    # Continue merging parents until we span the graph
    while len(set(mst_uf.parents.values())) > 1:
        # Take the cheapest edge
        if len(edges) < 1:
            break
        start, end, cost = edges.pop(0)
        # If the edge connects distinct subtrees, and thus doesn't induce a cycle, add it to the MST
        if mst_uf.find(start) != mst_uf.find(end):
            tree_out.add_edge(start, end, cost)
            # Update the union-find
            mst_uf.union(start, end)

    return tree_out



if __name__ == "__main__":

    # Source file for the input graph
    source = "Prims_input.txt"
    # Build the graph
    g = build_graph(read_file(source))

    # Timing
    begin = time.time()

    # Compute MST, first using Prim's algorithm
    mst_prims = prims_mst(g)

    print("Prim's MST ran in", time.time() - begin, "seconds")
    print("MST cost:", mst_prims.edge_sum)

    # Re-build the graph to recompute the MST using Kruskal's algorithm
    g = build_graph(read_file(source))

    # Timing
    begin = time.time()

    # Compute MST again, this time using Kruskal's algorithm
    mst_kruskal = kruskal_mst(g)

    print("Kruskal's MST ran in", time.time() - begin, "seconds")
    print("MST cost:", mst_kruskal.edge_sum)
