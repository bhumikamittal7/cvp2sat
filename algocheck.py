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
    t = []
    for i in range(m):
        t.append(basis[p][i] + basis[q][i] + np.random.randint(1, 2))
    return np.vstack([basis, t]).tolist(), p+1, q+1

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


def find_d(ip_cache, n):
    d = 0
    for i in range(1, n+1):
        for j in range(i, n+1):
            x = abs(ip_cache[(i, i)] - 2*ip_cache[(i, n+1)])
            y = abs(2*ip_cache[(i, j)])
            d = max(d, x, y)
    return d+10

# def make_soft_clauses(ip_cache, n):
#     count = n+2
#     clauses = []
#     d = find_d(ip_cache, n)
#     for i in range(1, n+1):
#         if ip_cache[(i, i)] < (2*ip_cache[(i, n+1)]):
#             wxi = d - (ip_cache[(i, i)] - (2*ip_cache[(i, n+1)]))
#             clauses.append([i, wxi])
#             clauses.append([-i, d])
#         for j in range(i+1, n+1):
#             wxj = d - 2*ip_cache[(i, j)]
#             clauses.append([count, wxj])
#             clauses.append([-count, d])
#             count += 1
#     return clauses, d

# ========================================================================================================================
def weights(ip_cache, n):
    weights = []
    for i in range(1, n+1):
        wi = (ip_cache[(i, i)] - (2*ip_cache[(i, n+1)]))
        weights.append([i, wi])
        for j in range(i+1, n+1):
            wj = ip_cache[(i, j)]
            weights.append([i, j, wj])
    return weights

def decider(ip_cache, n):
    count = n+2
    ans = [n+1]
    d = find_d(ip_cache, n)
    for i in range(1, n+1):
        if ip_cache[(i, i)] < (2*ip_cache[(i, n+1)]):
            ans.append(i)
        else:
            ans.append(-i)
        
    for i in range(1, n):
        for j in range(i+1, n+1):
            if i not in ans or j not in ans:
                ans.append(-count)
            else:
                ans.append(count)
            count += 1
    return ans, d
# ========================================================================================================================
# n = 5
# basis, p, q = random_basis(n, n, seed=9)
# ip_cache = inner_product_cache(basis, n)
# print(basis)
# print("============================================================")
# print(ip_cache)
# print("============================================================")
# print(p, q)
# print("============================================================")
# print(weights(ip_cache, n))

with open(f"checkforAlgo.txt", 'w') as file:
    for n in range(5, 6):
        seed = 42
        for i in range(seed, seed+1):
            basis, p, q = random_basis(n, n, seed=i)
            ip_cache = inner_product_cache(basis, n)

            softclauses,d = decider(ip_cache, n)
            print("p, q =", p, q)
            print(softclauses)
            #check if p and q are in the ans or not
            if p in softclauses and q in softclauses:
                file.write("found\n")
                file.write("============\n")
            else:
                file.write("nope\n")
                file.write(f"{n}\n")
                file.write(f"seed = {i}\n")
                file.write(f"{p}, {q}\n")
                file.write(f"softclauses = {softclauses}\n")
                file.write("============\n")
