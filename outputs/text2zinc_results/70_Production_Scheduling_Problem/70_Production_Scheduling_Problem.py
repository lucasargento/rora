# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:} \quad & t \in \{1,2,\ldots, T\} \quad \text{with } T=3,\\[1mm]
& D_t \text{ is the demand in period } t,\quad \text{with } D_1=10,\; D_2=20,\; D_3=10,\\[1mm]
& M \text{ is the maximum production amount under regular conditions (per period), with } M=5,\\[1mm]
& c_R \text{ is the cost per unit of regular production, with } c_R=10,\\[1mm]
& c_O \text{ is the cost per unit of overtime production, with } c_O=12,\\[1mm]
& h \text{ is the cost per unit of storing a product for one period, with } h=1.\\[2mm]
\textbf{Decision Variables:}\\[1mm]
& x_t^R \ge 0: \text{Units produced in period } t \text{ under regular production},\\[1mm]
& x_t^O \ge 0: \text{Units produced in period } t \text{ under overtime production},\\[1mm]
& s_t \ge 0: \text{Inventory (stored units) at the end of period } t.\\[2mm]
\textbf{Objective Function:}\\[1mm]
& \text{Minimize the total cost:} \\
& \quad \min \; Z = \sum_{t=1}^{T} \Bigl( c_R\, x_t^R + c_O\, x_t^O + h\, s_t \Bigr).\\[2mm]
\textbf{Constraints:}\\[1mm]
\textbf{(a) Inventory Balance Constraints:} \quad & \\
& s_0 = 0, \quad \text{(initial inventory)};\\[1mm]
& s_t = s_{t-1} + x_t^R + x_t^O - D_t, \quad \forall\, t=1,\ldots,T.\\[1mm]
\textbf{(b) Regular Production Capacity Constraints:} \quad & \\
& x_t^R \le M, \quad \forall\, t=1,\ldots,T.\\[1mm]
\textbf{(c) Non-negativity Constraints:} \quad & \\
& x_t^R \ge 0,\quad x_t^O \ge 0,\quad s_t \ge 0,\quad \forall\, t=1,\ldots,T.
\end{align*}

This formulation accurately models the production scheduling problem where the demand in each period must be met (through current production and possible inventory from previous periods), regular production is limited to M units per period, and overtime production is available at a higher cost. The objective is to minimize the sum of production and inventory holding costs over all periods while satisfying the demand exactly.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    T = 3  # Number of periods
    demand = [10.0, 20.0, 10.0]  # Demand in each period: period 1, period 2, period 3
    max_regular = 5.0  # Maximum production under regular conditions per period
    cost_regular = 10.0  # Cost per unit of regular production
    cost_overtime = 12.0  # Cost per unit of overtime production
    store_cost = 1.0  # Inventory holding cost per unit per period

    # Create the solver with CBC backend (Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables:
    # Regular production and overtime production for each period.
    x_reg = [solver.NumVar(0, max_regular, f"x_reg_{t}") for t in range(T)]
    x_ot = [solver.NumVar(0, solver.infinity(), f"x_ot_{t}") for t in range(T)]
    # Inventory at end of each period.
    s = [solver.NumVar(0, solver.infinity(), f"s_{t}") for t in range(T)]

    # Constraints:
    # Inventory balance constraints.
    # For period 1:
    # s0 = 0 (initial inventory is 0) is implicit, so for t=0: s0 = x_reg[0] + x_ot[0] - demand[0]
    solver.Add(x_reg[0] + x_ot[0] - demand[0] == s[0])
    # For periods t >= 2:
    for t in range(1, T):
        # s[t] = s[t-1] + x_reg[t] + x_ot[t] - demand[t]
        solver.Add(s[t-1] + x_reg[t] + x_ot[t] - demand[t] == s[t])

    # Objective function: Minimize total cost = sum{cost_regular*x_reg + cost_overtime*x_ot + store_cost*s}
    objective = solver.Objective()
    for t in range(T):
        objective.SetCoefficient(x_reg[t], cost_regular)
        objective.SetCoefficient(x_ot[t], cost_overtime)
        objective.SetCoefficient(s[t], store_cost)
    objective.SetMinimization()

    # Solve the model.
    status = solver.Solve()

    # Check if a solution has been found.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("Total cost =", solver.Objective().Value())
        for t in range(T):
            print(f"Period {t+1}: Regular = {x_reg[t].SolutionValue()}, Overtime = {x_ot[t].SolutionValue()}, Inventory = {s[t].SolutionValue()}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()