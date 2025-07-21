# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices:} & & & \\
i &=& \text{Customers}, & i = 1,2,\dots,\text{num\_customers} \\
j &=& \text{Candidate Warehouses}, & j = 1,2,\dots,\text{num\_warehouses} \\[10pt]

\textbf{Parameters:} & & & \\
P &=& \text{Number of warehouses to open}, & P \in \mathbb{Z}^+ \\
D_i &=& \text{Demand of customer } i, & i = 1,2,\dots,\text{num\_customers} \\
c_{ij} &=& \text{Distance from customer } i \text{ to warehouse } j, & \forall \, i,j \\[10pt]

\textbf{Decision Variables:} & & & \\
y_j &\in& \{0,1\}, & \text{where } y_j = 
\begin{cases}
1, & \text{if warehouse } j \text{ is opened}, \\
0, & \text{otherwise},
\end{cases} \quad j = 1,2,\dots,\text{num\_warehouses} \\[8pt]
x_{ij} &\in& \{0,1\}, & \text{where } x_{ij} = 
\begin{cases}
1, & \text{if customer } i \text{ is assigned to warehouse } j, \\
0, & \text{otherwise},
\end{cases} \quad \forall \, i,j \\[10pt]

\textbf{Objective Function:} & & & \\
\min \quad Z &=& \displaystyle \sum_{i=1}^{\text{num\_customers}} \sum_{j=1}^{\text{num\_warehouses}} D_i \, c_{ij} \, x_{ij} \\[10pt]

\textbf{Constraints:} & & & \\
\text{(1)} \quad \sum_{j=1}^{\text{num\_warehouses}} x_{ij} &=& 1, & \forall \, i = 1,2,\dots,\text{num\_customers} \quad \text{(Each customer is assigned to exactly one warehouse)} \\[8pt]
\text{(2)} \quad x_{ij} &\leq& y_j, & \forall \, i = 1,2,\dots,\text{num\_customers}, \; j = 1,2,\dots,\text{num\_warehouses} \quad \text{(A customer may only be assigned to an open warehouse)} \\[8pt]
\text{(3)} \quad \sum_{j=1}^{\text{num\_warehouses}} y_j &=& P, & \quad \text{(Exactly } P \text{ warehouses are opened)} \\[8pt]
\textbf{Variable Domains:} & & & \\
x_{ij} &\in& \{0,1\}, & \forall \, i,j \\
y_j &\in& \{0,1\}, & \forall \, j 
\end{array}
\]

This formulation fully captures the P-Median problem for the given transportation and logistics scenario.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    P = 2
    num_customers = 4
    num_warehouses = 3
    Demand = [100.0, 80.0, 80.0, 70.0]
    Distance = [
        [2.0, 10.0, 50.0],
        [2.0, 10.0, 52.0],
        [50.0, 60.0, 3.0],
        [40.0, 60.0, 1.0]
    ]

    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    # Decision Variables
    # y[j] = 1 if warehouse j is open, 0 otherwise.
    y = {}
    for j in range(num_warehouses):
        y[j] = solver.IntVar(0, 1, f'y[{j}]')

    # x[i][j] = 1 if customer i is assigned to warehouse j, 0 otherwise.
    x = {}
    for i in range(num_customers):
        for j in range(num_warehouses):
            x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

    # Constraints

    # Each customer is assigned to exactly one warehouse.
    for i in range(num_customers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_warehouses)]) == 1)

    # A customer may only be assigned to an open warehouse.
    for i in range(num_customers):
        for j in range(num_warehouses):
            solver.Add(x[i, j] <= y[j])

    # Exactly P warehouses are opened.
    solver.Add(solver.Sum([y[j] for j in range(num_warehouses)]) == P)

    # Objective: Minimize the demand-weighted distance.
    objective_terms = []
    for i in range(num_customers):
        for j in range(num_warehouses):
            objective_terms.append(Demand[i] * Distance[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve the model.
    status = solver.Solve()

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal Solution Found:")
        print("Objective value (total demand-weighted distance):", solver.Objective().Value())
        print("\nWarehouse decisions:")
        for j in range(num_warehouses):
            if y[j].solution_value() > 0.5:
                print(f"  Warehouse {j} is open")
            else:
                print(f"  Warehouse {j} is closed")
        print("\nCustomer assignments:")
        for i in range(num_customers):
            for j in range(num_warehouses):
                if x[i, j].solution_value() > 0.5:
                    print(f"  Customer {i} is assigned to Warehouse {j}")
    else:
        print("No optimal solution found.")

if __name__ == '__main__':
    main()