"""
CS 370 original-style artifact (baseline for CS 499 Milestone Three).

Tabular Q-learning on a discretized CartPole-like environment.
Q-values live in a nested dictionary. Transitions are appended to a
Python list that grows without bound (no replay sampling).

This file is the "before" snapshot: a working algorithm that does not
yet treat memory as a first-class data structure.
"""

from collections import defaultdict
import math
import random


class SimpleCartPole:
    """Minimal CartPole physics so the artifact runs without Gym."""

    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = self.masscart + self.masspole
        self.length = 0.5
        self.polemass_length = self.masspole * self.length
        self.force_mag = 10.0
        self.tau = 0.02
        self.x_threshold = 2.4
        self.theta_threshold = 12 * 2 * math.pi / 360
        self.state = None

    def reset(self):
        self.state = [
            random.uniform(-0.05, 0.05),
            random.uniform(-0.05, 0.05),
            random.uniform(-0.05, 0.05),
            random.uniform(-0.05, 0.05),
        ]
        return tuple(self.state)

    def step(self, action):
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (
            force + self.polemass_length * theta_dot ** 2 * sintheta
        ) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length
            * (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = [x, x_dot, theta, theta_dot]
        done = (
            abs(x) > self.x_threshold
            or abs(theta) > self.theta_threshold
        )
        reward = 1.0 if not done else 0.0
        return tuple(self.state), reward, done


def discretize(state, bins=(8, 8, 8, 8)):
    """Bucket continuous observations into a hashable tuple."""
    ranges = [
        (-2.4, 2.4),
        (-3.0, 3.0),
        (-0.21, 0.21),
        (-3.5, 3.5),
    ]
    buckets = []
    for value, (low, high), n in zip(state, ranges, bins):
        clipped = max(low, min(high, value))
        ratio = (clipped - low) / (high - low)
        buckets.append(int(ratio * (n - 1)))
    return tuple(buckets)


def default_q():
    return [0.0, 0.0]


def train(episodes=250, gamma=0.99, alpha=0.1, epsilon=0.2, seed=7):
    random.seed(seed)
    env = SimpleCartPole()
    q_table = defaultdict(default_q)
    # Naive growing list — O(n) to scan, unbounded RAM
    history = []
    returns = []

    for ep in range(episodes):
        state = discretize(env.reset())
        done = False
        total = 0.0
        steps = 0
        while not done and steps < 200:
            if random.random() < epsilon:
                action = random.choice([0, 1])
            else:
                action = 0 if q_table[state][0] >= q_table[state][1] else 1
            raw_next, reward, done = env.step(action)
            next_state = discretize(raw_next)
            best_next = max(q_table[next_state])
            td_target = reward + (0.0 if done else gamma * best_next)
            q_table[state][action] += alpha * (td_target - q_table[state][action])
            history.append((state, action, reward, next_state, done))
            state = next_state
            total += reward
            steps += 1
        returns.append(total)

    return {
        "returns": returns,
        "q_states": len(q_table),
        "history_len": len(history),
        "last_10_avg": sum(returns[-10:]) / 10,
    }


if __name__ == "__main__":
    result = train()
    print("Original tabular Q-learning")
    print(f"  Distinct discrete states visited: {result['q_states']}")
    print(f"  Unbounded history length:         {result['history_len']}")
    print(f"  Last-10 episode average return:   {result['last_10_avg']:.1f}")
    print("  Data structure: dict-of-lists Q-table + append-only Python list")
