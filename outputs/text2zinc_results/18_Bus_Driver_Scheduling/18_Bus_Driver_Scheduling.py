# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Parameters:} & & \\
& n_w &= \text{Number of works} = 24, \\
& n_s &= \text{Number of shifts} = 77, \\
& \underline{n}_s &= \text{Minimum number of shifts required} = 7, \\
& S_j \subseteq \{1,2,\ldots,n_w\} & \text{for } j = 1,\ldots, n_s, \quad \text{(set of works covered by shift } j\text{)}. \\[1ex]
\text{For convenience, define } & a_{ij} = \begin{cases}
1, & \text{if } i \in S_j,\\[1mm]
0, & \text{otherwise},
\end{cases} & \text{for } i=1,\ldots,n_w, \; j=1,\ldots,n_s. \\[1ex]
\\
\textbf{Decision Variables:} & & \\
x_j \in \{0,1\}, & & j = 1,\ldots,n_s, \quad \text{where } \\
& & x_j = \begin{cases}
1, & \text{if shift } j \text{ is selected},\\[1mm]
0, & \text{otherwise}.
\end{cases} \\[1ex]
\\
\textbf{Objective Function:} & & \\
\min & \displaystyle \sum_{j=1}^{n_s} x_j. & \quad \text{(Minimize the total number of selected shifts)} \\[2ex]
\\
\textbf{Constraints:} & & \\
\text{Coverage Constraints: } & \displaystyle \sum_{j=1}^{n_s} a_{ij} \, x_j = 1, & \quad \forall \; i = 1, \ldots, n_w, \quad \text{(each work is covered exactly once)}. \\[1ex]
\text{Minimum Shifts Requirement: } & \displaystyle \sum_{j=1}^{n_s} x_j \ge \underline{n}_s, & \quad \text{(ensure at least } \underline{n}_s \text{ shifts are selected)}. \\[1ex]
\end{array}
\]

This completes the full mathematical formulation of the bus driver scheduling problem as a set partitioning model.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem data
    num_work = 24
    num_shifts = 77
    min_num_shifts = 7

    # Shifts: each shift is given as a set of works (0-indexed works)
    shifts = [
        {11, 18},
        {11, 3, 4},
        {11, 18, 19},
        {11, 12, 14, 15},
        {11, 18, 19, 20},
        {11, 12, 19, 20},
        {1, 18},
        {1, 3, 4},
        {1, 18, 19},
        {1, 2, 14, 15},
        {1, 18, 19, 20},
        {1, 2, 19, 20},
        {1, 2, 3, 10},
        {7, 18},
        {7, 3, 4},
        {7, 18, 19},
        {7, 14, 15},
        {7, 18, 19, 20},
        {7, 8, 9, 10},
        {7, 14, 15, 16},
        {7, 8, 9, 5, 6},
        {7, 3, 4, 5, 6},
        {12, 13, 14, 10},
        {12, 13, 15, 16},
        {12, 13, 5, 6},
        {12, 13, 20, 21},
        {12, 13, 14, 21},
        {2, 3, 10},
        {2, 3, 15, 16},
        {2, 3, 5, 6},
        {2, 3, 20, 21},
        {2, 3, 4, 21},
        {8, 9, 10},
        {8, 9, 5, 6},
        {8, 9, 20, 21},
        {8, 9, 16, 17},
        {13, 14, 10},
        {13, 14, 21},
        {13, 14, 16, 17},
        {13, 14, 15, 17},
        {13, 14, 15, 16, 22},
        {13, 14, 21, 22},
        {3, 4, 21},
        {3, 4, 16, 17},
        {3, 4, 21, 22},
        {18, 10},
        {18, 15, 16},
        {18, 5, 6},
        {18, 20, 21},
        {18, 19, 21},
        {18, 15, 16, 17},
        {18, 19, 16, 17},
        {18, 19, 20, 17},
        {18, 20, 21, 22},
        {18, 19, 21, 22},
        {18, 19, 20, 22},
        {14, 15, 17},
        {14, 15, 16, 22},
        {4, 5, 6, 23},
        {19, 20, 17},
        {19, 20, 22},
        {19, 20, 21, 23},
        {19, 20, 22, 23},
        {19, 20, 21, 0},
        {15, 16, 22},
        {15, 16, 17, 23},
        {15, 16, 22, 23},
        {15, 16, 17, 0},
        {5, 6, 23},
        {20, 21, 23},
        {20, 21, 0},
        {10, 22},
        {10, 22, 23},
        {16, 17, 23},
        {16, 17, 0},
        {21, 23},
        {21, 0}
    ]

    # Create CP-SAT model
    model = cp_model.CpModel()

    # Create binary variables for each shift
    x = [model.NewBoolVar(f'x[{j}]') for j in range(num_shifts)]

    # For each work, ensure it is covered exactly once.
    # Note: Work indices are 0-indexed (0..num_work-1)
    for i in range(num_work):
        # Collect all shifts that cover work i
        involved_shifts = []
        for j in range(num_shifts):
            if i in shifts[j]:
                involved_shifts.append(x[j])
        # The work must be covered exactly once.
        model.Add(sum(involved_shifts) == 1)

    # Minimum shifts requirement constraint.
    model.Add(sum(x) >= min_num_shifts)

    # Objective: Minimize the total number of selected shifts.
    model.Minimize(sum(x))

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print('Solution Found:')
        print('Objective (total number of shifts selected) =', solver.ObjectiveValue())
        selected_shifts = []
        for j in range(num_shifts):
            if solver.Value(x[j]) == 1:
                selected_shifts.append(j)
        print('Selected shift indices:', selected_shifts)
    else:
        print('No solution found.')


if __name__ == '__main__':
    main()