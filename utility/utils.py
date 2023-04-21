import numpy as np


def generate_array_for_mean_and_std(n, mean, std):
    return mean + std * (np.round(2 * np.random.rand(n), 2) - 1)
