# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:}\\
& i \in \{1, 2, \ldots, n_{stores}\} \quad \text{(stores)}\\
& j \in \{1, 2, \ldots, n_{suppliers}\} \quad \text{(candidate warehouse locations)}\\[1em]

\textbf{Decision Variables:}\\
& y_j = \begin{cases}
1, & \text{if warehouse } j \text{ is opened},\\[0.5em]
0, & \text{otherwise},
\end{cases} \quad \forall j=1,\dots,n_{suppliers}\\[0.5em]
& x_{ij} = \begin{cases}
1, & \text{if store } i \text{ is supplied by warehouse } j,\\[0.5em]
0, & \text{otherwise},
\end{cases} \quad \forall i=1,\dots,n_{stores}, \; \forall j=1,\dots,n_{suppliers}\\[1em]

\textbf{Parameters:}\\
& n_{suppliers} \quad \text{(number of candidate warehouses)},\\[0.5em]
& n_{stores} \quad \text{(number of stores)},\\[0.5em]
& \text{building\_cost} \quad \text{(fixed cost to open any warehouse)},\\[0.5em]
& \text{capacity}_j, \quad j=1,\ldots,n_{suppliers} \quad \text{(capacity of warehouse } j\text{)},\\[0.5em]
& c_{ij}, \quad \forall i=1,\dots, n_{stores}, \ \forall j=1,\dots, n_{suppliers} \quad \text{(supply cost for store } i \text{ from warehouse } j\text{)}.\\[1em]

\textbf{Objective Function:}\\[0.5em]
\text{Minimize} \quad & Z = \underbrace{\sum_{j=1}^{n_{suppliers}} \text{building\_cost} \cdot y_j}_{\text{Warehouse opening costs}} + \underbrace{\sum_{i=1}^{n_{stores}} \sum_{j=1}^{n_{suppliers}} c_{ij} \cdot x_{ij}}_{\text{Supply costs}}.\\[1em]

\textbf{Constraints:}\\[0.5em]
\text{(1) Each store must be assigned to exactly one warehouse:} \quad & \sum_{j=1}^{n_{suppliers}} x_{ij} = 1, \quad \forall i=1,\ldots, n_{stores}.\\[0.5em]
\text{(2) Warehouse capacity constraints:} \quad & \sum_{i=1}^{n_{stores}} x_{ij} \leq \text{capacity}_j \, y_j, \quad \forall j=1,\ldots, n_{suppliers}.\\[0.5em]
\text{(3) Binary constraints:} \quad & x_{ij} \in \{0,1\}, \quad \forall i=1,\dots,n_{stores}, \ \forall j=1,\dots, n_{suppliers},\\[0.5em]
& y_j \in \{0,1\}, \quad \forall j=1,\dots,n_{suppliers}.
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    n_suppliers = 5
    n_stores = 10
    building_cost = 30
    capacity = [1, 4, 2, 1, 3]
    cost_matrix = [
        [20, 24, 11, 25, 30],
        [28, 27, 82, 83, 74],
        [74, 97, 71, 96, 70],
        [2, 55, 73, 69, 61],
        [46, 96, 59, 83, 4],
        [42, 22, 29, 67, 59],
        [1, 5, 73, 59, 56],
        [10, 73, 13, 43, 96],
        [93, 35, 63, 85, 46],
        [47, 65, 55, 71, 95]
    ]
    
    # Create CP-SAT model
    model = cp_model.CpModel()

    # Decision Variables
    # x[i][j] = 1 if store i is supplied by warehouse j
    x = {}
    for i in range(n_stores):
        for j in range(n_suppliers):
            x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')
    
    # y[j] = 1 if warehouse j is opened
    y = {}
    for j in range(n_suppliers):
        y[j] = model.NewBoolVar(f'y_{j}')
    
    # Constraints
    # Constraint 1: Each store is assigned to exactly one warehouse.
    for i in range(n_stores):
        model.Add(sum(x[(i, j)] for j in range(n_suppliers)) == 1)
    
    # Constraint 2: Warehouse capacity constraints.
    for j in range(n_suppliers):
        model.Add(sum(x[(i, j)] for i in range(n_stores)) <= capacity[j] * y[j])
    
    # Objective: Minimize building cost of warehouses and supply cost for assignments.
    objective_terms = []
    for j in range(n_suppliers):
        objective_terms.append(building_cost * y[j])
    for i in range(n_stores):
        for j in range(n_suppliers):
            objective_terms.append(cost_matrix[i][j] * x[(i, j)])
    
    model.Minimize(sum(objective_terms))
    
    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        print("Optimal objective value =", solver.ObjectiveValue())
        print("Warehouse decisions (y[j]):")
        for j in range(n_suppliers):
            print(f" Warehouse {j}: Open = {solver.Value(y[j])}")
        print("\nStore assignments (x[i][j]):")
        for i in range(n_stores):
            for j in range(n_suppliers):
                if solver.Value(x[(i, j)]) == 1:
                    print(f" Store {i} is assigned to Warehouse {j} (Cost = {cost_matrix[i][j]})")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()