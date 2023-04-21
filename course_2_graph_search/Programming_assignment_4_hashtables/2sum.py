

def read_input(src : str):
    arr = []
    with open(src) as file:
        for l in file.readlines():
            arr.append(int(l))
    return arr

def compute_2sum(A : list, lw_bnd : int, up_bnd : int):

    # Construct dict hash table
    H = {}

    pairs = 0

    for i in range(lw_bnd, up_bnd+1):
        for x in A:
            if (i - x) in H and i - x != x:
                pairs += 1
                H[x] = x
                break
            else:
                H[x] = x
    return pairs


if __name__ =="__main__":

    # Source file for input to the 2 sum computation
    source = "programming_prob-2sum.txt"

    # Read the input
    stream_in = read_input(source)

    pairs = compute_2sum(stream_in, -20, 0)

    print(pairs)


