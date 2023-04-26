import time

def read_input(src : str):
    arr = []
    with open(src) as file:
        for l in file.readlines():
            arr.append(int(l))
    return arr

def compute_2sum(A : list, lw_bnd : int, up_bnd : int):

    # Construct dict hash table
    H = A

    pairs = 0

    for i in range(lw_bnd, up_bnd+1):
        print(i)
        for x in H:
            if i - x in H and i - x != x:
                pairs += 1
                break
    return pairs


if __name__ =="__main__":

    # Source file for input to the 2 sum computation
    source = "programming_prob-2sum.txt"

    # Read the input
    stream_in = read_input(source)

    begin = time.time()
    pairs = compute_2sum(stream_in, -10, 10)
    print("2Sum ran in:", time.time() - begin, "seconds")
    print(pairs)


