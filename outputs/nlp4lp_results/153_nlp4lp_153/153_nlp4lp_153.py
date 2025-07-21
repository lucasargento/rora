# Problem Description:
'''Problem description: A corn farmer sends his corn to the city by either tractor or car.  A tractor can carry 40 kg of corn while a car can carry 20 kg of corn. Since tractors are very slow, the number of cars used has to be at least twice the number of tractors used. If at least 500 kg of corn need to be sent to the city, minimize the total number of tractors and cars needed.

Expected Output Schema:
{
  "variables": {
    "NumberOfCarsUsed": "float",
    "NumberOfTractorsUsed": "float",
    "CornTractor": "float",
    "CornCar": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is one precise formulation of the problem using the five-element structure.

--------------------------------------------------------------------
Sets:
- Vehicles = {tractor, car}  
  (Although the vehicles are described individually, the set is provided for clarity. Each vehicle type has a fixed capacity.)

--------------------------------------------------------------------
Parameters:
- capacity_tractor = 40 (kg per tractor)  
- capacity_car = 20 (kg per car)  
- minimum_corn = 500 (kg required to be transported)  
- car_to_tractor_ratio = 2  
  (This means the number of cars must be at least twice the number of tractors.)

--------------------------------------------------------------------
Variables:
- NumberOfTractorsUsed, an integer ≥ 0  
  (Represents the number of tractors used for transporting corn.)
- NumberOfCarsUsed, an integer ≥ 0  
  (Represents the number of cars used for transporting corn.)
- CornTractor, a float ≥ 0  
  (Amount of corn transported by tractors in kg; defined as CornTractor = capacity_tractor * NumberOfTractorsUsed.)
- CornCar, a float ≥ 0  
  (Amount of corn transported by cars in kg; defined as CornCar = capacity_car * NumberOfCarsUsed.)

--------------------------------------------------------------------
Objective:
- Minimize total vehicles = NumberOfTractorsUsed + NumberOfCarsUsed  
  (The goal is to minimize the total count of vehicles used.)

--------------------------------------------------------------------
Constraints:
1. Total corn transported meets the minimum requirement:  
   CornTractor + CornCar ≥ minimum_corn  
   (In expanded form: 40 * NumberOfTractorsUsed + 20 * NumberOfCarsUsed ≥ 500)

2. Vehicle mix constraint (cars are used at least twice as much as tractors):  
   NumberOfCarsUsed ≥ car_to_tractor_ratio * NumberOfTractorsUsed  
   (In expanded form: NumberOfCarsUsed ≥ 2 * NumberOfTractorsUsed)

3. Definitions of corn transported by each vehicle type:  
   CornTractor = capacity_tractor * NumberOfTractorsUsed  
   CornCar = capacity_car * NumberOfCarsUsed

--------------------------------------------------------------------
The final JSON output following the Expected Output Schema is:

{
  "variables": {
    "NumberOfCarsUsed": "integer >= 0 (number of cars used)",
    "NumberOfTractorsUsed": "integer >= 0 (number of tractors used)",
    "CornTractor": "float >= 0 (corn transported by tractors in kg = 40 * NumberOfTractorsUsed)",
    "CornCar": "float >= 0 (corn transported by cars in kg = 20 * NumberOfCarsUsed)"
  },
  "objective": "Minimize total vehicles = NumberOfTractorsUsed + NumberOfCarsUsed"
}

This complete model is now ready for implementation in a coding environment.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver using the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return None

    # Parameters
    capacity_tractor = 40  # kg per tractor
    capacity_car = 20      # kg per car
    minimum_corn = 500     # kg minimum to be transported
    ratio = 2              # cars must be at least 2 times the tractors

    # Decision Variables
    # We use integer decision variables for vehicles.
    tractors = solver.IntVar(0, solver.infinity(), 'NumberOfTractorsUsed')
    cars = solver.IntVar(0, solver.infinity(), 'NumberOfCarsUsed')
    # Additional variables representing the corn transported by each vehicle type.
    # They are linked to the number of vehicles by a definition constraint.
    corn_tractor = solver.NumVar(0, solver.infinity(), 'CornTractor')
    corn_car = solver.NumVar(0, solver.infinity(), 'CornCar')

    # Constraints
    # Link corn transported with number of vehicles:
    solver.Add(corn_tractor == capacity_tractor * tractors)
    solver.Add(corn_car == capacity_car * cars)
    # Total corn transported must be at least the minimum required.
    solver.Add(corn_tractor + corn_car >= minimum_corn)
    # Rule: number of cars >= 2 * number of tractors.
    solver.Add(cars >= ratio * tractors)

    # Objective: minimize the total number of vehicles used.
    solver.Minimize(tractors + cars)

    # Solve the model.
    status = solver.Solve()

    # Check the result status.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        result = {
            "Model": "Linear Model using ortools.linear_solver",
            "Solution": {
                "NumberOfTractorsUsed": tractors.solution_value(),
                "NumberOfCarsUsed": cars.solution_value(),
                "CornTractor": corn_tractor.solution_value(),
                "CornCar": corn_car.solution_value(),
                "ObjectiveValue": (tractors.solution_value() + cars.solution_value())
            }
        }
        return result
    else:
        print("No feasible solution found.")
        return None

def main():
    # Currently there's one formulation so we only call one model.
    result1 = solve_linear_model()

    # Print the results in a structured way.
    print("===================================")
    print("Results for Model Implementation 1:")
    print("===================================")
    if result1:
        print("Model Description:", result1["Model"])
        print("Solution:")
        print("  NumberOfTractorsUsed =", result1["Solution"]["NumberOfTractorsUsed"])
        print("  NumberOfCarsUsed     =", result1["Solution"]["NumberOfCarsUsed"])
        print("  CornTractor         =", result1["Solution"]["CornTractor"], "kg")
        print("  CornCar             =", result1["Solution"]["CornCar"], "kg")
        print("  Objective Value     =", result1["Solution"]["ObjectiveValue"])
    else:
        print("No feasible solution found for Model Implementation 1.")
    
if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
===================================
Results for Model Implementation 1:
===================================
Model Description: Linear Model using ortools.linear_solver
Solution:
  NumberOfTractorsUsed = 6.0
  NumberOfCarsUsed     = 13.0
  CornTractor         = 240.0 kg
  CornCar             = 260.0 kg
  Objective Value     = 19.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberOfCarsUsed': 13.0, 'NumberOfTractorsUsed': 6.0, 'CornTractor': 240.0, 'CornCar': 260.0}, 'objective': 19.0}'''

