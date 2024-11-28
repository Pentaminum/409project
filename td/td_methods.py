import numpy as np

# TD(0) Class
class TD:
    def __init__(self, n_features, n_actions, alpha=0.01, gamma=0.99):
        self.w = np.zeros((n_actions, n_features))  # Separate weights for each action
        self.alpha = alpha
        self.gamma = gamma

    def predict(self, state, action):
        return np.dot(self.w[action], state)  # Predict Q-value for a specific action

    def update(self, state, action, reward, next_state, next_action):
        # TD error
        delta = reward + self.gamma * self.predict(next_state, next_action) - self.predict(state, action)
        self.w[action] += self.alpha * delta * state


# GTD Class
class GradientTD:
    def __init__(self, n_features, n_actions, alpha=0.01, beta=0.005, gamma=0.99):
        self.w = np.zeros((n_actions, n_features))  # Main weights
        self.theta = np.zeros((n_actions, n_features))  # Auxiliary weights
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def predict(self, state, action):
        return np.dot(self.w[action], state)

    def update(self, state, action, reward, next_state, next_action):
        delta = reward + self.gamma * self.predict(next_state, next_action) - self.predict(state, action)
        self.theta[action] += self.beta * (delta * state - np.dot(state, self.theta[action]) * state)
        self.w[action] += self.alpha * (np.dot(state, self.theta[action]) * state)

    def calculate_mspbe(self, state, reward, next_state, action, next_action):
        td_error = reward + self.gamma * self.predict(next_state, next_action) - self.predict(state, action)
        projection_error = td_error - np.dot(state, self.theta[action])
        return projection_error ** 2


# Proximal Gradient TD Class
class ProximalTD:
    def __init__(self, n_features, n_actions, alpha=0.01, lambd=0.05, gamma=0.99):
        self.w = np.zeros((n_actions, n_features))
        self.alpha = alpha
        self.lambd = lambd
        self.gamma = gamma

    def predict(self, state, action):
        return np.dot(self.w[action], state)

    def update(self, state, action, reward, next_state, next_action):
        delta = reward + self.gamma * self.predict(next_state, next_action) - self.predict(state, action)
        grad = delta * state
        self.w[action] += self.alpha * grad
        self.w[action] = np.sign(self.w[action]) * np.maximum(np.abs(self.w[action]) - self.alpha * self.lambd, 0)

    def calculate_sparsity(self):
        return np.sum(np.abs(self.w) < 1e-3) / self.w.size  # Proportion of near-zero weights
