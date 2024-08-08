from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

# ======================= parameters =======================
p = 2
n = 4
dCap = 999
# ======================= helper functions =======================

def sigma(s):
    '''
    parse a two tuple and read if either of the element is n+1 or negative of n+1
    '''
    count = 0
    for i in s:
        if i == (n+1) or i == -(n+1):
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
            clauses.append([i,j])
            clauses.append([-i,j])
            clauses.append([i,-j])
            clauses.append([-i,-j])
    return clauses

# print(make_clauses(p,n))
# print(len(make_clauses(p,n)))
def inner_product(clause):
    return 1

def clause_weight(clause, dCap):
    '''
    calculate the weight of a clause based on the given formula.
    '''
    if clause[0] < 0 and clause[1] < 0:
        weight = dCap + ((2/3)*((-1)**(sigma(clause))) * inner_product(clause))
    else:
        weight = dCap - ((1/3)*((-1)**(sigma(clause))) * inner_product(clause))

    return weight

# print(clause_weight([-1,-2], dCap))

# ======================= maxsat =======================