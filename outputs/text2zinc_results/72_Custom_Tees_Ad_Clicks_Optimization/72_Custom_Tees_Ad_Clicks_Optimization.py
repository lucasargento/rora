# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Parameters:} & & & \\
A &=& \text{number of ad types}, & \quad \text{(in our example, } A=3\text{)};\\[1mm]
\text{GoalYoung} &=& \text{minimum total clicks desired by visitors aged 18–25}, & \quad (500);\\[1mm]
\text{GoalOld} &=& \text{minimum total clicks desired by visitors older than 25}, & \quad (600);\\[1mm]
\text{GoalUniqueYoung} &=& \text{minimum unique clicks required from visitors aged 18–25}, & \quad (250);\\[1mm]
\text{GoalUniqueOld} &=& \text{minimum unique clicks required from visitors older than 25}, & \quad (300);\\[1mm]
\text{YoungPct}_i &=& \text{estimated percentage of clicks from 18–25 visitors for ad } i, & \quad \text{given by YoungClicks }[i];\\[1mm]
\text{OldPct}_i &=& \text{estimated percentage of clicks from visitors older than 25 for ad } i, & \quad \text{given by OldClicks }[i];\\[1mm]
\text{UniquePct}_i &=& \text{estimated percentage of unique clicks (applies uniformly by age) for ad } i, & \quad \text{given by UniqueClicks }[i];\\[1mm]
c_i &=& \text{cost per 1000 clicks for ad } i, & \quad \text{given by Costs }[i];\\[1mm]
M_i &=& \text{maximum allowable clicks for ad } i, & \quad \text{given by MaxClicks }[i].\\[3mm]
\multicolumn{4}{l}{\textbf{Decision Variables:}}\\[2mm]
x_i &\ge& 0, & \quad \text{number of clicks purchased for ad type } i,\quad i=1,\ldots,A.
\end{array}
\]

\vspace{2mm}
\[
\begin{array}{rcl}
\textbf{Minimize:} & \displaystyle \sum_{i=1}^{A} c_i\,\frac{x_i}{1000} & \quad \text{(minimize total cost)}. \\[3mm]
\textbf{Subject to:} & &\\[2mm]
\displaystyle \sum_{i=1}^{A} \frac{\text{YoungPct}_i}{100}\, x_i &\ge& \text{GoalYoung}, \\[2mm]
\displaystyle \sum_{i=1}^{A} \frac{\text{OldPct}_i}{100}\, x_i &\ge& \text{GoalOld}, \\[2mm]
\displaystyle \sum_{i=1}^{A} \left( \frac{\text{YoungPct}_i}{100}\cdot\frac{\text{UniquePct}_i}{100}\right) x_i &\ge& \text{GoalUniqueYoung}, \\[2mm]
\displaystyle \sum_{i=1}^{A} \left( \frac{\text{OldPct}_i}{100}\cdot\frac{\text{UniquePct}_i}{100}\right) x_i &\ge& \text{GoalUniqueOld}, \\[2mm]
x_i &\le& M_i, \quad i=1,\ldots,A. \\[2mm]
&&\\[2mm]
x_i &\ge& \varepsilon_i > 0, \quad \text{for each } i \text{ (if a positive purchase is required in each ad type)}.
\end{array}
\]

\vspace{2mm}
\textbf{Explanation:}

1. \textbf{Decision Variables:}  
  For each ad type indexed by \( i \), the variable \( x_i \) represents the number of clicks Custom Tees purchases through that ad. The domain is \( x_i \ge 0 \) (and can be further restricted to be strictly positive if desired by \(\varepsilon_i>0\) to avoid trivial scenarios).

2. \textbf{Objective Function:}  
  The objective is to minimize the overall cost incurred for the purchased clicks. Since each ad type \( i \) has a cost \( c_i \) per 1000 clicks, the cost incurred by ad \( i \) is \( c_i\,\frac{x_i}{1000} \). Thus, the total cost is  
  \[
  \sum_{i=1}^{A} c_i\,\frac{x_i}{1000}.
  \]

