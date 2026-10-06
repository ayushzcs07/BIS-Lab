import random

# PSO parameters
N = 10 # Number of particles
D = 4 # Number of traffic signals
T = 50 # Maximum iterations

w = 0.7 # Inertia weight
c1 = 1.5 # Cognitive coefficient
c2 = 1.5 # Social coefficient

# Number of vehicles at each signal
traffic = [80, 60, 100, 70]

# Minimum and maximum green time
MIN_GREEN = 10
MAX_GREEN = 60


# Fitness function
# Higher fitness = better solution
def fitness(position):

    total_waiting_time = 0

    for i in range(D):

        green_time = position[i]

        # More green time -> less waiting
        waiting_time = traffic[i] * (60 - green_time)

        total_waiting_time += waiting_time

    # PSO here maximizes fitness,
    # so use negative waiting time
    return -total_waiting_time


# Initialize particles
particles = []

for i in range(N):

    position = []

    velocity = []

    for j in range(D):

        position.append(
            random.uniform(MIN_GREEN, MAX_GREEN)
        )

        velocity.append(
            random.uniform(-5, 5)
        )

    particles.append({
        "position": position,
        "velocity": velocity,
        "pbest": position.copy(),
        "pbest_fitness": fitness(position)
    })


# Find initial global best
global_best = particles[0]["pbest"].copy()
global_best_fitness = particles[0]["pbest_fitness"]

for particle in particles:

    if particle["pbest_fitness"] > global_best_fitness:

        global_best = particle["pbest"].copy()
        global_best_fitness = particle["pbest_fitness"]


# PSO main loop
for iteration in range(T):

    for particle in particles:

        # Generate random values
        r1 = random.random()
        r2 = random.random()

        # Update velocity
        for j in range(D):

            particle["velocity"][j] = (
                w * particle["velocity"][j]
                + c1 * r1 *
                (particle["pbest"][j] -
                 particle["position"][j])
                + c2 * r2 *
                (global_best[j] -
                 particle["position"][j])
            )

        # Update position
        for j in range(D):

            particle["position"][j] += \
                particle["velocity"][j]

            # Keep green time within limits
            particle["position"][j] = max(
                MIN_GREEN,
                min(MAX_GREEN,
                    particle["position"][j])
            )

        # Evaluate fitness
        current_fitness = fitness(
            particle["position"]
        )

        # Update personal best
        if current_fitness > particle["pbest_fitness"]:

            particle["pbest"] = \
                particle["position"].copy()

            particle["pbest_fitness"] = \
                current_fitness

        # Update global best
        if particle["pbest_fitness"] > global_best_fitness:

            global_best = \
                particle["pbest"].copy()

            global_best_fitness = \
                particle["pbest_fitness"]


# Output
print("\nOPTIMAL TRAFFIC SIGNAL TIMING")
print("--------------------------------")

for i in range(D):

    print(
        f"Signal {i + 1}: "
        f"{global_best[i]:.2f} seconds Green"
    )

print(
    "\nMinimum Total Waiting Time:",
    -global_best_fitness
)
