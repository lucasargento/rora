# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{\underline{Indices and Parameters:}}\\[1mm]
& t \in \{1,\dots,T\} & \text{(time periods)}\\[0.5mm]
& k \in \{1,\dots,K\} & \text{(generator types)}\\[0.5mm]
& Demand_t \in \mathbb{R}_+ & \text{Electricity demand in period } t\\[0.5mm]
& NumGenerator_k \in \mathbb{Z}_+ & \text{Number of available generators of type } k\\[0.5mm]
& MinLevel_k \in \mathbb{R}_+ & \text{Minimum production (MW) of type } k\text{ when on}\\[0.5mm]
& MaxLevel_k \in \mathbb{R}_+ & \text{Maximum production (MW) of type } k\\[0.5mm]
& RunCost_k \in \mathbb{R}_+ & \text{Hourly cost of running a generator of type } k \text{ at its minimum level}\\[0.5mm]
& ExtraCost_k \in \mathbb{R}_+ & \text{Extra hourly cost per MW above the minimum level for type } k\\[0.5mm]
& StartCost_k \in \mathbb{R}_+ & \text{Cost of starting up a generator of type } k\\[2mm]
\textbf{\underline{Decision Variables:}}\\[1mm]
& n_{k,t} \in \{0,1,2,\dots,NumGenerator_k\} & \text{Number of generators of type } k \text{ turned on in period } t,\\[0.5mm]
& p_{k,t} \ge 0 & \text{Additional production (MW) above the minimum from generators of type } k \text{ in period } t,\\[0.5mm]
& s_{k,t} \in \mathbb{Z}_+ & \text{Number of generators of type } k started up in period } t.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{\underline{Objective Function:}}\\[1mm]
\text{Minimize } Z &=& \sum_{t=1}^{T} \sum_{k=1}^{K} \Bigl[
    n_{k,t}\, \text{RunCost}_k  + \, p_{k,t}\, \text{ExtraCost}_k  + \, s_{k,t}\, \text{StartCost}_k
\Bigr].
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{\underline{Constraints:}}\\[2mm]
\text{(1) Demand Satisfaction:} & & \forall\, t=1,\dots,T: \\[0.5mm]
\quad \sum_{k=1}^{K} \Bigl( n_{k,t}\,\text{MinLevel}_k + p_{k,t} \Bigr) &\ge& Demand_t. \\[3mm]
\text{(2) Production Limits per Generator Type:} & & \forall\, k=1,\dots,K,\; t=1,\dots,T: \\[0.5mm]
\quad n_{k,t}\,\text{MinLevel}_k + p_{k,t} &\le& n_{k,t}\,\text{MaxLevel}_k, \\[0.5mm]
\quad \Rightarrow\quad p_{k,t} &\le& n_{k,t}\,\Bigl( \text{MaxLevel}_k - \text{MinLevel}_k \Bigr). \\[3mm]
\text{(3) Availability of Generators:} & & \forall\, k=1,\dots,K,\; t=1,\dots,T: \\[0.5mm]
\quad n_{k,t} &\le& NumGenerator_k. \\[3mm]
\text{(4) Startup Constraints:} & & \forall\, k=1,\dots,K: \\[0.5mm]
\quad \text{For } t=1:\quad s_{k,1} &=& n_{k,1}, \\[0.5mm]
\quad \text{For } t=2,\dots,T:\quad s_{k,t} &\ge& n_{k,t} - n_{k,t-1}. \\[3mm]
\text{(5) Nonnegativity and Integrality:} & & \forall\, k=1,\dots,K,\; t=1,\dots,T: \\[0.5mm]
\quad n_{k,t} &\in& \{0,1,2,\dots,NumGenerator_k\}, \\[0.5mm]
\quad p_{k,t} &\ge& 0, \\[0.5mm]
\quad s_{k,t} &\in& \mathbb{Z}_+.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{\underline{Full Formulation:}}
\end{array}
\]

