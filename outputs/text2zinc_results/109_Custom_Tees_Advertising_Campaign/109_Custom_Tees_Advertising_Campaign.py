# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Parameters:} \quad & a \in \{1,2,\dots,A\} \quad \text{with } A=3.\\[1mm]
\textbf{Parameters:}\\[0.5mm]
& \text{Budget} \in \mathbb{R}_+ \quad (\text{total advertising budget}),\\[0.5mm]
& \text{Costs}_a \in \mathbb{R}_+ \quad (\text{cost per 1000 clicks for ad } a),\\[0.5mm]
& \text{MaxClicks}_a \in \mathbb{R}_+ \quad (\text{upper limit on clicks from ad } a),\\[0.5mm]
& \text{YoungPerc}_a \in \mathbb{R}_+ \quad (\text{estimated percentage of clicks from visitors aged 18--25 for ad } a),\\[0.5mm]
& \text{OldPerc}_a \in \mathbb{R}_+ \quad (\text{estimated percentage of clicks from visitors older than 25 for ad } a),\\[0.5mm]
& \text{UniquePerc}_a \in \mathbb{R}_+ \quad (\text{estimated percentage of unique clicks for ad } a, \text{ same for both age groups}),\\[0.5mm]
& \text{GoalYoung} \in \mathbb{R}_+ \quad (\text{minimum required clicks from young visitors}),\\[0.5mm]
& \text{GoalOld} \in \mathbb{R}_+ \quad (\text{minimum required clicks from older visitors}),\\[0.5mm]
& \text{GoalUniqueYoung} \in \mathbb{R}_+ \quad (\text{minimum required unique clicks from young visitors}),\\[0.5mm]
& \text{GoalUniqueOld} \in \mathbb{R}_+ \quad (\text{minimum required unique clicks from older visitors}).\\[3mm]
\textbf{Decision Variables:}\\[0.5mm]
& x_a \ge 0,\quad \forall a \quad \text{(number of clicks purchased from ad type }a\text{)}.
\end{align*}

\noindent
\textbf{Model Formulation:}
\begin{align*}
\textbf{Objective:} \quad & \max \quad Z = \sum_{a=1}^{A} \frac{\text{UniquePerc}_a}{100}\, x_a
&&\text{(maximize total unique clicks)}\\[1mm]
\textbf{Subject to:}\\[0.5mm]
\text{(1) Budget Constraint:} \quad & \sum_{a=1}^{A} \frac{\text{Costs}_a}{1000}\, x_a \le \text{Budget}, \\[2mm]
\text{(2) Maximum Clicks per Ad:} \quad & x_a \le \text{MaxClicks}_a, \quad \forall a, \\[2mm]
\text{(3) Young Audience Clicks:} \quad & \sum_{a=1}^{A} \frac{\text{YoungPerc}_a}{100}\, x_a \ge \text{GoalYoung}, \\[2mm]
\text{(4) Old Audience Clicks:} \quad & \sum_{a=1}^{A} \frac{\text{OldPerc}_a}{100}\, x_a \ge \text{GoalOld}, \\[2mm]
\text{(5) Unique Young Audience Clicks:} \quad & \sum_{a=1}^{A} \frac{\text{UniquePerc}_a \cdot \text{YoungPerc}_a}{100 \cdot 100}\, x_a \ge \text{GoalUniqueYoung}, \\[2mm]
\text{(6) Unique Old Audience Clicks:} \quad & \sum_{a=1}^{A} \frac{\text{UniquePerc}_a \cdot \text{OldPerc}_a}{100 \cdot 100}\, x_a \ge \text{GoalUniqueOld}, \\[2mm]
\text{(7) Nonnegativity:} \quad & x_a \ge 0, \quad \forall a.
\end{align*}

\noindent
\textbf{Explanation:}

1. \emph{Decision Variables:}  
   The variable \( x_a \) denotes the number of clicks to purchase from advertisement type \( a \). It is nonnegative and, typically, might be required to be integer though here we model it as a continuous variable (its integrality can be enforced as needed).

2. \emph{Objective Function:}  
   We maximize
   \[
   Z = \sum_{a=1}^{A} \frac{\text{UniquePerc}_a}{100}\, x_a,
   \]
   which represents the total number of unique clicks obtained across all ad types, given that each ad type yields a unique click fraction of \(\text{UniquePerc}_a/100\) for every click purchased.

