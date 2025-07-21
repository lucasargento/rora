# Mathematical Formulation:
'''\begin{align*}
\intertext{\textbf{Parameters:}}
K & = 3,\\[1mm]
\text{SteelQuantity} & = 1000 \quad \text{(tons)},\\[0.5mm]
\text{ManganesePercent} & = 0.45 \quad \text{(required minimum fraction in steel)},\\[0.5mm]
\text{SiliconMinPercent} & = 3.25 \quad \text{(required minimum silicon fraction in steel)},\\[0.5mm]
\text{SiliconMaxPercent} & = 5.0 \quad \text{(allowed maximum silicon fraction in steel)},\\[0.5mm]
\text{SiliconContent}_k &\quad \text{for } k=1,\ldots,K \quad = [4.0,\;1.0,\;0.6]\quad \text{(percent per ton)},\\[0.5mm]
\text{ManganeseContent}_k &\quad \text{for } k=1,\ldots,K \quad = [0.45,\;0.5,\;0.4]\quad \text{(percent per ton)},\\[0.5mm]
\text{ManganesePrice} & = 8.0 \quad \text{(price per ton of pure manganese)},\\[0.5mm]
\text{MaterialCost}_k &\quad \text{for } k=1,\ldots,K \quad = [21,\;25,\;15]\quad \text{(price per ton of mineral }k\text{)},\\[0.5mm]
\text{SellingPrice} & = 0.45 \quad \text{(price per ton of steel sold)},\\[0.5mm]
\text{MeltingPrice} & = 0.005 \quad \text{(cost per ton to melt steel)}.
\intertext{\textbf{Decision Variables:}}
x_k &\ge 0,\quad k=1,2,\ldots,K,\quad\text{tons of mineral type }k\text{ used in production},\\[0.5mm]
y &\ge 0,\quad\text{tons of manganese added directly (as pure manganese)}.
\intertext{\textbf{Model:}}
\text{Maximize} \quad Z &= \text{SellingPrice}\cdot \text{SteelQuantity} - \Bigg[
\sum_{k=1}^{K} \text{MaterialCost}_k \, x_k + \text{ManganesePrice}\, y + \text{MeltingPrice}\cdot \text{SteelQuantity}
\Bigg]
\\[1mm]
\text{Subject to} \quad
\underbrace{\sum_{k=1}^{K} x_k + y = \text{SteelQuantity}}_{\text{Total Mass Balance}}
\\[1mm]
\underbrace{\frac{\sum_{k=1}^{K} \text{ManganeseContent}_k\, x_k + y}{\text{SteelQuantity}} \ge \text{ManganesePercent}}_{\substack{\text{Manganese composition:} \\ \text{the fraction of Mn must be at least }0.45}}
\\[1mm]
\underbrace{\frac{\sum_{k=1}^{K} \text{SiliconContent}_k\, x_k}{\text{SteelQuantity}} \ge \text{SiliconMinPercent}}_{\substack{\text{Silicon composition (lower bound):} \\ \text{at least }3.25\% \text{ Si in steel}}}
\\[1mm]
\underbrace{\frac{\sum_{k=1}^{K} \text{SiliconContent}_k\, x_k}{\text{SteelQuantity}} \le \text{SiliconMaxPercent}}_{\substack{\text{Silicon composition (upper bound):} \\ \text{at most }5.0\% \text{ Si in steel}}}
\end{align*}

\medskip

\textbf{Explanation:}

1. \textit{Decision Variables:}  
 • For each mineral type k, the variable $x_k$ (with $x_k \ge 0$) represents the tonnage of mineral k purchased and used in the steel production.  
 • The variable $y$ (with $y \ge 0$) represents the tonnage of direct manganese addition.  

2. \textit{Objective Function:}  
 We maximize the profit $Z$, which is calculated as the revenue from selling the total produced steel minus the sum of costs (purchasing minerals, purchasing manganese, and the melting cost per ton of steel). The production quantity is fixed to \text{SteelQuantity} (1000 tons).

3. \textit{Constraints:}  
 • \textbf{Mass Balance:} The sum of all mineral inputs and the directly added manganese must equal the total steel production.  
 • \textbf{Manganese Composition:} The overall manganese content (from both minerals and direct addition) must achieve at least the required percentage in the steel.  
 • \textbf{Silicon Composition:} The silicon content provided solely by the minerals must lie within the required lower and upper bounds. 

This model is fully self-contained and faithfully represents the original manufacturing and production problem, ensuring that non-trivial mixes (i.e., not relying exclusively on one mineral source) can be deduced from the optimization process while keeping the problem both feasible and bounded.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Create the solver using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Solver not created.")
        return

    # Problem Data
    K = 3
    SteelQuantity = 1000.0
    ManganesePercent = 0.45
    SiliconMinPercent = 3.25
    SiliconMaxPercent = 5.0
    SiliconContent = [4.0, 1.0, 0.6]
    ManganeseContent = [0.45, 0.5, 0.4]
    ManganesePrice = 8.0
    MaterialCost = [21, 25, 15]
    SellingPrice = 0.45
    MeltingPrice = 0.005

    # Decision Variables
    # x[k]: tons of mineral type k
    x = [solver.NumVar(0.0, solver.infinity(), f'x_{k}') for k in range(K)]
    # y: tons of manganese added directly
    y = solver.NumVar(0.0, solver.infinity(), 'y')

    # Constraints

    # Mass balance: total inputs equals steel quantity produced
    solver.Add(solver.Sum(x) + y == SteelQuantity)

    # Manganese composition: overall Mn content should be at least required fraction
    manganese_from_minerals = solver.Sum(ManganeseContent[k] * x[k] for k in range(K))
    solver.Add(manganese_from_minerals + y >= ManganesePercent * SteelQuantity)

    # Silicon composition constraints (only from minerals)
    silicon_from_minerals = solver.Sum(SiliconContent[k] * x[k] for k in range(K))
    solver.Add(silicon_from_minerals >= SiliconMinPercent * SteelQuantity)
    solver.Add(silicon_from_minerals <= SiliconMaxPercent * SteelQuantity)

    # Objective: maximize profit = selling revenue - (materials cost + manganese cost + melting cost)
    revenue = SellingPrice * SteelQuantity
    materials_cost = solver.Sum(MaterialCost[k] * x[k] for k in range(K))
    manganese_cost = ManganesePrice * y
    melting_cost = MeltingPrice * SteelQuantity
    profit = revenue - (materials_cost + manganese_cost + melting_cost)
    solver.Maximize(profit)

    # Solve the model
    status = solver.Solve()

    # Check the result and print the solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Solution Found:")
        print("Optimal Profit:", solver.Objective().Value())
        for k in range(K):
            print(f"x_{k} (tons of mineral {k+1}):", x[k].solution_value())
        print("y (tons of direct manganese):", y.solution_value())
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()