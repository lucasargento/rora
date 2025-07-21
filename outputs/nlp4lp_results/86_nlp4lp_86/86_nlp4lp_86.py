# Problem Description:
'''Problem description: A drug company is making allergy pills and fever reducing pills in two factories, factory 1 and factory 2. Factory 1 produces 20 allergy pills and 15 fever reducing pills per hour. Factory 2 produces 10 allergy pills and 30 fever reducing pills per hour.  Factory 1 is much more efficient and only requires 20 units of a rare compound while factory 2 requires 30 units of a rare compound. The company only has available 1000 units of the rare compound. If the company must make at least 700 allergy pills and 600 fever reducing pills, how many hours should each factory be run to minimize the total time needed?

Expected Output Schema:
{
  "variables": {
    "OperationalLevel": {
      "0": "float",
      "1": "float"
    },
    "MaxOperatingHours": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- F: set of factories = {Factory1, Factory2}

Parameters:
- allergy_rate[f]: number of allergy pills produced per hour at factory f, with
  - allergy_rate[Factory1] = 20 pills/hour
  - allergy_rate[Factory2] = 10 pills/hour
- fever_rate[f]: number of fever reducing pills produced per hour at factory f, with
  - fever_rate[Factory1] = 15 pills/hour
  - fever_rate[Factory2] = 30 pills/hour
- compound_consumption[f]: units of the rare compound used per hour at factory f, with
  - compound_consumption[Factory1] = 20 units/hour
  - compound_consumption[Factory2] = 30 units/hour
- min_allergy: minimum required allergy pills = 700 pills
- min_fever: minimum required fever reducing pills = 600 pills
- max_compound: available units of rare compound = 1000 units

Variables:
- x[f]: operating hours for factory f (continuous nonnegative variable), where f ∈ F
  (x[Factory1] and x[Factory2])
- total_time: total operating time = x[Factory1] + x[Factory2] (continuous variable)

Objective:
- Minimize total_time = x[Factory1] + x[Factory2]
  (This represents the total hours required to run the factories.)

Constraints:
1. Allergy pills production constraint:
   20 * x[Factory1] + 10 * x[Factory2] ≥ 700
2. Fever reducing pills production constraint:
   15 * x[Factory1] + 30 * x[Factory2] ≥ 600
3. Rare compound availability constraint:
   20 * x[Factory1] + 30 * x[Factory2] ≤ 1000
4. Non-negativity constraints:
   x[Factory1] ≥ 0, x[Factory2] ≥ 0

----------------------------------------------------------
Model Comments:
- All production rates are given in pills per hour.
- Compound consumption rates are in units of the rare compound per hour.
- The objective minimizes the total operating hours across both factories.
- It is assumed that running a factory for one hour produces the stated quantities independently of the other factory.
- All units have been consistently applied according to the problem description.

----------------------------------------------------------
Expected Output Schema Mapping:
{
  "variables": {
    "OperationalLevel": {
      "0": "x[Factory1] (hours)",
      "1": "x[Factory2] (hours)"
    },
    "MaxOperatingHours": "total_time (hours)"
  },
  "objective": "Minimize total_time = x[Factory1] + x[Factory2]"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_program():
    # Create the linear solver with the GLOP backend
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return None

    # Variables
    # x_factory1: operating hours for Factory1
    # x_factory2: operating hours for Factory2
    x_factory1 = solver.NumVar(0.0, solver.infinity(), 'x_factory1')
    x_factory2 = solver.NumVar(0.0, solver.infinity(), 'x_factory2')

    # total_time is the sum of operating hours, this will be our objective function.
    # In a linear model, we don't need to define a separate variable for the sum; we can set the objective as x1 + x2.
    
    # Constraints
    # 1. Allergy pills production: 20*x_factory1 + 10*x_factory2 >= 700
    solver.Add(20 * x_factory1 + 10 * x_factory2 >= 700)
    
    # 2. Fever reducing pills production: 15*x_factory1 + 30*x_factory2 >= 600
    solver.Add(15 * x_factory1 + 30 * x_factory2 >= 600)
    
    # 3. Rare compound availability: 20*x_factory1 + 30*x_factory2 <= 1000
    solver.Add(20 * x_factory1 + 30 * x_factory2 <= 1000)
    
    # Objective: minimize total operating hours = x_factory1 + x_factory2
    solver.Minimize(x_factory1 + x_factory2)
    
    # Solve the model
    status = solver.Solve()
    
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        # Collect variables in expected output schema format
        # "OperationalLevel": { "0": "x[Factory1] (hours)", "1": "x[Factory2] (hours)" }
        # "MaxOperatingHours": "total_time (hours)" (which is x_factory1 + x_factory2)
        # "objective": "Minimize total_time = x[Factory1] + x[Factory2]"
        total_time = x_factory1.solution_value() + x_factory2.solution_value()
        result = {
            "model": "Linear Program (Factory Hours Minimization)",
            "variables": {
                "OperationalLevel": {
                    "0": x_factory1.solution_value(),  # Factory1 hours
                    "1": x_factory2.solution_value()     # Factory2 hours
                },
                "MaxOperatingHours": total_time
            },
            "objective": x_factory1.solution_value() + x_factory2.solution_value()
        }
    else:
        print("The solver could not find an optimal solution.")

    return result

def main():
    # Since the provided formulation is unique and unambiguous, we use only one implementation.
    lp_result = solve_linear_program()
    
    if lp_result:
        print("Solution for the Linear Programming Formulation:")
        print("------------------------------------------------")
        print(f"Factory1 Operating Hours (x[Factory1]): {lp_result['variables']['OperationalLevel']['0']:.2f} hours")
        print(f"Factory2 Operating Hours (x[Factory2]): {lp_result['variables']['OperationalLevel']['1']:.2f} hours")
        print(f"Total Operating Hours (MaxOperatingHours): {lp_result['variables']['MaxOperatingHours']:.2f} hours")
        print(f"Objective Value (Minimized Total Time): {lp_result['objective']:.2f} hours")
    else:
        print("No feasible solution was found.")

if __name__ == "__main__":
    main()

'''Execution Results:
SUCCESS:
Solution for the Linear Programming Formulation:
------------------------------------------------
Factory1 Operating Hours (x[Factory1]): 33.33 hours
Factory2 Operating Hours (x[Factory2]): 3.33 hours
Total Operating Hours (MaxOperatingHours): 36.67 hours
Objective Value (Minimized Total Time): 36.67 hours
'''

'''Expected Output:
Expected solution

: {'variables': {'OperationalLevel': {'0': 27.5, '1': 15.0}, 'MaxOperatingHours': 27.5}, 'objective': 27.5}'''