3. \emph{Constraints:}
   \begin{itemize}
      \item \textbf{Budget Constraint (1):} The total spending for clicks, where each click from ad \(a\) costs \(\text{Costs}_a/1000\) (cost per click since the cost is given per 1000 clicks), must not exceed the available \(\text{Budget}\).
      \item \textbf{Maximum Clicks (2):} For each ad type, the number of clicks purchased cannot exceed the maximum allowable clicks.
      \item \textbf{Age-Specific Click Goals (3) \& (4):} The total clicks generated from young visitors (using the percentage \(\text{YoungPerc}_a/100\)) and from older visitors (using \(\text{OldPerc}_a/100\)) must respectively meet or exceed the set goals \(\text{GoalYoung}\) and \(\text{GoalOld}\).
      \item \textbf{Unique Click Goals (5) \& (6):} Given that the unique click percentage applies uniformly to both age groups, the unique clicks among the young (resp. older) visitors from ad \(a\) are modeled as  
      \[
      \frac{\text{UniquePerc}_a}{100} \times \frac{\text{YoungPerc}_a}{100} \, x_a \quad \text{and} \quad \frac{\text{UniquePerc}_a}{100} \times \frac{\text{OldPerc}_a}{100} \, x_a,
      \]
      respectively. The totals over all ads must meet the goals \(\text{GoalUniqueYoung}\) and \(\text{GoalUniqueOld}\).
   \end{itemize}

This complete model reflects the decision, objective, and constraints as given in the original description without any simplification, ensuring feasibility and boundedness for the optimization problem.
'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not available.")
        return

    # Data
    A = 3
    Budget = 105000
    Costs = [75, 100, 120]        # cost per 1000 clicks
    MaxClicks = [600, 300, 300]
    YoungPerc = [40, 30, 70]       # percentage for young visitors
    OldPerc = [60, 70, 30]         # percentage for old visitors
    UniquePerc = [40, 75, 90]      # percentage of unique clicks

    GoalYoung = 500
    GoalOld = 600
    GoalUniqueYoung = 250
    GoalUniqueOld = 300

    # Decision variables: number of clicks to purchase for each advertisement type.
    x = []
    for a in range(A):
        # x[a] can vary continuously between 0 and MaxClicks[a]
        x_var = solver.NumVar(0, MaxClicks[a], f'x_{a}')
        x.append(x_var)

    # Objective: maximize total unique clicks = sum(UniquePerc[a]/100 * x[a])
    objective = solver.Objective()
    for a in range(A):
        objective.SetCoefficient(x[a], UniquePerc[a] / 100)
    objective.SetMaximization()

    # Constraint 1: Budget Constraint: sum(Costs[a]/1000 * x[a]) <= Budget
    budget_constraint = solver.Constraint(-solver.infinity(), Budget)
    for a in range(A):
        budget_constraint.SetCoefficient(x[a], Costs[a] / 1000)

    # Constraint 3: Young Audience Clicks: sum(YoungPerc[a]/100 * x[a]) >= GoalYoung
    young_clicks_constraint = solver.Constraint(GoalYoung, solver.infinity())
    for a in range(A):
        young_clicks_constraint.SetCoefficient(x[a], YoungPerc[a] / 100)

    # Constraint 4: Old Audience Clicks: sum(OldPerc[a]/100 * x[a]) >= GoalOld
    old_clicks_constraint = solver.Constraint(GoalOld, solver.infinity())
    for a in range(A):
        old_clicks_constraint.SetCoefficient(x[a], OldPerc[a] / 100)

    # Constraint 5: Unique Young Audience Clicks:
    # sum((UniquePerc[a] * YoungPerc[a]) / (100*100) * x[a]) >= GoalUniqueYoung
    unique_young_constraint = solver.Constraint(GoalUniqueYoung, solver.infinity())
    for a in range(A):
        factor = (UniquePerc[a] * YoungPerc[a]) / 10000
        unique_young_constraint.SetCoefficient(x[a], factor)

    # Constraint 6: Unique Old Audience Clicks:
    # sum((UniquePerc[a] * OldPerc[a]) / (100*100) * x[a]) >= GoalUniqueOld
    unique_old_constraint = solver.Constraint(GoalUniqueOld, solver.infinity())
    for a in range(A):
        factor = (UniquePerc[a] * OldPerc[a]) / 10000
        unique_old_constraint.SetCoefficient(x[a], factor)

    # Solve the problem.
    status = solver.Solve()

    # Check the result status.
    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        print(f"Objective value (Total unique clicks): {objective.Value()}")
        for a in range(A):
            print(f"Clicks purchased from ad {a+1}: {x[a].solution_value()}")
        print(f"Total cost: {sum(Costs[a]/1000 * x[a].solution_value() for a in range(A))}")
        print(f"Young audience clicks: {sum(YoungPerc[a]/100 * x[a].solution_value() for a in range(A))}")
        print(f"Old audience clicks: {sum(OldPerc[a]/100 * x[a].solution_value() for a in range(A))}")
        print(f"Unique young clicks: {sum((UniquePerc[a]*YoungPerc[a])/(10000) * x[a].solution_value() for a in range(A))}")
        print(f"Unique old clicks: {sum((UniquePerc[a]*OldPerc[a])/(10000) * x[a].solution_value() for a in range(A))}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()