3. \textbf{Constraints:}
  (a) The first two constraints ensure that the total clicks from each age group meet or exceed their respective goals. For ad type \( i \), the percentage of clicks from young visitors is \(\frac{\text{YoungPct}_i}{100}\) and from older visitors is \(\frac{\text{OldPct}_i}{100}\). Hence:  
  \[
  \sum_{i=1}^{A} \frac{\text{YoungPct}_i}{100}\, x_i \ge \text{GoalYoung},\quad
  \sum_{i=1}^{A} \frac{\text{OldPct}_i}{100}\, x_i \ge \text{GoalOld}.
  \]

  (b) The next two constraints ensure that the unique clicks goals by age are satisfied. Assuming the estimated percentage of unique clicks applies uniformly across age groups, the unique young clicks from ad \( i \) equal \(\frac{\text{UniquePct}_i}{100}\) times the young clicks \(\frac{\text{YoungPct}_i}{100}\, x_i\), and similarly for older visitors. Therefore,  
  \[
  \sum_{i=1}^{A} \left( \frac{\text{YoungPct}_i}{100}\cdot\frac{\text{UniquePct}_i}{100}\right) x_i \ge \text{GoalUniqueYoung},\quad
  \sum_{i=1}^{A} \left( \frac{\text{OldPct}_i}{100}\cdot\frac{\text{UniquePct}_i}{100}\right) x_i \ge \text{GoalUniqueOld}.
  \]

  (c) Finally, each ad type has an upper limit on the number of clicks purchasable:  
  \[
  x_i \le M_i,\quad \forall\ i=1,\ldots,A.
  \]
  An additional constraint \( x_i \ge \varepsilon_i > 0 \) (with small positive \(\varepsilon_i\)) may be imposed to avoid the trivial solution of setting almost all \( x_i = 0 \) except one.

This complete formulation is both feasible and bounded given the problem data, and it fully reflects the stated real-world requirements without any simplification.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the linear solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print('Solver not created.')
        return

    # Problem data
    A = 3
    GoalYoung = 500
    GoalOld = 600
    GoalUniqueYoung = 250
    GoalUniqueOld = 300
    
    YoungClicks = [40, 30, 70]      # percentage values, e.g., 40 means 40%
    OldClicks = [60, 70, 30]        # percentage values, e.g., 60 means 60%
    Costs = [75, 100, 120]          # cost per 1000 clicks
    MaxClicks = [600, 300, 300]
    UniqueClicks = [40, 75, 90]     # percentage values
    
    # Decision variables: number of clicks purchased for each ad type.
    # Lower bound is 0; if strictly positive purchase is required, a small epsilon can be used.
    x = [solver.NumVar(0.0, MaxClicks[i], f'x_{i}') for i in range(A)]
    
    # Objective: Minimize total cost = sum(c_i * x_i / 1000)
    objective = solver.Objective()
    for i in range(A):
        objective.SetCoefficient(x[i], Costs[i] / 1000)
    objective.SetMinimization()

    # Constraint 1: Total clicks from young visitors must meet the GoalYoung.
    # sum((YoungClicks[i]/100) * x_i) >= GoalYoung
    constraint_young = solver.Constraint(GoalYoung, solver.infinity())
    for i in range(A):
        constraint_young.SetCoefficient(x[i], YoungClicks[i] / 100.0)
    
    # Constraint 2: Total clicks from old visitors must meet the GoalOld.
    # sum((OldClicks[i]/100) * x_i) >= GoalOld
    constraint_old = solver.Constraint(GoalOld, solver.infinity())
    for i in range(A):
        constraint_old.SetCoefficient(x[i], OldClicks[i] / 100.0)
    
    # Constraint 3: Unique clicks from young visitors.
    # sum((YoungClicks[i]/100 * UniqueClicks[i]/100) * x_i) >= GoalUniqueYoung
    constraint_unique_young = solver.Constraint(GoalUniqueYoung, solver.infinity())
    for i in range(A):
        constraint_unique_young.SetCoefficient(x[i], (YoungClicks[i] * UniqueClicks[i]) / 10000.0)
    
    # Constraint 4: Unique clicks from old visitors.
    # sum((OldClicks[i]/100 * UniqueClicks[i]/100) * x_i) >= GoalUniqueOld
    constraint_unique_old = solver.Constraint(GoalUniqueOld, solver.infinity())
    for i in range(A):
        constraint_unique_old.SetCoefficient(x[i], (OldClicks[i] * UniqueClicks[i]) / 10000.0)
    
    # (Optional) If a strictly positive purchase is required in each ad type,
    # set a lower bound > 0 (e.g. epsilon = 1e-3 or a minimum purchase requirement).
    # Uncomment the following lines to enforce a minimum purchase.
    # epsilon = 1e-3
    # for i in range(A):
    #     x[i].SetLb(epsilon)
    
    # Solve the problem.
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solution found:')
        for i in range(A):
            print(f'Ad type {i+1}: {x[i].solution_value()} clicks')
        print(f'Total minimized cost: {objective.Value()}')
    elif status == pywraplp.Solver.FEASIBLE:
        print('A feasible solution was found, but it may not be optimal.')
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    main()