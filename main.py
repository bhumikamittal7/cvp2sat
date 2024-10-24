from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random
#================================================================================
def random_basis(n, m):
    """
    generate n linearly independent vectors of dimension m, B = (b1, b2, ..., bn) in R^{m*n}
    """
    basis = np.eye(n, m, dtype=int)
    for i in range(n):
        for j in range(i , n):
            scalar = random.randint(0, 50)
            basis[i] += scalar * basis[j]
    
    # t = []
    # for i in range(m):
    #     t.append(basis[0][i])
    p,q = random.randint(0, n-1), random.randint(0, n-1)
    print(p+1, q+1)
    t = []
    for i in range(m):
        t.append(basis[p][i] + basis[q][i] + np.random.randint(1, 2))
    return np.vstack([basis, t]).tolist()

# def inner_product(basis, i, j):
#     """
#     inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
#     """
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
#     d = 100
#     clauses = []
#     for i in range(1, n+1):
#         wxi = d + (inner_product(basis, i, n+1)//n)
#         wxinot = d - ((n-1)*(inner_product(basis, i, n+1)//n))
#         # print(i, wxi)
#         clauses.append([i, wxi])
#         clauses.append([-i, wxinot])

#         for j in range(i+1, n+1):
#             wxj = d - inner_product(basis, i, j) + (inner_product(basis, i, n+1)//n) + (inner_product(basis, j, n+1)//n)
#             wxixj = d + (inner_product(basis, i, n+1)//n) + (inner_product(basis, j, n+1)//n)
#             # print(i, j, wxj, wxixj)
#             clauses.append([count, wxj])
#             clauses.append([-i, -j, wxixj])
#             count += 1
#     return clauses

def make_soft_clauses(ip_cache, n):
    count = n+2
    d = 99999
    clauses = []
    for i in range(1, n+1):
        wxi = d + (ip_cache[(i, n+1)]//n)
        wxinot = d - ((n-1)*(ip_cache[(i, n+1)]//n))
        # print(i, wxi)
        clauses.append([i, wxi])
        clauses.append([-i, wxinot])

        for j in range(i+1, n+1):
            wxj = d - ip_cache[(i, j)] + (ip_cache[(i, n+1)]//n) + (ip_cache[(j, n+1)]//n)
            wxixj = d + (ip_cache[(i, n+1)]//n) + (ip_cache[(j, n+1)]//n)
            # print(i, j, wxj, wxixj)
            clauses.append([count, wxj])
            clauses.append([-i, -j, wxixj])
            count += 1
    return clauses
#================================================================================
def print_file(filename, rc2):
    with open(filename, 'w') as file:
        for model in rc2.enumerate():
            file.write(f"Model: {model}, Cost: {rc2.cost}\n")
        file.write(f"Time taken: {rc2.oracle_time()}\n")

def run_maxsat(n, basis):
    rc2 = RC2(WCNF())

    ip_cache = inner_product_cache(basis, n)

    hardclauses = make_hard_clauses(n)
    softclauses = make_soft_clauses(ip_cache, n)

    print(hardclauses)
    print(softclauses)

    for c in hardclauses:
        rc2.add_clause(c)

    for c in softclauses:
        rc2.add_clause(c[:-1], weight=c[-1])

    rc2.compute()
    filename = 'mod_output.txt'
    print_file(filename, rc2)
    return rc2.oracle_time()
#================================================================================
n = 5
basis = random_basis(n, n)

print("basis = ", basis)
print("target = ", basis[-1])
oracle_time = run_maxsat(n, basis)
print(oracle_time)
