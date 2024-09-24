## DIMACS CNF format
Textual representation of CNF
- positive integers = variables
- negative integers = negated variables
- line starting with 'c' = comment (varisat: can be anywhere)
- header line = p cnf <variables> <clauses> (variables = number of variables, clauses = number of clauses)
- each clause is sequence of numbers separated by spaces, ending with 0
- each clause is newline

## Example
```
c This is a comment
p cnf 3 2
-1 3 0
1 3 -2 0
```
This represents the CNF formula (NOT x1 OR x3) AND (x1 OR x3 OR NOT x2)

## WDIMACS
- input file is given as an argument
- almost same as DIMACS, c = comment
- header line = p wcnf <variables> <clauses>
- first number in each clause is weight of clause (can be float or int)
- weight > 0

### Weighted Partial Max-SAT input format
- p wcnf <variables> <clauses> <top>
- top = for hard clause, when clause weight = top, it is hard clause
- for top, just use some large enough number

### Output format
- Comments: starts with 'c', informs about the program progress
- optimal solution: starts with 'o', number represnts the sum of the weights of the unsatisfied clauses in the optimal solution
- solution: s OPTIMUM FOUND, if the problem can be solved
- values: v line, specifies the found truth assignment
- numbers in v line: list of true literals


### Documentation
- [RC2](https://pysathq.github.io/docs/html/api/examples/rc2.html)