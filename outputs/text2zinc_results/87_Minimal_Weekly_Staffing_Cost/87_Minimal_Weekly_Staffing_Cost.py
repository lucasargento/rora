# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices:} \quad & i,j \in \{0,1,\dots,n-1\}. \\[1mm]
\textbf{Parameters:} \quad
& n = 7,\\[0.5mm]
& \text{demand}_j,\ j=0,\ldots,n-1,\ \text{with } \text{demand} = [5,7,7,10,16,18,12],\\[0.5mm]
& c_F = \text{full\_time\_pay} = 100,\\[0.5mm]
& c_P = \text{part\_time\_pay} = 150,\\[0.5mm]
& L_F = \text{full\_time\_shift} = 5,\\[0.5mm]
& L_P = \text{part\_time\_shift} = 2. \\[2mm]
\textbf{Decision Variables:} \quad 
& x_i \in \mathbb{Z}_{\ge 0} \quad \text{for } i=0,\ldots,n-1, \quad \text{number of full time workers starting on day } i, \\[0.5mm]
& y_i \in \mathbb{Z}_{\ge 0} \quad \text{for } i=0,\ldots,n-1, \quad \text{number of part time workers starting on day } i. \\[2mm]
\textbf{Objective Function:} \quad &\text{Minimize the total staffing cost over the cycle} \\[0.5mm]
\min \; Z &= \sum_{i=0}^{n-1} \Big( c_F \cdot L_F \cdot x_i + c_P \cdot L_P \cdot y_i \Big). \\[2mm]
\textbf{Coverage Constraints:} \quad & \text{For each day } j, \text{the total number of workers covering day } j \text{ must meet the demand.} \\[0.5mm]
& \sum_{i \,:\, j \in C_F(i)} x_i + \sum_{i \,:\, j \in C_P(i)} y_i \ge \text{demand}_j,\quad \forall \, j=0,\ldots,n-1, \\[2mm]
\text{where } \quad & C_F(i)=\{(i+k) \bmod n : k=0,1,\dots, L_F-1\},\\[0.5mm]
& \quad\quad\; C_P(i)=\{(i+k) \bmod n : k=0,1,\dots, L_P-1\}. \\[2mm]
\textbf{Nonnegativity and Integrality:} \quad & x_i,\, y_i \in \mathbb{Z}_{\ge0},\quad \forall\, i=0,\ldots,n-1.
\end{align*}

\bigskip

\textbf{Explanation:}

1. Decision variables x_i and y_i represent the number of full time and part time employees whose shift begins on day i of the recurring period. They are nonnegative integers.

2. The objective is to minimize the total cost of staffing, where each full time worker costs c_F per day and works L_F consecutive days (hence a total cost of c_F \cdot L_F per worker), and similarly for each part time worker.

3. For every day j in the cycle, the coverage constraint ensures that the sum of contributions from all workers (full time and part time) whose shifts cover day j is at least the required staffing demand for that day. The sets C_F(i) and C_P(i) capture the days covered by a worker that started on day i for full time and part time, respectively. The modulo operation ensures the schedule is cyclic over the n-day period.

This complete formulation accurately represents the workforce scheduling problem as described.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem data
    n = 7
    demand = [5, 7, 7, 10, 16, 18, 12]
    full_time_pay = 100
    part_time_pay = 150
    full_time_shift = 5
    part_time_shift = 2

    # Create model
    model = cp_model.CpModel()

    # Decision variables: number of workers starting on day i
    x = [model.NewIntVar(0, 1000, f'full_time_start_{i}') for i in range(n)]
    y = [model.NewIntVar(0, 1000, f'part_time_start_{i}') for i in range(n)]

    # Coverage constraints: for each day j, sum of workers covering day j must meet demand[j]
    for j in range(n):
        # Sum full time workers covering day j
        full_time_coverage = []
        for i in range(n):
            # Worker starting on day i covers day j if (j-i) mod n is in 0..full_time_shift-1
            if ((j - i) % n) < full_time_shift:
                full_time_coverage.append(x[i])
        # Sum part time workers covering day j
        part_time_coverage = []
        for i in range(n):
            if ((j - i) % n) < part_time_shift:
                part_time_coverage.append(y[i])
        model.Add(sum(full_time_coverage) + sum(part_time_coverage) >= demand[j])

    # Objective: minimize total staffing cost
    # Cost = full_time_pay * full_time_shift * x[i] + part_time_pay * part_time_shift * y[i]
    obj_terms = []
    for i in range(n):
        obj_terms.append(full_time_pay * full_time_shift * x[i])
        obj_terms.append(part_time_pay * part_time_shift * y[i])
    model.Minimize(sum(obj_terms))

    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal solution found:')
        print('Objective value (total cost):', solver.ObjectiveValue())
        for i in range(n):
            print(f'Day {i}: full time workers starting =', solver.Value(x[i]), 
                  f', part time workers starting =', solver.Value(y[i]))
    else:
        print('No feasible solution found.')


if __name__ == '__main__':
    main()