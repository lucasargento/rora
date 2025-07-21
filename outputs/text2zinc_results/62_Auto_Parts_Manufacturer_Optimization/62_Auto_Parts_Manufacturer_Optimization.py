# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices:} & m & \in \{1,2,\ldots,M\} & \text{(machines)}\\[1mm]
                 & p & \in \{1,2,\ldots,P\} & \text{(parts)}
\end{array}
\]

\[
\begin{array}{rcll}
\textbf{Parameters:} & \\
& \text{TimeRequired}_{m,p} & \ge 0, & \text{hours required on machine } m \text{ to produce one batch of part } p,\\[1mm]
& \text{MachineCosts}_m & > 0, & \text{cost per operating hour on machine } m,\\[1mm]
& \text{Availability}_m & > 0, & \text{available hours of machine } m \text{ per month},\\[1mm]
& \text{Prices}_p & > 0, & \text{selling price per batch of part } p,\\[1mm]
& \text{MinBatches}_p & \ge 0, & \text{minimum batches required for part } p,\\[1mm]
& M & \text{(total number of machines)} & , \quad P \text{ (total number of parts).}
\end{array}
\]

\[
\begin{array}{rcll}
\textbf{Decision Variables:} & \\
& x_p \in \mathbb{Z}_{+}, & \forall\, p \in \{1,\dots,P\}, & \text{number of batches of part } p \text{ to produce.}
\end{array}
\]

\[
\begin{align*}
\textbf{Maximize:} \quad Z &= \sum_{p=1}^{P} \text{Prices}_p\, x_p \;-\; \sum_{m=1}^{M} \text{MachineCosts}_m \left( \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p \right) \\[2mm]
\textbf{subject to:} \quad & \\
\text{(Machine Capacity Constraints)} \quad & \sum_{p=1}^{P} \text{TimeRequired}_{m,p}\, x_p \; \le \; \text{Availability}_m, \quad \forall\, m = 1,\dots,M, \\[2mm]
\text{(Minimum Production Constraints)} \quad & x_p \; \ge \; \text{MinBatches}_p, \quad \forall\, p = 1,\dots,P, \\[2mm]
\text{(Nontrivial Production Mix)} \quad & \text{For each } p, \;x_p > 0, \quad \text{(in addition to the minimum)} \\[2mm]
\textbf{and} \quad & x_p \in \mathbb{Z}_{+}, \quad \forall\, p=1,\dots,P.
\end{align*}
\]

\noindent In this formulation:  
- The decision variables xₚ represent the number of batches of part p to produce (where each batch consists of 100 parts).  
- The objective is to maximize profit, computed as total sales revenue minus the total machine operating costs.  
- The machine capacity constraints ensure that the cumulative processing time for all parts on each machine does not exceed its monthly available hours.  
- The minimum production constraints guarantee that the contractual minimum number of batches for each part is met.  
- The additional note on nontrivial production mix is included to avoid practical scenarios where only one product is produced.

This complete formulation captures the full manufacturing and production optimization problem without any simplifications.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the MILP solver using CBC.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    # Problem Data
    P = 4  # number of parts
    M = 3  # number of machines
    TimeRequired = [
        [2, 1, 3, 2],  # Machine 1: Time for parts 1..4
        [4, 2, 1, 2],  # Machine 2: Time for parts 1..4
        [6, 2, 1, 2]   # Machine 3: Time for parts 1..4
    ]
    MachineCosts = [160, 10, 15]      # Cost per operating hour for each machine
    Availability = [200, 300, 500]    # Available hours for each machine per month
    Prices = [570, 250, 585, 430]      # Selling price for one batch of each part
    MinBatches = [10, 10, 10, 10]      # Minimum batches required for each part

    # Decision Variables: x[p] = number of batches of part p to produce.
    x = []
    for p in range(P):
        # Lower bound set to MinBatches[p] to satisfy contract and nontrivial production mix.
        var = solver.IntVar(MinBatches[p], solver.infinity(), f'x[{p}]')
        x.append(var)

    # Machine capacity constraints: total processing time on each machine <= Availability.
    for m in range(M):
        constraint_expr = solver.Sum(TimeRequired[m][p] * x[p] for p in range(P))
        solver.Add(constraint_expr <= Availability[m])

    # Objective: Maximize profit.
    # Profit = Sum_p (Prices[p] * x[p]) - Sum_m MachineCosts[m] * (Sum_p TimeRequired[m][p] * x[p])
    # This is equivalent to: Sum_p (Prices[p] - Sum_m MachineCosts[m]*TimeRequired[m][p]) * x[p]
    objective = solver.Objective()
    for p in range(P):
        net_profit_coefficient = Prices[p] - sum(MachineCosts[m] * TimeRequired[m][p] for m in range(M))
        objective.SetCoefficient(x[p], net_profit_coefficient)
    objective.SetMaximization()

    # Solve the model.
    status = solver.Solve()

    # Check the result status.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f"Optimal objective value = {objective.Value()}")
        for p in range(P):
            print(f"x[{p}] (batches of part {p+1}) = {x[p].solution_value()}")
    else:
        print("No feasible solution found.")

if __name__ == "__main__":
    main()