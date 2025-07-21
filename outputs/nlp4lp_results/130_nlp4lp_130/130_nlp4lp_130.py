# Problem Description:
'''Problem description: A lawn mowing service provides neighborhood services using small teams and large teams. A small team requires 3 employees and can mow 50 sq ft of lawn. A large team requires 5 employees and can mow 80 sq ft of lawn. The company has 150 employees available. Because most people have smaller lawns in the city, the number of small teams must be at least 3 times as much as the number of large teams. In addition, to make sure the company can meet all demands, there has to be at least 6 large teams and at least 10 small teams. How many of each team type should be used to maximize the amount of lawn that can be mowed?

Expected Output Schema:
{
  "variables": {
    "SmallTeams": "float",
    "LargeTeams": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TeamTypes = {SmallTeam, LargeTeam}

Parameters:
- employees_small = 3        // Number of employees required for one small team [employees/team]
- employees_large = 5        // Number of employees required for one large team [employees/team]
- lawn_small = 50            // Lawn area mowed by one small team [sq ft/team]
- lawn_large = 80            // Lawn area mowed by one large team [sq ft/team]
- total_employees = 150      // Total employees available [employees]
- min_small_teams = 10       // Minimum number of small teams required [teams]
- min_large_teams = 6        // Minimum number of large teams required [teams]
- ratio_small_to_large = 3   // The number of small teams must be at least 3 times the number of large teams

Variables:
- SmallTeams: integer, number of small teams to deploy [teams]
- LargeTeams: integer, number of large teams to deploy [teams]

Objective:
- Maximize Total Lawn Mowed = (lawn_small * SmallTeams) + (lawn_large * LargeTeams) 
  [square feet]

Constraints:
1. Employee Availability: 
   (employees_small * SmallTeams) + (employees_large * LargeTeams) <= total_employees

2. Ratio Constraint: 
   SmallTeams >= ratio_small_to_large * LargeTeams

3. Minimum Team Requirements: 
   SmallTeams >= min_small_teams
   LargeTeams >= min_large_teams

Comments:
- All units are consistent. Employees are counted per team, and the total lawn area is measured in square feet.
- Decision variables are modeled as integers because partial teams are not allowed.
- The model seeks to maximize the total lawn area that can be mowed under the given labor and team composition restrictions.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the linear solver with SCIP backend
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "Linear Solver unavailable.", None

    # Parameters
    employees_small = 3
    employees_large = 5
    lawn_small = 50
    lawn_large = 80
    total_employees = 150
    min_small_teams = 10
    min_large_teams = 6
    ratio_small_to_large = 3

    # Variables: integer variables for each team count
    SmallTeams = solver.IntVar(0, solver.infinity(), 'SmallTeams')
    LargeTeams = solver.IntVar(0, solver.infinity(), 'LargeTeams')

    # Constraints
    # 1. Employee Availability:
    solver.Add(employees_small * SmallTeams + employees_large * LargeTeams <= total_employees)
    # 2. Ratio Constraint: SmallTeams >= 3 * LargeTeams
    solver.Add(SmallTeams >= ratio_small_to_large * LargeTeams)
    # 3. Minimum Team Requirements:
    solver.Add(SmallTeams >= min_small_teams)
    solver.Add(LargeTeams >= min_large_teams)

    # Objective: Maximize total lawn area mowed
    objective = solver.Objective()
    objective.SetCoefficient(SmallTeams, lawn_small)
    objective.SetCoefficient(LargeTeams, lawn_large)
    objective.SetMaximization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "variables": {
                "SmallTeams": SmallTeams.solution_value(),
                "LargeTeams": LargeTeams.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        solution = "No optimal solution found with Linear Solver."

    return solution, solver

def solve_with_cp_model():
    model = cp_model.CpModel()

    # Parameters
    employees_small = 3
    employees_large = 5
    lawn_small = 50
    lawn_large = 80
    total_employees = 150
    min_small_teams = 10
    min_large_teams = 6
    ratio_small_to_large = 3

    # Variables: using integer variables
    # For CP-SAT, we need upper bounds; we can set them based on available employees.
    max_small = total_employees // employees_small
    max_large = total_employees // employees_large
    SmallTeams = model.NewIntVar(0, max_small, 'SmallTeams')
    LargeTeams = model.NewIntVar(0, max_large, 'LargeTeams')

    # Constraints:
    # 1. Employee availability:
    model.Add(employees_small * SmallTeams + employees_large * LargeTeams <= total_employees)
    # 2. Ratio constraint: SmallTeams >= 3 * LargeTeams
    model.Add(SmallTeams >= ratio_small_to_large * LargeTeams)
    # 3. Minimum team requirements:
    model.Add(SmallTeams >= min_small_teams)
    model.Add(LargeTeams >= min_large_teams)

    # Objective: maximize total lawn area mowed
    # In CP-SAT we maximize using AddMaximize
    model.Maximize(lawn_small * SmallTeams + lawn_large * LargeTeams)

    # Solve the model using CP-SAT solver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        solution = {
            "variables": {
                "SmallTeams": solver.Value(SmallTeams),
                "LargeTeams": solver.Value(LargeTeams)
            },
            "objective": solver.ObjectiveValue()
        }
    else:
        solution = "No optimal solution found with CP-SAT."

    return solution, model

def main():
    # Solve using Linear Solver
    linear_solution, _ = solve_with_linear_solver()
    # Solve using CP-SAT
    cp_solution, _ = solve_with_cp_model()

    # Print results in structured format
    print("Results from Linear Solver:")
    print(linear_solution)
    print("\nResults from CP-SAT Solver:")
    print(cp_solution)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results from Linear Solver:
{'variables': {'SmallTeams': 40.0, 'LargeTeams': 6.0}, 'objective': 2480.0}

Results from CP-SAT Solver:
{'variables': {'SmallTeams': 40, 'LargeTeams': 6}, 'objective': 2480.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallTeams': 40.0, 'LargeTeams': 6.0}, 'objective': 2480.0}'''

