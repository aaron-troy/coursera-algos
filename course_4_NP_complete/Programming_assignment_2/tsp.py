import numpy as np
import itertools
from decimal import *
import cProfile

def read_input(src: str):
    """
    Helper function to read input txt file. First line is the number of cities in the graph.
    Subsequent lines are coordinates given for each of the cities
    Args:
        src: str, file path for the input

    Returns: inp, array of the inputs
    """
    with open(src) as file:
        inp = []
        for line in file.readlines():
            inp.append([float(i) for i in line.split()])
    return inp

def compute_dist_matrix(g):
    """
    Compute a matrix of Euclidean distances between all vertices
    :param g: list, input list of vertex coordinates
    :return: D, 2D np array of distances
    """

    D = np.zeros((len(g), len(g)))
    for i in range(len(g)):
        for j in range(len(g)):
            D[i, j] = D[j, i] = np.sqrt((g[i][0] - g[j][0])**2 + (g[i][1] - g[j][1])**2)
    return D

def tsp_dynamic(D):
    """
    Compute the minimum cost solution to the TSP problem given a distance matrix using a dynamic programming approach
    :param D: 2D nxn np array of distances between n nodes
    :return: float, cost of minimum cost tour
    """

    # Generate all possible subsets for each cardinality. Use frozenset so objects are hashable
    subsets = [[frozenset(s).union(frozenset([1])) for s in itertools.combinations(list(range(2, D.shape[0]+1)), n)] for n in range(1, D.shape[0])]
    subsets_flat = [frozenset([1])] + [item for sublist in subsets for item in sublist]

    # Dictionary for looking up the index of a given subset
    ss_dict = {subsets_flat[i]: i for i in range(len(subsets_flat))}

    # Array for storing recurrence results
    A = np.full((len(ss_dict), D.shape[0]), np.inf)
    A[0, 0] = 0
    i = 1
    # Iterate over possible cardinalities
    for SS_C in subsets:
        i += 1
        print(i / len(subsets))
        # Iterate over subsets with a given cardinality
        for S in SS_C:
            # Get array index for the subset
            s_j = ss_dict[S]
            # Look at all vertices in the set, save one
            for j in S - {1}:
                # Get array index of the set with j absent
                s_j_ = ss_dict[S - {j}]
                # Compute minimum path to add
                A[s_j, j-1] = min([A[s_j_, k-1] + D[k-1, j-1] for k in S - {j}])

    # Compute the minimum cost by adding the final edge back to home
    tsp_sol = min([A[-1, i] + D[0, i] for i in range(1, D.shape[0])])
    print('Minimum cost solution:', tsp_sol)
    return tsp_sol

if __name__ == "__main__":

    tsp_g = read_input("tsp_26_dist.txt")

    dist_matrix = np.array(tsp_g)

    #dist_matrix = np.array([[0, 10,15, 20], [10, 0, 25, 25], [15, 25, 0, 30], [20, 25, 30, 0]])

    tsp_dynamic(dist_matrix)


