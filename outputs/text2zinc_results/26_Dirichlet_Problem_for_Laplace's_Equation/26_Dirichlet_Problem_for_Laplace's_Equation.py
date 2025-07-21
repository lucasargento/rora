# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & r = 4,\quad c = 4,\quad Z = 0.0,\quad M = 100.0.\\[1mm]
\textbf{Index Sets:} \quad & i \in I = \{0,1,2,3,4\},\quad j \in J = \{0,1,2,3,4\}.\\[1mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \mathbb{R} \quad \forall\, (i,j) \in I \times J, \quad \text{with } Z \le x_{ij} \le M.\\[1mm]
\textbf{Boundary Conditions:}\\[0.5mm]
& x_{0,0} = Z,\quad x_{0,1} = M,\quad x_{0,2} = M,\quad x_{0,3} = M,\quad x_{0,4} = Z,\\[0.5mm]
& x_{1,0} = Z,\quad x_{1,4} = Z,\\[0.5mm]
& x_{2,0} = Z,\quad x_{2,4} = Z,\\[0.5mm]
& x_{3,0} = Z,\quad x_{3,4} = Z,\\[0.5mm]
& x_{4,0} = Z,\quad x_{4,1} = Z,\quad x_{4,2} = Z,\quad x_{4,3} = Z,\quad x_{4,4} = Z.\\[2mm]
\textbf{Interior Nodes (Dirichlet) Constraints:}\\[0.5mm]
& \text{For each interior cell } (i,j) \text{ with } i=1,2,3 \text{ and } j=1,2,3, \text{ enforce:}\\[0.5mm]
& \quad 4\, x_{ij} = x_{i-1,j} + x_{i+1,j} + x_{i,j-1} + x_{i,j+1}.\\[2mm]
\textbf{Objective Function:}\\[0.5mm]
& \text{Minimize } x_{1,1}.
\end{align*} 

\noindent This complete formulation models the finite-difference approximation of the Dirichlet problem for Laplace's equation on a 5-by-5 grid (with indices 0 to 4) where the boundary values are fixed as given and the interior nodes satisfy the five-point stencil relation. The goal is to minimize the value at cell $(1,1)$ while ensuring that all cells remain within the interval $[Z, M]$.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def main():
    # Problem parameters
    r = 4
    c = 4
    Z = 0.0
    M = 100.0
    # We have a grid from 0 to 4 (i.e., r+1 x c+1)
    num_rows = r + 1
    num_cols = c + 1

    # Create the solver using GLOP for continuous linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Create decision variables x[i, j] for i in {0,...,4} and j in {0,...,4}
    x = {}
    for i in range(num_rows):
        for j in range(num_cols):
            x[i, j] = solver.NumVar(Z, M, f'x_{i}_{j}')

    # Set boundary conditions
    # First row: x[0,0]=Z, x[0,1]=M, x[0,2]=M, x[0,3]=M, x[0,4]=Z
    solver.Add(x[0, 0] == Z)
    solver.Add(x[0, 1] == M)
    solver.Add(x[0, 2] == M)
    solver.Add(x[0, 3] == M)
    solver.Add(x[0, 4] == Z)

    # Row 1 boundaries: x[1,0]=Z, x[1,4]=Z
    solver.Add(x[1, 0] == Z)
    solver.Add(x[1, 4] == Z)

    # Row 2 boundaries: x[2,0]=Z, x[2,4]=Z
    solver.Add(x[2, 0] == Z)
    solver.Add(x[2, 4] == Z)

    # Row 3 boundaries: x[3,0]=Z, x[3,4]=Z
    solver.Add(x[3, 0] == Z)
    solver.Add(x[3, 4] == Z)

    # Row 4 boundaries: x[4,0]=Z, x[4,1]=Z, x[4,2]=Z, x[4,3]=Z, x[4,4]=Z
    solver.Add(x[4, 0] == Z)
    solver.Add(x[4, 1] == Z)
    solver.Add(x[4, 2] == Z)
    solver.Add(x[4, 3] == Z)
    solver.Add(x[4, 4] == Z)

    # Add interior Dirichlet constraints (five-point stencil)
    # For each interior cell (i,j) with i=1,2,3 and j=1,2,3:
    for i in range(1, num_rows - 1):
        for j in range(1, num_cols - 1):
            solver.Add(4 * x[i, j] == x[i - 1, j] + x[i + 1, j] + x[i, j - 1] + x[i, j + 1])

    # Objective: minimize the value of cell (1,1)
    objective = solver.Objective()
    objective.SetCoefficient(x[1, 1], 1)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal objective value =", objective.Value())
        print("Optimal grid solution:")
        for i in range(num_rows):
            row_values = [x[i, j].solution_value() for j in range(num_cols)]
            print(f"Row {i}: {row_values}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == "__main__":
    main()