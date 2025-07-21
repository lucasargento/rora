# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices:} & i = 1,\dots,10 & \quad & \text{(potential facilities)} \\
                 & j = 1,\dots,20 & \quad & \text{(customer zones)}
\end{array}
\]

\[
\begin{array}{rcll}
\textbf{Parameters:} & f_i \quad & \text{facility fixed cost for facility } i, & \quad i = 1,\dots,10, \\
                    & t_{ij} \quad & \text{transportation cost per unit from facility } i \text{ to customer } j, & \quad i=1,\dots,10,\; j=1,\dots,20, \\
                    & c_i \quad & \text{capacity of facility } i, & \quad i=1,\dots,10, \\
                    & d_j \quad & \text{demand of customer zone } j, & \quad j=1,\dots,20.
\end{array}
\]

\[
\begin{array}{rcll}
\textbf{Decision Variables:} & y_i \in \{0,1\} \quad & \text{= 1 if facility } i \text{ is established, } 0 \text{ otherwise,} & \quad i=1,\dots,10, \\
                             & x_{ij} \ge 0 \quad & \text{amount of goods shipped from facility } i \text{ to customer } j, & \quad i=1,\dots,10,\; j=1,\dots,20.
\end{array}
\]

\[
\begin{align*}
\textbf{Minimize} \quad & Z = \sum_{i=1}^{10} f_i\, y_i + \sum_{i=1}^{10}\sum_{j=1}^{20} t_{ij}\, x_{ij} \\
\\
\textbf{subject to:}& \\
\text{(1) Facility Capacity Constraints:} \quad & \sum_{j=1}^{20} x_{ij} \le c_i\, y_i, && \forall\, i=1,\dots,10, \\
\\
\text{(2) Customer Demand Satisfaction:} \quad & \sum_{i=1}^{10} x_{ij} \ge d_j, && \forall\, j=1,\dots,20, \\
\\
\text{(3) Nonnegativity and Binary:} \quad & x_{ij} \ge 0, && \forall\, i=1,\dots,10,\; j=1,\dots,20, \\
& y_i \in \{0,1\}, && \forall\, i=1,\dots,10.
\end{align*}
\]

\textbf{Explanation:}  
1. The binary variable \( y_i \) determines whether facility \( i \) is established.  
2. The continuous variable \( x_{ij} \) represents the quantity shipped from facility \( i \) to customer \( j \).  
3. The objective function minimizes the total cost, which is the sum of the fixed costs for opening facilities and the variable transportation costs incurred by shipping goods from facilities to customers.  
4. Constraint (1) ensures that if facility \( i \) is not open (\( y_i = 0 \)), no shipments can be made from it, and if it is open (\( y_i = 1 \)), the total shipment does not exceed its capacity \( c_i \).  
5. Constraint (2) guarantees that each customer's demand is met by the combined shipments from all facilities.  

This complete formulation accurately represents the capacitated facility location problem in transportation and logistics, ensuring feasibility and boundedness as required.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    NumberOfFacilities = 10
    NumberOfCustomers = 20

    FacilityFixedCost = [8517, 5068, 9433, 6127, 6033, 5966, 7762, 9406, 6602, 7040]
    FacilityCapacity = [301, 291, 453, 472, 492, 375, 493, 297, 331, 246]
    CustomerDemand = [117, 86, 69, 53, 110, 74, 136, 140, 126, 79, 54, 86, 114, 76, 136, 73, 144, 51, 53, 120]

    # Transportation cost matrix as a list of lists (10 x 20)
    FacilityToCustomerTransportCost = [
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

    # Create solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not found.")
        return

    # Decision variables:
    # y[i]: binary variable indicating if facility i is open
    y = {}
    for i in range(NumberOfFacilities):
        y[i] = solver.IntVar(0, 1, f'y_{i}')

    # x[i][j]: continuous variable for amount shipped from facility i to customer j
    x = {}
    for i in range(NumberOfFacilities):
        x[i] = {}
        for j in range(NumberOfCustomers):
            # Lower bound 0, no explicit upper bound needed (capacity constraints will limit)
            x[i][j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')

    # Constraints:
    # 1. Facility Capacity Constraints: sum_j x[i][j] <= FacilityCapacity[i] * y[i]
    for i in range(NumberOfFacilities):
        constraint_expr = solver.Sum([x[i][j] for j in range(NumberOfCustomers)])
        solver.Add(constraint_expr <= FacilityCapacity[i] * y[i])

    # 2. Customer Demand Satisfaction: sum_i x[i][j] >= CustomerDemand[j]
    for j in range(NumberOfCustomers):
        constraint_expr = solver.Sum([x[i][j] for i in range(NumberOfFacilities)])
        solver.Add(constraint_expr >= CustomerDemand[j])

    # Objective: Minimize fixed costs + transportation costs
    fixed_costs = solver.Sum([FacilityFixedCost[i] * y[i] for i in range(NumberOfFacilities)])
    transport_costs = solver.Sum([FacilityToCustomerTransportCost[i][j] * x[i][j]
                                  for i in range(NumberOfFacilities)
                                  for j in range(NumberOfCustomers)])
    solver.Minimize(fixed_costs + transport_costs)

    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal objective value =', solver.Objective().Value())
        for i in range(NumberOfFacilities):
            if y[i].solution_value() > 0.5:
                print(f'Facility {i} is open with capacity usage {sum(x[i][j].solution_value() for j in range(NumberOfCustomers)):.2f}')
                for j in range(NumberOfCustomers):
                    shipped = x[i][j].solution_value()
                    if shipped > 1e-6:
                        print(f'  Ship {shipped:.2f} units to Customer {j}')
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()