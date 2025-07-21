# Mathematical Formulation:
'''\begin{align*}
\textbf{Decision Variables:} \quad
& x_A \in \mathbb{Z}^+, \quad x_B \in \mathbb{Z}^+ \quad \text{with} \quad x_A \ge 1, \; x_B \ge 1, \\
& \text{where } x_A \text{ is the number of times Process A is executed, and} \\
& \quad\quad\quad x_B \text{ is the number of times Process B is executed.} \\[1em]
\textbf{Parameters:} \quad
& \text{GoldPerA} = 3,\quad \text{WiresPerA} = 2,\quad \text{CoinsPerA} = 5, \\
& \text{GoldPerB} = 5,\quad \text{WiresPerB} = 3,\quad \text{CoinsPerB} = 7, \\
& \text{TotalGold} = 500,\quad \text{TotalWires} = 300. \\[1em]
\textbf{Objective Function:} \quad
& \text{Maximize } Z = 5\, x_A + 7\, x_B, \\
& \quad \text{which represents the total number of coins plated.} \\[1em]
\textbf{Constraints:} \quad
& \text{Gold Constraint:} \quad 3\, x_A + 5\, x_B \le 500, \\
& \text{Wires Constraint:} \quad 2\, x_A + 3\, x_B \le 300.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Problem parameters
    GoldPerA = 3
    WiresPerA = 2
    CoinsPerA = 5

    GoldPerB = 5
    WiresPerB = 3
    CoinsPerB = 7

    TotalGold = 500
    TotalWires = 300

    # Define decision variables x_A and x_B (process executions) with lower bounds of 1.
    x_A = solver.IntVar(1, solver.infinity(), 'x_A')
    x_B = solver.IntVar(1, solver.infinity(), 'x_B')

    # Add constraints
    # Gold constraint: 3*x_A + 5*x_B <= 500
    solver.Add(GoldPerA * x_A + GoldPerB * x_B <= TotalGold)
    # Wires constraint: 2*x_A + 3*x_B <= 300
    solver.Add(WiresPerA * x_A + WiresPerB * x_B <= TotalWires)

    # Define objective function: Maximize 5*x_A + 7*x_B (total coins plated)
    objective = solver.Objective()
    objective.SetCoefficient(x_A, CoinsPerA)
    objective.SetCoefficient(x_B, CoinsPerB)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    # Check the result status
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Process A must be run: {int(x_A.solution_value())} times")
        print(f"Process B must be run: {int(x_B.solution_value())} times")
        print(f"Maximum coins plated: {int(objective.Value())}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution or is infeasible.")

if __name__ == '__main__':
    main()