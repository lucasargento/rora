# Problem Description:
'''Problem description: Both sulfate and ginger need to be added to a shampoo. One unit of sulfate takes 0.5 minutes to be effective while one unit of ginger takes 0.75 minutes to be effective. The shampoo must contain at least 100 units of sulfates and a total of 400 units of both ingredient. Since too much sulfate can damage the hair, there can be at most twice the amount of sulfate as ginger in the shampoo. How many units of each should be added to the shampoo to minimize the total amount of time it takes for the mixture to be effective? (Note: one must be added before the other)

Expected Output Schema:
{
  "variables": {
    "SulfateUnits": "float",
    "GingerUnits": "float",
    "SulfateAddedFirst": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one valid formulation of the optimization problem using the five‐element framework. In this version the decision is how many units of sulfate and ginger to add, together with a binary variable (coded as a float in this schema) that indicates if sulfate is added before ginger. Note that although the processing times are additive in this sequential setting (so that order does not affect the sum 0.5×SulfateUnits + 0.75×GingerUnits), the production requirement “one must be added before the other” is included through the variable SulfateAddedFirst. (In an implementation you may treat SulfateAddedFirst as a binary decision variable: 1 if sulfate is added first and 0 otherwise.)

------------------------------------------------------------
Sets:
- Ingredients = {Sulfate, Ginger}

------------------------------------------------------------
Parameters (with assumed units):
- sulfate_time: processing time per unit of sulfate = 0.5 minutes per unit.
- ginger_time: processing time per unit of ginger = 0.75 minutes per unit.
- min_sulfate_units: minimum required units of sulfate = 100 units.
- total_required_units: total units of ingredients = 400 units.
- max_sulfate_multiplier: maximum allowed ratio between sulfate and ginger = 2 (i.e. SulfateUnits ≤ 2 × GingerUnits).

------------------------------------------------------------
Variables:
- SulfateUnits: number of units of sulfate to add (continuous, nonnegative) [units].
- GingerUnits: number of units of ginger to add (continuous, nonnegative) [units].
- SulfateAddedFirst: indicator variable (binary, but typed here as a float 0 or 1) where 1 means sulfate is added first and 0 means ginger is added first.

------------------------------------------------------------
Objective:
Minimize total effective time in minutes:
  minimize Objective = sulfate_time × SulfateUnits + ginger_time × GingerUnits
                       = 0.5 × SulfateUnits + 0.75 × GingerUnits

------------------------------------------------------------
Constraints:
1. Total units constraint:
   SulfateUnits + GingerUnits = total_required_units
   (SulfateUnits + GingerUnits = 400)

2. Minimum sulfate requirement:
   SulfateUnits ≥ min_sulfate_units
   (SulfateUnits ≥ 100)

3. Maximum sulfate-to-ginger ratio constraint:
   SulfateUnits ≤ max_sulfate_multiplier × GingerUnits
   (SulfateUnits ≤ 2 × GingerUnits)

4. (Implicit ordering requirement)
   The decision variable SulfateAddedFirst indicates the order (with no extra time difference in the model since effective times are simply additive). This variable can be used in implementation if additional order‐dependent logic is needed.
  
------------------------------------------------------------
Note:
- All units in the time parameters are in minutes per unit.
- Although the sequential addition implies that one ingredient is added before the other, the total effective time is treated as the sum of the individual times.
- In this structured model the variable SulfateAddedFirst serves only to record the chosen order per the real-world instruction.
  
------------------------------------------------------------
The formatted answer (compatible with the expected output schema) is:

{
  "variables": {
    "SulfateUnits": "float (>= 0, units)",
    "GingerUnits": "float (>= 0, units)",
    "SulfateAddedFirst": "float (0 or 1, where 1 indicates sulfate is added first)"
  },
  "objective": "0.5 * SulfateUnits + 0.75 * GingerUnits (minimize total effective time in minutes)"
}

This model is now complete and consistent with the given problem description.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def run_model_version_1():
    """Model Version 1: Implementation of the shampoo mixing problem.
    Decision variables:
      - SulfateUnits: continuous (>=0)
      - GingerUnits: continuous (>=0)
      - SulfateAddedFirst: binary (0 or 1)
    Objective:
      Minimize total effective time = 0.5 * SulfateUnits + 0.75 * GingerUnits
    Constraints:
      1. SulfateUnits + GingerUnits = 400
      2. SulfateUnits >= 100
      3. SulfateUnits <= 2 * GingerUnits
      4. SulfateAddedFirst is a binary indicator of order (no effect on objective)
    """
    # Create solver instance with CBC (suitable for mixed integer linear programming)
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return None

    # Define decision variables
    sulfate = solver.NumVar(0, solver.infinity(), "SulfateUnits")
    ginger = solver.NumVar(0, solver.infinity(), "GingerUnits")
    # Binary variable: 1 if sulfate is added first, 0 otherwise.
    sulfate_order = solver.IntVar(0, 1, "SulfateAddedFirst")

    # Parameters
    sulfate_time = 0.5  # minutes per unit of sulfate
    ginger_time = 0.75  # minutes per unit of ginger
    min_sulfate_units = 100
    total_required_units = 400
    max_sulfate_multiplier = 2  # SulfateUnits <= 2 * GingerUnits

    # Constraint 1: Total units constraint
    solver.Add(sulfate + ginger == total_required_units)
    # Constraint 2: Minimum sulfate requirement
    solver.Add(sulfate >= min_sulfate_units)
    # Constraint 3: Maximum sulfate-to-ginger ratio constraint
    solver.Add(sulfate <= max_sulfate_multiplier * ginger)
    # Constraint 4: Implicit ordering requirement: variable exists (no extra constraint as processing times are additive)
    # (This variable can be used for order‐dependent logic if necessary.)

    # Objective: Minimize total effective time
    solver.Minimize(sulfate_time * sulfate + ginger_time * ginger)

    # Solve the model
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "SulfateUnits": sulfate.solution_value(),
            "GingerUnits": ginger.solution_value(),
            "SulfateAddedFirst": sulfate_order.solution_value(),
            "Objective": solver.Objective().Value()
        }
    else:
        print("The problem does not have an optimal solution!")
    return result

def main():
    results = {}
    # Only one formulation is provided, hence one model.
    results["Model_Version_1"] = run_model_version_1()
    
    # Print structured output for each model
    if results["Model_Version_1"]:
        print("Results for Model Version 1:")
        print("  SulfateUnits       =", results["Model_Version_1"]["SulfateUnits"])
        print("  GingerUnits        =", results["Model_Version_1"]["GingerUnits"])
        print("  SulfateAddedFirst  =", results["Model_Version_1"]["SulfateAddedFirst"])
        print("  Objective Value    =", results["Model_Version_1"]["Objective"])
    else:
        print("No optimal solution found for Model Version 1.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Results for Model Version 1:
  SulfateUnits       = 266.66666666666663
  GingerUnits        = 133.33333333333331
  SulfateAddedFirst  = 0.0
  Objective Value    = 233.33333333333331
'''

'''Expected Output:
Expected solution

: {'variables': {'SulfateUnits': 266.0, 'GingerUnits': 134.0, 'SulfateAddedFirst': 1.0}, 'objective': 233.5}'''

