# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & n \in \mathbb{N} \quad \text{(number of items)}, \quad a_i \in \mathbb{R}_{>0} \quad \forall i = 1, \dots, n \quad \text{(value of item } i\text{)}, \\
& k \in \mathbb{N} \quad \text{(number of groups)}. \\[1mm]
%
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\} \quad \forall \, i = 1,\dots,n,\; j = 1,\dots,k, \quad \text{where} \quad x_{ij} =
\begin{cases}
1, & \text{if item } i \text{ is assigned to group } j,\\[1mm]
0, & \text{otherwise.}
\end{cases} \\[1mm]
%
& Y \in \mathbb{R}_{\ge 0} \quad \text{(maximum sum among all groups)}. \\[2mm]
%
\textbf{Objective Function:} \quad & \min Y \\[2mm]
%
\textbf{Constraints:} \quad & \text{(a) Each item must be assigned to exactly one group:} \\
& \sum_{j=1}^{k} x_{ij} = 1, \quad \forall \, i = 1,\dots,n. \\[2mm]
%
& \text{(b) Definition of the maximum group sum:} \\
& \sum_{i=1}^{n} a_i \, x_{ij} \le Y, \quad \forall \, j = 1,\dots,k. \\[2mm]
%
& \text{(c) Feasibility and boundedness are ensured by the finite number of items and the positive values } a_i.
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Data
    n = 7
    a = [100, 51, 49, 40, 30, 20, 10]
    k = 3

    # Calculate bounds for Y
    lower_bound = max(a)
    upper_bound = sum(a)

    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Decision variables: x[i][j] = 1 if item i is assigned to group j, otherwise 0.
    x = {}
    for i in range(n):
        for j in range(k):
            x[i, j] = model.NewBoolVar(f"x_{i}_{j}")

    # Y: maximum sum among groups.
    Y = model.NewIntVar(lower_bound, upper_bound, "Y")

    # Constraint (a): Each item must be assigned to exactly one group.
    for i in range(n):
        model.Add(sum(x[i, j] for j in range(k)) == 1)

    # Constraint (b): For each group j, the total value must not exceed Y.
    for j in range(k):
        model.Add(sum(a[i] * x[i, j] for i in range(n)) <= Y)

    # Objective: minimize the maximum group sum Y.
    model.Minimize(Y)

    # Create solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Check and print the solution.
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Optimal objective value (Y):", solver.Value(Y))
        # Print group assignments
        for j in range(k):
            group_items = []
            group_sum = 0
            for i in range(n):
                if solver.Value(x[i, j]) == 1:
                    group_items.append(f"item {i} (value: {a[i]})")
                    group_sum += a[i]
            print(f"Group {j + 1}: {', '.join(group_items)} | Sum = {group_sum}")
    else:
        print("No feasible solution found.")


if __name__ == "__main__":
    main()