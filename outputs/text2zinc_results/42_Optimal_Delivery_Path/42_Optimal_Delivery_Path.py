# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices:} & n & = 1,2,\ldots,N, & \text{(east–west streets)} \\
                 & w & = 1,2,\ldots,W, & \text{(north–south avenues)} \\[1mm]
\textbf{Decision Variables:} & & & \\
&& x_{n,w} \in \{0,1\}, & \quad \forall\, n=1,\ldots,N,\; w=1,\ldots,W-1,\\[1mm]
&& y_{n,w} \in \{0,1\}, & \quad \forall\, n=1,\ldots,N-1,\; w=1,\ldots,W,\\[1mm]
& & \text{where} &  \\
& x_{n,w}=1 \quad \Longleftrightarrow \quad  \text{the delivery person takes the westward edge from} \ (n,w) \text{ to } (n,w+1),\\[1mm]
& y_{n,w}=1 \quad \Longleftrightarrow \quad  \text{the delivery person takes the northward edge from} \ (n,w) \text{ to } (n+1,w).\\[2mm]
\textbf{Parameters:} & & & \\
& \text{WestTime}_{n,w} >0, & \quad \forall\, n=1,\ldots,N,\; w=1,\ldots,W-1,\\[1mm]
& \text{NorthTime}_{n,w} >0, & \quad \forall\, n=1,\ldots,N-1,\; w=1,\ldots,W.\\[2mm]
\textbf{Data Example:} & N=3,& \;W=3, &\\[1mm]
& \text{WestTime} = \begin{array}{|c|c|} \hline 3.5 & 4.5\\ \hline 4   & 4\\ \hline 5   & 4\\ \hline \end{array}, & \quad \text{(indexed as } (n,w)\text{ with } n=1,2,3,\; w=1,2\text{)}\\[1mm]
& \text{NorthTime} = \begin{array}{|c|c|c|} \hline 10 & 10 & 9\\ \hline 9  & 9  & 12\\ \hline \end{array}, & \quad \text{(indexed as } (n,w)\text{ with } n=1,2,\; w=1,2,3\text{)}\\[2mm]
\textbf{Objective Function:} & \min & Z = \displaystyle \sum_{n=1}^{N-1}\sum_{w=1}^{W} \text{NorthTime}_{n,w}\, y_{n,w} \;+\; \sum_{n=1}^{N}\sum_{w=1}^{W-1} \text{WestTime}_{n,w}\, x_{n,w} & \quad \text{(minimize total travel time)}\\[3mm]
\textbf{Flow Conservation Constraints:} & & & \\[1mm]
\multicolumn{4}{l}{\text{For each intersection } (n,w)\in\{1,\dots,N\}\times\{1,\dots,W\}\text{:}}\\[1mm]
& \displaystyle \underbrace{\Bigl[\mathbb{I}_{\{n\le N-1\}}\, y_{n,w} \;+\; \mathbb{I}_{\{w\le W-1\}}\, x_{n,w}\Bigr]}_{\text{Flow leaving }(n,w)} & - & \displaystyle \underbrace{\Bigl[\mathbb{I}_{\{n\ge 2\}}\, y_{n-1,w} \;+\; \mathbb{I}_{\{w\ge 2\}}\, x_{n,w-1}\Bigr]}_{\text{Flow entering }(n,w)} \;=\; b_{n,w},\\[2mm]
&&& \text{where} \quad b_{n,w}=
\begin{cases}
1, & \mbox{if } (n,w)=(1,1);\\[1mm]
-1, & \mbox{if } (n,w)=(N,W);\\[1mm]
0, & \mbox{otherwise.}
\end{cases}
\end{array}
\]

An alternative, fully expanded formulation (avoiding indicator functions) is as follows:

\[
\begin{align*}
\textbf{At the origin } (1,1):\quad & \begin{array}{rcl}
y_{1,1} + x_{1,1} &=& 1. 
\end{array}\\[1mm]
\textbf{For nodes on the first row } (1,w),\; 2\le w\le W-1:\quad & \begin{array}{rcl}
y_{1,w} + x_{1,w} - x_{1,w-1} &=& 0.
\end{array}\\[1mm]
\textbf{For nodes on the first column } (n,1),\; 2\le n\le N-1:\quad & \begin{array}{rcl}
y_{n,1} + x_{n,1} - y_{n-1,1} &=& 0.
\end{array}\\[1mm]
\textbf{For interior nodes } (n,w),\; 2\le n\le N-1,\; 2\le w\le W-1:\quad & \begin{array}{rcl}
y_{n,w} + x_{n,w} - y_{n-1,w} - x_{n,w-1} &=& 0.
\end{array}\\[1mm]
\textbf{At the destination } (N,W):\quad & \begin{array}{rcl}
-\, y_{N-1,W} - x_{N,W-1} &=& -1 \quad \Longrightarrow \quad y_{N-1,W}+ x_{N,W-1} = 1.
\end{array}
\end{align*}
\]

