# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Indices:} & i,j \in I=\{1,2,\ldots,10\}. & \\[1mm]
\textbf{Parameters:} & 
\begin{array}{l}
\text{For each aircraft } i: \quad \displaystyle EA_i = \text{EarliestLandingTime}_i, \quad LA_i = \text{LatestLandingTime}_i, \quad TA_i = \text{TargetLandingTime}_i,\\[1mm]
\quad\quad\quad\quad\;\; PTB_i = \text{PenaltyTimeBeforeTarget}_i, \quad PTA_i = \text{PenaltyTimeAfterTarget}_i,\\[1mm]
\text{For each ordered pair } (i,j), \quad S_{ij} = \text{SeparationTimeMatrix}_{ij}.\\[1mm]
\end{array} \\[2mm]
\textbf{Decision Variables:} & 
\begin{array}{l}
t_i \in \mathbb{R}, \quad \text{the landing time of aircraft } i, \quad \forall i\in I,\\[1mm]
e_i \ge 0, \quad \text{the earliness (time by which landing is before the target)} \text{ for aircraft } i,\\[1mm]
l_i \ge 0, \quad \text{the lateness (time by which landing is after the target)} \text{ for aircraft } i,\\[1mm]
\delta_{ij} \in \{0,1\}, \quad \text{a binary variable with } \delta_{ij}=1 \text{ if aircraft } i \text{ lands before } j, \quad \forall i,j\in I,\; i<j.
\end{array} \\[2mm]
\textbf{Auxiliary Constant:} & M \text{ is a sufficiently large positive constant.} \\[3mm]
\textbf{Mathematical Model:} & & \\[1mm]
\begin{array}{rcl}
\displaystyle \min \quad & \displaystyle \sum_{i=1}^{10}\Big( PTB_i\;e_i + PTA_i\;l_i \Big) & \quad \text{(Total penalty)} \\[2mm]
\text{subject to} \quad &&\\[1mm]
& t_i + e_i - l_i = TA_i, & \forall i\in I, \quad \text{(Deviation representation)} \\[2mm]
& EA_i \le t_i \le LA_i, & \forall i\in I, \quad \text{(Landing window constraints)} \\[2mm]
& t_j \ge t_i + S_{ij} - M\,(1-\delta_{ij}), & \forall i,j\in I,\; i<j, \quad \text{(Separation if } i \text{ lands before } j\text{)} \\[2mm]
& t_i \ge t_j + S_{ji} - M\,\delta_{ij}, & \forall i,j\in I,\; i<j, \quad \text{(Separation if } j \text{ lands before } i\text{)} \\[2mm]
& \delta_{ij} + \delta_{ji} = 1, & \forall i,j\in I,\; i<j, \quad \text{(One ordering must hold)} \\[2mm]
& e_i \ge 0,\; l_i \ge 0, & \forall i\in I, \quad \text{(Nonnegativity of deviation variables)} \\[2mm]
& \delta_{ij} \in \{0,1\}, & \forall i,j\in I,\; i<j. & \\
\end{array}
\end{array}
\]

Here is a breakdown of the formulation:

1. Decision Variables:  
   • t₍ᵢ₎ is the continuous landing time for aircraft i and is bounded by EAᵢ and LAᵢ.  
   • e₍ᵢ₎ and l₍ᵢ₎ are nonnegative continuous variables that represent, respectively, the amount by which the landing is earlier than or later than the target TAᵢ. They are linked to tᵢ by tᵢ + eᵢ − lᵢ = TAᵢ.  
   • δ₍ᵢⱼ₎ is a binary variable that establishes the landing order between any two aircraft (only defined for i < j).

2. Objective Function:  
   The goal is to minimize the total penalty which is the sum of penalty costs for landing earlier than target (with coefficient PTBᵢ) and for landing later than target (with coefficient PTAᵢ) over all aircraft.

3. Constraints:  
   • The equality tᵢ + eᵢ − lᵢ = TAᵢ ensures that if an aircraft lands before its target time, the earliness variable takes up the difference (and lᵢ becomes 0), and vice‐versa.  
   • The landing window EAᵢ ≤ tᵢ ≤ LAᵢ forces each aircraft to land within its prescribed time window.  
   • The separation constraints employ a big‑M formulation along with binary variables δ₍ᵢⱼ₎ to guarantee that the required minimum time separation S₍ᵢⱼ₎ is maintained in the landing sequence. Specifically, if aircraft i lands before j (δ₍ᵢⱼ₎ = 1) then the first separation inequality is active; if not, the second is active.  
   • The constraint δ₍ᵢⱼ₎ + δ₍ⱼᵢ₎ = 1 (for i<j) ensures a unique ordering between every pair of aircraft.

