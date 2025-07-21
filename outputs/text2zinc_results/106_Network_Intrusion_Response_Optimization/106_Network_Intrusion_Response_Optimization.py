# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in \{1,2,\ldots,N\} \quad \text{(each cluster or intervention)} \\[1mm]
\textbf{Parameters:} \quad &
\begin{array}{ll}
N: & \text{Total number of interventions (clusters)};\\[1mm]
ISc_i: & \text{Processing time for isolating at the central system for intervention } i,\\[1mm]
SSc_i: & \text{Processing time for scanning at the central system for intervention } i,\\[1mm]
IDist_i: & \text{Processing time for isolating at the distributed system for intervention } i,\\[1mm]
SDist_i: & \text{Processing time for scanning at the distributed system for intervention } i,\\[1mm]
C_{cost}: & \text{Opportunity cost for a central system intervention},\\[1mm]
D_{cost}: & \text{Opportunity cost for a distributed system intervention},\\[1mm]
C_{max}: & \text{Maximum total hours available for central processing},\\[1mm]
D_{max}: & \text{Maximum total hours available for distributed processing}.
\end{array}\\[2mm]
\textbf{Decision Variables:} \quad & \\
& y_{i}^{IC} = 
\begin{cases}
1, & \text{if intervention } i \text{ is performed as isolation using the central system},\\[1mm]
0, & \text{otherwise},
\end{cases} \quad i=1,\ldots,N, \\[1mm]
& y_{i}^{SC} = 
\begin{cases}
1, & \text{if intervention } i \text{ is performed as a scan using the central system},\\[1mm]
0, & \text{otherwise},
\end{cases} \quad i=1,\ldots,N, \\[1mm]
& y_{i}^{ID} = 
\begin{cases}
1, & \text{if intervention } i \text{ is performed as isolation using the distributed system},\\[1mm]
0, & \text{otherwise},
\end{cases} \quad i=1,\ldots,N, \\[1mm]
& y_{i}^{SD} = 
\begin{cases}
1, & \text{if intervention } i \text{ is performed as a scan using the distributed system},\\[1mm]
0, & \text{otherwise},
\end{cases} \quad i=1,\ldots,N. \\[3mm]
\textbf{Objective Function:} \quad &
\text{Minimize the total cost} \\
\text{Minimize} \quad & Z = \sum_{i=1}^{N} \Bigl[ C_{cost}\,(y_{i}^{IC} + y_{i}^{SC}) + D_{cost}\,(y_{i}^{ID} + y_{i}^{SD}) \Bigr]. \\[3mm]
\textbf{Constraints:} \quad & \\[1mm]
\text{(1) One intervention per cluster:} \quad & 
y_{i}^{IC} + y_{i}^{SC} + y_{i}^{ID} + y_{i}^{SD} = 1, \quad \forall\, i=1,\ldots,N. \\[2mm]
\text{(2) Central processing time limit:} \quad &
\sum_{i=1}^{N} \Bigl[ ISc_i\, y_{i}^{IC} + SSc_i\, y_{i}^{SC} \Bigr] \leq C_{max}. \\[2mm]
\text{(3) Distributed processing time limit:} \quad &
\sum_{i=1}^{N} \Bigl[ IDist_i\, y_{i}^{ID} + SDist_i\, y_{i}^{SD} \Bigr] \leq D_{max}. \\[2mm]
\text{(4) Binary variable conditions:} \quad &
y_{i}^{IC},\; y_{i}^{SC},\; y_{i}^{ID},\; y_{i}^{SD} \in \{0,1\}, \quad \forall\, i=1,\ldots,N.
\end{align*}

\vspace{2mm}
\textbf{Notes:}  
\begin{itemize}
    \item The model selects for each cluster one of the four intervention methods: isolating or scanning by either the central or distributed system.
    \item The objective function minimizes the overall opportunity cost.
    \item Constraint (1) guarantees a consistent intervention decision per cluster.
    \item Constraints (2) and (3) ensure that processing time limitations for the central and distributed systems are not exceeded.
    \item The data provided (for example, for N $=$ 3, the processing times, costs, and maximum hours) should be used as parameter values when instantiating this model.
\end{itemize}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    N = 3
    IsolateCentral = [10, 6, 8]
    ScanCentral = [6, 4, 6]
    IsolateDistributed = [12, 9, 12]
    ScanDistributed = [18, 10, 15]
    CentralCost = 150
    DistributedCost = 70
    CentralMaxHours = 16
    DistributedMaxHours = 33

    # Create the solver (CBC MILP solver)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: binary variables for each intervention and method.
    # Methods: 0 -> IC, 1 -> SC, 2 -> ID, 3 -> SD
    y = {}
    for i in range(N):
        for j in range(4):
            y[i, j] = solver.BoolVar(f'y[{i},{j}]')

    # Constraint (1): One intervention per cluster
    for i in range(N):
        solver.Add(y[i, 0] + y[i, 1] + y[i, 2] + y[i, 3] == 1)

    # Constraint (2): Central processing time limit
    central_time = 0
    for i in range(N):
        central_time += IsolateCentral[i] * y[i, 0] + ScanCentral[i] * y[i, 1]
    solver.Add(central_time <= CentralMaxHours)

    # Constraint (3): Distributed processing time limit
    distributed_time = 0
    for i in range(N):
        distributed_time += IsolateDistributed[i] * y[i, 2] + ScanDistributed[i] * y[i, 3]
    solver.Add(distributed_time <= DistributedMaxHours)

    # Objective: Minimize total cost
    objective = solver.Objective()
    for i in range(N):
        objective.SetCoefficient(y[i, 0], CentralCost)
        objective.SetCoefficient(y[i, 1], CentralCost)
        objective.SetCoefficient(y[i, 2], DistributedCost)
        objective.SetCoefficient(y[i, 3], DistributedCost)
    objective.SetMinimization()

    # Solve the model
    result_status = solver.Solve()

    # Check the result and print the solution
    if result_status == pywraplp.Solver.OPTIMAL or result_status == pywraplp.Solver.FEASIBLE:
        print("Solution:")
        print("Total cost = ", solver.Objective().Value())
        for i in range(N):
            if y[i, 0].solution_value() == 1:
                method = "Isolate via Central"
            elif y[i, 1].solution_value() == 1:
                method = "Scan via Central"
            elif y[i, 2].solution_value() == 1:
                method = "Isolate via Distributed"
            elif y[i, 3].solution_value() == 1:
                method = "Scan via Distributed"
            else:
                method = "None"
            print(f"Intervention {i+1}: {method}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()