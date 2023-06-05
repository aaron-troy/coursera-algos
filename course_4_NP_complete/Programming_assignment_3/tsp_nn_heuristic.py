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
        for line in file.readlines()[1:10000]:
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

    cost = 0
    i = k = 0
    visit_count = 0

    verts = set(list(range(D.shape[0])))
    visited = set([i])

    while visited != verts:
        dist = min(D[i, ~np.isin(np.arange(len(D)), list(visited))])
        j = np.argwhere(D[i, :] == dist)[k][0]
        while j in visited:
            k += 1
            j = np.argwhere(D[i, :] == dist)[k][0]
        k = 0
        cost += dist
        visited.add(j)
        i = j

        visit_count = + 1
        print(visit_count)

    cost += D[i, 0]
    cost = np.sqrt(cost)

    print('Total cost:', cost)

    return cost



if __name__ == "__main__":

    tsp_g = read_input("nn.txt")

    dist_matrix = compute_sqr_dist_matrix(tsp_g)

    cProfile.run('tsp_nn_heuristic(dist_matrix)')

