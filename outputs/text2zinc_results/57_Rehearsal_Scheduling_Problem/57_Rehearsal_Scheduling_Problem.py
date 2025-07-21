# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Sets and Parameters:} & & \\[1mm]
P &=& \{1,\ldots,n\} \quad \text{(set of pieces), with } n = \texttt{num\_pieces},\\[1mm]
J &=& \{1,\ldots,m\} \quad \text{(set of players), with } m = \texttt{num\_players},\\[1mm]
d_i &\in& \mathbb{R}_{>0} \quad \forall\, i\in P \quad \text{(duration of piece } i\text{)},\\[1mm]
r_{ji} &\in& \{0,1\} \quad \forall\, j\in J,\; i\in P,\quad \text{with } r_{ji}=1 \text{ if player } j \text{ is required in piece } i,\\[1mm]
M &>& 0\quad \text{a sufficiently large constant.}\\[2mm]
\textbf{Decision Variables:} & & \\[1mm]
S_i &\in& \mathbb{R}_{\ge 0} \quad \forall\, i\in P,\quad \text{start time of piece } i,\\[1mm]
z_{ik} &\in& \{0,1\} \quad \forall\, i,k \in P,\; i\neq k,\quad 
\begin{array}{l}
\text{with } z_{ik}=1 \text{ if piece } i \text{ is scheduled before piece } k,
\end{array}\\[1mm]
A_j &\in& \mathbb{R}_{\ge 0} \quad \forall\, j\in J,\quad \text{arrival time of player } j,\\[1mm]
D_j &\in& \mathbb{R}_{\ge 0} \quad \forall\, j\in J,\quad \text{departure time of player } j.\\[2mm]
\textbf{Auxiliary Definitions:} & & \\[1mm]
\text{For each piece } i,\quad C_i &=& S_i + d_i \quad \text{(completion time of piece } i\text{)}.\\[2mm]
\text{For each player } j, \quad \text{the total playing time is } T_j &=& \sum_{i\in P} r_{ji}\,d_i.\\[2mm]
\text{The waiting time for player } j \text{ is } W_j &=& \Bigl(D_j - A_j\Bigr) - T_j.
\end{array}
\]

We now present the complete mathematical model.

\[
\begin{array}{rcll}
\textbf{Minimize:} & \displaystyle \min \; \sum_{j\in J} \; W_j &=& \displaystyle \min \; \sum_{j\in J} \Biggl[\, D_j - A_j - \sum_{i\in P} r_{ji}\,d_i \Biggr] & \quad \text{(Total waiting time)}\\[2mm]
\textbf{Subject to:} & & & \\[1mm]
\textbf{(a) \; Disjunctive Ordering Constraints:} & & & \\
& S_i + d_i \le S_k + M\,(1 - z_{ik}) &\quad \forall\, i,k\in P,\; i\ne k, & (1)\\[1mm]
& z_{ik} + z_{ki} = 1 &\quad \forall\, i,k\in P,\; i\ne k. & (2)\\[2mm]
\textbf{(b) \; Player Arrival and Departure Constraints:} & & & \\
& A_j \le S_i       &\quad \forall\, j\in J,\; \forall\, i\in P \text{ with } r_{ji}=1, & (3)\\[1mm]
& D_j \ge S_i + d_i  &\quad \forall\, j\in J,\; \forall\, i\in P \text{ with } r_{ji}=1, & (4)\\[2mm]
\textbf{(c) \; Reference Start Time:} & & & \\
& S_{i_0} = 0, &\quad \text{for some } i_0\in P \quad (\text{e.g., choose } i_0=1), & (5)\\[2mm]
\textbf{(d) \; Implicit Continuity:} & & & \\
& \text{(No idle time is introduced since the model will naturally set } S_i \text{ to yield a continuous schedule)}. & & 
\end{array}
\]

\vspace{2mm}
\textbf{Remarks:}

1. The variables S_i determine the start times of the pieces. The binary variables z_{ik} enforce a complete ordering (permutation) of all pieces.  
2. For each player j, the variables A_j and D_j are “free” to be set as early as possible and as late as necessary subject to (3) and (4); hence at optimality, A_j equals the minimum start time among the pieces in which player j participates, and D_j equals the maximum completion time among those pieces.  
3. The objective function minimizes the sum over players of (departure time minus arrival time minus the total playing duration), which is exactly the sum of waiting (idle) times.  
4. Constraint (5) eliminates time-shift invariance by fixing the start time of one arbitrarily chosen piece.

