# Problem Description:
'''Problem description: A shipping company can purchase regular and hybrid vans to make deliveries. A regular van can deliver 500 packages per day and produces 200 units of pollutants. A hybrid van can deliver 300 packages per day and produces 100 units of pollutants. Due to a new environmental law, they can produce at most 7000 units of pollutants per day. However, the company needs to be able to deliver at least 20000 packages per day. How many of each type of van should they buy to minimize the total number of vans needed?

Expected Output Schema:
{
  "variables": {
    "RegularVans": "float",
    "HybridVans": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- V: set of van types = {Regular, Hybrid}

Parameters:
- delivery_capacity[v] (packages per day): delivery_capacity[Regular] = 500, delivery_capacity[Hybrid] = 300
- pollutant_emission[v] (pollutant units per day): pollutant_emission[Regular] = 200, pollutant_emission[Hybrid] = 100
- max_pollutants (pollutant units per day) = 7000
- min_packages (packages per day) = 20000

Variables:
- x[v]: number of vans to purchase of type v (integer, nonnegative)
  - x[Regular]: number of regular vans
  - x[Hybrid]: number of hybrid vans

Objective:
- Minimize total vans = x[Regular] + x[Hybrid]

Constraints:
- Package delivery constraint: delivery_capacity[Regular] * x[Regular] + delivery_capacity[Hybrid] * x[Hybrid] >= min_packages
- Pollutant constraint: pollutant_emission[Regular] * x[Regular] + pollutant_emission[Hybrid] * x[Hybrid] <= max_pollutants

--------------------------------------------------------------------------------

Comments:
- All units are per day.
- Both decision variables are assumed integer though they are represented as float in the expected output schema.
- The model assumes each van works at full capacity every day.
- Alternative interpretation:
   If the van numbers are allowed to be fractional (due to leasing or averaging over days), then the variables can be continuous. Otherwise, they should be integer.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_integer_model():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Integer solver not available.")
        return None

    # Data
    delivery_capacity = {'Regular': 500, 'Hybrid': 300}
    pollutant_emission = {'Regular': 200, 'Hybrid': 100}
    max_pollutants = 7000
    min_packages = 20000

    # Variables: integer variables (nonnegative)
    regular = solver.IntVar(0, solver.infinity(), 'RegularVans')
    hybrid = solver.IntVar(0, solver.infinity(), 'HybridVans')

    # Objective: minimize total number of vans.
    solver.Minimize(regular + hybrid)

    # Constraints
    # Package delivery constraint: 500 * regular + 300 * hybrid >= 20000
    solver.Add(delivery_capacity['Regular'] * regular + delivery_capacity['Hybrid'] * hybrid >= min_packages)
    # Pollutant constraint: 200 * regular + 100 * hybrid <= 7000
    solver.Add(pollutant_emission['Regular'] * regular + pollutant_emission['Hybrid'] * hybrid <= max_pollutants)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "RegularVans": regular.solution_value(),
            "HybridVans": hybrid.solution_value(),
            "objective": (regular.solution_value() + hybrid.solution_value())
        }
    else:
        solution = None

    return solution

def solve_continuous_model():
    # Create the solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Continuous solver not available.")
        return None

    # Data
    delivery_capacity = {'Regular': 500, 'Hybrid': 300}
    pollutant_emission = {'Regular': 200, 'Hybrid': 100}
    max_pollutants = 7000
    min_packages = 20000

    # Variables: continuous variables (nonnegative)
    regular = solver.NumVar(0, solver.infinity(), 'RegularVans')
    hybrid = solver.NumVar(0, solver.infinity(), 'HybridVans')

    # Objective: minimize total number of vans.
    solver.Minimize(regular + hybrid)

    # Constraints
    solver.Add(delivery_capacity['Regular'] * regular + delivery_capacity['Hybrid'] * hybrid >= min_packages)
    solver.Add(pollutant_emission['Regular'] * regular + pollutant_emission['Hybrid'] * hybrid <= max_pollutants)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "RegularVans": regular.solution_value(),
            "HybridVans": hybrid.solution_value(),
            "objective": (regular.solution_value() + hybrid.solution_value())
        }
    else:
        solution = None

    return solution

def main():
    print("Integer Model (Mixed-Integer Programming) Solution:")
    int_solution = solve_integer_model()
    if int_solution:
        print("RegularVans:", int_solution["RegularVans"])
        print("HybridVans:", int_solution["HybridVans"])
        print("Total Vans (objective):", int_solution["objective"])
    else:
        print("No optimal solution found for the integer model.")

    print("\nContinuous Model (Fractional Variables) Solution:")
    cont_solution = solve_continuous_model()
    if cont_solution:
        print("RegularVans:", cont_solution["RegularVans"])
        print("HybridVans:", cont_solution["HybridVans"])
        print("Total Vans (objective):", cont_solution["objective"])
    else:
        print("No optimal solution found for the continuous model.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Integer Model (Mixed-Integer Programming) Solution:
RegularVans: 10.0
HybridVans: 50.0
Total Vans (objective): 60.0

Continuous Model (Fractional Variables) Solution:
RegularVans: 9.999999999999973
HybridVans: 50.00000000000005
Total Vans (objective): 60.00000000000002
'''

'''Expected Output:
Expected solution

: {'variables': {'RegularVans': 10.0, 'HybridVans': 50.0}, 'objective': 60.0}'''

