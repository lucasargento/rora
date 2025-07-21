# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\quad & p \in \{1,2,\dots,P\} \quad (\text{Parts}), \quad m \in \{1,2,\dots,M\} \quad (\text{Machines}), \\[1mm]
\\
\textbf{Parameters:}\quad & \text{NumParts} = P,\quad \text{NumMachines} = M, \\[1mm]
& T_{mp} \quad \text{(hours required on machine } m \text{ to produce one batch of part } p\text{)}, \\[1mm]
& C_m \quad \text{(machine cost per operating hour for machine } m\text{)}, \\[1mm]
& A_m \quad \text{(regular availability in hours for machine } m \text{ per month)}, \\[1mm]
& O_m \quad \text{(overtime hours available for machine } m\text{ per month)}, \\[1mm]
& R_p \quad \text{(revenue obtained from selling one batch of part } p\text{)}, \\[1mm]
& B_p \quad \text{(minimum number of batches required for part } p\text{)}, \\[1mm]
& S \quad \text{(standard labor cost per hour for machine } 1\text{)}, \quad
L \quad \text{(overtime labor cost per hour for machine } 1\text{)}.
\end{align*}

\vspace{2mm}
\noindent
\textbf{Decision Variables:}
\begin{align*}
x_p &\in \mathbb{Z}_{+},\quad \forall p=1,\dots,P, && \text{(number of batches of part } p \text{ to produce)}; \\[1mm]
y &\ge 0, && \text{(number of regular (standard) labor hours used on machine 1)}; \\[1mm]
z &\ge 0, && \text{(number of overtime labor hours used on machine 1)}.
\end{align*}

\noindent
\textbf{Model:}
\begin{align*}
\textbf{Maximize} \quad Z =\; & \underbrace{\sum_{p=1}^{P} R_p\, x_p}_\text{Total revenue} \;-\; \Bigg[ \underbrace{S\, y + L\, z}_{\substack{\text{Labor cost for outsourced } \\ \text{machine } 1}} \;+\; \underbrace{\sum_{m=2}^{M} C_m \left(\sum_{p=1}^{P} T_{mp}\, x_p\right)}_{\substack{\text{Operating cost for internal } \\ \text{machines } m=2,\dots,M} } \Bigg] \\
\\[1mm]
\textbf{subject to:} \quad 
& \textbf{(1) Machine 1 labor splitting:} \quad y + z = \sum_{p=1}^{P} T_{1p}\, x_p, \\
\\[1mm]
& \textbf{(2) Standard hour limit for machine 1:} \quad y \le A_1, \quad \text{(even though machine 1 is outsourced,}\\
& \quad\quad\quad\quad\quad\quad\text{the first } A_1 \text{ hours are charged at the lower (standard) rate)}; \\
\\[1mm]
& \textbf{(3) Overtime hour limit for machine 1:} \quad z \le O_1, \\
\\[1mm]
& \textbf{(4) Capacity constraints for internal machines:} \quad \sum_{p=1}^{P} T_{mp}\, x_p \le A_m + O_m, \quad \forall m=2,\dots,M, \\
\\[1mm]
& \textbf{(5) Minimum production requirements:} \quad x_p \ge B_p, \quad \forall p=1,\dots,P, \\
\\[1mm]
& \textbf{(6) Nonnegativity and integrality:} \quad x_p \in \mathbb{Z}_{+}, \; y \ge 0, \; z \ge 0.
\end{align*}

\noindent
\textbf{Notes:}

1. For machine 1 the usual availability constraint is not directly imposed on production because the machine is outsourced. Instead, its workload (i.e. the sum of production times over all parts) is partitioned into standard hours (up to availability $A_1$) and overtime hours (limited by $O_1$).  
2. For machines $m = 2,\dots,M$, production must respect the sum of regular availability and allowed overtime.
3. The decision variables $x_p$ (batches to produce) are enforced to meet the contractual minimums $B_p$, thus avoiding trivial production scenarios.
4. All parameters and constraints are defined so that the model is both feasible and bounded.

This complete formulation accurately represents the manufacturing and production optimization problem as described.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Data
    NumMachines = 3
    NumParts = 4

    # Time required (hours) to produce one batch of part p on machine m.
    # Rows: machines 1,2,3; Columns: parts 1,2,3,4.
    TimeRequired = [
        [2, 1, 3, 2],  # Machine 1 (outsourced)
        [4, 2, 1, 2],  # Machine 2 (internal)
        [6, 2, 1, 2]   # Machine 3 (internal)
    ]
    # Operating cost per hour for each machine.
    MachineCosts = [160, 10, 15]
    # Regular availability (hours) per machine per month.
    Availability = [200, 300, 500]
    # Price (revenue) for selling one batch of each part.
    Prices = [570, 250, 585, 430]
    # Minimum batches required per part.
    MinBatches = [10, 10, 10, 10]
    # Labor costs for outsourced machine 1.
    StandardCost = 20     # Standard rate cost per hour for machine 1 (up to availability).
    OvertimeCost = 30     # Overtime rate cost per hour for machine 1.
    # Available overtime hours for each machine.
    OvertimeHour = [400, 400, 300]

    # Decision Variables
    # x[p]: number of batches of part p produced (integer, must satisfy min production requirements).
    x = []
    for p in range(NumParts):
        x_p = solver.IntVar(MinBatches[p], solver.infinity(), f'x_{p}')
        x.append(x_p)

    # y: number of standard (regular) labor hours used on outsourced machine 1.
    # z: number of overtime labor hours used on outsourced machine 1.
    y = solver.NumVar(0, Availability[0], 'y')  # y is bounded by Availability[0].
    z = solver.NumVar(0, OvertimeHour[0], 'z')    # z is bounded by overtime hours available for machine 1.

    # Constraints

    # (1) Machine 1 labor splitting: y + z equals total production time on machine 1.
    solver.Add(y + z == sum(TimeRequired[0][p] * x[p] for p in range(NumParts)))

    # (2) Constraint (2) Standard hour limit for machine 1 is handled in variable y's upper bound.
    # (3) Constraint (3) Overtime hour limit for machine 1 is handled in variable z's upper bound.

    # (4) Capacity constraints for internal machines (machines 2 to M).
    for m in range(1, NumMachines):
        solver.Add(sum(TimeRequired[m][p] * x[p] for p in range(NumParts)) <= Availability[m] + OvertimeHour[m])

    # (5) Minimum production requirements already enforced by lower bounds on x[p].

    # Objective Function: Maximize profit
    # Profit = Total revenue - (Labor cost for machine 1 + Operating cost for internal machines)
    revenue = solver.Sum(Prices[p] * x[p] for p in range(NumParts))
    labor_cost_machine1 = StandardCost * y + OvertimeCost * z
    internal_cost = solver.Sum(
        MachineCosts[m] * sum(TimeRequired[m][p] * x[p] for p in range(NumParts))
        for m in range(1, NumMachines)
    )
    solver.Maximize(revenue - labor_cost_machine1 - internal_cost)

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal Objective Value =', solver.Objective().Value())
        for p in range(NumParts):
            print(f'Batches of part {p+1} = {x[p].SolutionValue()}')
        print(f'Regular labor hours (y) = {y.solution_value()}')
        print(f'Overtime labor hours (z) = {z.solution_value()}')
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()