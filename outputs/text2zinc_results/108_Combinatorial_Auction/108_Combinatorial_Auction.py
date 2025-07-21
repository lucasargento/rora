# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Indices} &:& j \in J = \{1,2,\ldots, \mathtt{num\_bids}\} & \text{(set of bids)}\\[1mm]
                &:& i \in I = \{1,2,\ldots, \mathtt{num\_items}\} & \text{(set of items)}\\[2mm]
\textbf{Parameters} &:& 
\begin{array}{l}
\mathtt{bids}_j \quad \text{is the bid amount offered in bid } j, \\
\mathtt{packages}_{j,i} \quad \text{is a binary parameter equal to } 1 \text{ if bid } j \text{ includes item } i \text{ and } 0 \text{ otherwise.}
\end{array}
\end{array}
\]

\[
\begin{array}{rcll}
\textbf{Decision Variables} &:& 
\begin{array}{l}
x_j \in \{0,1\} \quad \text{for } j \in J, \\
\text{where } x_j = 1 \text{ if bid } j \text{ is accepted, and } 0 \text{ otherwise.}
\end{array} & \\
\\[2mm]
\textbf{Objective Function} &:& \displaystyle \max \; Z = \sum_{j=1}^{\mathtt{num\_bids}} \mathtt{bids}_j \, x_j & \text{(Maximize total revenue)}\\[2mm]
\textbf{Constraints} &:& \displaystyle \sum_{j=1}^{\mathtt{num\_bids}} \mathtt{packages}_{j,i} \, x_j \le 1, \quad \forall i \in I & \text{(Each item is allocated at most once)}\\[2mm]
&& x_j \in \{0,1\}, \quad \forall j \in J. &
\end{array}
\]

\vspace{2mm}

\textbf{Discussion:}  
This model represents the combinatorial auction problem. The decision variable \(x_j\) denotes whether bid \(j\) is accepted. The objective is to maximize the total revenue from accepted bids, while the constraint for each item \(i\) ensures that the item is included in at most one accepted bid (i.e., bids selected do not overlap in their allocated items). No further simplifications have been made, and the model accurately reflects the entire problem as described.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    num_items = 7
    num_bids = 5
    bids = [8, 6, 5, 2, 2]
    packages = [
        [1, 1, 1, 1, 0, 0, 0],  # Bid 1: {1,2,3,4}
        [0, 1, 1, 0, 0, 1, 0],  # Bid 2: {2,3,6}
        [1, 0, 0, 1, 1, 0, 0],  # Bid 3: {1,4,5}
        [0, 1, 0, 0, 0, 0, 1],  # Bid 4: {2,7}
        [0, 0, 0, 0, 1, 1, 0]   # Bid 5: {5,6}
    ]
    
    # Create the model.
    model = cp_model.CpModel()

    # Decision variables: x[j] is 1 if bid j is accepted, else 0.
    x = [model.NewBoolVar(f'x_{j}') for j in range(num_bids)]
    
    # Constraint: each item can be allocated at most once.
    for i in range(num_items):
        model.Add(sum(x[j] * packages[j][i] for j in range(num_bids)) <= 1)
    
    # Objective: maximize the total bid revenue.
    model.Maximize(sum(bids[j] * x[j] for j in range(num_bids)))
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Optimal objective value:", solver.ObjectiveValue())
        for j in range(num_bids):
            if solver.Value(x[j]) == 1:
                print(f"Bid {j+1} accepted with bid value: {bids[j]}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()