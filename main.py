from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.formula import WCNFPlus
import numpy as np
import random
import olll

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
def mapvalues(n, i, j):
    if i < j:
        return ((n+1) + (j-i) + (((i-1)*(2*n-i))//2))

def make_hard_clauses(n):
    count = n+2
    hardclauses = [[n+1]]
    for i in range (1 , n+1):
        for j in range(i+1, n+1):
            hardclauses.append([-count, i])
            hardclauses.append([-count, j])
            hardclauses.append([count, -i, -j])
            count += 1

            for k in range(j+1, n+1):
                yij = mapvalues(n, i, j)
                yjk = mapvalues(n, j, k)
                yik = mapvalues(n, i, k)
                hardclauses.append([-yij, -yjk, yik])

    return hardclauses

def find_d(ip_cache, n):
    d = 0
    for i in range(1, n+1):
        for j in range(i, n+1):
            x = abs(ip_cache[(i, i)] - 2*ip_cache[(i, n+1)])
            y = abs(2*ip_cache[(i, j)])
            d = max(d, x, y)
    return d+10

def make_soft_clauses(ip_cache, n):
    print(ip_cache)
    count = n+2
    clauses = []
    d = find_d(ip_cache, n)
    print("d = ", d)
    for i in range(1, n+1):
        wxi = d + (2*ip_cache[(i, n+1)]) - ip_cache[(i, i)]
        clauses.append([i, wxi])
        clauses.append([-i, d])
        for j in range(i+1, n+1):
            wxj = d - 2*ip_cache[(i, j)]
            clauses.append([count, wxj])
            clauses.append([-count, d])
            count += 1


            # blah = d + (2*ip_cache[(i, n+1)]) - ip_cache[(i, i)] + (2*ip_cache[(j, n+1)]) - ip_cache[(j, j)] + d
            # if blah >= d//2:
            #     wxj = d - 2*ip_cache[(i, j)]
            #     clauses.append([count, wxj])
            #     clauses.append([-count, d])
            #     count += 1

    return clauses, d

# def cardconstraint(n):
#     clauses = []
#     for i in range(1, n+1):
#         clauses.append([[i, -i], 1])
#     return clauses
#================================================================================
def run_maxsat(n, basis, p, q):
    with open(f"out_{n}.txt", 'a') as file:
        wcnf = WCNFPlus()
        ip_cache = inner_product_cache(basis, n)

        hardclauses = make_hard_clauses(n)
        softclauses,d = make_soft_clauses(ip_cache, n)
        # cardclauses = cardconstraint(n*(n-1)//2)
        
        # for c in cardclauses:
        #     wcnf.append(c, is_atmost=True)

        for c in hardclauses:
            wcnf.append(c)

        for c in softclauses:
            wcnf.append(c[:-1], weight=c[-1])

        rc2 = RC2(wcnf,verbose=2, adapt= True, exhaust=True, minz=True, incr=True, solver="g3")
        # ip_cache = inner_product_cache(basis, n)

        # hardclauses = make_hard_clauses(n)
        # softclauses,d = make_soft_clauses(ip_cache, n)
        print(hardclauses)
        print("hc =" ,len(hardclauses))
        print(softclauses)
        print("sc =", len(softclauses))

        # for c in hardclauses:
        #     rc2.add_clause(c)

        # for c in softclauses:
        #     rc2.add_clause(c[:-1], weight=c[-1])

        # print(rc2.get_core())
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
    seed = 4
    for i in range(seed, seed+1):
        basis, p, q = random_basis(n, n, seed=i)
        print("basis = ", basis)
        print("target = ", basis[-1])
        print("p =", p, "q =", q)
        try:
            signal.alarm(120)
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
    n = 17
    n_values = list(range(n, n+1))

    with mp.Pool(processes=num_processes) as pool:
        pool.map(main_func, n_values)