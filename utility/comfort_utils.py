from utility.constants import inf


def comfort_function(Tmax, Tmin, Tset, Troom):
    if Troom <= Tmin or Troom >= Tmax:
        return inf
    elif Troom <= Tset:
        return (Tset - Troom) / (Troom - Tmin)
    elif Tset < Troom:
        return (Troom - Tset) / (Tmax - Troom)


def comfort_function_grad(Tmax, Tmin, Tset, Troom):
    if Troom <= Tmin:
        return -1e5
    elif Troom >= Tmax:
        return 1e5
    elif Troom <= Tset:
        return (Tmin - Tset) / (Troom - Tmin)**2
    elif Tset < Troom:
        return (Tmax - Tset) / (Tmax - Troom)**2
