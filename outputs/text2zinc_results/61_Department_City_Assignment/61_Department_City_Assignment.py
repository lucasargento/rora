# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & i,k \in \{1,\dots, \text{ndepts}\} \quad (\text{departments}), \quad j,\ell \in \{1,\dots, \text{ncities}\} \quad (\text{cities}).\\[1mm]
\textbf{Parameters:} \quad & \text{ndepts} \quad (\text{number of departments}),\\[0.5mm]
& \text{ncities} \quad (\text{number of cities}),\\[0.5mm]
& \text{benefit}_{ij} \quad (\text{benefit in £k of locating department } i \text{ in city } j),\\[0.5mm]
& \text{dist}_{j\ell} \quad (\text{communication cost per unit between city } j \text{ and city } \ell),\\[0.5mm]
& \text{comm}_{ik} \quad (\text{quantity of communication in k units between department } i \text{ and } k).\\[2mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\} \quad \forall i=1,\dots,\text{ndepts},\quad j=1,\dots,\text{ncities},\\[0.5mm]
&\quad \text{where} \quad x_{ij} = 
  \begin{cases}
    1, & \text{if department } i \text{ is located in city } j,\\[0.5mm]
    0, & \text{otherwise.}
  \end{cases}\\[2mm]
\textbf{Objective Function:}\\[0.5mm]
\text{Maximize} \quad & Z = \underbrace{\sum_{i=1}^{\text{ndepts}}\sum_{j=1}^{\text{ncities}} \text{benefit}_{ij}\, x_{ij}}_{\text{total benefit}} 
- \underbrace{\sum_{1 \le i < k \le \text{ndepts}} \sum_{j=1}^{\text{ncities}} \sum_{\ell=1}^{\text{ncities}} \text{comm}_{ik}\, \text{dist}_{j\ell}\, x_{ij}\, x_{k\ell}}_{\text{total communication costs}}.
\\[2mm]
\textbf{Constraints:}\\[0.5mm]
& \textbf{(1) Each department is assigned to exactly one city:} \\
& \quad \sum_{j=1}^{\text{ncities}} x_{ij} = 1 \quad \forall\, i = 1,\dots,\text{ndepts}. \\[1mm]
& \textbf{(2) City capacity: at most 3 departments per city:} \\
& \quad \sum_{i=1}^{\text{ndepts}} x_{ij} \le 3 \quad \forall\, j = 1,\dots,\text{ncities}. \\[1mm]
& \textbf{(3) Binary requirement:} \\
& \quad x_{ij} \in \{0,1\} \quad \forall\, i=1,\dots,\text{ndepts},\ j=1,\dots,\text{ncities}.
\end{align*}

\vspace{2mm}
This formulation fully captures the problem of locating departments in cities with associated relocation benefits and communication costs. The goal is to choose an assignment (i.e., values of the binary variables $x_{ij}$) so as to maximize the total savings (benefit minus the communication-related costs) subject to each department being located exactly once and each city accommodating at most 3 departments. This model is both feasible and bounded as required.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Data.
    ndepts = 5
    ncities = 3

    # benefits for each department in each city (£k)
    benefit = [
        [10, 10, 0],
        [15, 20, 0],
        [10, 15, 0],
        [20, 15, 0],
        [5, 15, 0]
    ]

    # communication cost per unit (£) between cities
    dist = [
        [5, 14, 13],
        [14, 5, 9],
        [13, 9, 10]
    ]

    # communication quantity (k units) between departments
    comm = [
        [0.0, 0.0, 1.0, 1.5, 0.0],
        [0.0, 0.0, 1.4, 1.2, 0.0],
        [0.0, 0.0, 0.0, 0.0, 2.0],
        [0.0, 0.0, 0.0, 0.0, 0.7],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]

    model = cp_model.CpModel()

    # Decision variables:
    # x[i][j] == 1 if department i is assigned to city j.
    x = {}
    for i in range(ndepts):
        for j in range(ncities):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')

    # For pairs of departments and assignment of cities, we linearize the product x[i,j] * x[k,l]
    # Only consider i < k.
    y = {}
    for i in range(ndepts):
        for k in range(i + 1, ndepts):
            for j in range(ncities):
                for l in range(ncities):
                    y[i, k, j, l] = model.NewBoolVar(f'y_{i}_{k}_{j}_{l}')
                    # Link y and x by linearization constraints.
                    model.AddBoolAnd([x[i, j], x[k, l]]).OnlyEnforceIf(y[i, k, j, l])
                    # If y is 0 then at least one of x[i,j] or x[k,l] is 0.
                    # Use reified constraints: y == 1 <=> (x[i,j] and x[k,l])
                    # Alternatively, add linear constraints:
                    model.Add(x[i, j] + x[k, l] - y[i, k, j, l] <= 1)

    # Constraints:
    # 1. Each department is assigned to exactly one city.
    for i in range(ndepts):
        model.Add(sum(x[i, j] for j in range(ncities)) == 1)

    # 2. City capacity: at most 3 departments per city.
    for j in range(ncities):
        model.Add(sum(x[i, j] for i in range(ndepts)) <= 3)

    # Objective: maximize total benefit minus total communication cost.
    # Total benefit: sum_{i,j} benefit[i][j] * x[i,j]
    total_benefit = sum(benefit[i][j] * x[i, j] for i in range(ndepts) for j in range(ncities))

    # Total communication cost: sum_{i<k} sum_{j,l} comm[i][k] * dist[j][l] * y[i,k,j,l]
    total_comm_cost = []
    for i in range(ndepts):
        for k in range(i + 1, ndepts):
            for j in range(ncities):
                for l in range(ncities):
                    coef = comm[i][k] * dist[j][l]
                    if coef != 0:
                        total_comm_cost.append(coef * y[i, k, j, l])
    # Define the objective: maximize benefit minus cost.
    model.Maximize(total_benefit - sum(total_comm_cost))

    # Create the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print(f'Objective value = {solver.ObjectiveValue()}')
        for i in range(ndepts):
            for j in range(ncities):
                if solver.Value(x[i, j]) == 1:
                    print(f'Department {i} in city {j}')
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()