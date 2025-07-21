# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:} \quad & i,j,p,q \in \{1,2,\ldots,n\}, \quad \text{with } n=10,\\[1mm]
& h_{ij} \in \{0,1\} \quad \text{for } i,j=1,\ldots,n, \quad \text{(given by the "huts" array)}.\\[3mm]
\textbf{Decision Variables:} \quad & x_{pq} \in \{0,1\} \quad \forall \, p,q \in \{1,\ldots,n\}, \\
& \quad\quad\; \text{where } x_{pq}=1 \text{ if an airdrop is selected at grid cell } (p,q), \text{ and } 0 \text{ otherwise}. \\[1mm]
& y_{ij}^{pq} \in \{0,1\} \quad \forall \, i,j,p,q \in \{1,\ldots,n\}, \\
& \quad\quad\; \text{where } y_{ij}^{pq}=1 \text{ if the villager(s) (or hut) located at } (i,j) \\
& \quad\quad\quad \text{is assigned to the drop location } (p,q), \text{ and } 0 \text{ otherwise}.\\[3mm]
\textbf{Objective Function:}\\[1mm]
\text{Minimize } \quad & Z = \sum_{i=1}^n \sum_{j=1}^n h_{ij} \; \sum_{p=1}^n \sum_{q=1}^n \left[ \left(i-p\right)^2+\left(j-q\right)^2 \right]\, y_{ij}^{pq}. \tag{Minimize total squared distance}\\[3mm]
\textbf{Constraints:}\\[1mm]
\text{(1) Exactly two airdrop locations are selected:} \quad & \sum_{p=1}^n \sum_{q=1}^n x_{pq} = 2. \tag{A}\\[2mm]
\text{(2) Each hut (i.e. each grid cell with } h_{ij}=1 \text{) is assigned to exactly one drop location:} \quad & \sum_{p=1}^n \sum_{q=1}^n y_{ij}^{pq} = h_{ij},\quad \forall \, i,j \in \{1,\ldots,n\}. \tag{B}\\[2mm]
\text{(3) A hut can only be assigned to a selected drop location:} \quad & y_{ij}^{pq} \leq x_{pq},\quad \forall \, i,j,p,q\in \{1,\ldots,n\}. \tag{C}\\[2mm]
\textbf{Domain:} \quad & x_{pq} \in \{0,1\},\quad y_{ij}^{pq} \in \{0,1\},\quad \forall \, i,j,p,q \in \{1,\ldots,n\}. 
\end{align*}

Explanation:

• The indices i,j denote the rows and columns for the villages (huts) with their corresponding need (1 if a hut is present, 0 otherwise).  
• The indices p,q denote the candidate grid positions where an airdrop can be placed.  
• Constraint (A) forces the selection of exactly two airdrop locations.  
• Constraint (B) ensures that if a hut exists at cell (i,j), it must be assigned to one and only one drop location.  
• Constraint (C) links the assignment to the selected airdrop locations, ensuring that a hut can only be assigned to a cell that has been chosen as an airdrop location.  
• The objective minimizes the sum of squared Euclidean distances between each hut and its closest (assigned) airdrop location.

This complete formulation accurately models the given transportation and logistics problem and is bounded and feasible under the stated assumptions.'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    n = 10
    # Define the huts grid (0 means no hut, 1 means hut present)
    huts = [
        [0,0,0,0,1,0,0,0,0,0],  # Row A
        [0,0,0,0,1,0,0,0,1,1],  # Row B
        [1,0,0,0,0,1,0,1,1,1],  # Row C
        [0,1,0,0,0,0,1,0,0,1],  # Row D
        [0,1,0,0,0,0,0,0,1,0],  # Row E
        [0,0,0,0,0,0,0,1,0,0],  # Row F
        [0,1,0,0,0,0,0,0,0,0],  # Row G
        [0,1,0,0,0,1,0,0,0,0],  # Row H
        [0,0,0,0,0,0,0,0,0,0],  # Row I
        [0,0,0,0,0,0,0,1,0,1]   # Row J
    ]
    
    model = cp_model.CpModel()

    # Decision variables:
    # x[p][q] is 1 if an airdrop is placed at cell (p,q)
    x = {}
    for p in range(n):
        for q in range(n):
            x[(p, q)] = model.NewBoolVar(f'x_{p}_{q}')
    
    # y[i,j,p,q] is 1 if hut at (i,j) is assigned to the drop at (p,q)
    # Note: we create this variable for every (i,j) even if no hut is present,
    # because of the constraint y <= x.
    y = {}
    for i in range(n):
        for j in range(n):
            for p in range(n):
                for q in range(n):
                    y[(i, j, p, q)] = model.NewBoolVar(f'y_{i}_{j}_{p}_{q}')

    # Constraint (A): Exactly two airdrop locations are selected.
    model.Add(sum(x[(p, q)] for p in range(n) for q in range(n)) == 2)

    # Constraint (B): Each hut (where huts[i][j] == 1) is assigned to exactly one drop location.
    # For cells with no hut (i.e., 0), the assignment sum must be 0.
    for i in range(n):
        for j in range(n):
            if huts[i][j] == 1:
                model.Add(sum(y[(i, j, p, q)] for p in range(n) for q in range(n)) == 1)
            else:
                model.Add(sum(y[(i, j, p, q)] for p in range(n) for q in range(n)) == 0)

    # Constraint (C): A hut can only be assigned to a selected drop location.
    for i in range(n):
        for j in range(n):
            for p in range(n):
                for q in range(n):
                    model.Add(y[(i, j, p, q)] <= x[(p, q)])
                    
    # Objective: Minimize the sum of squared distances of huts to their assigned drop location.
    # Using 0-based indices; the squared Euclidean distance between (i,j) and (p,q)
    # is (i - p)^2 + (j - q)^2.
    objective_terms = []
    for i in range(n):
        for j in range(n):
            if huts[i][j] == 1:
                for p in range(n):
                    for q in range(n):
                        distance_sq = (i - p) * (i - p) + (j - q) * (j - q)
                        objective_terms.append(distance_sq * y[(i, j, p, q)])
                        
    model.Minimize(sum(objective_terms))
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('Optimal drop locations (p,q):')
        drop_locations = []
        for p in range(n):
            for q in range(n):
                if solver.Value(x[(p, q)]) == 1:
                    drop_locations.append((p, q))
                    print(f'  Drop at cell ({p}, {q})')
        print(f'\nObjective value (total squared distance): {solver.ObjectiveValue()}')
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()