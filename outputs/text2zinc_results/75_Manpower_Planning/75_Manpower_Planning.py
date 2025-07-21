# Mathematical Formulation:
'''Below is one complete “translation” of the written description into a mathematical‐programming model. In our formulation the planning horizon is T = 3 years and the three worker “categories” are indexed by j ∈ {1, 2, 3} (for unskilled, semi‐skilled, and skilled, respectively). (Any other index set notation is possible.) In our model the company “moves” from its current (experienced) manpower level Ij and then may add (external) recruits R, may “trim” by redundancies D, and—if needed—may “over‐staff” (that is, to keep extra heads on the payroll when the requirement is lower) paying an extra cost; finally it may “down‐scale” by putting some workers on short–time work S (with every such worker “providing” only half–time production). In addition, we “penalize” any shortfall (or “excess”) in the effective work force versus the yearly requirement by adding extra cost factors (per worker) MoreOneWaste and LessOneWaste. (Comparing the effective work force versus requirement is one way to “capture” the cost impact from any deviation – whether because too few new recruits have survived their “first year” or because redundancies have been applied.)  

We now define:

■ Indices and parameters:
 • t = 1, 2, 3 (years)  
 • j ∈ {1, 2, 3} (worker categories)  
 • aₜⱼ: estimated manpower requirement in year t for category j. (For example,  
  a₁₁ = 1000, a₁₂ = 1400, a₁₃ = 1000,  
  a₂₁ = 500, a₂₂ = 2000, a₂₃ = 1500,   
  a₃₁ = 0,  a₃₂ = 2500, a₃₃ = 2000.)  
 • Iⱼ: current (initial) strength for category j (I = [2000, 1500, 1000]).  
 • Rcapⱼ: maximum number of recruits that can be hired in any year for category j  
  (Rcap = [500, 800, 500]).  
 • N: maximum number of workers that can be put on short–time work in any category (N = 50).  
 • M: maximum total number of “over–staffed” (excess) workers allowed over the whole company in any year (M = 150).  
 • C₍ᴿ₎ⱼ: cost of a redundancy (layoff) in category j (CostRedundancy = [200, 500, 500]).  
 • C₍ᴼ₎ⱼ: cost per extra (over–staff) employee in category j (CostOverman = [1500, 2000, 3000]).  
 • C₍ˢ₎ⱼ: cost per employee per year put on short–time work in category j (CostShort = [500, 400, 400]).  
 • \(\gamma^-_j\) = LessOneWasteⱼ: “cost reduction” per unit “over–staffing” (i.e. if one has surplus effective capacity, a saving of 0.25, 0.2, or 0.1 is realized for j = 1,2,3, respectively).  
 • \(\gamma^+_j\) = MoreOneWasteⱼ: “additional cost” per unit shortage (if one has a shortfall, an extra cost of 0.1, 0.05, 0.05 is incurred for j = 1,2,3, respectively).  

The idea behind the last two parameters is to “adjust” the cost when the effective labour (after allowing for short–time workers producing only half–time) deviates from the requirement.

■ Decision Variables (for each year t and category j):

 (1) Workforce and flows  
  Yₜⱼ ≥ 0  : total number of workers “on the books” at the end of year t in category j.  
  Rₜⱼ ≥ 0  : number of new recruits hired in period t in category j, with  
             Rₜⱼ ≤ Rcapⱼ.  
  Dₜⱼ ≥ 0  : number of workers made redundant in period t in category j.  

 The dynamics are modeled by:  
  • For t = 1: Y₁ⱼ = Iⱼ + R₁ⱼ – D₁ⱼ.  
  • For t = 2, 3: Yₜⱼ = Y₍ₜ₋₁₎ⱼ + Rₜⱼ – Dₜⱼ.

 (2) Short–time working  
  Sₜⱼ ≥ 0  : number of workers in category j placed on short–time work in year t  
         with Sₜⱼ ≤ N.  
  An employee on short–time work “produces” only half the capacity of a full–time worker.

 (3) “Deviation” variables that capture under– or over–fulfilment of the requirement  
  Let the effective work force in year t and category j be  
    Eₜⱼ = Yₜⱼ – 0.5\,Sₜⱼ.
  Then we define the nonnegative “slack/deviation” variables  
  Uₜⱼ⁺ ≥ 0  : shortage (if Eₜⱼ is less than aₜⱼ, this “deficit” is penalized)  
  Uₜⱼ⁻ ≥ 0  : surplus (if Eₜⱼ exceeds aₜⱼ, this extra capacity yields a cost‐saving, though extra “over–staffing” cost is also incurred).

 The balancing (or “requirement–fulfilment”) equation is:  
  Eₜⱼ + Uₜⱼ⁻ – Uₜⱼ⁺ = aₜⱼ.  
 In other words, any extra effective workforce above the requirement is Uₜⱼ⁻ (and costs extra overman cost C₍ᴼ₎ⱼ but gives a “saving” γ⁻ⱼ) while any shortfall Uₜⱼ⁺ is penalized at rate γ⁺ⱼ.

 A company–wide upper bound is imposed on the total “over–staffing” (the surplus part):  
  \(\sum_{j=1}^3 U_{t j}^- \le M,\) for each year t.

■ Objective Function

The company’s declared objective is to minimize total costs over the planning horizon. In our formulation the cost incurred in each period and category comes from:
 (a) paying redundancies (cost C₍ᴿ₎ⱼ per worker),  
 (b) hiring more workers than needed (over–staffing cost C₍ᴼ₎ⱼ per extra worker, applied to Uₜⱼ⁻),  
 (c) using short–time work (cost C₍ˢ₎ⱼ per worker put on short–time), and  
 (d) incurring penalty (or receiving “savings”) when the effective work force Eₜⱼ deviates from the requirement, i.e.  
  – a penalty of \(\gamma^+_j\) per shortfall unit Uₜⱼ⁺ and  
  – a “saving” (or reduction in cost) of \(\gamma^-_j\) per surplus unit Uₜⱼ⁻.

Thus the total (annual) cost is
  \(\displaystyle \sum_{t=1}^3\sum_{j=1}^3 \Bigl[ C_{(R)j}\,D_{t j} + \,C_{(O)j}\,U_{t j}^- + C_{(S)j}\,S_{t j} + \gamma^+_j\,U_{t j}^+ - \gamma^-_j\,U_{t j}^- \Bigr].\)

Because all costs add, the overall objective is:  
  Minimize  Z = \(\displaystyle \sum_{t=1}^3 \sum_{j=1}^3 \Bigl[ C_{(R)j}\,D_{t j} + C_{(O)j}\,U_{t j}^- + C_{(S)j}\,S_{t j} + \gamma^+_j\,U_{t j}^+ - \gamma^-_j\,U_{t j}^- \Bigr].\)

■ Complete Formulation

We now put everything together. (Any reader familiar with operations research will recognize that additional “bookkeeping” variables or a slightly different state–transition may also be used. Here we have opted for one self–contained formulation.)  

\[
\begin{align*}
\textbf{Indices:}\quad & t=1,2,3,\quad j=1,2,3. \\[1mm]
\textbf{Parameters:}\quad & a_{t j} \quad \text{(requirement)},\\[1mm]
& I_j,\quad Rcap_j,\quad N,\quad M,\\[1mm]
& C_{(R)j},\quad C_{(O)j},\quad C_{(S)j},\\[1mm]
& \gamma^-_j,\quad \gamma^+_j. \\[1mm]
\textbf{Decision variables:}\quad & Y_{t j} \ge 0,\quad R_{t j} \ge 0,\quad D_{t j} \ge 0,\quad S_{t j} \ge 0,\\[1mm]
& U^+_{t j} \ge 0,\quad U^-_{t j} \ge 0. \\[2mm]
\textbf{Model:}\\[2mm]
\text{Minimize}\quad & Z = \sum_{t=1}^{3} \sum_{j=1}^{3} \Bigl[ C_{(R)j}\,D_{t j} + C_{(O)j}\,U^-_{t j} + C_{(S)j}\,S_{t j} + \gamma^+_j\,U^+_{t j} - \gamma^-_j\,U^-_{t j} \Bigr] \quad (1)\\[2mm]
\text{subject to:}\\[2mm]
\textbf{(a) Workforce dynamics:} \\
& Y_{1 j} = I_j + R_{1 j} - D_{1 j}, \quad \forall j, \quad (2a)\\[1mm]
& Y_{t j} = Y_{t-1, j} + R_{t j} - D_{t j}, \quad \forall j,\; t=2,3, \quad (2b)\\[2mm]
\textbf{(b) Effective workforce and requirement balance:} \\
& \bigl(Y_{t j} - 0.5\,S_{t j}\bigr) + U^-_{t j} - U^+_{t j} = a_{t j}, \quad \forall j,\; t=1,2,3, \quad (3)\\[2mm]
\textbf{(c) Overstaff (company–wide) limit:} \\
& \sum_{j=1}^{3} U^-_{t j} \le M,\quad \forall t=1,2,3, \quad (4)\\[2mm]
\textbf{(d) Recruitment limit:} \\
& R_{t j} \le Rcap_j,\quad \forall j,\; t=1,2,3, \quad (5)\\[2mm]
\textbf{(e) Short–time working limit:} \\
& S_{t j} \le N,\quad \forall j,\; t=1,2,3, \quad (6)\\[2mm]
\textbf{(f) Non–negativity:} \\
& Y_{t j},\, R_{t j},\, D_{t j},\, S_{t j},\, U^+_{t j},\, U^-_{t j} \ge 0,\quad \forall j,\; t=1,2,3. \quad (7)
\end{align*}
\]

■ Explanation

1. The “workforce dynamics” (constraints (2a) and (2b)) explain how the in–house staff evolves from the current strength Ij through recruitment R and controlled layoffs D.  
2. Constraint (3) computes the effective workforce in year t and category j as the total Yₜⱼ minus half the number placed on short–time Sₜⱼ. Any shortage (U⁺ₜⱼ) or surplus (U⁻ₜⱼ) is “balanced” so that the net effective capacity meets the requirement aₜⱼ.  
3. Constraint (4) ensures that across categories the “over–staffed” (extra, surplus) workers do not exceed the overall limit M.  
4. Constraints (5) and (6) enforce the annual recruitment and short–time work limits.  
5. The objective (1) minimizes the sum over periods and categories of the costs for redundancies, over–staffing, and short–time work plus any additional shortage penalties (at rate γ⁺ⱼ) while “rewarding” (by cost reduction at rate γ⁻ⱼ) any surplus.

This model is fully self–contained and reflects all aspects of the real–world problem description without trivializing any scenario. (Any implementation – for example in OR–Tools – would simply need to instantiate the given parameters and this model structure.)'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver using CBC as the backend
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    T = 3  # years
    J = 3  # worker categories (j=0: unskilled, j=1: semi-skilled, j=2: skilled)

    # Parameters
    # a[t][j]: manpower requirement in year t (t=0,1,2)
    a = [
        [1000, 1400, 1000],  # year 1
        [500, 2000, 1500],   # year 2
        [0, 2500, 2000]      # year 3
    ]
    
    # Initial strength for each category (I)
    I = [2000, 1500, 1000]
    
    # Maximum recruitment in any year for each category (Rcap)
    Rcap = [500, 800, 500]
    
    # Maximum number of workers put on short-time work in any category (N)
    N = 50
    
    # Maximum total overstaffing allowed company-wide per year (M)
    M = 150

    # Costs and penalties per category
    CostRedundancy = [200, 500, 500]   # C(R)j: cost of a redundancy (layoff)
    CostOverman = [1500, 2000, 3000]     # C(O)j: cost per extra (overstaff) worker
    CostShort = [500, 400, 400]          # C(S)j: cost per worker on short-time work
    gamma_minus = [0.25, 0.2, 0.1]       # cost reduction per surplus unit (U^-)
    gamma_plus = [0.1, 0.05, 0.05]       # penalty per shortage unit (U^+)

    # Decision Variables:
    # Y[t][j]: total workers on the books at end of year t in category j (integer)
    # R[t][j]: number of recruits in year t in category j (integer)
    # D[t][j]: number of redundancies in year t in category j (integer)
    # S[t][j]: number on short-time work in year t in category j (integer)
    # Uplus[t][j]: shortage (continuous)
    # Uminus[t][j]: surplus (continuous)
    Y = [[solver.IntVar(0, solver.infinity(), f"Y_{t}_{j}") for j in range(J)] for t in range(T)]
    R = [[solver.IntVar(0, Rcap[j], f"R_{t}_{j}") for j in range(J)] for t in range(T)]
    D = [[solver.IntVar(0, solver.infinity(), f"D_{t}_{j}") for j in range(J)] for t in range(T)]
    S = [[solver.IntVar(0, N, f"S_{t}_{j}") for j in range(J)] for t in range(T)]
    Uplus = [[solver.NumVar(0.0, solver.infinity(), f"Uplus_{t}_{j}") for j in range(J)] for t in range(T)]
    Uminus = [[solver.NumVar(0.0, solver.infinity(), f"Uminus_{t}_{j}") for j in range(J)] for t in range(T)]
    
    # (a) Workforce dynamics
    # For t = 0: Y[0][j] = I[j] + R[0][j] - D[0][j]
    for j in range(J):
        solver.Add(Y[0][j] == I[j] + R[0][j] - D[0][j])
    
    # For t = 1,2: Y[t][j] = Y[t-1][j] + R[t][j] - D[t][j]
    for t in range(1, T):
        for j in range(J):
            solver.Add(Y[t][j] == Y[t-1][j] + R[t][j] - D[t][j])
    
    # (b) Effective workforce and requirement balance:
    # For each year t and category j:
    # (Y[t][j] - 0.5 * S[t][j]) + Uminus[t][j] - Uplus[t][j] = a[t][j]
    for t in range(T):
        for j in range(J):
            solver.Add(Y[t][j] - 0.5 * S[t][j] + Uminus[t][j] - Uplus[t][j] == a[t][j])
    
    # (c) Overstaffing company-wide limit for each year: sum_j Uminus[t][j] <= M
    for t in range(T):
        solver.Add(sum(Uminus[t][j] for j in range(J)) <= M)
    
    # (d) Recruitment limit (already enforced by variable bounds, but can add explicitly)
    for t in range(T):
        for j in range(J):
            solver.Add(R[t][j] <= Rcap[j])
    
    # (e) Short-time working limit (already enforced by variable bounds S[t][j] <= N)

    # Objective Function
    # Minimize total cost = sum_t,j [ CostRedundancy[j]*D[t][j] + CostOverman[j]*Uminus[t][j]
    #                              + CostShort[j]*S[t][j] + gamma_plus[j]*Uplus[t][j] - gamma_minus[j]*Uminus[t][j] ]
    objective = solver.Objective()
    for t in range(T):
        for j in range(J):
            objective.SetCoefficient(D[t][j], CostRedundancy[j])
            # Overstaffing cost net: cost of overman minus saving for surplus
            objective.SetCoefficient(Uminus[t][j], CostOverman[j] - gamma_minus[j])
            objective.SetCoefficient(S[t][j], CostShort[j])
            objective.SetCoefficient(Uplus[t][j], gamma_plus[j])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Optimal objective value =', solver.Objective().Value())
        for t in range(T):
            print(f"Year {t + 1}:")
            for j in range(J):
                print(f"  Category {j + 1}:")
                print(f"    Y (End Workforce)    = {Y[t][j].solution_value()}")
                print(f"    R (Recruits)         = {R[t][j].solution_value()}")
                print(f"    D (Redundancies)     = {D[t][j].solution_value()}")
                print(f"    S (Short-time work)  = {S[t][j].solution_value()}")
                print(f"    Uplus (Shortage)     = {Uplus[t][j].solution_value()}")
                print(f"    Uminus (Surplus)     = {Uminus[t][j].solution_value()}")
        print()
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()