import cProfile
def karatsuba(num1: int, num2: int):
    """
    Perform multiplication of two integers using Karatsuba's recursive algorithm.
    :param num1: integer 1
    :param num2: integer 2
    :return: product of num1 and num2
    """

    # Base case for small numbers
    if ((num1 < 10 ) or num2 < 10):
        return num1 * num2

    N = min(len(str(num1)), len(str(num2)))
    m = int(N / 2)

    # Split the number in two
    x1 = int(str(num1)[:-m])
    x0 = int(str(num1)[-m:])

    y1 = int(str(num2)[:-m])
    y0 = int(str(num2)[-m:])

    # Perform recursive multiplications
    z0 = karatsuba(x0, y0)
    z1 = karatsuba((x1 + x0), (y1 + y0))
    z2 = karatsuba(x1, y1)

    # Combine the results
    return z2 * (10**(2*m)) + ((z1 - z2 - z0) * (10**m)) + z0



if __name__ == '__main__':

    i_1 = 3141592653589793238462643383279502884197169399375105820974944592
    i_2 = 2718281828459045235360287471352662497757247093699959574966967627

    # Run using the recursive Karatsuba's algorithm
    cProfile.run("print(karatsuba(i_1, i_2))")

