# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & i = 1, 2, \dots, \text{OriginNum} \quad \text{and} \quad j = 1, 2, \dots, \text{DestinationNum}. \\[1mm]

\textbf{Decision Variables:} \quad & x_{ij} \ge 0 \quad \forall \, i, j, \quad \text{where } x_{ij} \text{ denotes the units of goods transported from origin } i \text{ to destination } j.\\[2mm]

\textbf{Parameters:} \quad & \text{Supply: } s_i \quad \text{for } i = 1,2,\dots,\text{OriginNum}, \\[0.5mm]
& \text{Demand: } d_j \quad \text{for } j = 1,2,\dots,\text{DestinationNum}, \\[0.5mm]
& \text{Transportation Cost: } c_{ij} \quad \text{for } i = 1,2,\dots,\text{OriginNum}, \; j = 1,2,\dots,\text{DestinationNum}. \\[2mm]

\textbf{Objective Function:} \quad & \min \; Z = \sum_{i=1}^{\text{OriginNum}} \sum_{j=1}^{\text{DestinationNum}} c_{ij} \, x_{ij}. \\[2mm]

\textbf{Constraints:} \\[0.5mm]
\text{(1) Supply Constraints:} \quad & \sum_{j=1}^{\text{DestinationNum}} x_{ij} \le s_i, \quad \forall \, i = 1,2,\dots,\text{OriginNum}. \\[0.5mm]
\text{(2) Demand Constraints:} \quad & \sum_{i=1}^{\text{OriginNum}} x_{ij} = d_j, \quad \forall \, j = 1,2,\dots,\text{DestinationNum}. \\[0.5mm]
\text{(3) Non-negativity Constraints:} \quad & x_{ij} \ge 0, \quad \forall \, i,j.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    origin_num = 2
    destination_num = 4
    supply = [29, 49]
    demand = [6, 28, 19, 23]
    cost = [
        [5, 10, 6, 3],
        [8, 5, 4, 7]
    ]

    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[i, j] = units transported from origin i to destination j
    # These variables are non-negative integers
    x = {}
    for i in range(origin_num):
        for j in range(destination_num):
            x[i, j] = solver.IntVar(0, supply[i], f'x_{i}_{j}')

    # Constraints
    # (1) Supply constraints: total goods shipped from origin i <= supply[i]
    for i in range(origin_num):
        solver.Add(sum(x[i, j] for j in range(destination_num)) <= supply[i])
    
    # (2) Demand constraints: total goods received at destination j = demand[j]
    for j in range(destination_num):
        solver.Add(sum(x[i, j] for i in range(origin_num)) == demand[j])
    
    # Objective: minimize the total transportation cost
    objective = solver.Objective()
    for i in range(origin_num):
        for j in range(destination_num):
            objective.SetCoefficient(x[i, j], cost[i][j])
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print(f"Total Cost = {solver.Objective().Value()}")
        for i in range(origin_num):
            for j in range(destination_num):
                print(f"x[{i+1}][{j+1}] = {x[i, j].solution_value()}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()