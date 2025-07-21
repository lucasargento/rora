# Problem Description:
'''Problem description: There has been a horrible accident and patients need to be taken to the hospital by either a helicopter or bus. A helicopter can transport 5 patients per trip and takes 1 hour. On the other hand, a bus can transport 8 patients per trip and takes 3 hours. At least 120 patients need to be transported and at least 30% of the trips should be by helicopter. In addition, there can be at most 10 bus trips. How should the patients be taken to minimize the total time to transport the patients?

Expected Output Schema:
{
  "variables": {
    "HelicopterTrips": "float",
    "BusTrips": "float",
    "PatientsHelicopter": "float",
    "PatientsBus": "float"
  },
  "objective": "float"
}'''

# Mathematical Formulation:
'''Sets:
- TransportModes = {Helicopter, Bus}

Parameters:
- helicopter_capacity = 5        // patients transported per helicopter trip [patients/trip]
- bus_capacity = 8               // patients transported per bus trip [patients/trip]
- helicopter_trip_time = 1       // time per helicopter trip [hour/trip]
- bus_trip_time = 3              // time per bus trip [hour/trip]
- min_patients = 120             // minimum number of patients to transport [patients]
- min_helicopter_ratio = 0.3     // minimum ratio of helicopter trips to total trips [fraction]
- max_bus_trips = 10             // maximum number of bus trips allowed [trips]

Variables:
- HelicopterTrips: integer ≥ 0   // number of helicopter trips to schedule [trips]
- BusTrips: integer ≥ 0          // number of bus trips to schedule [trips]
- PatientsHelicopter: integer ≥ 0  // number of patients transported by helicopter [patients]
- PatientsBus: integer ≥ 0         // number of patients transported by bus [patients]

Objective:
- Minimize total time = HelicopterTrips * helicopter_trip_time + BusTrips * bus_trip_time
  // This represents the sum of time spent on helicopter and bus trips [hours]

Constraints:
1. Patient Coverage Constraint:
   - PatientsHelicopter + PatientsBus ≥ min_patients
   - Note: PatientsHelicopter is defined as helicopter_capacity * HelicopterTrips and PatientsBus as bus_capacity * BusTrips

2. Helicopter Trip Ratio Constraint:
   - HelicopterTrips ≥ min_helicopter_ratio * (HelicopterTrips + BusTrips)
   - This ensures that at least 30% of the trips are by helicopter

3. Bus Trip Capacity Constraint:
   - BusTrips ≤ max_bus_trips

4. Definition Constraints:
   - PatientsHelicopter = helicopter_capacity * HelicopterTrips
   - PatientsBus = bus_capacity * BusTrips

5. Non-negativity Constraints:
   - HelicopterTrips, BusTrips, PatientsHelicopter, PatientsBus ≥ 0

-------------------------------------------------
For implementation purposes, one can substitute the expressions for PatientsHelicopter and PatientsBus directly into the patient coverage constraint. The variables HelicopterTrips and BusTrips would typically be modeled as integer decision variables even though they are listed as floats in the expected output schema.

The objective and constraints are given in consistent units (hours for time and patients for patient counts), ensuring a coherent model.

-----------------------------------------------
Expected JSON output (schema):

{
  "variables": {
    "HelicopterTrips": "float",
    "BusTrips": "float",
    "PatientsHelicopter": "float",
    "PatientsBus": "float"
  },
  "objective": "float"
}'''

# Generated Code:
#!/usr/bin/env python3
"""
This script implements the optimization problem using two separate formulations with Google OR-Tools.
Both formulations solve the problem of transporting patients with helicopter and bus trips under given constraints.

Formulation 1: Substitute expressions for PatientsHelicopter and PatientsBus directly.
Formulation 2: Introduce separate decision variables for PatientsHelicopter and PatientsBus and add linking constraints.
"""

from ortools.linear_solver import pywraplp
import json

