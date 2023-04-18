"""

"""

import time, heap

def read_file(source : str):

    arr = []

    with open(source) as file:
        for l in file.readlines():
            arr.append(int(l))
    return arr

def get_median_stream(arr : list):

    H_low = heap.MaxHeap()
    H_high = heap.MinHeap()

    M = [arr[0]]
    temp = M.copy()

    H_low.insert(arr[0])

    for a in arr[1:]:
        if min(H_high.heap_arr[1:]) != H_high.heap_arr[1]:
            print('stop')
        if H_low.heap_size > H_high.heap_size:
            if a >= H_low.heap_arr[1]:
                H_high.insert(a)
            else:
                H_high.insert(H_low.pop_root())
                H_low.insert(a)
            M.append(H_low.heap_arr[1])
        else:
            if a > H_high.heap_arr[1]:
                H_low.insert(H_high.pop_root())
                H_high.insert(a)
            else:
                H_low.insert(a)
            M.append(H_low.heap_arr[1])

        temp.append(a)
        temp.sort()
        if len(temp) % 2 == 0:
            gt = temp[int(len(temp) / 2) - 1]
        else:
            gt = temp[int((len(temp) + 1) / 2) - 1]
        if H_high.heap_arr[1] < H_low.heap_arr[1]:
            print('stop')
    return M

if __name__ =="__main__":
    # Timing
    begin = time.time()

    # Source file for the input graph
    source = "Median.txt"
    # Build the graph
    G = read_file(source)
    medians = get_median_stream(G)

    # Sum, modulo 10000, for Coursera assignment
    print(sum(medians) % 10000)

