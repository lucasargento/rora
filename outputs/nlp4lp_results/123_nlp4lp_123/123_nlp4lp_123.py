# Problem Description:
'''Problem description: An engineering school has a bridge building competition where students must build as many beam bridges and truss bridges as they can using Popsicle sticks and glue. A beam bridge requires 30 Popsicle sticks and 5 units of glue while a truss bridge requires 50 Popsicle sticks and 8 units of glue. Each team has at most 600 Popsicle sticks and 100 units of glue. In addition, each team can build at most 5 truss bridges and the number of beam bridges must be larger than the number of truss bridges. If a beam bridge can hold 40 grams and a truss bridge can hold 60 grams, how many of each bridge should a team build to maximize the total mass that can be supported?

Expected Output Schema:
{
  "variables": {
    "BeamBridges": "float",
    "TrussBridges": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Bridges = {Beam, Truss}

Parameters:
- sticks_per_beam = 30    // Popsicle sticks required per beam bridge (units: sticks)
- glue_per_beam = 5       // Glue units required per beam bridge (units: glue units)
- capacity_beam = 40      // Mass supported by a beam bridge (units: grams)
- sticks_per_truss = 50   // Popsicle sticks required per truss bridge (units: sticks)
- glue_per_truss = 8      // Glue units required per truss bridge (units: glue units)
- capacity_truss = 60     // Mass supported by a truss bridge (units: grams)
- max_sticks = 600        // Maximum available popsicle sticks (units: sticks)
- max_glue = 100          // Maximum available glue (units: glue units)
- max_truss_bridges = 5   // Maximum number of truss bridges allowed per team

Variables:
- BeamBridges: integer, number of beam bridges built (≥ 0) [units: bridges]
- TrussBridges: integer, number of truss bridges built (≥ 0) [units: bridges]

Objective:
- Maximize TotalMassSupported = (capacity_beam * BeamBridges) + (capacity_truss * TrussBridges)
  // This represents the sum of the supported masses by all built bridges (units: grams)

Constraints:
1. Popsicle Sticks Constraint:
   (sticks_per_beam * BeamBridges) + (sticks_per_truss * TrussBridges) ≤ max_sticks
2. Glue Constraint:
   (glue_per_beam * BeamBridges) + (glue_per_truss * TrussBridges) ≤ max_glue
3. Maximum Truss Bridges Constraint:
   TrussBridges ≤ max_truss_bridges
4. Relative Count Constraint:
   BeamBridges ≥ TrussBridges + 1
   // Ensures that the number of beam bridges is strictly larger than the number of truss bridges

Comments:
- All parameters are assumed to be in consistent units as given in the problem.
- The decision variables are modeled as integers since the number of bridges built must be whole numbers.
- The relative count constraint is written as BeamBridges ≥ TrussBridges + 1 to capture the strict inequality in an integer context.

Expected Output Schema:
{
  "variables": {
    "BeamBridges": "float",
    "TrussBridges": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_model_1():
    # Create the solver using CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters as given
    sticks_per_beam = 30
    glue_per_beam = 5
    capacity_beam = 40
    sticks_per_truss = 50
    glue_per_truss = 8
    capacity_truss = 60
    max_sticks = 600
    max_glue = 100
    max_truss_bridges = 5

    # Decision Variables
    # Using integer variables for bridge counts (non-negative integers).
    BeamBridges = solver.IntVar(0, solver.infinity(), 'BeamBridges')
    TrussBridges = solver.IntVar(0, solver.infinity(), 'TrussBridges')

    # Constraints
    # 1. Popsicle Sticks Constraint: 30 * BeamBridges + 50 * TrussBridges <= 600
    solver.Add(sticks_per_beam * BeamBridges + sticks_per_truss * TrussBridges <= max_sticks)
    
    # 2. Glue Constraint: 5 * BeamBridges + 8 * TrussBridges <= 100
    solver.Add(glue_per_beam * BeamBridges + glue_per_truss * TrussBridges <= max_glue)
    
    # 3. Maximum Truss Bridges Constraint: TrussBridges <= 5
    solver.Add(TrussBridges <= max_truss_bridges)
    
    # 4. Relative Count Constraint: BeamBridges >= TrussBridges + 1
    solver.Add(BeamBridges >= TrussBridges + 1)
    
    # Objective: maximize capacity_beam*BeamBridges + capacity_truss*TrussBridges
    objective = solver.Objective()
    objective.SetCoefficient(BeamBridges, capacity_beam)
    objective.SetCoefficient(TrussBridges, capacity_truss)
    objective.SetMaximization()

    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['BeamBridges'] = BeamBridges.solution_value()
        result['TrussBridges'] = TrussBridges.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = "The problem does not have an optimal solution."

    # Structure result as expected schema.
    return result

def main():
    # Since the mathematical formulation is uniquely defined, we only implement one version.
    results = {}
    model1_results = solve_model_1()
    results["Model1"] = model1_results

    # Print the results in a structured way.
    print("Optimization Results:")
    for model, res in results.items():
        print(f"\n{model} Results:")
        if 'error' in res:
            print(res['error'])
        else:
            print("Variables:")
            print(f"  BeamBridges: {res['BeamBridges']}")
            print(f"  TrussBridges: {res['TrussBridges']}")
            print(f"Objective Value (Total Mass Supported in grams): {res['objective']}")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Optimization Results:

Model1 Results:
Variables:
  BeamBridges: 20.0
  TrussBridges: 0.0
Objective Value (Total Mass Supported in grams): 800.0
'''

'''Expected Output:
Expected solution

: {'variables': {'BeamBridges': 20.0, 'TrussBridges': 0.0}, 'objective': 800.0}'''

