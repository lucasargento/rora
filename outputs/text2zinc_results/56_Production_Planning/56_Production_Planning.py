# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & k \in \{1, 2, \dots, K\} \quad \text{(products)}, \quad s \in \{1, 2, \dots, S\} \quad \text{(production stations or machines)}. \\[1mm]
\textbf{Parameters:} \quad & \text{ProduceTime}_{k,s} \quad \text{(time required for one unit of product } k \text{ on station } s\text{)},\\[0.5mm]
& \text{AvailableTime}_s \quad \text{(total available processing time on station } s\text{)}, \\[0.5mm]
& \text{Profit}_k \quad \text{(profit per unit of product } k\text{)}.\\[2mm]
\textbf{Decision Variables:} \quad &
x_k \in \mathbb{Z}_{+} \quad \text{for all } k=1,\dots,K, \quad \text{with the additional condition } x_k \geq 1.
\quad \text{(Production quantity of product } k\text{)}
\\[2mm]
\textbf{Objective Function:} \quad &
\text{maximize} \quad Z = \sum_{k=1}^{K} \text{Profit}_k \, x_k.
\\[2mm]
\textbf{Constraints:} \quad &
\text{(1) Machine/Station time capacity constraints:} \\[0.5mm]
& \sum_{k=1}^{K} \text{ProduceTime}_{k,s} \, x_k \leq \text{AvailableTime}_s
\quad \forall \, s=1,\dots,S. \\[1.5mm]
& \text{(2) Non-trivial production (each product is produced in a nonzero quantity):} \\[0.5mm]
& x_k \geq 1 \quad \forall \, k=1,\dots,K.
\end{align*} 

\noindent This formulation exactly represents the manufacturing problem with multiple products and production stages, ensuring that production on each station does not exceed its available time and that each product is produced in a non-trivial quantity, while maximizing the total profit.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    NumProducts = 2
    NumMachines = 2
    # ProduceTime[k][s] for k in 0..NumProducts-1 and s in 0..NumMachines-1
    ProduceTime = [
        [1, 3],  # Product 1 time on machine 1 and 2
        [2, 1]   # Product 2 time on machine 1 and 2
    ]
    AvailableTime = [200, 100]  # Available time for machine 1 and machine 2
    Profit = [20, 10]  # Profit per unit for Product 1 and Product 2

    # Create the linear solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print('Solver not created.')
        return

    # Decision variables: x[k] >= 1 and integer
    x = []
    for k in range(NumProducts):
        x_k = solver.IntVar(1, solver.infinity(), f'x_{k}')
        x.append(x_k)

    # Constraints:
    # For each machine/production station, total production time of all products is within available time.
    for s in range(NumMachines):
        constraint_expr = solver.Sum([ProduceTime[k][s] * x[k] for k in range(NumProducts)])
        solver.Add(constraint_expr <= AvailableTime[s])

    # Objective: maximize total profit.
    objective = solver.Objective()
    for k in range(NumProducts):
        objective.SetCoefficient(x[k], Profit[k])
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Optimal solution found:')
        for k in range(NumProducts):
            print(f'Product {k+1} production quantity: {int(x[k].solution_value())}')
        print(f'Optimal profit: {objective.Value()}')
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()