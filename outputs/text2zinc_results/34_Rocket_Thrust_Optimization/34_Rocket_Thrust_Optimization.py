# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad & X_0,\; V_0,\; X_T,\; V_T \in \mathbb{R}, \quad T \in \mathbb{Z}_{>0} \\[1mm]
\textbf{Decision Variables:} \quad & x_t \in \mathbb{R}, && t = 0,1,\dots,T \quad (\text{position at time } t), \\[0.5mm]
& v_t \in \mathbb{R}, && t = 0,1,\dots,T \quad (\text{velocity at time } t), \\[0.5mm]
& a_t \in \mathbb{R}, && t = 0,1,\dots,T-1 \quad (\text{acceleration (thrust) applied at time } t), \\[0.5mm]
& z \in \mathbb{R}_{+} \quad (\text{auxiliary variable representing } \max_{t} |a_t|). \\[2mm]
\textbf{Objective:} \quad & \minimize_{x_t,\, v_t,\, a_t, \, z} \quad z \\[2mm]
\textbf{Subject to:} \\[0.5mm]
\text{(1) Discrete-time dynamics (position):} \quad & x_{t+1} = x_t + v_t, \quad t = 0,1,\dots, T-1, \\[0.5mm]
\text{(2) Discrete-time dynamics (velocity):} \quad & v_{t+1} = v_t + a_t, \quad t = 0,1,\dots, T-1, \\[0.5mm]
\text{(3) Acceleration bounded by } z: \quad & -z \le a_t \le z, \quad t = 0,1,\dots, T-1, \\[0.5mm]
\text{(4) Initial conditions:} \quad & x_0 = X_0, \quad  v_0 = V_0, \\[0.5mm]
\text{(5) Terminal conditions:} \quad & x_T = X_T, \quad v_T = V_T.
\end{align*} 

\noindent This formulation models the optimal control problem for the rocket, where the goal is to minimize the maximum (in absolute value) thrust (acceleration) required over the time horizon, while satisfying the discrete dynamics of position and velocity as well as the specified boundary conditions.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    X0 = 0.0
    V0 = 0.0
    XT = 1.0
    VT = 0.0
    T = 20

    # Create the solver using GLOP (linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    infinity = solver.infinity()

    # Decision variables
    x = [solver.NumVar(-infinity, infinity, f'x_{t}') for t in range(T+1)]
    v = [solver.NumVar(-infinity, infinity, f'v_{t}') for t in range(T+1)]
    a = [solver.NumVar(-infinity, infinity, f'a_{t}') for t in range(T)]
    # z is non-negative
    z = solver.NumVar(0.0, infinity, 'z')

    # Constraints

    # 1. Discrete-time dynamics for position: x[t+1] = x[t] + v[t]
    for t in range(T):
        solver.Add(x[t+1] == x[t] + v[t])

    # 2. Discrete-time dynamics for velocity: v[t+1] = v[t] + a[t]
    for t in range(T):
        solver.Add(v[t+1] == v[t] + a[t])

    # 3. Acceleration bounded by z: -z <= a[t] <= z
    for t in range(T):
        solver.Add(a[t] <= z)
        solver.Add(a[t] >= -z)

    # 4. Initial conditions: x0 = X0, v0 = V0
    solver.Add(x[0] == X0)
    solver.Add(v[0] == V0)

    # 5. Terminal conditions: x_T = XT, v_T = VT
    solver.Add(x[T] == XT)
    solver.Add(v[T] == VT)

    # Objective: minimize z (max absolute acceleration)
    objective = solver.Objective()
    objective.SetCoefficient(z, 1)
    objective.SetMinimization()

    # Solve
    status = solver.Solve()

    # Check and print the solution
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Minimum maximum thrust (z): {z.solution_value()}")
        for t in range(T):
            print(f"Time {t}: acceleration = {a[t].solution_value()}")
        # Optionally, print positions and velocities
        for t in range(T+1):
            print(f"Time {t}: position = {x[t].solution_value()}, velocity = {v[t].solution_value()}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution or is infeasible.")

if __name__ == '__main__':
    main()