from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random
from numpy.linalg import matrix_rank


# ======================= helper functions =======================
def random_basis(n, m):
    """
    generate n linearly independent vectors of dimension m, B = (b1, b2, ..., bn) in R^{m*n}
    """
    basis = np.eye(n, m, dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(-99, 99)
            basis[i] += scalar * basis[j]
    # print("basis = ", basis[-2])
    t = []
    for i in range(m):
        t.append(basis[0][i] + basis[-1][i])

    return np.vstack([basis, t]).tolist()
    # return np.vstack([basis, t]).tolist()

# def generate_random_vector(m):
#     """
#     generate a random vector t in R^m
#     """
#     return np.random.randint(-99, 100, m)

def inner_product(basis, i, j):
    """
    inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    """
    return np.dot(basis[i-1], basis[j-1])

def make_clauses_and_weights(basis, n):
    """
    generate SAT clauses and their weights based on the given formula
    """
    k = len(basis)
    count = n+1
    clauses = []
    for i in range(1, n):
        for j in range(i+1, n+1):
            wi = (inner_product(basis, i, i) - 2*inner_product(basis, i, k))
            wj = (inner_product(basis, j, j) - 2*inner_product(basis, j, k))
            clauses.append([i, wi])
            clauses.append([j, wj])
            clauses.append([count, wi+wj+2*inner_product(basis, i, j)])
            clauses.append([-(count), j, 0])
            clauses.append([-(count), i, 0])
            clauses.append([(count), -i, -j, 0])
            count += 1
    return clauses

def print_file(filename, rc2):
    with open(filename, 'w') as file:
        for model in rc2.enumerate():
            file.write(f"Model: {model}, Cost: {rc2.cost}\n")
        file.write(f"Time taken: {rc2.oracle_time()}\n")

# ======================= input/parameters =======================
# n = 10
# basis = random_basis(n, n)
# clauses = make_clauses_and_weights(basis, n)
# print(clauses[3][-1])
# ======================= maxsat function =======================

def run_maxsat(n, basis):
    rc2 = RC2(WCNF())
    
    clauses = make_clauses_and_weights(basis, n)
    print(clauses)  
    
    for clause in clauses:
        # print(clause[:-1])
        # print(clause[-1])
        if clause[-1] == 0:
            rc2.add_clause(clause[:-1]) #hard clauses
        else:
            rc2.add_clause(clause[:-1], weight=clause[-1])  # soft clauses
    
    rc2.compute()
    print(rc2.cost)
    filename = 'models_output.txt'
    print_file(filename, rc2)
    
    return rc2.oracle_time()

x = 4
y = x+1
for n in range(x, y):
    print("n = ", n)
    # basis = random_basis(n, n)
    basis = [[1, -99, 43, -95], [0, 1, 54, -75], [0, 0, 1, 32], [0, 0, 0, 1], [4, -96, 47, -60]]
    print("basis = ", basis)
    print("target = ", basis[-1])
    oracle_time = run_maxsat(n, basis)
    print(f"Solver Oracle Time for {n} variables: {oracle_time}")