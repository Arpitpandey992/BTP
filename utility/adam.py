import numpy as np

from utility.cost_utils import cost_function_grad
from utility.constants import grid_prices
from weather.temperature import get_temperature_values


def grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax):
    # Define the variables to optimize
    x = [28] * 96
    # print(x)
    # Define the hyperparameters for Adam optimization
    alphaGrad = 0.1
    beta1 = 0.9
    beta2 = 0.999
    epsilon = 1e-8

    # Initialize the variables for Adam optimization
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    t = 0

    # Define the training loop
    while True:
        t += 1
        # Compute the gradient of the function with respect to x
        grad = np.array([])
        Tprev = external_temperatures[0]
        for i in range(len(x)):
            Troom = x[i]
            Tnext = x[min(i + 1, len(x) - 1)]
            To = external_temperatures[i]
            price = grid_prices[i // 4]
            # print(cost_function_grad(Tnext, Troom, Tprev, To, price, Tmax, Tmin, Tset, 0))
            grad = np.append(grad, cost_function_grad(Tnext, Troom, Tprev, To, price, Tmax, Tmin, Tset, alpha))
            Tprev = To
        # print(grad)
        # Update the first moment estimates
        m = beta1 * m + (1 - beta1) * grad
        # Update the second moment estimates
        v = beta2 * v + (1 - beta2) * grad**2
        # Compute the bias-corrected first and second moment estimates
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        # Compute the update for x
        deltaGrad = alphaGrad * m_hat / (np.sqrt(v_hat) + epsilon)
        x -= deltaGrad
        # print(x)
        # Check if the change in x is small enough
        if np.all(abs(deltaGrad) < 1e-3) or t > 1000:
            return x
            break
    # Print the optimum value of x
    # print("Optimum value of x:", x)
    # Print the minimum value of the function
    # print("Minimum value of the function:", overall_cost_function(x, 0))


def test_adam(alpha: float = 0.5):
    Tmin = 17
    Tset = 23
    Tmax = 30
    external_temperatures = get_temperature_values()
    print(f"External temperatures : {external_temperatures}\n")
    print(f'adam at aplha = {alpha}:\n{grad_descent(alpha, external_temperatures,Tmin, Tset, Tmax)}')
