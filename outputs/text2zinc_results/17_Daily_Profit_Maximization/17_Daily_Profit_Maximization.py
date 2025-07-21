# Mathematical Formulation:
'''Below is one fully‐detailed mathematical formulation of the problem. In our formulation we assume that x_i (for i = 1, …, N) represents the (non‐negative, and if desired integer) number of units of product i produced, and O is the non‐negative number of overtime assembly hours actually used. In addition, we introduce a binary variable y∈{0,1} that “activates” the supplier discount on raw materials if the daily raw material cost reaches the threshold. (A sufficiently large constant M is used in the linking constraints for the discount condition.) Finally, to avoid solutions that are “trivial” in the sense of producing only one product or nothing at all, we add a non‐trivial production constraint.

The complete model is given below.

\[
\begin{align*}
\textbf{Decision Variables:} \quad & x_i \ge 0,\quad i=1,\ldots,N, \quad (\text{units of product } i\text{ produced})\\[1mm]
& O \ge 0,\quad (\text{overtime assembly hours used})\\[1mm]
& y \in \{0,1\},\quad (\text{discount indicator: }y=1 \text{ if raw material cost } \ge \text{DiscountThreshold})\\[3mm]
\textbf{Parameters:} \quad &\text{For } i=1,\ldots,N:\\[1mm]
& \quad AssemblyHour_i \, (\text{assembly hours required per unit of product } i)\\[1mm]
& \quad TestingHour_i \, (\text{testing hours required per unit of product } i)\\[1mm]
& \quad MaterialCost_i \, (\$ \text{ raw material cost per unit of product } i)\\[1mm]
& \quad Price_i \, (\$ \text{ selling price per unit of product } i)\\[1mm]
& \text{Other Parameters:}\\[1mm]
& \quad MaxAssembly \, (\text{regular assembly hours available per day})\\[1mm]
& \quad MaxTesting \, (\text{testing hours available per day})\\[1mm]
& \quad MaxOvertimeAssembly \, (\text{maximum overtime assembly hours available})\\[1mm]
& \quad OvertimeAssemblyCost \, (\text{cost per overtime assembly hour})\\[1mm]
& \quad MaterialDiscount \, (\text{percentage discount, e.g. }10\text{ for }10\%\text{ discount})\\[1mm]
& \quad DiscountThreshold \, (\$ \text{ threshold for obtaining the discount})\\[1mm]
& \quad M \, (\text{sufficiently large positive constant})\\[3mm]
\textbf{Objective Function:} \quad &\text{Maximize daily profit } Z, \text{ defined as total revenue minus total cost, that is:}\\[1mm]
\displaystyle \max \quad Z =\; & \sum_{i=1}^N Price_i \, x_i \;-\; \Bigl\{ \left[1-\frac{MaterialDiscount}{100}\,y\right]\,\sum_{i=1}^N MaterialCost_i \, x_i\Bigr\} \;-\; OvertimeAssemblyCost\, O \\[3mm]
\textbf{Subject to:} \quad &&\\[1mm]
\textbf{(1) Assembly hours constraint:} \quad & \sum_{i=1}^N AssemblyHour_i\, x_i \le MaxAssembly \,+\, O, \quad &\text{(total assembly hours needed can be met by regular and overtime assembly)}\\[1mm]
\textbf{(2) Overtime limit:} \quad & O \le MaxOvertimeAssembly, \quad &\text{(overtime hours cannot exceed capacity)}\\[1mm]
\textbf{(3) Testing hours constraint:} \quad & \sum_{i=1}^N TestingHour_i\, x_i \le MaxTesting, \quad &\text{(total testing hours requirement is bounded)}\\[1mm]
\textbf{(4) Discount activation constraints:}\\[1mm]
& \sum_{i=1}^N MaterialCost_i\, x_i \ge DiscountThreshold\;y, \quad &\text{(if }y=1,\text{ raw material cost must meet threshold)}\\[1mm]
& \sum_{i=1}^N MaterialCost_i\, x_i \le DiscountThreshold \;+\; M\,(1-y), \quad &\text{(if }y=0,\text{ total cost is forced to be below or near the threshold)}\\[1mm]
\textbf{(5) Non‐trivial production constraint:} \quad & \sum_{i=1}^N x_i \ge 1, \quad &\text{(at least one unit of some product is produced)}
\end{align*}
\]

A few notes on the formulation:

• The material cost in the objective is charged at full price if y = 0 and at a discounted price (i.e. multiplied by 1 – MaterialDiscount/100) when y = 1.  
• The binary discount indicator y is linked to the raw material spending through the Big‑M constraints.  
• All constraints together ensure feasibility and boundedness of the problem.

This complete model accurately represents all aspects of the problem and is ready to be implemented in an OR‑tools model by another solver.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create solver using CBC MIP solver.
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("CBC solver unavailable.")
        return

    # -------------------------------
    # Data
    # -------------------------------
    N = 2
    AssemblyHour = [0.25, 0.3333]
    TestingHour = [0.125, 0.3333]
    MaterialCost = [1.2, 0.9]
    MaxAssembly = 10
    MaxTesting = 70
    Price = [9, 8]
    MaxOvertimeAssembly = 50
    OvertimeAssemblyCost = 5
    MaterialDiscount = 10  # percentage, e.g. 10 for 10%
    DiscountThreshold = 300

    # Big-M parameters (sufficiently large)
    M_discount = 1e6  # For discount activation constraints.
    M_big = 1e6       # For linearizing product y*T

    # -------------------------------
    # Decision Variables
    # -------------------------------
    # x[i]: number of units of product i produced (integer, >=0)
    x = [solver.IntVar(0, solver.infinity(), f'x_{i}') for i in range(N)]
    # O: overtime assembly hours used (continuous, >=0)
    O = solver.NumVar(0, MaxOvertimeAssembly, 'O')
    # y: binary variable to indicate if discount is activated.
    y = solver.BoolVar('y')
    
    # T: total raw material cost (continuous)
    T = solver.NumVar(0, solver.infinity(), 'T')
    # W: auxiliary variable to linearize the product y * T
    W = solver.NumVar(0, solver.infinity(), 'W')

    # -------------------------------
    # Constraints
    # -------------------------------
    # (1) Assembly hours constraint:
    # sum(AssemblyHour[i]* x[i]) <= MaxAssembly + O
    solver.Add(sum(AssemblyHour[i] * x[i] for i in range(N)) <= MaxAssembly + O)

    # (2) Overtime limit is already enforced by variable upper bound on O.
    # (3) Testing hours constraint:
    solver.Add(sum(TestingHour[i] * x[i] for i in range(N)) <= MaxTesting)

    # (4) Discount activation constraints:
    # First, define T = sum(MaterialCost[i]*x[i])
    solver.Add(T == sum(MaterialCost[i] * x[i] for i in range(N)))
    # Constraint linking discount activation:
    solver.Add(T >= DiscountThreshold * y)
    solver.Add(T <= DiscountThreshold + M_discount * (1 - y))

    # (4b) Linearization constraints for W = y * T:
    solver.Add(W <= T)
    solver.Add(W <= M_big * y)
    solver.Add(W >= T - M_big * (1 - y))
    solver.Add(W >= 0)

    # (5) Non-trivial production constraint: at least one unit is produced.
    solver.Add(sum(x[i] for i in range(N)) >= 1)

    # -------------------------------
    # Objective Function
    # -------------------------------
    # Profit = Total Revenue - (Discounted Raw Material Cost) - Overtime Cost
    # Discounted raw material cost = (1 - MaterialDiscount/100) * T when y=1; full T when y=0.
    # This is expressed as: T - (MaterialDiscount/100)* (y * T), which is T - (MaterialDiscount/100)*W.
    revenue = sum(Price[i] * x[i] for i in range(N))
    cost_material = T - (MaterialDiscount / 100.0) * W
    cost_overtime = OvertimeAssemblyCost * O
    profit = revenue - cost_material - cost_overtime

    solver.Maximize(profit)

    # -------------------------------
    # Solve
    # -------------------------------
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Solution:")
        for i in range(N):
            print(f"Product {i}: {x[i].solution_value()} units")
        print(f"Overtime assembly hours used (O): {O.solution_value()}")
        print(f"Discount activated (y): {y.solution_value()}")
        print(f"Total raw material cost (T): {T.solution_value()}")
        print(f"Objective value (Profit): {solver.Objective().Value()}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()