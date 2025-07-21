# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Decision Variables:} \\
&& x_t \in \mathbb{R}, \quad \forall t = 0,1,\dots, T, \quad \text{(Position of the rocket at time }t\text{)}; \\
&& v_t \in \mathbb{R}, \quad \forall t = 0,1,\dots, T, \quad \text{(Velocity of the rocket at time }t\text{)}; \\
&& a_t \in \mathbb{R}, \quad \forall t = 0,1,\dots, T-1, \quad \text{(Acceleration (control) applied at time }t\text{)}. \\[1em]

\textbf{Parameters:} \\
&& x_0 = 0, \quad v_0 = 0, \quad \text{(Initial position and velocity)}; \\
&& x_T = 1, \quad v_T = 0, \quad \text{(Target final position and velocity)}; \\
&& T = 20. \\[1em]

\textbf{Objective Function:} \\
&& \text{Minimize} \quad J = \sum_{t=0}^{T-1} \lvert a_t \rvert. \\[1em]

\textbf{Constraints:} \\
&& \text{Dynamics (Position update):} \quad x_{t+1} = x_t + v_t, \quad \forall \, t = 0,1,\dots, T-1; \\
&& \text{Dynamics (Velocity update):} \quad v_{t+1} = v_t + a_t, \quad \forall \, t = 0,1,\dots, T-1; \\
&& \text{Initial conditions:} \quad x_0 = 0, \quad v_0 = 0; \\
&& \text{Terminal conditions:} \quad x_T = 1, \quad v_T = 0.
\end{array}
\]

Alternatively, presented in a single aligned block:

\[
\begin{aligned}
\textbf{Decision Variables:} \quad
& x_t \in \mathbb{R}, \quad t = 0,1,\dots, T, \quad \text{(Position)}; \\
& v_t \in \mathbb{R}, \quad t = 0,1,\dots, T, \quad \text{(Velocity)}; \\
& a_t \in \mathbb{R}, \quad t = 0,1,\dots, T-1, \quad \text{(Acceleration/control)}; \\[1em]
\textbf{Parameters:} \quad
& x_0 = 0, \quad v_0 = 0, \quad x_T = 1, \quad v_T = 0, \quad T = 20; \\[1em]
\textbf{Objective:} \quad
& \min_{\,\{a_t\}_{t=0}^{T-1}} \; \sum_{t=0}^{T-1} \lvert a_t \rvert; \\[1em]
\textbf{Subject to:} \quad
& x_{t+1} = x_t + v_t, \quad t = 0,1,\dots, T-1; \\
& v_{t+1} = v_t + a_t, \quad t = 0,1,\dots, T-1; \\
& x_0 = 0, \quad v_0 = 0; \\
& x_T = 1, \quad v_T = 0.
\end{aligned}
\]

This formulation fully captures the real-world energy and natural resources problem for the rocket's trajectory, ensuring that the dynamics, boundary conditions, and fuel consumption (modeled as the sum of the absolute accelerations) are all properly represented.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    T = 20
    InitialPosition = 0.0
    InitialVelocity = 0.0
    FinalPosition = 1.0
    FinalVelocity = 0.0

    # Create solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables:
    # x[t]: position at time t for t=0,...,T
    x = [solver.NumVar(-solver.infinity(), solver.infinity(), f'x_{t}') for t in range(T + 1)]
    # v[t]: velocity at time t for t=0,...,T
    v = [solver.NumVar(-solver.infinity(), solver.infinity(), f'v_{t}') for t in range(T + 1)]
    # a[t]: acceleration at time t for t=0,...,T-1 (control input)
    a = [solver.NumVar(-solver.infinity(), solver.infinity(), f'a_{t}') for t in range(T)]
    # u[t]: auxiliary variables for absolute value of a[t]
    u = [solver.NumVar(0, solver.infinity(), f'u_{t}') for t in range(T)]

    # Add equality constraints for dynamics:
    # x[t+1] = x[t] + v[t] for t = 0,1,...,T-1
    for t in range(T):
        solver.Add(x[t + 1] == x[t] + v[t])
    
    # v[t+1] = v[t] + a[t] for t = 0,1,...,T-1
    for t in range(T):
        solver.Add(v[t + 1] == v[t] + a[t])
    
    # Absolute value constraints: u[t] >= a[t] and u[t] >= -a[t] for t = 0,...,T-1
    for t in range(T):
        solver.Add(u[t] >= a[t])
        solver.Add(u[t] >= -a[t])

    # Initial conditions
    solver.Add(x[0] == InitialPosition)
    solver.Add(v[0] == InitialVelocity)
    
    # Terminal conditions
    solver.Add(x[T] == FinalPosition)
    solver.Add(v[T] == FinalVelocity)

    # Objective: minimize the total fuel consumption given by sum(u[t])
    objective = solver.Sum(u[t] for t in range(T))
    solver.Minimize(objective)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("Objective value (total fuel consumption):", solver.Objective().Value())
        print("\nTime\tPosition\tVelocity\tAcceleration\t|Acceleration|")
        for t in range(T):
            print(f"{t:2d}\t{x[t].SolutionValue():10.4f}\t{v[t].SolutionValue():10.4f}\t"
                  f"{a[t].SolutionValue():15.4f}\t{u[t].SolutionValue():15.4f}")
        # Print final state
        print(f"{T:2d}\t{x[T].SolutionValue():10.4f}\t{v[T].SolutionValue():10.4f}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()