from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

wcnf = WCNF()
wcnf.append([-1, -2])  
wcnf.append([-1, -3])

wcnf.append([1], weight=1)  
wcnf.append([2], weight=1)
wcnf.append([3], weight=1)

with RC2(wcnf) as rc2:
    rc2.compute()
    print(rc2.cost)
    print(rc2.model)