\[
\begin{aligned}
\textbf{Minimize } Z =\; & \sum_{t=1}^{T} \sum_{k=1}^{K} \Bigl[ n_{k,t}\, \text{RunCost}_k + p_{k,t}\, \text{ExtraCost}_k + s_{k,t}\, \text{StartCost}_k \Bigr] \\[1mm]
\textbf{subject to:}\quad
& \sum_{k=1}^{K} \Bigl( n_{k,t}\,\text{MinLevel}_k + p_{k,t} \Bigr) \ge Demand_t, \quad \forall\, t=1,\dots,T, \\[1mm]
& p_{k,t} \le n_{k,t}\,\Bigl( \text{MaxLevel}_k - \text{MinLevel}_k \Bigr), \quad \forall\, k=1,\dots,K,\; t=1,\dots,T, \\[1mm]
& n_{k,t} \le NumGenerator_k, \quad \forall\, k=1,\dots,K,\; t=1,\dots,T, \\[1mm]
& s_{k,1} = n_{k,1}, \quad \forall\, k=1,\dots,K, \\[1mm]
& s_{k,t} \ge n_{k,t} - n_{k,t-1}, \quad \forall\, k=1,\dots,K,\; t=2,\dots,T, \\[1mm]
& n_{k,t} \in \{0, 1, 2, \ldots, NumGenerator_k\}, \quad \forall\, k=1,\dots,K,\; t=1,\dots,T, \\[1mm]
& p_{k,t} \ge 0, \quad \forall\, k=1,\dots,K,\; t=1,\dots,T, \\[1mm]
& s_{k,t} \in \mathbb{Z}_+, \quad \forall\, k=1,\dots,K,\; t=1,\dots,T.
\end{aligned}
\]

This complete formulation accurately represents the real‐world problem from the energy and natural resources context. It determines for each generator type k and each period t the number of generators activated (nₖ,ₜ), the extra production above the minimum level (pₖ,ₜ), and the number of start-ups (sₖ,ₜ), ensuring the demand is met in every period while minimizing the total cost of running and starting up generators.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Data
    # There are 5 time periods because Demand has 5 elements.
    Demand = [15000, 30000, 25000, 40000, 27000]
    T = len(Demand)
    NumGenerator = [12, 10, 5]
    MinLevel = [850, 1250, 1500]
    MaxLevel = [2000, 1750, 4000]
    RunCost = [1000, 2600, 3000]
    ExtraCost = [2.0, 1.3, 3.0]
    StartCost = [2000, 1000, 500]
    K = len(NumGenerator)
    
    # Create solver: use CBC Mixed Integer Programming Solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print('Solver not created.')
        return

    # Decision variables
    # n[k][t]: number of generators of type k on in period t.
    n = {}
    # p[k][t]: extra production above minimum for generator type k in period t.
    p = {}
    # s[k][t]: number of generators of type k started up in period t.
    s = {}
    
    for k in range(K):
        for t in range(T):
            n[k, t] = solver.IntVar(0, NumGenerator[k], f'n_{k}_{t}')
            # p is continuous variable (>=0); production can be fractional.
            p[k, t] = solver.NumVar(0.0, solver.infinity(), f'p_{k}_{t}')
            s[k, t] = solver.IntVar(0, NumGenerator[k], f's_{k}_{t}')
    
    # Objective: Minimize total cost
    objective = solver.Objective()
    for k in range(K):
        for t in range(T):
            objective.SetCoefficient(n[k, t], RunCost[k])
            objective.SetCoefficient(p[k, t], ExtraCost[k])
            objective.SetCoefficient(s[k, t], StartCost[k])
    objective.SetMinimization()

    # Constraint 1: Demand Satisfaction for each period t
    for t in range(T):
        constraint_expr = solver.Sum([n[k, t] * MinLevel[k] + p[k, t] for k in range(K)])
        solver.Add(constraint_expr >= Demand[t])
        
    # Constraint 2: Production limits for each generator type and period
    for k in range(K):
        for t in range(T):
            max_extra = MaxLevel[k] - MinLevel[k]
            solver.Add(p[k, t] <= n[k, t] * max_extra)
    
    # Constraint 3: Availability of generators
    for k in range(K):
        for t in range(T):
            solver.Add(n[k, t] <= NumGenerator[k])
    
    # Constraint 4: Startup constraints
    for k in range(K):
        # For t = 0: s[k,0] = n[k,0]
        solver.Add(s[k, 0] == n[k, 0])
        # For t >= 1: s[k,t] >= n[k,t] - n[k,t-1]
        for t in range(1, T):
            solver.Add(s[k, t] >= n[k, t] - n[k, t-1])
    
    # Solve the model
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal objective value: {solver.Objective().Value()}')
        for t in range(T):
            print(f'Period {t + 1}: Demand = {Demand[t]}')
            for k in range(K):
                n_val = n[k, t].solution_value()
                p_val = p[k, t].solution_value()
                s_val = s[k, t].solution_value()
                print(f'  Generator type {k + 1}: on = {n_val}, extra production = {p_val}, startups = {s_val}')
            print()
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it may not be optimal.')
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()