This complete model accurately represents the Transportation and Logistics problem where the delivery person selects a sequence of north or west moves on an N \times W grid (with N-1 north steps and W-1 west steps required) to minimize the total travel time, taking into account the time cost on each block as specified by the parameters NorthTime and WestTime. The model is feasible (a valid path exists) and bounded, and its formulation is fully self-contained.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    N = 3  # Number of east-west streets (rows)
    W = 3  # Number of north-south streets (columns)
    # WestTime indexed as (n, w) with n=1..N, w=1..W-1
    WestTime = {
        (1, 1): 3.5, (1, 2): 4.5,
        (2, 1): 4,   (2, 2): 4,
        (3, 1): 5,   (3, 2): 4,
    }
    # NorthTime indexed as (n, w) with n=1..N-1, w=1..W
    NorthTime = {
        (1, 1): 10, (1, 2): 10, (1, 3): 9,
        (2, 1): 9,  (2, 2): 9,  (2, 3): 12,
    }
    
    # Create solver using CBC mixed integer programming solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables:
    # x[n,w] = 1 if moving west from (n, w) to (n, w+1)
    x = {}
    for n in range(1, N + 1):
        for w in range(1, W):  # w=1,...,W-1
            x[(n, w)] = solver.IntVar(0, 1, f"x_{n}_{w}")
    # y[n,w] = 1 if moving north from (n, w) to (n+1, w)
    y = {}
    for n in range(1, N):
        for w in range(1, W + 1):  # w=1,...,W
            y[(n, w)] = solver.IntVar(0, 1, f"y_{n}_{w}")

    # Objective: minimize total travel time
    objective = solver.Objective()
    # Add westward travel times
    for key, var in x.items():
        time = WestTime[key]
        objective.SetCoefficient(var, time)
    # Add northward travel times
    for key, var in y.items():
        time = NorthTime[key]
        objective.SetCoefficient(var, time)
    objective.SetMinimization()

    # Flow conservation constraints:
    # Alternative formulation as described.

    # At the origin (1,1): y[1,1] + x[1,1] = 1.
    solver.Add(y[(1, 1)] + x[(1, 1)] == 1)

    # For nodes on the first row (1,w), w = 2,...,W-1.
    for w in range(2, W):
        # Constraint: y(1,w) + x(1,w) - x(1,w-1) = 0.
        solver.Add(y[(1, w)] + x[(1, w)] - x[(1, w - 1)] == 0)

    # For nodes on the first column (n,1), n = 2,...,N-1.
    for n in range(2, N):
        # Constraint: y(n,1) + x(n,1) - y(n-1,1) = 0.
        solver.Add(y[(n, 1)] + x[(n, 1)] - y[(n - 1, 1)] == 0)

    # For interior nodes (n,w), n = 2,...,N-1 and w = 2,...,W-1.
    for n in range(2, N):
        for w in range(2, W):
            # Constraint: y(n,w) + x(n,w) - y(n-1,w) - x(n,w-1) = 0.
            solver.Add(y[(n, w)] + x[(n, w)] - y[(n - 1, w)] - x[(n, w - 1)] == 0)

    # At the destination (N,W): y[N-1,W] + x[N,W-1] = 1.
    solver.Add(y[(N - 1, W)] + x[(N, W - 1)] == 1)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print(f"Total travel time: {solver.Objective().Value()}")
        print("Decisions:")
        # Print all x variables where decision is 1.
        for n in range(1, N + 1):
            for w in range(1, W):
                if x[(n, w)].solution_value() > 0.5:
                    print(f"  At intersection ({n},{w}): move WEST to ({n},{w+1}) with time {WestTime[(n, w)]}")
        # Print all y variables where decision is 1.
        for n in range(1, N):
            for w in range(1, W + 1):
                if y[(n, w)].solution_value() > 0.5:
                    print(f"  At intersection ({n},{w}): move NORTH to ({n+1},{w}) with time {NorthTime[(n, w)]}")
    elif status == pywraplp.Solver.INFEASIBLE:
        print("The problem is infeasible.")
    else:
        print("The solver did not find an optimal solution.")

if __name__ == '__main__':
    main()