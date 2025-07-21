# Problem Description:
'''Problem description: A music company produces two types of digital keyboards, one is full-weighted and another is semi-weighted. Both keyboards are sold for $2800 and $2400 respectively. There are about 3500 oscillator chips available every day from which the full-weighted version requires 20 chips while the semi-weighted version requires 15 chips. The company has a total of 6 working hours a day. Both of these keyboards require a production time of 1.2 hours. What should be the manufacturing quantity for each of the keyboards to maximize the total revenue?

Expected Output Schema:
{
  "variables": {
    "QuantityFullWeighted": "float",
    "QuantitySemiWeighted": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- K: set of keyboard types = {FullWeighted, SemiWeighted}

Parameters:
- price[FullWeighted] = 2800 (revenue per full-weighted keyboard produced in USD per unit)
- price[SemiWeighted] = 2400 (revenue per semi-weighted keyboard produced in USD per unit)
- chipsNeeded[FullWeighted] = 20 (oscillator chips required per full-weighted keyboard, chips per unit)
- chipsNeeded[SemiWeighted] = 15 (oscillator chips required per semi-weighted keyboard, chips per unit)
- totalChips = 3500 (total available oscillator chips per day, in chips)
- productionTimePerUnit = 1.2 (production time required per keyboard, in hours per unit; same for both types)
- totalProductionTime = 6 (total available production time per day, in hours)

Variables:
- QuantityFullWeighted: number of full-weighted keyboards to produce (continuous nonnegative variable, in units)
- QuantitySemiWeighted: number of semi-weighted keyboards to produce (continuous nonnegative variable, in units)

Objective:
- Maximize total revenue = price[FullWeighted] * QuantityFullWeighted + price[SemiWeighted] * QuantitySemiWeighted

Constraints:
1. Chip availability constraint:
   (chipsNeeded[FullWeighted] * QuantityFullWeighted) + (chipsNeeded[SemiWeighted] * QuantitySemiWeighted) ≤ totalChips
2. Production time constraint:
   productionTimePerUnit * (QuantityFullWeighted + QuantitySemiWeighted) ≤ totalProductionTime

Comments:
- It is assumed that fractional production quantities are acceptable (continuous decision variables). If only integer quantities are allowed, then the variables should be defined as integer ≥ 0.
- All time and chip units are consistent with the provided data (hours for production time, chips for chip usage, USD for revenue).
- The objective function considers only revenue since no costs are given.

Expected Output Schema:
{
  "variables": {
    "QuantityFullWeighted": "float",
    "QuantitySemiWeighted": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_continuous_production():
    # Create the linear solver with the GLOP backend (for continuous variables).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, "Solver not created."

    # Parameters
    price_full = 2800         # revenue per full-weighted keyboard produced (USD)
    price_semi = 2400         # revenue per semi-weighted keyboard produced (USD)
    chips_needed_full = 20    # oscillator chips required per full-weighted keyboard
    chips_needed_semi = 15    # oscillator chips required per semi-weighted keyboard
    total_chips = 3500        # total available oscillator chips per day
    production_time_per_unit = 1.2  # production time required per keyboard in hours
    total_production_time = 6       # total available production time per day in hours

    # Variables: Since fractional production quantities are acceptable, we use continuous variables.
    quantity_full = solver.NumVar(0.0, solver.infinity(), 'QuantityFullWeighted')
    quantity_semi = solver.NumVar(0.0, solver.infinity(), 'QuantitySemiWeighted')

    # Objective: Maximize total revenue.
    objective = solver.Objective()
    objective.SetCoefficient(quantity_full, price_full)
    objective.SetCoefficient(quantity_semi, price_semi)
    objective.SetMaximization()

    # Constraint 1: Chip availability.
    ct_chips = solver.Constraint(-solver.infinity(), total_chips)
    ct_chips.SetCoefficient(quantity_full, chips_needed_full)
    ct_chips.SetCoefficient(quantity_semi, chips_needed_semi)

    # Constraint 2: Production time.
    ct_time = solver.Constraint(-solver.infinity(), total_production_time)
    ct_time.SetCoefficient(quantity_full, production_time_per_unit)
    ct_time.SetCoefficient(quantity_semi, production_time_per_unit)

    # Solve the model.
    status = solver.Solve()

    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result = {
            "variables": {
                "QuantityFullWeighted": quantity_full.solution_value(),
                "QuantitySemiWeighted": quantity_semi.solution_value()
            },
            "objective": objective.Value()
        }
    else:
        result = {"status": "The problem does not have an optimal solution."}

    return result, None

def main():
    # In this task we have one formulation (continuous production variables)
    continuous_result, error = solve_continuous_production()

    print("Continuous Production Formulation Results:")
    if error:
        print(error)
    else:
        print(continuous_result)

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Continuous Production Formulation Results:
{'variables': {'QuantityFullWeighted': 5.000000000000001, 'QuantitySemiWeighted': 0.0}, 'objective': 14000.000000000002}
'''

'''Expected Output:
Expected solution

: {'variables': {'QuantityFullWeighted': 5.0, 'QuantitySemiWeighted': 0.0}, 'objective': 14000.0}'''

