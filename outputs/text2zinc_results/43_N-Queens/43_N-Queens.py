# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & n = 6 \\[1mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\}, \quad \forall\, i,j \in \{1,2,\dots,n\}, \\
& \text{where } x_{ij} = 
\begin{cases}
1, & \text{if a queen is placed on square } (i,j), \\
0, & \text{otherwise.}
\end{cases} \\[1mm]
\textbf{Objective Function:}\\[0.5mm]
& \min \; 0 \quad \text{(or equivalently, solve as a feasibility problem)} \\[1mm]
\textbf{Constraints:}\\[0.5mm]
\text{(1) Row Constraints:} \quad & \sum_{j=1}^{n} x_{ij} = 1, \quad \forall\, i \in \{1,2,\dots,n\}, \\
\text{(2) Column Constraints:} \quad & \sum_{i=1}^{n} x_{ij} = 1, \quad \forall\, j \in \{1,2,\dots,n\}, \\[1mm]
\text{(3) Major Diagonals Constraints:} \quad & \sum_{\substack{1 \leq i,j \leq n \\ i - j = k}} x_{ij} \leq 1, \quad \forall\, k \in \{-n+1, -n+2, \dots, n-1\}, \\[1mm]
\text{(4) Minor Diagonals Constraints:} \quad & \sum_{\substack{1 \leq i,j \leq n \\ i + j = l}} x_{ij} \leq 1, \quad \forall\, l \in \{2,3,\dots,2n\}.
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    n = 6  # Size of the chessboard and number of queens
    model = cp_model.CpModel()

    # Create decision variables: x[i][j] is 1 if a queen is placed at (i, j), else 0.
    x = {}
    for i in range(n):
        for j in range(n):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

    # Row constraints: each row must have exactly one queen.
    for i in range(n):
        model.Add(sum(x[(i, j)] for j in range(n)) == 1)

    # Column constraints: each column must have exactly one queen.
    for j in range(n):
        model.Add(sum(x[(i, j)] for i in range(n)) == 1)

    # Major Diagonals constraints (i - j constant)
    for diff in range(-n + 1, n):
        diag_vars = []
        for i in range(n):
            j = i - diff
            if 0 <= j < n:
                diag_vars.append(x[(i, j)])
        if diag_vars:
            model.Add(sum(diag_vars) <= 1)

    # Minor Diagonals constraints (i + j constant)
    for sum_val in range(0, 2 * n - 1):
        diag_vars = []
        for i in range(n):
            j = sum_val - i
            if 0 <= j < n:
                diag_vars.append(x[(i, j)])
        if diag_vars:
            model.Add(sum(diag_vars) <= 1)

    # Objective: minimize 0 (feasibility problem)
    model.Minimize(0)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("Solution:")
        for i in range(n):
            row = ""
            for j in range(n):
                if solver.Value(x[(i, j)]) == 1:
                    row += " Q "
                else:
                    row += " . "
            print(row)
        print(f"Objective value: {solver.ObjectiveValue()}")
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()