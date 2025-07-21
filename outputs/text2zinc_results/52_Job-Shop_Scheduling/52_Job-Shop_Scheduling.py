# Mathematical Formulation:
'''\begin{align*}
\textbf{Indices and Sets:}\\[1mm]
&i \in I = \{1, 2, \dots, n\} \quad &&\text{(jobs, where } n = \mathtt{num\_jobs}\text{)}\\[1mm]
&r \in R = \{1, 2, \dots, m\} \quad &&\text{(operation positions in a job, where } m = \mathtt{num\_machines}\text{)}\\[1mm]
&j \in M = \{1, 2, \dots, m\} \quad &&\text{(machines)}\\[2mm]
\textbf{Data:}\\[1mm]
& p_{i,j} \quad &&\text{processing time of job } i \text{ on machine } j,\ \text{given by the matrix } \mathtt{job\_times}.\\[1mm]
& o_{i,j} \quad &&\text{the prescribed position in the sequence at which job } i \text{ is processed on machine } j,\ \text{given by } \mathtt{job\_order}.\\[1mm]
& \mathtt{max\_time} \quad &&\text{an upper bound on time horizon.}\\[2mm]
\textbf{Auxiliary Mapping:}\\[1mm]
&\text{For each job } i \text{ and position } r\in R,\text{ define } M(i,r) \text{ as the unique machine } j \text{ such that } o_{i,j} = r.\\[2mm]
\textbf{Decision Variables:}\\[1mm]
& S_{i,r} \in [0,\mathtt{max\_time}] \quad &&\text{start time of the } r\text{-th operation (i.e., on machine } M(i,r)\text{) of job } i.\\[1mm]
& C_{i,r} \in [0,\mathtt{max\_time}] \quad &&\text{completion time of the } r\text{-th operation of job } i, \text{ with } C_{i,r} = S_{i,r} + p_{i, M(i,r)}.\\[1mm]
& \delta_{i,k,j} \in \{0,1\} \quad &&\forall\, i,k\in I,\ i<k,\ \forall\, j\in M \text{ that appear in both jobs,}\\[1mm]
&&&\text{indicating the processing order on machine } j \text{ between jobs } i \text{ and } k.\\[2mm]
& C_{\max} \in [0,\mathtt{max\_time}] \quad &&\text{the overall makespan (maximum completion time)}.\\[2mm]
\textbf{Objective Function:}\\[1mm]
& \text{Minimize} \quad C_{\max} &\\[2mm]
\textbf{Constraints:}\\[1mm]
\text{(1) Job precedence constraints:}\\[1mm]
& \forall i \in I,\ \forall r=1,\dots, m-1:\quad & C_{i,r} &\le S_{i,r+1}, \quad\text{where } C_{i,r} = S_{i,r} + p_{i, M(i,r)}. \\[2mm]
\text{(2) Machine non‐overlap constraints:}\\[1mm]
& \text{For every machine } j \in M \text{ and for every pair of distinct jobs } i,k \in I \text{ that use } j\text{,}\\[1mm]
& \text{let } r = \text{ such that } M(i,r)=j \quad \text{and} \quad r' = \text{ such that } M(k,r')=j. \text{ Then,}\\[1mm]
& \forall\, i,k\in I,\ i<k \text{ with } j \text{ used by both:}\\[1mm]
& S_{i,r} + p_{i,j} \le S_{k,r'} + M\,(1-\delta_{i,k,j}), \\[1mm]
& S_{k,r'} + p_{k,j} \le S_{i,r} + M\,\delta_{i,k,j}, \quad\text{where } M \text{ is a suitably large constant (e.g. } \mathtt{max\_time}\text{)}.\\[2mm]
\text{(3) Makespan constraint:}\\[1mm]
& \forall i \in I:\quad C_{i,m} &\le C_{\max}, \quad\text{where } C_{i,m} = S_{i,m} + p_{i, M(i,m)}.\\[2mm]
\text{(4) Consistency of completion times:}\\[1mm]
& \forall i \in I,\ \forall r \in R:\quad C_{i,r} &= S_{i,r} + p_{i, M(i,r)}.\\[2mm]
\textbf{Summary of the Model:}\\[1mm]
\text{Minimize } & C_{\max} \\[1mm]
\text{subject to:}\\[1mm]
& S_{i,r} \ge 0, \quad \forall\, i\in I,\ r\in R,\\[1mm]
& C_{i,r} = S_{i,r} + p_{i, M(i,r)}, \quad \forall\, i\in I,\ r\in R,\\[1mm]
& S_{i,r+1} \ge C_{i,r}, \quad \forall\, i\in I,\ r=1,\dots,m-1,\\[1mm]
& S_{i,r} + p_{i,j} \le S_{k,r'} + M\,(1-\delta_{i,k,j}),\\[1mm]
& \quad\forall \, i,k\in I,\ i<k,\ \forall\, j \in M \text{ with } \exists\, r,\, r' \text{ satisfying } M(i,r)=M(k,r')=j,\\[1mm]
& S_{k,r'} + p_{k,j} \le S_{i,r} + M\,\delta_{i,k,j},\\[1mm]
& \quad\forall \, i,k\in I,\ i<k,\ \forall\, j \in M \text{ with } \exists\, r,\, r' \text{ satisfying } M(i,r)=M(k,r')=j,\\[1mm]
& C_{i,m} \le C_{\max},\quad \forall\, i\in I,\\[1mm]
& \delta_{i,k,j} \in \{0,1\},\quad \forall\, i,k\in I,\ i<k,\ \forall\, j \in M \text{ used by both jobs.}
\end{align*}

\vspace{2mm}
\textbf{Explanation:}\\[1mm]
1. \emph{Decision Variables:}  
   - S_{i,r} denotes the start time of the r-th operation for job i; its domain is [0, max\_time].  
   - C_{i,r} is defined as the corresponding completion time (start time plus processing time on the assigned machine).  
   - \delta_{i,k,j} is a binary variable that enforces the sequencing between jobs i and k on a common machine j.  
   - C_{\max} represents the overall makespan and is to be minimized.  
2. \emph{Objective Function:} We minimize C_{\max} (i.e. minimize the earliest possible finish time over all jobs).  
3. \emph{Constraints:}  
   - The job precedence constraints enforce that within each job, the operations follow the required order (as specified by o_{i,j} encoded via the mapping M(i,r)).  
   - The machine non‐overlap constraints, using the binary variables \delta_{i,k,j} and a big‐M constant, ensure that no two jobs are processed simultaneously on the same machine.  
   - The makespan constraints guarantee that C_{\max} is at least the finishing time of the final operation for each job.  
   - The consistency constraints define the relationship between start times and completion times.  
4. The model is fully specified, bounded (by max\_time) and feasible provided the data (job\_times and job\_order) yield a consistent job processing sequence.

This complete formulation accurately represents the Job-Shop Scheduling Problem as described.'''

