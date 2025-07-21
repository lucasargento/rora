# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} &:& i = 1,\ldots,C \quad (\text{courses}), \quad p = 1,\ldots,P \quad (\text{periods}), \\[1mm]
&& \text{with } C \text{ representing the number of courses and } P \text{ the number of periods.} \\[2mm]

\textbf{Parameters:} &:& 
\begin{array}{rl}
  available_{ip} & \in \{0,1\}, \quad \text{where } available_{ip}=1 \text{ if course } i \text{ is available in period } p, \\[1mm]
  conflict_{ij} & \in \{0,1\}, \quad \text{where } conflict_{ij}=1 \text{ if courses } i \text{ and } j \text{ cannot be scheduled simultaneously}, \\[1mm]
  requirement_i & \in \mathbb{Z}_+, \quad \text{the number of lectures required for course } i, \\[1mm]
  R & \in \mathbb{Z}_+, \quad \text{the number of rooms available per period.}
\end{array} \\[2mm]

\textbf{Decision Variables:} &:&
\begin{array}{rl}
  y_{ip} & \in \{0,1\}, \quad \text{for all } i=1,\ldots,C, \; p=1,\ldots,P, \\[1mm]
  && \quad \text{where } y_{ip}=1 \text{ if course } i \text{ is scheduled in period } p, \\
  && \quad \text{and } y_{ip}=0 \text{ otherwise.}
\end{array} \\[4mm]

\textbf{Objective Function:} &:&
\begin{array}{rl}
  \min\; & 0, \quad \text{(This is a feasibility problem, so the objective is a dummy objective.)}
\end{array} \\[4mm]

\textbf{Constraints:} &:&
\begin{array}{rl}
  \text{(1) Lecture Requirement:} & \displaystyle \sum_{p=1}^{P} y_{ip} = requirement_i, \quad \forall \; i=1,\ldots,C, \\[2mm]
  \text{(2) Availability:} & y_{ip} \leq available_{ip}, \quad \forall \; i=1,\ldots,C,\; \forall \; p=1,\ldots,P, \\[2mm]
  \text{(3) Room Capacity per Period:} & \displaystyle \sum_{i=1}^{C} y_{ip} \leq R, \quad \forall \; p=1,\ldots,P, \\[2mm]
  \text{(4) Conflict Avoidance:} & y_{ip} + y_{jp} \leq 1, \quad \forall \; p=1,\ldots,P,\; \forall \; (i,j) \text{ with } i < j \text{ and } conflict_{ij}=1.
\end{array}
\end{array}
\]

This model fully represents the Timetable scheduling problem: 

• Each course i must have exactly requirement₍ᵢ₎ lectures scheduled over the available periods.  
• A course can only be scheduled in a period if it is available during that period.  
• The total number of lectures scheduled in any period cannot exceed the number of available rooms R.  
• Conflicting courses cannot have lectures scheduled simultaneously in the same period.

All constraints and parameters are included to ensure the problem is both feasible and bounded.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    courses = 5
    periods = 20
    rooms = 2

    # available matrix: available[i][p] == 1 if course i can be scheduled in period p.
    available = [
        [0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1],
        [1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
        [0,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1],
        [1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    # conflict matrix: conflict[i][j] == 1 if course i and course j cannot be scheduled at the same period.
    conflict = [
        [0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [1, 0, 1, 1, 0]
    ]

    # Requirement: number of lectures required per course.
    requirement = [6, 10, 14, 6, 4]

    # Create the model
    model = cp_model.CpModel()

    # Variables: y[i][p] is 1 if course i is scheduled in period p.
    y = {}
    for i in range(courses):
        for p in range(periods):
            y[(i, p)] = model.NewBoolVar(f'y_{i}_{p}')

    # Constraint 1: Lecture Requirement for each course.
    for i in range(courses):
        model.Add(sum(y[(i, p)] for p in range(periods)) == requirement[i])

    # Constraint 2: Availability: course can only be scheduled in a period if available.
    for i in range(courses):
        for p in range(periods):
            if available[i][p] == 0:
                model.Add(y[(i, p)] == 0)

    # Constraint 3: Room Capacity per Period.
    for p in range(periods):
        model.Add(sum(y[(i, p)] for i in range(courses)) <= rooms)

    # Constraint 4: Conflict Avoidance: conflicting courses cannot share same period.
    for p in range(periods):
        for i in range(courses):
            for j in range(i + 1, courses):
                if conflict[i][j] == 1:
                    model.Add(y[(i, p)] + y[(j, p)] <= 1)

    # Dummy objective: We just need to find a feasible solution.
    model.Minimize(0)

    # Create the solver and solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("Solution:")
        for i in range(courses):
            scheduled_periods = []
            for p in range(periods):
                if solver.Value(y[(i, p)]) == 1:
                    scheduled_periods.append(p + 1)  # periods indexed starting at 1 for output
            print(f"Course {i + 1}: Scheduled periods -> {scheduled_periods}")
        print(f"Objective value: {solver.ObjectiveValue()}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()