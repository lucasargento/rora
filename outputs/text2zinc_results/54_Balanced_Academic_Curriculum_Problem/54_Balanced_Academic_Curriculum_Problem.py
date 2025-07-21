# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & i = 1,2,\ldots,n_{\text{courses}}, \quad j = 1,2,\ldots,n_{\text{periods}}. \\[1mm]
\textbf{Parameters:} \quad & n_{\text{courses}} \quad \text{(number of courses)},\\[0.5mm]
& n_{\text{periods}} \quad \text{(number of academic periods)},\\[0.5mm]
& \ell, \; u \quad \text{(lower and upper bounds for academic load per period)},\\[0.5mm]
& c_\ell, \; c_u \quad \text{(lower and upper bounds for number of courses per period)},\\[0.5mm]
& a_i \quad \text{(academic load of course } i\text{)}, \quad i=1,\ldots,n_{\text{courses}}. \\[2mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\}, \quad \forall\, i=1,\ldots,n_{\text{courses}},\, j=1,\ldots,n_{\text{periods}}, \\
& \quad\text{where } x_{ij}=1 \text{ if course } i \text{ is assigned to period } j; \; 0 \text{ otherwise}. \\[1mm]
& Y \in \mathbb{R}_{\ge 0}, \quad \text{representing the maximum academic load among all periods}. \\[2mm]
\textbf{Objective Function:} \quad & \min \; Y. \\[2mm]
\textbf{Constraints:} \\[0.5mm]
1.\ & \textbf{Assignment:} \quad \sum_{j=1}^{n_{\text{periods}}} x_{ij} = 1, \quad \forall\, i=1,\ldots,n_{\text{courses}}, \\[0.5mm]
2.\ & \textbf{Period Load Bounds:} \quad \ell \le \sum_{i=1}^{n_{\text{courses}}} a_i\, x_{ij} \le u,\quad \forall\, j=1,\ldots,n_{\text{periods}},\\[0.5mm]
3.\ & \textbf{Courses per Period Bounds:} \quad c_\ell \le \sum_{i=1}^{n_{\text{courses}}} x_{ij} \le c_u,\quad \forall\, j=1,\ldots,n_{\text{periods}},\\[0.5mm]
4.\ & \textbf{Definition of Maximum Load:} \quad \sum_{i=1}^{n_{\text{courses}}} a_i\, x_{ij} \le Y, \quad \forall\, j=1,\ldots,n_{\text{periods}}.  
\end{align*}

\textbf{Data Instance (Example):}
\[
n_{\text{courses}} = 6, \quad n_{\text{periods}} = 3, \quad \ell = 10, \quad u = 30, \quad c_\ell = 2, \quad c_u = 4,
\]
\[
\text{and} \quad (a_1, a_2, a_3, a_4, a_5, a_6) = (5, 10, 15, 10, 5, 10).
\]

This complete formulation accurately describes the Balanced Academic Curriculum Problem (BACP) as a scheduling optimization model using binary assignment variables and a minimization of the maximum period load, subject to all specified bounds and assignment constraints.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Problem Data
    n_courses = 6
    n_periods = 3
    load_per_period_lb = 10
    load_per_period_ub = 30
    courses_per_period_lb = 2
    courses_per_period_ub = 4
    course_load = [5, 10, 15, 10, 5, 10]

    model = cp_model.CpModel()

    # Decision variables: x[i][j] == 1 if course i is assigned to period j.
    x = {}
    for i in range(n_courses):
        for j in range(n_periods):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # Maximum load variable: Y
    total_load = sum(course_load)
    Y = model.NewIntVar(0, total_load, 'Y')

    # Period loads: create an auxiliary variable for each period to sum course loads
    period_load = {}
    for j in range(n_periods):
        period_load[j] = model.NewIntVar(load_per_period_lb, load_per_period_ub, f'load_{j}')
        # Set period load to be the sum of courses' loads in period j.
        model.Add(period_load[j] == sum(course_load[i] * x[i, j] for i in range(n_courses)))
        # Constraint to enforce that each period's load does not exceed Y.
        model.Add(period_load[j] <= Y)

    # Constraint 1: Each course is assigned to exactly one period.
    for i in range(n_courses):
        model.Add(sum(x[i, j] for j in range(n_periods)) == 1)

    # Constraint 2 has been taken care of by the domain of period_load and its definition.

    # Constraint 3: Number of courses per period bounds.
    for j in range(n_periods):
        courses_in_period = sum(x[i, j] for i in range(n_courses))
        model.Add(courses_in_period >= courses_per_period_lb)
        model.Add(courses_in_period <= courses_per_period_ub)

    # Objective: minimize the maximum period load Y.
    model.Minimize(Y)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('Optimal solution found:')
        print('Objective (Maximum period load) =', solver.Value(Y))
        for j in range(n_periods):
            assigned_courses = []
            for i in range(n_courses):
                if solver.Value(x[i, j]) == 1:
                    assigned_courses.append(i)
            load_val = solver.Value(period_load[j])
            print(f'Period {j+1}: Courses {assigned_courses}, total load = {load_val}')
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()