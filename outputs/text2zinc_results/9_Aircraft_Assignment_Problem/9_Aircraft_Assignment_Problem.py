# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i \in \{1,2,\ldots, N\} \quad \text{(aircraft index)}, \quad j \in \{1,2,\ldots, M\} \quad \text{(route index)}.\\[1mm]
\textbf{Parameters:} \quad & N = \text{TotalAircraft}, \quad M = \text{TotalRoutes},\\[1mm]
& a_i \quad = \text{Availability of aircraft } i \quad \left(i=1,\ldots,N\right),\\[1mm]
& d_j \quad = \text{Passenger demand on route } j \quad \left(j=1,\ldots,M\right),\\[1mm]
& c_{ij} \quad = \text{Passenger capacity if aircraft } i \text{ serves route } j \quad \left(i=1,\ldots,N; \, j=1,\ldots,M\right),\\[1mm]
& k_{ij} \quad = \text{Cost of operating a flight with aircraft } i \text{ on route } j \quad \left(i=1,\ldots,N; \, j=1,\ldots,M\right).
\end{align*}

\vspace{2mm}
%-------------------------------------------------------------------
\textbf{Decision Variables:}\\[2mm]
Let 
\begin{align*}
y_{ij} \in \mathbb{Z}_+ \quad \text{for all } i=1,\ldots,N,\; j=1,\ldots,M,
\end{align*}
where 
\begin{itemize}
  \item $y_{ij}$ represents the number of flights (or assignments) of aircraft $i$ to route $j$. 
\end{itemize}

\vspace{2mm}
%-------------------------------------------------------------------
\textbf{Objective Function:}\\[2mm]
The goal is to minimize the total cost of the assignments. Thus, the objective function is given by

\begin{align*}
\min \; Z = \sum_{i=1}^{N} \sum_{j=1}^{M} k_{ij}\, y_{ij}.
\end{align*}

\vspace{2mm}
%-------------------------------------------------------------------
\textbf{Constraints:}\\[2mm]
\textbf{(1) Aircraft Availability Constraints:} \\
Each aircraft $i$ has a limited number of flights it can operate (its overall availability):

\begin{align*}
\sum_{j=1}^{M} y_{ij} \leq a_i, \quad \forall\, i=1,\ldots,N.
\end{align*}

\vspace{2mm}
\textbf{(2) Route Demand Constraints:}\\
Each route $j$ has a required number of passengers to be carried. Since a flight operated by aircraft $i$ on route $j$ can carry up to $c_{ij}$ passengers, the aggregate capacity assigned to route $j$ must meet or exceed the demand $d_j$:

\begin{align*}
\sum_{i=1}^{N} c_{ij}\, y_{ij} \geq d_j, \quad \forall\, j=1,\ldots,M.
\end{align*}

\vspace{2mm}
\textbf{(3) Nonnegativity and Integer Restrictions:}\\[2mm]
\begin{align*}
y_{ij} \in \mathbb{Z}_+, \quad \forall\, i=1,\ldots,N,\; j=1,\ldots,M.
\end{align*}

\vspace{2mm}
%-------------------------------------------------------------------
\textbf{Summary:}\\[2mm]
The complete mathematical model for this Aircraft Assignment Problem is therefore:

\begin{align*}
\min_{y_{ij}} \quad & \sum_{i=1}^{N} \sum_{j=1}^{M} k_{ij}\, y_{ij} \\[1mm]
\text{s.t.} \quad & \sum_{j=1}^{M} y_{ij} \leq a_i, & \quad \forall\, i=1,\ldots,N, \\[1mm]
& \sum_{i=1}^{N} c_{ij}\, y_{ij} \geq d_j, & \quad \forall\, j=1,\ldots,M, \\[1mm]
& y_{ij} \in \mathbb{Z}_+, & \quad \forall\, i=1,\ldots,N,\; j=1,\ldots,M.
\end{align*}

\vspace{2mm}
\textbf{Notes:}
\begin{itemize}
    \item The variable $y_{ij}$ indicates how many flights by aircraft $i$ on route $j$ are scheduled. This formulation allows multiple flights (assignments) from the same aircraft to a given route provided that the aircraft’s overall availability is not exceeded.
    \item The route demand constraints ensure that the total number of passengers that can be carried by the allocated flights on each route is at least the route's demand.
    \item The model is feasible and bounded provided that the given data (Availability, Demand, Capacity, and Costs matrices) lead to a possibility of meeting all demands without exceeding aircraft availabilities.
\end{itemize}

This fully detailed formulation reflects the entire problem as described and is ready to be used as a basis for an OR-Tools implementation.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    TotalAircraft = 4
    TotalRoutes = 4

    # Availability of each aircraft
    Availability = [500, 600, 700, 800]

    # Demand for each route
    Demand = [200, 300, 400, 500]

    # Capacity matrix for aircraft i on route j
    Capacity = [
        [100, 200, 300, 400],  # Aircraft 1
        [200, 300, 400, 500],  # Aircraft 2
        [300, 400, 500, 600],  # Aircraft 3
        [400, 500, 600, 700]   # Aircraft 4
    ]

    # Cost matrix for aircraft i on route j
    Costs = [
        [10, 20, 30, 40],  # Aircraft 1
        [20, 30, 40, 50],  # Aircraft 2
        [30, 40, 50, 60],  # Aircraft 3
        [40, 50, 60, 70]   # Aircraft 4
    ]

    # Create the solver: Using CBC Mixed Integer programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return

    # Decision Variables:
    # y[i][j] is the number of flights of aircraft i assigned to route j.
    y = {}
    for i in range(TotalAircraft):
        for j in range(TotalRoutes):
            y[i, j] = solver.IntVar(0, solver.infinity(), f'y_{i}_{j}')

    # Objective: Minimize total cost of assignments
    objective = solver.Objective()
    for i in range(TotalAircraft):
        for j in range(TotalRoutes):
            objective.SetCoefficient(y[i, j], Costs[i][j])
    objective.SetMinimization()

    # Constraints:
    # (1) Aircraft Availability: Sum of flights for each aircraft <= availability
    for i in range(TotalAircraft):
        constraint = solver.RowConstraint(-solver.infinity(), Availability[i], f'Aircraft_{i}_availability')
        for j in range(TotalRoutes):
            constraint.SetCoefficient(y[i, j], 1)

    # (2) Route Demand: Total capacity assigned to each route must be >= demand.
    for j in range(TotalRoutes):
        constraint = solver.RowConstraint(Demand[j], solver.infinity(), f'Route_{j}_demand')
        for i in range(TotalAircraft):
            constraint.SetCoefficient(y[i, j], Capacity[i][j])

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Optimal solution found:")
        print(f"Total Cost = {solver.Objective().Value():.2f}")
        for i in range(TotalAircraft):
            for j in range(TotalRoutes):
                if y[i, j].solution_value() > 0:
                    print(f"Aircraft {i + 1} assigned {y[i, j].solution_value():.0f} flights to Route {j + 1}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()