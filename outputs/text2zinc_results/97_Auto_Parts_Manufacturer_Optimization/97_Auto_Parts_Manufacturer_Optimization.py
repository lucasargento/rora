# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & p \in \{1,\dots,P\} &&\text{(parts)}\\[1mm]
& m \in \{1,\dots,M\} &&\text{(machines)}\\[1mm]
\textbf{Parameters:} \quad & \text{TimeRequired}_{mp}: \text{ time in hours to produce one batch of part } p \text{ on machine } m,\\[1mm]
& \text{MachineCosts}_m: \text{ cost per hour to operate machine } m,\\[1mm]
& \text{Availability}_m: \text{ hours available on machine } m \text{ per month},\\[1mm]
& \text{Prices}_p: \text{ selling price for one batch (100 parts) of part } p,\\[1mm]
& \text{MinBatches}_p: \text{ minimum number of batches required for part } p.\\[2mm]

\textbf{Decision Variables:} \quad & x_p \in \mathbb{Z}_{\ge 0} \quad \text{for } p=1,\dots,P, \quad\text{with} \quad x_p \ge \text{MinBatches}_p.
\end{align*}

\noindent The variable \(x_p\) represents the number of batches of part \(p\) to produce each month.

\vspace{2mm}

\textbf{Objective Function:}

We wish to maximize profit, defined as total revenue minus total operating costs. The revenue obtained by producing \(x_p\) batches of part \(p\) is \(\text{Prices}_p \, x_p\). The operating cost incurred on machine \(m\) when producing part \(p\) is \(\text{MachineCosts}_m \, \text{TimeRequired}_{mp} \, x_p\). Even though machines \(M-1\) and \(M\) share availability, their operating costs are still incurred based on the time used. Therefore, the total profit is given by

\begin{align*}
\text{Maximize} \quad Z = \sum_{p=1}^{P} \, \text{Prices}_p \, x_p \; - \; \left[ \sum_{p=1}^{P} \sum_{m=1}^{M} \text{MachineCosts}_m \, \text{TimeRequired}_{mp} \, x_p \right].
\end{align*}

\vspace{2mm}

\textbf{Constraints:}

Since machine \(M-1\) and machine \(M\) share available hours, their individual capacity constraints are replaced by a combined constraint. The remaining machines (if any) have separate availability constraints.

\smallskip
\textbf{(a) Capacity constraints for machines without sharing:} \\
For all machines \(m = 1,\,2,\,\dots,\,M-2\) (if \(M \ge 3\)):
\begin{align*}
\sum_{p=1}^{P} \text{TimeRequired}_{mp} \, x_p \le \text{Availability}_m.
\end{align*}

\smallskip
\textbf{(b) Combined capacity constraint for machines \(M-1\) and \(M\):} \\
\begin{align*}
\sum_{p=1}^{P} \Bigl( \text{TimeRequired}_{(M-1),p} + \text{TimeRequired}_{M,p} \Bigr) \, x_p \le \text{Availability}_{M-1} + \text{Availability}_{M}.
\end{align*}

\smallskip
\textbf{(c) Minimum production requirements:} \\
For every part \(p=1,\dots,P\):
\begin{align*}
x_p \ge \text{MinBatches}_p.
\end{align*}

\smallskip
\textbf{(d) Integrality:} \\
For every part \(p=1,\dots,P\):
\begin{align*}
x_p \in \mathbb{Z}.
\end{align*}

\vspace{2mm}

\textbf{Complete Mathematical Formulation:}

