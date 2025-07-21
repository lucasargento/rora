# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices and Parameters:} \\
\quad & k & = 1,\;2,\;\ldots,\;K, & \quad \text{where } K=19 \text{ is the number of data points}.\\[1mm]
\quad & y^{(k)} & \in \mathbb{R}, & \quad \text{observed value of } y \text{ at data point } k,\\[1mm]
\quad & x^{(k)} & \in \mathbb{R}, & \quad \text{observed value of } x \text{ at data point } k.\\[3mm]

\textbf{Decision Variables:} \\
\quad & a & \in \mathbb{R}, & \quad \text{constant term (intercept) of the quadratic curve},\\[1mm]
\quad & b & \in \mathbb{R}, & \quad \text{linear coefficient of the quadratic curve},\\[1mm]
\quad & c & \in \mathbb{R}, & \quad \text{quadratic coefficient of the quadratic curve},\\[1mm]
\quad & \delta_k & \ge 0,\; \forall k=1,\ldots,K, & \quad \text{auxiliary variable representing the absolute deviation at data point } k.\\[3mm]

\textbf{Mathematical Model:} \\[1mm]
\begin{align*}
\text{minimize} \quad & \sum_{k=1}^{K} \delta_k \\[2mm]
\text{subject to} \quad 
& \delta_k \ge y^{(k)} - \Bigl(a + b\,x^{(k)} + c\,\bigl(x^{(k)}\bigr)^2\Bigr), \quad && k = 1,\ldots,K, \\[1mm]
& \delta_k \ge -\Bigl(y^{(k)} - \bigl(a + b\,x^{(k)} + c\,\bigl(x^{(k)}\bigr)^2\bigr)\Bigr), \quad && k = 1,\ldots,K, \\[1mm]
& \delta_k \ge 0, \quad && k = 1,\ldots,K, \\[1mm]
& a \in \mathbb{R}, \quad b \in \mathbb{R}, \quad c \in \mathbb{R}.
\end{align*}
\end{array}
\]

Explanation:
1. Decision variables a, b, and c represent the coefficients of the quadratic curve y = c x^2 + b x + a.  
2. For each data point k, the variable \(\delta_k\) captures the absolute deviation between the observed value \(y^{(k)}\) and the value predicted by the quadratic model.  
3. The objective is to minimize the sum of these absolute deviations, ensuring the best quadratic fit in the sense of least absolute deviations (LAD).  
4. The constraints ensure that \(\delta_k\) bounds the absolute residual \(\left| y^{(k)} - \left(a + b\,x^{(k)} + c\,\bigl(x^{(k)}\bigr)^2 \right) \right|\) for all k.

This formulation is complete, self-contained, and reflects the entire problem with full accuracy.'''

# Generated Code:
from ortools.linear_solver import pywraplp


def main():
    # Data
    observed_values = [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7,
                       3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3]
    observed_x_values = [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0,
                         4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
    K = len(observed_values)

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver could not be created.")
        return

    # Decision variables: a, b, c are unconstrained reals.
    a = solver.NumVar(-solver.infinity(), solver.infinity(), 'a')
    b = solver.NumVar(-solver.infinity(), solver.infinity(), 'b')
    c = solver.NumVar(-solver.infinity(), solver.infinity(), 'c')

    # Auxiliary variables (absolute deviations) for each data point.
    delta = []
    for k in range(K):
        delta_k = solver.NumVar(0.0, solver.infinity(), f'delta_{k}')
        delta.append(delta_k)

    # Constraints: Ensure delta_k >= | y_k - (a + b*x_k + c*x_k^2) | for all k.
    for k in range(K):
        x_k = observed_x_values[k]
        y_k = observed_values[k]
        # Constraint: delta_k >= y_k - (a + b*x_k + c*x_k^2)
        solver.Add(delta[k] >= y_k - (a + b * x_k + c * (x_k ** 2)))
        # Constraint: delta_k >= -(y_k - (a + b*x_k + c*x_k^2))
        solver.Add(delta[k] >= -(y_k - (a + b * x_k + c * (x_k ** 2))))

    # Objective: minimize the sum of absolute deviations.
    objective = solver.Objective()
    for k in range(K):
        objective.SetCoefficient(delta[k], 1.0)
    objective.SetMinimization()

    # Solve the problem.
    status = solver.Solve()

    # Check and print the solution.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("Objective value =", objective.Value())
        print("a =", a.solution_value())
        print("b =", b.solution_value())
        print("c =", c.solution_value())
        for k in range(K):
            print(f"delta_{k} =", delta[k].solution_value())
    else:
        print("No optimal solution found.")


if __name__ == '__main__':
    main()