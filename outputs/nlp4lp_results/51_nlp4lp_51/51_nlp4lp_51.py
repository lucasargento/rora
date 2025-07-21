# Problem Description:
'''Problem description: An oil and gas company operates on 300 acres of land where they use oil wells of small and large size. Per acre of land, a small oil well can produce 2 barrels of oil. Per acre of land, a large oil well can produce 5 barrels of oil. However, a small oil well produces 10 units of pollution and requires 5 drill bits per acre and a large oil well produces 20 units of pollution and requires 10 drill bits per acre. The company has available 2500 drill bits and due to strict environmental laws can produce at most 4500 units of pollution. For how many acres should each oil well be used to maximize the total production of oil?

Expected Output Schema:
{
  "variables": {
    "LandAllocated": {
      "0": "float",
      "1": "float"
    }
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete five-element model formulation for the oil well acreage allocation problem.

-----------------------------
Sets:
- W: set of oil well types = {small, large}

-----------------------------
Parameters:
- TotalAcres: total acres available for allocation (acres) = 300
- Production[w]: oil produced per acre when using well type w (barrels per acre)
  • Production[small] = 2
  • Production[large] = 5
- DrillBitUsage[w]: number of drill bits required per acre for well type w (bits per acre)
  • DrillBitUsage[small] = 5
  • DrillBitUsage[large] = 10
- Pollution[w]: pollution generated per acre for well type w (pollution units per acre)
  • Pollution[small] = 10
  • Pollution[large] = 20
- TotalDrillBits: total available drill bits (bits) = 2500
- MaxPollution: maximum allowable pollution (pollution units) = 4500

-----------------------------
Variables:
- AcreAllocation[w]: acres allocated to well type w
  • AcreAllocation[w] is continuous and ≥ 0  (for w in W)
  [Interpretation: Decision variable for how many acres to use for each oil well type.]

-----------------------------
Objective:
- Maximize TotalOilProduction, where
  TotalOilProduction = sum over w in W of (Production[w] * AcreAllocation[w])
  [Units: barrels]

-----------------------------
Constraints:
1. Land Availability Constraint:
  sum over w in W of AcreAllocation[w] ≤ TotalAcres
    [Total acres allocated must not exceed 300 acres.]

2. Drill Bit Availability Constraint:
  sum over w in W of (DrillBitUsage[w] * AcreAllocation[w]) ≤ TotalDrillBits
    [Total drill bits used cannot exceed 2500 bits.]

3. Pollution Constraint:
  sum over w in W of (Pollution[w] * AcreAllocation[w]) ≤ MaxPollution
    [Total pollution generated must not exceed 4500 pollution units.]

-----------------------------

This model is self-contained and uses clear, consistent units (acres, barrels, bits, pollution units) as given in the problem description. The decision variables (AcreAllocation[small] and AcreAllocation[large]) represent the acreage on which each type of oil well is used, and the objective is to maximize total oil production while satisfying land, resource, and environmental constraints.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_lp_model():
    # Create the linear solver with the GLOP backend for continuous optimization.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Error: Could not create solver.")
        return None

    # Parameters
    TotalAcres = 300
    TotalDrillBits = 2500
    MaxPollution = 4500

    Production = {'small': 2, 'large': 5}
    DrillBitUsage = {'small': 5, 'large': 10}
    Pollution = {'small': 10, 'large': 20}
    
    # Variables: acres allocated to each well type, continuous and >= 0
    acre_small = solver.NumVar(0.0, solver.infinity(), 'AcreAllocation_small')
    acre_large = solver.NumVar(0.0, solver.infinity(), 'AcreAllocation_large')
    
    # Constraint 1: Land Availability Constraint: small + large <= TotalAcres
    solver.Add(acre_small + acre_large <= TotalAcres)
    
    # Constraint 2: Drill Bit Availability Constraint: 5 * small + 10 * large <= TotalDrillBits
    solver.Add(DrillBitUsage['small'] * acre_small + DrillBitUsage['large'] * acre_large <= TotalDrillBits)
    
    # Constraint 3: Pollution Constraint: 10 * small + 20 * large <= MaxPollution
    solver.Add(Pollution['small'] * acre_small + Pollution['large'] * acre_large <= MaxPollution)

    # Objective: Maximize Total Oil Production = 2 * small + 5 * large
    objective = solver.Objective()
    objective.SetCoefficient(acre_small, Production['small'])
    objective.SetCoefficient(acre_large, Production['large'])
    objective.SetMaximization()
    
    # Solve the model
    status = solver.Solve()
    
    # Prepare results
    result = {}
    
    if status == pywraplp.Solver.OPTIMAL:
        result['model_type'] = 'Linear Programming using ortools.linear_solver'
        result['variables'] = {
            "LandAllocated": {
                "small": acre_small.solution_value(),
                "large": acre_large.solution_value()
            }
        }
        result['objective'] = objective.Value()
    else:
        result['model_type'] = 'Linear Programming using ortools.linear_solver'
        result['status'] = 'The problem does not have an optimal solution.'
    
    return result

def main():
    results = {}
    # As per formulation provided, only one model is proposed.
    # We implement the model using the linear solver.
    lp_result = solve_lp_model()
    results['LinearSolverModel'] = lp_result

    # Print results in a structured way.
    import json
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
    "LinearSolverModel": {
        "model_type": "Linear Programming using ortools.linear_solver",
        "variables": {
            "LandAllocated": {
                "small": 0.0,
                "large": 225.00000000000003
            }
        },
        "objective": 1125.0000000000002
    }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'LandAllocated': {'0': 0.0, '1': 225.0}}, 'objective': 1125.0}'''

