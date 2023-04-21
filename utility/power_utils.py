from utility.constants import Po, changeTime, staticTime

def power_consumption(Ti, Tf, To):
    Pnet = 0
    if min(Ti, Tf) >= To or max(Ti, Tf) <= To:
        Pnet = Po * changeTime * abs((Ti + Tf) / 2 - To) + Po * staticTime * abs(Tf - To)
    else:
        roomTime = ((To - Ti) * changeTime) / (Tf - Ti)
        Pnet = Po * (changeTime - 2 * roomTime) * abs((Ti + Tf) / 2 - To) + Po * staticTime * abs(Tf - To) + 2 * Po * roomTime * abs(Ti - Tf)
    return Pnet / (60 * 1000)


def power_price_gradient(Tnext, T, Tprev, To, price):
    grad = 0
    if min(Tprev, T) >= To or max(Tprev, T) <= To:
        if Tprev + T != 2 * To:
            grad += 0.5 * Po * changeTime * abs((Tprev + T) / 2 - To) / ((Tprev + T) / 2 - To)
        if T != To:
            grad += Po * staticTime * abs(T - To) / (T - To)
    else:
        roomTime = ((To - Tprev) * changeTime) / (T - Tprev)
        roomTimeGrad = -((To - Tprev) * changeTime) / ((T - Tprev)**2)
        if Tprev + T != 2 * To:
            grad += 0.5 * Po * (changeTime - 2 * roomTime) * abs((Tprev + T) / 2 - To) / ((Tprev + T) / 2 - To) + Po * (-2 * roomTimeGrad) * abs((Tprev + T) / 2 - To)
        if T != To:
            grad += Po * staticTime * abs(T - To) / (T - To)
        if Tprev != T:
            grad += -2 * Po * roomTime * abs(Tprev - T) / (Tprev - T) + 2 * Po * roomTimeGrad * abs(Tprev - T)

    if min(T, Tnext) >= To or max(T, Tnext) <= To:
        if T + Tnext != 2 * To:
            grad += 0.5 * Po * changeTime * abs((T + Tnext) / 2 - To) / ((T + Tnext) / 2 - To)
    else:
        roomTime = ((To - T) * changeTime) / (Tnext - T)
        roomTimeGrad = ((To - Tnext) * changeTime) / (T - Tnext)**2
        if T + Tnext != 2 * To:
            grad += 0.5 * Po * (changeTime - 2 * roomTime) * abs((T + Tnext) / 2 - To) / ((T + Tnext) / 2 - To) + Po * (-2 * roomTimeGrad) * abs((T + Tnext) / 2 - To)
        if Tprev != T:
            grad += 2 * Po * roomTime * abs(T - Tnext) / (T - Tnext) + 2 * Po * roomTimeGrad * abs(T - Tnext)

    return grad * price / (60 * 1000)


def grad_checker(Tnext, T, Tprev, To, price):
    epsilon = 1e-7
    grad = 0
    grad += price * (power_consumption(Tprev, T + epsilon, To) - power_consumption(Tprev, T - epsilon, To)) / (2 * epsilon)
    grad += price * (power_consumption(T + epsilon, Tnext, To) - power_consumption(T - epsilon, Tnext, To)) / (2 * epsilon)
    if abs(grad - power_price_gradient(Tnext, T, Tprev, To, price)) > 100 * epsilon:
        print(Tnext, T, Tprev, To, price)
        print(grad * price, power_price_gradient(Tnext, T, Tprev, To, price))
