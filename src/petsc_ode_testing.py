import numpy as np
import matplotlib.pyplot as plt
import os
from equations import (
    exponential_decay, logistic_growth, simple_harmonic_motion, lorenz_system, van_der_pol
)
from ode_integrators import euler, rk4
from petsc4py import PETSc

# Ensure results directory exists
os.makedirs("results/figures", exist_ok=True)

def compute_errors(y_exact, y_numerical):
    y_exact, y_numerical = np.array(y_exact), np.array(y_numerical)
    N = len(y_exact)
    l2_error = np.linalg.norm(y_exact - y_numerical) / N
    max_error = np.max(np.abs(y_exact - y_numerical))
    rmse = np.sqrt(np.mean((y_exact - y_numerical) ** 2))
    return l2_error, max_error, rmse

def petsc_solve(f, y0, t):
    dt = t[1] - t[0]
    N = len(t)
    y = np.zeros((N, len(y0))) if isinstance(y0, (list, np.ndarray)) else np.zeros(N)
    y[0] = y0

    ts = PETSc.TS().create()
    ts.setType(PETSc.TS.Type.RK)
    ts.setTime(0.0)
    ts.setTimeStep(dt)
    ts.setMaxSteps(N - 1)
    ts.setMaxTime(t[-1])

    y0 = np.array(y0, ndmin=1)
    Y = PETSc.Vec().createSeq(len(y0))
    Y.setArray(y0)
    
    def rhs(ts, t, Y, Ydot):
        y_arr = Y.getArray()
        Ydot.setArray(f(t, y_arr).copy())  # Ensure array is writable


    ts.setRHSFunction(rhs)
    print("Initial Y:", Y.array)
    ts.solve(Y)

    for i in range(1, N):
        y[i] = Y.getArray()
    
    return y

# Define time grids
t = np.linspace(0, 5, 100)
t_shm = np.linspace(0, 10, 200)
t_vdp = np.linspace(0, 10, 200)

# Initial conditions
y0_exp = 1
y0_logistic = 1
y0_shm = [1, 0]
y0_vdp = [2, 0]

# Exact solutions
exact_exp = y0_exp * np.exp(-t)
exact_logistic = 10 / (1 + (10 - y0_logistic) / y0_logistic * np.exp(-t))
exact_shm = np.cos(t_shm)

# Solve with PETSc
petsc_exp = petsc_solve(exponential_decay, y0_exp, t)
petsc_logistic = petsc_solve(logistic_growth, y0_logistic, t)
petsc_shm = np.array(petsc_solve(simple_harmonic_motion, y0_shm, t_shm))[:, 0]
petsc_vdp = np.array(petsc_solve(van_der_pol, y0_vdp, t_vdp))

# Solve with Euler and RK4
euler_exp = euler(exponential_decay, y0_exp, t)
rk4_exp = rk4(exponential_decay, y0_exp, t)
euler_shm = np.array(euler(simple_harmonic_motion, y0_shm, t_shm))[:, 0]
rk4_shm = np.array(rk4(simple_harmonic_motion, y0_shm, t_shm))[:, 0]

euler_vdp = np.array(euler(van_der_pol, y0_vdp, t_vdp))
rk4_vdp = np.array(rk4(van_der_pol, y0_vdp, t_vdp))

# Compute errors
errors = {
    "Euler (Exp)": compute_errors(exact_exp, euler_exp),
    "RK4 (Exp)": compute_errors(exact_exp, rk4_exp),
    "PETSc (Exp)": compute_errors(exact_exp, petsc_exp),
    "Euler (SHM)": compute_errors(exact_shm, euler_shm),
    "RK4 (SHM)": compute_errors(exact_shm, rk4_shm),
    "PETSc (SHM)": compute_errors(exact_shm, petsc_shm),
}

# Plot results
def plot_results(t, exact, euler_sol, rk4_sol, petsc_sol, title, filename):
    plt.figure(figsize=(10, 5))
    plt.plot(t, exact, label="Exact", linewidth=2)
    plt.plot(t, euler_sol, "--", label="Euler", alpha=0.7)
    plt.plot(t, rk4_sol, "--", label="RK4", alpha=0.7)
    plt.plot(t, petsc_sol, "--", label="PETSc", alpha=0.7)
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.savefig(f"results/figures/{filename}")
    plt.show()

plot_results(t, exact_exp, euler_exp, rk4_exp, petsc_exp, "Exponential Decay", "exp.png")
plot_results(t_shm, exact_shm, euler_shm, rk4_shm, petsc_shm, "Simple Harmonic Motion", "shm.png")

# Save LaTeX error report
latex_filename = "results/error_report.tex"
with open(latex_filename, "w") as file:
    file.write("\\begin{table}[h]\n")
    file.write("    \\centering\n")
    file.write("    \\begin{tabular}{|l|c|c|c|} \\hline\n")
    file.write("    Method & L2 Error & Max Error & RMSE \\ \\hline\n")
    for key, value in errors.items():
        file.write(f"    {key} & {value[0]:.6f} & {value[1]:.6f} & {value[2]:.6f} \\ \\hline\n")
    file.write("    \\end{tabular}\n")
    file.write("    \\caption{Numerical Errors for Different Methods}\n")
    file.write("    \\label{tab:errors}\n")
    file.write("\\end{table}\n")

print(f"LaTeX report saved to {latex_filename}")
