# Mathematical Formulation:
'''\[
\begin{array}{rll}
\textbf{Decision Variables:} & & \\[1mm]
x_N & = \text{Acres fished using the net method} & (x_N \ge 0)\\[1mm]
x_L & = \text{Acres fished using the fishing line method} & (x_L \ge 0)\\[2mm]
\textbf{Parameters:} & & \\[1mm]
\text{TotalAcres} & = 250, & \text{Total available lake acres}\\[1mm]
\text{TotalBait} & = 800, & \text{Total available bait}\\[1mm]
\text{MaxPain} & = 350, & \text{Maximum tolerable pain}\\[1mm]
\text{FishPerNetAcre} & = 8, & \text{Fish caught per acre using a net}\\[1mm]
\text{FishPerLineAcre} & = 5, & \text{Fish caught per acre using a fishing line}\\[1mm]
\text{BaitPerNetAcre} & = 4, & \text{Bait required per acre using a net}\\[1mm]
\text{BaitPerLineAcre} & = 3, & \text{Bait required per acre using a fishing line}\\[1mm]
\text{PainPerNetAcre} & = 2, & \text{Pain caused per acre using a net}\\[1mm]
\text{PainPerLineAcre} & = 1, & \text{Pain caused per acre using a fishing line}\\[2mm]
\textbf{Mathematical Model:} & & \\[1mm]
\text{Maximize} \quad & Z = 8x_N + 5x_L \\[2mm]
\text{Subject to:} \quad & x_N + x_L \le 250 \quad & \text{(Lake area constraint)} \\[1mm]
& 4x_N + 3x_L \le 800 \quad & \text{(Bait consumption constraint)} \\[1mm]
& 2x_N + x_L \le 350 \quad & \text{(Pain tolerance constraint)} \\[1mm]
& x_N \ge 0, \quad x_L \ge 0 \quad & \text{(Non-negativity constraints)}
\end{array}
\]

This formulation fully captures the decision variables, the objective (maximizing total fish caught), and all the constraints reflecting the limited lake area, bait, and maximum tolerable pain, ensuring that the problem is both feasible and bounded.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the linear solver using GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Define decision variables:
    x_N = solver.NumVar(0.0, solver.infinity(), 'x_N')  # Acres using net
    x_L = solver.NumVar(0.0, solver.infinity(), 'x_L')  # Acres using fishing line

    # Problem Parameters:
    TotalAcres = 250
    TotalBait = 800
    MaxPain = 350

    FishPerNetAcre = 8
    FishPerLineAcre = 5

    BaitPerNetAcre = 4
    BaitPerLineAcre = 3

    PainPerNetAcre = 2
    PainPerLineAcre = 1

    # Constraints:
    # Lake area constraint: x_N + x_L <= TotalAcres
    solver.Add(x_N + x_L <= TotalAcres)
    
    # Bait consumption constraint: 4*x_N + 3*x_L <= TotalBait
    solver.Add(BaitPerNetAcre * x_N + BaitPerLineAcre * x_L <= TotalBait)

    # Pain tolerance constraint: 2*x_N + x_L <= MaxPain
    solver.Add(PainPerNetAcre * x_N + PainPerLineAcre * x_L <= MaxPain)

    # Objective Function: Maximize total fish caught = 8*x_N + 5*x_L
    solver.Maximize(FishPerNetAcre * x_N + FishPerLineAcre * x_L)

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Optimal fish caught = ', solver.Objective().Value())
        print('Acres fished using net = ', x_N.solution_value())
        print('Acres fished using fishing line = ', x_L.solution_value())
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it is not proven to be optimal.')
        print('Fish caught = ', solver.Objective().Value())
        print('Acres fished using net = ', x_N.solution_value())
        print('Acres fished using fishing line = ', x_L.solution_value())
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()