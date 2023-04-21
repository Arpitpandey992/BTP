import numpy as np
from utility.adam import grad_descent
from utility.cost_utils import cost_function_grad, overall_cost_function
from utility.constants import grid_prices
from weather.temperature import get_temperature_values


def objective_function(room_temperatures, alpha, external_temperatures):
    return overall_cost_function(grid_prices, room_temperatures, external_temperatures, Tmax, Tmin, Tset, alpha)


def objective_function_grad(room_temperatures, alpha, external_temperatures):
    x = grad_descent(0.5, external_temperatures)
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
    return grad


def bfgs(cost_func, theta0, alfa, external_temperatures, max_iter=1000, tol=1e-6):
    """
    Minimizes the given cost function using the Broyden-Fletcher-Goldfarb-Shanno (BFGS) algorithm.

    Parameters:
    -----------
    cost_func : function
        A function that takes a numpy array theta as input and returns a scalar cost J.
    theta0 : numpy array
        The initial estimate of the optimal theta that minimizes the cost function.
    max_iter : int, optional
        The maximum number of iterations allowed for the algorithm.
    tol : float, optional
        The tolerance level for the change in the cost function between iterations.

    Returns:
    --------
    tuple
        A tuple containing the optimal estimate of theta and the final cost J.
    """

    n = len(theta0)
    theta = theta0
    H = np.eye(n)
    J = cost_func(theta, alfa, external_temperatures)
    J_vals = [J]
    grad = objective_function_grad(theta, alfa, external_temperatures)
    print(grad)

    for i in range(max_iter):
        print(i)
        d = -H @ grad
        # print(d)
        alpha = line_search(cost_func, theta, alfa, d, external_temperatures)
        print("alpha = " + str(alpha))
        theta_new = theta + alpha * d
        s = theta_new - theta
        # print(s)
        y = objective_function_grad(theta_new, alfa, external_temperatures) - grad
        # print("grad = " + str(y))
        rho = 1 / (y @ s)
        H_new = (np.eye(n) - rho * s.reshape(-1, 1) @ y.reshape(1, -1)) @ H @ (np.eye(n) - rho * y.reshape(-1, 1) @ s.reshape(1, -1)) + rho * s.reshape(-1, 1) @ s.reshape(1, -1)
        J_new = cost_func(theta_new, alfa, external_temperatures)
        J_vals.append(J_new)
        if abs(J_new - J) < tol:
            break
        theta = theta_new
        J = J_new
        grad = objective_function_grad(theta, alfa, external_temperatures)
        H = H_new
        print(J)
    return theta, J


def line_search(cost_func, theta, alfa, d, external_temperatures, alpha=100, rho=0.5, c=1e-4):
    """
    Performs a line search to find the optimal step size alpha for the search direction d.

    Parameters:
    -----------
    cost_func : function
        A function that takes a numpy array theta as input and returns a scalar cost J.
    theta : numpy array
        The current estimate of the optimal theta that minimizes the cost function.
    d : numpy array
        The search direction for the next update to theta.
    alpha : float, optional
        An initial estimate of the optimal step size alpha.
    rho : float, optional
        The shrinkage factor for the step size alpha in each iteration.
    c : float, optional
        The constant factor for the Armijo-Goldstein condition in the line search.

    Returns:
    --------
    float
        The optimal step size alpha.
    """

    J = cost_func(theta, alfa, external_temperatures)
    grad = objective_function_grad(theta, alfa, external_temperatures)
    # print("line grad = " + str(grad))
    c1 = c * grad @ d

    while True:
        theta_new = theta + alpha * d
        J_new = cost_func(theta_new, alfa, external_temperatures)
        print("J_new = " + str(J_new))
        print("J = " + str(J))
        print("alpha = " + str(alpha))
        print("c1 = " + str(c1))
        print("J - alpha * c1 = " + str(J - alpha * c1))
        if J_new <= J + alpha * c1:
            return alpha
        alpha *= rho


def test_bfgs():
    external_temperatures = get_temperature_values()
    bfgs(objective_function, [28] * 96, 0.5, external_temperatures)
