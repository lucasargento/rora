# Mathematical Formulation:
'''\[
\begin{aligned}
\textbf{Indices:} \quad & s \in \{1,\dots,S\} \quad \text{(schools)}, \\
& g \in \{1,\dots,G\} \quad \text{(student groups / grades)}, \\
& n \in \{1,\dots,N\} \quad \text{(neighborhoods)}. \\[1em]

\textbf{Parameters:} \quad
& \text{Capacity}_{s,g} \ge 0, \quad \forall \, s \in \{1,\dots,S\},\, g \in \{1,\dots,G\}, \\
& \text{Population}_{n,g} \ge 0, \quad \forall \, n \in \{1,\dots,N\},\, g \in \{1,\dots,G\}, \\
& \text{Distance}_{n,s} \ge 0, \quad \forall \, n \in \{1,\dots,N\},\, s \in \{1,\dots,S\}. \\[1em]

\textbf{Decision Variables:} \quad
& x_{n,s,g} \ge 0, \quad \forall \, n \in \{1,\dots,N\},\, s \in \{1,\dots,S\},\, g \in \{1,\dots,G\}, \\
& \quad \text{where } x_{n,s,g} \text{ represents the number of students of group } g \text{ from neighborhood } n \\
& \quad \text{assigned to school } s. \\[1em]

\textbf{Objective Function:} \quad
& \text{Minimize } Z = \sum_{n=1}^N \sum_{s=1}^S \sum_{g=1}^G \text{Distance}_{n,s} \, x_{n,s,g}. \\[1em]

\textbf{Constraints:} \\[0.5em]

& \textbf{(1) Demand Fulfillment:} \quad \forall\, n \in \{1,\dots,N\},\, g \in \{1,\dots,G\}: \\
& \quad \sum_{s=1}^S x_{n,s,g} = \text{Population}_{n,g}. \quad \text{(Every student in each group and neighborhood is assigned)} \\[1em]

& \textbf{(2) School Capacity:} \quad \forall\, s \in \{1,\dots,S\},\, g \in \{1,\dots,G\}: \\
& \quad \sum_{n=1}^N x_{n,s,g} \le \text{Capacity}_{s,g}. \quad \text{(Assignments at each school do not exceed its capacity)} \\[1em]

& \textbf{(3) Non-negativity:} \quad \forall\, n,\, s,\, g: \quad x_{n,s,g} \ge 0.
\end{aligned}
\]

This completes the full and exact mathematical formulation of the scheduling problem.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    S = 3  # number of schools
    G = 2  # number of student groups
    N = 4  # number of neighborhoods

    # Capacity matrix: Capacity[s][g]
    capacity = [
        [15, 20],  # School 1 capacities for groups 1 and 2
        [20, 15],  # School 2 capacities for groups 1 and 2
        [5,  17]   # School 3 capacities for groups 1 and 2
    ]
    
    # Population matrix: population[n][g]
    population = [
        [7, 19],  # Neighborhood 1 populations for groups 1 and 2
        [4, 12],  # Neighborhood 2 populations for groups 1 and 2
        [9, 2],   # Neighborhood 3 populations for groups 1 and 2
        [6, 8]    # Neighborhood 4 populations for groups 1 and 2
    ]
    
    # Distance matrix: distance[n][s]
    distance = [
        [5.2, 4.0, 3.1],  # Neighborhood 1 distances to schools 1,2,3
        [3.8, 5.5, 6.1],  # Neighborhood 2 distances to schools 1,2,3
        [4.2, 3.5, 5.0],  # Neighborhood 3 distances to schools 1,2,3
        [5.0, 4.1, 3.2]   # Neighborhood 4 distances to schools 1,2,3
    ]
    
    # Create the solver (using the GLOP linear solver for continuous LP)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[n][s][g] for all neighborhoods, schools, and groups.
    # We'll create a 3D list of variables.
    x = {}
    for n in range(N):
        for s in range(S):
            for g in range(G):
                x[(n, s, g)] = solver.NumVar(0, solver.infinity(), f'x_{n}_{s}_{g}')

    # Constraints
    # (1) Demand Fulfillment: for each neighborhood n and group g, sum_{s} x_{n,s,g} == population[n][g]
    for n in range(N):
        for g in range(G):
            constraint = solver.Constraint(population[n][g], population[n][g])
            for s in range(S):
                constraint.SetCoefficient(x[(n, s, g)], 1)

    # (2) School Capacity: for each school s and group g, sum_{n} x_{n,s,g} <= capacity[s][g]
    for s in range(S):
        for g in range(G):
            constraint = solver.Constraint(0, capacity[s][g])
            for n in range(N):
                constraint.SetCoefficient(x[(n, s, g)], 1)

    # Objective: Minimize total distance traveled by all students
    objective = solver.Objective()
    for n in range(N):
        for s in range(S):
            for g in range(G):
                objective.SetCoefficient(x[(n, s, g)], distance[n][s])
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()

    # Check the result status
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print('Objective value =', objective.Value())
        for n in range(N):
            for s in range(S):
                for g in range(G):
                    val = x[(n, s, g)].solution_value()
                    if val > 1e-6:  # print only non-zero assignments
                        print(f'Assign {val} students from neighborhood {n+1}, group {g+1} to school {s+1}')
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver did not find an optimal solution.")

if __name__ == '__main__':
    main()