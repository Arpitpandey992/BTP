from utility.comfort_utils import comfort_function, comfort_function_grad
from utility.power_utils import power_consumption, power_price_gradient
from utility.constants import grid_prices


def overall_cost_function(grid_prices, room_temperatures, external_temperatures, Tmax, Tmin, Tset, alpha):
    cost = 0
    Ti = external_temperatures[0]
    for i in range(len(room_temperatures)):
        Troom = room_temperatures[i]
        To = external_temperatures[i]
        price = grid_prices[i // 4]
        cost += alpha * price * power_consumption(Ti, Troom, To) + (1 - alpha) * comfort_function(Tmax, Tmin, Tset, Troom)
        # print(power_consumption(Ti, Troom, To), comfort_function(Tmax, Tmin, Tset, Troom))
        Ti = To
    return cost


def overall_price_function(grid_prices, room_temperatures, external_temperatures):
    cost = 0
    Ti = external_temperatures[0]
    for i in range(len(room_temperatures)):
        Troom = room_temperatures[i]
        To = external_temperatures[i]
        price = grid_prices[i // 4]
        cost += price * power_consumption(Ti, Troom, To)
        Ti = To
    return cost


def cost_function_grad(Tnext, T, Tprev, To, price, Tmax, Tmin, Tset, alpha):
    grad = alpha * power_price_gradient(Tnext, T, Tprev, To, price) + (1 - alpha) * (comfort_function_grad(Tmax, Tmin, Tset, T))
    return grad


def objective_function(room_temperatures, alpha, external_temperatures, Tmin, Tset, Tmax):
    return overall_cost_function(grid_prices, room_temperatures, external_temperatures, Tmax, Tmin, Tset, alpha)