def solve_model1():
    """Model 1: Substituting the expressions directly."""
    # Create the solver using the CBC MIP backend.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not available.")
        return None

    # Parameters
    helicopter_capacity = 5
    bus_capacity = 8
    helicopter_trip_time = 1
    bus_trip_time = 3
    min_patients = 120
    min_helicopter_ratio = 0.3
    max_bus_trips = 10

    # Decision variables: number of trips for each transport mode (integer >= 0)
    HelicopterTrips = solver.IntVar(0.0, solver.infinity(), 'HelicopterTrips')
    BusTrips = solver.IntVar(0.0, solver.infinity(), 'BusTrips')

    # Objective: minimize total time = helicopter_trip_time * HelicopterTrips + bus_trip_time * BusTrips
    objective = solver.Objective()
    objective.SetCoefficient(HelicopterTrips, helicopter_trip_time)
    objective.SetCoefficient(BusTrips, bus_trip_time)
    objective.SetMinimization()

    # Constraint 1: Patient coverage using the capacity of trips: 5 * HelicopterTrips + 8 * BusTrips >= 120
    solver.Add(helicopter_capacity * HelicopterTrips + bus_capacity * BusTrips >= min_patients)

    # Constraint 2: At least 30% of trips are helicopter trips.
    # HelicopterTrips >= 0.3*(HelicopterTrips + BusTrips)
    # Equivalently, 7*HelicopterTrips - 3*BusTrips >= 0 (by multiplying both sides by 10: 10*HelicopterTrips >= 3*HelicopterTrips + 3*BusTrips)
    solver.Add(7 * HelicopterTrips - 3 * BusTrips >= 0)

    # Constraint 3: Bus trips are limited: BusTrips <= 10.
    solver.Add(BusTrips <= max_bus_trips)

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["HelicopterTrips"] = HelicopterTrips.solution_value()
        result["BusTrips"] = BusTrips.solution_value()
        # Derived patients transported:
        result["PatientsHelicopter"] = helicopter_capacity * HelicopterTrips.solution_value()
        result["PatientsBus"] = bus_capacity * BusTrips.solution_value()
        result["objective"] = objective.Value()
        result["status"] = "Optimal"
    else:
        result["status"] = "Infeasible or no optimal solution found"
    return result

def solve_model2():
    """Model 2: Using separate decision variables for Patients with linking constraints."""
    # Create a separate solver instance.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not available.")
        return None

    # Parameters
    helicopter_capacity = 5
    bus_capacity = 8
    helicopter_trip_time = 1
    bus_trip_time = 3
    min_patients = 120
    min_helicopter_ratio = 0.3
    max_bus_trips = 10

    # Decision variables
    HelicopterTrips = solver.IntVar(0.0, solver.infinity(), 'HelicopterTrips')
    BusTrips = solver.IntVar(0.0, solver.infinity(), 'BusTrips')
    # Patients transported are introduced as separate variables
    PatientsHelicopter = solver.IntVar(0.0, solver.infinity(), 'PatientsHelicopter')
    PatientsBus = solver.IntVar(0.0, solver.infinity(), 'PatientsBus')

    # Objective: minimize total time = helicopter_trip_time * HelicopterTrips + bus_trip_time * BusTrips
    objective = solver.Objective()
    objective.SetCoefficient(HelicopterTrips, helicopter_trip_time)
    objective.SetCoefficient(BusTrips, bus_trip_time)
    objective.SetMinimization()

    # Constraint 1: Patient coverage: PatientsHelicopter + PatientsBus >= min_patients
    solver.Add(PatientsHelicopter + PatientsBus >= min_patients)

    # Constraint 2: Helicopter Trip Ratio: HelicopterTrips >= min_helicopter_ratio * (HelicopterTrips + BusTrips)
    # Multiply by 10 to avoid floating points: 7*HelicopterTrips - 3*BusTrips >= 0
    solver.Add(7 * HelicopterTrips - 3 * BusTrips >= 0)

    # Constraint 3: Bus Trip limit.
    solver.Add(BusTrips <= max_bus_trips)

    # Constraint 4: Definition constraints linking trips and patients.
    solver.Add(PatientsHelicopter == helicopter_capacity * HelicopterTrips)
    solver.Add(PatientsBus == bus_capacity * BusTrips)

    status = solver.Solve()
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result["HelicopterTrips"] = HelicopterTrips.solution_value()
        result["BusTrips"] = BusTrips.solution_value()
        result["PatientsHelicopter"] = PatientsHelicopter.solution_value()
        result["PatientsBus"] = PatientsBus.solution_value()
        result["objective"] = objective.Value()
        result["status"] = "Optimal"
    else:
        result["status"] = "Infeasible or no optimal solution found"
    return result

def main():
    results = {}
    results["Model1_SubstitutedExpressions"] = solve_model1()
    results["Model2_WithLinkingVariables"] = solve_model2()

    # Print results in a structured JSON format
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

'''Execution Results:
SUCCESS:
{
  "Model1_SubstitutedExpressions": {
    "HelicopterTrips": 24.0,
    "BusTrips": 0.0,
    "PatientsHelicopter": 120.0,
    "PatientsBus": 0.0,
    "objective": 24.0,
    "status": "Optimal"
  },
  "Model2_WithLinkingVariables": {
    "HelicopterTrips": 24.0,
    "BusTrips": 0.0,
    "PatientsHelicopter": 120.0,
    "PatientsBus": 0.0,
    "objective": 24.0,
    "status": "Optimal"
  }
}
'''

'''Expected Output:
Expected solution

: {'variables': {'HelicopterTrips': 24.0, 'BusTrips': 0.0, 'PatientsHelicopter': -0.0, 'PatientsBus': -0.0}, 'objective': 24.0}'''

