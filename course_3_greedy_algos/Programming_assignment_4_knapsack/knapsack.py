"""
Compute the optimal value for the knapsack problem. Includes both iterative and recursive dynamic programming solutions. 
The iterative approach is preferable for small inputs, but becomes infeasible at larger scales. 
"""
import sys, time, threading


def read_input(src : str):
    """
    Helper function for reading input txt file for knapsack problems. Input is formatted with the first line
    containing integers for the total knapsack size and number of available items. Subsequent lines are the
    value and weight of each item.

    Args:
        src: str, file path to input

    Returns:
        size: int, total knapsack size
        items: dict of lists, each key maps to a list with an item value and weight as entries 0 and 1
    """
    with open(src) as file:
        items = []
        for line in file.readlines():
            items.append([int(i) for i in line.split()])
        size, _ = items.pop(0)
        items = {i+1 : items[i] for i in range(len(items))}
    return size, items

def max_knapsack_value_recurse(items: dict, W: int, end, sols: dict = {}):
    """
    Attempt at recursive implementation for larger inputs. Seems to run a bit slower than the iterative approach, at
    least for small inputs.
    Args:
        items: dict of lists, each key maps to a list with an item value and weight as entries 0 and 1
        W: int, knapsack size
        end: int, key to start from.
        sols: dict, for internal recursive use only

    Returns: dict, values are the maximum value for a key, key is tuple of knapsack size and key of the last item added
    """
    # Get the value and weight of the next item
    value, weight = items[end]

    # If we are at the lowest key, the entry is just the value
    if end == 1:
        if weight < W:
            sols[(W, end)] = value
        else:
            sols[(W, end)] = 0
        return sols

    # If we haven't yet computed for the preceding key, recurse with the same size
    if (W, end - 1) not in sols:
        sols = max_knapsack_value_recurse(items, W, end - 1, sols=sols)
    case_1 = sols[(W, end - 1)]

    # If the item is too large to fit in the remaining space, retain the solution with fewer items
    if weight > W:
        sols[(W, end)] = case_1
        return sols
    # Otherwise, compute what the value would be if we added the item
    else:
        if (W - weight, end - 1) not in sols:
            sols = max_knapsack_value_recurse(items, W - weight, end - 1, sols=sols)
        case_2 = sols[(W - weight, end - 1)] + value

        sols[(W, end)] = max(case_1, case_2)
    return sols

def max_knapsack_value_iter(items: dict, W: int):
    """
    Compute the maximum attainable knapsack value for a list of items and maximum capacity using an iterative
    dynamic programming approach.
    Args:
        items: dict of lists, each key maps to a list with an item value and weight as entries 0 and 1
        W: int, maximum knapsack capacity

    Returns: max_val, int. the maximum knapsack value attainable
    """
    # Knapsack sizes; start from the smallest item
    sizes = list(range(W))
    # Empty array to populate
    A = [[0] * len(sizes)]
    keys = list(items.keys())
    keys.sort()
    for k in keys:
        value, weight = items[k]
        S = []
        for j in range(len(sizes)):
            if weight > sizes[j]:
                S.append(A[k-1][j])
            else:
                S.append(max(A[k-1][j], (A[k-1][sizes[j] - weight] + value)))
        A.append(S)
    return A[-1][-1]

def threaded_knapsack(inputs : dict, W: int):
    """
    Separate function for running the recursive solution on a custom thread with increased stack size.
    """
    begin = time.time()

    # Compute again, using the recursive implementation
    recurse_solutions = max_knapsack_value_recurse(inputs, W, max(inputs.keys()), sols={})
    max_val_recurse = recurse_solutions[(W, len(inputs))]

    print("Recursive knapsack computation ran in", time.time() - begin, "seconds for input of size", W, ",", len(inputs))
    print("Max value:", max_val_recurse)


if __name__ == "__main__":

    # Source file for the input symbol weights
    source = "knapsack1.txt"

    # Read the input
    W, inputs = read_input(source)

    # Timing
    begin = time.time()

    # Compute the maximum knapsack value, first using the standard itrerative approach
    max_val_iter = max_knapsack_value_iter(inputs, W)

    print("Iterative knapsack computation ran in", time.time() - begin, "seconds for input of size", W, "x", len(inputs))
    print("Max value:", max_val_iter)

    # Timing
    begin = time.time()

    # Compute again, using the recursive implementation
    recurse_solutions = max_knapsack_value_recurse(inputs, W, max(inputs.keys()))
    max_val_recurse = recurse_solutions[(W, len(inputs))]

    print("Recursive knapsack computation ran in", time.time() - begin, "seconds for input of size", W, "x", len(inputs))
    print("Max value:", max_val_recurse)

    if max_val_recurse != max_val_iter:
        print('Value discrepancy!')

    # Try now with the large input. The iterative approach is not feasible here.
    source = "knapsack_big.txt"

    # Read the input
    W, inputs = read_input(source)

    # Increase recursion limit
    sys.setrecursionlimit(2 ** 20)

    # Create a custom thread with increased stack size to avoid stack overflow.
    threading.stack_size(0x2000000)
    thread = threading.Thread(target=threaded_knapsack(inputs, W))
    thread.start()
    thread.join()




