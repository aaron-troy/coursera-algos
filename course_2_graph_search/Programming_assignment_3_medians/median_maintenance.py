"""
Maintenance of a median computed from an incoming stream of numbers.

A dual heap algorithm is used. One heap is max heap with the smallest n / 2 numbers for n numbers seen
thus far. The other is a min heap with the larger half of numbers streamed thus far. Maintaining these
invariants, along with those of a min and max heap, it follows that the median at any given time is:

-- The root of the larger heap, if n is odd
-- The average of the roots of the two heaps, is n is even.

This approach  runs in Nlog(N), and is considerably faster than a naive, loop based approach.
"""

import time, heap
import numpy as np

def read_file(source : str):
    """
    Helper function for reading the input file, returned as an array
    """
    arr = []
    with open(source) as file:
        for l in file.readlines():
            arr.append(int(l))
    return arr

def get_median_stream(arr : list):
    """
    Produce a stream of median values using min heap and max heap data structures
    :param arr: Input array
    :return: M, stream of medians. I.e. M[0] is the median of arr[0],
    M[1] is the median value of arr[0:2], M[2] --> arr[0:3], etc.
    """
    # Min and max heaps. Max heap has the smaller half of numbers seen so far, min heap the rest
    H_low = heap.MaxHeap()
    H_high = heap.MinHeap()

    M = [arr[0]]

    # Start with the lower heap larger
    H_low.insert(arr[0])

    for a in arr[1:]:
        # If the heaps aren't the same size, we need to add to the higher one, a min heap
        if H_low.heap_size > H_high.heap_size:
            # If the entry to add is larger the high heap's root, just add it
            if a >= H_low.heap_arr[1]:
                H_high.insert(a)
            # Otherwise, transfer the root from the lower heap, add to the lower heap
            else:
                H_high.insert(H_low.pop_root())
                H_low.insert(a)
            # Computer median. Number seen so far is even.
            M.append((H_low.heap_arr[1]+H_high.heap_arr[1]) / 2)
        else:
            # Choose where to add, leaving the lower heap larfer
            if a > H_high.heap_arr[1]:
                H_low.insert(H_high.pop_root())
                H_high.insert(a)
            else:
                H_low.insert(a)
            # Computer median. Number seen so far is odd.
            M.append(H_low.heap_arr[1])
    return M

if __name__ =="__main__":

    # Source file for the input graph
    source = "Median.txt"
    # Build the graph
    G = read_file(source)

    # Timing
    begin = time.time()
    medians = get_median_stream(G)
    print("Heap based median stream compute in", time.time() - begin, "seconds")
    # Sum, modulo 10000, for Coursera assignment
    print(sum(medians) % 10000)

    np_medians = []
    begin = time.time()
    for i in range(1,len(G)):
        np_medians.append(np.median(G[0:i]))
    np_medians.append(np.median(G))
    print("Numpy based median stream computed in", time.time() - begin, "seconds")
    print((sum(np_medians)) % 10000)

