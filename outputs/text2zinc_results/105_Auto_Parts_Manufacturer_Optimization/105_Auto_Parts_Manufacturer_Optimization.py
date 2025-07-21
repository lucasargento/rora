# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & m \in \{1,\ldots, M\} \quad \text{(machines)}, \quad p \in \{1,\ldots, P\} \quad \text{(part types)}. \\[1mm]
%
\textbf{Parameters:} \quad &
\begin{array}{lcl}
\text{TimeRequired}_{m,p}  &:& \text{Time (hours) needed on machine } m \text{ for one batch of part } p, \\
\text{MachineCost}_{m}     &:& \text{Cost (per hour) of operating machine } m,\\[1mm]
\text{Availability}_{m}    &:& \text{Total hours available on machine } m \text{ per month},\\[1mm]
\text{Price}_p             &:& \text{Revenue obtained (per batch of 100 parts) of part } p,\\[1mm]
\text{SetupTime}_p         &:& \text{Setup time (in hours) required on machine 1 prior to producing part } p.
\end{array} \\[2mm]
%
\textbf{Decision Variables:} \quad &
\begin{array}{rcl}
x_p &\in& \mathbb{Z}_{\ge 0} \quad \text{-- number of batches of part } p \text{ produced in a month},\\[1mm]
y_p &\in& \{0,1\} \quad \text{-- binary variable indicating whether production of part } p \text{ occurs}.
\end{array} \\[2mm]
%
\textbf{Auxiliary (Big M):} \quad &
\text{For each part } p,\text{ choose a sufficiently large constant } U_p \text{ so that } x_p \le U_p \text{ if } y_p=1.
\\[2mm]
%
\textbf{Objective Function:} \\
\text{Maximize} \quad & Z = \underbrace{\sum_{p=1}^{P} \text{Price}_p\, x_p}_{\text{Total Revenue}} - 
\underbrace{\sum_{m=1}^{M} \text{MachineCost}_{m} \left( \sum_{p=1}^{P} \gamma_{m,p} \right)}_{\text{Total Machine Operating Cost}},
\end{align*}

where the machine-time consumption terms are defined by
\[
\gamma_{m,p} = \begin{cases}
\text{SetupTime}_p\, y_p + \text{TimeRequired}_{1,p}\, x_p, & \text{if } m=1,\\[1mm]
\text{TimeRequired}_{m,p}\, x_p, & \text{if } m=2,\ldots,M.
\end{cases}
\]

\begin{align*}
%
\textbf{Constraints:} \quad\\[1mm]
%\text{(1) Machine capacity constraints:} \\[0.5mm]
\text{For } m=1:\quad & \sum_{p=1}^{P}\left( \text{SetupTime}_p\, y_p + \text{TimeRequired}_{1,p}\, x_p \right) \le \text{Availability}_1,\\[1mm]
\text{For } m=2,\ldots, M:\quad & \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p \le \text{Availability}_m,\\[2mm]
%
%\text{(2) Linking production and setup decisions:} \\[0.5mm]
\text{For each } p=1,\ldots,P:\quad & x_p \le U_p\, y_p,\\[2mm]
%
%\text{(3) Nonnegativity and integrality:} \\[0.5mm]
& x_p \in \mathbb{Z}_{\ge 0}, \quad y_p \in \{0,1\} \quad \text{for all } p=1,\ldots,P.
\end{align*}

\vspace{2mm}
\textbf{Explanation:} 

1. Decision Variables:
   - x_p represents the number of batches (each of 100 parts) of part p produced in a month.
   - y_p is a binary variable activated (equal to 1) if any batch of part p is produced; this activation incurs the setup time cost on machine 1.
   
2. Objective Function:
   - We maximize profit, given by total revenue (sales price per batch times batches produced) minus the total cost of operating each machine. For machine 1 the operating cost includes both the setup time (if applicable) and the production time per batch; for other machines only production processing time is considered.

3. Constraints:
   - Machine capacity constraints ensure that the sum of the operating hours (including the setup time for machine 1) does not exceed the available machine hours.
   - The linking constraints enforce that if no batches of a part are produced (i.e., \(y_p=0\)) then \(x_p=0\); if \(x_p>0\) then \(y_p\) must be 1.
   - Nonnegativity and integrality constraints ensure a meaningful production plan.

This complete model reflects the entire manufacturing and production problem accurately and is both feasible and bounded under appropriate choices of the constants \(U_p\).'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Data parameters
    M = 3
    P = 4

    # Time required: rows correspond to machines (m=0,1,2), columns to parts (p=0,..,3)
    TimeRequired = [
        [2, 1, 3, 2],  # Machine 1
        [4, 2, 1, 2],  # Machine 2
        [6, 2, 1, 2]   # Machine 3
    ]

    MachineCosts = [160, 10, 15]
    Availability = [200, 300, 500]
    Prices = [570, 250, 585, 430]
    SetupTime = [12, 8, 4, 0]

    # Create model
    model = cp_model.CpModel()

    # Decision variables:
    # x[p] = number of batches produced for part p (non-negative integer)
    # y[p] = 1 if part p is produced (setup incurred), 0 otherwise
    x = [model.NewIntVar(0, 10000, f'x_{p}') for p in range(P)]
    y = [model.NewBoolVar(f'y_{p}') for p in range(P)]

    # Compute Big-M constants U_p for linking constraints (based on machine 1 capacity)
    U = []
    for p in range(P):
        # Avoid division by zero if TimeRequired[0][p] is 0 (should not occur in this problem)
        if TimeRequired[0][p] > 0:
            max_batches = (Availability[0] - SetupTime[p]) // TimeRequired[0][p]
            U.append(max_batches if max_batches >= 0 else 0)
        else:
            U.append(10000)
    
    # Linking constraints: if y[p] = 0 then x[p] = 0; else x[p] <= U[p]
    for p in range(P):
        model.Add(x[p] <= U[p] * y[p])

    # Machine capacity constraints

    # For machine 1: sum_p (SetupTime[p]*y[p] + TimeRequired[0][p]*x[p]) <= Availability[0]
    machine1_expr = []
    for p in range(P):
        machine1_expr.append(SetupTime[p] * y[p] + TimeRequired[0][p] * x[p])
    model.Add(sum(machine1_expr) <= Availability[0])

    # For machines 2 to M: sum_p TimeRequired[m][p] * x[p] <= Availability[m]
    for m in range(1, M):
        expr = []
        for p in range(P):
            expr.append(TimeRequired[m][p] * x[p])
        model.Add(sum(expr) <= Availability[m])

    # Objective function:
    # Profit = Total revenue - Total machine operating cost
    # Revenue: sum_p Prices[p] * x[p]
    # Machine cost:
    #   For machine 1: cost = MachineCosts[0]*(SetupTime[p]*y[p] + TimeRequired[0][p]*x[p])
    #   For machine m=2..M: cost = MachineCosts[m]*(TimeRequired[m][p]*x[p])
    revenue = sum(Prices[p] * x[p] for p in range(P))
    cost_machine1 = sum(MachineCosts[0] * (SetupTime[p] * y[p] + TimeRequired[0][p] * x[p]) for p in range(P))
    cost_other = 0
    for m in range(1, M):
        cost_other += sum(MachineCosts[m] * TimeRequired[m][p] * x[p] for p in range(P))
    profit = revenue - (cost_machine1 + cost_other)
    model.Maximize(profit)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f'Optimal profit: {solver.ObjectiveValue()}')
        for p in range(P):
            batches = solver.Value(x[p])
            produced = solver.Value(y[p])
            print(f'Part {p + 1}: Batches produced = {batches}, Production selected = {produced}')
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()