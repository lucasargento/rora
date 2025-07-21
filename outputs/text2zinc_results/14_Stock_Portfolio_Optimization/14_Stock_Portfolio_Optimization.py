# Mathematical Formulation:
'''\[
\begin{array}{rcl}
\textbf{Parameters:} & & \\
& N \in \mathbb{N} & \text{(number of different stocks)} \\
& Bought_i \ge 0,\quad BuyPrice_i > 0,\quad CurrentPrice_i > 0,\quad FuturePrice_i > 0,\quad i=1,\ldots,N, & \\
& TransactionRate \ge 0,\quad TaxRate \ge 0,\quad K \ge 0, & \\
& \Delta_i \;:=\; \max\{0,\; (CurrentPrice_i - BuyPrice_i)\},\quad i=1,\ldots,N. & \\[1ex]

\textbf{Decision Variables:} & & \\
& x_i \in [0,\,Bought_i],\quad i=1,\ldots,N, & \text{(shares of stock $i$ to sell; fractional amounts allowed)} \\[1ex]

\textbf{Auxiliary Expression:} & & \\
& R_i \;:=\; x_i \left[ CurrentPrice_i \left(1 - \frac{TransactionRate}{100}\right) - \frac{TaxRate}{100}\,\Delta_i \right],\quad i=1,\ldots,N, & \text{(net cash received from selling stock $i$)} \\[1ex]

\textbf{Objective Function:} & & \\
\text{maximize} \quad Z \;=\; & \displaystyle \sum_{i=1}^N \Big[(Bought_i - x_i)\, FuturePrice_i\Big] \;+\; \sum_{i=1}^N R_i. & \\[1ex]

\textbf{Subject to:} & & \\
& \displaystyle \sum_{i=1}^N R_i \;\ge\; K, & \text{(the net sale proceeds must raise at least \$K)} \\[1ex]
& 0 \;\le\; x_i \;\le\; Bought_i,\quad \forall\, i=1,\ldots,N. &
\end{array}
\]

Below is a brief explanation of each part:

1. Decision Variables:  
 • x₍ᵢ₎ is the (possibly fractional) number of shares of asset i that the investor elects to sell. Its domain is from 0 to the number initially held, Bought₍ᵢ₎.

2. Objective Function (Maximization):  
 • The first term, ∑₍ᵢ₌₁₎ᴺ (Bought₍ᵢ₎ – x₍ᵢ₎) FuturePrice₍ᵢ₎, represents the future value of the shares that remain in the portfolio.  
 • The second term, ∑₍ᵢ₌₁₎ᴺ R₍ᵢ₎, represents the net cash received from selling shares (i.e. after paying transaction costs and, for stocks with a capital gain, the capital gains tax).  
 • Thus the objective is to maximize the total expected portfolio value one year from now (the sum of the future value of unsold stocks and the cash generated from sales).

3. Constraints:  
 • The sales must raise at least K dollars after transaction costs and taxes.  
 • Additionally, the amount sold of each stock cannot exceed the number originally held.

This formulation is self-contained, reflects the full details of the problem without simplification, and is bounded and feasible under reasonable parameter values.'''

# Generated Code:
from ortools.linear_solver import pywraplp

def main():
    # Problem data
    N = 3
    Bought = [100, 150, 80]
    BuyPrice = [50, 40, 30]
    CurrentPrice = [60, 35, 32]
    FuturePrice = [65, 44, 34]
    TransactionRate = 1.0  # percentage
    TaxRate = 15.0         # percentage
    K = 5000

    # Precompute delta and net price coefficient for each asset
    delta = [max(0, CurrentPrice[i] - BuyPrice[i]) for i in range(N)]
    # Coefficient for x_i in the sale proceeds R_i:
    # R_i = x_i * [CurrentPrice_i * (1 - TransactionRate/100) - (TaxRate/100) * delta_i]
    net_coeff = [CurrentPrice[i]*(1 - TransactionRate/100) - (TaxRate/100)*delta[i] for i in range(N)]

    # Create solver using GLOP (for linear programming)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Solver not created.")
        return

    # Decision variables: x[i] = number of shares to sell for asset i, continuous between 0 and Bought[i]
    x = [solver.NumVar(0, Bought[i], f'x[{i}]') for i in range(N)]

    # Auxiliary expression: R[i] = net proceeds for asset i from sale
    # Since it's linear in x[i] with constant coefficient, we treat it as an expression.
    R = [solver.Sum([x[i] * net_coeff[i]]) for i in range(N)]

    # Constraint: total net proceeds must be at least K
    total_R = solver.Sum(R)
    solver.Add(total_R >= K)

    # Objective: maximize portfolio expected value next year
    # Future value of unsold shares: (Bought[i] - x[i]) * FuturePrice[i]
    objective_expr = solver.Sum([(Bought[i] - x[i]) * FuturePrice[i] for i in range(N)]) + total_R
    solver.Maximize(objective_expr)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found:")
        for i in range(N):
            print(f"  Sell {x[i].solution_value():.4f} shares of stock {i+1}")
        print(f"Optimal portfolio value next year: {solver.Objective().Value():.4f}")
        print(f"Total net cash raised: {total_R.solution_value():.4f}")
    elif status == pywraplp.Solver.FEASIBLE:
        print("A feasible solution was found, but it may not be optimal.")
    else:
        print("The problem does not have an optimal solution.")

if __name__ == '__main__':
    main()