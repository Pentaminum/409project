import numpy as np
import matplotlib.pyplot as plt


# Epsilon-Greedy Policy
def epsilon_greedy_policy(env, state, value_function, epsilon):
    if np.random.rand() < epsilon:
        return env.action_space.sample()  # Explore
    else:
        q_values = [value_function.predict(state, action) for action in range(env.action_space.n)]
        return np.argmax(q_values)  # Exploit


# Softmax Policy
def softmax_policy(env, state, value_function, tau):
    q_values = np.array([value_function.predict(state, action) for action in range(env.action_space.n)])
    q_values -= np.max(q_values)  # Stabilize softmax
    exp_q = np.exp(q_values / tau)
    probabilities = exp_q / np.sum(exp_q)
    return np.random.choice(env.action_space.n, p=probabilities)


# Multi-Trial Runner
def run_multiple_trials(method_function, env_name, n_trials, n_episodes, **kwargs):
    all_rewards = []
    all_metrics = []

    for trial in range(n_trials):
        print(f"Running trial {trial + 1}/{n_trials}...")
        rewards, metrics = method_function(env_name, n_episodes=n_episodes, **kwargs)
        all_rewards.append(rewards)
        all_metrics.append(metrics)

    avg_rewards = np.mean(all_rewards, axis=0)
    std_rewards = np.std(all_rewards, axis=0)
    avg_metrics = np.mean(all_metrics, axis=0)
    std_metrics = np.std(all_metrics, axis=0)

    return avg_rewards, std_rewards, avg_metrics, std_metrics


# Plot Results
def plot_results(avg, std, ylabel, title, filename):
    plt.figure()
    plt.plot(avg, label="Average")
    plt.fill_between(range(len(avg)), avg - std, avg + std, alpha=0.2)
    plt.xlabel("Episode")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(filename)
    plt.close()
