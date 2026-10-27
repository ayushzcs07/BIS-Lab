import random
import math

# Constants
N = 5               # Number of locations
ANTS = 10            # Number of ants
ITERATIONS = 100
ALPHA = 1.0          # Pheromone importance
BETA = 2.0           # Distance importance
RHO = 0.5            # Pheromone evaporation rate
Q = 100.0            # Pheromone deposit factor

# Distance matrix
distance = [
    [0,  10, 15, 20, 12],
    [10, 0,  35, 25, 17],
    [15, 35, 0,  30, 28],
    [20, 25, 30, 0,  18],
    [12, 17, 28, 18, 0]
]

# Initialize pheromone matrix
pheromone = [[1.0 for _ in range(N)] for _ in range(N)]


def main():
    best_route = []
    best_distance = math.inf

    # Main ACO loop
    for iteration in range(ITERATIONS):

        for ant in range(ANTS):
            route = [0] * (N + 1)
            visited = [False] * N
            total_distance = 0.0

            # Start from location 0
            route[0] = 0
            visited[0] = True

            # Construct the route
            for step in range(1, N):
                current = route[step - 1]
                probabilities = [0.0] * N
                total = 0.0

                # Calculate transition probabilities
                for city in range(N):
                    if not visited[city]:
                        probabilities[city] = (
                            pheromone[current][city] ** ALPHA
                            * (1.0 / distance[current][city]) ** BETA
                        )
                        total += probabilities[city]

                # Roulette-wheel selection
                random_value = random.random() * total
                next_city = -1

                for city in range(N):
                    if not visited[city]:
                        random_value -= probabilities[city]

                        if random_value <= 0.0:
                            next_city = city
                            break

                # Fallback for floating-point rounding
                if next_city == -1:
                    for city in range(N - 1, -1, -1):
                        if not visited[city]:
                            next_city = city
                            break

                route[step] = next_city
                visited[next_city] = True

                total_distance += distance[current][next_city]

            # Return to the starting location
            route[N] = 0
            total_distance += distance[route[N - 1]][0]

            # Update the best route
            if total_distance < best_distance:
                best_distance = total_distance
                best_route = route.copy()

            # Deposit pheromones on the route
            for i in range(N):
                start = route[i]
                end = route[i + 1]

                pheromone[start][end] += Q / total_distance
                pheromone[end][start] += Q / total_distance

        # Evaporate pheromones
        for i in range(N):
            for j in range(N):
                pheromone[i][j] *= (1.0 - RHO)

    # Display results
    print("Best route:", " ".join(map(str, best_route)))
    print(f"Total distance: {best_distance:.2f}")


if __name__ == "__main__":
    main()
