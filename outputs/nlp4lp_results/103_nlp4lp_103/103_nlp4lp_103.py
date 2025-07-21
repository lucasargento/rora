# Problem Description:
'''Problem description: A boy needs to get enough magnesium and zinc in his diet by eating chewable gummies and taking pills. Each gummy contains 3 units of magnesium and 4 units of zinc. Each pill contains 2 units of magnesium and 5 units of zinc. The boy must take at least 10 pills. Since he prefers gummies more, he must eat at least 3 times the amount of gummies as pills. If the boy can consume at most 200 units of magnesium, how many of each should he eat to maximize his zinc intake?

Expected Output Schema:
{
  "variables": {
    "NumberOfGummies": "float",
    "NumberOfPills": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of supplement types = {Gummy, Pill}

Parameters:
- mg_per_gummy: 3 (units of magnesium per gummy)
- zn_per_gummy: 4 (units of zinc per gummy)
- mg_per_pill: 2 (units of magnesium per pill)
- zn_per_pill: 5 (units of zinc per pill)
- max_mg: 200 (maximum units of magnesium that can be consumed)
- min_pills: 10 (minimum number of pills that must be taken)
- gummy_ratio: 3 (the number of gummies must be at least 3 times the number of pills)

Variables:
- NumberOfGummies: continuous nonnegative variable representing the number of chewable gummies consumed (units)
- NumberOfPills: continuous nonnegative variable representing the number of pills consumed (units)

Objective:
- Maximize total zinc intake = (zn_per_gummy * NumberOfGummies) + (zn_per_pill * NumberOfPills)
  That is: Maximize Z = 4 * NumberOfGummies + 5 * NumberOfPills

Constraints:
1. Magnesium constraint:
   - mg_per_gummy * NumberOfGummies + mg_per_pill * NumberOfPills ≤ max_mg
   - 3 * NumberOfGummies + 2 * NumberOfPills ≤ 200

2. Minimum pills constraint:
   - NumberOfPills ≥ min_pills
   - NumberOfPills ≥ 10

3. Gummies preference constraint (gummy consumption is at least 3 times pill consumption):
   - NumberOfGummies ≥ gummy_ratio * NumberOfPills
   - NumberOfGummies ≥ 3 * NumberOfPills

4. Non-negativity:
   - NumberOfGummies ≥ 0
   - NumberOfPills ≥ 0

------------------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "NumberOfGummies": "float",
    "NumberOfPills": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Solver not created."
    
    # Parameters
    mg_per_gummy = 3
    zn_per_gummy = 4
    mg_per_pill = 2
    zn_per_pill = 5
    max_mg = 200
    min_pills = 10
    gummy_ratio = 3
    
    # Define variables: continuous nonnegative.
    NumberOfGummies = solver.NumVar(0.0, solver.infinity(), 'NumberOfGummies')
    NumberOfPills = solver.NumVar(0.0, solver.infinity(), 'NumberOfPills')
    
    # Constraint 1: Magnesium constraint: 3 * NumberOfGummies + 2 * NumberOfPills <= 200
    solver.Add(mg_per_gummy * NumberOfGummies + mg_per_pill * NumberOfPills <= max_mg)
    
    # Constraint 2: Minimum pills constraint: NumberOfPills >= 10
    solver.Add(NumberOfPills >= min_pills)
    
    # Constraint 3: Gummies preference constraint: NumberOfGummies >= 3 * NumberOfPills
    solver.Add(NumberOfGummies >= gummy_ratio * NumberOfPills)
    
    # Objective: Maximize total zinc intake = 4 * NumberOfGummies + 5 * NumberOfPills
    objective = solver.Objective()
    objective.SetCoefficient(NumberOfGummies, zn_per_gummy)
    objective.SetCoefficient(NumberOfPills, zn_per_pill)
    objective.SetMaximization()
    
    # Solve the problem
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfGummies": NumberOfGummies.solution_value(),
                "NumberOfPills": NumberOfPills.solution_value()
            },
            "objective": objective.Value()
        }
        return result, None
    else:
        return None, "The problem does not have an optimal solution."

def main():
    # Since only one formulation is proposed in the mathematical description,
    # we implement one model using the ortools.linear_solver.
    result_lp, error_lp = solve_linear_program()
    
    # Prepare a structured result output for the implemented model.
    if result_lp is not None:
        print("Linear Programming Model Solution:")
        print(result_lp)
    else:
        print("Linear Programming Model Error:")
        print(error_lp)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Linear Programming Model Solution:
{'variables': {'NumberOfGummies': 54.54545454545455, 'NumberOfPills': 18.181818181818183}, 'objective': 309.0909090909091}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfGummies': 54.54545454545455, 'NumberOfPills': 18.181818181818187}, 'objective': 309.0909090909091}'''

