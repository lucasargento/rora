# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Parameters:} & & & \\[1mm]
N &\in& \mathbb{Z}_{+} & \text{number of currencies} \\[1mm]
\text{Start}_i &\in& \mathbb{R}_{+} & \text{initial units held of currency } i,\quad i=1,\ldots,N \\[1mm]
\text{Limit}_i &\in& \mathbb{R}_{+} & \text{maximum total units of currency } i \text{ allowed to be exchanged (involved in transactions)} \\[1mm]
\text{Rate}_{i,j} &\in& \mathbb{R}_{+} & \text{exchange rate converting one unit of currency } i \text{ to currency } j,\quad i,j=1,\ldots,N \\[1mm]
r_i &\in& \mathbb{R}_{+} & \text{conversion factor from currency } i \text{ to the numeraire (say, currency 1), with } r_1=1\text{ and } r_i=\text{Rate}_{i,1}\text{ for } i\ge2 \\[2mm]
\textbf{Decision Variables:} & & & \\[1mm]
x_{ij} &\ge& 0,\quad \forall\, i,j\in\{1,\ldots,N\},\; i\neq j 
& \begin{array}{l}\text{Amount of currency } i \text{ exchanged into currency } j. \\
\text{(No “exchange” is defined for } i=j\text{.)}\end{array} \\[2mm]
u_i &\ge& 0,\quad \forall\, i\in\{1,\ldots,N\} 
& \text{Final holdings (end‐of–day amount) in currency } i. \\[2mm]
\textbf{Model:} & & & \\[1mm]
\textbf{(P)}\quad \max_{\,x,u}\quad & & Z = \displaystyle \sum_{i=1}^{N} r_i\, u_i & \text{(Final wealth measured in the numeraire)} \\[2mm]
\text{s.t.}\quad & & & \\[1mm]
\text{Flow Balance:} &\quad u_i &= \text{Start}_i - \displaystyle \sum_{\substack{j=1 \\ j\neq i}}^{N} x_{ij} + \displaystyle \sum_{\substack{j=1 \\ j\neq i}}^{N} \text{Rate}_{j,i}\, x_{ji}, \quad & i=1,\ldots,N, \quad (1) \\[2mm]
\text{Exchange Limits:} &\quad \displaystyle \sum_{\substack{j=1 \\ j\neq i}}^{N} \; x_{ij} \;+\; \displaystyle \sum_{\substack{j=1 \\ j\neq i}}^{N}\; \text{Rate}_{j,i}\, x_{ji} &\le& \text{Limit}_i,\quad i=1,\ldots,N,\quad (2) \\[2mm]
\text{Nonnegativity:} &\quad x_{ij} &\ge& 0,\quad \forall\, i,j \text{ with } i\neq j, \quad (3) \\[1mm]
&\quad u_i &\ge& 0,\quad i=1,\ldots,N.\quad (4)
\end{array}
\]

\vspace{2mm}
\textbf{Explanation:}

1. Decision Variables:  
 • For each ordered pair of distinct currencies (i,j), the variable 
  \( x_{ij} \) represents the amount of currency \( i \) that is exchanged into currency \( j \).  
 • For each currency \( i \), the auxiliary variable \( u_i \) denotes the final amount held in currency \( i \) after all transactions.

2. Objective Function:  
 We maximize the final wealth expressed in a chosen numeraire (taken here as currency 1).  
 The conversion factors \( r_i \) (with \( r_1=1 \) and for \( i\ge2 \), \( r_i=\text{Rate}_{i,1} \)) convert the end‐of–day holdings to the numeraire.  
 Thus, the objective is  
  \[
  \max \; Z = \sum_{i=1}^{N} r_i\, u_i.
  \]

3. Constraints:  
 (a) The Flow Balance constraints (1) ensure that for each currency \( i \) the final holding \( u_i \) equals the initial holding minus the amount exchanged out plus the correctly “rated” incoming exchanges.  
 (b) The Exchange Limits constraints (2) capture the regulation that the total amount of currency \( i \) that is “involved” in a transaction (either as the currency being exchanged or as the currency received, where the received amount is measured in units of currency \( i \) via the rate conversion) does not exceed \( \text{Limit}_i \).  
 (c) Nonnegativity constraints (3)–(4) ensure that no exchange or final holding is negative.

4. Feasibility and Boundedness:  
 The available resources (given by \( \text{Start}_i \)) and the imposed upper limits \( \text{Limit}_i \) on transactions guarantee that the decision variables are bounded and that the problem is feasible under proper data (for example, if the limits are sufficiently high to allow some beneficial conversion while adhering to no–arbitrage conditions).

This full formulation accurately reflects the original finance and investment problem and is ready for implementation in a solver (e.g. via ortools).  
'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def main():
    # Create the solver (using GLOP for linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Problem Data
    N = 3
    Start = [100.0, 50.0, 200.0]
    Limit = [1000.0, 200.0, 3000.0]
    Rate = [
        [0.99, 0.9,  1.02],
        [0.95, 0.99, 0.92],
        [0.9,  0.91, 0.99]
    ]
    # Conversion factors from currency i to numeraire (currency 1 assumed)
    r = [1.0] + [Rate[i][0] for i in range(1, N)]  # r[0]=1, r[i]=Rate[i][0] for i>=1

    # Decision variables:
    # x[i][j] for i != j: amount of currency i exchanged into currency j
    x = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                x[(i, j)] = solver.NumVar(0.0, solver.infinity(), f'x_{i}_{j}')
    # u[i]: final holdings in currency i
    u = {}
    for i in range(N):
        u[i] = solver.NumVar(0.0, solver.infinity(), f'u_{i}')

    # Flow Balance Constraints:
    # u_i = Start_i - sum_{j != i} x_{i,j} + sum_{j != i} Rate_{j,i} * x_{j,i}
    for i in range(N):
        outgoing = solver.Sum([x[(i, j)] for j in range(N) if i != j])
        incoming = solver.Sum([Rate[j][i] * x[(j, i)] for j in range(N) if i != j])
        solver.Add(u[i] == Start[i] - outgoing + incoming)

    # Exchange Limits Constraints:
    # sum_{j != i} x_{i,j} + sum_{j != i} Rate_{j,i} * x_{j,i} <= Limit_i
    for i in range(N):
        outgoing = solver.Sum([x[(i, j)] for j in range(N) if i != j])
        incoming = solver.Sum([Rate[j][i] * x[(j, i)] for j in range(N) if i != j])
        solver.Add(outgoing + incoming <= Limit[i])

    # Objective: Maximize sum_{i=1}^{N} r_i * u_i  (r[0]=1, r[1]=Rate[1][0], r[2]=Rate[2][0])
    objective = solver.Sum([r[i] * u[i] for i in range(N)])
    solver.Maximize(objective)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print(f'Optimal objective value: {solver.Objective().Value()}')
        for i in range(N):
            print(f'u[{i}] = {u[i].solution_value()}')
        for i in range(N):
            for j in range(N):
                if i != j:
                    print(f'x[{i}][{j}] = {x[(i,j)].solution_value()}')
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()