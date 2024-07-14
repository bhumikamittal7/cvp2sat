# Boolean Satisfiability Problem (SAT)
Boolean expression/formula consists of variables, operators, and parentheses. The formula is _satisfiable_ if there exists a assignment of variables that can make the formula TRUE. Else it is unsatisfiable. The Boolean satisfiability problem (SAT) is, given a formula, check whether it is satisfiable. 

SAT was the first problem known to be NP-complete. NP-completeness only refers to the run-time of the worst case instances.

### Operators 
- AND (conjunction, ∧)
- OR (disjunction, ∨)
- NOT (negation, ¬)

## Conjunctive normal form
Can be thought of AND of ORs (product of sums). It contains conjunction of disjunctions. 

- **Literal:** A _literal_ is either a variable (in which case it is called a positive literal) or the negation of a variable (called a negative literal). 
- **Clause:** A _clause_ is a disjunction of literal(s).

At least one literal in every clause becomes true to make the SAT true.

## 3-SAT
Each clause is limited to at most 3 literals. We can reduce the unrestricted SAT problem to 3-SAT by converting each clause to an conjunction of $n-2$ clauses. This transformation is not logically equivalent but they are equisatisfiable; the length growth of the formula is polynomial. 

## $k$-SAT
Each clause is limited to at most $k$ literals. To make it exactly $k$ literals, just pad it with dummy variables/duplicate literals.

## 2-SAT and why it can be solved in poly-time
Each clause is limited to at most 2 literals. We can solve this using backtracing algorithm. Another method can be by mapping the instance to a graph and checking for the existance of paths using BFS/DFS. 