import time

def read_input(src : str):
    """
    Helper function to read input txt file. First line the number of entries.
    Subsequent lines are the symbol weights
    Args:
        src: str, file path for the input

    Returns: list of symbol weights

    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append(int(line))
    return inp


def compute_mwis(pg: list):
    """
    Compute the maximum independent set of a weighted path graph passed as list. Employs dynamic programming
    implementation
    Args:
        pg: list, input path graph, entries are node weights

    Returns: set, the maximum idependent spanning set
    """

    # Copy the list for downstream mutation
    pg = pg.copy()

    # Initial max weights: empty graph and single node
    max_weights = [0, pg.pop(0)]

    # Forward pass; Set each cumulative weight
    while pg:
        nxt = pg.pop(0)
        # If the last cumulative weight is greater than including nxt, repeat the last weight
        if max_weights[-1] > (max_weights[-2] + nxt):
            max_weights.append(max_weights[-1])
        # Otherwise, compute a new cumulative weight and append it
        else:
            max_weights.append(max_weights[-2] + nxt)

    # Reverse pass; Work backwards through the cumulative weights. Include indices in the MWIS based on the decision
    # made in the foward pass.
    mwis = set()
    i = len(max_weights) - 1
    while i > 1:
        nxt = max_weights[i]
        # If the last weight is greater than the preceding one, element i must be in the MWIS, and i-1 isn't
        if nxt > max_weights[i-1]:
            mwis.add(i)
            i -= 2
        # Otherwise it isn't in the MWIS, and we move to the next.
        else:
            i -= 1

    # Add the first node from the graph if the second was not added at the end of the reverse pass
    if i == 1:
        mwis.add(i)
    return mwis



if __name__ == "__main__":

    # Source file for the input symbol weights
    source = "mwis.txt"

    # Build the graph
    graph = read_input(source)

    # Timing
    begin = time.time()

    # Comput MWIS
    mwis = compute_mwis(graph)

    print("MWIS computed in", time.time() - begin, "seconds")

    test_set = dict.fromkeys([1,2,3,4,17,117,517,997])
    for key in test_set:
        test_set[key] = (key in mwis)
    print(test_set)

