# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & n \in \mathbb{Z}_{>0} \quad (\text{number of nodes}), \quad \text{num\_edges} \in \mathbb{Z}_{>0} \quad (\text{number of arcs}), \\[1mm]
& E = \{ (i,j) \mid \text{arc from node } i \text{ to node } j, \, (i,j) \text{ given for } 1 \leq j \leq \text{num\_edges} \}, \\[1mm]
& a_{ij} \ge 0 \quad \text{for each } (i,j) \in E \quad (\text{capacity of arc } (i,j)), \\[1mm]
& s \in \{1,\ldots,n\} \quad (\text{source node}), \quad t \in \{1,\ldots,n\} \quad (\text{sink node}),\\[1mm]
& \text{with } n=9,\; s=1,\; t=n,\; \text{num\_edges}=14, \text{ and the specific data as given.} \\[3mm]
\textbf{Decision Variables:} \quad & x_{ij} \ge 0 \quad \forall\, (i,j) \in E, \\[1mm]
& F \ge 0 \quad \text{(the total flow from source } s \text{ to sink } t \text{)}. \\[3mm]
\textbf{Objective Function:} \quad & \max F. \\[3mm]
\textbf{Constraints:} \\[1mm]
\text{(1) Capacity Constraints:}\quad & x_{ij} \le a_{ij} \quad \forall\,(i,j) \in E. \\[2mm]
\text{(2) Flow Conservation Constraints:} \\[1mm]
& \text{For the source } s:\quad \sum_{\{j \mid (s,j) \in E\}} x_{sj} - \sum_{\{j \mid (j,s) \in E\}} x_{js} = F, \\[2mm]
& \text{For the sink } t:\quad \sum_{\{j \mid (t,j) \in E\}} x_{tj} - \sum_{\{j \mid (j,t) \in E\}} x_{jt} = -F, \\[2mm]
& \text{For every intermediate node } i \in \{1,\ldots,n\}\setminus\{s,t\}: \\[1mm]
& \quad \sum_{\{j \mid (i,j) \in E\}} x_{ij} - \sum_{\{j \mid (j,i) \in E\}} x_{ji} = 0.
\end{align*}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    n = 9
    s = 1
    t = n
    num_edges = 14
    edges = [
        (1, 2),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 5),
        (3, 8),
        (4, 5),
        (5, 2),
        (5, 6),
        (5, 7),
        (6, 7),
        (6, 8),
        (7, 9),
        (8, 9)
    ]
    capacities = [14, 23, 10, 9, 12, 18, 26, 11, 25, 4, 7, 8, 15, 20]

    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Variables: flow on each edge, and total flow F
    x = {}
    for idx, (i, j) in enumerate(edges):
        # x[i,j] is bounded by [0, capacity]
        x[(i, j)] = solver.NumVar(0, capacities[idx], f'x_{i}_{j}')
    
    F = solver.NumVar(0, solver.infinity(), 'F')

    # Flow conservation constraints for every node
    # For each node, sum of outgoing flows minus incoming flows must equal:
    #   For source: equals F.
    #   For sink: equals -F.
    #   For intermediate nodes: equals 0.
    for node in range(1, n+1):
        outflow = solver.Sum(x[(i, j)] for (i, j) in edges if i == node)
        inflow = solver.Sum(x[(i, j)] for (i, j) in edges if j == node)
        
        if node == s:
            # source: outflow - inflow = F
            solver.Add(outflow - inflow == F)
        elif node == t:
            # sink: outflow - inflow = -F
            solver.Add(outflow - inflow == -F)
        else:
            # intermediate nodes: equilibrium (0)
            solver.Add(outflow - inflow == 0)

    # Capacity constraints are already embedded in the variable bounds.
    
    # Objective: maximize F
    solver.Maximize(F)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Maximum flow (F): {F.solution_value()}")
        print("Flow on each edge:")
        for (i, j) in edges:
            print(f"Edge ({i}, {j}): {x[(i, j)].solution_value()}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("No solution found.")
        
if __name__ == '__main__':
    main()