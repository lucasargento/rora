# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} & i \in \{1,2,3,4,5\} & \quad \text{(Programmers)} \\
                 & j \in \{1,2,3,4,5\} & \quad \text{(Jobs)}
\end{array}
\]

\[
\begin{align*}
\textbf{Decision Variables:} \quad & x_{ij} =
\begin{cases}
1, & \text{if programmer } i \text{ is assigned to job } j,\\[1mm]
0, & \text{otherwise;}
\end{cases} \quad \text{for all } i=1,\ldots,5, \; j=1,\ldots,5.
\end{align*}
\]

\[
\begin{align*}
\textbf{Parameters:} \quad & \text{Let } cost_{ij} \text{ be the preference (cost) of programmer } i \text{ for job } j, \\
                           & \text{with the following given cost matrix:} \\
                           & \quad cost = \begin{bmatrix}
                           4 & 1 & 3 & 5 & 2 \\
                           2 & 1 & 3 & 4 & 5 \\
                           3 & 2 & 4 & 1 & 5 \\
                           2 & 3 & 4 & 5 & 1 \\
                           4 & 2 & 3 & 1 & 5 \\
                           \end{bmatrix}.
\end{align*}
\]

\[
\begin{align*}
\textbf{Objective Function:} \quad & \min \quad Z = \sum_{i=1}^{5} \sum_{j=1}^{5} cost_{ij} \, x_{ij}.
\end{align*}
\]

\[
\begin{align*}
\textbf{Constraints:} & \\[1mm]
\text{(1) Each Programmer is assigned exactly one job:} \quad & \sum_{j=1}^{5} x_{ij} = 1, \quad \forall\, i = 1,\ldots,5. \\[1mm]
\text{(2) Each Job is assigned to exactly one programmer:} \quad & \sum_{i=1}^{5} x_{ij} = 1, \quad \forall\, j = 1,\ldots,5. \\[1mm]
\text{(3) Binary Decision Variables:} \quad & x_{ij} \in \{0,1\}, \quad \forall\, i = 1,\ldots,5, \; j = 1,\ldots,5.
\end{align*}
\]

This complete formulation accurately models the assignment (scheduling) problem, ensuring that every programmer is allocated exactly one job and each job is filled by exactly one programmer, while minimizing the total sum of preference costs.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    num_programmers = 5
    num_jobs = 5
    cost = [
        [4, 1, 3, 5, 2],
        [2, 1, 3, 4, 5],
        [3, 2, 4, 1, 5],
        [2, 3, 4, 5, 1],
        [4, 2, 3, 1, 5]
    ]
    
    # Create model
    model = cp_model.CpModel()
    
    # Create decision variables: x[i][j] = 1 if programmer i is assigned to job j.
    x = {}
    for i in range(num_programmers):
        for j in range(num_jobs):
            x[i, j] = model.NewBoolVar(f'x[{i},{j}]')
    
    # Constraints:
    # Each programmer is assigned exactly one job.
    for i in range(num_programmers):
        model.Add(sum(x[i, j] for j in range(num_jobs)) == 1)
    
    # Each job is assigned to exactly one programmer.
    for j in range(num_jobs):
        model.Add(sum(x[i, j] for i in range(num_programmers)) == 1)
    
    # Objective function: minimize the sum of preference costs.
    objective_terms = []
    for i in range(num_programmers):
        for j in range(num_jobs):
            objective_terms.append(cost[i][j] * x[i, j])
    model.Minimize(sum(objective_terms))
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Objective value: {solver.ObjectiveValue()}')
        print('Assignment:')
        for i in range(num_programmers):
            for j in range(num_jobs):
                if solver.Value(x[i, j]) == 1:
                    print(f'Programmer {i + 1} assigned to Job {j + 1} with cost {cost[i][j]}')
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()