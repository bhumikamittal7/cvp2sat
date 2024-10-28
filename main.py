from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random

import signal
import sys

import multiprocessing as mp

def handler(signum, frame):
    raise TimeoutError("Function execution exceeded the time limit.")

#================================================================================
def random_basis(n, m, seed=None):
    """
    generate n linearly independent vectors of dimension m, B = (b1, b2, ..., bn) in R^{m*n}
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    basis = np.eye(n, m, dtype=int)
    for i in range(n):
        for j in range(i , n):
            scalar = random.randint(-50, 50)
            basis[i] += scalar * basis[j]
    
    p,q = random.randint(0, n-1), random.randint(0, n-1)
    # print("ans: ", p+1, q+1)
    t = []
    for i in range(m):
        t.append(basis[p][i] + basis[q][i] + np.random.randint(1, 2))
    return np.vstack([basis, t]).tolist(), p+1, q+1

# def inner_product(basis, i, j):
#     return np.dot(basis[i-1], basis[j-1])

def inner_product_cache(basis, n):
    """
    precompute all inner products between basis vectors
    """
    cache = {}
    for i in range(1, n + 2):
        for j in range(i, n + 2):
            cache[(i, j)] = np.dot(basis[i - 1], basis[j - 1])
            cache[(j, i)] = cache[(i, j)]
    return cache
#================================================================================
def make_hard_clauses(n):
    count = n+2
    hardclauses = [[n+1]]
    for i in range (1 , n+1):
        for j in range(i+1, n+1):
            hardclauses.append([-count, i])
            hardclauses.append([-count, j])
            hardclauses.append([count, -i, -j])
            count += 1
    return hardclauses

# def make_soft_clauses(basis, n):
#     count = n+2
#     d = 9999
#     clauses = []
#     for i in range(1, n+1):
#         wxi = d + (2*inner_product(basis, i, n+1)) - inner_product(basis, i, i)
#         clauses.append([i, wxi])
#         clauses.append([-i, d])
#         for j in range(i+1, n+1):
#             wxj = d - (2*inner_product(basis, i, j))
#             clauses.append([count, wxj])
#             clauses.append([-count, d])
#             count += 1
#     return clauses

def find_d(ip_cache, n):
    d = 0
    for i in range(1, n+1):
        for j in range(i, n+1):
            x = abs(ip_cache[(i, i)] - 2*ip_cache[(i, n+1)])
            y = abs(2*ip_cache[(i, j)])
            d = max(d, x, y)
    return d+10

def make_soft_clauses(ip_cache, n):
    count = n+2
    clauses = []
    d = find_d(ip_cache, n)
    # print("d = ", d)
    for i in range(1, n+1):
        wxi = d + (2*ip_cache[(i, n+1)]) - ip_cache[(i, i)]
        clauses.append([i, wxi])
        clauses.append([-i, d])
        for j in range(i+1, n+1):
            wxj = d - 2*ip_cache[(i, j)]
            clauses.append([count, wxj])
            clauses.append([-count, d])
            count += 1
    return clauses, d
#================================================================================
# def print_file(filename, rc2):
#     with open(filename, 'w') as file:
#         for model in rc2.enumerate():
#             file.write(f"Model: {model}, Cost: {rc2.cost}\n")
#         file.write(f"Time taken: {rc2.oracle_time()}\n")

#================================================================================
def run_maxsat(n, basis, p, q):
    with open(f"out_{n}.txt", 'a') as file:
        rc2 = RC2(WCNF())
        ip_cache = inner_product_cache(basis, n)

        hardclauses = make_hard_clauses(n)
        softclauses,d = make_soft_clauses(ip_cache, n)
        # print(hardclauses)
        # print(softclauses)

        for c in hardclauses:
            rc2.add_clause(c)

        for c in softclauses:
            rc2.add_clause(c[:-1], weight=c[-1])

        # print("=====================================================================")
        file.write(f"n = {n}\n")
        file.write(f"d = {d}\n")
        file.write(f"ans = {p}, {q}\n")
        file.write(f"model: {rc2.compute()}\n")
        file.write(f"cost: {rc2.cost}\n")
        file.write(f"Oracle time: {rc2.oracle_time()}\n")
        file.write("=====================================================================\n")

    return 1
#================================================================================
signal.signal(signal.SIGALRM, handler)

def main_func(n):
    seed = 42
    for i in range(seed, seed+10):
        basis, p, q = random_basis(n, n, seed=i)
        # print("basis = ", basis)
        # print("target = ", basis[-1])
        try:
            signal.alarm(3600)
            run_maxsat(n, basis, p, q)
        except TimeoutError:
            with open(f"out{n}.txt", "a") as file:
                file.write(f"TimeoutError: Skipping n = {n} as it exceeded the time limit of 1 hr.")
        finally:
            signal.alarm(0)
#================================================================================
if __name__ == '__main__':
    num_processes = mp.cpu_count()
    print("number of cpu cores: ", num_processes)
    # print("=====================================================================")

    n_values = list(range(5, 7))

    with mp.Pool(processes=num_processes) as pool:
        pool.map(main_func, n_values)

# for n in range(5, 6):
#     main_func(n)
