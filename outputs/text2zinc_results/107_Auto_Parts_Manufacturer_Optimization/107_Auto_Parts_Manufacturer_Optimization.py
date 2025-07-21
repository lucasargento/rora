# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Decision Variables:}  \qquad & & & \\[1mm]
x_p & \in & \mathbb{Z}_{+} & \text{number of batches of part } p,\; p=1,\ldots,P, \text{ with } x_p \ge \text{MinBatches}_p, \\[1mm]
y_m & \in & \mathbb{R}_{+} & \text{extra machine-hours purchased for machine } m,\; m=1,\ldots,M,\; 0\le y_m\le \text{MaxExtra}_m. \\[3mm]
\textbf{Parameters:} \qquad & & & \\
\text{TimeRequired}_{m,p} &:& \text{hours required on machine } m \text{ to produce one batch of part } p, & m=1,\ldots,M,\; p=1,\ldots,P,\\[1mm]
\text{MachineCosts}_{m} &:& \text{cost per hour on machine } m \text{ for regular (available) time}, & m=1,\ldots,M,\\[1mm]
\text{Availability}_{m} &:& \text{available hours per month on machine } m, & m=1,\ldots,M,\\[1mm]
\text{ExtraCosts}_{m} &:& \text{cost per hour for extra (purchased) time on machine } m, & m=1,\ldots,M,\\[1mm]
\text{Prices}_{p} &:& \text{revenue per batch sold of part } p, & p=1,\ldots,P,\\[1mm]
\text{MinBatches}_{p} &:& \text{minimum number of batches required for part } p, & p=1,\ldots,P.\\[3mm]
\textbf{Auxiliary Definitions:} \qquad & & & \\
T_m &=& \displaystyle \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p, & \forall m=1,\ldots,M.
\end{array}
\]

We now write the full mathematical model.

\[
\begin{array}{rlcl}
\displaystyle \max_{x,y} & Z = \displaystyle \sum_{p=1}^{P} \text{Prices}_{p}\, x_p 
  - \sum_{m=1}^{M} \Bigl[ \text{MachineCosts}_{m} \Bigl( \displaystyle \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p - y_m \Bigr)
  + \text{ExtraCosts}_{m}\, y_m \Bigr] 
  & & \textbf{(Profit)} \\[2mm]
\text{subject to} \\[1mm]
& \displaystyle \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p \le \text{Availability}_{m} + y_m, 
  & \forall m=1,\ldots,M, & \textbf{(Machine time capacity)} \\[2mm]
& y_m \ge \displaystyle \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p - \text{Availability}_{m}, 
  & \forall m=1,\ldots,M, & \textbf{(Extra hours lower bound)} \\[2mm]
& 0 \le y_m \le \text{MaxExtra}_{m}, 
  & \forall m=1,\ldots,M, & \textbf{(Extra time purchase limits)} \\[2mm]
& x_p \ge \text{MinBatches}_{p}, 
  & \forall p=1,\ldots,P, & \textbf{(Contractual minimum production)} \\[2mm]
& x_p \in \mathbb{Z}_{+}, \quad y_m \in \mathbb{R}_{+}, 
  & \forall p=1,\ldots,P,\; \forall m=1,\ldots,M. & \textbf{(Integrality and nonnegativity)}
\end{array}
\]

\textbf{Explanation:}

1. The decision variable xₚ represents the number of batches (each of 100 parts) of part p produced per month. It must be at least the contractual minimum (MinBatchesₚ) and is integer-valued.  
2. The variable yₘ represents the extra machine-hours purchased for machine m beyond its regular monthly availability. It is bounded by the maximum hours that can be purchased (MaxExtraₘ).  
3. For each machine m, the total machine time required (∑ₚ TimeRequiredₘ,ₚ xₚ) can be satisfied using the available hours (Availabilityₘ) plus any extra hours purchased yₘ.  
4. To correctly account for costs, the cost on machine m is given by charging the regular rate (MachineCostsₘ) for the hours used within regular availability and the extra rate (ExtraCostsₘ) for any additional hours (captured by yₘ). This is modeled in the objective function by writing the cost as 
   MachineCostsₘ·(Tₘ – yₘ) + ExtraCostsₘ·yₘ, so that when extra time is needed (i.e. when Tₘ > Availabilityₘ, forcing yₘ = Tₘ – Availabilityₘ), the cost becomes MachineCostsₘ·Availabilityₘ + ExtraCostsₘ·(Tₘ – Availabilityₘ).  
5. The objective function maximizes profit, which is total revenue (from selling batches) minus the total operating costs (including the extra hours cost).

This complete formulation accurately and fully represents the manufacturing and production optimization problem described.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    M = 3
    P = 4
    # Time required on machine m for part p (m=0,...,2, p=0,...,3)
    TimeRequired = [
        [2, 1, 3, 2],   # Machine 1
        [4, 2, 1, 2],   # Machine 2
        [6, 2, 1, 2]    # Machine 3
    ]
    MachineCosts = [160, 10, 15]
    Availability = [200, 300, 500]
    Prices = [570, 250, 585, 430]
    MinBatches = [10, 10, 10, 10]
    ExtraCosts = [0, 15, 22.5]
    MaxExtra = [0, 80, 80]

    # Create solver using SCIP (or CBC if SCIP is unavailable)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return

    infinity = solver.infinity()

    # Decision Variables:
    # x[p]: number of batches of part p (integer, at least MinBatches[p])
    x = [solver.IntVar(MinBatches[p], infinity, f'x[{p}]') for p in range(P)]

    # y[m]: extra machine-hours purchased for machine m (continuous between 0 and MaxExtra[m])
    y = [solver.NumVar(0, MaxExtra[m], f'y[{m}]') for m in range(M)]

    # Constraints:
    # For each machine m:
    #   sum_{p} TimeRequired[m][p]*x[p] <= Availability[m] + y[m]
    #   y[m] >= sum_{p} TimeRequired[m][p]*x[p] - Availability[m]
    for m in range(M):
        # Calculate sum_{p} TimeRequired[m][p]*x[p]
        time_expr = solver.Sum([TimeRequired[m][p] * x[p] for p in range(P)])
        # Machine time capacity constraint
        solver.Add(time_expr <= Availability[m] + y[m])
        # Lower bound on extra time purchased if required
        solver.Add(y[m] >= time_expr - Availability[m])

    # Objective:
    # Maximize profit = sum_{p} Prices[p]*x[p] -
    #                  sum_{m} [ MachineCosts[m]*(sum_{p} TimeRequired[m][p]*x[p] - y[m]) + ExtraCosts[m]*y[m] ]
    revenue_expr = solver.Sum([Prices[p] * x[p] for p in range(P)])
    machine_cost_expr = 0
    for m in range(M):
        time_expr = solver.Sum([TimeRequired[m][p] * x[p] for p in range(P)])
        # Cost = MachineCosts[m]*(time_expr - y[m]) + ExtraCosts[m]*y[m]
        machine_cost_expr += MachineCosts[m] * (time_expr - y[m]) + ExtraCosts[m] * y[m]
    solver.Maximize(revenue_expr - machine_cost_expr)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Objective value (Profit): {solver.Objective().Value()}")
        for p in range(P):
            print(f"Number of batches for part {p+1}: {x[p].solution_value()}")
        for m in range(M):
            print(f"Extra machine-hours purchased for machine {m+1}: {y[m].solution_value()}")
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver did not find an optimal solution.")

if __name__ == '__main__':
    main()