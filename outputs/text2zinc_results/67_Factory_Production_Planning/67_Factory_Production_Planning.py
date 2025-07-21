# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\quad
& k \in \{1,\dots,K\} \quad\text{(products)},\\[1mm]
& m \in \{1,\dots,M\} \quad\text{(machine types)},\\[1mm]
& i \in \{1,\dots,I\} \quad\text{(time periods; i.e., months)}.\\[2mm]
\textbf{Parameters:}\quad
& \text{NumMachines}_m,\; m=1,\dots,M, \quad\text{number of machines of type } m,\\[1mm]
& \text{Profit}_k,\; k=1,\dots,K, \quad\text{profit obtained per unit sold of product } k,\\[1mm]
& T_{k,m},\; k=1,\dots,K,\; m=1,\dots,M, \quad\text{machine time (in hours) required to produce one unit of product } k \text{ on machine } m,\\[1mm]
& \text{Downtime}_m,\; m=1,\dots,M, \quad\text{number of months machine type } m \text{ must be down for maintenance,}\\[1mm]
& \text{Limit}_{k,i},\; k=1,\dots,K,\; i=1,\dots,I,\quad\text{upper bound on production quantity of product } k \text{ in month } i,\\[1mm]
& \text{StorePrice},\quad\text{storage cost per unit per month (e.g., }0.5\text{)},\\[1mm]
& \text{KeepQuantity},\quad\text{minimum inventory to keep at the end of months } i\ge 2 \text{ (e.g., }100\text{)},\\[1mm]
& \text{WorkHours},\quad\text{number of working hours per shift (e.g., }8\text{)}.\\[1mm]
& \text{C} = 24\text{ days} \times 2\text{ shifts/day} \times \text{WorkHours} \quad\text{(total available hours per machine per month if operational).}\\[2mm]
\textbf{Decision Variables:}\\[1mm]
& x_{k,i} \ge 0\quad\text{[continuous or integer]}: \quad\text{units of product } k \text{ produced in month } i,\\[1mm]
& y_{k,i} \ge 0\quad\text{[continuous or integer]}: \quad\text{units of product } k \text{ sold in month } i,\\[1mm]
& s_{k,i} \ge 0\quad\text{[continuous or integer]}: \quad\text{inventory (stock) level of product } k \text{ at the end of month } i,\\[1mm]
& z_{m,i} \in \{0,1\}:\quad\text{1 if machine type } m \text{ is operational in month } i,\text{ 0 if under maintenance.}\\[2mm]
\textbf{Objective Function:}\\[1mm]
\text{Maximize } \quad & Z = \sum_{i=1}^I \sum_{k=1}^K \left( \text{Profit}_k \, y_{k,i} - \text{StorePrice}\, s_{k,i} \right). \\[2mm]
\textbf{Constraints:}\\[1mm]
\underline{\text{(1) Inventory Balance:}}\\[1mm]
& s_{k,1} = x_{k,1} - y_{k,1} \quad \forall\, k=1,\dots,K,\\[1mm]
& s_{k,i} = s_{k,i-1} + x_{k,i} - y_{k,i} \quad \forall\, k=1,\dots,K,\; i=2,\dots,I.\\[2mm]
\underline{\text{(2) Storage Limits:}}\\[1mm]
& s_{k,i} \le 100 \quad \forall\, k=1,\dots,K,\; i=1,\dots,I,\\[1mm]
& s_{k,i} \ge \text{KeepQuantity} \quad \forall\, k=1,\dots,K,\; i=2,\dots,I.\\[2mm]
\underline{\text{(3) Production Capacity via Machines:}}\\[1mm]
& \sum_{k=1}^K T_{k,m}\, x_{k,i} \le z_{m,i}\cdot \text{NumMachines}_m \cdot C,\quad \forall\, m=1,\dots,M,\; i=1,\dots,I,\\[1mm]
& \text{with } C=24\times2\times\text{WorkHours}.\\[2mm]
\underline{\text{(4) Production Limits:}}\\[1mm]
& x_{k,i} \le \text{Limit}_{k,i} \quad \forall\, k=1,\dots,K,\; i=1,\dots,I.\\[2mm]
\underline{\text{(5) Maintenance Scheduling for Machines:}}\\[1mm]
& \sum_{i=1}^I z_{m,i} = I - \text{Downtime}_m, \quad \forall\, m=1,\dots,M.\\[2mm]
\underline{\text{(6) Non-Trivial Production (to avoid degenerate scenarios):}}\\[1mm]
& \sum_{k=1}^K y_{k,i} \ge \epsilon \quad \forall\, i=1,\dots,I, \quad \text{with } \epsilon > 0 \text{ (a small positive number)}.\\[2mm]
\textbf{Variable Domains:}\\[1mm]
& x_{k,i}\ge 0,\quad y_{k,i}\ge 0,\quad s_{k,i}\ge 0\quad \forall\, k=1,\dots,K,\; i=1,\dots,I,\\[1mm]
& z_{m,i}\in\{0,1\}\quad \forall\, m=1,\dots,M,\; i=1,\dots,I.
\end{align*}

