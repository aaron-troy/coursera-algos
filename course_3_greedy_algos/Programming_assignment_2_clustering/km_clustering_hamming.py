"""
Completing k-means clustering on a very large input graph of binary strings. Distance between
graph members is the Hamming distance. Main computes the maximum number of clusters that will
preserve some minimum Hamming distance spacing

Implementation makes use of the union-find data structure, with lazy union-by-rank and path compression.
"""

import time
import union_find
import itertools

# Minimum spacing to compute the max number of clusters for
MIN_SPACE = 3

def read_hamming_graph(src: str):
    """
    Helper function to read in the graph. Input a text file. The first row is two numbers, the
    number of graph members and bits for each member's location. Subsequent rows are binary strings
    for each member's location.
    """
    with open(src) as file:
        nodes = []
        i = 1
        for line in file.readlines()[1:]:
            nodes.append(line.strip().replace(" ", ""))
            i += 1
    return nodes

def generate_neighborhood(member_dict: dict, home: str, min_hd: int=1):
    """
    Helper function that checks the graph for all possible members within a given Hamming distance
    of a home member. Returns a list of neighbors meeting this criteria
    """
    # Home member should be in the graph and of non-zero length
    assert home in member_dict
    assert len(home) > 0

    # Indexes a neighbor may differ at
    bit_idxs = list(range(0, len(home)))

    neighborhood = []
    # Search the neighborhood within the given Hamming distance
    for i in range(1, min_hd + 1):
        # Try all possible combinations of differences
        for comb in itertools.combinations(bit_idxs, i):
            add = list(home)
            # Flip bits at the specific indices
            for j in comb:
                add[j] = str(1 - int(add[j]))
            add = "".join(add)
            # If the candidate neighbor is in the graph, keep it.
            if add in member_dict:
                neighborhood.append("".join(add))
    return neighborhood


def max_clusters_hamming(G : list, min_spacing :int = 3):
    """
    Computes the maximum number of clusters in a graph that will preserve a passed minimum
    spacing between clusters. Employs a distributed greedy approach and union-find data structure.

    For each member, we check all possible members within the mimimum distance. If they are in the
    graph, perform a union. This approach avoids computing all pairwise distances followed by sorting,
    which is not feasible for an input of this size.
    """
    # Generate a copy of the graph to allow mutation
    members = G.copy()

    # Set up union-find
    U = union_find.UnionFind()
    for member in members:
        U.add_member(member)

    # Check the neighborhood with min sizing around all members. If there are neighbors,
    # perform a union.
    while members:
        m = members.pop()
        N = generate_neighborhood(U.ids, m, min_spacing - 1)
        for n in N:
            if U.find(n) != U.find(m):
                U.union(m, n)
    # Enforce path compression
    for m in U.parents:
        U.parents[m] = U.find(m)

    # Return the number of clusters
    return len(set(U.parents.values()))

if __name__ == "__main__":

    # Source file for the input graph
    source = "clustering_big.txt"

    # Build the graph
    G = read_hamming_graph(source)

    # Timing
    begin = time.time()

    # Run k-means clustering based on Hamming distance
    max_k = max_clusters_hamming(G, min_spacing=MIN_SPACE)

    print("KM clustering ran in", time.time() - begin, "seconds")
    print("The max number of clusters is", max_k, "for a minimum spacing of H = ", MIN_SPACE)