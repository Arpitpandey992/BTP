import random

from utility.cost_utils import objective_function
from utility.constants import grid_prices
from weather.temperature import get_temperature_values


# Define the PSO algorithm
def pso(objective_function, num_variables, num_particles, max_iterations, alpha, external_temperatures, Tmin, Tset, Tmax):
    # Set the PSO parameters
    w = 0.729    # inertia weight
    c1 = 1.49445  # cognitive weight
    c2 = 1.49445  # social weight
    min_bounds = [20] * num_variables  # minimum search space boundary
    max_bounds = [26] * num_variables  # maximum search space boundary

    # Initialize the particle positions and velocities
    particles = []
    for i in range(num_particles):
        particle = {'position': [random.uniform(min_bounds[j], max_bounds[j]) for j in range(num_variables)],
                    'velocity': [random.uniform(-10, 10) for j in range(num_variables)],
                    'best_position': [],
                    'best_fitness': float('inf')}
        particle['fitness'] = objective_function(particle['position'], alpha, external_temperatures, Tmin, Tset, Tmax)
        particle['best_position'] = particle['position']
        particle['best_fitness'] = particle['fitness']
        particles.append(particle)

    # Initialize the global best position and fitness
    global_best_position = [random.uniform(min_bounds[j], max_bounds[j]) for j in range(num_variables)]
    global_best_fitness = float('inf')

    # Run the PSO algorithm for the specified number of iterations
    for iteration in range(max_iterations):
        for particle in particles:
            # Update the particle's velocity
            for j in range(num_variables):
                r1 = random.random()
                r2 = random.random()
                r3 = random.random()
                if r3 > 0.5:
                    r3 = 1
                else:
                    r3 = -1
                cognitive_velocity = c1 * r1 * (particle['best_position'][j] - particle['position'][j])
                social_velocity = c2 * r2 * (global_best_position[j] - particle['position'][j])
                particle['velocity'][j] = r3 * w * particle['velocity'][j] + cognitive_velocity + social_velocity

            # Update the particle's position
            for j in range(num_variables):
                particle['position'][j] += particle['velocity'][j]

                # Ensure the particle stays within the search space boundaries
                if particle['position'][j] < min_bounds[j]:
                    particle['position'][j] = min_bounds[j]
                elif particle['position'][j] > max_bounds[j]:
                    particle['position'][j] = max_bounds[j]

            # Update the particle's fitness
            particle['fitness'] = objective_function(particle['position'], alpha, external_temperatures, Tmin, Tset, Tmax)

            # Update the particle's best position and fitness
            if particle['fitness'] < particle['best_fitness']:
                particle['best_position'] = particle['position']
                particle['best_fitness'] = particle['fitness']

            # Update the global best position and fitness
            if particle['fitness'] < global_best_fitness:
                global_best_position = particle['position']
                global_best_fitness = particle['fitness']

        # Print the best fitness value of the current iteration
        print(f"Iteration {iteration}: Best fitness value = {global_best_fitness}")

    # Return the global best position and fitness
    return global_best_position, global_best_fitness


def test_pso():
    # Run the PSO algorithm for a problem with 96 variables
    num_variables = 96
    num_particles = 500
    max_iterations = 100
    Tmin = 17
    Tset = 23
    Tmax = 30
    external_temperatures = get_temperature_values()
    global_best_position, global_best_fitness = pso(objective_function, num_variables, num_particles, max_iterations, 0.5, external_temperatures, Tmin, Tset, Tmax)

    # Print the global best position and fitness
    print(f"Global best position = {global_best_position}")
    print(f"Global best fitness = {global_best_fitness}")
