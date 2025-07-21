# Problem Description:
'''Problem description: An dog hospital has 2000 units of tooth medication to make both small and large bones. A small bone requires 10 units of tooth medication and 12 units of meat. A large bone requires 15 units of tooth medication and 15 units of meat. Since most dogs prefer the small bones, at least 50% of the bones made must be small. In addition, the hospital must make at least 30 large bones. How many of each bone should be made to minimize the amount of meat needed?

Expected Output Schema:
{
  "variables": {
    "SmallBones": "float",
    "LargeBones": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Bones: the set of bone types = {Small, Large}

Parameters:
- MedicationStock: total available tooth medication [units] = 2000
- MedicationReq_Small: tooth medication required per small bone [units] = 10
- MedicationReq_Large: tooth medication required per large bone [units] = 15
- MeatReq_Small: meat required per small bone [units] = 12
- MeatReq_Large: meat required per large bone [units] = 15
- MinLargeBones: minimum number of large bones to produce [bones] = 30
- MinSmallFraction: minimum fraction of small bones among all bones = 0.5  
  (This implies that the number of small bones must be at least equal to the number of large bones.)

Variables:
- SmallBones: number of small bones produced (nonnegative integer)
- LargeBones: number of large bones produced (nonnegative integer)

Objective:
- Minimize total meat usage = (MeatReq_Small * SmallBones) + (MeatReq_Large * LargeBones)

Constraints:
1. Tooth medication usage constraint:
   MedicationReq_Small * SmallBones + MedicationReq_Large * LargeBones <= MedicationStock
   → 10 * SmallBones + 15 * LargeBones <= 2000

2. Proportion constraint on bone types (at least 50% of bones are small):
   SmallBones >= (SmallBones + LargeBones) / 2
   This simplifies to: SmallBones >= LargeBones

3. Minimum large bone production:
   LargeBones >= MinLargeBones
   → LargeBones >= 30

4. Non-negativity:
   SmallBones >= 0  
   LargeBones >= 0

Additional Notes:
- All ingredients are measured in consistent "units".  
- The decision variables are assumed to be integers, since you cannot produce a fraction of a bone.
  
This completes the structured mathematical model for the given problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return {"error": "Solver not created."}

    # Variables: nonnegative integers.
    # Upper bounds are derived from medication constraint.
    SmallBones = solver.IntVar(0, 2000 // 10, 'SmallBones')  # max 200 (2000/10)
    LargeBones = solver.IntVar(0, 2000 // 15, 'LargeBones')  # max 133 (integer division)

    # Constraint 1: Tooth medication usage: 10*SmallBones + 15*LargeBones <= 2000.
    solver.Add(10 * SmallBones + 15 * LargeBones <= 2000)

    # Constraint 2: Proportion: at least 50% of bones are small -> SmallBones >= LargeBones.
    solver.Add(SmallBones >= LargeBones)

    # Constraint 3: Minimum large bone production: LargeBones >= 30.
    solver.Add(LargeBones >= 30)

    # Objective: minimize total meat usage = 12*SmallBones + 15*LargeBones.
    objective = solver.Objective()
    objective.SetCoefficient(SmallBones, 12)
    objective.SetCoefficient(LargeBones, 15)
    objective.SetMinimization()

    # Solve.
    status = solver.Solve()

    if status != pywraplp.Solver.OPTIMAL:
        return {"error": "No optimal solution found using linear solver."}

    # Extract solution.
    solution = {
        "variables": {
            "SmallBones": SmallBones.solution_value(),
            "LargeBones": LargeBones.solution_value()
        },
        "objective": objective.Value()
    }
    return solution


def solve_with_cp_model():
    # Create the CpModel.
    model = cp_model.CpModel()

    # Given the constraints, we can set reasonable upper bounds.
    # Maximum small bones = floor(2000/10) = 200, maximum large bones = floor(2000/15) = 133.
    max_small = 200
    max_large = 133

    SmallBones = model.NewIntVar(0, max_small, 'SmallBones')
    LargeBones = model.NewIntVar(0, max_large, 'LargeBones')

    # Constraint 1: Tooth medication usage constraint.
    model.Add(10 * SmallBones + 15 * LargeBones <= 2000)

    # Constraint 2: Proportion constraint (at least 50% of bones are small).
    model.Add(SmallBones >= LargeBones)

    # Constraint 3: Minimum large bone production.
    model.Add(LargeBones >= 30)

    # Objective: minimize the total meat usage = 12*SmallBones + 15*LargeBones.
    model.Minimize(12 * SmallBones + 15 * LargeBones)

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {"error": "No solution found using CP-SAT model."}

    solution = {
        "variables": {
            "SmallBones": solver.Value(SmallBones),
            "LargeBones": solver.Value(LargeBones)
        },
        "objective": solver.ObjectiveValue()
    }
    return solution


def main():
    # Solve using OR-Tools Linear Solver (MIP formulation).
    ls_solution = solve_with_linear_solver()
    
    # Solve using OR-Tools CP-SAT model.
    cp_solution = solve_with_cp_model()
    
    # Print results in a structured manner.
    print("Results using Linear Solver (MIP):")
    print(ls_solution)
    print("\nResults using CP-SAT Model:")
    print(cp_solution)


if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results using Linear Solver (MIP):
{'variables': {'SmallBones': 30.0, 'LargeBones': 30.0}, 'objective': 810.0}

Results using CP-SAT Model:
{'variables': {'SmallBones': 30, 'LargeBones': 30}, 'objective': 810.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'SmallBones': 30.0, 'LargeBones': 30.0}, 'objective': 810.0}'''

