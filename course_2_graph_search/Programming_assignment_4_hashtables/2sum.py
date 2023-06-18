"""
Computation of the number of integers within two bounds that have a 2 sum pair within a given list.
Implemented using native python dict hashtable -- this is quite slow. As far as I'm aware this is about
the best we can do in Python. The dict implementation is still light years faster than a naive list approach.
"""

import time
def read_input(src : str):
    """
    Read input txt file -- one integer per row.
    :param src: path to input file
    :return: list of numbers from input file
    """
    arr = []
    with open(src) as file:
        for l in file.readlines():
            arr.append(int(l))
    return arr

def compute_2sum(a: list, lw_bnd: int, up_bnd: int):
    """
    Compute the number of integers within a lower and upper bound that have a 2sum pair in a given list of
    numbers. Implemented using a dict hashtable - for each entry, we try to lookup the corresponding entry
    for a 2 sum.
    :param a: list of entries to compute 2sum pairs for
    :param lw_bnd: lower bound for 2sum range
    :param up_bnd: upper bound for 2sum range
    :return: number of pairs
    """
    # Construct dict hash table
    h = dict.fromkeys(a)
    num_of_pairs = 0

    for i in range(lw_bnd, up_bnd+1):
        print(i)
        for x in h:
            if i - x in h and i - x != x:
                num_of_pairs += 1
                break
    return num_of_pairs


if __name__ =="__main__":

    # Source file for input to the 2 sum computation
    source = "programming_prob-2sum.txt"

    # Read the input
    stream_in = read_input(source)

    begin = time.time()
    pairs = compute_2sum(stream_in, -10, 10)
    print("2Sum ran in:", time.time() - begin, "seconds")
    print(pairs)


