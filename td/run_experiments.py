import numpy as np
from td.td_methods import TD, GradientTD, ProximalTD
from td.utils import epsilon_greedy_policy, softmax_policy, run_multiple_trials, plot_results

# Define TD(0), GTD, and Proximal Gradient functions (similar to earlier examples but with metrics tracking)
def td_learning(env_name, n_episodes=500, alpha=0.01, gamma=0.99, epsilon=0.1):
    import gym
    env = gym.make(env_name)
    n_features = env.observation_space.shape[0]
    n_actions = env.action_space.n
    agent = TD(n_features, n_actions, alpha, gamma)
    rewards = []
    msbe_log = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        state = np.array(state)
        total_reward = 0
        done = False

        while not done:
            # Epsilon-greedy action selection
            action = epsilon_greedy_policy(env, state, agent, epsilon)
            next_state, reward, done, truncated, _ = env.step(action)
            next_state = np.array(next_state)
            next_action = epsilon_greedy_policy(env, next_state, agent, epsilon)
            
            # TD(0) update
            agent.update(state, action, reward, next_state, next_action)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        # Track MSBE (even though TD doesn't explicitly optimize it)
        msbe = np.mean(
            [(reward + gamma * agent.predict(state, action) - agent.predict(state, action)) ** 2
             for action in range(n_actions)]
        )
        msbe_log.append(msbe)

    env.close()
    return rewards, msbe_log

def gtd_learning(env_name, n_episodes=500, alpha=0.01, beta=0.005, gamma=0.99, tau=1.0):
    import gym
    env = gym.make(env_name)
    n_features = env.observation_space.shape[0]
    n_actions = env.action_space.n
    agent = GradientTD(n_features, n_actions, alpha, beta, gamma)
    rewards = []
    mspbe_log = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        state = np.array(state)
        total_reward = 0
        done = False

        while not done:
            # Softmax action selection
            action = softmax_policy(env, state, agent, tau)
            next_state, reward, done, truncated, _ = env.step(action)
            next_state = np.array(next_state)
            next_action = softmax_policy(env, next_state, agent, tau)
            
            # GTD update
            agent.update(state, action, reward, next_state, next_action)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        # Track MSPBE
        mspbe = agent.calculate_mspbe(state, reward, next_state, action, next_action)
        mspbe_log.append(mspbe)

    env.close()
    return rewards, mspbe_log

def proximal_learning(env_name, n_episodes=500, alpha=0.01, lambd=0.05, gamma=0.99, tau=1.0):
    import gym
    env = gym.make(env_name)
    n_features = env.observation_space.shape[0]
    n_actions = env.action_space.n
    agent = ProximalTD(n_features, n_actions, alpha, lambd, gamma)
    rewards = []
    sparsity_log = []

    for episode in range(n_episodes):
        state, _ = env.reset()
        state = np.array(state)
        total_reward = 0
        done = False

        while not done:
            # Softmax action selection
            action = softmax_policy(env, state, agent, tau)
            next_state, reward, done, truncated, _ = env.step(action)
            next_state = np.array(next_state)
            next_action = softmax_policy(env, next_state, agent, tau)
            
            # Proximal Gradient TD update
            agent.update(state, action, reward, next_state, next_action)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        # Track sparsity (proportion of near-zero weights)
        sparsity = agent.calculate_sparsity()
        sparsity_log.append(sparsity)

    env.close()
    return rewards, sparsity_log


if __name__ == "__main__":
    n_trials = 5
    n_episodes = 500

    # TD(0)
    avg_rewards_td, std_rewards_td, avg_metrics_td, std_metrics_td = run_multiple_trials(
        td_learning, "MountainCar-v0", n_trials=n_trials, n_episodes=n_episodes, alpha=0.01, gamma=0.99, epsilon=0.1
    )
    plot_results(avg_rewards_td, std_rewards_td, "Total Reward", "TD(0) Average Reward", "plots/td_avg_rewards.png")

    # GTD
    avg_rewards_gtd, std_rewards_gtd, avg_metrics_gtd, std_metrics_gtd = run_multiple_trials(
        gtd_learning, "MountainCar-v0", n_trials=n_trials, n_episodes=n_episodes, alpha=0.01, beta=0.005, gamma=0.99, tau=1.0
    )
    plot_results(avg_rewards_gtd, std_rewards_gtd, "Total Reward", "GTD Average Reward", "plots/gtd_avg_rewards.png")

    # Proximal Gradient TD
    avg_rewards_prox, std_rewards_prox, avg_metrics_prox, std_metrics_prox = run_multiple_trials(
        proximal_learning, "MountainCar-v0", n_trials=n_trials, n_episodes=n_episodes, alpha=0.01, lambd=0.05, gamma=0.99, tau=1.0
    )
    plot_results(avg_rewards_prox, std_rewards_prox, "Total Reward", "Proximal Gradient Average Reward", "plots/proximal_avg_rewards.png")
