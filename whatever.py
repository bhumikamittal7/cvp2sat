def mapvalues(n, i, j):
    if i < j:
        return ((n+1) + (j-i) + (((i-1)*(2*n-i))//2))

# print(mapvalues(7, 4, 7))
#==============================================================================================================
import numpy as np
import random

def random_basis(n, m, seed=None):
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
    cache = {}
    for i in range(1, n + 2):
        for j in range(i, n + 2):
            cache[(i, j)] = np.dot(basis[i - 1], basis[j - 1])
            cache[(j, i)] = cache[(i, j)]
    return cache

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


def soft_clause_weight_map(softclauses):
    clause_weight_dict = {}    
    for clause in softclauses:
        literal, weight = clause
        clause_weight_dict[literal] = weight
    return clause_weight_dict

def main_func(n):
    seed = 42
    basis, p, q = random_basis(n, n, seed=seed)
    ip_cache = inner_product_cache(basis, n)
    softclauses,d = make_soft_clauses(ip_cache, n)
    weightmap = soft_clause_weight_map(softclauses)
    return weightmap, softclauses, d

# print(main_func(7))
#==============================================================================================================
model = [-1, -2, -3, -4, 5, 6, 7, 8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, 27, -28, -29]
lst = []
n = 7
for i in range(n):
    if model[i] > 0:
        lst.append(i+1)

lst1 = lst.copy()

for i in lst:
    for j in lst:
        if i < j:
            lst1.append(mapvalues(n, i, j))

# print(lst1)
weightmap = main_func(7)[0]
softclauses_new = []
for i in lst1:
    softclauses_new.append([i, weightmap[i]])
    softclauses_new.append([-i, weightmap[-i]])
print(softclauses_new)
# print(mapvalues(7, 4, 7))
#==============================================================================================================

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

def run_maxsat(softclauses_new):
    rc2 = RC2(WCNF())
    for c in softclauses_new:
        rc2.add_clause(c[:-1], weight=c[-1])
    return rc2.compute(), rc2.cost, rc2.oracle_time()

print(run_maxsat(softclauses_new))