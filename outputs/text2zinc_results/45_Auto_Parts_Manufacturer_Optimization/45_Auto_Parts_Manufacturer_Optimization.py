# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices and Sets:} & & \\
p &\in& \mathcal{P} = \{1,2,\dots,P\} \quad \text{(auto parts)}\\[1mm]
m &\in& \mathcal{M} = \{1,2,\dots,M\} \quad \text{(machines)}\\[3mm]
\textbf{Decision Variables:} & & \\
x_p &\in& \mathbb{Z}_{\ge0}, \quad \forall\, p\in\mathcal{P} \quad \text{(number of batches of part } p\text{ produced)}\\[1mm]
l^{\text{std}} &\ge& 0 \quad \text{(labor hours on Machine 1 charged at the standard cost)}\\[1mm]
l^{\text{ot}} &\ge& 0 \quad \text{(labor hours on Machine 1 charged at the overtime cost)}\\[3mm]
\textbf{Parameters:} & & \\
\text{TimeRequired}_{m,p} &\in& \mathbb{R}_{>0}, \quad \forall\, m\in\mathcal{M},\, p\in\mathcal{P}\\[1mm]
\text{MachineCosts}_m &\in& \mathbb{R}_{>0}, \quad \forall\, m\in\mathcal{M}\\[1mm]
\text{Availability}_m &\in& \mathbb{R}_{>0}, \quad \forall\, m\in\mathcal{M}\setminus\{1\} \quad \text{(note: the availability constraint for Machine 1 is disregarded)}\\[1mm]
\text{Prices}_p &\in& \mathbb{R}_{>0}, \quad \forall\, p\in\mathcal{P}\\[1mm]
\text{MinBatches}_p &\in& \mathbb{Z}_{>0}, \quad \forall\, p\in\mathcal{P}\\[1mm]
\text{StandardCost} &\in& \mathbb{R}_{>0}\\[1mm]
\text{OvertimeCost} &\in& \mathbb{R}_{>0}\\[1mm]
\text{OvertimeHour} &\in& \mathbb{R}_{>0}\\[1mm]
\text{MinProfit} &\in& \mathbb{R}
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Model Formulation:} & & \\[1mm]
\textbf{Objective:} && \text{Maximize Profit } Z, \text{ where} \\[2mm]
Z &=& \displaystyle \sum_{p\in\mathcal{P}} \text{Prices}_p\,x_p \\[2mm]
&& \quad - \Bigg[ \, \underbrace{\text{StandardCost}\;l^{\text{std}} + \text{OvertimeCost}\;l^{\text{ot}}}_{\substack{\text{Labor cost for Machine 1 (outsourced)}}} + \underbrace{\sum_{m\in \mathcal{M}\setminus\{1\}} \text{MachineCosts}_m\,\Biggl( \sum_{p\in\mathcal{P}} \text{TimeRequired}_{m,p}\, x_p \Biggr)}_{\substack{\text{Operating cost for Machines }2,\dots,M}} \, \Bigg] \\[4mm]
\textbf{Subject to:} && \\[2mm]
\textbf{(1) Machine 1 Labor Hours Splitting:} && l^{\text{std}} + l^{\text{ot}} = \sum_{p\in\mathcal{P}} \text{TimeRequired}_{1,p}\, x_p \\[2mm]
\textbf{(2) Standard Labor Hours Limit:} && l^{\text{std}} \le \text{OvertimeHour} \\[2mm]
\textbf{(3) Availability Constraints for Machines }m=2,\dots,M: && \displaystyle \sum_{p\in\mathcal{P}} \text{TimeRequired}_{m,p}\,x_p \le \text{Availability}_m, \quad \forall\, m \in \mathcal{M}\setminus\{1\} \\[2mm]
\textbf{(4) Minimum Production Requirements:} && x_p \ge \text{MinBatches}_p,\quad \forall\, p\in\mathcal{P} \\[2mm]
\textbf{(5) Minimum Profit Constraint:} && Z \ge \text{MinProfit} \\[3mm]
&& \\
\textbf{Non-Negativity and Integer Constraints:} && x_p\in \mathbb{Z}_{\ge0},\quad l^{\text{std}} \ge 0,\quad l^{\text{ot}} \ge 0
\end{array}
\]

