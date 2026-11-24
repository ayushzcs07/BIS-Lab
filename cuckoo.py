import random
import heapq

# PCB Routing using Cuckoo Search Algorithm

ROWS, COLS = 10, 10
START = (0, 0)
GOAL = (9, 9)

OBSTACLES = {
    (3,0), (3,1), (3,2), (3,3), (3,4),
    (3,6), (3,7), (3,8),
    (6,2), (6,3), (6,4), (6,5),
    (6,7), (6,8),
    (1,5), (2,5), (4,5), (5,5), (7,5)
}

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]


# Generate a path using randomized Dijkstra search
def generate_path(flight):
    dist = {START: 0}
    parent = {}
    pq = [(0, START)]

    while pq:
        cost, u = heapq.heappop(pq)

        if cost != dist[u]:
            continue

        if u == GOAL:
            break

        for dx, dy in DIRECTIONS:
            v = (u[0] + dx, u[1] + dy)

            if not (0 <= v[0] < ROWS and 0 <= v[1] < COLS):
                continue

            if v in OBSTACLES:
                continue

            # Randomized cost influenced by Levy flight
            weight = 1 + random.random() * 0.15 * flight
            new_cost = cost + weight

            if new_cost < dist.get(v, float('inf')):
                dist[v] = new_cost
                parent[v] = u
                heapq.heappush(pq, (new_cost, v))

    if GOAL not in parent:
        return None

    # Reconstruct path
    path = []
    cur = GOAL

    while cur != START:
        path.append(cur)
        cur = parent[cur]

    path.append(START)
    path.reverse()

    return path


# Calculate fitness: path length + penalty for turns
def fitness(path):
    turns = 0

    for i in range(2, len(path)):
        d1 = (path[i-1][0] - path[i-2][0],
              path[i-1][1] - path[i-2][1])

        d2 = (path[i][0] - path[i-1][0],
              path[i][1] - path[i-1][1])

        if d1 != d2:
            turns += 1

    length = len(path) - 1

    return length + 0.35 * turns


# Generate Levy flight (heavy-tailed random movement)
def levy_flight():
    return min(8, max(1, int(random.paretovariate(1.5))))


# Cuckoo Search
def cuckoo_search(n=12, Pa=0.25, T=30):
    random.seed(7)

    # Initialize nests randomly
    nests = [generate_path(levy_flight()) for _ in range(n)]
    nests = [p for p in nests if p is not None]

    best = min(nests, key=fitness)

    for t in range(T):

        # Select cuckoo randomly
        cuckoo = generate_path(levy_flight())

        # Select random nest
        if cuckoo is not None:
            idx = random.randrange(len(nests))

            # Replace nest if new solution is better
            if fitness(cuckoo) < fitness(nests[idx]):
                nests[idx] = cuckoo

        # Sort nests according to fitness
        nests.sort(key=fitness)

        # Abandon worst nests
        abandon = max(1, int(Pa * len(nests)))

        nests[-abandon:] = [
            generate_path(levy_flight())
            for _ in range(abandon)
        ]

        nests = [p for p in nests if p is not None]

        # Update best solution
        if nests and fitness(nests[0]) < fitness(best):
            best = nests[0]

    return best


# Display PCB grid
def display_board(path):
    board = [['.' for _ in range(COLS)] for _ in range(ROWS)]

    for r, c in OBSTACLES:
        board[r][c] = '#'

    for r, c in path:
        board[r][c] = '*'

    board[START[0]][START[1]] = 'S'
    board[GOAL[0]][GOAL[1]] = 'G'

    print("\nPCB Routing Grid:")
    for row in board:
        print(' '.join(row))


# Main program
best_path = cuckoo_search()

print("PCB Routing using Cuckoo Search")
print("Start:", START)
print("Goal :", GOAL)
print("Best Path:", best_path)
print("Path Length:", len(best_path) - 1)
print("Fitness:", round(fitness(best_path), 2))

display_board(best_path)