\begin{align*}
\textbf{Decision Variables:} \quad & x_p \in \mathbb{Z}, \quad x_p \ge \text{MinBatches}_p, \quad \forall p=1,\dots,P. \\[1mm]
\textbf{Maximize:} \quad & Z = \sum_{p=1}^{P} \text{Prices}_p \, x_p - \sum_{p=1}^{P} \sum_{m=1}^{M} \text{MachineCosts}_m \, \text{TimeRequired}_{mp} \, x_p. \\[1mm]
\textbf{Subject to:} \quad & \sum_{p=1}^{P} \text{TimeRequired}_{mp} \, x_p \le \text{Availability}_m, \quad \forall m = 1,\dots,M-2, \\[1mm]
& \sum_{p=1}^{P} \Bigl( \text{TimeRequired}_{(M-1),p} + \text{TimeRequired}_{M,p} \Bigr)\,x_p \le \text{Availability}_{M-1} + \text{Availability}_M, \\[1mm]
& x_p \ge \text{MinBatches}_p, \quad \forall p=1,\dots,P, \\[1mm]
& x_p \in \mathbb{Z}, \quad \forall p=1,\dots,P.
\end{align*}

\vspace{2mm}

\textbf{Notes:}
1. The objective is a maximization of total profit (revenue minus operating costs).  
2. The capacity constraints ensure that the cumulative processing time on each machine does not exceed its monthly availability. In the case of machines \(M-1\) and \(M\), their processing times are aggregated and compared against the sum of their availabilities.  
3. The minimum production requirement \(x_p \ge \text{MinBatches}_p\) guarantees that each part is produced in sufficient quantities to satisfy the contractual obligations, thus preventing trivial scenarios where production is concentrated on only one part.  
4. The model is fully bounded and feasible provided that the aggregated machine availabilities and other parameter values are set consistently.  

This formulation thus accurately represents the given manufacturing and production optimization problem.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    M = 3  # Number of machines
    P = 4  # Number of parts

    # Time required for one batch of part p on machine m (indexed from 0)
    TimeRequired = [
        [2, 1, 3, 2],  # Machine 1
        [4, 2, 1, 2],  # Machine 2
        [6, 2, 1, 2]   # Machine 3
    ]
    
    # Machine operating costs (indexed from 0)
    MachineCosts = [160, 10, 15]

    # Machine availabilities per month (indexed from 0)
    Availability = [200, 300, 500]
    
    # Selling prices for each part (indexed from 0)
    Prices = [570, 250, 585, 430]
    
    # Minimum batches required for each part (indexed from 0)
    MinBatches = [10, 10, 10, 10]
    
    # Create the solver (CBC Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables: x[p] >= MinBatches[p] and integer
    x = []
    for p in range(P):
        var = solver.IntVar(MinBatches[p], solver.infinity(), f'x_{p}')
        x.append(var)
    
    # Constraint (a): For machines 1 to M-2 (if any)
    # Here M >= 3, so we add constraint for machine 0 only
    for m in range(M - 2):
        constraint_expr = solver.Sum(TimeRequired[m][p] * x[p] for p in range(P))
        solver.Add(constraint_expr <= Availability[m])
    
    # Constraint (b): Combined capacity for machines M-1 and M (machines indexed M-2 and M-1)
    combined_time = solver.Sum((TimeRequired[M-2][p] + TimeRequired[M-1][p]) * x[p] for p in range(P))
    combined_availability = Availability[M-2] + Availability[M-1]
    solver.Add(combined_time <= combined_availability)
    
    # Objective: Maximize profit = Revenue - Operating costs
    revenue = solver.Sum(Prices[p] * x[p] for p in range(P))
    operating_cost = solver.Sum(
        solver.Sum(MachineCosts[m] * TimeRequired[m][p] * x[p] for m in range(M))
        for p in range(P)
    )
    solver.Maximize(revenue - operating_cost)
    
    # Solve the model
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for p in range(P):
            print(f"Number of batches for part {p+1}: {int(x[p].solution_value())}")
        objective_value = solver.Objective().Value()
        print(f"Optimal profit: {objective_value}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
        for p in range(P):
            print(f"Number of batches for part {p+1}: {int(x[p].solution_value())}")
        objective_value = solver.Objective().Value()
        print(f"Profit: {objective_value}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()