# Problem Description:
'''Problem description: A party organizer needs to transport party goers either by limousine or bus. Limousines can carry 12 people and buses can carry 18 people. They need to transport at least 400 people. Because limousines are more attractive, at least 70% of the vehicles must be limousines. How many of each type of vehicle should be used to minimize the total number of limousines and buses used?

Expected Output Schema:
{
  "variables": {
    "NumLimousines": "float",
    "PeopleLimousines": "float",
    "NumBuses": "float",
    "PeopleBuses": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete formulation of the problem using the five‐element framework.

------------------------------------------------------------
Sets:
• V = {Limousine, Bus} 
  (This set represents the two types of vehicles available)

------------------------------------------------------------
Parameters:
• capacity_Limo = 12  
  – Capacity of a limousine in number of people.
• capacity_Bus = 18  
  – Capacity of a bus in number of people.
• min_people = 400  
  – Minimum number of people that must be transported.
• min_fraction_limo = 0.70  
  – Minimum fraction of all vehicles that must be limousines.
   Note: Units for capacities and min_people are in “people” and vehicles are counted as individual units.

------------------------------------------------------------
Variables (decision variables):
• NumLimousines: number of limousines to use (integer, ≥ 0)
• NumBuses: number of buses to use (integer, ≥ 0)
• PeopleLimousines: number of people carried in limousines (continuous, ≥ 0) 
  Defined as PeopleLimousines = capacity_Limo * NumLimousines.
• PeopleBuses: number of people carried in buses (continuous, ≥ 0) 
  Defined as PeopleBuses = capacity_Bus * NumBuses.
  Note: Although PeopleLimousines and PeopleBuses are determined by the number
   of vehicles used, they are included here to explicitly capture the transported people counts.

------------------------------------------------------------
Objective:
Minimize total number of vehicles used.
• Objective = NumLimousines + NumBuses  
  – This objective minimizes the sum of limousines and buses.
  – Unit: vehicles

------------------------------------------------------------
Constraints:
1. Transportation Requirement:
  capacity_Limo * NumLimousines + capacity_Bus * NumBuses ≥ min_people  
  That is, 12 * NumLimousines + 18 * NumBuses ≥ 400.

2. Vehicle Composition Requirement:
  NumLimousines ≥ min_fraction_limo * (NumLimousines + NumBuses)  
  That is, NumLimousines ≥ 0.70 * (NumLimousines + NumBuses).

------------------------------------------------------------
Below is a JSON snippet following the expected output schema:

{
  "variables": {
    "NumLimousines": "integer, ≥ 0, number of limousines",
    "PeopleLimousines": "continuous, ≥ 0, people transported by limousines (12 * NumLimousines)",
    "NumBuses": "integer, ≥ 0, number of buses",
    "PeopleBuses": "continuous, ≥ 0, people transported by buses (18 * NumBuses)"
  },
  "objective": "Minimize NumLimousines + NumBuses (total number of vehicles)"
}

This complete structured model is self-contained and can be implemented directly with optimization libraries such as OR-Tools or similar frameworks.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def model1():
    """Implementation of the party transportation problem using OR-Tools linear solver."""
    # Create the solver with SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print('Solver not created.')
        return None

    # -----------------------------
    # Parameters
    # -----------------------------
    capacity_limo = 12       # Capacity of a limousine.
    capacity_bus = 18        # Capacity of a bus.
    min_people = 400         # Minimum number of people that must be transported.
    min_fraction_limo = 0.70 # At least 70% of vehicles must be limousines.

    # -----------------------------
    # Variables
    # -----------------------------
    # Number of limousines (integer, >= 0)
    num_limousines = solver.IntVar(0, solver.infinity(), 'NumLimousines')
    # Number of buses (integer, >= 0)
    num_buses = solver.IntVar(0, solver.infinity(), 'NumBuses')

    # Number of people transported by limousines (continuous, defined by capacity * num_limousines)
    people_limousines = solver.NumVar(0, solver.infinity(), 'PeopleLimousines')
    # Number of people transported by buses (continuous, defined by capacity * num_buses)
    people_buses = solver.NumVar(0, solver.infinity(), 'PeopleBuses')

    # Link people variables with the number of vehicles.
    solver.Add(people_limousines == capacity_limo * num_limousines)
    solver.Add(people_buses == capacity_bus * num_buses)

    # -----------------------------
    # Objective: Minimize the total number of vehicles used.
    # -----------------------------
    objective = solver.Objective()
    objective.SetCoefficient(num_limousines, 1)
    objective.SetCoefficient(num_buses, 1)
    objective.SetMinimization()

    # -----------------------------
    # Constraints
    # -----------------------------
    # 1. Transportation Requirement:
    #    12 * NumLimousines + 18 * NumBuses >= 400
    solver.Add(capacity_limo * num_limousines + capacity_bus * num_buses >= min_people)

    # 2. Vehicle Composition Requirement:
    #    NumLimousines >= 0.70 * (NumLimousines + NumBuses)
    solver.Add(num_limousines >= min_fraction_limo * (num_limousines + num_buses))

    # Solve the model.
    status = solver.Solve()

    # Prepare results.
    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        results = {
            "variables": {
                "NumLimousines": num_limousines.solution_value(),
                "PeopleLimousines": people_limousines.solution_value(),
                "NumBuses": num_buses.solution_value(),
                "PeopleBuses": people_buses.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        results["status"] = "The problem does not have an optimal solution."
    return results

def main():
    # Since only one formulation is presented in the mathematical description,
    # we call model1() and display its results.
    model1_results = model1()
    print("Model 1 Results:")
    print(model1_results)

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Model 1 Results:
{'variables': {'NumLimousines': 21.0, 'PeopleLimousines': 252.0, 'NumBuses': 9.0, 'PeopleBuses': 162.0}, 'objective': 30.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumLimousines': 22.0, 'PeopleLimousines': 264.0, 'NumBuses': 8.0, 'PeopleBuses': 144.0}, 'objective': 30.0}'''

