import numpy as np

# Grey Wolf Optimizer for Model Parameter
# and Feature Selection Optimization

np.random.seed(0)

# Generate sample dataset
X = np.random.randn(80, 5)

y = 3 * X[:, 0] - 2 * X[:, 2] + np.random.randn(80) * 0.15

N = 30 # Number of wolves
T = 150 # Maximum iterations
dim = 10 # 5 feature selection + 5 model weights

# Bounds for wolf positions
lb = np.array([-1]*5 + [-5]*5)
ub = np.array([1]*5 + [5]*5)


# Fitness function
def fitness(wolf):
    # First 5 values represent feature selection
    mask = wolf[:5] > 0

    if not mask.any():
        mask[np.argmax(wolf[:5])] = True

    # Last 5 values represent model parameters
    weights = wolf[5:]

    # Prediction using selected features
    prediction = X[:, mask] @ weights[mask]

    # Mean Squared Error
    mse = np.mean((y - prediction)**2)

    # Penalty for selecting unnecessary features
    return mse + 0.15 * mask.sum()


# Initialize wolves randomly
wolves = np.random.uniform(lb, ub, (N, dim))


# Grey Wolf Optimizer
for t in range(T):

    # Sort wolves according to fitness
    ranked = sorted(wolves, key=fitness)

    Alpha = ranked[0].copy()
    Beta = ranked[1].copy()
    Delta = ranked[2].copy()

    # Decrease a from 2 to 0
    a = 2 - 2 * t / T

    for i in range(N):

        # Calculate A and C for Alpha
        A1 = 2 * a * np.random.rand(dim) - a
        C1 = 2 * np.random.rand(dim)
        D1 = np.abs(C1 * Alpha - wolves[i])
        X1 = Alpha - A1 * D1

        # Calculate A and C for Beta
        A2 = 2 * a * np.random.rand(dim) - a
        C2 = 2 * np.random.rand(dim)
        D2 = np.abs(C2 * Beta - wolves[i])
        X2 = Beta - A2 * D2

        # Calculate A and C for Delta
        A3 = 2 * a * np.random.rand(dim) - a
        C3 = 2 * np.random.rand(dim)
        D3 = np.abs(C3 * Delta - wolves[i])
        X3 = Delta - A3 * D3

        # Update wolf position
        wolves[i] = (X1 + X2 + X3) / 3

        # Keep wolf within search boundaries
        wolves[i] = np.clip(wolves[i], lb, ub)


# Find final best wolf
best = min(wolves, key=fitness)

# Extract selected features and parameters
mask = best[:5] > 0

if not mask.any():
    mask[np.argmax(best[:5])] = True

weights = best[5:]
selected_features = np.where(mask)[0]

prediction = X[:, mask] @ weights[mask]
mse = np.mean((y - prediction)**2)


# Display output
print("Grey Wolf Optimizer - Model Parameter and Feature Selection")
print("Best Fitness:", round(fitness(best), 4))
print("Selected Features:", selected_features.tolist())
print("Optimized Model Parameters:", np.round(weights, 3))
print("Mean Squared Error:", round(mse, 4))
print("Optimization Completed")