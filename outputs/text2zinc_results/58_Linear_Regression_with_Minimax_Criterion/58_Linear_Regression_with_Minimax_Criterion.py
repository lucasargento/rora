# Mathematical Formulation:
'''\begin{align*}
\textbf{Decision Variables:} \quad 
& a \in \mathbb{R} \quad \text{(intercept of the line)},\\[1mm]
& b \in \mathbb{R} \quad \text{(slope of the line)},\\[1mm]
& d \in \mathbb{R},\ d \ge 0 \quad \text{(maximum absolute deviation, to be minimized)}.
\\[2mm]
\textbf{Parameters:} \quad 
& \text{NumObs} \in \mathbb{Z}_{>0} \quad \text{(number of observations, here 19)},\\[1mm]
& \{x_i\}_{i=1}^{\text{NumObs}} \quad \text{(observed values of } x \text{)},\\[1mm]
& \{y_i\}_{i=1}^{\text{NumObs}} \quad \text{(observed values of } y \text{)}.
\\[2mm]
\textbf{Objective Function:} \quad 
& \min \; d.
\\[2mm]
\textbf{Constraints:} \quad & \text{For each } i = 1,2,\ldots,\text{NumObs}:\\[1mm]
& y_i - (b\,x_i + a) \leq d,\\[1mm]
& -(y_i - (b\,x_i + a)) \leq d.\\[2mm]
\textbf{Complete Mathematical Model:} \quad & 
\begin{array}{rl}
\min\limits_{a,b,d} & d\\[2mm]
\text{s.t.}  & y_i - (b\, x_i + a) \le d, \quad i = 1,\ldots, \text{NumObs},\\[1mm]
            & -(y_i - (b\, x_i + a)) \le d, \quad i = 1,\ldots, \text{NumObs},\\[1mm]
            & d \ge 0,\\[1mm]
            & a \in \mathbb{R}, \; b \in \mathbb{R}.
\end{array}
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    NumObs = 19
    Y = [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
    X = [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]

    # Create solver using GLOP (LP solver)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not found.")
        return

    # Decision Variables: a (intercept), b (slope) and d (maximum deviation)
    a = solver.NumVar(-solver.infinity(), solver.infinity(), 'a')
    b = solver.NumVar(-solver.infinity(), solver.infinity(), 'b')
    d = solver.NumVar(0.0, solver.infinity(), 'd')

    # Constraints: for each observed data point, two inequality constraints
    for i in range(NumObs):
        # y_i - (b*x_i + a) <= d
        solver.Add(Y[i] - (b * X[i] + a) <= d)
        # -(y_i - (b*x_i + a)) <= d  <=>  (b*x_i + a) - y_i <= d
        solver.Add((b * X[i] + a) - Y[i] <= d)

    # Objective: minimize the maximum absolute deviation d
    objective = solver.Objective()
    objective.SetCoefficient(d, 1)
    objective.SetMinimization()

    status = solver.Solve()

    # Output the solution
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("a (Intercept):", a.solution_value())
        print("b (Slope):", b.solution_value())
        print("Maximum deviation d:", d.solution_value())
        print("Objective value (minimized maximum deviation):", objective.Value())
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()