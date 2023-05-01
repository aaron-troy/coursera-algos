"""
 Implement k-means clustering using a greedy / Kuskal's algorithm approach. We will make use of a lazy
 union-find by rank data strcuture to speed things up. The naive implementation of Kruskals will be quadratic
 in the size of the graph -- we need to complete n edge adds and each requires  the use of graph search
 to ensure a cycle is not being added.

 We would like is some data structure that allows us to rapidly check if two nodes are already connected,
 and maintain this while we merge sub-trees through Kruskals algorithm. This is achieved by the union-find
 data structure.


 In this data structure, each member maintains a pointer to its parent.
"""

import time
import union_find

def read_graph(src: str):
    with open(src) as file:
        edges = []
        for line in file.readlines()[1:]:
            edges.append([int(i) for i in line.split()])
    return edges

def km_cluster(G : list, num_clusters: int):

    # Get a list of edges, sorted by increasing distance
    edges = sorted(G, key= lambda x: x[2])

    # Setup union-find
    U = union_find.UnionFind()
    for m1, m2, _ in edges:
        U.add_member(m1)
        U.add_member(m2)

    # Keep track of the number of merges
    merges = 0

    while merges < len(U.ids) - num_clusters:
        # Pop lowest remaining distance
        start, end, distance = edges.pop(0)

        # If the edge isn't from within a cluster, merge the clusters
        if U.find(start) != U.find(end):
            U.union(start, end)
            merges += 1

    # Get the maximum spacing
    while len(edges) > 0:
        start, end, spacing = edges.pop(0)
        if U.find(start) != U.find(end):
            return spacing

    # Return false if there is no max spacing
    return False

if __name__ == "__main__":

    # Source file for the input graph
    source = "clustering1.txt"

    # Build the graph
    G = read_graph(source)

    # Timing
    begin = time.time()

    # Run k-means clustering
    max_spacing = km_cluster(G, 4)

    print("KM clustering ran in", time.time() - begin, "seconds")
    print("Max spacing:", max_spacing)