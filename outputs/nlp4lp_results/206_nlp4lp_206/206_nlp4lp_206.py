# Problem Description:
'''Problem description: A food delivery person can either have shifts on bikes or scooters. A shift on a bike can deliver 10 orders, takes 5 units of energy, and brings in $50 on tips because it is faster. A shift on a scooter can deliver 7 orders, takes 6 units of energy, and brings in $43 on tips.  The delivery person has available 40 shifts a month and has 230 units of energy and must bring at least 320 orders. He must have at least 5 shifts on a scooter because bikes are harder to get. How many shifts on each type of transportation should the delivery person schedule to maximize tips received?

Expected Output Schema:
{
  "variables": {
    "BikeShifts": "float",
    "ScooterShifts": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- T: set of transportation modes = {Bike, Scooter}

Parameters:
- orders_Bike = 10 orders per Bike shift
- orders_Scooter = 7 orders per Scooter shift
- energy_Bike = 5 energy units per Bike shift
- energy_Scooter = 6 energy units per Scooter shift
- tips_Bike = 50 dollars per Bike shift (tip revenue)
- tips_Scooter = 43 dollars per Scooter shift (tip revenue)
- max_shifts = 40 shifts available per month
- max_energy = 230 energy units available per month
- min_orders = 320 orders required per month
- min_scooter_shifts = 5 shifts minimum required for Scooter

Variables:
- BikeShifts: number of Bike shifts scheduled (integer ≥ 0)
- ScooterShifts: number of Scooter shifts scheduled (integer ≥ 0)

Objective:
- Maximize total_tips = (tips_Bike * BikeShifts) + (tips_Scooter * ScooterShifts)

Constraints:
1. Shift availability constraint:
   BikeShifts + ScooterShifts ≤ max_shifts
2. Energy capacity constraint:
   (energy_Bike * BikeShifts) + (energy_Scooter * ScooterShifts) ≤ max_energy
3. Minimum orders constraint:
   (orders_Bike * BikeShifts) + (orders_Scooter * ScooterShifts) ≥ min_orders
4. Scooter shift minimum constraint:
   ScooterShifts ≥ min_scooter_shifts

--------------------------------------------------
Expected Output Schema:
{
  "variables": {
    "BikeShifts": "float",   // non-negative integer representing number of bike shifts
    "ScooterShifts": "float" // non-negative integer representing number of scooter shifts
  },
  "objective": "float"       // maximum tip revenue in dollars
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_with_linear_solver():
    # Create solver using GLOP - since our variables are integer, use CBC_MIXED_INTEGER_PROGRAMMING.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    max_shifts = 40
    max_energy = 230
    min_orders = 320
    min_scooter_shifts = 5

    orders_bike = 10
    orders_scooter = 7
    energy_bike = 5
    energy_scooter = 6
    tips_bike = 50
    tips_scooter = 43

    # Variables: Number of shifts (non-negative integers)
    BikeShifts = solver.IntVar(0, max_shifts, 'BikeShifts')
    ScooterShifts = solver.IntVar(0, max_shifts, 'ScooterShifts')

    # Constraints:
    # 1. Total shifts constraint: BikeShifts + ScooterShifts <= max_shifts
    solver.Add(BikeShifts + ScooterShifts <= max_shifts)

    # 2. Energy capacity constraint: 5 * BikeShifts + 6 * ScooterShifts <= max_energy
    solver.Add(energy_bike * BikeShifts + energy_scooter * ScooterShifts <= max_energy)

    # 3. Minimum orders constraint: 10 * BikeShifts + 7 * ScooterShifts >= min_orders
    solver.Add(orders_bike * BikeShifts + orders_scooter * ScooterShifts >= min_orders)

    # 4. Scooter shift minimum constraint: ScooterShifts >= min_scooter_shifts
    solver.Add(ScooterShifts >= min_scooter_shifts)

    # Objective: maximize total tips = 50*BikeShifts + 43*ScooterShifts
    objective = solver.Objective()
    objective.SetCoefficient(BikeShifts, tips_bike)
    objective.SetCoefficient(ScooterShifts, tips_scooter)
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "BikeShifts": BikeShifts.solution_value(),
                "ScooterShifts": ScooterShifts.solution_value()
            },
            "objective": objective.Value()
        }
        return result
    else:
        print("The problem does not have an optimal solution.")
        return None

def main():
    print("Solving the Food Delivery Optimization Problem using Linear Programming (OR-Tools)...")
    result = solve_with_linear_solver()

    if result:
        print("Optimal solution found:")
        print("BikeShifts  =", result["variables"]["BikeShifts"])
        print("ScooterShifts =", result["variables"]["ScooterShifts"])
        print("Maximum Tips = $", result["objective"])
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving the Food Delivery Optimization Problem using Linear Programming (OR-Tools)...
Optimal solution found:
BikeShifts  = 35.0
ScooterShifts = 5.0
Maximum Tips = $ 1965.0
'''

'''Expected Output:
Expected solution

: {'variables': {'BikeShifts': 35.0, 'ScooterShifts': 5.0}, 'objective': 1965.0}'''

