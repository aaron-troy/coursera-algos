"""
Greedy algorithms for scheduling a list of input tasks, each with an associated weight and length.
"""
import time
def read_file(src : str):
    """
    Helper function to read input file for job scheduling. Input is txt file, first row contains the number of jobs,
    subsequent rows have a job weight and length
    Args:
        src: file path for the input file
    Returns: dict, job ID as key to a list with weight and length as entries
    """
    d = {}
    with open(src) as file:
        i = 0
        for l in file.readlines()[1:]:
            d[i] = [int(j) for j in l.split()]
            i += 1
    return d

def greedy_difference_schedule(jobs: dict):
    """
    Implementation of greedy scheduling algorithm, scheduling based on difference between task
    weight and length. Computes the total weighted completion time for the resulting schedule.
    Result is not optimal.
    """
    # Assemble a list of tuples, sorted by decreasing difference, then weight
    sch = []
    for i, (w, l) in jobs.items():
        sch.append((i, w, l, w-l))
    sch_sorted = sorted(sch, key=lambda x: (-x[3], -x[1]))

    # Compute the total weighted completion time
    comp_times = []
    t = 0
    for i, w, l, _ in sch_sorted:
        comp_times.append(w * (l + t))
        t += l
    return sum(comp_times)

def greedy_quotient_schedule(jobs: dict):
    """
    Implementation of greedy scheduling algorithm, scheduling based on decreasing weight / lenght quotient
    Computes the total weighted completion time for the resulting schedule. Result is not optimal.
    """
    # Assemble a list of tuples, sorted by decreasing difference, then weight
    sch = []
    for i, (w, l) in jobs.items():
        sch.append((i, w, l, w / l))
    sch_sorted = sorted(sch, key=lambda x: (-x[3]))

    # Compute the total weighted completion time
    comp_times = []
    t = 0
    for i, w, l, _ in sch_sorted:
        comp_times.append(w * (l + t))
        t += l
    return sum(comp_times)


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


