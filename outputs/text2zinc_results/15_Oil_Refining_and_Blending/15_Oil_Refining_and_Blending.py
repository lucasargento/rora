# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in I = \{1,\ldots,I\} \quad,\quad m \in M = \{1,\ldots,M\}. \\
\\
\textbf{Parameters:} \quad & \text{BuyPrice}_{i,m} \quad \text{(cost per ton of oil } i \text{ in month } m\text{)},\\[1mm]
& \text{SellPrice} \quad \text{(revenue per ton of final product)},\\[1mm]
& \text{IsVeg}_i \in \{0,1\} \quad \text{(1 if oil } i \text{ is vegetable, 0 otherwise)},\\[1mm]
& \text{MaxVegRefining} \quad \text{(maximum tons of vegetable oil that can be refined per month)},\\[1mm]
& \text{MaxNonvegRefining} \quad \text{(maximum tons of non‐vegetable oil that can be refined per month)},\\[1mm]
& \text{StorageSize} \quad \text{(maximum storage capacity in tons for each oil type)},\\[1mm]
& \text{StorageCost} \quad \text{(cost per ton per month for storing raw oil)},\\[1mm]
& \text{MaxHardness},\; \text{MinHardness} \quad \text{(upper and lower bounds on the hardness of the final product)},\\[1mm]
& \text{Hardness}_i \quad \text{(hardness value of oil } i\text{)},\\[1mm]
& \text{InitialAmount}_i \quad \text{(initial storage, in tons, of oil } i\text{)},\\[1mm]
& \text{MinUsage}_i \quad \text{(minimum usage in tons if oil } i \text{ is used in a month)},\\[1mm]
& \text{Dependencies}_{i,j} \in \{0,1\} \quad \text{(if } \text{Dependencies}_{i,j}=1, \text{ then use of oil } i \text{ requires use of oil } j\text{)}.
\\[3mm]
\textbf{Decision Variables:} & \\[1mm]
x_{i,m} &\ge 0,\quad \text{tons of raw oil } i \text{ purchased in month } m, \\[1mm]
u_{i,m} &\ge 0,\quad \text{tons of raw oil } i \text{ refined in month } m \; \Bigl(\text{note: no loss in refining} \Bigr), \\[1mm]
s_{i,m} &\ge 0,\quad \text{tons of oil } i \text{ held in storage at the end of month } m, \\[1mm]
z_{i,m} &\in \{0,1\},\quad \text{binary indicator: } z_{i,m}=1 \text{ if oil } i \text{ is used (i.e. } u_{i,m} >0\text{) in month } m.
\\[3mm]
\textbf{Auxiliary Notation:} \quad & V = \{ i \in I : \text{IsVeg}_i=1 \} \quad,\quad NV = \{ i \in I : \text{IsVeg}_i=0 \}.
\\[3mm]
\textbf{Objective Function:} \quad & \text{Maximize Profit } P, \text{ given by} \\
P =\; & \sum_{m \in M} \Biggl[ \, \text{SellPrice}\,\left(\sum_{i \in I} u_{i,m}\right) - \sum_{i \in I} \Bigl( \text{BuyPrice}_{i,m}\,x_{i,m} + \text{StorageCost}\,s_{i,m} \Bigr) \Biggr].
\\[3mm]
\textbf{Subject to:} & \\[1mm]
\textbf{(1) Inventory Flow (Balance) Equations:} \quad & \text{For each oil } i \in I \text{ and month } m=1,\ldots,M,\\[1mm]
& s_{i,0} = \text{InitialAmount}_i, \\[1mm]
& s_{i,1} = s_{i,0} + x_{i,1} - u_{i,1},\\[1mm]
& s_{i,m} = s_{i,m-1} + x_{i,m} - u_{i,m} \quad \forall\, m = 2,\ldots,M,\\[1mm]
& s_{i,M} = \text{InitialAmount}_i \quad \text{(the ending storage must equal the initial amount)}.
\\[3mm]
\textbf{(2) Storage Capacity:} \quad & \forall\, i \in I,\; \forall\, m \in M:\quad 0 \le s_{i,m} \le \text{StorageSize}.
\\[3mm]
\textbf{(3) Refining Capacity Limits:} \quad & \forall\, m \in M: \\[1mm]
& \sum_{i \in V} u_{i,m} \le \text{MaxVegRefining},\\[1mm]
& \sum_{i \in NV} u_{i,m} \le \text{MaxNonvegRefining}.
\\[3mm]
\textbf{(4) Technological (Hardness) Constraints:} \quad & \forall\, m \in M \text{ such that } \sum_{i\in I} u_{i,m} > 0: \\[1mm]
& \text{MinHardness} \left(\sum_{i \in I} u_{i,m}\right) \le \sum_{i \in I} \text{Hardness}_i\,u_{i,m} \le \text{MaxHardness} \left(\sum_{i \in I} u_{i,m}\right). 
\\[3mm]
\textbf{(5) Minimum Usage and Linking to Binary Variables:} \quad & \forall\, i \in I,\; \forall\, m \in M:\\[1mm]
& u_{i,m} \ge \text{MinUsage}_i \, z_{i,m}, \\[1mm]
& u_{i,m} \le M^{\max}_{i,m}\, z_{i,m}, \quad \text{where } M^{\max}_{i,m} \text{ is a sufficiently large constant.}
\\[3mm]
\textbf{(6) Maximum Number of Oils Used (Mixing Limit):} \quad & \forall\, m \in M: \quad \sum_{i \in I} z_{i,m} \le 3.
\\[3mm]
\textbf{(7) Dependency Constraints:} \quad & \forall\, m \in M,\; \forall\, i,j \in I \text{ with } \text{Dependencies}_{i,j}=1: \quad z_{i,m} \le z_{j,m}.
\\[3mm]
\textbf{(8) Domain Constraints:} \quad & \forall\, i \in I,\; \forall\, m \in M: \\
& x_{i,m} \ge 0,\quad u_{i,m} \ge 0,\quad s_{i,m} \ge 0,\\[1mm]
& z_{i,m} \in \{0,1\}.
\end{align*}

