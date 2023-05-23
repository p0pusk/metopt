import numpy as np
from scipy.optimize import minimize

def objective(x):
    y = x[0]
    z = x[1]
    return -1 * ((2 * (np.sqrt(1 - y**2)+z) * y - np.pi * z**2))

def constraint1(x):
    y = x[0]
    return 1 - y

def constraint2(x):
    y = x[0]
    z = x[1]
    return 2 * z - y

# Initial guess for the variables
x0 = [0.5, 0.5]

# Define the constraints
constraints = [
    {'type': 'ineq', 'fun': constraint1},
    {'type': 'ineq', 'fun': constraint2}
]

# Minimize the negative of the objective function to find the maximum
result = minimize(objective, x0, method='SLSQP', constraints=constraints)

if result.success:
    x_opt = result.x
    max_value = -1 * result.fun
    print("Optimization successful.")
    print("Maximum value:", max_value)
    print("Optimal variables (y, z):", x_opt)
else:
    print("Optimization failed. Constraints not satisfied.")