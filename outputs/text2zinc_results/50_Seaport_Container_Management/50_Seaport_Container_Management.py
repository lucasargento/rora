# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & t = 1,\dots,T \\[1mm]
\textbf{Parameters:} \quad & T \quad \text{(number of months)}\\[0.5mm]
& D_t \quad \text{demand (number of containers) in month } t,\quad t=1,\dots,T\\[0.5mm]
& c^{\text{unload}}_t \quad \text{cost to unload one container in month } t,\quad t=1,\dots,T\\[0.5mm]
& U_t \quad \text{maximum containers that can be unloaded in month } t,\quad t=1,\dots,T\\[0.5mm]
& h \quad \text{holding cost per container carried to the next month}\\[0.5mm]
& M \quad \text{maximum number of containers that can be held in the yard}\\[0.5mm]
& I_0 \quad \text{initial number of containers available at the beginning of month 1}\\[0.5mm]
& N \quad \text{maximum number of cranes available (and therefore can be rented)}\\[0.5mm]
& Q \quad \text{capacity (in containers) of each crane}\\[0.5mm]
& c^{\text{crane}} \quad \text{rental cost per crane per month}
\\[3mm]
\textbf{Decision Variables:} \quad & \\
x_t &\ge 0,\quad \text{integer, number of containers unloaded in month } t,\quad t=1,\dots,T,\\[0.5mm]
y_t &\ge 0,\quad \text{integer, number of containers in inventory (yard) at end of month } t,\quad t=1,\dots,T,\\[0.5mm]
w_t &\ge 0,\quad \text{integer, number of cranes rented in month } t,\quad t=1,\dots,T.
\\[3mm]
\textbf{Objective Function:} \quad & \text{Minimize total cost over the planning horizon} \\
\min \quad & \sum_{t=1}^{T} \left( c^{\text{unload}}_t x_t + c^{\text{crane}} w_t \right) + \sum_{t=1}^{T-1} h\, y_t 
\\[3mm]
\textbf{Constraints:} \\[1mm]
\textbf{(a) Inventory Balance:} \quad & \\
\text{For } t = 1: \quad & I_0 + x_1 = D_1 + y_1, \\
\text{For } t = 2,\dots,T: \quad & y_{t-1} + x_t = D_t + y_t, \\
\text{Terminal condition:} \quad & y_T = 0. \\[1mm]
\textbf{(b) Unloading Capacity:} \quad & \\
& x_t \le U_t, \quad \forall\, t=1,\dots,T. \\[1mm]
\textbf{(c) Yard Storage Capacity:} \quad & \\
& y_t \le M, \quad \forall\, t=1,\dots,T. \\[1mm]
\textbf{(d) Crane Loading Capacity:} \quad & \\
& w_t \, Q \ge D_t, \quad \forall\, t=1,\dots,T. \\[1mm]
\textbf{(e) Crane Availability:} \quad & \\
& w_t \le N, \quad \forall\, t=1,\dots,T. \\[1mm]
\textbf{(f) Integrality and Nonnegativity:} \quad & \\
& x_t \in \mathbb{Z}_{+},\quad y_t \in \mathbb{Z}_{+},\quad w_t \in \mathbb{Z}_{+}, \quad \forall\, t=1,\dots,T.
\end{align*}

\vspace{2mm}
This complete mathematical model faithfully represents the transportation and logistics problem described. The objective is to minimize total costs from unloading, inventory holding, and crane rentals while meeting the monthly shipping container demands subject to operational capacity constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    T = 4
    Demands = [450, 700, 500, 750]
    UnloadCosts = [75, 100, 105, 130]
    UnloadCapacity = [800, 500, 450, 700]
    HoldingCost = 20
    MaxContainer = 500
    InitContainer = 200
    NumCranes = 4
    CraneCapacity = 200
    CraneCost = 1000

    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables
    x = [solver.IntVar(0, UnloadCapacity[t], f'x_{t}') for t in range(T)]  # containers unloaded in month t
    y = [solver.IntVar(0, MaxContainer, f'y_{t}') for t in range(T)]         # containers stored at end of month t
    w = [solver.IntVar(0, NumCranes, f'w_{t}') for t in range(T)]             # cranes rented in month t

    # Constraints

    # (a) Inventory Balance
    # For t = 0: I0 + x_0 = D_0 + y_0
    solver.Add(InitContainer + x[0] == Demands[0] + y[0])
    # For t = 1 to T-1: y[t-1] + x[t] = D[t] + y[t]
    for t in range(1, T):
        solver.Add(y[t-1] + x[t] == Demands[t] + y[t])
    # Terminal condition: y[T-1] = 0
    solver.Add(y[T-1] == 0)
    
    # (b) Unloading capacity is already enforced in variable upper bounds (x[t] <= UnloadCapacity[t])
    
    # (c) Yard Storage Capacity is enforced in variable upper bounds (y[t] <= MaxContainer)
    
    # (d) Crane Loading Capacity: w[t] * CraneCapacity >= Demands[t]
    for t in range(T):
        solver.Add(w[t] * CraneCapacity >= Demands[t])
        
    # (e) Crane Availability is enforced by the upper bound (w[t] <= NumCranes)

    # Objective function: minimize total cost
    # Sum from t=0 to T-1: (UnloadCosts[t] * x[t] + CraneCost * w[t]) + holding cost for months 0 to T-2 (y[t])
    objective = solver.Objective()
    for t in range(T):
        objective.SetCoefficient(x[t], UnloadCosts[t])
        objective.SetCoefficient(w[t], CraneCost)
        if t < T - 1:
            objective.SetCoefficient(y[t], HoldingCost)
    objective.SetMinimization()

    # Solve model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal objective value =", objective.Value())
        for t in range(T):
            print(f"Month {t+1}:")
            print(f"  Containers unloaded (x_{t+1}) = {x[t].solution_value()}")
            print(f"  Containers stored at end (y_{t+1}) = {y[t].solution_value()}")
            print(f"  Cranes rented (w_{t+1}) = {w[t].solution_value()}")
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver ended with an unexpected status:", status)

if __name__ == '__main__':
    main()