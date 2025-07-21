# Problem Description:
'''Problem description: A company in the middle east delivers their packages to customers on camels and horses. A camel can carry 50 packages while a horse can carry 60 packages. A camel requires 20 units of food while a horse requires 30 units of food. The company needs to deliver at least 1000 packages and they have 450 units of food available. Since horses are not as suited for the hot climate, the number of horses cannot exceed the number of camels. How many of each animal should be used to minimize the total number of animals?

Expected Output Schema:
{
  "variables": {
    "NumberOfCamels": "float",
    "NumberOfHorses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- AnimalTypes: set of animal types = {Camel, Horse}

Parameters:
- capacity[AnimalTypes]:
  • Camel: number of packages a camel can carry = 50 (packages per camel)
  • Horse: number of packages a horse can carry = 60 (packages per horse)
- foodRequirement[AnimalTypes]:
  • Camel: units of food required per camel = 20 (food units per camel)
  • Horse: units of food required per horse = 30 (food units per horse)
- requiredPackages: minimum number of packages to be delivered = 1000 (packages)
- availableFood: total available food = 450 (food units)

Variables:
- NumberOfCamels: number of camels to use, non-negative integer (units)
- NumberOfHorses: number of horses to use, non-negative integer (units)

Objective:
- Minimize total animals used = NumberOfCamels + NumberOfHorses

Constraints:
1. Package delivery constraint:
   50 * NumberOfCamels + 60 * NumberOfHorses >= requiredPackages  
   (Total delivered packages must be at least 1000.)

2. Food availability constraint:
   20 * NumberOfCamels + 30 * NumberOfHorses <= availableFood  
   (Total food required by animals must not exceed 450 food units.)

3. Horse climate suitability constraint:
   NumberOfHorses <= NumberOfCamels  
   (Due to horses being less suited for the hot climate, their number cannot exceed the number of camels.)

Comments:
- All units are consistent as stated (packages for capacity, food units for food requirements).
- Although animals are inherently integer, if required by solver, NumberOfCamels and NumberOfHorses should be defined as integer decision variables.

Expected Output Schema:
{
  "variables": {
    "NumberOfCamels": "float",
    "NumberOfHorses": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return None, None, "Solver not created."

    # PARAMETERS
    # Package capacities.
    capacity_camel = 50  # packages per camel
    capacity_horse = 60  # packages per horse
    # Food requirements.
    food_camel = 20  # food units per camel
    food_horse = 30  # food units per horse
    # Requirements.
    required_packages = 1000  # packages
    available_food = 450      # food units

    # VARIABLES: non-negative integers.
    camels = solver.IntVar(0, solver.infinity(), 'NumberOfCamels')
    horses = solver.IntVar(0, solver.infinity(), 'NumberOfHorses')

    # CONSTRAINTS
    # 1. Package delivery constraint:
    #    50 * NumberOfCamels + 60 * NumberOfHorses >= 1000
    solver.Add(capacity_camel * camels + capacity_horse * horses >= required_packages)

    # 2. Food availability constraint:
    #    20 * NumberOfCamels + 30 * NumberOfHorses <= 450
    solver.Add(food_camel * camels + food_horse * horses <= available_food)

    # 3. Horse climate suitability constraint:
    #    NumberOfHorses <= NumberOfCamels
    solver.Add(horses <= camels)

    # OBJECTIVE: Minimize total animals = NumberOfCamels + NumberOfHorses.
    objective = solver.Objective()
    objective.SetCoefficient(camels, 1)
    objective.SetCoefficient(horses, 1)
    objective.SetMinimization()

    # SOLVE the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberOfCamels": camels.solution_value(),
            "NumberOfHorses": horses.solution_value()
        }
        # Objective value: total animals used.
        total_animals = objective.Value()
        return solution, total_animals, None
    else:
        return None, None, "The problem does not have an optimal solution."

def main():
    results = {}

    # Implementation 1: Using the linear solver formulation.
    sol1, obj1, error1 = solve_linear_model()
    if error1:
        results["LinearModel"] = {"error": error1}
    else:
        results["LinearModel"] = {
            "variables": sol1,
            "objective": obj1
        }
    
    # If additional formulations were provided, they would be solved in separate blocks.
    # For now, we have only one formulation.

    # Print the results in a structured format.
    print(results)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{'LinearModel': {'variables': {'NumberOfCamels': 12.0, 'NumberOfHorses': 7.0}, 'objective': 19.0}}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfCamels': 12.0, 'NumberOfHorses': 7.0}, 'objective': 19.0}'''

