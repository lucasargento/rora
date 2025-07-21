# Mathematical Formulation:
'''\begin{align*}
\textbf{Parameters:} \quad &\\[1mm]
N &\in \mathbb{N} \quad &&\text{Number of days in the recurring period, with } n = 1, 2, \dots, N.\\[1mm]
\text{Num}_n &\in \mathbb{N} \quad &&\text{Number of employees required on day } n, \; n=1,\dots,N.\\[1mm]
W &\in \mathbb{N} \quad &&\text{Number of consecutive working days (WorkingDays).}\\[1mm]
R &\in \mathbb{N} \quad &&\text{Number of consecutive resting days (RestingDays).}\\[1mm]
P &= W + R \quad &&\text{Length of the individual employee cycle (period).}\\[2mm]
\textbf{Decision Variables:} \quad &\\[1mm]
x_s &\in \mathbb{Z}_+ \quad &&\text{Number of employees with cycle offset } s, \quad s = 0,1,\dots,P-1.
\intertext{Each employee’s cycle is assumed to start at day } s, \text{ and such an employee is scheduled to work on day } n \text{ if}
\left[(n-s) \bmod P < W\right] &= 1, \quad \text{and is off otherwise. Here, } [\cdot] \text{ is the Iverson bracket, i.e., }
\\[2mm]
\textbf{Objective Function:} \quad &\\[1mm]
\min \quad Z &= \sum_{s=0}^{P-1} x_s.
\intertext{The objective is to minimize the total number of employees hired.}
\intertext{%
\textbf{Constraints:} \quad &\\[1mm]
\text{For each day } n=1,\dots,N, \quad &\\[1mm]
\sum_{s=0}^{P-1} \left[ \,(n-s) \bmod P < W \,\right] \, x_s &\geq \text{Num}_n.
\end{align*}

\textbf{Explanation:}  
\begin{itemize}
    \item The index $s \in \{0,1,\dots,P-1\}$ denotes the starting offset in the $P$–day cycle for an employee. An employee with offset $s$ is on duty on day $n$ if and only if the remainder of $(n-s)$ modulo $P$ is less than $W$, i.e., in their working period.
    \item The constraint for each day $n$ ensures that the sum of all employees working on that day (across all cycle offsets) meets or exceeds the required staffing level $\text{Num}_n$.
    \item The decision variables $x_s$ are nonnegative integers.
    \item The model is feasible and bounded provided that the staffing requirements $\text{Num}_n$ and cycle parameters $W,R$ are such that a cyclic schedule can cover the demands.
\end{itemize}

This formulation fully captures the scheduling problem with a recurring cycle and the corresponding coverage constraints.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem Data
    N = 6
    Num = [5, 10, 2, 3, 2, 10]  # Number of employees required for days 1..N
    WorkingDays = 5
    RestingDays = 2
    P = WorkingDays + RestingDays  # Length of the cycle

    # Create the solver using CBC (Mixed Integer Programming)
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not found.")
        return

    # Decision Variables: x[s] for s = 0,1,...,P-1
    x = {}
    for s in range(P):
        x[s] = solver.IntVar(0, solver.infinity(), f'x[{s}]')

    # Constraints: For each day n = 1,...,N, ensure sufficient employees are working.
    # An employee with offset s works on day n if ((n - s) mod P) < WorkingDays.
    for n in range(1, N + 1):
        constraint_expr = []
        for s in range(P):
            if ((n - s) % P) < WorkingDays:
                constraint_expr.append(x[s])
        # Add constraint: sum of employees working on day n must be >= Num[n-1]
        solver.Add(solver.Sum(constraint_expr) >= Num[n - 1])

    # Objective: Minimize the total number of employees hired.
    objective = solver.Sum(x[s] for s in range(P))
    solver.Minimize(objective)

    # Solve the model.
    status = solver.Solve()

    # Check and print the results.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Optimal solution found:')
        print('Total number of employees:', int(solver.Objective().Value()))
        for s in range(P):
            print(f'Employees with cycle offset {s}: {int(x[s].solution_value())}')
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()