\[
\begin{array}{l}
\textbf{Notes:} \\[2mm]
\bullet \; \text{The decision variables } x_p \text{ represent the number of batches (each batch containing 100 parts) for part } p. \\[2mm]
\bullet \; \text{For Machine 1, since its individual availability is disregarded, the total labor hours required } \\
\quad \; \left(\sum_{p} \text{TimeRequired}_{1,p}\, x_p\right) \text{ are split into two parts: standard hours (up to } \text{OvertimeHour}\text{) and overtime hours.} \\[2mm]
\bullet \; \text{The cost of operating Machines } m=2,\dots,M \text{ is computed based on the time used per batch and the corresponding cost per hour.} \\[2mm]
\bullet \; \text{The objective is to maximize the net profit (i.e., revenues minus total operating costs), while ensuring that} \\
\quad \; \text{the net profit is at least } \text{MinProfit} \text{ and all production and availability constraints are satisfied.} \\[2mm]
\bullet \; \text{The formulation prevents trivial solutions, as each part must be produced in at least the minimum number of batches} \\
\quad \; \text{required by its contract, and production decisions must respect the machine hour limits and cost structure.}
\end{array}
\]

This complete formulation represents the entire real‐world manufacturing optimization problem with all its constraints and details.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    M = 3
    P = 4

    # Time required on each machine for each part (machines x parts):
    # Machine 1 (index 0): [2, 1, 3, 2]
    # Machine 2 (index 1): [4, 2, 1, 2]
    # Machine 3 (index 2): [6, 2, 1, 2]
    TimeRequired = [
        [2, 1, 3, 2],
        [4, 2, 1, 2],
        [6, 2, 1, 2]
    ]

    MachineCosts = [160, 10, 15]  # cost for machines 1,2,3 (machine 1 is outsourced)
    Availability = [200, 300, 500]  # machine 1 availability disregarded; machines 2 and 3 used
    Prices = [570, 250, 585, 430]
    MinBatches = [10, 10, 10, 10]

    StandardCost = 20
    OvertimeCost = 30
    OvertimeHour = 400
    MinProfit = 5000

    # Create the solver using CBC MIP Solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    infinity = solver.infinity()

    # Decision Variables
    # x[p]: number of batches of part p produced (integer)
    x = [solver.IntVar(0, infinity, f'x_{p}') for p in range(P)]
    
    # l_std: labor hours on Machine 1 (outsourced) charged at standard cost (continuous)
    l_std = solver.NumVar(0, infinity, 'l_std')
    # l_ot: labor hours on Machine 1 (outsourced) charged at overtime cost (continuous)
    l_ot = solver.NumVar(0, infinity, 'l_ot')

    # Constraint 1: Machine 1 Labor Hours Splitting
    # l_std + l_ot == sum_p (TimeRequired[0][p] * x[p])
    machine1_expr = solver.Sum([TimeRequired[0][p] * x[p] for p in range(P)])
    solver.Add(l_std + l_ot == machine1_expr)

    # Constraint 2: Standard Labor Hours Limit: l_std <= OvertimeHour
    solver.Add(l_std <= OvertimeHour)

    # Constraint 3: Availability Constraints for Machines 2 to M (m=2,...,M i.e. indices 1,...,M-1)
    for m in range(1, M):
        machine_expr = solver.Sum([TimeRequired[m][p] * x[p] for p in range(P)])
        solver.Add(machine_expr <= Availability[m])

    # Constraint 4: Minimum Production Requirements for each part
    for p in range(P):
        solver.Add(x[p] >= MinBatches[p])

    # Revenue expression: sum_p Prices[p] * x[p]
    revenue = solver.Sum([Prices[p] * x[p] for p in range(P)])

    # Labor cost on Machine 1 (outsourced): StandardCost*l_std + OvertimeCost*l_ot
    labor_cost = StandardCost * l_std + OvertimeCost * l_ot

    # Operating cost for Machines 2 to M (m=2,...,M)
    machine_operating_cost = solver.Sum(
        [MachineCosts[m] * solver.Sum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(1, M)]
    )

    total_cost = labor_cost + machine_operating_cost

    # Profit expression: revenue - total_cost
    profit = revenue - total_cost

    # Constraint 5: Minimum Profit Constraint: profit >= MinProfit
    solver.Add(profit >= MinProfit)

    # Objective: maximize profit
    solver.Maximize(profit)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Solution:')
        print('Optimal profit =', solver.Objective().Value())
        for p in range(P):
            print(f' Part {p+1} batches =', x[p].solution_value())
        print('Machine 1 standard labor hours (l_std) =', l_std.solution_value())
        print('Machine 1 overtime labor hours (l_ot)   =', l_ot.solution_value())

        # For additional clarity, print revenue and cost details:
        revenue_val = revenue.solution_value()
        labor_cost_val = labor_cost.solution_value()
        machine_cost_val = machine_operating_cost.solution_value()
        total_cost_val = total_cost.solution_value()
        profit_val = profit.solution_value()
        print('Revenue =', revenue_val)
        print('Labor cost (Machine 1) =', labor_cost_val)
        print('Operating cost (Machines 2 & 3) =', machine_cost_val)
        print('Total cost =', total_cost_val)
        print('Net Profit =', profit_val)
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()