# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in \{1,2,\ldots,M\} \quad \text{(types of smaller rolls)}, \quad j \in \{1,2,\ldots,N\} \quad \text{(cutting patterns)}. \\[1mm]
\textbf{Parameters:} \quad & M = 4, \quad N = 49, \\
& \text{large\_roll\_width} \in \mathbb{R}_{+} \quad (=70), \\
& d_i \in \mathbb{R}_{+} \quad \text{(demand for smaller roll of type } i\text{)}, \quad \forall i=1,\ldots,M, \\
& w_i \in \mathbb{R}_{+} \quad \text{(width of smaller roll of type } i\text{)}, \quad \forall i=1,\ldots,M, \\
& a_{ij} \in \mathbb{Z}_{+} \quad \text{(number of smaller rolls of type } i \text{ produced by pattern } j\text{)}, \quad \forall i=1,\ldots,M,\; j=1,\ldots,N. \\[1mm]
\textbf{Additional Data Verification:} \quad & \text{For each pattern } j, \text{ it is assumed that} \\
& \sum_{i=1}^{M} w_i\, a_{ij} \le \text{large\_roll\_width}. \\[2mm]
\textbf{Decision Variables:} \quad & x_j \in \mathbb{Z}_{+} \quad \text{for each } j=1,\ldots,N, \quad \text{representing the number of large rolls cut using pattern } j. \\[2mm]
\textbf{Objective Function:} \quad & \text{Minimize the total number of large rolls used:} \\
\min \quad & Z = \sum_{j=1}^{N} x_j. \\[2mm]
\textbf{Constraints:} \\[2mm]
& \text{(a) Demand satisfaction for each type } i: \\
& \sum_{j=1}^{N} a_{ij}\, x_j \ge d_i, \quad \forall\, i=1,\ldots,M. \\[2mm]
& \text{(b) (Implicit) Feasibility of cutting patterns is assumed, i.e., for each } j: \\
& \sum_{i=1}^{M} w_i\, a_{ij} \le \text{large\_roll\_width}. \\[2mm]
& \text{(c) Non-negativity and integrality:} \\
& x_j \in \mathbb{Z}_{+}, \quad \forall\, j=1,\ldots,N.
\end{align*} 

\vspace{2mm}
This complete model accurately represents the manufacturing and production problem by:
\\[1mm]
1. Defining clear decision variables (the number of large rolls to cut with each available pattern).\\[1mm]
2. Establishing the minimization objective of the total large rolls used.\\[1mm]
3. Including constraints ensuring that the production using the selected cutting patterns meets or exceeds the customer demand for each type of smaller roll.\\[1mm]
4. Confirming that each pre-defined pattern is feasible with respect to the large roll width.\\[1mm]
5. Maintaining integrality and non-negativity to avoid trivial, infeasible or unbounded scenarios.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    M = 4
    N = 49
    large_roll_width = 70
    demands = [40, 65, 80, 75]
    roll_width_options = [17, 14, 11, 8.5]
    
    # Patterns given as a flat list; we reshape into a list of lists (N x M)
    patterns_flat = [
        4, 0, 0, 0,
        3, 1, 0, 0,
        3, 0, 1, 0,
        2, 2, 0, 0,
        3, 0, 0, 2,
        2, 1, 2, 0,
        2, 1, 1, 1,
        2, 1, 0, 2,
        2, 0, 3, 0,
        2, 0, 2, 1,
        2, 0, 1, 2,
        1, 3, 1, 0,
        1, 3, 0, 1,
        1, 2, 2, 0,
        1, 2, 1, 1,
        1, 2, 0, 2,
        1, 1, 3, 0,
        0, 5, 0, 0,
        0, 4, 1, 0,
        0, 4, 0, 1,
        0, 3, 2, 0,
        2, 0, 0, 4,
        1, 1, 2, 2,
        1, 1, 1, 3,
        1, 1, 0, 4,
        1, 0, 4, 1,
        1, 0, 3, 2,
        1, 0, 2, 3,
        1, 0, 1, 4,
        0, 3, 1, 2,
        0, 3, 0, 3,
        0, 2, 3, 1,
        0, 2, 2, 2,
        0, 2, 1, 3,
        0, 2, 0, 4,
        0, 1, 5, 0,
        0, 1, 4, 1,
        0, 1, 3, 2,
        0, 0, 6, 0,
        0, 0, 5, 1,
        1, 0, 0, 6,
        0, 1, 2, 4,
        0, 1, 1, 5,
        0, 1, 0, 6,
        0, 0, 4, 3,
        0, 0, 3, 4,
        0, 0, 2, 5,
        0, 0, 1, 6,
        0, 0, 0, 8
    ]
    
    # Reshape the flat list into a list of lists, each inner list representing a pattern for the 4 roll types.
    patterns = []
    for j in range(N):
        start = j * M
        end = start + M
        patterns.append(patterns_flat[start:end])
    
    # Create MILP solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return
    
    # Decision Variables: x_j is the number of large rolls used with pattern j
    x = []
    for j in range(N):
        x.append(solver.IntVar(0, solver.infinity(), f'x_{j}'))
    
    # Objective: Minimize the total number of large rolls used
    solver.Minimize(solver.Sum(x[j] for j in range(N)))
    
    # Constraints: For each smaller roll type i, production must meet or exceed its demand.
    for i in range(M):
        constraint_expr = solver.Sum(patterns[j][i] * x[j] for j in range(N))
        solver.Add(constraint_expr >= demands[i])
    
    # Optional: verify feasibility of patterns against the large roll width
    # This check is not needed for the solver since data is assumed to be feasible.
    for j in range(N):
        total_width = sum(roll_width_options[i] * patterns[j][i] for i in range(M))
        if total_width > large_roll_width + 1e-6:
            print(f"Warning: Pattern {j} exceeds the available large roll width.")
    
    # Solve the model
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print("Total large rolls used =", solver.Objective().Value())
        for j in range(N):
            if x[j].solution_value() > 0:
                print(f"Pattern {j+1}: Use {int(x[j].solution_value())} times")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
    else:
        print("No feasible solution found.")
    
if __name__ == '__main__':
    main()