This complete model represents the Aircraft Landing Problem in full detail and is both feasible and bounded (for an appropriate choice of M).'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Data Input
    TotalAircrafts = 10
    EA = [129, 195, 89, 90, 110, 120, 124, 126, 135, 160]
    TA = [155, 258, 98, 106, 123, 135, 138, 140, 150, 180]
    LA = [689, 653, 517, 501, 634, 603, 657, 592, 510, 604]
    PTA = [24, 25, 10, 13, 10, 20, 24, 12, 16, 27]
    PTB = [24, 25, 10, 13, 10, 20, 24, 12, 16, 27]
    
    # SeparationTimeMatrix as a 2D list (0-indexed)
    sep = [
        [99999, 11,    12, 10, 10, 11, 12, 12, 12, 10],
        [14, 99999,   10, 12, 12, 10, 13, 14, 11, 13],
        [11, 14,   99999, 10, 11, 12, 9, 10, 11, 13],
        [8, 10,    11, 99999, 8, 12, 8, 8, 9, 9],
        [10, 10,   14, 14, 99999, 10, 8, 14, 11, 10],
        [11, 9,    11, 11, 14, 99999, 9, 9, 9, 12],
        [12, 13,   13, 8, 14, 14, 99999, 8, 13, 11],
        [14, 8,    8, 14, 12, 8, 14, 99999, 8, 12],
        [11, 12,   11, 11, 13, 11, 11, 14, 99999, 9],
        [11, 9,    10, 10, 8, 14, 8, 14, 9, 99999]
    ]
    
    # Big M value sufficiently large. For our case, we choose:
    M = 10000
    
    model = cp_model.CpModel()
    
    # Decision variables
    t = []
    e = []
    l = []
    for i in range(TotalAircrafts):
        # Define landing time variable for each aircraft
        t_i = model.NewIntVar(EA[i], LA[i], f't_{i}')
        t.append(t_i)
        # Earliness and lateness variables (can be zero up to a maximum bound)
        # Upper bound can be defined as a difference from target landing time to the extreme.
        e_i = model.NewIntVar(0, TA[i] - EA[i] if TA[i] - EA[i] > 0 else 0, f'e_{i}')
        l_i = model.NewIntVar(0, LA[i] - TA[i] if LA[i] - TA[i] > 0 else 0, f'l_{i}')
        e.append(e_i)
        l.append(l_i)
    
    # Binary variables for ordering for each pair (i, j) with i < j.
    delta = {}
    for i in range(TotalAircrafts):
        for j in range(i+1, TotalAircrafts):
            delta[(i, j)] = model.NewBoolVar(f'delta_{i}_{j}')
    
    # Constraints
    # Deviation constraints: t_i + e_i - l_i = TA[i]
    for i in range(TotalAircrafts):
        model.Add(t[i] + e[i] - l[i] == TA[i])
    
    # Separation constraints for each pair of aircraft (i, j), i < j.
    for i in range(TotalAircrafts):
        for j in range(i+1, TotalAircrafts):
            # If aircraft i lands before j (delta = 1): t_j >= t_i + S_ij
            model.Add(t[j] >= t[i] + sep[i][j] - M * (1 - delta[(i, j)]))
            # If aircraft j lands before i (delta = 0): t_i >= t[j] + S_ji
            model.Add(t[i] >= t[j] + sep[j][i] - M * (delta[(i, j)]))
    
    # Objective: Minimize total penalty = sum(PTB[i]*e[i] + PTA[i]*l[i])
    objective_terms = []
    for i in range(TotalAircrafts):
        objective_terms.append(PTB[i] * e[i])
        objective_terms.append(PTA[i] * l[i])
    model.Minimize(sum(objective_terms))
    
    # Create solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal solution found:')
        print(f'Objective value: {solver.ObjectiveValue()}')
        for i in range(TotalAircrafts):
            print(f'Aircraft {i+1}: Landing time = {solver.Value(t[i])}, ' +
                  f'Earliness = {solver.Value(e[i])}, Lateness = {solver.Value(l[i])}')
        print('Ordering (for i<j, delta[i,j] = 1 means aircraft i lands before j):')
        for i in range(TotalAircrafts):
            for j in range(i+1, TotalAircrafts):
                print(f'delta[{i+1},{j+1}] = {solver.Value(delta[(i, j)])}', end='  ')
            print()
    else:
        print('No feasible solution found.')

if __name__ == '__main__':
    main()