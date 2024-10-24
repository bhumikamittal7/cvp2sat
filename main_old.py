from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import numpy as np
import random
from numpy.linalg import matrix_rank
#================================================================================
#ignore this for while, let's hardcode the basis for now as an example
def random_basis(n, m):
    """
    generate n linearly independent vectors of dimension m, B = (b1, b2, ..., bn) in R^{m*n}
    """
    basis = np.eye(n, m, dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(-99, 99)
            basis[i] += scalar * basis[j]
    t = []
    for i in range(m):
        t.append(basis[1][i])

    return np.vstack([basis, t]).tolist()

def inner_product(basis, i, j):
    """
    inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    """
    return np.dot(basis[i-1], basis[j-1])
#================================================================================
def make_clauses_and_weights(basis, n):
    """
    generate SAT clauses and their weights based on the given formula
    """
    d = 9999
    k = len(basis)
    #this is used to introduce new variables in the clauses for y1 <-> x1 & x2. This represents these y variables for each such pair. 
    count = n+2 
    clauses = []
    clauses.append([n+1, 0])  #hard clause

    for i in range(1, n+1):
        for j in range(i+1, n+2):
            widash = inner_product(basis, i, i) - 2*inner_product(basis, i, k) + inner_product(basis, k, k)
            wjdash = inner_product(basis, j, j) - 2*inner_product(basis, j, k) + inner_product(basis, k, k)
            
            wi = d - widash
            wj = d - wjdash
            wk = d -(widash + wjdash +2*inner_product(basis, i, j) - + inner_product(basis, k, k))
            
            # wi = widash
            # wj = wjdash
            # wk = (widash + wjdash +2*inner_product(basis, i, j))
            
            #putting the weight in the last element of the clause
            clauses.append([i, wi])
            if j != n+1:
                clauses.append([j, wj])
            clauses.append([count, wk])

            #weight = 0 for hard clauses, will later be used to differentiate between hard and soft clauses
            clauses.append([-(count), j, 0])    
            clauses.append([-(count), i, 0])
            clauses.append([(count), -i, -j, 0])   
            count += 1
    return clauses

#================================================================================
def print_file(filename, rc2):
    with open(filename, 'w') as file:
        for model in rc2.enumerate():
            file.write(f"Model: {model}, Cost: {rc2.cost}\n")
        file.write(f"Time taken: {rc2.oracle_time()}\n")
#================================================================================
def run_maxsat(n, basis):
    rc2 = RC2(WCNF())
    
    clauses = make_clauses_and_weights(basis, n)
    print(clauses)  
    
    for clause in clauses:
        if clause[-1] == 0:
            rc2.add_clause(clause[:-1]) #hard clauses
        else:
            rc2.add_clause(clause[:-1], weight=clause[-1])  # soft clauses
    
    rc2.compute()
    filename = 'mod_output.txt'
    print_file(filename, rc2)
    return rc2.oracle_time()
#================================================================================

# basis = [[1, -99, 43, -95], [0, 1, 54, -75], [0, 0, 1, 32], [0, 0, 0, 1], [4, -96, 47, -60]]
n = 2
# basis = random_basis(n, n)
basis = [[1, 91], [0, 1], [1, 92]]
print("basis = ", basis)
print("target = ", basis[-1])
oracle_time = run_maxsat(n, basis)   #here n = 4, as the last vector is the target vector

