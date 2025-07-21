# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & n \in \mathbb{Z}_{>0} \quad\text{(number of rows)}, \quad m \in \mathbb{Z}_{>0} \quad\text{(number of columns)},\\[1mm]
& \text{Given a grid (matrix) } g \in \mathbb{R}^{n \times m}, \text{ where } g_{ij} \text{ is the number in row } i \text{ and column } j.\\[2mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\} \quad \forall\, i=1,\ldots,n,\; j=1,\ldots,m,\\[1mm]
& \quad \text{where } x_{ij} = 1 \text{ if and only if the number in row } i \text{ and column } j \text{ is selected.}\\[2mm]
\textbf{Objective Function:} \quad & \text{Maximize the total sum of the selected numbers:} \\
& \max \; Z = \sum_{i=1}^{n}\sum_{j=1}^{m} g_{ij}\,x_{ij}.\\[2mm]
\textbf{Constraints:}\\[1mm]
% Each row must have exactly one number selected.
(1) &\quad \sum_{j=1}^{m} x_{ij} = 1, \quad \forall\, i = 1, \ldots, n.\\[2mm]
% Path continuity constraints for rows i and i+1:
(2) &\quad \text{For each } i=1,\ldots,n-1 \text{ and each } j = 1, \ldots, m, \text{ if the number in row } i \text{ and column } j \text{ is selected, then in the next row the selection must be in one of the adjacent columns.} \\[1mm]
&\quad x_{ij} \le \sum_{k \in A(j)} x_{(i+1)k}, \quad \forall\, i = 1, \ldots, n-1,\; j = 1, \ldots, m,\\[1mm]
&\quad \text{where } A(j) := \{\, k \in \{1,\ldots,m\} \mid k = j-1 \text{ or } k = j \text{ or } k = j+1 \,\}.\\[2mm]
\textbf{Domain:} \quad & x_{ij} \in \{0,1\}, \quad \forall\, i = 1, \ldots, n,\, j = 1, \ldots, m.
\end{align*}

\vspace{2mm}
This model fully represents the problem:  
- The decision variables x_{ij} indicate the choice of one number per row.  
- The objective is a maximization of the total sum collected along the chosen path.  
- Constraint (1) ensures exactly one selection per row.  
- Constraint (2) guarantees that the move from row i to row i+1 is feasible (i.e. from the current column j only moves to columns j-1, j, or j+1 are allowed, taking into account boundary conditions).  

This formulation is complete, self-contained, and suitable for conversion into an implementation (e.g., using OR-Tools).'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Problem data
    n = 3
    m = 3
    grid = [
        [0, 1, 1],
        [0, 2, 1],
        [10, 0, 0]
    ]

    model = cp_model.CpModel()

    # Decision variables: x[i][j] is 1 if cell (i,j) is selected.
    x = {}
    for i in range(n):
        for j in range(m):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

    # Constraint (1): Exactly one selection per row.
    for i in range(n):
        model.Add(sum(x[(i, j)] for j in range(m)) == 1)

    # Constraint (2): Adjacency constraints between consecutive rows.
    for i in range(n - 1):
        for j in range(m):
            # Determine allowed next columns (j-1, j, j+1) considering boundaries.
            allowed_cols = []
            if j - 1 >= 0:
                allowed_cols.append(j - 1)
            allowed_cols.append(j)
            if j + 1 < m:
                allowed_cols.append(j + 1)
            model.Add(x[(i, j)] <= sum(x[(i + 1, k)] for k in allowed_cols))

    # Objective: Maximize the sum of selected numbers.
    model.Maximize(sum(grid[i][j] * x[(i, j)] for i in range(n) for j in range(m)))

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        optimal_value = solver.ObjectiveValue()
        path = []
        for i in range(n):
            for j in range(m):
                if solver.Value(x[(i, j)]) == 1:
                    path.append(j)
                    break

        print('Optimal value:', optimal_value)
        print('Selected path (column indices for each row):', path)
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()