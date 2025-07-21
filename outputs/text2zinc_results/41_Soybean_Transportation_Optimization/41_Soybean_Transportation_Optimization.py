# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & k \in \mathcal{K} = \{1,2, \dots, \text{NumTerminals}\} \quad\text{and}\quad l \in \mathcal{L} = \{1,2, \dots, \text{NumPorts}\} \\[1mm]

\textbf{Parameters:} \quad & \text{Supply at terminal } k: \; s_{k}, \quad k \in \mathcal{K} \\
& \text{Demand at destination (port) } l: \; d_{l}, \quad l \in \mathcal{L} \\
& \text{Transportation cost per ton from terminal } k \text{ to port } l: \; c_{kl}, \quad k \in \mathcal{K}, \; l \in \mathcal{L} \\[1mm]

\textbf{Decision Variables:} \quad & x_{kl} \ge 0, \quad \forall\, k \in \mathcal{K}, \; l \in \mathcal{L} \\
& \text{where } x_{kl} \text{ is the quantity (in metric tons) of soybeans transported from terminal } k \text{ to port } l. \\[1mm]

\textbf{Objective Function:} \quad & \text{Minimize the total transportation cost:} \\
\min \quad & Z = \sum_{k \in \mathcal{K}} \sum_{l \in \mathcal{L}} c_{kl} \, x_{kl} \\[1mm]

\textbf{Constraints:}\\[1mm]

& \text{Supply Constraints: Each terminal cannot ship more than its available supply} \\
& \sum_{l \in \mathcal{L}} x_{kl} \le s_{k}, \quad \forall\, k \in \mathcal{K} \\[1mm]

& \text{Demand Constraints: The demand at each destination (port) must be exactly met} \\
& \sum_{k \in \mathcal{K}} x_{kl} = d_{l}, \quad \forall\, l \in \mathcal{L} \\[1mm]

& \text{Nonnegativity Constraints:} \quad x_{kl} \ge 0, \quad \forall\, k \in \mathcal{K}, \; l \in \mathcal{L}
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    num_terminals = 3
    num_ports = 4
    cost = [
        [34, 49, 17, 26],
        [52, 64, 23, 14],
        [20, 28, 12, 17]
    ]
    demand = [65, 70, 50, 45]
    supply = [150, 100, 100]
    
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[k][l] >= 0, representing tons transported from terminal k to port l.
    x = {}
    for k in range(num_terminals):
        for l in range(num_ports):
            x[k, l] = solver.NumVar(0, solver.infinity(), f'x_{k}_{l}')

    # Supply constraints: each terminal cannot ship more than its available supply.
    for k in range(num_terminals):
        constraint = solver.Constraint(0, supply[k], f'supply_{k}')
        for l in range(num_ports):
            constraint.SetCoefficient(x[k, l], 1)

    # Demand constraints: meet exactly the demand at each port.
    for l in range(num_ports):
        constraint = solver.Constraint(demand[l], demand[l], f'demand_{l}')
        for k in range(num_terminals):
            constraint.SetCoefficient(x[k, l], 1)

    # Objective: minimize total transportation cost.
    objective = solver.Objective()
    for k in range(num_terminals):
        for l in range(num_ports):
            objective.SetCoefficient(x[k, l], cost[k][l])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        for k in range(num_terminals):
            for l in range(num_ports):
                print(f"Transportation from Terminal {k+1} to Port {l+1}: {x[k, l].solution_value():.2f} tons")
        print(f"Optimal cost = {objective.Value():.2f}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()