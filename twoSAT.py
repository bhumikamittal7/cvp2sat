import re

def validateInput(exp):
    # Each clause is at most 2 literals
    # Variables are lowercase alphabets, no upper case or digits
    # & - AND
    # | - OR
    # ! - NOT
    # () for clauses 
    pattern = re.compile(r'^\s*(\(\s*!?[a-z]\s*(\|\s*!?[a-z]\s*)?\)\s*(&\s*\(\s*!?[a-z]\s*(\|\s*!?[a-z]\s*)?\)\s*)*)\s*$')
    if not pattern.match(exp):
        raise ValueError("Invalid input format")
    return True


def readInput(exp):
    validateInput(exp)
    exp = exp.replace(' ', '').replace('(', '').replace(')', '')
    exp = exp.split('&')
    result = []
    for i in exp:
        temp = i.split('|')
        for j in range(len(temp)):
            if temp[j][0] == '!':
                temp[j] = -1 * (ord(temp[j][1]) - 96)
            else:
                temp[j] = ord(temp[j][0]) - 96
        result.append(temp)
    return result

def convert2graph(exp):
    #construct a graph from the expression such that 
    # for a given clause [1, 2] it will have edges -1->2 and -2->1
    graph = {}
    for clause in exp:
        if len(clause) == 2:
            a, b = clause
            if -a not in graph:
                graph[-a] = []
            if -b not in graph:
                graph[-b] = []
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []
            graph[-a].append(b)
            graph[-b].append(a)
        elif len(clause) == 1:
            a = clause[0]
            if -a not in graph:
                graph[-a] = []
            if a not in graph:
                graph[a] = []
            graph[-a].append(a)
    return graph

def findPath(graph, a, b):
    visited = set()
    stack = [a]
    while stack:
        node = stack.pop()
        if node == b:
            return True
        if node not in visited:
            visited.add(node)
            if node in graph:
                stack.extend(graph[node])
    return False

def twoSAT(exp):
    exp = readInput(exp)
    graph = convert2graph(exp)
    for i in range(1, 27):
        if findPath(graph, i, -i) and findPath(graph, -i, i):
            return False
    return True

x = '(a)&(!a)'
print(readInput(x))
print(convert2graph(readInput(x)))
print(twoSAT(x))
print("************")

x = '(a|!b)&(c|d)&(!d|b)'
print(readInput(x))
print(convert2graph(readInput(x)))
print(twoSAT(x))
print("************")

x = '(a|b)&(!a)&(!b)'
print(readInput(x))
print(convert2graph(readInput(x)))
print(twoSAT(x))
