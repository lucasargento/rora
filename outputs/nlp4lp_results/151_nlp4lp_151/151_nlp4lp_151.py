# Problem Description:
'''Problem description: A toy store hires seasonal and full-time volunteers to deliver gifts and gives them points for service. A seasonal volunteer can deliver 5 gifts and gets 2 points. A full-time volunteer can deliver 8 gifts and gets 5 points. The store can only give out 200 points. In addition, a maximum of 30% of the volunteers can be seasonal and at least 10 must be full-time. How many of each volunteer is needed to maximize the total number of gifts that can be delivered?

Expected Output Schema:
{
  "variables": {
    "SeasonalVolunteers": "float",
    "FullTimeVolunteers": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''{
  "Sets": {
    "VolunteerTypes": ["Seasonal", "FullTime"]
  },
  "Parameters": {
    "gifts_per_seasonal": "Number of gifts delivered by a seasonal volunteer (5 gifts)",
    "points_per_seasonal": "Points given to a seasonal volunteer (2 points)",
    "gifts_per_fulltime": "Number of gifts delivered by a full-time volunteer (8 gifts)",
    "points_per_fulltime": "Points given to a full-time volunteer (5 points)",
    "max_total_points": "Maximum total points available (200 points)",
    "max_seasonal_ratio": "Maximum allowed ratio of seasonal volunteers over total volunteers (0.30)",
    "min_fulltime": "Minimum required number of full-time volunteers (10 volunteers)"
  },
  "Variables": {
    "SeasonalVolunteers": "Nonnegative real number representing the number of seasonal volunteers (can be cast to integer in implementation)",
    "FullTimeVolunteers": "Nonnegative real number representing the number of full-time volunteers (can be cast to integer in implementation)"
  },
  "Objective": "Maximize total_gifts = (gifts_per_seasonal * SeasonalVolunteers) + (gifts_per_fulltime * FullTimeVolunteers)",
  "Constraints": [
    {
      "name": "Points Constraint",
      "expression": "(points_per_seasonal * SeasonalVolunteers) + (points_per_fulltime * FullTimeVolunteers) <= max_total_points",
      "comment": "The total points given to all volunteers cannot exceed 200 points."
    },
    {
      "name": "Seasonal Volunteer Ratio Constraint",
      "expression": "SeasonalVolunteers <= max_seasonal_ratio * (SeasonalVolunteers + FullTimeVolunteers)",
      "comment": "At most 30% of the total volunteers can be seasonal."
    },
    {
      "name": "Minimum FullTime Volunteers Constraint",
      "expression": "FullTimeVolunteers >= min_fulltime",
      "comment": "At least 10 full-time volunteers are required."
    },
    {
      "name": "Nonnegativity Constraint",
      "expression": "SeasonalVolunteers >= 0 and FullTimeVolunteers >= 0",
      "comment": "Number of volunteers cannot be negative."
    }
  ]
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_program():
    # Create the MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, "Solver not created!"

    # Define decision variables (as integers)
    # SeasonalVolunteers: nonnegative integer
    # FullTimeVolunteers: nonnegative integer
    S = solver.IntVar(0, solver.infinity(), 'SeasonalVolunteers')
    F = solver.IntVar(0, solver.infinity(), 'FullTimeVolunteers')
    
    # Constraint: Points Constraint
    # (2 * S + 5 * F) <= 200
    solver.Add(2 * S + 5 * F <= 200)
    
    # Constraint: Seasonal Volunteer Ratio Constraint
    # S <= 0.30 * (S + F) equivalent to S - 0.30S <= 0.30F  => 0.70S <= 0.30F
    # To avoid floating point precision issues, multiply both sides by 10:
    # 7S <= 3F
    solver.Add(7 * S <= 3 * F)
    
    # Constraint: Minimum FullTime Volunteers Constraint: F >= 10
    solver.Add(F >= 10)
    
    # Objective: Maximize total gifts delivered = 5 * S + 8 * F
    objective = solver.Objective()
    objective.SetCoefficient(S, 5)
    objective.SetCoefficient(F, 8)
    objective.SetMaximization()
    
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return None, "The integer model did not find an optimal solution."
    
    result = {
      "SeasonalVolunteers": S.solution_value(),
      "FullTimeVolunteers": F.solution_value(),
      "objective": objective.Value()
    }
    return result, None

def solve_continuous_program():
    # Create the LP solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "LP Solver not created!"

    # Define decision variables (as continuous nonnegative numbers)
    S = solver.NumVar(0.0, solver.infinity(), 'SeasonalVolunteers')
    F = solver.NumVar(0.0, solver.infinity(), 'FullTimeVolunteers')
    
    # Constraint: Points Constraint: 2*S + 5*F <= 200
    solver.Add(2 * S + 5 * F <= 200)
    
    # Constraint: Seasonal Volunteer Ratio Constraint: S <= 0.30 * (S + F)
    # Rearranged: S - 0.30*S <= 0.30*F  => 0.70*S <= 0.30*F
    solver.Add(0.70 * S <= 0.30 * F)
    
    # Constraint: Minimum FullTime Volunteers Constraint: F >= 10
    solver.Add(F >= 10)
    
    # Objective: Maximize total gifts delivered = 5*S + 8*F
    objective = solver.Objective()
    objective.SetCoefficient(S, 5)
    objective.SetCoefficient(F, 8)
    objective.SetMaximization()
    
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return None, "The LP model did not find an optimal solution."
    
    result = {
      "SeasonalVolunteers": S.solution_value(),
      "FullTimeVolunteers": F.solution_value(),
      "objective": objective.Value()
    }
    return result, None

def main():
    ip_result, ip_error = solve_integer_program()
    lp_result, lp_error = solve_continuous_program()

    print("Integer Programming Model Result:")
    if ip_error:
        print("Error:", ip_error)
    else:
        print(ip_result)

    print("\nContinuous Linear Programming Model Result:")
    if lp_error:
        print("Error:", lp_error)
    else:
        print(lp_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Integer Programming Model Result:
{'SeasonalVolunteers': 14.0, 'FullTimeVolunteers': 34.0, 'objective': 342.0}

Continuous Linear Programming Model Result:
{'SeasonalVolunteers': 14.634146341463412, 'FullTimeVolunteers': 34.146341463414636, 'objective': 346.3414634146342}
'''

'''Expected Output:
Expected solution

: {'variables': {'SeasonalVolunteers': 14.0, 'FullTimeVolunteers': 34.0}, 'objective': 342.0}'''

