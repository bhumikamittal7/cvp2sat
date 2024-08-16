from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import random
import numpy as np

# ======================= helper functions =======================
def random_basis(n, m):
    '''
    Generate n linearly independent vectors of dimension m
    B = (b1, b2, ..., bn) \in \mathbb{R}^{m*n}
    '''
    basis = np.eye(n, m, dtype=int).tolist()
    
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(0, 1)
            if scalar:
                basis[i] = [(basis[i][k] + basis[j][k]) % 2 for k in range(m)]
    
    # Add an additional random vector t
    basis.append(generate_random_vector(m))
    return basis

def generate_random_vector(m):
    '''
    Generate a random vector t \in \mathbb{R}^m
    '''
    return np.random.randint(0, 2, m).tolist()

def inner_product(basis, i, j):
    '''
    Inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    '''
    return np.dot(basis[i-1], basis[j-1])

def sigma(clause, n):
    '''
    Parse a clause and count if either of the elements is n+1 or negative of n+1
    '''
    return sum(1 for x in clause if abs(x) == n + 1)

def make_clauses(n):
    '''
    Generate 2-SAT clauses with all possible combinations of n variables and their negations.
    '''
    for i in range(1, n+1):
        for j in range(i+1, n+2):
            yield [i, j]
            yield [-i, j]
            yield [i, -j]
            yield [-i, -j]

def clause_weight(clause, dCap, basis, n):
    '''
    Calculate the weight of a clause based on the given formula.
    '''
    weight = 0
    inner_prod = inner_product(basis, abs(clause[0]), abs(clause[1]))
    sign_factor = (-1) ** sigma(clause, n)
    
    if clause[0] < 0 and clause[1] < 0:
        weight = dCap + ((2 / 3) * sign_factor * inner_prod)
    else:
        weight = dCap - ((1 / 3) * sign_factor * inner_prod)

    return weight

def print_file(filename, rc2):
    with open(filename, 'w') as file:
        for model in rc2.enumerate():
            file.write(f"Model: {model}, Cost: {rc2.cost}\n")
        file.write(f"Time taken: {rc2.oracle_time()}")

# ======================= input/parameters =======================
n = 4
m = 256
dCap = 99         #some large constant used to adjust the weight of the clauses
basis = random_basis(n, m)

# ======================= test =======================
# print(basis)  
# print(sigma([-5,5]), 2)

# print(list(make_clauses(n)))
# print(len(list(make_clauses(n))))

# ======================= maxsat =======================
rc2 = RC2(WCNF())
rc2.add_clause([n + 1])  # set x_{n+1} = 1 (hard clause, based on assumption)

clauses = list(make_clauses(n))
for clause in clauses:
    rc2.add_clause(clause, weight=clause_weight(clause, dCap, basis, n))

# for model in rc2.enumerate():
#     print(model, rc2.cost)
filename = 'models_output.txt'
print_file(filename, rc2)

print(rc2.oracle_time())
rc2.delete()
