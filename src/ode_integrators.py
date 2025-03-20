import numpy as np

def euler(f, y0, t):
    """ Euler's method for solving ODEs. """
    y0 = np.asarray(y0)
    y = np.zeros((len(t), *y0.shape))  # for scalar and vector cases and shape handling
    y[0] = y0

    for i in range(1, len(t)):
        h = t[i] - t[i - 1]
        y[i] = y[i - 1] + h * np.asarray(f(t[i - 1], y[i - 1]))  # ensure correct shape

    return y

def rk4(f, y0, t):
    """ Runge-Kutta 4th order method for solving ODEs. """
    y0 = np.asarray(y0)
    y = np.zeros((len(t), *y0.shape)) 
    y[0] = y0

    for i in range(1, len(t)):
        h = t[i] - t[i - 1]
        k1 = np.asarray(f(t[i - 1], y[i - 1]))
        k2 = np.asarray(f(t[i - 1] + h / 2, y[i - 1] + h * k1 / 2))
        k3 = np.asarray(f(t[i - 1] + h / 2, y[i - 1] + h * k2 / 2))
        k4 = np.asarray(f(t[i - 1] + h, y[i - 1] + h * k3))
        y[i] = y[i - 1] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return y
