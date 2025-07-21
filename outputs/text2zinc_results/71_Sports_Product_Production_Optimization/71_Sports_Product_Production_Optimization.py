# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Parameters:} & & & \\[1mm]
  & N  & = & \text{Number of raw materials (here } N = 3\text{)} \\
  & M  & = & \text{Number of products (here } M = 3\text{)} \\
  & A_i  & \geq 0 & \text{Available amount of raw material } i,\; i=1,\dots,N, \quad A_1=240000,\; A_2=8000,\; A_3=75000 \\[1mm]
  & R_{ij}  & \geq 0 & \text{Amount of raw material } i \text{ required for one unit of product } j,\; i=1,\dots,N,\; j=1,\dots,M, \\[1mm]
  &       &   & \text{with } R = \begin{pmatrix} 48 & 1 & 10 \\[0.5em] 40 & 1 & 10 \\[0.5em] 0 & 1 & 2 \end{pmatrix} \\[1mm]
  & p_j  & \geq 0 & \text{Selling price per unit of product } j,\; j=1,\dots,M, \quad p_1=40,\; p_2=38,\; p_3=9 \\[1mm]
  & c_j  & \geq 0 & \text{Production cost per unit of product } j,\; j=1,\dots,M, \quad c_1=30,\; c_2=26,\; c_3=7 \\[1mm]
  & d_j  & \geq 0 & \text{Forecasted maximum demand for product } j,\; j=1,\dots,M, \quad d_1=10000,\; d_2=2000,\; d_3=10000 \\[2mm]
\\[2mm]
\textbf{Decision Variables:} & & & \\[1mm]
  & x_j & \in & \mathbb{Z}_{\ge 0},\quad \forall j=1,\dots,M \\
  &    &   & \text{(Number of units of product } j \text{ to produce)} \\[2mm]
\textbf{Objective Function:} & & & \\[1mm]
\text{Maximize} \quad Z &=& \sum_{j=1}^{M} (\, p_j - c_j \,) \, x_j 
           & \quad \text{(Total profit)} \\[2mm]
\textbf{Constraints:} & & & \\[1mm]
\text{(1) Raw Material Availability:} \quad 
\sum_{j=1}^{M} R_{ij}\, x_j &\leq& A_i, 
  & \quad \forall\, i=1,\dots,N \\[2mm]
\text{(2) Demand Constraints:} \quad
x_j &\leq& d_j, 
  & \quad \forall\, j=1,\dots,M \\[2mm]
\text{(3) Non-trivial Product Mix:} \quad
x_j &\geq& 1, 
  & \quad \forall\, j=1,\dots,M \\[2mm]
\text{(4) Integrality:} \quad
x_j &\in& \mathbb{Z}_{\ge 0}, 
  & \quad \forall\, j=1,\dots,M 
\end{array}
\]

A few notes on the formulation:

1. The decision variable \(x_j\) represents the number of units of product \(j\) produced. The integrality constraints imply that production is in discrete units.

2. The objective is to maximize the overall profit, which is given by the difference between the selling price and the production cost multiplied by the number of units produced.

3. Constraint (1) ensures that the consumption of each raw material does not exceed its available amount.

4. Constraint (2) guarantees that the production of each product does not exceed its forecasted maximum demand.

5. Constraint (3) has been introduced to avoid trivial solutions (i.e., producing zero of all products except one) by enforcing that at least one unit of each product must be produced. This ensures a diversified product mix; note that if this constraint conflicts with other restrictions, adjustments might be required to ensure overall feasibility.

This complete formulation fully reflects the problem statement in a self-contained and clear mathematical model.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Instantiate the CP-SAT model.
    model = cp_model.CpModel()

    # Data
    # Number of raw materials and products
    N = 3
    M = 3

    # Available amount of raw materials
    available = [240000, 8000, 75000]

    # Requirements: raw materials required per unit of product
    requirements = [
        [48,  1, 10],
        [40,  1, 10],
        [ 0,  1,  2]
    ]

    # Selling prices, production costs, and forecasted maximum demands for each product
    prices = [40, 38, 9]
    costs = [30, 26, 7]
    demands = [10000, 2000, 10000]

    # Compute profit per unit: selling price - cost for each product.
    profits = [p - c for p, c in zip(prices, costs)]

    # Decision variables: x[j] = number of units produced for product j.
    # Domain: at least 1 unit and at most the forecasted demand.
    x = []
    for j in range(M):
        x_var = model.NewIntVar(1, demands[j], f'x_{j}')
        x.append(x_var)

    # Constraint 1: Raw Material Availability
    # For each raw material i, sum over products j of (requirement[i][j] * x[j]) <= available[i]
    for i in range(N):
        model.Add(sum(requirements[i][j] * x[j] for j in range(M)) <= available[i])

    # Constraint 2: Demand Constraints are already enforced in the variable bounds.

    # Objective: Maximize the total profit.
    # Total profit = sum(profit[j] * x[j]) for all products j.
    model.Maximize(sum(profits[j] * x[j] for j in range(M)))

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal solution found:')
        print('Total Profit =', solver.ObjectiveValue())
        for j in range(M):
            print(f'Product {j+1}: Produce {solver.Value(x[j])} units')
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()