# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices:} & k & \in \{1,2,\dots, K\} & \quad \text{(spare part types)} \\
                 & s & \in \{1,2,\dots, S\} & \quad \text{(shops or machines)} \\[1em]
\textbf{Parameters:} & & & \\
\text{NumParts}   & = & K, & \text{number of spare parts (here } K=5 \text{)}\\[0.5em]
\text{NumMachines} & = & S, & \text{number of shops/machines (here } S=2 \text{)}\\[0.5em]
T_{k,s}         & : & \mathbb{Z}_{>0}, & \text{worker-hours required for one unit of part } k \text{ at machine } s\\[0.5em]
P_{k}           & : & \mathbb{R},     & \text{profit from one unit of spare part } k\\[0.5em]
C_s             & : & \mathbb{R}_{>0}, & \text{total available working hours at machine } s\\[1em]
\textbf{Decision Variables:} & & & \\
x_{k} & \in & \mathbb{Z}_{\ge0}, & \quad \text{number of units of spare part } k \text{ to produce, for } k=1,\dots, K.\\[1em]
\textbf{Mathematical Model:} & & & \\
\max \quad & z = & \displaystyle \sum_{k=1}^{K} P_{k}\, x_{k}, & \quad \text{(maximize total profit)}\\[1em]
\text{s.t.} \quad & \displaystyle \sum_{k=1}^{K} T_{k,s}\, x_{k} & \leq C_{s}, & \quad s=1,2,\dots,S \quad \text{(machine capacity constraints)}\\[1em]
& x_{k} & \ge 0, & \quad k=1,2,\dots,K\,.\\[1em]
\end{array}
\]

\[
\begin{aligned}
\textbf{Where:} \quad & K = 5, \quad S = 2,\\[0.5em]
& \text{Time data: } T_{k,s} = \begin{array}{c|cc}
k \backslash s & 1 & 2\\ \hline
1 & 2 & 3\\[0.2em]
2 & 1 & 2\\[0.2em]
3 & 3 & 1\\[0.2em]
4 & 2 & 1\\[0.2em]
5 & 3 & 1\\[0.array}
\quad & (\text{worker-hours per unit})\\[1em]
& \text{Profit data: } P = \begin{bmatrix}30, & 20, & 40, & 25, & 10\end{bmatrix},\\[0.5em]
& \text{Capacity data: } C = \begin{bmatrix}700, & 1000\end{bmatrix}\,.\\[0.5em]
\end{aligned}
\]

\textbf{Remarks:}  
1. The decision variables xₖ are assumed to be integers, reflecting the fact that production quantities are discrete.  
2. The capacity constraints ensure that the allocation of production respects the available worker-hours at each shop.  
3. The model is feasible and bounded, with non‐negative production and limited machine hours.  
4. Non-trivial production mixes (i.e., not producing exclusively one product unless optimal) will naturally result from solving this maximization model.
'''

# Generated Code:
from ortools.linear_solver import pywraplp


def main():
    # Create the solver using CBC mixed integer programming
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return

    # Data
    num_parts = 5
    num_machines = 2

    # Time matrix: worker-hours required for each part on each machine.
    # Rows correspond to parts (index 0 to 4) and columns to machines (index 0 to 1).
    time = [
        [2, 3],  # Part 1
        [1, 2],  # Part 2
        [3, 1],  # Part 3
        [2, 1],  # Part 4
        [3, 1]   # Part 5
    ]

    # Profit for each part
    profit = [30, 20, 40, 25, 10]

    # Capacity available on each machine
    capacity = [700, 1000]

    # Decision Variables: number of units to produce for each part (non-negative integers)
    x = [solver.IntVar(0, solver.infinity(), f'x_{k + 1}') for k in range(num_parts)]

    # Constraints: For each machine, total worker-hours across all parts do not exceed capacity.
    for s in range(num_machines):
        solver.Add(solver.Sum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s])

    # Objective: maximize total profit
    objective = solver.Objective()
    for k in range(num_parts):
        objective.SetCoefficient(x[k], profit[k])
    objective.SetMaximization()

    # Solve the problem and output the solution.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print("Objective value =", objective.Value())
        for k in range(num_parts):
            print(f"x[{k + 1}] = {int(x[k].solution_value())}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
        print("Objective value =", objective.Value())
        for k in range(num_parts):
            print(f"x[{k + 1}] = {int(x[k].solution_value())}")
    else:
        print("The problem does not have an optimal solution.")


if __name__ == '__main__':
    main()