import numpy as np

def exponential_decay(t, y, lambda_=1.0):
    """dy/dt = -lambda * y"""
    return -lambda_ * y

def logistic_growth(t, y, r=1, K=10):
    """dy/dt = r * y * (1 - y/K)"""
    return r * y * (1 - y/K)

def simple_harmonic_motion(t, y, omega=1.0):
    """dx/dt = v, dv/dt = -omega^2 * x"""
    x, v = y
    return np.array([v, -omega**2 * x])

def lorenz_system(t, y):
    """Lorenz system of differential equations"""
    sigma, rho, beta = 10, 28, 8/3
    dx_dt = sigma * (y[1] - y[0])
    dy_dt = y[0] * (rho - y[2]) - y[1]
    dz_dt = y[0] * y[1] - beta * y[2]
    return np.array([dx_dt, dy_dt, dz_dt])

def van_der_pol(t, y, mu=1.0):
    """Van der Pol oscillator"""
    y1, y2 = y
    return np.array([y2, mu * (1 - y1**2) * y2 - y1])
