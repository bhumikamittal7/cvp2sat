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
            scalar = random.randint(-99, 99)
            basis[i] += scalar * basis[j]
    
    t = []
    for i in range(m):
        t.append(basis[2][i] + basis[0][i]+1)

    return np.vstack([basis, t]).tolist()
#================================================================================

def inner_product(basis, i, j):
    return np.dot(basis[i-1], basis[j-1])

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

def make_soft_clauses(basis, n):
    count = n+2
    d = 99999
    clauses = []
    for i in range(1, n+1):
        wxi = d + (inner_product(basis, i, n+1)//n)
        wxinot = d - ((n-1)*(inner_product(basis, i, n+1)//n))
        clauses.append([i, wxi])
        clauses.append([-i, wxinot])

        for j in range(i+1, n+1):
            wxj = d - inner_product(basis, i, j) + (inner_product(basis, i, n+1)//n) + (inner_product(basis, j, n+1)//n)
            wxixj = d + (inner_product(basis, i, n+1)//n) + (inner_product(basis, j, n+1)//n)
            clauses.append([count, wxj])
            clauses.append([-i, -j, wxixj])
            count += 1
    return clauses


def calculate_total_weight(assignment, softclauses, n):
    sigma = 0
    for i in assignment:
        weight = softclauses[-1]
    pass


n = 3
assignment = [1,0,1,1,0,1,0]
# for i in range(n):
#     assignment.append(random.randint(0, 1))
# print(assignment)

print("#===============================================================================")
basis = random_basis(n, n)
print(basis[:-1])
print(basis[-1])
print("#===============================================================================")
hardclauses = make_hard_clauses(n)
print(hardclauses)
print("#===============================================================================")
softclauses = make_soft_clauses(basis, n)
print(softclauses)
print("#===============================================================================")

