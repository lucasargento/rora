# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\quad & i \in \{1,2,\ldots,15\} \quad \text{(projects)}\\[1mm]
& k \in \{1,2,\ldots,6\} \quad \text{(index for "not\_with" pairs)}\\[1mm]
& \ell \in \{1,2,\ldots,5\} \quad \text{(index for "requires" pairs)}\\[2mm]

\textbf{Data:}\quad & \text{max\_budget } = 225 \quad \text{(million SEK)}\\[1mm]
& \text{max\_persons } = 28 \quad \text{(number of persons available)}\\[1mm]
& \text{max\_projects } = 9 \quad \text{(maximum number of projects selected)}\\[1mm]
& v_i:\ \text{value of project } i \quad \Big( \text{with } v = [600,400,100,150,80,120,200,220,90,380,290,130,80,270,280]\ \text{in thousand SEK}\Big) \\[1mm]
& b_i:\ \text{budget requirement of project } i \quad \Big( \text{with } b = [35,34,26,12,10,18,32,11,10,22,27,18,16,29,22]\ \text{in million SEK}\Big)\\[1mm]
& p_i:\ \text{personnel requirement of project } i \quad \Big( p = [5,3,4,2,2,2,4,1,1,5,3,2,2,4,3] \Big)\\[2mm]

\textbf{Conflict Pairs ("not\_with" relations):}\quad & \text{For } k=1,\ldots,6,\ \text{ let } (i_k, j_k) \text{ be given by:} \\
& (i_1, j_1) = (1,10),\quad (i_2, j_2) = (5,6),\quad (i_3, j_3) = (6,5),\\[1mm]
& (i_4, j_4) = (10,1),\quad (i_5, j_5) = (11,15),\quad (i_6, j_6) = (15,11).\\[2mm]

\textbf{Required Pairs ("requires" relations):}\quad & \text{For } \ell=1,\ldots,5,\ \text{ let } (r_\ell, s_\ell) \text{ be given by:} \\
& (r_1, s_1) = (3,15),\quad (r_2, s_2) = (4,15),\quad (r_3, s_3) = (8,7),\\[1mm]
& (r_4, s_4) = (13,2),\quad (r_5, s_5) = (14,2).\\[2mm]

\textbf{Decision Variables:}\\[1mm]
& x_i \in \{0,1\} \quad \forall i \in \{1,\ldots,15\} \\
& \quad \text{where } x_i=1 \text{ if project } i \text{ is selected, and } x_i=0 \text{ otherwise.}\\[2mm]

\textbf{Objective Function:}\\[1mm]
& \text{maximize} \quad Z = \sum_{i=1}^{15} v_i \, x_i. \\[2mm]

\textbf{Constraints:}\\[1mm]
& \text{(Budget Constraint)} \quad \sum_{i=1}^{15} b_i \, x_i \leq 225. \\[2mm]
& \text{(Personnel Constraint)} \quad \sum_{i=1}^{15} p_i \, x_i \leq 28. \\[2mm]
& \text{(Maximum Projects Constraint)} \quad \sum_{i=1}^{15} x_i \leq 9. \\[2mm]
& \text{(Mutual Exclusion Constraints)} \quad \text{For each } k=1,\ldots,6: \quad x_{i_k} + x_{j_k} \leq 1. \\[2mm]
& \text{(Required Selection Constraints)} \quad \text{For each } \ell=1,\ldots,5: \quad x_{r_\ell} - x_{s_\ell} = 0.
\end{align*} 

This formulation accurately models the knapsack (investment) problem with budget, personnel, project count limitations, conflict restrictions (projects that cannot be selected together) and dependency restrictions (projects that must be selected together), ensuring the problem is both feasible and bounded.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem Data
    num_projects = 15
    max_budget = 225
    max_persons = 28
    max_projects = 9
    values = [600, 400, 100, 150, 80, 120, 200, 220, 90, 380, 290, 130, 80, 270, 280]
    budgets = [35, 34, 26, 12, 10, 18, 32, 11, 10, 22, 27, 18, 16, 29, 22]
    personell = [5, 3, 4, 2, 2, 2, 4, 1, 1, 5, 3, 2, 2, 4, 3]

    # Not_with pairs (project indices are 1-indexed in the problem, convert to 0-indexed)
    not_with = [
        (1, 10),
        (5, 6),
        (6, 5),
        (10, 1),
        (11, 15),
        (15, 11)
    ]
    not_with = [(i - 1, j - 1) for i, j in not_with]

    # Requires pairs (project indices are 1-indexed in the problem, convert to 0-indexed)
    requires = [
        (3, 15),
        (4, 15),
        (8, 7),
        (13, 2),
        (14, 2)
    ]
    requires = [(r - 1, s - 1) for r, s in requires]

    # Create the model
    model = cp_model.CpModel()

    # Variables: x[i] = 1 if project i is selected.
    x = [model.NewBoolVar(f'x[{i}]') for i in range(num_projects)]

    # Budget constraint
    model.Add(sum(budgets[i] * x[i] for i in range(num_projects)) <= max_budget)

    # Personnel constraint
    model.Add(sum(personell[i] * x[i] for i in range(num_projects)) <= max_persons)

    # Maximum projects constraint
    model.Add(sum(x[i] for i in range(num_projects)) <= max_projects)

    # Mutual exclusion constraints: cannot pick both projects in each pair
    for i, j in not_with:
        model.Add(x[i] + x[j] <= 1)

    # Required selection constraints: if one is selected then the other must be selected too (x[r] == x[s])
    for r, s in requires:
        model.Add(x[r] == x[s])

    # Objective: maximize total value
    model.Maximize(sum(values[i] * x[i] for i in range(num_projects)))

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('Optimal solution found:')
        print(f'Objective value: {solver.ObjectiveValue()}')
        print('Selected Projects:')
        for i in range(num_projects):
            if solver.Value(x[i]) == 1:
                print(f'Project {i+1} (Value: {values[i]}, Budget: {budgets[i]}, Personell: {personell[i]})')
    else:
        print('No feasible solution found.')


if __name__ == '__main__':
    main()