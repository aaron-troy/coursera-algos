
import time


def read_file(source : str):
    """
    Helper function for reading the input file, returned as an array
    """
    D = {}
    with open(source) as file:
        i = 0
        for l in file.readlines()[1:]:
            D[i] = [int(j) for j in l.split()]
            i += 1
    return D

def greedy_difference(J : dict):
    return 0

if __name__ =="__main__":

    # Source file for the input graph
    source = "jobList.txt"
    # Build the graph
    jobs = read_file(source)
    print(jobs.values())
    # Timing
    begin = time.time()