\vspace{3mm}
\textbf{Explanation:}\\
1. The decision variables x, y, and s denote production, sales, and inventory levels, respectively, for every product and period. The binary variables z indicate whether each machine type is operational (1) or undergoing maintenance (0) in each month.\\[1mm]
2. The objective is to maximize the net profit obtained from sales revenues (Profit × units sold) minus the cost incurred by storing unsold inventory.\\[1mm]
3. Constraint (1) enforces the flow balance—inventory carried over is what was produced minus what was sold. Constraint (2) limits storage capacity and enforces a minimum inventory (except possibly in the first period). Constraint (3) guarantees that the production scheduled does not exceed the available machine time; note that if a machine is down (i.e. z_{m,i}=0), no production can use that machine in that month. Constraint (4) enforces product‐specific production limits per month. Constraint (5) ensures that for each machine type, exactly the prescribed number of months (I – Downtime) they are operational. Finally, constraint (6) excludes trivial solutions where no sales occur.\\[1mm]
4. This formulation is complete, feasible, and bounded given the finite production limits and machine capacities.
\medskip

This model is self–contained and fully represents the manufacturing, storage, and maintenance scheduling decisions necessary to maximize profit in the given setting.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver (CBC is a MIP solver)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # ----- Problem Data -----
    # Indices sizes
    M = 5  # number of machine types
    K = 7  # number of products
    I = 6  # number of time periods (months)

    # Parameters
    NumMachines = [4, 2, 3, 1, 1]  # for machine types 0..4
    Profit = [10, 6, 8, 4, 11, 9, 3]  # profit per unit sold for each product

    # Time required (hours) to produce one unit of product k on machine m.
    # Provided data is for products 0..5; we add a row of zeros for product 6.
    Time = [
        [0.5, 0.1, 0.2, 0.05, 0.0],   # product 0
        [0.7, 0.2, 0.0, 0.03, 0.0],    # product 1
        [0.0, 0.0, 0.8, 0.0, 0.01],    # product 2
        [0.0, 0.3, 0.0, 0.07, 0.0],    # product 3
        [0.3, 0.0, 0.0, 0.1, 0.05],    # product 4
        [0.5, 0.0, 0.6, 0.08, 0.05],   # product 5
        [0.0, 0.0, 0.0, 0.0, 0.0]      # product 6 (added extra row)
    ]

    # Downtime in months for each machine type (m index 0..4)
    Downtime = [0, 1, 1, 1, 1]

    # Production Limit matrix for each product (rows) and month (columns)
    # Using first 42 numbers in row-major order to form a 7x6 matrix.
    Limit = [
        [500, 600, 300, 200,   0, 500],   # product 0
        [1000, 500, 600, 300, 100, 500],   # product 1
        [300, 200,   0, 400, 500, 100],    # product 2
        [300, 200, 100, 300,   0,   0],    # product 3
        [500, 100, 300, 800, 400, 500],     # product 4
        [200, 1000,1100, 200, 300, 400],     # product 5
        [0,   300, 500, 100, 150, 100]      # product 6
    ]

    StorePrice = 0.5    # cost per unit stored per month
    KeepQuantity = 100  # minimum inventory to keep (except first month)
    WorkHours = 8.0
    C = 24 * 2 * WorkHours  # Total available hours per machine per month

    epsilon = 1  # small positive number to enforce non-trivial sales

    # ----- Decision Variables -----
    # x[k][i]: units produced of product k in month i.
    # y[k][i]: units sold of product k in month i.
    # s[k][i]: ending inventory for product k at end of month i.
    x = {}
    y = {}
    s = {}
    for k in range(K):
        for i in range(I):
            # Production and sales: non-negative integers.
            x[k, i] = solver.IntVar(0, Limit[k][i], f'x_{k}_{i}')
            y[k, i] = solver.IntVar(0, Limit[k][i], f'y_{k}_{i}')
            # Inventory: bounded above by storage limit 100 (as per constraint).
            s[k, i] = solver.IntVar(0, 100, f's_{k}_{i}')

    # z[m][i]: binary variable indicating if machine type m is operational in month i.
    z = {}
    for m in range(M):
        for i in range(I):
            z[m, i] = solver.BoolVar(f'z_{m}_{i}')

    # ----- Constraints -----

    # (1) Inventory Balance:
    for k in range(K):
        # For first month: s[k,0] = x[k,0] - y[k,0]
        solver.Add(s[k, 0] == x[k, 0] - y[k, 0])
        # For subsequent months:
        for i in range(1, I):
            solver.Add(s[k, i] == s[k, i - 1] + x[k, i] - y[k, i])

    # (2) Storage Limits:
    for k in range(K):
        for i in range(I):
            # s[k,i] <= 100 is already enforced by the variable's upper bound.
            if i >= 1:
                solver.Add(s[k, i] >= KeepQuantity)

    # (3) Production Capacity via Machines:
    for m in range(M):
        for i in range(I):
            # Sum over products: T[k][m] * x[k,i]
            production_time = solver.Sum(Time[k][m] * x[k, i] for k in range(K))
            # Capacity available when machine is operational:
            solver.Add(production_time <= z[m, i] * NumMachines[m] * C)

    # (4) Production Limits:
    for k in range(K):
        for i in range(I):
            solver.Add(x[k, i] <= Limit[k][i])

    # (5) Maintenance Scheduling for Machines:
    for m in range(M):
        # Sum_{i} z[m,i] == I - Downtime[m]
        solver.Add(solver.Sum(z[m, i] for i in range(I)) == I - Downtime[m])

    # (6) Non-Trivial Production (sales must be at least epsilon):
    for i in range(I):
        solver.Add(solver.Sum(y[k, i] for k in range(K)) >= epsilon)

    # ----- Objective Function ---
    # Maximize total profit = Sum_{i,k} (Profit[k] * y[k,i] - StorePrice * s[k,i])
    objective = solver.Sum(Profit[k] * y[k, i] - StorePrice * s[k, i] for k in range(K) for i in range(I))
    solver.Maximize(objective)

    # ----- Solve the Problem -----
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Solution:')
        print(f'Optimal objective value = {solver.Objective().Value()}')
        print()
        for i in range(I):
            print(f'--- Month {i + 1} ---')
            for k in range(K):
                prod = x[k, i].SolutionValue()
                sold = y[k, i].SolutionValue()
                inv = s[k, i].SolutionValue()
                if prod or sold or inv:
                    print(f'Product {k + 1}: Produced = {prod}, Sold = {sold}, Inventory = {inv}')
            for m in range(M):
                status_str = "Operational" if z[m, i].SolutionValue() > 0.5 else "Maintenance"
                print(f'Machine type {m + 1}: {status_str}')
            print()
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()