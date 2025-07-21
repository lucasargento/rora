# Problem Description:
'''Problem description: In a science fair, there are two types of tables that can be used to display the children’s science experiments. At the circular tables, 4 poster boards and 5 participants can fit around the table to cater to 8 guests. At the rectangular tables, 4 poster boards and 4 participants can fit around the table to cater to 12 guests. However, each circular table takes up 15 units of space while each rectangular table takes up 20 units of space. The science fair has must be able to fit at least 500 participants and 300 poster boards. If the science fair has available 1900 units of space, how many of each type of table should be set up to maximize the number of catered guests?

Expected Output Schema:
{
  "variables": {
    "CircularTables": "float",
    "RectangularTables": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of table types = {Circular, Rectangular}

Parameters:
- GuestsPerTable: number of guests catered per table.
  • Circular: 8 guests per table
  • Rectangular: 12 guests per table
- ParticipantsPerTable: number of participants that can be accommodated per table.
  • Circular: 5 participants per table
  • Rectangular: 4 participants per table
- PosterBoardsPerTable: number of poster boards that can be accommodated per table.
  • Circular: 4 poster boards per table
  • Rectangular: 4 poster boards per table
- TableSpace:
  • Circular: 15 space units per table
  • Rectangular: 20 space units per table
- TotalSpace: total available space = 1900 space units
- MinParticipants: minimum required participant capacity = 500 participants
- MinPosterBoards: minimum required poster board capacity = 300 poster boards
  Note: All space, participant, and poster board units are assumed consistent as given in the problem.

Variables:
- CircularTables (integer ≥ 0): number of circular tables to set up
- RectangularTables (integer ≥ 0): number of rectangular tables to set up

Objective:
Maximize TotalCateredGuests = (8 * CircularTables) + (12 * RectangularTables)
  Note: Guest numbers are per table based on the table type.

Constraints:
1. Participant Capacity Constraint:
  (5 * CircularTables) + (4 * RectangularTables) ≥ 500
2. Poster Board Capacity Constraint:
  (4 * CircularTables) + (4 * RectangularTables) ≥ 300
3. Space Constraint:
  (15 * CircularTables) + (20 * RectangularTables) ≤ 1900

This model fully captures the problem requirements using the five-element framework.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not available.")
        return None

    # Variables
    # CircularTables: integer >=0
    # RectangularTables: integer >=0
    circular_tables = solver.IntVar(0, solver.infinity(), 'CircularTables')
    rectangular_tables = solver.IntVar(0, solver.infinity(), 'RectangularTables')
    
    # Objective: maximize 8 * CircularTables + 12 * RectangularTables.
    objective = solver.Objective()
    objective.SetCoefficient(circular_tables, 8)
    objective.SetCoefficient(rectangular_tables, 12)
    objective.SetMaximization()
    
    # Constraints:
    # (5 * CircularTables) + (4 * RectangularTables) ≥ 500 (Participant Capacity)
    solver.Add(5 * circular_tables + 4 * rectangular_tables >= 500)
    
    # (4 * CircularTables) + (4 * RectangularTables) ≥ 300 (Poster Board Capacity)
    solver.Add(4 * circular_tables + 4 * rectangular_tables >= 300)
    
    # (15 * CircularTables) + (20 * RectangularTables) ≤ 1900 (Space Constraint)
    solver.Add(15 * circular_tables + 20 * rectangular_tables <= 1900)
    
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["CircularTables"] = circular_tables.solution_value()
        result["RectangularTables"] = rectangular_tables.solution_value()
        # Get the objective value
        result["objective"] = objective.Value()
    else:
        print("No feasible solution found.")
        result = None
    return result

def main():
    # Solve the model using the linear solver approach.
    print("Results from Linear Solver Model:")
    lp_result = solve_linear_program()
    if lp_result is not None:
        # Construct a structured output similar to the expected JSON output
        output = {
            "variables": {
                "CircularTables": lp_result["CircularTables"],
                "RectangularTables": lp_result["RectangularTables"]
            },
            "objective": lp_result["objective"]
        }
        print(output)
    else:
        print("No solution available from the linear model.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver Model:
{'variables': {'CircularTables': 60.0, 'RectangularTables': 50.0}, 'objective': 1080.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'CircularTables': 60.0, 'RectangularTables': 50.0}, 'objective': 1080.0}'''

