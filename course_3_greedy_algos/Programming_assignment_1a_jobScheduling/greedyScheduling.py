"""
Greedy algorithms for scheduling a list of input tasks, each with an associated weight and length.
"""
import time
def read_file(source : str):
    """
    Helper function for reading the input file, returned as a dict unique ids to job weights and lengths.
    The input is a text file, with the first line containing the number of jobs.
    Each subsequent line has 2 integers, corresponding the job weight and length.
    """
    D = {}
    with open(source) as file:
        i = 0
        for l in file.readlines()[1:]:
            D[i] = [int(j) for j in l.split()]
            i += 1
    return D

def greedy_difference_schedule(J : dict):
    """
    Implementation of greedy scheduling algorithm, scheduling based on difference between task
    weight and length. Computes the total weighted completion time for the resulting schedule.
    Result is not optimal.
    """
    # Assemble a list of tuples, sorted by decreasing difference, then weight
    sch = []
    for i, (w,l) in J.items():
        sch.append((i,w,l,w-l))
    sch_sorted = sorted(sch, key=lambda x: (-x[3], -x[1]))

    # Compute the total weighted completion time
    compTimes = []
    t = 0
    for i, w, l, _ in sch_sorted:
        compTimes.append(w * (l + t))
        t += l
    return sum(compTimes)

def greedy_quotient_schedule(J : dict):
    """
    Implementation of greedy scheduling algorithm, scheduling based on decreasing weight / lenght quotient
    Computes the total weighted completion time for the resulting schedule. Result is not optimal.
    """
    # Assemble a list of tuples, sorted by decreasing difference, then weight
    sch = []
    for i, (w, l) in J.items():
        sch.append((i, w, l, w / l))
    sch_sorted = sorted(sch, key=lambda x: (-x[3]))

    # Compute the total weighted completion time
    compTimes = []
    t = 0
    for i, w, l, _ in sch_sorted:
        compTimes.append(w * (l + t))
        t += l
    return sum(compTimes)


if __name__ =="__main__":

    # Source file for the input graph
    source = "jobList.txt"
    # Read the input
    jobs = read_file(source)
    # Timing
    begin = time.time()
    # Compute greedy scheduling using greedy difference
    compTime = greedy_difference_schedule(jobs)
    print('Greedy difference ran in', time.time() - begin, "seconds")
    print('Total weighted completion time:', compTime)


    # Timing
    begin = time.time()
    # Compute greedy scheduling using greedy quotient
    compTime = greedy_quotient_schedule(jobs)
    print('Greedy quotient ran in', time.time() - begin, "seconds")
    print('Total weighted completion time:', compTime)


