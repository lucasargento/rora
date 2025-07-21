# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} & & \\
i &=& 1,\ldots, N \quad \text{(people)}\\[1mm]
d &=& 1,\ldots, D \quad \text{(days)}\\[2mm]

\textbf{Parameters:} & & \\
p_{i,d} &\in& \{0,1\} \quad \text{for } i=1,\ldots,N,\; d=1,\ldots,D, \\
&& \quad\text{(}p_{i,d}=1 \text{ if person } i \text{ participates on day } d,\; 0 \text{ otherwise)};\\[2mm]
O_i &=& \displaystyle \sum_{d=1}^{D} \frac{p_{i,d}}{\sum_{j=1}^{N} p_{j,d}} \quad \text{for } i=1,\ldots,N,\\[2mm]

\textbf{Decision Variables:} & & \\
x_{i,d} &\in& \{0,1\} \quad \text{for } i=1,\ldots,N,\; d=1,\ldots,D, \\
&& \quad\text{(}x_{i,d} = 1 \text{ if person } i \text{ is assigned as driver on day } d,\; 0 \text{ otherwise)};\\[2mm]
z_i &\ge& 0 \quad \text{for } i=1,\ldots,N, \\
&& \quad\text{(}z_i \text{ represents the absolute deviation between driving assignments and } O_i \text{)}.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Objective:} & & \\
\min \quad & \displaystyle \sum_{i=1}^{N} z_i & \quad \text{(Minimize total fairness deviation)}.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Subject to:} & & \\[1mm]
\text{(1) Exactly one driver per day:} & & \displaystyle \sum_{i=1}^{N} x_{i,d} = 1,\quad \forall\, d=1,\ldots, D, \\[2mm]
\text{(2) Only a participating person can drive:} & & x_{i,d} \le p_{i,d},\quad \forall\, i=1,\ldots, N,\; \forall\, d=1,\ldots, D, \\[2mm]
\text{(3) Absolute deviation constraints (fairness):} & & z_i \ge \displaystyle \sum_{d=1}^{D} x_{i,d} - O_i,\quad \forall\, i=1,\ldots, N, \\[2mm]
& & z_i \ge O_i - \displaystyle \sum_{d=1}^{D} x_{i,d},\quad \forall\, i=1,\ldots, N.
\end{array}
\]

\[
\begin{array}{rcl}
\textbf{Notes:} & & \\
& & \text{For each day } d,\; \text{the term } \frac{1}{\sum_{j=1}^{N} p_{j,d}} \text{ represents the individual obligation } \\
& & \text{if person } i \text{ participates (since there are } \sum_{j=1}^{N} p_{j,d} \text{ participants).}\\[2mm]
& & \text{The model minimizes the total absolute difference between each person’s actual driving} \\
& & \text{assignments } \left(\sum_{d} x_{i,d}\right) \text{ and their corresponding obligation } O_i.\\[2mm]
& & \text{The constraints ensure feasibility (each day exactly one driver among the participants)} \\
& & \text{and boundedness (all terms are finite since } 0\le x_{i,d} \le 1 \text{ and } 0 \le z_i \le D).
\end{array}
\]
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Carpool Fairness Problem Data
    num_days = 5
    num_people = 4
    # participation[person][day]: 1 if participates, 0 otherwise
    participation = [
        [1, 1, 1, 0, 0],  # Person 1
        [1, 0, 1, 0, 0],  # Person 2
        [1, 1, 1, 1, 1],  # Person 3
        [0, 1, 1, 1, 1]   # Person 4
    ]

    # Pre-calculate obligations O_i for each person.
    # O_i = sum_{d=1}^{num_days} (p[i,d] / (sum_{j} p[j,d]))
    O = [0.0] * num_people
    # For each day, first sum up participation for that day
    participants_per_day = []
    for d in range(num_days):
        total = sum(participation[i][d] for i in range(num_people))
        participants_per_day.append(total)
    for i in range(num_people):
        obligation = 0.0
        for d in range(num_days):
            if participation[i][d] == 1:
                # Avoid division by zero; here total should be >= 1 since person participated.
                obligation += 1.0 / participants_per_day[d]
        O[i] = obligation

    # Create the solver using CBC_MIXED_INTEGER_PROGRAMMING.
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables:
    # x[i][d] = 1 if person i drives on day d
    x = {}
    for i in range(num_people):
        for d in range(num_days):
            x[i, d] = solver.IntVar(0, 1, f'x_{i}_{d}')

    # z[i] represents the absolute deviation for person i (continuous variable).
    z = {}
    for i in range(num_people):
        # Upper bound can be num_days.
        z[i] = solver.NumVar(0, num_days, f'z_{i}')

    # Constraint (1): Exactly one driver per day.
    for d in range(num_days):
        solver.Add(solver.Sum(x[i, d] for i in range(num_people)) == 1)

    # Constraint (2): Only a participating person can drive.
    for i in range(num_people):
        for d in range(num_days):
            # If person does not participate, x[i,d] must be 0.
            solver.Add(x[i, d] <= participation[i][d])

    # Constraint (3): Absolute deviation constraints for fairness.
    # Let drive_count_i = sum_{d} x[i,d]
    for i in range(num_people):
        drive_count = solver.Sum(x[i, d] for d in range(num_days))
        # z_i >= drive_count_i - O_i
        solver.Add(z[i] >= drive_count - O[i])
        # z_i >= O_i - drive_count_i
        solver.Add(z[i] >= O[i] - drive_count)

    # Objective: minimize sum of all deviations.
    objective = solver.Sum(z[i] for i in range(num_people))
    solver.Minimize(objective)

    # Solve the model.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print("Objective (Total Deviation):", solver.Objective().Value())
        print()
        # For each day, print assigned driver.
        for d in range(num_days):
            for i in range(num_people):
                if x[i, d].solution_value() > 0.5:
                    print(f"Day {d+1}: Person {i+1} drives")
        print()
        # Print deviations and drive counts per person.
        for i in range(num_people):
            drive_count = sum(x[i, d].solution_value() for d in range(num_days))
            print(f"Person {i+1}: Drive count = {drive_count}, Obligation = {O[i]:.3f}, Deviation = {z[i].solution_value():.3f}")
    else:
        print("No optimal solution found.")

if __name__ == "__main__":
    main()