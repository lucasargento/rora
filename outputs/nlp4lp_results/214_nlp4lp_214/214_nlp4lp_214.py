# Problem Description:
'''Problem description: A metal-working shop has access to two types of metal-working equipment, a chop saw and a steel cutter. A chop saw can work 25 pounds of steel and generates 25 units of waste every day. A steel cutter can only cut 5 pounds of steel and generates 3 units of waste every day.  The metal-working shop is expecting an increase in demand and must cut 520 pounds of metal every day. However, there is a waste limitation due to the fines that may be in place if too much heavy metal is discarded and they may at most produce 400 units of waste every day. How should the metal-working shop purchase their metal-working equipment to decrease the total number of metal-working equipment needed?

Expected Output Schema:
{
  "variables": {
    "NumberOfChopSaws": "float",
    "NumberOfSteelCutters": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is the structured formulation using the five-element framework.

------------------------------------------------------------
Sets:
- E: set of equipment types = {ChopSaw, SteelCutter}

------------------------------------------------------------
Parameters:
- pounds_per_ChopSaw = 25 (pounds of steel cut by one Chop Saw per day)
- pounds_per_SteelCutter = 5 (pounds of steel cut by one Steel Cutter per day)
- waste_per_ChopSaw = 25 (waste units produced by one Chop Saw per day)
- waste_per_SteelCutter = 3 (waste units produced by one Steel Cutter per day)
- required_steel = 520 (pounds of steel to be cut per day)
- max_waste = 400 (maximum waste units allowed per day)

------------------------------------------------------------
Variables:
- NumberOfChopSaws (integer, ≥ 0): number of Chop Saws purchased
- NumberOfSteelCutters (integer, ≥ 0): number of Steel Cutters purchased

------------------------------------------------------------
Objective:
Minimize TotalEquipment = NumberOfChopSaws + NumberOfSteelCutters  
(This reflects the goal of decreasing the total number of metal-working equipment needed.)

------------------------------------------------------------
Constraints:
1. Metal Cutting Requirement:  
   (pounds_per_ChopSaw * NumberOfChopSaws) + (pounds_per_SteelCutter * NumberOfSteelCutters) ≥ required_steel  
   i.e., 25 * NumberOfChopSaws + 5 * NumberOfSteelCutters ≥ 520

2. Waste Limitation:  
   (waste_per_ChopSaw * NumberOfChopSaws) + (waste_per_SteelCutter * NumberOfSteelCutters) ≤ max_waste  
   i.e., 25 * NumberOfChopSaws + 3 * NumberOfSteelCutters ≤ 400

------------------------------------------------------------
Notes:
- Although equipment numbers must be whole numbers (integers), the expected output schema lists them as floats. When implementing the model, consider enforcing integer decisions.
- All units are assumed consistent (pounds for steel and waste units for waste), based on the problem description.
- The decision variables indicate the daily operational capacity based on the capacities and waste production rates of the equipment.

The resulting model is thus complete and self-contained for the given optimization problem.

------------------------------------------------------------

Expected Output Schema:
{
  "variables": {
    "NumberOfChopSaws": "float", 
    "NumberOfSteelCutters": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return None, "Solver not created."

    # Decision Variables (integer variables)
    chopSaw = solver.IntVar(0, solver.infinity(), 'NumberOfChopSaws')
    steelCutter = solver.IntVar(0, solver.infinity(), 'NumberOfSteelCutters')

    # Parameters
    pounds_per_ChopSaw = 25
    pounds_per_SteelCutter = 5
    waste_per_ChopSaw = 25
    waste_per_SteelCutter = 3
    required_steel = 520
    max_waste = 400

    # Constraints
    # 1. Metal Cutting Requirement: 25 * chopSaw + 5 * steelCutter >= 520
    solver.Add(pounds_per_ChopSaw * chopSaw + pounds_per_SteelCutter * steelCutter >= required_steel)

    # 2. Waste Limitation: 25 * chopSaw + 3 * steelCutter <= 400
    solver.Add(waste_per_ChopSaw * chopSaw + waste_per_SteelCutter * steelCutter <= max_waste)

    # Objective: Minimize total equipment = chopSaw + steelCutter
    solver.Minimize(chopSaw + steelCutter)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfChopSaws": float(chopSaw.solution_value()),
                "NumberOfSteelCutters": float(steelCutter.solution_value())
            },
            "objective": float(solver.Objective().Value())
        }
        return result, None
    elif status == pywraplp.Solver.FEASIBLE:
        return None, "A feasible solution was found, but it might not be optimal."
    else:
        return None, "No feasible solution found."

def solve_relaxed_model():
    # Create the LP solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Solver not created."

    # Decision Variables (continuous variables)
    chopSaw = solver.NumVar(0.0, solver.infinity(), 'NumberOfChopSaws')
    steelCutter = solver.NumVar(0.0, solver.infinity(), 'NumberOfSteelCutters')

    # Parameters
    pounds_per_ChopSaw = 25
    pounds_per_SteelCutter = 5
    waste_per_ChopSaw = 25
    waste_per_SteelCutter = 3
    required_steel = 520
    max_waste = 400

    # Constraints
    # 1. Metal Cutting Requirement: 25 * chopSaw + 5 * steelCutter >= 520
    solver.Add(pounds_per_ChopSaw * chopSaw + pounds_per_SteelCutter * steelCutter >= required_steel)

    # 2. Waste Limitation: 25 * chopSaw + 3 * steelCutter <= 400
    solver.Add(waste_per_ChopSaw * chopSaw + waste_per_SteelCutter * steelCutter <= max_waste)

    # Objective: Minimize total equipment = chopSaw + steelCutter
    objective = solver.Sum([chopSaw, steelCutter])
    solver.Minimize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfChopSaws": chopSaw.solution_value(),
                "NumberOfSteelCutters": steelCutter.solution_value()
            },
            "objective": solver.Objective().Value()
        }
        return result, None
    elif status == pywraplp.Solver.FEASIBLE:
        return None, "A feasible solution was found, but it might not be optimal."
    else:
        return None, "No feasible solution found."

def main():
    print("Solving Integer Model (MIP) with CBC:")
    int_result, int_error = solve_integer_model()
    if int_result:
        print("Integer Model Optimal Solution:")
        print(int_result)
    else:
        print("Integer Model Error: " + int_error)
    
    print("\nSolving Relaxed Model (LP) with GLOP:")
    rel_result, rel_error = solve_relaxed_model()
    if rel_result:
        print("Relaxed Model Optimal Solution:")
        print(rel_result)
    else:
        print("Relaxed Model Error: " + rel_error)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving Integer Model (MIP) with CBC:
Integer Model Optimal Solution:
{'variables': {'NumberOfChopSaws': 8.0, 'NumberOfSteelCutters': 64.0}, 'objective': 72.0}

Solving Relaxed Model (LP) with GLOP:
Relaxed Model Optimal Solution:
{'variables': {'NumberOfChopSaws': 8.800000000000002, 'NumberOfSteelCutters': 59.999999999999986}, 'objective': 68.79999999999998}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfChopSaws': 8.0, 'NumberOfSteelCutters': 64.0}, 'objective': 72.0}'''

