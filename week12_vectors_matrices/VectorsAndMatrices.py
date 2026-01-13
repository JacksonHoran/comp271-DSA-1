# Jackson Horan
# 10/16/25
# Vectors and Matricies - comparison of determinant and gaussian

import random
import time

def minor(A, row, col):
    """Computes a minor matrix from the major matrix.

    Args:
        A ( list[list] ): The major matrix for which the minor is to be computed
        from.
        row (int): The index of the row to remove.
        col (int): The index of the collumn to remove.

    Returns:
        list[list]: A minor of matrix A
    """
    return [row[:col] + row[col+1:] for row in (A[:row] + A[row+1:])]

def determinant(A) -> int:
    """Compute the determinant of a square matrix A (list of lists).

    Args:
        A ( list[list] ): The sqaure matrix for which the determinent is to be
        computed

    Returns:
        int: The determinent of the sqaure matrix.
    """
    n = len(A)
    det = 0
    # Trivial case
    if n == 1:
        det = A[0][0]
    # Base case
    elif n == 2:
        det = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    else:
        for c in range(n):
            det += ((-1)**c) * (A[0][c]) * determinant(minor(A, 0, c))
    return det

def randomMatrix(n: int) -> list[list]:
    """Return a sqaure matrix of n x n diomension with random values between 
    0 and 20

    Args:
        n (int): The dimension n for an n x x matrix.

    Returns:
        list[list]: The random n x n matrix.
    """
    return [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]

def randomVector(n: int) -> list:
    """Return a random vector with values between 1 and 20.

    Args:
        n (int): The dimension of the vector.

    Returns:
        list: An n x 1 vector.
    """
    return [random.randint(1, 20) for _ in range(n)]


def randomTest() -> tuple[int, int]:
    """Return the maximum dimension, n, for which the determinent of an n x n
    matrix can be computed in 1 minute.

    Returns:
        n (int): The maximum dimension of the sqaure matrix determinent.
        total_time (int): The nanosecond time to compute the maximum dimension
        determinent. 
    """
    total_time = 0
    n = 1
    while total_time < 1000000000: 
        matrix = randomMatrix(n)
        start = time.time_ns()
        determinant(matrix)
        end = time.time_ns()
        total_time = end-start
        n += 1
    return n, total_time

def gauss(A: list[list], b):
    """Solve the linear system Ax = b using Gaussian elimination.

    Args:
        A (list[list]): An n x n coefficient matrix representing the system.
        b (list): An n-dimensional right-hand-side vector.

    Returns:
        list: the n dimension solution vector to the system.
    """
    m = len(A)
    for k in range(0, m-1):
        for i in range(k + 1, m):
            mik = A[i][k] / A[k][k]
            for j in range(k, m):
                A[i][j] = A[i][j] - mik * A[k][j]
            b[i] = b[i] - mik * b[k]
    x = [0] * m
    for i in range(m - 1, -1, -1):
        s = 0
        for j in range(i + 1, m):
            s = s + A[i][j] * x[j]
        x[i] = (b[i] - s) / A[i][i]
    return x

def prettyPrint(A):
    for row in A:
        print(row)
    print()

if __name__ == "__main__":
    sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for n in sizes:
        Adet = randomMatrix(n)
        Agauss = randomMatrix(n)
        bgauss = randomVector(n)

        start_det = time.time_ns()
        determinant(Adet)
        end_det = time.time_ns()
        det_time = end_det - start_det

        start_gauss = time.time_ns()
        gauss(Agauss, bgauss)
        end_gauss = time.time_ns()
        gauss_time = end_gauss - start_gauss

        print(f"{n},{det_time},{gauss_time}")


