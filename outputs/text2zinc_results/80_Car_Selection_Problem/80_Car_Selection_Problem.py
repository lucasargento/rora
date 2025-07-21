# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Parameters:} \quad & & &  \\
  & P & = & \text{Total number of participants (here } P=25\text{)}, \\
  & C & = & \text{Total number of cars (here } C=25\text{)}, \\
  & a_{ij} & \in & \{0,1\} \quad \forall\, i=1,\ldots,P,\; j=1,\ldots,C,\ \text{with } a_{ij}=1 \text{ if participant } i \text{ is interested in car } j, \\
  & & & \text{and } a_{ij}=0 \text{ otherwise.} \\[1em]
\textbf{Decision Variables:} \quad & & & \\
  & x_{ij} & \in & \{0,1\} \quad \forall\, i=1,\ldots,P,\; j=1,\ldots,C, \\
  & & & \text{where } x_{ij}=1 \text{ indicates that participant } i \text{ is assigned car } j, \\
  & & & \text{and } x_{ij}=0 \text{ otherwise.} \\[1em]
\textbf{Objective Function:} \quad & & & \\
\text{maximize} \quad & z & = & \sum_{i=1}^{P} \sum_{j=1}^{C} x_{ij}. \\[1em]
\textbf{Subject to:} \quad & & & \\
\text{(1) Participant Assignment Constraint:} \quad & \sum_{j=1}^{C} x_{ij} & \leq & 1, \quad \forall\, i=1,\ldots,P, \\
\text{(2) Car Availability Constraint:} \quad & \sum_{i=1}^{P} x_{ij} & \leq & 1, \quad \forall\, j=1,\ldots,C, \\
\text{(3) Interest Feasibility Constraint:} \quad & x_{ij} & \leq & a_{ij}, \quad \forall\, i=1,\ldots,P,\; j=1,\ldots,C.
\end{array}
\]

This formulation is a complete and self-contained integer programming model for the Car Selection Problem, ensuring that each participant is assigned at most one car, each car is assigned at most to one participant, and assignments can only be made where there is expressed interest.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    ParticipantNum = 25
    CarNum = 25
    InterestMatrix = [
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1]
    ]
    
    # Create CP-SAT model
    model = cp_model.CpModel()

    # Decision variables: x[i][j] = 1 if participant i is assigned car j
    x = {}
    for i in range(ParticipantNum):
        for j in range(CarNum):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')
            # Interest feasibility constraint: if participant is not interested, x must be 0.
            if InterestMatrix[i][j] == 0:
                model.Add(x[i, j] == 0)
            # Alternatively, one could add: model.Add(x[i, j] <= InterestMatrix[i][j])

    # Participant assignment constraint: each participant gets at most one car.
    for i in range(ParticipantNum):
        model.Add(sum(x[i, j] for j in range(CarNum)) <= 1)

    # Car availability constraint: each car can be assigned to at most one participant.
    for j in range(CarNum):
        model.Add(sum(x[i, j] for i in range(ParticipantNum)) <= 1)

    # Objective: maximize total number of assignments.
    model.Maximize(sum(x[i, j] for i in range(ParticipantNum) for j in range(CarNum)))

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal objective value =', solver.ObjectiveValue())
        print('Assignments (participant, car):')
        for i in range(ParticipantNum):
            for j in range(CarNum):
                if solver.Value(x[i, j]) == 1:
                    print(f'Participant {i} assigned to Car {j}')
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()