# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Decision Variables:} & & & \\
x & = & \text{Number of circular tables to set up} & x \in \mathbb{Z}_{\ge 1}, \\
y & = & \text{Number of rectangular tables to set up} & y \in \mathbb{Z}_{\ge 1}. \\[1em]

\textbf{Parameters:} & & & \\
\text{ParticipantsPerCircular} &=& 5, & \quad \text{Participants at a circular table,} \\
\text{ParticipantsPerRectangular} &=& 4, & \quad \text{Participants at a rectangular table,} \\
\\
\text{BoardsPerCircular} &=& 4, & \quad \text{Poster boards at a circular table,} \\
\text{BoardsPerRectangular} &=& 4, & \quad \text{Poster boards at a rectangular table,} \\
\\
\text{GuestsPerCircular} &=& 8, & \quad \text{Guests accommodated by a circular table,} \\
\text{GuestsPerRectangular} &=& 12, & \quad \text{Guests accommodated by a rectangular table,} \\
\\
\text{SpacePerCircular} &=& 15, & \quad \text{Space (in square units) required per circular table,} \\
\text{SpacePerRectangular} &=& 20, & \quad \text{Space (in square units) required per rectangular table,} \\
\\
\text{TotalSpace} &=& 1900, & \quad \text{Total available space,} \\
\text{MinParticipants} &=& 500, & \quad \text{Minimum number of participants required,} \\
\text{MinBoards} &=& 300, & \quad \text{Minimum number of poster boards required.} \\[1em]

\textbf{Objective Function:} & & & \\
\text{Maximize} \quad Z &=& 8x + 12y, & \quad \text{(Total number of guests)} \\[1em]

\textbf{Constraints:} & & & \\
\text{(1) Space Constraint:} & 15x + 20y & \leq & 1900, \\[0.5em]
\text{(2) Participant Constraint:} & 5x + 4y & \geq & 500, \\[0.5em]
\text{(3) Poster Board Constraint:} & 4x + 4y & \geq & 300. \\[1em]

\textbf{Complete Mathematical Formulation:} & & & \\[0.5em]
\boxed{
\begin{aligned}
&\text{Maximize} \quad && Z = 8x + 12y, \\
&\text{subject to} \quad && 15x + 20y \le 1900, \\
& && 5x + 4y \ge 500, \\
& && 4x + 4y \ge 300, \\
& && x \ge 1,\quad y \ge 1, \\
& && x,y \in \mathbb{Z}.
\end{aligned}
}
\end{array}
\]

This formulation fully represents the problem with:
1. Decision variables defined as nonnegative integers (with a minimum of 1 each to avoid trivial scenarios),
2. An objective function that maximizes the total number of guests,
3. Constraints on total space available, minimum participants, and minimum poster boards needed.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the MILP solver with the CBC backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x = circular tables, y = rectangular tables (integer >= 1)
    x = solver.IntVar(1, solver.infinity(), 'circular_tables')
    y = solver.IntVar(1, solver.infinity(), 'rectangular_tables')

    # Parameters
    ParticipantsPerCircular = 5
    ParticipantsPerRectangular = 4
    BoardsPerCircular = 4
    BoardsPerRectangular = 4
    GuestsPerCircular = 8
    GuestsPerRectangular = 12
    SpacePerCircular = 15
    SpacePerRectangular = 20
    TotalSpace = 1900
    MinParticipants = 500
    MinBoards = 300

    # Constraints
    # (1) Space Constraint: 15x + 20y <= 1900
    solver.Add(SpacePerCircular * x + SpacePerRectangular * y <= TotalSpace)
    
    # (2) Participant Constraint: 5x + 4y >= 500
    solver.Add(ParticipantsPerCircular * x + ParticipantsPerRectangular * y >= MinParticipants)
    
    # (3) Poster Board Constraint: 4x + 4y >= 300
    solver.Add(BoardsPerCircular * x + BoardsPerRectangular * y >= MinBoards)

    # Objective: Maximize total guests = 8x + 12y
    objective = solver.Objective()
    objective.SetCoefficient(x, GuestsPerCircular)
    objective.SetCoefficient(y, GuestsPerRectangular)
    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Solution:')
        print(f'Number of circular tables (x): {x.solution_value()}')
        print(f'Number of rectangular tables (y): {y.solution_value()}')
        print(f'Total guests (objective): {objective.Value()}')
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()