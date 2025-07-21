# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:}\quad & a = 1,\dots,A \quad (\text{alloys}),\qquad s = 1,\dots,S \quad (\text{steel types})\\[1mm]
\textbf{Decision Variables:}\quad & x_{a,s} \ge 0 \quad \text{(tons of alloy } a \text{ used in steel type } s\text{)},\\[1mm]
& t_s \ge 0 \quad \text{(tons of steel type } s \text{ produced)}\\[2mm]
\textbf{Objective Function:}\quad & \text{Maximize Profit } Z \text{ defined as} \\[1mm]
& Z = \sum_{s=1}^S (\text{SteelPrice}_s \cdot t_s) - \sum_{a=1}^A \sum_{s=1}^S (\text{AlloyPrice}_a \cdot x_{a,s}) \\[2mm]
\textbf{Subject to:}\\[1mm]
\text{(1) Steel Composition:} \quad & \sum_{a=1}^{A} x_{a,s} = t_s, && \forall\, s=1,\dots,S, \quad \text{(all constituents sum to total steel)} \\[1mm]
\text{(2) Carbon Content Requirements:} \quad & \sum_{a=1}^{A} (\text{CarbonContent}_a \cdot x_{a,s}) \ge \text{CarbonMin}_s \cdot t_s, && \forall\, s=1,\dots,S, \\[1mm]
\text{(3) Nickel Content Limits:} \quad & \sum_{a=1}^{A} (\text{NickelContent}_a \cdot x_{a,s}) \le \text{NickelMax}_s \cdot t_s, && \forall\, s=1,\dots,S, \\[1mm]
\text{(4) Alloy 1 Limitation:} \quad & x_{1,s} \le 0.4\, t_s, && \forall\, s=1,\dots,S, \quad \text{(at most 40\% of alloy 1 in any steel)} \\[1mm]
\text{(5) Alloy Availability:} \quad & \sum_{s=1}^{S} x_{a,s} \le \text{AvailableAlloy}_a, && \forall\, a=1,\dots,A, \\[1mm]
\text{(6) Nontrivial Production (Product Mix):} \quad & t_s \ge \varepsilon, && \forall\, s=1,\dots,S, \quad (\varepsilon > 0 \text{ is a small constant}) \\[1mm]
\text{(7) Nonnegativity:} \quad & x_{a,s} \ge 0, \quad t_s \ge 0, && \forall\, a=1,\dots,A,\; s=1,\dots,S.
\end{align*}

\textbf{Parameters (for clarity):}
\[
\begin{array}{rcl}
A &=& \text{Total number of alloys (here } A=3\text{)}\\[1mm]
S &=& \text{Total number of steel types (here } S=2\text{)}\\[1mm]
\text{AvailableAlloy}_a &:& \text{tons available of alloy } a,\quad \text{e.g., } [40,\,50,\,80]\\[1mm]
\text{CarbonContent}_a &:& \text{percentage of carbon in alloy } a,\quad \text{e.g., } [3,\;4,\;3.5]\\[1mm]
\text{NickelContent}_a &:& \text{percentage of nickel in alloy } a,\quad \text{e.g., } [1,\;1.5,\;1.8]\\[1mm]
\text{AlloyPrice}_a &:& \text{purchase price per ton of alloy } a,\quad \text{e.g., } [380,\;400,\;440]\\[1mm]
\text{SteelPrice}_s &:& \text{selling price per ton of steel type } s,\quad \text{e.g., } [650,\;600]\\[1mm]
\text{CarbonMin}_s &:& \text{minimum required carbon percentage for steel type } s,\quad \text{e.g., } [3.6,\;3.4]\\[1mm]
\text{NickelMax}_s &:& \text{maximum allowed nickel percentage for steel type } s,\quad \text{e.g., } [1.5,\;1.7]
\end{array}
\]

This formulation is a full and exact representation of the manufacturing and production problem, ensuring that the profit is maximized subject to alloy availability, steel quality requirements, a mix constraint to prevent trivial solutions, and the specific limitation on the amount of alloy 1 in any steel type.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def main():
    # Data
    A = 3
    S = 2
    AvailableAlloy = [40, 50, 80]
    CarbonContent = [3, 4, 3.5]
    NickelContent = [1, 1.5, 1.8]
    AlloyPrice = [380, 400, 440]
    SteelPrice = [650, 600]
    CarbonMin = [3.6, 3.4]
    NickelMax = [1.5, 1.7]
    epsilon = 1e-3  # small constant to avoid trivial production
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision Variables
    # x[a][s]: tons of alloy a used in steel s
    x = {}
    for a in range(A):
        for s in range(S):
            x[a, s] = solver.NumVar(0.0, solver.infinity(), f'x_{a}_{s}')
            
    # t[s]: tons of steel produced for steel type s
    t = {}
    for s in range(S):
        t[s] = solver.NumVar(epsilon, solver.infinity(), f't_{s}')

    # Constraints
    # (1) Steel composition: sum_a x[a,s] == t[s] for each s
    for s in range(S):
        constraint_expr = solver.Sum([x[a, s] for a in range(A)])
        solver.Add(constraint_expr == t[s])
    
    # (2) Carbon content: sum_a (CarbonContent[a] * x[a,s]) >= CarbonMin[s] * t[s]
    for s in range(S):
        constraint_expr = solver.Sum([CarbonContent[a] * x[a, s] for a in range(A)])
        solver.Add(constraint_expr >= CarbonMin[s] * t[s])
    
    # (3) Nickel content: sum_a (NickelContent[a] * x[a,s]) <= NickelMax[s] * t[s]
    for s in range(S):
        constraint_expr = solver.Sum([NickelContent[a] * x[a, s] for a in range(A)])
        solver.Add(constraint_expr <= NickelMax[s] * t[s])
    
    # (4) Alloy 1 limitation: x[0,s] <= 0.4 * t[s] for each s (Alloy 1 is index 0)
    for s in range(S):
        solver.Add(x[0, s] <= 0.4 * t[s])
    
    # (5) Alloy availability: for each alloy a, sum_s x[a,s] <= AvailableAlloy[a]
    for a in range(A):
        constraint_expr = solver.Sum([x[a, s] for s in range(S)])
        solver.Add(constraint_expr <= AvailableAlloy[a])
    
    # Objective: Maximize profit
    # Profit = sum_s (SteelPrice[s] * t[s]) - sum_a sum_s (AlloyPrice[a] * x[a,s])
    profit_expr = solver.Sum([SteelPrice[s] * t[s] for s in range(S)])
    cost_expr = solver.Sum([AlloyPrice[a] * x[a, s] for a in range(A) for s in range(S)])
    solver.Maximize(profit_expr - cost_expr)
    
    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found!")
        print("Objective value =", solver.Objective().Value())
        for s in range(S):
            print(f"Steel type {s+1}:")
            print("  Production (tons):", t[s].solution_value())
            for a in range(A):
                print(f"   Alloy {a+1} used (tons):", x[a, s].solution_value())
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()