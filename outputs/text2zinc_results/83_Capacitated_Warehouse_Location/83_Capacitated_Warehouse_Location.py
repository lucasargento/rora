# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\\[1mm]
& i \in I = \{1, 2, \dots, 10\} \quad \text{(potential warehouse locations)},\\[1mm]
& j \in J = \{1, 2, \dots, 20\} \quad \text{(customers)}.\\[2mm]
\textbf{Parameters:}\\[1mm]
& d_j \quad \text{Demand of customer } j,\quad \forall j \in J,\\[1mm]
& c_{ij} \quad \text{Service allocation cost of serving customer } j \text{ from warehouse } i,\quad \forall i \in I,\; \forall j \in J,\\[1mm]
& C_i \quad \text{Capacity of warehouse } i,\quad \forall i \in I,\\[1mm]
& L_i \quad \text{Minimum demand to be served by warehouse } i \text{ if opened},\quad \forall i \in I,\\[1mm]
& f_i \quad \text{Fixed operating cost of warehouse } i,\quad \forall i \in I,\\[1mm]
& k_{\min} \quad \text{Minimum number of warehouses to be operational (opened)},\\[1mm]
& k_{\max} \quad \text{Maximum number of warehouses to be operational (opened)}.\\[2mm]
\textbf{Decision Variables:}\\[1mm]
& x_{ij} \ge 0 \quad \text{Amount of customer } j \text{'s demand satisfied by warehouse } i,\quad \forall i \in I,\; \forall j \in J,\\[1mm]
& y_i \in \{0,1\} \quad \text{Binary variable that equals } 1 \text{ if warehouse } i \text{ is opened, } 0 \text{ otherwise},\quad \forall i \in I.\\[2mm]
\textbf{Mathematical Model:}\\[1mm]
\min \quad & \sum_{i \in I} \sum_{j \in J} c_{ij}\, x_{ij} \;+\; \sum_{i \in I} f_i\, y_i \\[1mm]
\text{s.t.} \quad 
& \sum_{i \in I} x_{ij} = d_j, \quad \forall j \in J, \quad \text{(Each customer's demand must be fully met)} \\[1mm]
& \sum_{j \in J} x_{ij} \le C_i\, y_i, \quad \forall i \in I, \quad \text{(Flow from a warehouse does not exceed its capacity, and is zero if closed)} \\[1mm]
& \sum_{j \in J} x_{ij} \ge L_i\, y_i, \quad \forall i \in I, \quad \text{(If warehouse } i \text{ is opened, it must serve at least } L_i \text{ demand)} \\[1mm]
& \sum_{i \in I} y_i \ge k_{\min}, \quad \text{(At least } k_{\min} \text{ warehouses must be open)} \\[1mm]
& \sum_{i \in I} y_i \le k_{\max}, \quad \text{(At most } k_{\max} \text{ warehouses can be open)} \\[1mm]
& x_{ij} \ge 0, \quad \forall i \in I,\; \forall j \in J, \\[1mm]
& y_i \in \{0,1\}, \quad \forall i \in I.
\end{align*}  

In this formulation, the objective function minimizes the sum of the service allocation costs and the fixed operating costs for the warehouses that are opened. The constraints ensure that every customer's demand is met exactly, that each warehouse does not exceed its capacity (and if it is not opened, no flow is allowed), and that open warehouses serve at least a minimum amount of demand. Additionally, limits are imposed on the total number of warehouses that can be operational. This complete model accurately represents the described Transportation and Logistics problem.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    NumberOfLocations = 10
    NumberOfCustomers = 20
    CustomerDemand = [117, 86, 69, 53, 110, 74, 136, 140, 126, 79, 54, 86, 114, 76, 136, 73, 144, 51, 53, 120]
    ServiceAllocationCost = [
        [80, 94, 44, 51, 190, 44, 129, 178, 129, 91, 172, 119, 177, 150, 90, 51, 53, 97, 184, 87],
        [139, 33, 104, 135, 50, 176, 97, 121, 47, 29, 186, 163, 149, 108, 156, 169, 100, 160, 153, 85],
        [153, 36, 18, 170, 18, 181, 178, 68, 171, 106, 159, 110, 21, 106, 91, 29, 144, 140, 155, 116],
        [103, 59, 78, 125, 14, 11, 152, 95, 76, 173, 36, 148, 75, 132, 59, 153, 113, 74, 185, 71],
        [193, 186, 130, 145, 114, 150, 33, 154, 20, 75, 103, 30, 137, 131, 167, 32, 53, 150, 176, 166],
        [159, 130, 156, 65, 36, 59, 199, 124, 104, 72, 180, 73, 43, 152, 143, 90, 161, 65, 172, 141],
        [173, 121, 110, 127, 22, 159, 195, 137, 47, 10, 87, 11, 154, 66, 126, 60, 152, 54, 20, 25],
        [181, 34, 186, 152, 109, 195, 133, 198, 30, 65, 69, 19, 109, 143, 108, 196, 59, 133, 10, 123],
        [82, 113, 147, 21, 88, 24, 38, 16, 70, 122, 148, 192, 116, 108, 18, 20, 143, 18, 116, 142],
        [176, 170, 87, 91, 195, 183, 124, 89, 72, 97, 89, 23, 45, 196, 97, 27, 83, 81, 171, 148]
    ]
    WarehouseCapacity = [3010, 2910, 4530, 4720, 4920, 3750, 4930, 2970, 3310, 2460]
    MinimumDemandFromWarehouse = [64, 55, 27, 71, 93, 90, 89, 87, 43, 50]
    MinimumOpenWarehouses = 3
    MaximumOpenWarehouses = 8
    WarehouseFixedCost = [8517, 5068, 9433, 6127, 6033, 5966, 7762, 9406, 6602, 7040]
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables
    x = {}
    for i in range(NumberOfLocations):
        for j in range(NumberOfCustomers):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')
    y = {}
    for i in range(NumberOfLocations):
        y[i] = solver.IntVar(0, 1, f'y_{i}')

    # Constraints

    # Each customer's demand must be met exactly by all warehouses.
    for j in range(NumberOfCustomers):
        solver.Add(solver.Sum([x[i, j] for i in range(NumberOfLocations)]) == CustomerDemand[j])
    
    # Warehouse capacity and minimum demand constraints.
    for i in range(NumberOfLocations):
        # Capacity constraint: total allocation does not exceed capacity if open, else must be 0.
        solver.Add(solver.Sum([x[i, j] for j in range(NumberOfCustomers)]) <= WarehouseCapacity[i] * y[i])
        # Minimum demand served if warehouse is open.
        solver.Add(solver.Sum([x[i, j] for j in range(NumberOfCustomers)]) >= MinimumDemandFromWarehouse[i] * y[i])
        
    # At least minimum open warehouses
    solver.Add(solver.Sum([y[i] for i in range(NumberOfLocations)]) >= MinimumOpenWarehouses)
    # At most maximum open warehouses
    solver.Add(solver.Sum([y[i] for i in range(NumberOfLocations)]) <= MaximumOpenWarehouses)
    
    # Objective: minimize service allocation cost + fixed cost for opening a warehouse.
    objective = solver.Sum([ServiceAllocationCost[i][j] * x[i, j] for i in range(NumberOfLocations) for j in range(NumberOfCustomers)]) + \
                solver.Sum([WarehouseFixedCost[i] * y[i] for i in range(NumberOfLocations)])
    solver.Minimize(objective)
    
    # Solve the model
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Solution:")
        print("Total cost =", solver.Objective().Value())
        for i in range(NumberOfLocations):
            if y[i].solution_value() > 0.5:
                print(f"Warehouse {i} is open; served demand =", sum(x[i, j].solution_value() for j in range(NumberOfCustomers)))
                for j in range(NumberOfCustomers):
                    if x[i, j].solution_value() > 1e-6:
                        print(f"  Customer {j} demand served: {x[i, j].solution_value()}")
    else:
        print("The problem does not have a feasible solution.")

if __name__ == '__main__':
    main()