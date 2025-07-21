# Mathematical Formulation:
'''\begin{align*}
\textbf{Decision Variables:}\quad & p_k \quad \text{for } k = 0,1,2,\dots,K, \quad \text{with } p_k \ge 0. \\[1mm]
\textbf{Objective Function:}\quad & \text{maximize} \quad \sum_{k=0}^{K} k^4\, p_k \\[1mm]
\textbf{Constraints:}\quad 
& \text{Normalization:}          && \sum_{k=0}^{K} p_k = 1, \\[1mm]
& \text{First moment (mean):}    && \sum_{k=0}^{K} k\, p_k = \text{ExpectedZ}, \\[1mm]
& \text{Second moment:}          && \sum_{k=0}^{K} k^2\, p_k = \text{ExpectedZSquared}.
\end{align*}

In this model, the decision variables p_k represent the probability that the random variable Z takes the value k (for k = 0,1,2,…,K) and are subject to non-negativity and total probability equal to 1. The objective is to maximize the fourth moment of Z, given the constraints on the first two moments. This formulation is both feasible and bounded under the specified conditions.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Parameters
    K = 6  # k = 0,1,...,6
    ExpectedZ = 3
    ExpectedZSquared = 10

    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create solver.")
        return

    # Decision variables: p_k for k = 0, 1, ..., K, each representing a probability.
    p = {}
    for k in range(K + 1):
        p[k] = solver.NumVar(0.0, 1.0, f'p_{k}')

    # Constraint: The probabilities must sum to one.
    solver.Add(sum(p[k] for k in range(K + 1)) == 1)

    # Constraint: First moment (expected value)
    solver.Add(sum(k * p[k] for k in range(K + 1)) == ExpectedZ)

    # Constraint: Second moment
    solver.Add(sum((k ** 2) * p[k] for k in range(K + 1)) == ExpectedZSquared)

    # Objective: Maximize the fourth moment E[Z^4] = sum_{k=0}^{K} k^4 * p_k
    objective = solver.Objective()
    for k in range(K + 1):
        objective.SetCoefficient(p[k], k ** 4)
    objective.SetMaximization()

    # Solve the problem
    result_status = solver.Solve()

    # Check result status and output solution
    if result_status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for k in range(K + 1):
            print(f"p[{k}] = {p[k].solution_value()}")
        print(f"Optimal objective value (upper bound on E[Z^4]): {objective.Value()}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()