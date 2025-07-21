# Mathematical Formulation:
'''\begin{align*}
\textbf{Sets and Parameters:} \quad & I = \{1,2,\dots,n\} \quad \text{with } n = \text{num\_people} \quad \text{(here, } n=8\text{)},\\[1mm]
& c_{ij} \in \{0,1\}\quad \forall\, i,j \in I, \quad \text{the compatibility matrix, where } c_{ij}=1 \text{ if person } i \text{ can donate to person } j,\\[1mm]
& \text{and } c_{ij}=0 \text{ otherwise.}
\\[2mm]
\textbf{Decision Variables:} \quad & x_{ij} \in \{0,1\} \quad \forall\, i,j \in I, \\
&\quad \text{with } x_{ij}=1 \text{ if person } i \text{ donates a kidney to person } j, \\
&\quad \text{and } x_{ij}=0 \text{ otherwise.}
\\[2mm]
\textbf{Objective Function:} \quad & \text{Maximize the total number of kidney exchanges:} \\
& \max \quad Z = \sum_{i\in I} \sum_{j\in I} x_{ij}.
\\[2mm]
\textbf{Constraints:} \quad
& \textbf{(1) Compatibility: For each potential donation, only compatible pairs are allowed:}\\[1mm]
& \quad x_{ij} \leq c_{ij} \quad \forall\, i,j \in I, \\[2mm]
& \textbf{(2) No Self-Donation:}\\[1mm]
& \quad x_{ii} = 0 \quad \forall\, i \in I, \\[2mm]
& \textbf{(3) At most One Donation and One Reception per Person:}\\[1mm]
& \quad \sum_{j\in I} x_{ij} \leq 1 \quad \forall\, i \in I, \quad \text{(each person can donate at most once)};\\[1mm]
& \quad \sum_{j\in I} x_{ji} \leq 1 \quad \forall\, i \in I, \quad \text{(each person can receive at most once)}; \\[2mm]
& \textbf{(4) Cycle/Exchange Validity Requirement: Every donor must also receive a kidney:}\\[1mm]
& \quad \sum_{j\in I} x_{ij} = \sum_{j\in I} x_{ji} \quad \forall\, i \in I.
\end{align*}

This formulation models the kidney exchange program by 
1. introducing binary decision variables for potential donor–recipient pairs (subject to compatibility),
2. maximizing the total number of kidney transplants,
3. and enforcing that each participating individual both donates and receives exactly one kidney, thereby ensuring a valid cycle exchange.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    num_people = 8
    compatible = [
        [0, 1, 1, 0, 0, 0, 0, 0],  # Person 1 can donate to 2, 3
        [1, 0, 0, 0, 0, 1, 0, 0],  # Person 2 can donate to 1, 6
        [1, 0, 0, 1, 0, 0, 1, 0],  # Person 3 can donate to 1, 4, 7
        [0, 1, 0, 0, 0, 0, 0, 0],  # Person 4 can donate to 2
        [0, 1, 0, 0, 0, 0, 0, 0],  # Person 5 can donate to 2
        [0, 0, 0, 0, 1, 0, 0, 0],  # Person 6 can donate to 5
        [0, 0, 0, 0, 0, 0, 0, 1],  # Person 7 can donate to 8
        [0, 0, 1, 0, 0, 0, 0, 0]   # Person 8 can donate to 3
    ]
    
    model = cp_model.CpModel()
    
    # Decision variables: x[i][j] = 1 if person i donates to person j
    x = {}
    for i in range(num_people):
        for j in range(num_people):
            x[i, j] = model.NewBoolVar('x_%i_%i' % (i, j))
    
    # Objective: Maximize total number of kidney exchanges
    model.Maximize(sum(x[i, j] for i in range(num_people) for j in range(num_people)))
    
    # Constraints:
    # (1) Compatibility: x[i][j] <= compatible[i][j] for all i, j
    for i in range(num_people):
        for j in range(num_people):
            if compatible[i][j] == 0:
                model.Add(x[i, j] == 0)
    
    # (2) No Self-Donation: x[i][i] == 0 for all i
    for i in range(num_people):
        model.Add(x[i, i] == 0)
    
    # (3) At most One Donation per Person and at most One Reception per Person
    for i in range(num_people):
        model.Add(sum(x[i, j] for j in range(num_people)) <= 1)
        model.Add(sum(x[j, i] for j in range(num_people)) <= 1)
    
    # (4) Cycle/Exchange Validity: Donation count equals reception count per person
    for i in range(num_people):
        model.Add(sum(x[i, j] for j in range(num_people)) == sum(x[j, i] for j in range(num_people)))
    
    # Create solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print('Optimal objective value =', solver.ObjectiveValue())
        for i in range(num_people):
            for j in range(num_people):
                if solver.Value(x[i, j]) == 1:
                    print(f'Person {i+1} donates to Person {j+1}')
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()