import random

# Subjects and their teachers
subjects = {
    "DSA": "Teacher1",
    "DBMS": "Teacher2",
    "OS": "Teacher3",
    "CN": "Teacher4",
    "AI": "Teacher5",
    "Maths": "Teacher6"
}

days = 5
periods = 6
population_size = 10
generations = 100
mutation_rate = 0.1


# Create a random timetable
def create_chromosome():
    timetable = []

    subject_list = list(subjects.keys())

    for i in range(days * periods):
        timetable.append(random.choice(subject_list))

    return timetable


# Calculate fitness
def fitness(timetable):

    conflicts = 0

    # Check teacher conflicts
    for day in range(days):
        teachers = []

        for period in range(periods):
            index = day * periods + period
            subject = timetable[index]
            teacher = subjects[subject]

            if teacher in teachers:
                conflicts += 1

            teachers.append(teacher)

    # Check if same subject occurs more than once in a day
    for day in range(days):
        daily_subjects = []

        for period in range(periods):
            index = day * periods + period
            subject = timetable[index]

            if subject in daily_subjects:
                conflicts += 1

            daily_subjects.append(subject)

    # Higher fitness = better timetable
    return 1 / (1 + conflicts)


# Selection
def selection(population):
    population.sort(key=fitness, reverse=True)

    # Select best two chromosomes
    return population[0], population[1]


# Crossover
def crossover(parent1, parent2):

    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


# Mutation
def mutation(chromosome):

    if random.random() < mutation_rate:
        position = random.randint(0, len(chromosome) - 1)
        chromosome[position] = random.choice(list(subjects.keys()))

    return chromosome


# Initial population
population = []

for i in range(population_size):
    population.append(create_chromosome())


# Genetic Algorithm
for generation in range(generations):

    new_population = []

    while len(new_population) < population_size:

        parent1, parent2 = selection(population)

        child1, child2 = crossover(parent1, parent2)

        child1 = mutation(child1)
        child2 = mutation(child2)

        new_population.append(child1)
        new_population.append(child2)

    population = new_population[:population_size]


# Find best timetable
best_timetable = max(population, key=fitness)

print("\nFINAL COLLEGE TIMETABLE")
print("-----------------------")

for day in range(days):

    print(f"\nDay {day + 1}:")

    for period in range(periods):

        index = day * periods + period

        print(
            f"Period {period + 1}: {best_timetable[index]}"
        )

print("\nFitness:", fitness(best_timetable))
