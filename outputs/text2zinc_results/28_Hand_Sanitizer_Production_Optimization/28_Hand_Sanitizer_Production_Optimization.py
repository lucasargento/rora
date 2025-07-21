# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Decision Variables:} \\
\quad L &\in& \mathbb{Z}, & L \ge 1 \quad \text{(number of liquid sanitizers produced)} \\
\quad F &\in& \mathbb{Z}, & F \ge 1 \quad \text{(number of foam sanitizers produced)} \\[1mm]
\textbf{Parameters:} \\
\quad w_L &=& 40, & \text{(water required per liquid sanitizer)} \\
\quad a_L &=& 50, & \text{(alcohol required per liquid sanitizer)} \\
\quad w_F &=& 60, & \text{(water required per foam sanitizer)} \\
\quad a_F &=& 40, & \text{(alcohol required per foam sanitizer)} \\
\quad W_{\text{total}} &=& 2000, & \text{(total available water)} \\
\quad A_{\text{total}} &=& 2100, & \text{(total available alcohol)} \\
\quad h_L &=& 30, & \text{(hands cleaned per liquid sanitizer)} \\
\quad h_F &=& 20, & \text{(hands cleaned per foam sanitizer)} \\
\quad L_{\text{max}} &=& 30, & \text{(maximum liquid sanitizers allowed)} \\[1mm]
\textbf{Mathematical Model:} \\[1mm]
\text{maximize} \quad & Z = & h_L L + h_F F &= 30L + 20F \\[1mm]
\text{subject to} \quad 
& w_L L + w_F F &\le &\; W_{\text{total}} \quad \Longrightarrow \quad 40L + 60F \le 2000, \\[1mm]
& a_L L + a_F F &\le &\; A_{\text{total}} \quad \Longrightarrow \quad 50L + 40F \le 2100, \\[1mm]
& L &\le &\; L_{\text{max}} \quad \Longrightarrow \quad L \le 30, \\[1mm]
& F &\ge &\; L + 1, \quad \text{(ensure more foam sanitizers than liquid sanitizers)} \\[1mm]
& L,\, F &\ge &\; 1, \quad \text{and } L,\, F \in \mathbb{Z} \quad \text{(non-trivial production for both products).}
\end{array}
\]'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver: using CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not available.")
        return
        
    # Problem Parameters
    water_per_liquid = 40
    alcohol_per_liquid = 50
    water_per_foam = 60
    alcohol_per_foam = 40
    
    total_water = 2000
    total_alcohol = 2100
    
    hands_per_liquid = 30
    hands_per_foam = 20
    
    max_liquid = 30
    
    # Decision Variables: L: number of liquid sanitizers, F: number of foam sanitizers
    L = solver.IntVar(1, max_liquid, 'L')  # L >= 1 and L <= max_liquid
    # Upper bound for F can be set as large, using total resource constraints can be limited, set to total_water//water_per_foam
    F = solver.IntVar(1, total_water // water_per_foam, 'F')  # F >= 1
    
    # Constraints
    # Water constraint: 40L + 60F <= 2000
    solver.Add(water_per_liquid * L + water_per_foam * F <= total_water)
    
    # Alcohol constraint: 50L + 40F <= 2100
    solver.Add(alcohol_per_liquid * L + alcohol_per_foam * F <= total_alcohol)
    
    # F must be at least L + 1 (more foam sanitizers than liquid sanitizers)
    solver.Add(F >= L + 1)
    
    # Objective: maximize cleaning capacity = 30L + 20F
    objective = solver.Objective()
    objective.SetCoefficient(L, hands_per_liquid)
    objective.SetCoefficient(F, hands_per_foam)
    objective.SetMaximization()
    
    # Solve the problem
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        print('Number of liquid sanitizers (L):', int(L.solution_value()))
        print('Number of foam sanitizers (F):', int(F.solution_value()))
        print('Maximum number of hands cleaned:', int(objective.Value()))
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it might not be optimal.")
        print('Number of liquid sanitizers (L):', int(L.solution_value()))
        print('Number of foam sanitizers (F):', int(F.solution_value()))
        print('Hands cleaned:', int(objective.Value()))
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()