# Generated Code:
from ortools.sat.python import cp_model


def main():
    # Problem Data
    num_machines = 4
    num_jobs = 4
    max_time = 200

    # Processing times: job_times[job][machine]
    job_times = [
        [30, 60, 2, 5],    # Algy
        [75, 25, 3, 10],   # Bertie
        [15, 10, 5, 30],   # Charlie
        [1, 1, 1, 90]      # Digby
    ]

    # Job processing order: job_order[job][machine] represents the order position (1-indexed)
    # For each job, order values indicate the sequence position in which the corresponding machine is processed.
    job_order = [
        [2, 1, 3, 4],     # Algy: first operation on machine with order '1' (machine 1), then machine with order '2' (machine 0), then ...
        [1, 3, 2, 4],     # Bertie
        [2, 3, 1, 4],     # Charlie
        [3, 2, 4, 1]      # Digby
    ]

    # Create the mapping M: For each job i and operation index r (0-indexed),
    # determine the machine j such that job_order[i][j] == r+1.
    M = [[None for _ in range(num_machines)] for _ in range(num_jobs)]
    for i in range(num_jobs):
        for j in range(num_machines):
            order = job_order[i][j]
            # order is 1-indexed, so operation index is order-1.
            M[i][order - 1] = j

    # Create the model.
    model = cp_model.CpModel()

    # Variables: S[i][r] is start time for job i's r-th operation. C[i][r] is completion time.
    S = {}
    C = {}
    for i in range(num_jobs):
        for r in range(num_machines):
            S[i, r] = model.NewIntVar(0, max_time, f"S_{i}_{r}")
            C[i, r] = model.NewIntVar(0, max_time, f"C_{i}_{r}")

    # Makespan variable
    C_max = model.NewIntVar(0, max_time, "C_max")

    # Big M constant
    big_M = max_time

    # Decision variables delta: for every pair of distinct jobs (i,k) with i < k and for each machine j.
    # Only create delta for machines j (0-indexed) because all jobs use all machines.
    delta = {}
    for j in range(num_machines):
        for i in range(num_jobs):
            for k in range(i + 1, num_jobs):
                delta[i, k, j] = model.NewBoolVar(f"delta_{i}_{k}_{j}")

    # Constraints

    # (4) Consistency: C[i][r] = S[i][r] + p[i, M(i,r)]
    for i in range(num_jobs):
        for r in range(num_machines):
            machine_j = M[i][r]
            p_time = job_times[i][machine_j]
            model.Add(C[i, r] == S[i, r] + p_time)

    # (1) Job precedence: within each job, the operations must be sequential.
    for i in range(num_jobs):
        for r in range(num_machines - 1):
            model.Add(S[i, r + 1] >= C[i, r])

    # (2) Machine non-overlap constraints: for every pair of jobs using the same machine j.
    for j in range(num_machines):
        # For each pair of jobs, find the operation index corresponding to machine j.
        for i in range(num_jobs):
            # Find operation index r_i for job i such that machine = j.
            r_i = None
            for r in range(num_machines):
                if M[i][r] == j:
                    r_i = r
                    break
            for k in range(i + 1, num_jobs):
                r_k = None
                for r in range(num_machines):
                    if M[k][r] == j:
                        r_k = r
                        break
                # Enforce disjoint processing on machine j using delta variables:
                # Option 1: Job i then job k
                model.Add(S[i, r_i] + job_times[i][j] <= S[k, r_k] + big_M * (1 - delta[i, k, j]))
                # Option 2: Job k then job i
                model.Add(S[k, r_k] + job_times[k][j] <= S[i, r_i] + big_M * delta[i, k, j])

    # (3) Makespan constraint: the completion time of the last operation for each job is <= C_max.
    for i in range(num_jobs):
        model.Add(C[i, num_machines - 1] <= C_max)

    # Objective: minimize makespan.
    model.Minimize(C_max)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Solution:")
        print(f"Optimal makespan = {solver.Value(C_max)}")
        for i in range(num_jobs):
            print(f"Job {i}:")
            for r in range(num_machines):
                machine_j = M[i][r]
                start = solver.Value(S[i, r])
                comp = solver.Value(C[i, r])
                print(f"  Operation {r+1} on Machine {machine_j}: Start = {start}, Duration = {job_times[i][machine_j]}, Completion = {comp}")
        print()
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()