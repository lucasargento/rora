# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & K \in \mathbb{Z}_{++}, \quad \{(x_i, y_i)\}_{i=1}^K \text{ given data, with } K=19, \\[1mm]
& x_i \in \mathbb{R} \quad \text{for } i=1,\ldots,K, \quad y_i \in \mathbb{R} \quad \text{for } i=1,\ldots,K. \\[3mm]

\textbf{Decision Variables:} \quad & a \in \mathbb{R}, \quad \text{(intercept of the line)}; \\[1mm]
& b \in \mathbb{R}, \quad \text{(slope of the line)}; \\[1mm]
& d_i \in \mathbb{R}_+ \quad \text{for } i=1,\ldots,K, \quad \text{(absolute deviation of the } i\text{-th data point)}. \\[3mm]

\textbf{Objective Function:} \quad & \min_{a,\,b,\{d_i\}} \quad \sum_{i=1}^K d_i \quad \text{(minimize total absolute deviation)}. \\[3mm]

\textbf{Constraints:} \quad & d_i \ge y_i - \bigl( b\,x_i + a \bigr), \quad \forall\, i=1,\ldots,K, \\[1mm]
& d_i \ge \bigl( b\,x_i + a \bigr) - y_i, \quad \forall\, i=1,\ldots,K.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp


def main():
    # Data
    K = 19
    Y = [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
    X = [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables: a (intercept), b (slope) and d_i (absolute deviations).
    a = solver.NumVar(-solver.infinity(), solver.infinity(), 'a')
    b = solver.NumVar(-solver.infinity(), solver.infinity(), 'b')
    d = [solver.NumVar(0.0, solver.infinity(), f'd_{i}') for i in range(K)]

    # Adding constraints for absolute deviation:
    # d_i >= y_i - (b*x_i + a) and d_i >= (b*x_i + a) - y_i for each data point.
    for i in range(K):
        solver.Add(d[i] >= Y[i] - (b * X[i] + a))
        solver.Add(d[i] >= (b * X[i] + a) - Y[i])

    # Objective: Minimize the sum of absolute deviations.
    objective = solver.Sum(d)
    solver.Minimize(objective)

    # Solve the model.
    status = solver.Solve()

    # Output the solution if found.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("Objective value (sum of absolute deviations) =", solver.Objective().Value())
        print("Intercept (a) =", a.solution_value())
        print("Slope (b) =", b.solution_value())
        for i in range(K):
            print(f"d_{i} =", d[i].solution_value())
    else:
        print("The problem does not have an optimal solution.")


if __name__ == '__main__':
    main()