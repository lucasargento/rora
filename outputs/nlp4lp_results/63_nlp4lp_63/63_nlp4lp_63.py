# Problem Description:
'''Problem description: A fire department employs regular and emergency fire fighters. A regular fire fighter works 10 hours per shift and earns $300. An emergency fire fighter works 6 hours per shift and earns $100. Due to wildfires in the region, the fire department needs at least 300 hours of fire fighter time. If the fire department has a budget of $7000, how many of each should the fire department hire to minimize the total number of fire fighters?

Expected Output Schema:
{
  "variables": {
    "ShiftsPerType": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the complete five‐element structured model following the instructions:

------------------------------
Sets:
- FighterTypes = {regular, emergency}
  (Interpretation: "regular" corresponds to a regular fire fighter and "emergency" to an emergency fire fighter.)

------------------------------
Parameters:
- shift_hours[regular] = 10 (hours per shift for a regular fire fighter)
- shift_hours[emergency] = 6 (hours per shift for an emergency fire fighter)
- shift_cost[regular] = 300 (dollars per shift for a regular fire fighter)
- shift_cost[emergency] = 100 (dollars per shift for an emergency fire fighter)
- required_hours = 300 (minimum total fire fighter hours required)
- available_budget = 7000 (total budget in dollars)
  
(Note: All units are consistent. Hours and dollars are used as given in the problem.)

------------------------------
Variables:
- ShiftsPerType with two indices:
  • ShiftsPerType["regular"]: integer, number of shifts assigned to regular fire fighters
  • ShiftsPerType["emergency"]: integer, number of shifts assigned to emergency fire fighters
  
(Assumption: Each shift corresponds to hiring one fire fighter for that shift.)

------------------------------
Objective:
- Minimize total_firefighters = ShiftsPerType["regular"] + ShiftsPerType["emergency"]

------------------------------
Constraints:
1. Fire fighter hours constraint:
   10 * ShiftsPerType["regular"] + 6 * ShiftsPerType["emergency"] ≥ required_hours
   (Ensures that the total worked hours is at least 300 hours.)

2. Budget constraint:
   300 * ShiftsPerType["regular"] + 100 * ShiftsPerType["emergency"] ≤ available_budget
   (Ensures that the total cost does not exceed $7000.)

------------------------------

For ease of mapping to code, one can use indices "0" and "1" corresponding to "regular" and "emergency", respectively, when setting up the variable ShiftsPerType. The expected output schema shows the dictionary keys "0" and "1" representing the two fighter types.

The output schema representation could thus be:

{
  "variables": {
    "ShiftsPerType": {
      "0": "float",  // corresponds to regular fire fighters (10 hours per shift, $300 per shift)
      "1": "float"   // corresponds to emergency fire fighters (6 hours per shift, $100 per shift)
    }
  },
  "objective": "float"   // minimized total number of fire fighters
}

This completes the precise translation of the problem into the five-element mathematical optimization model.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_firefighter_problem():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameter definitions
    shift_hours = {"0": 10, "1": 6}      # "0": regular, "1": emergency
    shift_cost = {"0": 300, "1": 100}      # "0": regular, "1": emergency
    required_hours = 300
    available_budget = 7000

    # Decision variables: number of shifts (integer variables)
    # Using keys "0" for regular and "1" for emergency as per expected schema.
    shifts = {}
    shifts["0"] = solver.IntVar(0, solver.infinity(), 'Shifts_regular')
    shifts["1"] = solver.IntVar(0, solver.infinity(), 'Shifts_emergency')

    # Objective: minimize the total number of fire fighters (shifts total)
    objective = solver.Objective()
    objective.SetCoefficient(shifts["0"], 1)
    objective.SetCoefficient(shifts["1"], 1)
    objective.SetMinimization()

    # Constraint 1: Total fire fighter hours must be at least required_hours
    solver.Add(shift_hours["0"] * shifts["0"] + shift_hours["1"] * shifts["1"] >= required_hours)

    # Constraint 2: Total cost must not exceed available budget
    solver.Add(shift_cost["0"] * shifts["0"] + shift_cost["1"] * shifts["1"] <= available_budget)

    # Solve the model.
    status = solver.Solve()

    # Process the results.
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['variables'] = {
            'ShiftsPerType': {
                "0": shifts["0"].SolutionValue(),
                "1": shifts["1"].SolutionValue()
            }
        }
        result['objective'] = objective.Value()
    else:
        result['error'] = "The problem does not have an optimal solution."

    return result

def main():
    # Since only one formulation is provided, we solve it using a linear programming model.
    result1 = solve_firefighter_problem()

    # Display the results in a structured way.
    print("Result from the Linear Programming Model:")
    if 'error' in result1:
        print(result1['error'])
    else:
        print("Optimal Variables (ShiftsPerType):")
        print("  Regular (index '0'): {}".format(result1['variables']['ShiftsPerType']["0"]))
        print("  Emergency (index '1'): {}".format(result1['variables']['ShiftsPerType']["1"]))
        print("Objective Value (Total number of fire fighters): {}".format(result1['objective']))

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Result from the Linear Programming Model:
Optimal Variables (ShiftsPerType):
  Regular (index '0'): 15.0
  Emergency (index '1'): 25.0
Objective Value (Total number of fire fighters): 40.0
'''

'''Expected Output:
Expected solution

: {'variables': {'ShiftsPerType': {'0': 15.0, '1': 25.0}}, 'objective': 40.0}'''

