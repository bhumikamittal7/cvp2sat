from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import random

# ======================= helper functions =======================
def random_basis(n, m):
    '''
    Generate n linearly independent vectors of dimension m
    B = (b1, b2, ..., bn) \in \mathbb{R}^{m*n}
    '''
    basis = [[1 if i == j else 0 for j in range(m)] for i in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            scalar = random.randint(0,1)
            basis[i] = [basis[i][k] + scalar * basis[j][k] for k in range(m)]    
    return basis

def generate_random_vector(m):
    '''
    t \in \mathbb{R}^m
    '''
    return [random.randint(0,1) for i in range(m)]

def inner_product(basis, i, j):
    '''
    inner product of the basis vectors, b_i and b_j where i and j are the elements of the clause.
    '''
    m = len(basis[0])
    return sum([basis[i-1][k] * basis[j-1][k] for k in range(m)])

def sigma(s,n):
    '''
    parse a two tuple and read if either of the element is n+1 or negative of n+1
    '''
    count = 0
    for i in s:
        if i == (n+1) or i == -(n+1):
            count += 1
    return count

def make_clauses(n):
    '''
    generate 2-SAT clauses with all possible combinations of n variables and their negations.
    '''
    clauses = []
    for i in range(1,n+1):
        for j in range(i+1,n+2):
            clauses.append([i,j])
            clauses.append([-i,j])
            clauses.append([i,-j])
            clauses.append([-i,-j])
    return clauses

def clause_weight(clause, dCap, basis):
    '''
    calculate the weight of a clause based on the given formula.
    '''
    if clause[0] < 0 and clause[1] < 0:
        weight = dCap + ((2/3)*((-1)**(sigma(clause, n))) * (inner_product(basis, abs(clause[0]), abs(clause[1]))))
    else:
        weight = dCap - ((1/3)*((-1)**(sigma(clause, n))) * (inner_product(basis, abs(clause[0]), abs(clause[1]))))

    return weight

# ======================= input/parameters =======================
n = 4
m = 256
dCap = 99        #some large constant used to adjust the weight of the clauses
basis = random_basis(n, m)
t = generate_random_vector(m)
basis.append(t)

# ======================= test =======================
# print(basis)  
# print(t)
# print(sigma([-5,5]))

# print(make_clauses(n))
# print(len(make_clauses(n)))

# ======================= maxsat =======================
rc2 = RC2(WCNF())  
rc2.add_clause([n+1])     #set x_{n+1} = 1 (hard clause, because based on assumption)
for clause in make_clauses(n):
    rc2.add_clause(clause, weight=clause_weight(clause, dCap, basis))

for model in rc2.enumerate():
    print(model, rc2.cost)
print(rc2.oracle_time())
rc2.delete()