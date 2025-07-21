# Problem Description:
'''Problem description: An autobody shop needs to purchase two types of car jacks, an automatic electric one, or a gas-powered one. The automatic electric one can process 5 cars every hour and uses 6 units of electricity whereas the gas-powered one can process 4 cars each hour using 7 units of gas. Since there is a limit to how many automatic electric ones there can be due to the limited number of power outlets, the shop must use less than 15 automatic electric ones. The shop can use at most 50 units of electricity and 80 units of gas. How many of each type of jack should the shop purchase to maximize the amount of cars processed every hour?

Expected Output Schema:
{
  "variables": {
    "AutoElectricJacksUsed": "float",
    "GasPoweredJacksUsed": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- J: set of jack types = {AutoElectric, GasPowered}

Parameters:
- processing_rate_AutoElectric: number of cars processed per hour by one automatic electric jack = 5 [cars/hour]
- processing_rate_GasPowered: number of cars processed per hour by one gas-powered jack = 4 [cars/hour]
- electricity_consumption_AutoElectric: units of electricity used per automatic electric jack = 6 [electricity units per jack]
- gas_consumption_GasPowered: units of gas used per gas-powered jack = 7 [gas units per jack]
- max_electricity: total available units of electricity = 50 [electricity units]
- max_gas: total available units of gas = 80 [gas units]
- max_AutoElectric_units: maximum allowed number of automatic electric jacks (due to outlet limitations) = 14 [jacks]
  (Note: "less than 15" is interpreted as at most 14 units)

Variables:
- AutoElectricJacksUsed: number of automatic electric jacks to purchase [integer, ≥ 0]
- GasPoweredJacksUsed: number of gas-powered jacks to purchase [integer, ≥ 0]

Objective:
- Maximize total_cars_processed = (processing_rate_AutoElectric * AutoElectricJacksUsed) + (processing_rate_GasPowered * GasPoweredJacksUsed)
  [cars processed per hour]

Constraints:
1. Outlet constraint for automatic electric jacks:
   AutoElectricJacksUsed ≤ max_AutoElectric_units
2. Electricity availability constraint:
   electricity_consumption_AutoElectric * AutoElectricJacksUsed ≤ max_electricity
3. Gas availability constraint:
   gas_consumption_GasPowered * GasPoweredJacksUsed ≤ max_gas
4. Non-negativity and integrality:
   AutoElectricJacksUsed, GasPoweredJacksUsed are integer and ≥ 0

This completes the structured mathematical model for the autobody shop problem.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def solve_with_linear_solver():
    # Create the MIP solver with CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Linear solver not available.")
        return None

    # Parameters
    processing_rate_AE = 5      # cars per hour per auto electric jack
    processing_rate_GP = 4      # cars per hour per gas powered jack
    electricity_consumption_AE = 6  # units of electricity per auto electric jack
    gas_consumption_GP = 7          # units of gas per gas powered jack
    max_electricity = 50            # total units of electricity available
    max_gas = 80                    # total units of gas available
    max_AE_units = 14               # maximum auto electric jacks allowed (less than 15)

    # Decision variables
    # We need integer nonnegative, so lower bound 0 and integer type.
    auto_electric = solver.IntVar(0, max_AE_units, 'AutoElectricJacksUsed')
    # Note: gas powered jacks upper bound by resource constraint, but set a large upper bound.
    gas_powered = solver.IntVar(0, solver.infinity(), 'GasPoweredJacksUsed')

    # Constraints
    # Electricity constraint for auto electric jacks:
    solver.Add(electricity_consumption_AE * auto_electric <= max_electricity)
    # Gas constraint for gas powered jacks:
    solver.Add(gas_consumption_GP * gas_powered <= max_gas)

    # Note: The outlet constraint for auto electric jacks is already implied by the variable bound.
    
    # Objective: Maximize total number of cars processed per hour.
    objective = solver.Objective()
    objective.SetCoefficient(auto_electric, processing_rate_AE)
    objective.SetCoefficient(gas_powered, processing_rate_GP)
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "AutoElectricJacksUsed": auto_electric.solution_value(),
            "GasPoweredJacksUsed": gas_powered.solution_value(),
            "objective": objective.Value()
        }
        return solution
    else:
        print("The linear (MIP) model did not find an optimal solution.")
        return None

def solve_with_cp_sat():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    processing_rate_AE = 5      # cars per hour per auto electric jack
    processing_rate_GP = 4      # cars per hour per gas powered jack
    electricity_consumption_AE = 6  # units of electricity per auto electric jack
    gas_consumption_GP = 7          # units of gas per gas powered jack
    max_electricity = 50            # total units of electricity available
    max_gas = 80                    # total units of gas available
    max_AE_units = 14               # maximum auto electric jacks allowed (less than 15)

    # Decision variables: CP-SAT requires integer variables.
    auto_electric = model.NewIntVar(0, max_AE_units, 'AutoElectricJacksUsed')
    # For gas powered, define a reasonable upper bound from gas constraint: floor(80/7)=11, but to be safe use 80.
    gas_powered = model.NewIntVar(0, max_gas, 'GasPoweredJacksUsed')

    # Constraints
    # Electricity constraint for auto electric jacks.
    # 6 * auto_electric <= 50 => auto_electric <= 50/6. 
    model.Add(electricity_consumption_AE * auto_electric <= max_electricity)
    # Gas constraint for gas powered jacks.
    model.Add(gas_consumption_GP * gas_powered <= max_gas)

    # Objective: Maximize total cars processed per hour.
    # CP-SAT requires objectives to be linear integer expressions.
    total_cars = processing_rate_AE * auto_electric + processing_rate_GP * gas_powered
    model.Maximize(total_cars)

    # Solve using CpSolver.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {
            "AutoElectricJacksUsed": solver.Value(auto_electric),
            "GasPoweredJacksUsed": solver.Value(gas_powered),
            "objective": solver.ObjectiveValue()
        }
        return solution
    else:
        print("The CP-SAT model did not find a feasible solution.")
        return None

def main():
    print("Solving using OR-Tools Linear Solver (MIP):")
    linear_solution = solve_with_linear_solver()
    if linear_solution is not None:
        print("Solution:")
        print("  AutoElectricJacksUsed =", linear_solution["AutoElectricJacksUsed"])
        print("  GasPoweredJacksUsed   =", linear_solution["GasPoweredJacksUsed"])
        print("  Total cars processed    =", linear_solution["objective"])
    else:
        print("No optimal solution found in linear solver.")

    print("\nSolving using OR-Tools CP-SAT Solver:")
    cp_sat_solution = solve_with_cp_sat()
    if cp_sat_solution is not None:
        print("Solution:")
        print("  AutoElectricJacksUsed =", cp_sat_solution["AutoElectricJacksUsed"])
        print("  GasPoweredJacksUsed   =", cp_sat_solution["GasPoweredJacksUsed"])
        print("  Total cars processed    =", cp_sat_solution["objective"])
    else:
        print("No feasible solution found in CP-SAT solver.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Solving using OR-Tools Linear Solver (MIP):
Solution:
  AutoElectricJacksUsed = 8.0
  GasPoweredJacksUsed   = 11.0
  Total cars processed    = 84.0

Solving using OR-Tools CP-SAT Solver:
Solution:
  AutoElectricJacksUsed = 8
  GasPoweredJacksUsed   = 11
  Total cars processed    = 84.0
'''

'''Expected Output:
Expected solution

: {'variables': {'AutoElectricJacksUsed': 8.0, 'GasPoweredJacksUsed': 11.0}, 'objective': 84.0}'''

