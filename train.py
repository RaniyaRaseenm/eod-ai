import numpy as np
import random
from eod_env import EODEnvironment

q_table = {}

def get_key(state):
    return (
        tuple(state["agent_position"]),
        state["current_bomb_index"] is not None,
        state["scan_done"]
    )

def train(episodes=500):
    env = EODEnvironment()
    actions = env.ACTIONS
    lr = 0.1
    gamma = 0.95
    epsilon = 1.0

    for ep in range(episodes):
        state = env.reset()
        while not state["done"]:
            key = get_key(state)
            if key not in q_table:
                q_table[key] = np.zeros(len(actions))
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = actions[np.argmax(q_table[key])]
            next_state, reward, done = env.step(action)
            next_key = get_key(next_state)
            if next_key not in q_table:
                q_table[next_key] = np.zeros(len(actions))
            idx = actions.index(action)
            q_table[key][idx] += lr * (
                reward + gamma * np.max(q_table[next_key]) - q_table[key][idx]
            )
            state = next_state
        epsilon = max(0.1, epsilon * 0.995)
        if ep % 100 == 0:
            print(f"Episode {ep} done")
    print("✅ Training complete!")
    return q_table

if __name__ == "__main__":
    train()