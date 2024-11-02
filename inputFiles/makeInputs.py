from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random

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


def main_func(n):
    seed = 42
    basis, p, q = random_basis(n, n, seed=seed)
    # print("basis = ", basis)
    # print("target = ", basis[-1])
    ip_cache = inner_product_cache(basis, n)

    hardclauses = make_hard_clauses(n)
    softclauses,d = make_soft_clauses(ip_cache, n)
    # print("hardclauses = ", hardclauses)
    # print("softclauses = ", softclauses)
    # print("d = ", d)
    # print("p = ", p)
    # print("q = ", q)
    return hardclauses, softclauses, d, p, q


def save_wcnf(hardclauses, softclauses, top, filename="output.txt"):
    max_var = max(
        abs(var) for clause in (hardclauses + softclauses) for var in clause[:-1]
    )

    nbclauses = len(hardclauses) + len(softclauses)

    with open(filename, 'w') as file:
        file.write("c\n")
        file.write("c Generated WCNF file\n")
        file.write("c\n")
        file.write(f"p wcnf {max_var} {nbclauses} {top}\n")
        
        for clause in hardclauses:
            clause_str = f"{top} " + " ".join(map(str, clause)) + " 0\n"
            file.write(clause_str)

        for clause in softclauses:
            weight = clause[-1]
            literals = clause[:-1]
            clause_str = f"{weight} " + " ".join(map(str, literals)) + " 0\n"
            file.write(clause_str)

    print(f"WCNF file saved as {filename}")

for n in range(5, 50):
    hardclauses, softclauses, d, p, q = main_func(n)
    d = d + 10
    save_wcnf(hardclauses, softclauses, d, f"input_{n}.txt")