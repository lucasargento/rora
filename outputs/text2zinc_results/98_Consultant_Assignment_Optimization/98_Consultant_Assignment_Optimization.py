# Mathematical Formulation:
'''\[
\begin{array}{rll}
\textbf{Indices and Sets:} & i \in I = \{1,2,\dots,5\} & \quad \text{(projects)}\\[1mm]
                         & j \in J = \{1,2,\dots,3\} & \quad \text{(consultants)}\\[2mm]
\textbf{Parameters:}    & \text{FixedCosts}_j, & \quad j \in J, \quad \text{fixed cost for hiring consultant } j,\\[1mm]
                         & \text{AdditionalCosts}_{ij}, & \quad (i,j) \in I \times J, \quad \text{cost for assigning consultant } j \text{ to project } i,\\[1mm]
                         & M, & \quad \text{MaxProjectsPerConsultant (here, } M=3 \text{)}.\\[2mm]
\textbf{Decision Variables:} & x_{ij} \in \{0,1\}, & \quad \forall (i,j) \in I \times J,\; \text{where } x_{ij}=1 \text{ if project } i \text{ is assigned to consultant } j,\\[1mm]
                         & y_j \in \{0,1\}, & \quad \forall j \in J,\; \text{where } y_j=1 \text{ if consultant } j \text{ is hired.}\\[2mm]
\textbf{Objective:}     & \displaystyle \min \quad Z = \sum_{j \in J} \text{FixedCosts}_j \, y_j + \sum_{i \in I}\sum_{j \in J} \text{AdditionalCosts}_{ij} \, x_{ij}. & \\[2mm]
\textbf{Subject to:}    & \displaystyle \sum_{j \in J} x_{ij} = 1, & \quad \forall i \in I, \quad \text{(each project must be assigned to exactly one consultant)}\\[2mm]
                         & \displaystyle \sum_{i \in I} x_{ij} \leq M, & \quad \forall j \in J, \quad \text{(each consultant can handle at most } M \text{ projects)}\\[2mm]
                         & \displaystyle x_{ij} \leq y_j, & \quad \forall (i,j) \in I \times J, \quad \text{(a consultant must be hired to be assigned a project)}.
\end{array}
\]

This formulation fully captures the assignment problem by defining the binary decision variables, the objective function (minimizing total cost), and all the necessary constraints ensuring every project is assigned and that a consultant’s project load does not exceed the maximum allowed.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    num_projects = 5  # Number of projects (I)
    num_consultants = 3  # Number of consultants (J)
    
    # Consultant fixed costs: FixedCosts[j] for j = 0,...,2
    fixed_costs = [100, 150, 135]
    
    # Additional costs matrix for assigning project i to consultant j: additional_costs[i][j]
    additional_costs = [
        [10, 12, 20],  # Project 1
        [10, 8, 12],   # Project 2
        [15, 8, 20],   # Project 3
        [10, 6, 15],   # Project 4
        [8, 10, 15]    # Project 5
    ]
    
    # Maximum number of projects per consultant
    max_projects_per_consultant = 3
    
    # Create the solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables
    # x[i][j] = 1 if project i is assigned to consultant j, otherwise 0.
    x = {}
    for i in range(num_projects):
        for j in range(num_consultants):
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')
    
    # y[j] = 1 if consultant j is hired, otherwise 0.
    y = {}
    for j in range(num_consultants):
        y[j] = solver.BoolVar(f'y_{j}')
    
    # Constraints
    # Each project must be assigned to exactly one consultant.
    for i in range(num_projects):
        solver.Add(solver.Sum(x[i, j] for j in range(num_consultants)) == 1)
    
    # Each consultant can handle at most max_projects_per_consultant projects.
    for j in range(num_consultants):
        solver.Add(solver.Sum(x[i, j] for i in range(num_projects)) <= max_projects_per_consultant)
    
    # Link assignment and consultant hiring: A consultant must be hired to be assigned a project.
    for i in range(num_projects):
        for j in range(num_consultants):
            solver.Add(x[i, j] <= y[j])
    
    # Objective: Minimize fixed costs for hiring consultants and additional assignment costs.
    objective = solver.Sum(fixed_costs[j] * y[j] for j in range(num_consultants))
    objective += solver.Sum(additional_costs[i][j] * x[i, j]
                              for i in range(num_projects)
                              for j in range(num_consultants))
    solver.Minimize(objective)
    
    # Solve the model.
    status = solver.Solve()
    
    # Output results.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Total Cost = {solver.Objective().Value()}")
        print("\nConsultant Hiring Decisions:")
        for j in range(num_consultants):
            if y[j].solution_value() > 0.5:
                print(f"  Consultant {j+1} is hired (Fixed cost = {fixed_costs[j]})")
            else:
                print(f"  Consultant {j+1} is not hired")
                
        print("\nProject Assignments:")
        for i in range(num_projects):
            for j in range(num_consultants):
                if x[i, j].solution_value() > 0.5:
                    print(f"  Project {i+1} is assigned to Consultant {j+1} (Additional cost = {additional_costs[i][j]})")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()