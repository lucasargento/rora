# Problem Description:
'''Problem description: A production company needs to transport their equipment and staff for a movie they are shooting using large mobile production units or small mobile production units. Large mobile production units can hold 6 people and takes up 2 parking spots whereas small mobile production units can hold only 2 people and takes up 1 parking spot. Movie stars prefer to have their small mobile production unit to share with a close staff, therefore at least 5 units must be small mobile units. However, due to logistic limitations, large mobile production units are more space efficient per spot, they must make up at least 75% of all vehicles. If the movie needs to transport 80 people, minimize the total number of parking spots required by this production.

Expected Output Schema:
{
  "variables": {
    "NumberLargeUnits": "float",
    "NumberSmallUnits": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Below is a complete formulation of the problem using the five-element modeling framework.

--------------------------------------------------

Sets:
• No explicit sets are needed since the decision is over two vehicle types (large and small). You can think of the vehicle types as an implicit set V = {Large, Small}.

Parameters:
• capacityLarge = 6           // Number of people that a large unit can transport [people/unit]
• capacitySmall = 2           // Number of people that a small unit can transport [people/unit]
• parkingLarge = 2            // Number of parking spots a large unit occupies [spots/unit]
• parkingSmall = 1            // Number of parking spots a small unit occupies [spots/unit]
• requiredPeople = 80         // Total number of people that must be transported [people]
• minSmallUnits = 5           // Minimum number of small mobile units required [units]
• minLargeFraction = 0.75     // Minimum required fraction of large units among all vehicles [dimensionless]

Variables:
• LargeUnits: number of large mobile production units used [integer, ≥ 0]
• SmallUnits: number of small mobile production units used [integer, ≥ 0]

Note: We assume that vehicles are integer quantities. If fractional vehicles are considered (e.g., for planning relaxations), change the type accordingly.

Objective:
• Minimize total parking spots required.
  Expressed as: Minimize TotalParking = parkingLarge * LargeUnits + parkingSmall * SmallUnits
  [Objective: minimize spots (units: spots)]

Constraints:
1. People transport capacity:
   capacityLarge * LargeUnits + capacitySmall * SmallUnits ≥ requiredPeople
   (Ensures that the chosen fleet can transport at least 80 people.)

2. Minimum small units requirement:
   SmallUnits ≥ minSmallUnits
   (At least 5 small units must be used.)

3. Large unit fleet composition constraint:
   The large units must be at least 75% of all vehicles. In equation form:
   LargeUnits / (LargeUnits + SmallUnits) ≥ minLargeFraction
   This inequality can be rearranged (assuming LargeUnits + SmallUnits > 0) to:
   LargeUnits ≥ (minLargeFraction / (1 - minLargeFraction)) * SmallUnits
   With minLargeFraction = 0.75, note that (0.75 / (1-0.75)) = 3, so this constraint becomes:
   LargeUnits ≥ 3 * SmallUnits

--------------------------------------------------

The following JSON schema summarizes the key decision variables and the objective value:

{
  "variables": {
    "NumberLargeUnits": "integer (≥ 0)",
    "NumberSmallUnits": "integer (≥ 0)"
  },
  "objective": "Total parking spots used = 2 * NumberLargeUnits + 1 * NumberSmallUnits"
}

--------------------------------------------------

This formulation is now complete, self-contained, and fully reflects the requirements stated in the original problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    """Solve the production transportation problem treating vehicles as integers."""
    # Create MIP solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer Model: Solver not created.")
        return None

    # Parameters
    capacity_large = 6        # people per large unit
    capacity_small = 2        # people per small unit
    parking_large = 2         # parking spots per large unit
    parking_small = 1         # parking spots per small unit
    required_people = 80      # total number of people to transport
    min_small_units = 5       # at least 5 small units required
    min_large_fraction = 0.75 # large units must be at least 75% of all vehicles
    # With fraction 0.75, constraint becomes: LargeUnits >= (0.75/(1-0.75))*SmallUnits = 3*SmallUnits

    # Decision variables: nonnegative integers
    large_units = solver.IntVar(0, solver.infinity(), 'LargeUnits')
    small_units = solver.IntVar(0, solver.infinity(), 'SmallUnits')

    # Constraint 1: People capacity
    solver.Add(capacity_large * large_units + capacity_small * small_units >= required_people)
    
    # Constraint 2: Minimum small units 
    solver.Add(small_units >= min_small_units)
    
    # Constraint 3: Large unit fleet composition: LargeUnits >= 3 * SmallUnits
    solver.Add(large_units >= 3 * small_units)

    # Objective: Minimize total parking spots = 2*LargeUnits + 1*SmallUnits
    objective = solver.Objective()
    objective.SetCoefficient(large_units, parking_large)
    objective.SetCoefficient(small_units, parking_small)
    objective.SetMinimization()

    # Solve the model
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumberLargeUnits'] = int(large_units.solution_value())
        result['NumberSmallUnits'] = int(small_units.solution_value())
        result['objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found for the integer model."
    return result

def solve_continuous_model():
    """Solve the production transportation problem treating vehicles as continuous variables.
       This can represent a planning relaxation where vehicles are fractional."""
    # Create LP solver with GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Continuous Model: Solver not created.")
        return None

    # Parameters
    capacity_large = 6
    capacity_small = 2
    parking_large = 2
    parking_small = 1
    required_people = 80
    min_small_units = 5
    min_large_fraction = 0.75  # leads to the constraint: LargeUnits >= 3 * SmallUnits

    # Decision variables: nonnegative continuous variables.
    large_units = solver.NumVar(0.0, solver.infinity(), 'LargeUnits')
    small_units = solver.NumVar(0.0, solver.infinity(), 'SmallUnits')

    # Constraint 1: People capacity
    solver.Add(capacity_large * large_units + capacity_small * small_units >= required_people)
    
    # Constraint 2: Minimum small units (even though continuous, we keep the lower bound)
    solver.Add(small_units >= min_small_units)
    
    # Constraint 3: Fleet composition constraint
    solver.Add(large_units >= 3 * small_units)

    # Objective: Minimize total parking spots = 2 * LargeUnits + 1 * SmallUnits
    objective = solver.Objective()
    objective.SetCoefficient(large_units, parking_large)
    objective.SetCoefficient(small_units, parking_small)
    objective.SetMinimization()

    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['NumberLargeUnits'] = large_units.solution_value()
        result['NumberSmallUnits'] = small_units.solution_value()
        result['objective'] = objective.Value()
    else:
        result['error'] = "No optimal solution found for the continuous model."
    return result

def main():
    print("Solving production transportation problem using two formulations.\n")
    
    # Solve the integer model (vehicles as integers)
    integer_result = solve_integer_model()
    print("Integer Model (Vehicles as Integers):")
    if integer_result is not None:
        if 'error' in integer_result:
            print("  Error:", integer_result['error'])
        else:
            print("  NumberLargeUnits =", integer_result['NumberLargeUnits'])
            print("  NumberSmallUnits =", integer_result['NumberSmallUnits'])
            print("  Total Parking Spots =", integer_result['objective'])
    else:
        print("  Integer model did not run.")
    
    print("\n---------------------------\n")
    
    # Solve the continuous model (planning relaxation with continuous vehicles)
    continuous_result = solve_continuous_model()
    print("Continuous Model (Vehicles as Continuous Variables):")
    if continuous_result is not None:
        if 'error' in continuous_result:
            print("  Error:", continuous_result['error'])
        else:
            print("  NumberLargeUnits =", continuous_result['NumberLargeUnits'])
            print("  NumberSmallUnits =", continuous_result['NumberSmallUnits'])
            print("  Total Parking Spots =", continuous_result['objective'])
    else:
        print("  Continuous model did not run.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solving production transportation problem using two formulations.

Integer Model (Vehicles as Integers):
  NumberLargeUnits = 15
  NumberSmallUnits = 5
  Total Parking Spots = 35.0

---------------------------

Continuous Model (Vehicles as Continuous Variables):
  NumberLargeUnits = 15.0
  NumberSmallUnits = 5.0
  Total Parking Spots = 35.0
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberLargeUnits': 15.0, 'NumberSmallUnits': 5.0}, 'objective': 35.0}'''

