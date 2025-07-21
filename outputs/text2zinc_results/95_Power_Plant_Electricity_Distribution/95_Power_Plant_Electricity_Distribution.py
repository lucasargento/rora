# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & p = 1,2,\ldots,P \quad\text{(power plants)}, \quad c = 1,2,\ldots,C \quad\text{(cities)}. \\[1mm]

\textbf{Decision Variables:} \quad & x_{p,c} \geq 0 \quad \forall\, p = 1,\ldots,P,\; c = 1,\ldots,C, \\
& \text{where } x_{p,c} \text{ is the amount of electricity (in appropriate units)}\\
& \quad \text{transmitted from power plant } p \text{ to city } c. \\[2mm]

\textbf{Parameters:} \quad & \text{Supply}_p: \text{Electricity capacity available at power plant } p,\\[0.5mm]
& \text{Demand}_c: \text{Peak electricity demand of city } c,\\[0.5mm]
& \text{TC}_{p,c}: \text{Transmission cost per unit of electricity from power plant } p \text{ to city } c.\\[2mm]

\textbf{Objective Function:} \quad & \min \; Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{TC}_{p,c} \, x_{p,c}. \\[2mm]

\textbf{Constraints:} \\[0.5mm]
\text{(1) Power Plant Capacity Constraints:} \quad & \sum_{c=1}^{C} x_{p,c} \leq \text{Supply}_p, \quad \forall\, p=1,\ldots,P. \\[1mm]
\text{(2) City Demand Satisfaction Constraints:} \quad & \sum_{p=1}^{P} x_{p,c} = \text{Demand}_c, \quad \forall\, c=1,\ldots,C. \\[1mm]
\text{(3) Non-negativity Constraints:} \quad & x_{p,c} \geq 0, \quad \forall\, p=1,\ldots,P,\; c=1,\ldots,C.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    P = 3  # number of power plants
    C = 2  # number of cities
    supply = [30, 25, 45]
    demand = [40, 60]
    transmission_costs = [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
    
    # Create the linear solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[p][c] >= 0 for each power plant p and city c
    x = {}
    for p in range(P):
        for c in range(C):
            x[p, c] = solver.NumVar(0, solver.infinity(), f'x_{p}_{c}')

    # Constraints:
    # (1) Power Plant Capacity constraints: sum_{c} x[p,c] <= supply[p] for each power plant
    for p in range(P):
        constraint = solver.RowConstraint(0, supply[p], f'capacity_{p}')
        for c in range(C):
            constraint.SetCoefficient(x[p, c], 1)

    # (2) City Demand Satisfaction constraints: sum_{p} x[p,c] == demand[c] for each city
    for c in range(C):
        constraint = solver.RowConstraint(demand[c], demand[c], f'demand_{c}')
        for p in range(P):
            constraint.SetCoefficient(x[p, c], 1)

    # Objective: minimize the total transmission cost
    objective = solver.Objective()
    for p in range(P):
        for c in range(C):
            objective.SetCoefficient(x[p, c], transmission_costs[p][c])
    objective.SetMinimization()
    
    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print(f'Optimal objective value = {objective.Value()}')
        for p in range(P):
            for c in range(C):
                print(f'Power plant {p+1} -> City {c+1}: {x[p, c].solution_value()}')
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it may not be optimal.')
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()