This full formulation precisely captures the scheduling problem described, is feasible (with proper data) and bounded, and can be directly transformed into an OR-Tools implementation by another modeler.
\]'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data
    num_pieces = 5
    num_players = 3
    durations = [4, 6, 3, 5, 7]
    # rehearsal[j][i] = 1 if player j is required in piece i
    rehearsal = [
        [1, 1, 0, 1, 0],
        [0, 1, 1, 0, 1],
        [1, 1, 0, 1, 1]
    ]
    
    # We set a large value for "M" and a horizon for start times.
    M = 100
    horizon = M  # A safe upper bound on start times
    
    model = cp_model.CpModel()
    
    # Decision Variables:
    # Start times for pieces.
    S = [model.NewIntVar(0, horizon, f"S_{i}") for i in range(num_pieces)]
    
    # For ordering: For each unordered pair (i,j) with i < j, create binary variable z[i,j]
    z = {}
    for i in range(num_pieces):
        for j in range(i+1, num_pieces):
            z[(i, j)] = model.NewBoolVar(f"z_{i}_{j}")
    
    # Arrival and departure times for players.
    A = [model.NewIntVar(0, horizon, f"A_{j}") for j in range(num_players)]
    D = [model.NewIntVar(0, horizon, f"D_{j}") for j in range(num_players)]
    
    # Constraint (c): Fix the start time of the first piece to 0.
    model.Add(S[0] == 0)
    
    # (a) Disjunctive Ordering Constraints
    # For each unordered pair of distinct pieces (i,j), use z to force an ordering.
    for i in range(num_pieces):
        for j in range(i+1, num_pieces):
            # If z[(i,j)] is true then piece i is scheduled before piece j:
            #    S[i] + durations[i] <= S[j] + M*(1 - z[(i,j)])
            model.Add(S[i] + durations[i] <= S[j] + M * (1 - z[(i, j)]))
            # If z[(i,j)] is false then piece j precedes piece i:
            #    S[j] + durations[j] <= S[i] + M*(z[(i,j)])
            model.Add(S[j] + durations[j] <= S[i] + M * z[(i, j)])
    
    # (b) Player Arrival and Departure Constraints.
    # For each player j and each piece i for which they are required:
    for j in range(num_players):
        for i in range(num_pieces):
            if rehearsal[j][i] == 1:
                model.Add(A[j] <= S[i])
                model.Add(D[j] >= S[i] + durations[i])
    
    # Compute constant playing time for each player.
    playing_time = []
    for j in range(num_players):
        pt = sum(durations[i] for i in range(num_pieces) if rehearsal[j][i] == 1)
        playing_time.append(pt)
    
    # Define waiting time for each player: (D[j] - A[j] - playing_time[j])
    waiting = []
    for j in range(num_players):
        # Create an integer variable for waiting time.
        w = model.NewIntVar(0, horizon, f"W_{j}")
        model.Add(w == D[j] - A[j] - playing_time[j])
        waiting.append(w)
    
    # Objective: minimize total waiting time.
    model.Minimize(sum(waiting))
    
    # Solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution:")
        # Print start times for pieces
        for i in range(num_pieces):
            print(f"Piece {i}: start = {solver.Value(S[i])}, duration = {durations[i]}, finish = {solver.Value(S[i]) + durations[i]}")
        
        # Print ordering decisions (for i < j)
        print("\nOrdering decisions:")
        for i in range(num_pieces):
            for j in range(i+1, num_pieces):
                if solver.Value(z[(i, j)]) == 1:
                    print(f"Piece {i} is before Piece {j}")
                else:
                    print(f"Piece {j} is before Piece {i}")
        
        # Print players' arrival, departure, waiting time and playing time.
        print("\nPlayers' schedules:")
        for j in range(num_players):
            arrival = solver.Value(A[j])
            departure = solver.Value(D[j])
            wait = solver.Value(waiting[j])
            print(f"Player {j}: arrival = {arrival}, departure = {departure}, playing_time = {playing_time[j]}, waiting = {wait}")
        
        print("\nTotal waiting time =", solver.ObjectiveValue())
    else:
        print("The problem is infeasible.")

if __name__ == '__main__':
    main()