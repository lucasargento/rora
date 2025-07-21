# Problem Description:
'''Problem description: A dietician recommends her client eat blueberries and strawberries to meet her anti-oxidant and mineral requirement. A pack of blueberries contains 3 units of anti-oxidants and 5 units of minerals. A pack of strawberries contains 1 unit of anti-oxidants and 7 units of minerals. The client must get at least 90 units of anti-oxidants and 100 units of minerals. In addition, because blueberries are not in season, the dietician recommend she eats at least 3 times as many packs of strawberries as blueberries. If a pack of blueberries contains 5 grams of sugar and a pack of strawberries contains 7 grams of sugar, how many of packs of each should she consume to minimize her sugar intake?

Expected Output Schema:
{
  "variables": {
    "NumberOfBlueberryPacks": "float",
    "NumberOfStrawberryPacks": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Fruit: {Blueberries, Strawberries}

Parameters:
- antioxidant_per_pack: 
  - Blueberries = 3 units per pack
  - Strawberries = 1 unit per pack
- mineral_per_pack:
  - Blueberries = 5 units per pack
  - Strawberries = 7 units per pack
- sugar_per_pack:
  - Blueberries = 5 grams per pack
  - Strawberries = 7 grams per pack
- min_antioxidants = 90 units (total required)
- min_minerals = 100 units (total required)
- min_strawberry_ratio = 3 
  (This means the number of Strawberry packs should be at least 3 times the number of Blueberry packs)

Variables:
- NumberOfBlueberryPacks: integer variable, number of packs of blueberries to consume, with lower bound 0
- NumberOfStrawberryPacks: integer variable, number of packs of strawberries to consume, with lower bound 0

Objective:
- Minimize total sugar intake = (5 * NumberOfBlueberryPacks) + (7 * NumberOfStrawberryPacks)
  [Sugar is measured in grams]

Constraints:
1. Antioxidant requirement: (3 * NumberOfBlueberryPacks) + (1 * NumberOfStrawberryPacks) >= 90
2. Mineral requirement: (5 * NumberOfBlueberryPacks) + (7 * NumberOfStrawberryPacks) >= 100
3. Seasonal fruit ratio: NumberOfStrawberryPacks >= 3 * NumberOfBlueberryPacks

In summary, the model directs the dietician to choose nonnegative integer numbers for packs of blueberries and strawberries to minimize sugar intake while ensuring the client’s antioxidant and mineral needs are met and maintaining at least three times as many strawberry packs as blueberry packs.

Expected Output Schema:
{
  "variables": {
    "NumberOfBlueberryPacks": "integer ≥ 0",
    "NumberOfStrawberryPacks": "integer ≥ 0"
  },
  "objective": "Minimize (5 * NumberOfBlueberryPacks + 7 * NumberOfStrawberryPacks) grams of sugar"
}'''

# Generated Code:
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create the CBC solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return {"status": "Solver not available."}

    # Variables: nonnegative integers for packs.
    blueberry = solver.IntVar(0, solver.infinity(), 'NumberOfBlueberryPacks')
    strawberry = solver.IntVar(0, solver.infinity(), 'NumberOfStrawberryPacks')

    # Constraint 1: Antioxidant requirement
    # 3 * NumberOfBlueberryPacks + 1 * NumberOfStrawberryPacks >= 90
    solver.Add(3 * blueberry + 1 * strawberry >= 90)

    # Constraint 2: Mineral requirement
    # 5 * NumberOfBlueberryPacks + 7 * NumberOfStrawberryPacks >= 100
    solver.Add(5 * blueberry + 7 * strawberry >= 100)

    # Constraint 3: At least three times as many strawberry packs as blueberry packs
    solver.Add(strawberry >= 3 * blueberry)

    # Objective: Minimize total sugar intake in grams
    # Sugar intake = 5 * blueberry + 7 * strawberry
    solver.Minimize(5 * blueberry + 7 * strawberry)

    status = solver.Solve()
    result = {}

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "NumberOfBlueberryPacks": int(blueberry.solution_value()),
                "NumberOfStrawberryPacks": int(strawberry.solution_value())
            },
            "objective": solver.Objective().Value()
        }
    else:
        result["status"] = "No optimal solution found or problem is infeasible."

    return result

def main():
    results = {}
    
    # Use Linear Solver implementation as the formulation is linear.
    linear_result = solve_with_linear_solver()
    results["Linear_Solver_Implementation"] = linear_result
    
    # Print results in a structured way.
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'Linear_Solver_Implementation': {'variables': {'NumberOfBlueberryPacks': 15, 'NumberOfStrawberryPacks': 45}, 'objective': 390.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfBlueberryPacks': 15.0, 'NumberOfStrawberryPacks': 45.0}, 'objective': 390.0}'''

