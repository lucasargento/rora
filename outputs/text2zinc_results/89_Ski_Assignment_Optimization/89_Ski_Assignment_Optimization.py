# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Sets and Parameters} \\
I & = & \{1, 2, 3, 4, 5, 6\} \quad (\text{indices for skis}) \\
J & = & \{1, 2, 3, 4, 5\} \quad (\text{indices for skiers}) \\[1em]
s_i & = & \text{ski height of ski } i,\quad \text{with } s_1 = 1,\; s_2 = 2,\; s_3 = 5,\; s_4 = 7,\; s_5 = 13,\; s_6 = 21 \\
h_j & = & \text{height of skier } j,\quad \text{with } h_1 = 3,\; h_2 = 4,\; h_3 = 7,\; h_4 = 11,\; h_5 = 18 \\[1em]
d_{ij} & = & \left| s_i - h_j \right| \quad (\text{absolute disparity between ski } i \text{ and skier } j) \\[2em]

\textbf{Decision Variables} \\
x_{ij} & \in & \{0,1\}, \quad \forall\, i \in I,\; j \in J, \\
& & \quad \text{where } x_{ij} = 
\begin{cases}
1, & \text{if ski } i \text{ is assigned to skier } j, \\
0, & \text{otherwise.}
\end{cases} \\[2em]

\textbf{Mathematical Model} \\[1em]
\begin{aligned}
\min_{x_{ij}} \quad & \sum_{j \in J} \sum_{i \in I} d_{ij}\, x_{ij} \\[1em]
\text{s.t.} \quad 
& \sum_{i \in I} x_{ij} = 1, & \quad \forall\, j \in J, \quad &\text{(Each skier is assigned exactly one ski)} \\[1em]
& \sum_{j \in J} x_{ij} \le 1, & \quad \forall\, i \in I, \quad &\text{(Each ski is assigned to at most one skier)} \\[1em]
& x_{ij} \in \{0,1\}, & \quad \forall\, i \in I,\; j \in J. & \quad \text{(Binary assignment)}
\end{aligned}
\end{array}
\]'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    num_skis = 6
    num_skiers = 5
    ski_heights = [1, 2, 5, 7, 13, 21]
    skier_heights = [3, 4, 7, 11, 18]

    # Precompute disparities: |s_i - h_j|
    disparities = {}
    for i in range(num_skis):
        for j in range(num_skiers):
            disparities[(i, j)] = abs(ski_heights[i] - skier_heights[j])

    # Create the CP-SAT Model.
    model = cp_model.CpModel()
    
    # Decision variables: x[i][j] = 1 if ski i is assigned to skier j.
    x = {}
    for i in range(num_skis):
        for j in range(num_skiers):
            x[(i, j)] = model.NewBoolVar(f"x_{i}_{j}")

    # Each skier gets exactly one ski.
    for j in range(num_skiers):
        model.Add(sum(x[(i, j)] for i in range(num_skis)) == 1)
    
    # Each ski is assigned to at most one skier.
    for i in range(num_skis):
        model.Add(sum(x[(i, j)] for j in range(num_skiers)) <= 1)

    # Objective: minimize total disparity.
    model.Minimize(
        sum(disparities[(i, j)] * x[(i, j)] for i in range(num_skis) for j in range(num_skiers))
    )

    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        print("Total disparity:", solver.ObjectiveValue())
        for j in range(num_skiers):
            for i in range(num_skis):
                if solver.Value(x[(i, j)]) == 1:
                    print(f"Skier {j+1} (height {skier_heights[j]}) is assigned Ski {i+1} (height {ski_heights[i]}), disparity = {disparities[(i, j)]}")
    else:
        print("No feasible solution found.")

if __name__ == "__main__":
    main()