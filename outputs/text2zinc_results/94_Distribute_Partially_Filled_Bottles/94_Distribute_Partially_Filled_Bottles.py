# Mathematical Formulation:
'''\begin{align*}
\textbf{Sets and Parameters:} \quad & 
\begin{array}{rcl}
I &=& \{1, 2, \dots, n\} \quad\text{(set of bottle types)},\\[1mm]
P &=& \{1, 2, \dots, \text{num\_people}\} \quad\text{(set of persons)},\\[1mm]
b_i &\in& \mathbb{Z}_+,\quad i\in I, \quad\text{(number of bottles available of type }i\text{)},\\[1mm]
t_i &\in& \mathbb{Z},\quad i\in I, \quad\text{(fill level of a bottle of type }i\text{; e.g., }t=[2,1,0]\text{)},\\[1mm]
B &\triangleq& \dfrac{\sum_{i\in I} b_i}{\text{num\_people}},\quad\text{(bottles per person)},\\[1mm]
L &\triangleq& \dfrac{\sum_{i\in I} b_i \, t_i}{\text{num\_people}},\quad\text{(total liquid per person)}.
\end{array} \\[2mm]

\textbf{Decision Variables:} \quad & 
\begin{array}{rcl}
x_{i,p} &\in& \mathbb{Z}_+, \quad \forall\, i\in I,\, p\in P,\\[1mm]
&& \text{where } x_{i,p} \text{ is the number of bottles of type } i \\
&& \text{allocated to person } p.
\end{array} \\[2mm]

\textbf{Objective Function:}\\[1mm]
& \text{Since the goal is to find all feasible distributions that satisfy the conditions,}\\[1mm]
& \min \; 0. \quad \text{(A dummy zero objective, so that the problem is formulated as a feasibility problem.)} \\[2mm]

\textbf{Constraints:} \quad & 
\begin{array}{rcl}
\text{(1) Supply constraints:} && \displaystyle \sum_{p\in P} x_{i,p} = b_i,\quad \forall\, i\in I. \\[2mm]

\text{(2) Equal number of bottles per person:} && \displaystyle \sum_{i\in I} x_{i,p} = B,\quad \forall\, p\in P. \\[2mm]

\text{(3) Equal total liquid per person:} && \displaystyle \sum_{i\in I} t_i\, x_{i,p} = L,\quad \forall\, p\in P. \\[2mm]

\text{(4) Lexicographical ordering of allocations:} &&\text{For symmetry breaking and uniqueness, require that}\\[1mm]
&& \text{for every two consecutive persons } p \text{ and } p+1, \\
&&\quad \bigl( x_{1,p},\, x_{2,p},\, \dots,\, x_{n,p} \bigr) \leq_{\text{lex}} \bigl( x_{1,p+1},\, x_{2,p+1},\, \dots,\, x_{n,p+1} \bigr),\\[1mm]
&& \text{i.e., } \forall\, p\in \{1,\dots,\text{num\_people}-1\},\\[1mm]
&& \quad \exists\, k\in I \text{ such that } x_{i,p} = x_{i,p+1} \text{ for all } i < k \quad \text{and} \quad x_{k,p} \le x_{k,p+1}.
\end{array}
\end{align*}

\textbf{Notes:}
1. The parameters $b_i$ and $t_i$ are provided by the problem data (for example, with $n=3$, one might have $b = [5,8,11]$ and $t = [2,1,0]$ corresponding to full, half‐full, and empty bottles, respectively).
2. The quantities $B$ and $L$ are assumed to be integers; hence the overall problem is feasible only if $\sum_{i\in I} b_i$ and $\sum_{i\in I} b_i \, t_i$ are divisible by $\text{num\_people}$.
3. The lexicographical ordering constraint is stated here in logical form. In an implementation using mixed integer programming, this may require additional modeling (e.g., via auxiliary binary variables and big‐M constraints) to enforce the lexicographic relation.
4. This formulation is a feasibility (or satisfaction) problem; the objective is merely a dummy objective. However, it is bounded (because the variable values are bounded by the quantities $b_i$) and nontrivial (since not every allocation satisfies both the bottle count and liquid equality constraints).

This completes the full mathematical model for the bottle distribution puzzle.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem data
    n = 3
    b = [5, 8, 11]       # number of bottles for each type
    t = [2, 1, 0]        # liquid levels for each type (full, half-full, empty)
    num_people = 3

    # Derived parameters
    total_bottles = sum(b)
    B = total_bottles // num_people  # bottles per person
    total_liquid = sum(b_i * t_i for b_i, t_i in zip(b, t))
    L = total_liquid // num_people   # liquid per person

    # Create CP-SAT model
    model = cp_model.CpModel()

    # Decision variables: x[i][p] is the count of bottles of type i allocated to person p.
    x = {}
    for i in range(n):
        for p in range(num_people):
            # Upper bound: cannot allocate more than available bottles of that type to one person.
            x[(i, p)] = model.NewIntVar(0, b[i], f'x_{i}_{p}')

    # Constraint 1: Supply constraints for each bottle type.
    for i in range(n):
        model.Add(sum(x[(i, p)] for p in range(num_people)) == b[i])

    # Constraint 2: Each person gets exactly B bottles.
    for p in range(num_people):
        model.Add(sum(x[(i, p)] for i in range(n)) == B)

    # Constraint 3: Each person gets exactly L units of liquid.
    for p in range(num_people):
        model.Add(sum(t[i] * x[(i, p)] for i in range(n)) == L)

    # Lexicographical ordering constraints.
    # We create a linearization using weighted sums.
    # Choose weights so that the significance of type i is higher than all lower types.
    # Compute weights: for index i, weight_i = product_{j > i} (b[j] + 1)
    weights = [0] * n
    prod = 1
    for i in reversed(range(n)):
        weights[i] = prod
        prod *= (b[i] + 1)

    for p in range(num_people - 1):
        # Lexicographical ordering constraint: weighted sum for person p <= weighted sum for person p+1.
        expr_p = sum(weights[i] * x[(i, p)] for i in range(n))
        expr_next = sum(weights[i] * x[(i, p + 1)] for i in range(n))
        model.Add(expr_p <= expr_next)

    # Dummy objective: minimize 0 (feasibility problem)
    model.Minimize(0)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("Solution Found:")
        print(f"Objective value = {solver.ObjectiveValue()}")
        for p in range(num_people):
            alloc = [solver.Value(x[(i, p)]) for i in range(n)]
            print(f"Person {p + 1}: {alloc}")
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()