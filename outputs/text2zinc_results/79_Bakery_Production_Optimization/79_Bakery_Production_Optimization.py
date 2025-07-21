# Mathematical Formulation:
'''\begin{align*}
\textbf{Decision Variables:} \quad
& A \in \mathbb{Z}_{>0} \quad \text{(number of almond croissants to produce)}\\[1mm]
& P \in \mathbb{Z}_{>0} \quad \text{(number of pistachio croissants to produce)}\\[2mm]
\textbf{Parameters:} \quad
& b_A = 5 \quad \text{(butter per almond croissant)}\\[1mm]
& b_P = 3 \quad \text{(butter per pistachio croissant)}\\[1mm]
& f_A = 8 \quad \text{(flour per almond croissant)}\\[1mm]
& f_P = 6 \quad \text{(flour per pistachio croissant)}\\[1mm]
& T_B = 600 \quad \text{(total available butter)}\\[1mm]
& T_F = 800 \quad \text{(total available flour)}\\[1mm]
& t_A = 12 \quad \text{(baking time per almond croissant)}\\[1mm]
& t_P = 10 \quad \text{(baking time per pistachio croissant)}\\[1mm]
& m = 3 \quad \text{(minimum almond-to-pistachio production ratio)}
\\[2mm]
\textbf{Objective Function:} \quad
& \min \; Z = t_A A + t_P P = 12\,A + 10\,P\\[2mm]
\textbf{Constraints:}\\[1mm]
& \text{(1) Butter Constraint:} \quad b_A A + b_P P \le T_B, \quad \Longrightarrow \quad 5\,A + 3\,P \le 600,\\[2mm]
& \text{(2) Flour Constraint:} \quad f_A A + f_P P \le T_F, \quad \Longrightarrow \quad 8\,A + 6\,P \le 800,\\[2mm]
& \text{(3) Production Ratio:} \quad A \ge m\,P, \quad \Longrightarrow \quad A \ge 3\,P,\\[2mm]
& \text{(4) Non-trivial Production:} \quad A \ge 1,\quad P \ge 1,\\[2mm]
& \text{(5) Integrality and Non-negativity:} \quad A,P \in \mathbb{Z}^{+}.
\end{align*}'''

# Generated Code:
from ortools.sat.python import cp_model

def main():
    # Create the CP-SAT model.
    model = cp_model.CpModel()

    # Parameters
    butter_per_almond = 5
    butter_per_pistachio = 3
    flour_per_almond = 8
    flour_per_pistachio = 6
    total_butter = 600
    total_flour = 800
    time_per_almond = 12
    time_per_pistachio = 10
    min_almond_ratio = 3

    # Decision variables: A and P are produced numbers for almond and pistachio croissants.
    # Lower bound is 1 (at least 1 is produced).
    A = model.NewIntVar(1, total_butter // butter_per_almond, 'AlmondCroissants')
    P = model.NewIntVar(1, total_butter // butter_per_pistachio, 'PistachioCroissants')

    # Constraints
    # (1) Butter constraint: 5A + 3P <= 600
    model.Add(butter_per_almond * A + butter_per_pistachio * P <= total_butter)

    # (2) Flour constraint: 8A + 6P <= 800
    model.Add(flour_per_almond * A + flour_per_pistachio * P <= total_flour)

    # (3) Production ratio constraint: A >= 3P
    model.Add(A >= min_almond_ratio * P)

    # Objective: minimize baking time 12A + 10P
    model.Minimize(time_per_almond * A + time_per_pistachio * P)

    # Create solver and solve the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Optimal solution found:")
        print(f"Almond Croissants : {solver.Value(A)}")
        print(f"Pistachio Croissants : {solver.Value(P)}")
        print(f"Total Baking Time : {solver.Value(time_per_almond * A + time_per_pistachio * P)}")
    else:
        print("No feasible solution found.")

if __name__ == '__main__':
    main()