
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N 5               // Number of locations
#define ANTS 10            // Number of ants
#define ITERATIONS 100
#define ALPHA 1.0          // Pheromone importance
#define BETA 2.0           // Distance importance
#define RHO 0.5            // Pheromone evaporation rate
#define Q 100.0            // Pheromone deposit factor

double distance[N][N] = {
    {0,  10, 15, 20, 12},
    {10, 0,  35, 25, 17},
    {15, 35, 0,  30, 28},
    {20, 25, 30, 0,  18},
    {12, 17, 28, 18, 0}
};

double pheromone[N][N];

int main(void)
{
    int bestRoute[N + 1];
    double bestDistance = INFINITY;

    srand((unsigned int)time(NULL));

    // Initialize pheromones
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            pheromone[i][j] = 1.0;

    for (int iter = 0; iter < ITERATIONS; iter++)
    {
        for (int ant = 0; ant < ANTS; ant++)
        {
            int route[N + 1];
            int visited[N] = {0};
            double totalDistance = 0.0;

            // Start from location 0
            route[0] = 0;
            visited[0] = 1;

            for (int step = 1; step < N; step++)
            {
                int current = route[step - 1];
                double probability[N] = {0};
                double sum = 0.0;

                // Calculate transition probabilities
                for (int city = 0; city < N; city++)
                {
                    if (!visited[city])
                    {
                        probability[city] =
                            pow(pheromone[current][city], ALPHA) *
                            pow(1.0 / distance[current][city], BETA);

                        sum += probability[city];
                    }
                }

                // Select next location using roulette wheel
                double randomValue =
                    ((double)rand() / RAND_MAX) * sum;

                int next = -1;
                for (int city = 0; city < N; city++)
                {
                    if (!visited[city])
                    {
                        randomValue -= probability[city];

                        if (randomValue <= 0.0)
                        {
                            next = city;
                            break;
                        }
                    }
                }

                // Fallback for floating-point rounding
                if (next == -1)
                    for (int city = N - 1; city >= 0; city--)
                        if (!visited[city])
                        {
                            next = city;
                            break;
                        }

                route[step] = next;
                visited[next] = 1;
                totalDistance += distance[current][next];
            }

            // Return to starting location
            route[N] = 0;
            totalDistance += distance[route[N - 1]][0];

            // Save the best route
            if (totalDistance < bestDistance)
            {
                bestDistance = totalDistance;
                for (int i = 0; i <= N; i++)
                    bestRoute[i] = route[i];
            }

            // Deposit pheromones on this route
            for (int i = 0; i < N; i++)
            {
                int from = route[i];
                int to = route[i + 1];

                pheromone[from][to] += Q / totalDistance;
                pheromone[to][from] += Q / totalDistance;
            }
        }

        // Evaporate pheromones
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                pheromone[i][j] *= (1.0 - RHO);
    }

    // Display the best route
    printf("Best route: ");
    for (int i = 0; i <= N; i++)
        printf("%d ", bestRoute[i]);

    printf("\nTotal distance: %.2f\n", bestDistance);

    return 0;
}

