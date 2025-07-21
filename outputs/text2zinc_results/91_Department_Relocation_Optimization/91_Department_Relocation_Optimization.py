# Mathematical Formulation:
'''\[
\begin{array}{rcll}
\textbf{Sets and Parameters:}&&&\\[1mm]
\mathcal{K} &=& \{1,2,\dots, K\} & \text{(departments)}\\[1mm]
\mathcal{L} &=& \{1,2,\dots, L\} & \text{(cities, including London)}\\[1mm]
\text{Benefit}_{k\ell} &\in& \mathbb{R}  & \forall k\in \mathcal{K},\, \ell\in \mathcal{L} \quad\text{(benefit, in thousands of pounds, if department }k\text{ is located in city }\ell\text{)}\\[1mm]
\text{Communication}_{kj} &\in& \mathbb{R}_{\ge 0}  & \forall k,j \in \mathcal{K} \quad\text{(communication requirement between departments }k\text{ and }j\text{)}\\[1mm]
\text{Cost}_{\ell m} &\in& \mathbb{R}_{\ge 0}  & \forall \ell, m\in \mathcal{L} \quad\text{(unit communication cost between city } \ell \text{ and city } m\text{)}\\[3mm]
\textbf{Decision Variables:}&&&\\[1mm]
x_{k\ell} &\in& \{0,1\} & \forall k\in \mathcal{K},\, \ell\in \mathcal{L}, \quad\text{where } x_{k\ell} = 
\begin{cases}
1, & \text{if department } k \text{ is assigned to city } \ell,\\[1mm]
0, & \text{otherwise.}
\end{cases}
\end{array}
\]

\vspace{3mm}

\noindent The company wishes to choose the location for each department so as to minimize the overall yearly cost. This overall cost consists of the communication costs between departments (which depend on the cities where they are located) minus the benefits obtained from relocating a department.

\vspace{2mm}

\[
\begin{array}{rcl}
\textbf{Minimize} && Z = \sum_{k\in \mathcal{K}}\sum_{j\in \mathcal{K}} \sum_{\ell\in \mathcal{L}} \sum_{m\in \mathcal{L}} \text{Communication}_{kj} \cdot \text{Cost}_{\ell m}\, x_{k\ell}\, x_{jm} \; - \; \sum_{k\in \mathcal{K}}\sum_{\ell\in \mathcal{L}} \text{Benefit}_{k\ell}\, x_{k\ell}. \\[2mm]
\textbf{Subject to} &&&\\[1mm]
\text{(1) Assignment Constraint:} && \sum_{\ell\in \mathcal{L}} x_{k\ell} = 1, & \forall k \in \mathcal{K}, \\[2mm]
\text{(2) Capacity Constraint:} && \sum_{k\in \mathcal{K}} x_{k\ell} \le 3, & \forall \ell \in \mathcal{L}, \\[2mm]
&&&\\[1mm]
\textbf{Decision Variables:} && x_{k\ell} \in \{0,1\}, & \forall k \in \mathcal{K}, \; \forall \ell \in \mathcal{L}.
\end{array}
\]

\vspace{3mm}

\noindent A brief explanation of each component:

1. \textbf{Decision Variables:}  
   The binary variable \( x_{k\ell} \) indicates whether department \( k \) is located in city \( \ell \) (including London).

2. \textbf{Objective Function:}  
   The objective is to minimize the overall cost which has two parts:
   - The first term,
     \[
     \sum_{k\in \mathcal{K}}\sum_{j\in \mathcal{K}} \sum_{\ell\in \mathcal{L}} \sum_{m\in \mathcal{L}} \text{Communication}_{kj} \cdot \text{Cost}_{\ell m}\, x_{k\ell}\, x_{jm},
     \]
     represents the communication cost incurred between every pair of departments \( (k,j) \) given the cost of communication between their cities.
   - The second term,
     \[
     - \sum_{k\in \mathcal{K}}\sum_{\ell\in \mathcal{L}} \text{Benefit}_{k\ell}\, x_{k\ell},
     \]
     subtracts the benefit (in thousands of pounds) obtained by relocating the departments (or keeping them in London where applicable).

3. \textbf{Constraints:}
   - The assignment constraint ensures that each department is assigned to exactly one city.
   - The capacity constraint guarantees that no city (including London) hosts more than three departments.

This complete and self‐contained mathematical formulation accurately represents the original real–world economic and business decision problem.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Data
    # Number of departments and cities
    K = 5
    L = 3

    # Provided Benefit matrix for departments at relocation cities (first two columns).
    # For London (third city) we assume a benefit of 0.
    # Original provided Benefit (shape 5x2):
    # Row 1: [10, 10]
    # Row 2: [15, 20]
    # Row 3: [10, 15]
    # Row 4: [20, 15]
    # Row 5: [5, 15]
    provided_benefit = [
        [10, 10],
        [15, 20],
        [10, 15],
        [20, 15],
        [5, 15]
    ]
    # build full Benefit matrix for L=3 locations, assuming 0 benefit for London (3rd city)
    Benefit = [row + [0] for row in provided_benefit]

    # Communication matrix between departments (5x5)
    Communication = [
        [0.0, 0.0, 1.0, 1.5, 0.0],
        [0.0, 0.0, 0.0, 1.4, 1.2],
        [0.0, 1.0, 1.4, 0.0, 0.0],
        [2.0, 1.5, 1.2, 0.0, 2.0],
        [0.7, 0.0, 0.0, 2.0, 0.7]
    ]

    # Cost matrix between cities (3x3)
    Cost = [
        [5, 14, 13],
        [15, 5, 9],
        [13, 9, 10]
    ]
    
    # Scale factor to convert decimal coefficients to integers
    scale = 10

    model = cp_model.CpModel()

    # Decision variables: x[k][l] = 1 if department k is assigned to city l.
    x = {}
    for k in range(K):
        for l in range(L):
            x[k, l] = model.NewBoolVar(f'x[{k},{l}]')

    # Assignment Constraint: Every department is assigned to exactly one city.
    for k in range(K):
        model.Add(sum(x[k, l] for l in range(L)) == 1)

    # Capacity Constraint: At most 3 departments per city.
    for l in range(L):
        model.Add(sum(x[k, l] for k in range(K)) <= 3)

    # Create product variables y[k,j,l,m] = x_{k,l} * x_{j,m}
    y = {}
    for k in range(K):
        for j in range(K):
            for l in range(L):
                for m in range(L):
                    y[k, j, l, m] = model.NewBoolVar(f'y[{k},{j},{l},{m}]')
                    # Linearization constraints for product of two booleans:
                    model.Add(y[k, j, l, m] <= x[k, l])
                    model.Add(y[k, j, l, m] <= x[j, m])
                    model.Add(y[k, j, l, m] >= x[k, l] + x[j, m] - 1)

    # Objective: minimize overall cost = communication cost - benefit.
    # Communication cost part: sum_{k,j,l,m} Communication[k][j] * Cost[l][m] * (scaled factor) * y[k,j,l,m]
    # Benefit part: sum_{k,l} Benefit[k][l] * (scaled factor) * x[k,l]
    objective_terms = []
    for k in range(K):
        for j in range(K):
            for l in range(L):
                for m in range(L):
                    comm_val = int(round(Communication[k][j] * scale))
                    coef = comm_val * Cost[l][m]
                    if coef != 0:
                        objective_terms.append(coef * y[k, j, l, m])
    # Subtract benefits; scale benefit as well.
    benefit_terms = []
    for k in range(K):
        for l in range(L):
            benefit_terms.append(Benefit[k][l] * scale * x[k, l])
    
    model.Minimize(sum(objective_terms) - sum(benefit_terms))
    
    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Optimal solution found:')
        print(f'Objective value: {solver.ObjectiveValue()/scale:.2f}')
        for k in range(K):
            for l in range(L):
                if solver.Value(x[k, l]) == 1:
                    # Determine city name: For simplicity, city 2 (index 2) is London.
                    city = f'City {l+1}' if l != 2 else 'London'
                    print(f'Department {k+1} assigned to {city}')
    else:
        print("No feasible solution found.")


if __name__ == '__main__':
    main()