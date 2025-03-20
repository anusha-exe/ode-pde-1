import numpy as np
import matplotlib.pyplot as plt
import os
from equations import (
    exponential_decay, logistic_growth, simple_harmonic_motion, lorenz_system, van_der_pol
)
from ode_integrators import euler, rk4

# debugging
os.makedirs("results/figures", exist_ok=True)

# error metrics
def compute_errors(y_exact, y_numerical):
    y_exact, y_numerical = np.array(y_exact), np.array(y_numerical)
    N = len(y_exact)
    l2_error = np.linalg.norm(y_exact - y_numerical) / N
    max_error = np.max(np.abs(y_exact - y_numerical))
    rmse = np.sqrt(np.mean((y_exact - y_numerical) ** 2))
    return l2_error, max_error, rmse

# defining time grid
t = np.linspace(0, 5, 100)
# initial conditions for exponential growth and logistic decay
y0_exp = 1  
y0_logistic = 1  

# exact solutions
exact_exp = y0_exp * np.exp(-t)
exact_logistic = 10 / (1 + (10 - y0_logistic) / y0_logistic * np.exp(-t))

# numerical solutions for a simple ODE
euler_exp = euler(exponential_decay, y0_exp, t)
rk4_exp = rk4(exponential_decay, y0_exp, t)
euler_logistic = euler(logistic_growth, y0_logistic, t)
rk4_logistic = rk4(logistic_growth, y0_logistic, t)

# computing errors and create a dictionary
errors = {
    "Euler (Exponential Decay)": compute_errors(exact_exp, euler_exp),
    "RK4 (Exponential Decay)": compute_errors(exact_exp, rk4_exp),
    "Euler (Logistic Growth)": compute_errors(exact_logistic, euler_logistic),
    "RK4 (Logistic Growth)": compute_errors(exact_logistic, rk4_logistic),
}

# print the errors
for key, value in errors.items():
    print(f"{key}: L2 Error={value[0]:.6f}, Max Error={value[1]:.6f}, RMSE={value[2]:.6f}")

# plotting
def plot_results(t, exact, euler_sol, rk4_sol, title, filename):
    plt.figure(figsize=(10, 5))
    plt.plot(t, exact, label="Exact", linewidth=2)
    plt.plot(t, euler_sol, "--", label="Euler", alpha=0.7)
    plt.plot(t, rk4_sol, "--", label="RK4", alpha=0.7)
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.savefig(f"results/figures/{filename}")
    plt.show()


plot_results(t, exact_exp, euler_exp, rk4_exp, "Exponential Decay", "exponential_decay.png")
plot_results(t, exact_logistic, euler_logistic, rk4_logistic, "Logistic Growth", "logistic_growth.png")

## Simple Harmonic Motion
t_shm = np.linspace(0, 10, 200)
y0_shm = [1, 0]

# SHM exact solution: y = cos(t) (taking omega = 1)
exact_shm = np.cos(t_shm)

# numerical solutions for SHM
euler_shm = np.array(euler(simple_harmonic_motion, y0_shm, t_shm))[:, 0]
rk4_shm = np.array(rk4(simple_harmonic_motion, y0_shm, t_shm))[:, 0]

# Compute errors
errors["Euler (SHM)"] = compute_errors(exact_shm, euler_shm)
errors["RK4 (SHM)"] = compute_errors(exact_shm, rk4_shm)

# Plot SHM
plot_results(t_shm, exact_shm, euler_shm, rk4_shm, "Simple Harmonic Motion", "shm.png")

## Lorenz System
t_lorenz = np.linspace(0, 5, 1000)
y0_lorenz = [1, 1, 1]

# Lorenz being chaotic, getting an explicit exact solution is not possible. We assume RK4 as "ground truth"
rk4_lorenz = np.array(rk4(lorenz_system, y0_lorenz, t_lorenz))
euler_lorenz = np.array(euler(lorenz_system, y0_lorenz, t_lorenz))

# compute errors using RK4 as reference
errors["Euler (Lorenz)"] = compute_errors(rk4_lorenz[:, 0], euler_lorenz[:, 0])

# plotting Lorenz
plt.figure()
plt.plot(euler_lorenz[:, 0], euler_lorenz[:, 2], label="Euler")
plt.plot(rk4_lorenz[:, 0], rk4_lorenz[:, 2], label="RK4")
plt.xlabel("X")
plt.ylabel("Z")
plt.legend()
plt.savefig("results/figures/lorenz.png")
plt.show()

## Van der Pol Oscillator
t_vdp = np.linspace(0, 10, 200)
y0_vdp = [2, 0]

# assuming RK4 as "ground truth"
rk4_vdp = np.array(rk4(van_der_pol, y0_vdp, t_vdp))
euler_vdp = np.array(euler(van_der_pol, y0_vdp, t_vdp))

# compute errors using RK4 as reference
errors["Euler (Van der Pol)"] = compute_errors(rk4_vdp[:, 0], euler_vdp[:, 0])

# plotting Van der Pol
plt.figure()
plt.plot(euler_vdp[:, 0], euler_vdp[:, 1], label="Euler")
plt.plot(rk4_vdp[:, 0], rk4_vdp[:, 1], label="RK4")
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.legend()
plt.savefig("results/figures/vdp.png")
plt.show()

# printing final errors
print("\nFinal Errors:")
for key, value in errors.items():
    print(f"{key}: L2 Error={value[0]:.6f}, Max Error={value[1]:.6f}, RMSE={value[2]:.6f}")

# #  LaTeX format printing so that it can be directly copy pasted to doc
# print("\\hline")
# for key, value in errors.items():
#     method, test_case = key.split(" (")
#     test_case = test_case.strip(")")
#     print(f"{method} & {value[0]:.6f} & {value[1]:.6f} & {value[2]:.6f} \\\\")
# print("\\hline")

latex_filename = "results/error_report.tex"

# open LaTeX file
with open(latex_filename, "w") as file:

    # table structure
    file.write("\\begin{table}[h]\n")
    file.write("    \\centering\n")
    file.write("    \\begin{tabular}{|l|c|c|c|} \\hline\n")
    file.write("    Method & L2 Error & Max Error & RMSE \\\\ \\hline\n")

    # write each row of the table with formatted error values
    for key, value in errors.items():
        file.write(f"    {key} & {value[0]:.6f} & {value[1]:.6f} & {value[2]:.6f} \\\\ \\hline\n")

    # close the table
    file.write("    \\end{tabular}\n")
    file.write("    \\caption{Numerical Errors for Different Methods}\n")
    file.write("    \\label{tab:errors}\n")
    file.write("\\end{table}\n")

print(f"LaTeX report saved to {latex_filename}")

