# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & l = 1,\dots,L \quad \text{(process index)}, \quad o = 1,\dots,O \quad \text{(crude oil type index)}, \quad p = 1,\dots,P \quad \text{(product/price index)}. \\[1mm]

\textbf{Given Data:} \quad & \text{Allocated resources: } A_o,\; o=1,\dots,O, \\
& \text{Selling prices: } r_p,\; p=1,\dots,P, \\
& \text{Input requirements: } a_{l,o},\; l=1,\dots,L,\; o=1,\dots,O, \\
& \text{Output amounts: } b_{l,p},\; l=1,\dots,L,\; p=1,\dots,P, \\
& \text{Process cost per barrel (of product produced): } c_l,\; l=1,\dots,L. \\[2mm]

\textbf{Decision Variables:} \quad & x_l \ge 0 \quad \text{for } l=1,\dots,L, \\
& \quad \text{where } x_l \text{ is the (possibly fractional) number of times process } l \text{ is executed.} \\[2mm]

\textbf{Production Relationships:} \quad & \text{For each process } l \text{ and product } p, \text{ the production quantity is } \, y_{l,p} = b_{l,p}\, x_l. \\[2mm]

\textbf{Objective Function:} \quad & \text{Maximize net revenue, which is total sales revenue less the production cost incurred.} \\
\text{Maximize} \quad & Z = \sum_{l=1}^{L} \sum_{p=1}^{P} \Bigl( r_p\, b_{l,p} - c_l\, b_{l,p} \Bigr) \, x_l. \\[2mm]

\textbf{Constraints:} \\[2mm]
\text{(1) Resource (Crude Oil) Availability:} \quad & \sum_{l=1}^{L} a_{l,o}\, x_l \le A_o, \quad \forall \, o=1,\dots,O. \\[2mm]
\text{(2) Process Execution Nonnegativity:} \quad & x_l \ge 0, \quad \forall\, l=1,\dots,L.
\end{align*}

\vspace{2mm}
\textbf{Remarks:}
\begin{itemize}
    \item The term \( r_p\, b_{l,p} \) represents the revenue (price per barrel times barrels produced) for product \( p \) when process \( l \) is executed once.
    \item The cost incurred by process \( l \) is \( c_l \) per barrel produced, and since process \( l \) produces \( b_{l,p} \) barrels of product \( p \), the total cost for process \( l \) (if executed once) is \( c_l\, b_{l,p} \) for product \( p \) (and summed over all products produced in that process).
    \item There is no separate cost for the crude oil since it has already been allocated.
    \item The feasible region is defined by the resource (crude oil) constraints and the nonnegativity of the decision variables. This formulation is both feasible and bounded under the assumption that the allocated crude oil quantities \( A_o \) are finite and nonnegative.
    \item Although the model naturally may choose to execute only those processes that maximize net revenue, the decision-making structure (using multiple processes with varied input/output mixes) discourages a trivial product mix. If desired, additional constraints (e.g., minimum production requirements for each product) might be added to enforce diversification.
\end{itemize}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    O = 2     # number of crude oil types
    P = 2     # number of products/price points
    L = 3     # number of processes

    # Allocated crude oil resources for each type
    Allocated = [8000, 5000]

    # Selling prices for each product
    Price = [38, 33]

    # Input requirements: a matrix with dimensions L x O.
    # Each row l represents process l and columns represent crude oil type requirements.
    Input = [
        [3, 5],  # Process 1 requirements for crude oil types 1 and 2
        [1, 1],  # Process 2 requirements
        [5, 3]   # Process 3 requirements
    ]

    # Output produced: a matrix with dimensions L x P.
    # Each row l represents process l and columns represent barrels produced for product p.
    Output = [
        [4, 3],  # Process 1 yields for product 1 and 2
        [1, 1],  # Process 2 yields
        [3, 4]   # Process 3 yields
    ]

    # Process cost per barrel of product produced for each process
    Cost = [51, 11, 40]

    # Create the linear solver with the GLOP backend for linear programming.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Define decision variables: x[l] is the number of times process l is executed.
    x = [solver.NumVar(0, solver.infinity(), f'x_{l}') for l in range(L)]

    # Calculate net revenue coefficients for each process.
    # For each process l, net revenue = sum_p (Price[p]*Output[l][p] - Cost[l]*Output[l][p])
    net_rev = []
    for l in range(L):
        revenue = sum(Price[p] * Output[l][p] for p in range(P))
        cost_total = sum(Cost[l] * Output[l][p] for p in range(P))
        net_rev.append(revenue - cost_total)

    # Set objective: maximize total net revenue.
    objective = solver.Objective()
    for l in range(L):
        objective.SetCoefficient(x[l], net_rev[l])
    objective.SetMaximization()

    # Add resource (crude oil) constraints:
    # For each crude oil type o: sum_l (Input[l][o] * x[l]) <= Allocated[o]
    for o in range(O):
        ct = solver.Constraint(-solver.infinity(), Allocated[o])
        for l in range(L):
            ct.SetCoefficient(x[l], Input[l][o])

    # Solve the problem.
    status = solver.Solve()

    # Check the result.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for l in range(L):
            print(f"Process {l+1} executions: {x[l].solution_value()}")
        print(f"Optimal net revenue: {solver.Objective().Value()}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
        for l in range(L):
            print(f"Process {l+1} executions: {x[l].solution_value()}")
        print(f"Net revenue: {solver.Objective().Value()}")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()