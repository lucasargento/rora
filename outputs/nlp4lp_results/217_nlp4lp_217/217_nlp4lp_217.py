# Problem Description:
'''Problem description: A clothing company can sell their product in two types of stores, a retail store and a factory outlet. A retail store brings in 200 customers every day and requires 6 employees to operate. A factory outlet brings in 80 customers every day and due to the lower traffic and being in more remote areas, requires 4 employees to run. Company executives decided that there must be at least 1200 customers every day, and can make available 50 employees. How should the company distribute their product to the two types of store to reduce the number of stores that must be open?

Expected Output Schema:
{
  "variables": {
    "NumberRetailStores": "float",
    "NumberFactoryOutlets": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- S: set of store types = {RetailStore, FactoryOutlet}

Parameters:
- customers_retail: number of customers a retail store attracts per day = 200 [customers/day]
- employees_retail: number of employees required per retail store = 6 [employees/store]
- customers_factory: number of customers a factory outlet attracts per day = 80 [customers/day]
- employees_factory: number of employees required per factory outlet = 4 [employees/store]
- min_customers: minimum number of customers required per day = 1200 [customers/day]
- available_employees: total employees available = 50 [employees]

Variables:
- NumberRetailStores: number of retail stores to open (integer, ≥ 0) [stores]
- NumberFactoryOutlets: number of factory outlets to open (integer, ≥ 0) [stores]

Objective:
- Minimize total number of open stores = NumberRetailStores + NumberFactoryOutlets

Constraints:
1. Customer Requirement: (customers_retail * NumberRetailStores) + (customers_factory * NumberFactoryOutlets) ≥ min_customers  
   i.e., 200 * NumberRetailStores + 80 * NumberFactoryOutlets ≥ 1200
2. Employee Availability: (employees_retail * NumberRetailStores) + (employees_factory * NumberFactoryOutlets) ≤ available_employees  
   i.e., 6 * NumberRetailStores + 4 * NumberFactoryOutlets ≤ 50

Comments:
- All parameter units are consistent: customer counts per day and employee counts.
- The decision variables should preferably be integers since partial stores are not meaningful.
- This model minimizes the total number of stores while ensuring at least 1200 daily customers are reached and employee usage does not exceed the 50 available employees.'''

# Generated Code:
#!/usr/bin/env python3
from ortools.linear_solver import pywraplp

def solve_linear_model():
    # Create the solver using SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created. Please check installation.")
        return None

    # Decision Variables (integers, ≥ 0)
    number_retail = solver.IntVar(0, solver.infinity(), 'NumberRetailStores')
    number_factory = solver.IntVar(0, solver.infinity(), 'NumberFactoryOutlets')

    # Parameters
    customers_retail = 200       # customers per retail store per day
    employees_retail = 6         # employees required per retail store
    customers_factory = 80       # customers per factory outlet per day
    employees_factory = 4        # employees required per factory outlet
    min_customers = 1200         # minimum customers per day required
    available_employees = 50     # total employees available

    # Constraints:
    # 1. Customer requirement: 200 * NumberRetailStores + 80 * NumberFactoryOutlets ≥ 1200
    solver.Add(customers_retail * number_retail + customers_factory * number_factory >= min_customers)

    # 2. Employee availability: 6 * NumberRetailStores + 4 * NumberFactoryOutlets ≤ 50
    solver.Add(employees_retail * number_retail + employees_factory * number_factory <= available_employees)

    # Objective: Minimize total number of open stores
    solver.Minimize(number_retail + number_factory)

    # Solve the model
    status = solver.Solve()

    # Check if an optimal solution was found and return the results in the required schema.
    if status == pywraplp.Solver.OPTIMAL:
        solution = {
            "NumberRetailStores": number_retail.solution_value(),
            "NumberFactoryOutlets": number_factory.solution_value(),
            "objective": solver.Objective().Value()
        }
        return solution
    else:
        print("No optimal solution found for the linear formulation.")
        return None

def main():
    # Since only one formulation is provided, we only run the linear model.
    result_linear = solve_linear_model()

    print("Results:")
    if result_linear:
        print("Linear Formulation Solution:")
        print(result_linear)
    else:
        print("No feasible solution found in the linear formulation.")

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
Results:
Linear Formulation Solution:
{'NumberRetailStores': 6.0, 'NumberFactoryOutlets': 0.0, 'objective': 6.0}
'''

'''Expected Output:
Expected solution

: {'variables': {'NumberRetailStores': 6.0, 'NumberFactoryOutlets': -0.0}, 'objective': 6.0}'''

