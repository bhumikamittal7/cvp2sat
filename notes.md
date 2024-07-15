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

## Why is 3-SAT NP-complete?
- 3-SAT is in NP: Given a solution, we can verify it in polynomial time (kinda trivial).
- 3-SAT is NP-hard: We can reduce any instance of SAT to 3-SAT in polynomial time. For any problem in NP, a nondeterministic polynomial-time algorithm exists to solve this problem or a verifier to check a solution. The verifier is an algorithm that can be implemented as a circuit. The circuit consists of AND, OR, and NOT gates, which can be represented as a formula. This formula can be converted to 3-SAT form, where each clause has exactly 3 literals, which is equivalent to the original formula. Thus, all problems in NP can be converted to 3-SAT, and the inputs to the original problem are equivalent to the converted inputs to 3-SAT. 
- QED: 3-SAT is NP-complete.

## Why can'twe use algorithms for 2-SAT to solve 3-SAT in poly-time?
Because the structure of the problem is different. In 2-SAT, the clauses are connected in a way that they form a directed graph. In 3-SAT, the clauses are connected in a way that they form a hypergraph (an edge can connect any number of vertices and is called hyperedge).

# MaxSAT Problem
Given a Boolean formula, find an assignment that maximizes the number of satisfied clauses. This is an optimization problem. 

For a number $\delta \in [0, 1]$, if there exists an assignment that satisfies at least $\delta$ fraction of the clauses, then the formula is $\delta$-satisfiable. 

It is Max-$k$-SAT if the formula is in conjunctive normal form and each clause has at most $k$ literals.

## Weighted MaxSAT
Each clause has a weight associated with it. The goal is to find an assignment that maximizes the sum of the weights of the satisfied clauses.

If there exists an assignment for which the of the weights of the satisfied clauses is at least $d$, then the formula is satisfiable.

# Hypergraph
A hypergraph is a generalization of a graph in which an edge can connect any number of vertices. A hypergraph is a pair $H = (V, E)$ where $V$ is a set of vertices and $E$ is a set of hyperedges. Each hyperedge is a subset of $V$.

## $p$-uniform hypergraph
A hypergraph is $p$-uniform if every hyperedge has exactly $p$ vertices.

# CLique Problem
Given a graph $G = (V, E)$ and an integer $k$, find a subset $V' \subseteq V$ of size $k$ such that the subgraph induced by $V'$ is a clique. A clique is a subset of vertices such that every pair of vertices is connected by an edge.

<!-- ## $k$-CLique Problem
A $k$-clique is a set of $k$ vertices that will have all $k$ choose $p$ hyperedges between them and its total weight is the sum of the weights of the hyperedges.  -->

# Coloring Problem
Given a graph $G = (V, E)$, find a coloring of the vertices such that no two adjacent vertices have the same color. The chromatic number of a graph is the minimum number of colors needed to color the graph.

## $k$-Coloring Problem
Given a graph $G = (V, E)$ and an integer $k$, find a coloring of the vertices such that no two adjacent vertices have the same color and the number of colors used is at most $k$.

## Reduction from 3-Coloring to 3-SAT
Given a graph $G = (V, E)$, we can reduce the 3-coloring problem to 3-SAT as follows:
- Since the graph is 3-colorable, each vertex can be colored with one of the 3 colors. We create 3 variables for each vertex $v \in V$: $x_{v, 1}$, $x_{v, 2}$, and $x_{v, 3}$, where $x_{v, i}$ is true if vertex $v$ is colored with color $i$.

- For each edge $(u, v) \in E$, create the following clauses:
  - $(\neg x_{u, 1} \lor \neg x_{v, 1}) \land (\neg x_{u, 2} \lor \neg x_{v, 2}) \land (\neg x_{u, 3} \lor \neg x_{v, 3})$ (at least one of the vertices must be colored differently).

- For each vertex $v \in V$, create the following clause:
    - $$(x_{v, 1} \lor x_{v, 2} \lor x_{v, 3}) \land (\neg x_{v, 1} \lor \neg x_{v, 2}) \land (\neg x_{v, 1} \lor \neg x_{v, 3}) \land (\neg x_{v, 2} \lor \neg x_{v, 3})$$
    (each vertex must be colored with one of the 3 colors but cannot be colored with more than one color)

The 3-SAT formula is satisfiable if and only if the graph is 3-colorable.

# Closest Vector Problem (CVP)
Given a lattice $L$ and a target vector $t$, find the lattice point $v \in L$ that is closest to $t$. This means the norm of the difference between $v$ and $t$ is minimized. Intutively, the CVP is about finding the closest point in the lattice to a given point (this point need not be in the lattice).

## (0,1)-CVP
In the (0,1)-CVP, given a basis $B \in \mathbb{Z}^{m \times n}$ of a lattice $L$, and a target vector $t \in \mathbb{Z}^m$ and a number $d>0$, if there exists a vector $z \in \{0,1\}^n$ such that $||Bz-t|| \leq d$, then the problem is a yes-instance.

Intuitively, in (0,1)-CVP the lattice vectors are sum of the subset of the basis vectors. By the sum of the subset of the basis vectors, we mean that each basis vector is either included or not included in the sum.