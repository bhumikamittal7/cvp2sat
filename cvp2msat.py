from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import random

def random_basis(n):
    '''
    Generate n linearly independent vectors
    '''
    basis = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(-10, 10)
            basis[i] = [basis[i][k] + scalar * basis[j][k] for k in range(n)]    
    return basis

# ======================= parameters =======================
n = 4
dCap = 10000
basis = random_basis(n)
# ======================= helper functions =======================
def inner_product(basis, i, j):
    '''
    inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    '''
    return sum([basis[i][k] * basis[j][k] for k in range(n)])

def sigma(s):
    '''
    parse a two tuple and read if either of the element is n+1 or negative of n+1
    '''
    count = 0
    for i in s:
        if i == (n+1):
            count += 1
    return count

# print(sigma([-5,5]))

def make_clauses(n):
    '''
    generate 2-SAT clauses with all possible combinations of n variables and their negations.
    '''
    clauses = []
    for i in range(1,n+1):
        for j in range(i+1,n+2):
            if j == n+1:
                clauses.append([i,j])
                clauses.append([-i,j])
            else:
                clauses.append([i,j])
                clauses.append([-i,j])
                clauses.append([i,-j])
                clauses.append([-i,-j])
    return clauses

# print(make_clauses(p,n))
# print(len(make_clauses(p,n)))

def clause_weight(clause, dCap, basis):
    '''
    calculate the weight of a clause based on the given formula.
    '''
    if clause[0] < 0 and clause[1] < 0:
        weight = dCap + ((2/3)*((-1)**(sigma(clause))) * (inner_product(basis, abs(clause[0]), abs(clause[1]))))
    else:
        weight = dCap - ((1/3)*((-1)**(sigma(clause))) * (inner_product(basis, abs(clause[0]), abs(clause[1]))))

    return weight

# print(clause_weight([-1,-2], dCap))

# ======================= maxsat =======================
rc2 = RC2(WCNF())  
for clause in make_clauses(n):
    rc2.add_clause(clause, weight=clause_weight(clause, dCap, basis))

for model in rc2.enumerate():
    print(model, rc2.cost)
rc2.delete()
