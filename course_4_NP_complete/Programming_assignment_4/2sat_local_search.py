import numpy as np
import random
import cProfile

def read_input(src: str):
    """
    Helper function to read input txt file.
    Args:
        src: str, file path for the input

    Returns: inp, array of the input constraints
    """
    with open(src) as file:
        inp = []
        for line in file.readlines()[1:]:
            inp.append([int(i) for i in line.split()])
    return inp

def check_assignment(const: list, agn: list):
    res = np.array([-1])
    for c in const:
        a_1 = (agn[np.abs(c[0])] == (c[0] >= 0))
        a_2 = (agn[np.abs(c[1])] == (c[1] >= 0))
        if not (a_1 or a_2):
            return random.choice([np.abs(c[0]), np.abs(c[1])])
    return -1


def two_sat_local_srch(constraints: list, n: int):

    for j in range(int(np.ceil(np.log2(n)))):
        #print(j / np.log2(n))
        assignment = np.array([None] + [random.getrandbits(1) for i in range(n)])
        for k in range(2*(n**2)):
            print(k)
            chk = check_assignment(constraints, assignment)
            if chk < 0:
                return assignment
            else:
                assignment[chk] = 1 - assignment[chk]

    print('Unsatisfiable constraint!')
    return None



if __name__ == "__main__":

    two_sat_in = read_input("2sat_1.txt")

    two_sat_local_srch(two_sat_in, len(two_sat_in))

