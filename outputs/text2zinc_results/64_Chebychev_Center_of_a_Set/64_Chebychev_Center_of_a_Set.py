# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} &\\[1mm]
M &\in \mathbb{N}, \quad \text{number of linear inequalities defining } P,\\[1mm]
N &\in \mathbb{N}, \quad \text{dimension of the ambient space } \mathbb{R}^N,\\[1mm]
a_i &\in \mathbb{R}^N, \quad i = 1,\ldots, M, \quad \text{coefficient vectors in the constraints},\\[1mm]
b_i &\in \mathbb{R}, \quad i = 1,\ldots, M, \quad \text{right-hand side constants in the constraints}.\\[3mm]
\textbf{Decision Variables:} &\\[1mm]
y &\in \mathbb{R}^N, \quad \text{the center of the ball},\\[1mm]
r &\in \mathbb{R}, \quad r \geq 0, \quad \text{the radius of the ball}.
\\[3mm]
\textbf{Problem Description:} &\\[1mm]
\text{Given the polyhedron } P &= \{ x \in \mathbb{R}^N \mid a_i^T x \leq b_i,\; i=1,\ldots,M \},\\[1mm]
\text{find the ball } B(y,r) &= \{ x \in \mathbb{R}^N \mid \|x-y\|_2 \leq r \} \\
&\text{of maximum radius } r \ge 0 \text{ such that } B(y,r) \subseteq P.
\\[3mm]
\textbf{Mathematical Model:} &\\[1mm]
\underset{y\in \mathbb{R}^N,\; r\in \mathbb{R}}{\text{maximize}} \quad & r\\[2mm]
\text{subject to} \quad & a_i^T y + \|a_i\|_2\, r \leq b_i, \quad i = 1,\ldots,M,\\[2mm]
& r \geq 0.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp
import math

def main():
    # Problem Data
    M = 4
    N = 2
    A = [
        [1.0, 0.0],
        [-1.0, 0.0],
        [0.0, 1.0],
        [0.0, -1.0]
    ]
    B = [2.0, 2.0, 3.0, 5.0]
    
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: y (vector in R^N) and r (radius >= 0)
    y = [solver.NumVar(-solver.infinity(), solver.infinity(), f'y_{j}') for j in range(N)]
    r = solver.NumVar(0.0, solver.infinity(), 'r')

    # Constraints: a_i^T y + ||a_i||_2 * r <= b_i, for each inequality i.
    for i in range(M):
        norm_ai = math.sqrt(sum(A[i][j] ** 2 for j in range(N)))
        constraint_expr = solver.Sum([A[i][j] * y[j] for j in range(N)]) + norm_ai * r
        solver.Add(constraint_expr <= B[i])
    
    # Objective: maximize r (Chebychev radius)
    solver.Maximize(r)

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print('Optimal radius r =', r.solution_value())
        for j in range(N):
            print(f'y[{j}] =', y[j].solution_value())
        print('Optimal objective value =', solver.Objective().Value())
    elif status == pywraplp.Solver.INFEASIBLE:
        print('Problem is infeasible.')
    else:
        print('Solver ended with status:', status)

if __name__ == '__main__':
    main()