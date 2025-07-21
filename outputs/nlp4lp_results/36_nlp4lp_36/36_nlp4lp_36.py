# Problem Description:
'''Problem description: A farmer has 500 acres of land to grow turnips and pumpkins. Turnips require 50 minutes of watering and $80 worth of pesticide per acre. Pumpkins require 90 minutes of watering and $50 worth of pesticide per acre. The farmer has 40000 minutes available for watering and $34000 available to spend on pesticide. If the revenue per acre of turnips is $300 and the revenue per acre of pumpkins is $450, how many acres of each should he grow to maximize his revenue.

Expected Output Schema:
{
  "variables": {
    "LandTurnips": "float",
    "LandPumpkins": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- Crop: set of crops = {Turnips, Pumpkins}

Parameters:
- acres_available: Total available land [acres] = 500
- watering_time: Minutes of watering required per acre for each crop [minutes/acre]
  • Turnips: 50
  • Pumpkins: 90
- pesticide_cost: Pesticide cost per acre for each crop [USD/acre]
  • Turnips: 80
  • Pumpkins: 50
- revenue: Revenue per acre for each crop [USD/acre]
  • Turnips: 300
  • Pumpkins: 450
- total_watering_minutes: Total available watering time [minutes] = 40000
- total_pesticide_budget: Total available pesticide budget [USD] = 34000

Variables:
- LandTurnips: Acres planted with Turnips [continuous, acres, >= 0]
- LandPumpkins: Acres planted with Pumpkins [continuous, acres, >= 0]

Objective:
- Maximize total revenue, defined as:
  Total Revenue = (300 * LandTurnips) + (450 * LandPumpkins)

Constraints:
1. Land constraint:
  LandTurnips + LandPumpkins ≤ 500
2. Watering time constraint:
  (50 * LandTurnips) + (90 * LandPumpkins) ≤ 40000
3. Pesticide budget constraint:
  (80 * LandTurnips) + (50 * LandPumpkins) ≤ 34000

------------------------------------------------------
For clarity, note that all units are consistent:
- Acre measurements for land.
- Minutes for watering.
- USD per acre for costs and revenue.
This formulation models the decision of how many acres to allocate to turnips and pumpkins in order to maximize the farmer's revenue under the given resource constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def model1():
    # Create the linear solver using GLOP.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None, None

    # Define decision variables:
    # LandTurnips: Acres planted with Turnips (>= 0)
    # LandPumpkins: Acres planted with Pumpkins (>= 0)
    land_turnips = solver.NumVar(0.0, solver.infinity(), 'LandTurnips')
    land_pumpkins = solver.NumVar(0.0, solver.infinity(), 'LandPumpkins')

    # Constraints:

    # 1. Land constraint: LandTurnips + LandPumpkins <= 500
    solver.Add(land_turnips + land_pumpkins <= 500)

    # 2. Watering time constraint: (50 * LandTurnips) + (90 * LandPumpkins) <= 40000
    solver.Add(50 * land_turnips + 90 * land_pumpkins <= 40000)

    # 3. Pesticide budget constraint: (80 * LandTurnips) + (50 * LandPumpkins) <= 34000
    solver.Add(80 * land_turnips + 50 * land_pumpkins <= 34000)

    # Objective: Maximize revenue = 300*LandTurnips + 450*LandPumpkins
    objective = solver.Objective()
    objective.SetCoefficient(land_turnips, 300)
    objective.SetCoefficient(land_pumpkins, 450)
    objective.SetMaximization()

    # Solve the problem.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "LandTurnips": land_turnips.solution_value(),
            "LandPumpkins": land_pumpkins.solution_value()
        }
        objective_value = objective.Value()
        return solution, objective_value
    else:
        print("The problem does not have an optimal solution.")
        return None, None

def main():
    # Only one formulation is provided in the mathematical description,
    # so we only create one separate model implementation.
    solution1, objective1 = model1()
    if solution1 is not None:
        print("Model 1 (Linear Programming Optimization) Results:")
        print({
            "variables": solution1,
            "objective": objective1
        })
    else:
        print("Model 1: No optimal solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Model 1 (Linear Programming Optimization) Results:
{'variables': {'LandTurnips': 124.99999999999997, 'LandPumpkins': 375.00000000000006}, 'objective': 206250.00000000003}
'''

'''Expected Output:
Expected solution

: {'variables': {'LandTurnips': 125.0, 'LandPumpkins': 375.0}, 'objective': 206250.0}'''