\textbf{Notes:}
\begin{itemize}
  \item The inventory balance (1) ensures that the amount of oil carried over in storage reflects past purchases and usage, and the final storage is fixed to the given initial levels.
  \item The hardness constraints (4) use a weighted average formulation. (When no oil is processed in a month, these constraints are inactive.)
  \item Constraint (5) ensures that if an oil is used (i.e. $z_{i,m}=1$) then at least $\text{MinUsage}_i$ tons must be processed.
  \item Constraint (6) guarantees that in any month no more than three distinct oils are blended to form the final product.
  \item Constraint (7) captures any technological dependencies among oils as given.
  \item The objective maximizes the total profit earned over all months, accounting for raw material purchasing and storage costs against sales revenue.
\end{itemize}

This complete formulation reflects the full manufacturing and production problem with all the details provided, ensuring feasibility and boundedness without trivializing the product mix.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Data
    M = 6  # number of months
    I = 5  # number of oils

    # Buy prices given as 6 rows (months) x 5 columns (oils)
    buy_prices = [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135],
    ]
    sell_price = 150

    # Oil characteristics
    is_veg = [1, 1, 0, 0, 0]  # 1 if vegetable, 0 otherwise
    max_veg_refine = 200
    max_nonveg_refine = 250
    storage_capacity = 1000
    storage_cost = 5

    # It seems MinHardness and MaxHardness might be swapped in the description.
    # Here we assume final product hardness must lie between min_hardness and max_hardness.
    # We choose min_hardness=3 and max_hardness=6.
    min_hardness = 3
    max_hardness = 6
    hardness = [8.8, 6.1, 2.0, 4.2, 5.0]

    initial_amount = 500  # initial storage for each oil (for m=0 state)
    min_usage = 20

    # Dependencies: Dependencies[i][j] == 1 means if oil i is used then oil j must be used.
    # Data as given:
    # Row0: oil0 -> oil4 ; Row1: oil1 -> oil4 ; others: no dependency.
    dependencies = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    bigM = 1e5

    # Decision Variables:
    # x[i][m]: tons of raw oil i purchased in month m.
    x = {}
    # u[i][m]: tons of raw oil i refined in month m.
    u = {}
    # z[i][m]: binary: 1 if oil i is used (u>0) in month m.
    z = {}
    # s[i][m]: tons in storage for oil i at end of period m.
    # Inventory periods: m = 0, ..., M where m=0 is initial inventory.
    s = {}

    for i in range(I):
        for m in range(M):
            x[i, m] = solver.NumVar(0.0, solver.infinity(), f'x[{i},{m}]')
            u[i, m] = solver.NumVar(0.0, solver.infinity(), f'u[{i},{m}]')
            z[i, m] = solver.IntVar(0, 1, f'z[{i},{m}]')
        # Create s for periods 0 to M (M+1 periods)
        for m in range(M+1):
            # For m = 0, fix storage to initial amount.
            if m == 0:
                s[i, m] = solver.NumVar(initial_amount, initial_amount, f's[{i},{m}]')
            else:
                s[i, m] = solver.NumVar(0.0, storage_capacity, f's[{i},{m}]')

    # Constraints

    # (1) Inventory Flow Equations:
    for i in range(I):
        for m in range(M):
            # s[i, m+1] = s[i, m] + x[i, m] - u[i, m]
            solver.Add(s[i, m+1] == s[i, m] + x[i, m] - u[i, m])
        # Final storage equals initial amount
        solver.Add(s[i, M] == initial_amount)

    # (2) Storage Capacity already enforced by variable bounds for s[i, m] for m>=1.

    # (3) Refining Capacity Limits per month:
    for m in range(M):
        # Vegetable oils
        solver.Add(solver.Sum(u[i, m] for i in range(I) if is_veg[i] == 1) <= max_veg_refine)
        # Non-vegetable oils
        solver.Add(solver.Sum(u[i, m] for i in range(I) if is_veg[i] == 0) <= max_nonveg_refine)

    # (4) Hardness Constraints: for each month m, if any oil is processed.
    for m in range(M):
        total_refined = solver.Sum(u[i, m] for i in range(I))
        weighted_hardness = solver.Sum(hardness[i] * u[i, m] for i in range(I))
        # When total_refined is zero, these constraints are trivially satisfied.
        solver.Add(weighted_hardness >= min_hardness * total_refined)
        solver.Add(weighted_hardness <= max_hardness * total_refined)

    # (5) Minimum Usage and Linking to Binary Variables:
    for i in range(I):
        for m in range(M):
            solver.Add(u[i, m] >= min_usage * z[i, m])
            solver.Add(u[i, m] <= bigM * z[i, m])

    # (6) Maximum Number of Oils Used (Mixing Limit) per month:
    for m in range(M):
        solver.Add(solver.Sum(z[i, m] for i in range(I)) <= 3)

    # (7) Dependency Constraints:
    # If Dependencies[i][j] == 1 then z[i,m] <= z[j,m]
    for m in range(M):
        for i in range(I):
            for j in range(I):
                if dependencies[i][j] == 1:
                    solver.Add(z[i, m] <= z[j, m])

    # (8) Domain constraints are handled by variables declarations.

    # Objective: Maximize profit over all months.
    # Profit = Sum_m [ sell_price * sum_i u[i,m] - sum_i (buy_price[m][i]* x[i,m] + storage_cost * s[i, m+1] ) ]
    revenue = 0
    cost = 0
    for m in range(M):
        revenue += sell_price * solver.Sum(u[i, m] for i in range(I))
        for i in range(I):
            cost += buy_prices[m][i] * x[i, m]
            # storage cost is applied on storage at end of month m+1 (m>=0, m+1 from 1 to M)
            cost += storage_cost * s[i, m+1]
    solver.Maximize(revenue - cost)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal Objective Value =", solver.Objective().Value())
        for m in range(M):
            print(f"\nMonth {m+1}:")
            for i in range(I):
                xi = x[i, m].solution_value()
                ui = u[i, m].solution_value()
                zi = z[i, m].solution_value()
                print(f"  Oil {i+1}: Purchase = {xi:.2f}, Refine = {ui:.2f}, Used = {int(zi)}")
            # Also print combined refining in month m.
            total_u = sum(u[i, m].solution_value() for i in range(I))
            print(f"  Total refined: {total_u:.2f}")
        for i in range(I):
            print(f"\nFinal storage for Oil {i+1}:")
            # s[i,M] should equal the initial amount.
            print(f"  Storage = {s[i, M].solution_value():.2f}")
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()