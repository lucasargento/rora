# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Sets and Parameters:} \\
\mathcal{K} & = & \{1,2,3,4,5\} & \text{(spare parts)} \\
\mathcal{S} & = & \{1,2\} & \text{(shops or machines)} \\[1mm]
\text{For each } k \in \mathcal{K} \text{ and } s \in \mathcal{S}:\\[1mm]
T_{k,s} &=& \text{Time in worker‐hours required to process spare part } k \text{ on machine } s, & \text{with} \\[0.5mm]
&& \begin{array}{l}
T_{1,1}=2,\quad T_{1,2}=3,\\[0.2mm]
T_{2,1}=1,\quad T_{2,2}=2,\\[0.2mm]
T_{3,1}=3,\quad T_{3,2}=2,\\[0.2mm]
T_{4,1}=3,\quad T_{4,2}=1,\\[0.2mm]
T_{5,1}=1,\quad T_{5,2}=1,
\end{array} \\[2mm]
p_{k} &=& \text{Profit obtained per unit of spare part } k, & \text{with} \\
&& (p_1,p_2,p_3,p_4,p_5) = (30,20,40,25,10), \\[2mm]
C_{s} &=& \text{Capacity (available worker-hours) on machine } s, & \text{with} \\
&& (C_1,C_2) = (700,1000). \\[4mm]

\textbf{Decision Variables:} & & & \\
x_{k} & \in & \mathbb{Z}^{+}, \quad \forall k \in \mathcal{K}, & \text{(Number of units of spare part } k \text{ produced)} \\
& \text{with} & x_k \ge 1, & \quad \forall k \in \mathcal{K} \quad \text{(enforcing a non‐trivial mix)} \\[4mm]

\textbf{Mathematical Model:} & & & \\[2mm]
\textbf{Objective:} \quad \max \quad & Z &=& \sum_{k \in \mathcal{K}} p_{k} \, x_{k} \\[4mm]

\textbf{Subject to:} \\[2mm]
\text{Machine capacity constraints:} \quad 
& \sum_{k \in \mathcal{K}} T_{k,s} \, x_{k} & \le & \; C_{s}, \quad \forall s \in \mathcal{S}, \\[2mm]
\text{Non-negativity and integrality:} \quad
& x_{k} & \in & \; \mathbb{Z}^{+} \quad \forall k \in \mathcal{K}.
\end{array}
\]

This model fully specifies the manufacturing planning problem: each product requires specific processing times at each machine, profit is accrued per unit produced, and the total processing time on each machine is limited by its capacity. The additional lower bound constraint (i.e., \(x_k \ge 1\) for all \(k\)) prevents a trivial solution in which only one product is produced while all others are zero, ensuring a diversified product mix.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    K = 5
    S = 2
    # Time requirements: index 0 corresponds to spare part 1, etc.
    Time = [
        [2, 3],  # Spare part 1: time on machine 1 and machine 2
        [1, 2],  # Spare part 2
        [3, 2],  # Spare part 3
        [3, 1],  # Spare part 4
        [1, 1]   # Spare part 5
    ]
    Profit = [30, 20, 40, 25, 10]
    Capacity = [700, 1000]  # Machine capacities for machine 1 and 2

    # Create the solver using CBC for Mixed Integer Programming.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[k] >= 1 and integer for k in 0..K-1.
    x = []
    for k in range(K):
        var = solver.IntVar(1, solver.infinity(), f'x[{k}]')
        x.append(var)

    # Machine capacity constraints: For each machine s, sum_k (Time[k][s] * x[k]) <= Capacity[s]
    for s in range(S):
        constraint_expr = solver.Sum(Time[k][s] * x[k] for k in range(K))
        solver.Add(constraint_expr <= Capacity[s])

    # Objective: maximize profit = sum_k (Profit[k] * x[k])
    objective = solver.Objective()
    for k in range(K):
        objective.SetCoefficient(x[k], Profit[k])
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Solution:')
        print('Objective value =', objective.Value())
        for k in range(K):
            print(f'Spare part {k+1}: Production quantity =', x[k].solution_value())
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()