from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random
import time
import signal

# ======================= helper functions =======================
def random_basis(n, m):
    """
    generate n linearly independent vectors of dimension m
    B = (b1, b2, ..., bn) in R^{m*n}
    """

    basis = np.eye(n, m, dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(-99, 99)
            basis[i] += scalar * basis[j]

    return np.vstack([basis, generate_random_vector(m)]).tolist()

def generate_random_vector(m):
    """
    generate a random vector t in R^m
    """
    return np.random.randint(-99, 100, m)

def inner_product(basis, i, j):
    """
    inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    """
    return np.dot(basis[i-1], basis[j-1])

def sigma(clause, n):
    """
    parse a clause and count if either of the elements is n+1 or negative of n+1
    """
    return sum(1 for x in clause if abs(x) == n + 1)

def make_clauses(n):
    """
    generate 2-SAT clauses with all possible combinations of n variables and their negations.
    """
    clauses = []
    for i in range(1, n+1):
        for j in range(i+1, n+2):
            clauses.append([i, j])
            clauses.append([-i, j])
            clauses.append([i, -j])
            clauses.append([-i, -j])
    return clauses

def clause_weight(clause, dCap, basis, n):
    """
    calculate the weight of a clause based on the given formula.
    """
    inner_prod = inner_product(basis, abs(clause[0]), abs(clause[1]))
    sign_factor = (-1) ** sigma(clause, n)
    if clause[0] < 0 and clause[1] < 0:
        weight = dCap + (2/3) * sign_factor * inner_prod
    else:
        weight = dCap - (1/3) * sign_factor * inner_prod
    return weight

def print_file(filename, rc2):
    with open(filename, 'w') as file:
        for model in rc2.enumerate():
            file.write(f"Model: {model}, Cost: {rc2.cost}\n")
        file.write(f"Time taken: {rc2.oracle_time()}\n")

# ======================= input/parameters =======================
# n = 6  # rank
# m = n  # dimension (for full rank, m = n)
dCap = 9999  # some large constant used to adjust the weight of the clauses
# basis = random_basis(n, m)

# ======================= maxsat function =======================
def run_maxsat(n, dCap, basis):
    rc2 = RC2(WCNF())
    rc2.add_clause([n + 1])  # set x_{n+1} = 1 (hard clause)
    
    clauses = make_clauses(n)
    clause_weights = [clause_weight(clause, dCap, basis, n) for clause in clauses]
    
    for clause, weight in zip(clauses, clause_weights):
        rc2.add_clause(clause, weight=weight)
    
    filename = 'models_output.txt'
    print_file(filename, rc2)
    
    return rc2.oracle_time()

# ======================= timeout =======================
timeout_seconds = 5*60

def timeout_handler(signum, frame):
    raise TimeoutError("MaxSAT solver timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(timeout_seconds)

for n in range(1,11):
    basis = random_basis(n, n)
    try:
        start_time = time.time()
        oracle_time = run_maxsat(n, dCap, basis)
        print(f"Solver Oracle Time for {n} variables: {oracle_time}")
    except TimeoutError:
        elapsed_time = time.time() - start_time
        print(f"MaxSAT solver timed out for {n} variables after {elapsed_time} seconds.")
    finally:
        signal.alarm(0)


# ======================= test =======================
# print(basis)  
# print(d)
# print(sigma([-5,5],4))

# print(list(make_clauses(n)))
# print(len(list(make_clauses(n))))

# ======================= maxsat =======================
# rc2 = RC2(WCNF())
# rc2.add_clause([n + 1])  # set x_{n+1} = 1 (hard clause, based on assumption)

# clauses = list(make_clauses(n))
# for clause in clauses:
#     rc2.add_clause(clause, weight=clause_weight(clause, dCap, basis, n))

# # for model in rc2.enumerate():
# #     print(model, rc2.cost)

# filename = 'models_output.txt'
# print_file(filename, rc2)

# print(rc2.oracle_time())
# rc2.delete()