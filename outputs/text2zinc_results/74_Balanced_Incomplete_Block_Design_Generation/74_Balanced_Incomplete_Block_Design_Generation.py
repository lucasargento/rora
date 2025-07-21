# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & v = 4, \quad k = 2, \quad \lambda = 1, \\[1mm]
& \text{Let } r = \frac{\lambda\,(v-1)}{k-1} = \frac{1\,(4-1)}{2-1} = 3, \quad
b = \frac{v\,r}{k} = \frac{4\cdot 3}{2} = 6. \\[1mm]
\intertext{\textbf{Decision Variables:} For each object $i=1,\dots,v$ and each block $j=1,\dots,b$,}
& x_{ij} \in \{0,1\} \quad \text{where } x_{ij} = 
\begin{cases}
1, & \text{if object } i \text{ is assigned to block } j,\\[1mm]
0, & \text{otherwise.}
\end{cases} \\[1mm]
\intertext{\textbf{Objective Function:}}
& \text{Minimize } 0 \quad \text{(a feasibility model)}. \\[1mm]
\intertext{\textbf{Constraints:}}
\text{\underline{(1) Row (Object) Occurrence Constraints:} } \quad &
\sum_{j=1}^{b} x_{ij} = r, \quad \forall \, i = 1,\dots,v. \\[1mm]
\text{\underline{(2) Column (Block) Size Constraints:} } \quad &
\sum_{i=1}^{v} x_{ij} = k, \quad \forall \, j = 1,\dots,b. \\[1mm]
\text{\underline{(3) Pairwise Co-occurrence Constraints:} } \quad &
\sum_{j=1}^{b} x_{ij}\,x_{hj} = \lambda, \quad \forall \, 1 \le i < h \le v.
\end{align*} 

This model completely represents the Balanced Incomplete Block Design (BIBD) problem for the given parameters, ensuring that each block contains exactly $k$ objects, every object appears in exactly $r$ blocks, and every pair of distinct objects appears together in exactly $\lambda$ blocks.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Parameters for BIBD
    v = 4
    k = 2
    lambd = 1  # lambda is a reserved keyword in Python

    # Derived parameters
    r = (lambd * (v - 1)) // (k - 1)  # number of blocks each object appears in
    b = (v * r) // k  # number of blocks

    # Create the model
    model = cp_model.CpModel()

    # Decision variables: x[i][j] = 1 if object i is in block j, 0 otherwise.
    x = {}
    for i in range(v):
        for j in range(b):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

    # Constraint (1): Each object appears in exactly r blocks.
    for i in range(v):
        model.Add(sum(x[(i, j)] for j in range(b)) == r)

    # Constraint (2): Each block has exactly k objects.
    for j in range(b):
        model.Add(sum(x[(i, j)] for i in range(v)) == k)

    # Constraint (3): Each pair of objects appears together in exactly lambd blocks.
    # For binary variables, the product x[i,j]*x[h,j] is equivalent to their AND.
    for i in range(v):
        for h in range(i + 1, v):
            # Create auxiliary variables for the product for each block.
            y_vars = []
            for j in range(b):
                y = model.NewBoolVar(f'y_{i}_{h}_{j}')
                model.AddMultiplicationEquality(y, [x[(i, j)], x[(h, j)]])
                y_vars.append(y)
            model.Add(sum(y_vars) == lambd)

    # Objective: feasibility problem (minimize 0)
    model.Minimize(0)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution:")
        for i in range(v):
            row = []
            for j in range(b):
                row.append(str(solver.Value(x[(i, j)])))
            print("Object {}: {}".format(i + 1, " ".join(row)))
        print("Objective value:", solver.ObjectiveValue())
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()