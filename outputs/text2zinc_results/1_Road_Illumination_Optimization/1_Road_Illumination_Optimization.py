# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & i = 1,\ldots, N \quad \text{(road segments)}, \quad j = 1,\ldots, M \quad \text{(lamps)}. \\[1mm]
\textbf{Parameters:} \quad & \text{coeff}_{i,j} \quad \text{-- contribution of lamp } j \text{ to the illumination of segment } i,\\[0.5mm]
& b_i \quad \text{-- desired illumination at segment } i, \quad \text{for } i=1,\dots,N. \\[2mm]
\textbf{Decision Variables:} \quad & p_j \ge 0, \quad \text{for } j=1,\dots,M, \quad \text{(power of lamp } j\text{)},\\[0.5mm]
& e_i \ge 0, \quad \text{for } i=1,\dots,N, \quad \text{(absolute error in illumination at segment } i\text{)}. \\[2mm]
\textbf{Illumination Relationship:} \quad & I_i = \sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j, \quad \text{for } i=1,\dots,N. \\[2mm]
\textbf{Objective Function:} \quad & \text{Minimize the total absolute error:} \\
& \min_{p,\,e} \quad \sum_{i=1}^{N} e_i. \\[2mm]
\textbf{Constraints:} \quad & \text{For each segment } i=1,\dots,N, \text{ the absolute error is modeled by:} \\[0.5mm]
& \sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j - b_i \le e_i, \\[0.5mm]
& -\Bigl(\sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j - b_i\Bigr) \le e_i. \\[2mm]
\textbf{Complete Mathematical Model:} \\
\text{(P)} \quad & \min_{p,\,e} \quad \sum_{i=1}^{N} e_i \\[1mm]
\text{s.t.} \quad & \sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j - b_i \le e_i, \quad i=1,\dots,N, \\[1mm]
& -\left(\sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j - b_i\right) \le e_i, \quad i=1,\dots,N, \\[1mm]
& p_j \ge 0, \quad j=1,\dots,M, \\[1mm]
& e_i \ge 0, \quad i=1,\dots,N.
\end{align*} 

\textbf{Notes:}
\begin{itemize}
    \item The variable $p_j$ represents the power assigned to lamp $j$, and the model assumes non-negative lamp powers.
    \item The auxiliary variables $e_i$ capture the absolute deviation between the achieved illumination $I_i = \sum_{j=1}^{M} \text{coeff}_{i,j}\, p_j$ and the desired illumination $b_i$ for each segment $i$.
    \item The objective minimizes the total absolute error, ensuring that the realized illuminations are as close as possible to the desired levels.
    \item The model is both feasible and bounded under the assumption that there exists at least one non-negative lamp power assignment that approximates the desired illuminations within finite error.
\end{itemize}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    N = 3  # number of segments
    M = 2  # number of lamps
    coefficients = [
        [0.5, 0.3],  # coefficients for segment 1
        [0.2, 0.4],  # coefficients for segment 2
        [0.1, 0.6]   # coefficients for segment 3
    ]
    desired = [14, 3, 12]  # desired illuminations for segments 1, 2, 3

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Variables: p[j] for lamp power, e[i] for absolute error at segment i.
    p = [solver.NumVar(0, solver.infinity(), f'p_{j}') for j in range(M)]
    e = [solver.NumVar(0, solver.infinity(), f'e_{i}') for i in range(N)]

    # Constraints: For each segment i, model absolute error equations:
    # sum(coeff[i][j]*p[j]) - desired[i] <= e[i]
    # -(sum(coeff[i][j]*p[j]) - desired[i]) <= e[i]
    for i in range(N):
        illumination = solver.Sum([coefficients[i][j] * p[j] for j in range(M)])
        solver.Add(illumination - desired[i] <= e[i])
        solver.Add(-(illumination - desired[i]) <= e[i])

    # Objective: Minimize the sum of absolute errors
    objective = solver.Sum(e)
    solver.Minimize(objective)

    # Solve the model.
    status = solver.Solve()

    # Check and output the solution.
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution Found:")
        print("Objective (total absolute error) =", solver.Objective().Value())
        for j in range(M):
            print(f"p_{j} (Lamp {j + 1} power) =", p[j].solution_value())
        for i in range(N):
            print(f"e_{i} (Segment {i + 1} absolute error) =", e[i].solution_value())
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()