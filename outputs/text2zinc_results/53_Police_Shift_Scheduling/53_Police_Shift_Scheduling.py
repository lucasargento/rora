# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:} \quad & s \in \{1,2,\ldots, N\} \quad\text{with } N = \text{NumShifts}. \\[1mm]
\textbf{Decision Variables:} \quad & x_s \in \mathbb{Z}_{\ge 0}, \quad \forall s=1,\ldots,N. \\
& \text{Here, } x_s \text{ represents the number of police officers scheduled to start at shift } s. \\[1mm]
\textbf{Parameters:} \quad & \text{OfficersNeeded}_s \quad \forall s=1,\ldots,N, \quad\text{the required number of officers in shift } s; \\[0.5mm]
& \text{ShiftCosts}_s \quad \forall s=1,\ldots,N, \quad\text{the cost incurred when an officer starts at shift } s. \\[1mm]
\textbf{Assumptions:} \quad & \text{Each officer who starts at shift } s \text{ works for two consecutive shifts, namely shifts } s \text{ and } s+1. \\
& \text{We assume a cyclic schedule, i.e., shift } N+1 \text{ is equivalent to shift } 1. \\[1mm]
\textbf{Objective Function:} \quad & \text{Minimize the total start-up cost:} \\
\min \quad & \sum_{s=1}^{N} \text{ShiftCosts}_s \, x_s. \\[1mm]
\textbf{Constraints:} \quad & \text{For each shift } s, \text{ the sum of officers that started in the previous shift and the current shift provides coverage.} \\
\text{Coverage:} \quad & x_{s} + x_{s-1} \ge \text{OfficersNeeded}_s, \quad \forall s=1,\ldots,N, \\
& \text{with the cyclic index convention } x_{0} \equiv x_{N}.
\end{align*}

\noindent This formulation fully models the scheduling problem: the decision variables denote the number of officers starting at each shift, the objective minimizes the total cost across all shifts, and the constraints guarantee that every shift is sufficiently covered by officers working two consecutive shifts. The model is both feasible and bounded under reasonable data and the assumption of a cyclic schedule.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Problem data
    NumShifts = 6
    OfficersNeeded = [15, 13, 11, 11, 9, 7]
    ShiftCosts = [500, 480, 450, 460, 470, 490]

    # Create the CP-SAT model.
    model = cp_model.CpModel()
    
    # Define a sufficient upper bound for officers starting in a shift.
    max_officers = sum(OfficersNeeded)
    
    # Decision variables: x[s] represents the number of officers starting at shift s.
    x = [model.NewIntVar(0, max_officers, f'x_{s}') for s in range(NumShifts)]
    
    # Constraints: Each shift s is covered by officers starting in shift s and the previous shift.
    for s in range(NumShifts):
        prev = (s - 1) % NumShifts  # cyclic index (previous shift)
        model.Add(x[s] + x[prev] >= OfficersNeeded[s])
        
    # Objective: Minimize the total cost of starting shifts.
    model.Minimize(sum(ShiftCosts[s] * x[s] for s in range(NumShifts)))
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    # Output the results.
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f'Optimal objective value: {solver.ObjectiveValue()}')
        for s in range(NumShifts):
            print(f'Number of officers to start at shift {s+1}: {solver.Value(x[s])}')
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()