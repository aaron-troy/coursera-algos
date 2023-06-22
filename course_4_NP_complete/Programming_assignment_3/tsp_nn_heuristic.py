import numpy as np
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
        for line in file.readlines()[1:]:
            inp.append([float(i) for i in line.split()[1:]])
    return inp

def compute_sqr_dist_matrix(g):
    """
    Compute a matrix of squared distances between vertices. Squared distance is used to avoid computing roots.
    """
    D = np.zeros((len(g), len(g)))
    for i in range(len(g)):
        for j in range(len(g)):
            D[i, j] = ((g[i][0] - g[j][0])**2 + (g[i][1] - g[j][1])**2)
    return D

def tsp_nn_heuristic(D):
    """
    Estimate the cost of the TSP problem using the nearest neighbor heuristic.
    Args:
        D: 2D np.array, squared Euclidean distance between each pair of cities/

    Returns: float, cost of the TSP
    """

    cost = 0
    i = k = 0
    visit_count = 0

    verts = set(list(range(D.shape[0])))
    visited = set([i])

    while visited != verts:
        # Compute distance to NN that is unvisited
        dist = min(D[i, ~np.isin(np.arange(len(D)), list(visited))])
        # Get the index for nearest neighbour not yet visited
        j = np.argwhere((D[i, :] * ~np.isin(np.arange(len(D)), list(visited))) == dist)[0][0]

        # Add the cost, Euclidean distance
        cost += np.sqrt(dist)

        # Add to the visited set
        visited.add(j)
        i = j

        visit_count += 1
        print(visit_count)

    # Cost of returning home
    cost += np.sqrt(D[i, 0])

    print('Total cost:', cost)

    return cost



if __name__ == "__main__":

    tsp_g = read_input("nn.txt")

    dist_matrix = compute_sqr_dist_matrix(tsp_g)

    cProfile.run('tsp_nn_heuristic(dist_matrix)')

