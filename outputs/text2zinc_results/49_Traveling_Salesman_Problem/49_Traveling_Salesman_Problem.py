# Mathematical Formulation:
'''\begin{align*}
\textbf{Sets and Indices:} \quad & V = \{0,1,\ldots,N-1\} \quad \text{(set of cities)} \\[1mm]
\textbf{Parameters:} \quad & N \quad \text{(number of cities)}, \\
& \text{StartCity (fixed at city } 0 \text{)}, \\
& d_{ij} \quad \text{(distance from city } i \text{ to city } j\text{, with } d_{ij} = d_{ji} \text{)}, \quad \forall i,j \in V \\[2mm]
\textbf{Decision Variables:} \\[1mm]
x_{ij} &= \begin{cases}
1, & \text{if the traveler travels directly from city } i \text{ to city } j, \\
0, & \text{otherwise},
\end{cases}
\quad \forall i,j \in V,\; i \neq j \\[1mm]
u_{i} &\in \mathbb{R} \quad \text{for } i \in V \setminus \{0\} 
\quad \text{(auxiliary variables used for subtour elimination)} \\[2mm]
\textbf{Objective Function:} \\[1mm]
\text{Minimize} \quad Z &= \sum_{i \in V} \sum_{\substack{j \in V \\ j \neq i}} d_{ij}\, x_{ij} \\[2mm]
\textbf{Subject to:} \\[1mm]
\text{(1) Departure from each city:} \quad & \sum_{\substack{j \in V \\ j \neq i}} x_{ij} = 1, \quad \forall i \in V \\[1mm]
\text{(2) Arrival to each city:} \quad & \sum_{\substack{i \in V \\ i \neq j}} x_{ij} = 1, \quad \forall j \in V \\[1mm]
\text{(3) Subtour Elimination (MTZ constraints):} \quad & u_i - u_j + N\, x_{ij} \leq N - 1, \quad \forall i,j \in V \setminus \{0\},\; i \neq j \\[1mm]
& 1 \leq u_i \leq N-1, \quad \forall i \in V \setminus \{0\} \\[1mm]
\text{(4) Binary Decision Variables:} \quad & x_{ij} \in \{0,1\}, \quad \forall i,j \in V,\; i \neq j
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp


def main():
    # Data
    N = 6
    start_city = 0
    # Distance matrix: 6x6 symmetric matrix. Indexes: 0...5.
    distances = [
        [0, 182, 70, 399, 56, 214],
        [182, 0, 255, 229, 132, 267],
        [70, 255, 0, 472, 127, 287],
        [399, 229, 472, 0, 356, 484],
        [56, 132, 127, 356, 0, 179],
        [214, 267, 287, 484, 179, 0],
    ]

    # Create the solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print('Solver not installed.')
        return

    # Decision variables: x[i][j] is binary, if traveler goes from i to j.
    x = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # Auxiliary variables for MTZ subtour elimination: only for cities except start
    u = {}
    for i in range(N):
        if i != start_city:
            u[i] = solver.IntVar(1, N - 1, f'u_{i}')

    # Constraints

    # (1) Departure: each city i leaves exactly once.
    for i in range(N):
        solver.Add(solver.Sum(x[i, j] for j in range(N) if i != j) == 1)

    # (2) Arrival: each city j is arrived into exactly once.
    for j in range(N):
        solver.Add(solver.Sum(x[i, j] for i in range(N) if i != j) == 1)

    # (3) MTZ Subtour Elimination constraints:
    # For cities i,j in V\{start_city}, i != j
    for i in range(N):
        if i == start_city:
            continue
        for j in range(N):
            if j == start_city or i == j:
                continue
            # u[i] - u[j] + N * x[i,j] <= N - 1
            solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

    # Objective: minimize total travel distance.
    objective = solver.Sum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)
    solver.Minimize(objective)

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal route found:")
        print("Total distance =", solver.Objective().Value())
        # Reconstruct the tour
        route = [start_city]
        current_city = start_city
        while True:
            for j in range(N):
                if current_city != j and x[current_city, j].solution_value() > 0.5:
                    next_city = j
                    route.append(next_city)
                    current_city = next_city
                    break
            if current_city == start_city:
                break

        print("Route:", " -> ".join(str(city) for city in route))
    else:
        print("The problem does not have an optimal solution.")


if __name__ == '__main__':
    main()