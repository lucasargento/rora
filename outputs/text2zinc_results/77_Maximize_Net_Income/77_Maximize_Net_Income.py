# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\\[1mm]
& i \in \{1,\dots,P\} \quad \text{(products)} \\[2mm]
\textbf{Decision Variables:}\\[1mm]
& x_i \in \mathbb{Z}_+, \quad \text{for } i=1,\dots,P, \quad \text{(number of units of product } i \text{ produced)}\\[1mm]
& y \in \{0,1\}, \quad \text{where } y=1 \text{ if the machinery upgrade is performed, and } y=0 \text{ otherwise.}\\[2mm]
\textbf{Parameters:}\\[1mm]
& P:\, \text{number of products.}\\[1mm]
& \text{Cash} \ge 0:\, \text{initial cash available for investments.}\\[1mm]
& \text{Hour}_i>0:\, \text{machine hours required per unit of product } i, \quad i=1,\dots,P.\\[1mm]
& \text{Cost}_i>0:\, \text{production cost per unit of product } i, \quad i=1,\dots,P.\\[1mm]
& \text{Price}_i>0:\, \text{selling price per unit of product } i, \quad i=1,\dots,P.\\[1mm]
& \text{InvestPercentage}_i \in [0,1]:\, \text{percentage of the sales revenue of product } i \text{ that must be reinvested},\quad i=1,\dots,P.\\[1mm]
& \text{UpgradeHours} \ge 0:\, \text{additional machine hours available if the upgrade is performed.}\\[1mm]
& \text{UpgradeCost} \ge 0:\, \text{cash cost to perform the upgrade.}\\[1mm]
& \text{AvailableHours} \ge 0:\, \text{base machine hours available in the production period.}\\[2mm]
\textbf{Objective Function:}\\[1mm]
\text{Maximize} \quad & Z = \sum_{i=1}^{P} \Bigl[ \Bigl( (1-\text{InvestPercentage}_i)\,\text{Price}_i - \text{Cost}_i \Bigr)x_i \Bigr] - \text{UpgradeCost}\,y.
\end{align*}

\noindent
\textbf{Subject to:}

\begin{align*}
\text{(Cash constraint):} \quad & \sum_{i=1}^{P} \text{Cost}_i\, x_i + \text{UpgradeCost}\, y \le \text{Cash} + \sum_{i=1}^{P} \text{InvestPercentage}_i\, \text{Price}_i\, x_i,\\[1mm]
\text{(Machine capacity constraint):} \quad & \sum_{i=1}^{P} \text{Hour}_i\, x_i \le \text{AvailableHours} + \text{UpgradeHours}\, y,\\[1mm]
\text{(Non-trivial production constraints):} \quad & x_i \ge 1,\quad \forall\, i=1,\dots,P,\\[1mm]
\text{(Variable domains):} \quad & x_i \in \mathbb{Z}_+, \quad \forall\, i=1,\dots,P, \quad y \in \{0,1\}.
\end{align*}

\noindent
\textbf{Explanation:}

1. The decision variable $x_i$ represents the production quantity for product $i$. The constraint $x_i \ge 1$ (instead of allowing zero production) is included to ensure a non‐trivial product mix, so that the solution does not consist of producing only one product. 

2. The binary variable $y$ indicates whether the company invests in upgrading the machine capacity. If $y=1$, the available machine hours are increased by $\text{UpgradeHours}$, and the cash cost $\text{UpgradeCost}$ is incurred.

3. The cash constraint ensures that the sum of the production expenditures plus any upgrade cost does not exceed the sum of the initial cash and the portion of the sales revenues that is available for financing operations. 

4. The machine capacity constraint guarantees that the total hours used in production do not exceed the available hours (which can be increased by the upgrade).

This complete model faithfully translates the problem description into a formal mixed‐integer programming formulation.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Instantiate a mixed integer solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return

    # --- Problem Data ---
    P = 2
    Cash = 3000
    Hour = [2, 6]  # machine hours per unit for each product
    Cost = [3, 2]  # production cost per unit for each product
    Price = [6, 5]  # selling price per unit for each product
    InvestPercentage = [0.4, 0.3]  # invested percentage per product
    UpgradeHours = 2000  # additional machine hours if upgrade is performed
    UpgradeCost = 400  # cash cost to perform the upgrade
    AvailableHours = 2000  # base machine hours available

    # --- Decision Variables ---
    # x[i]: number of units produced for product i (integer, >= 1)
    x = [solver.IntVar(1, solver.infinity(), f'x_{i}') for i in range(P)]
    # y: binary variable for machinery upgrade (0 or 1)
    y = solver.IntVar(0, 1, 'y')

    # --- Constraints ---

    # Cash Constraint:
    # Sum(Cost[i]*x[i]) + UpgradeCost*y <= Cash + Sum(InvestPercentage[i]*Price[i]*x[i])
    # Rearranged: Sum((Cost[i] - InvestPercentage[i]*Price[i]) * x[i]) + UpgradeCost*y <= Cash
    cash_expr = solver.Sum([(Cost[i] - InvestPercentage[i] * Price[i]) * x[i] for i in range(P)]) + UpgradeCost * y
    solver.Add(cash_expr <= Cash)

    # Machine Capacity Constraint:
    # Sum(Hour[i]*x[i]) <= AvailableHours + UpgradeHours*y
    machine_expr = solver.Sum([Hour[i] * x[i] for i in range(P)])
    solver.Add(machine_expr <= AvailableHours + UpgradeHours * y)

    # --- Objective Function ---
    # Maximize Z = Sum(((1 - InvestPercentage[i])*Price[i] - Cost[i]) * x[i]) - UpgradeCost*y
    profit_expr = solver.Sum([((1 - InvestPercentage[i]) * Price[i] - Cost[i]) * x[i] for i in range(P)]) - UpgradeCost * y
    solver.Maximize(profit_expr)

    # --- Solve the Model ---
    status = solver.Solve()

    # Check the result status and print the solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Solution:")
        for i in range(P):
            print(f"  x[{i+1}] = {x[i].solution_value()}")
        print(f"  Upgrade (y) = {y.solution_value()}")
        print("Objective value =", solver.Objective().Value())
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()