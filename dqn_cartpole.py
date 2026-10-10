"""
Enhanced CS 499 artifact: Deep Q-learning on the same CartPole physics
used in the original file.

Enhancements versus the CS 370-style tabular baseline
-----------------------------------------------------
1. ReplayBuffer (circular array) replaces the unbounded Python list.
   Insert is O(1). Memory is capped.
2. Function approximation (small two-layer network) replaces the
   discrete Q-table so continuous states do not need bucketing.
3. A lagged target network stabilizes the TD target.
4. Minibatch updates break the correlation of consecutive samples.
5. Epsilon decays, so exploration shrinks as the policy improves.

The environment class is copied (not imported) so original/ and
enhanced/ can be graded independently.
"""

import math
import random
from copy import deepcopy

from replay_buffer import ReplayBuffer


class SimpleCartPole:
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
        return list(self.state)

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
        done = abs(x) > self.x_threshold or abs(theta) > self.theta_threshold
        reward = 1.0 if not done else 0.0
        return list(self.state), reward, done


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class TinyQNetwork:
    """Two-layer perceptron implemented with plain Python lists.

    Kept dependency-free so the zip runs on any machine that has
    Python 3. Hidden width is small on purpose: CartPole state is
    only four numbers, and the point of the artifact is the algorithm
    and the buffer, not a framework demo.
    """

    def __init__(self, n_in=4, n_hidden=16, n_out=2, seed=0):
        rng = random.Random(seed)
        scale_h = 1.0 / math.sqrt(n_in)
        scale_o = 1.0 / math.sqrt(n_hidden)
        self.w1 = [
            [rng.uniform(-scale_h, scale_h) for _ in range(n_in)]
            for _ in range(n_hidden)
        ]
        self.b1 = [0.0] * n_hidden
        self.w2 = [
            [rng.uniform(-scale_o, scale_o) for _ in range(n_hidden)]
            for _ in range(n_out)
        ]
        self.b2 = [0.0] * n_out

    def forward(self, x):
        hidden = []
        for weights, bias in zip(self.w1, self.b1):
            hidden.append(max(0.0, dot(weights, x) + bias))  # ReLU
        out = []
        for weights, bias in zip(self.w2, self.b2):
            out.append(dot(weights, hidden) + bias)
        return out, hidden

    def predict(self, x):
        out, _ = self.forward(x)
        return out

    def train_step(self, states, targets, lr=0.003):
        """SGD on mean-squared error of Q-values."""
        for x, y in zip(states, targets):
            out, hidden = self.forward(x)
            d_out = [o - t for o, t in zip(out, y)]
            d_hidden = [0.0] * len(hidden)
            for j, weights in enumerate(self.w2):
                for i, w in enumerate(weights):
                    d_hidden[i] += d_out[j] * w
                self.b2[j] -= lr * d_out[j]
                for i in range(len(weights)):
                    self.w2[j][i] -= lr * d_out[j] * hidden[i]
            for i in range(len(hidden)):
                if hidden[i] <= 0:
                    continue
                self.b1[i] -= lr * d_hidden[i]
                for k in range(len(self.w1[i])):
                    self.w1[i][k] -= lr * d_hidden[i] * x[k]


def hard_update(dst, src):
    dst.w1 = deepcopy(src.w1)
    dst.b1 = deepcopy(src.b1)
    dst.w2 = deepcopy(src.w2)
    dst.b2 = deepcopy(src.b2)


def train(
    episodes=250,
    gamma=0.99,
    batch_size=32,
    buffer_capacity=2000,
    target_sync=25,
    epsilon_start=1.0,
    epsilon_end=0.05,
    seed=7,
):
    random.seed(seed)
    env = SimpleCartPole()
    policy_net = TinyQNetwork(seed=seed)
    target_net = TinyQNetwork(seed=seed + 1)
    hard_update(target_net, policy_net)
    buffer = ReplayBuffer(buffer_capacity)

    returns = []
    epsilon = epsilon_start

    for ep in range(episodes):
        state = env.reset()
        done = False
        total = 0.0
        steps = 0
        while not done and steps < 200:
            if random.random() < epsilon:
                action = random.choice([0, 1])
            else:
                q_values = policy_net.predict(state)
                action = 0 if q_values[0] >= q_values[1] else 1
            next_state, reward, done = env.step(action)
            buffer.push(state, action, reward, next_state, done)

            if len(buffer) >= batch_size:
                batch = buffer.sample(batch_size)
                states = [t.state for t in batch]
                targets = []
                for t in batch:
                    q = policy_net.predict(t.state)
                    if t.done:
                        q[t.action] = t.reward
                    else:
                        q[t.action] = t.reward + gamma * max(
                            target_net.predict(t.next_state)
                        )
                    targets.append(q)
                policy_net.train_step(states, targets)

            state = next_state
            total += reward
            steps += 1

        if (ep + 1) % target_sync == 0:
            hard_update(target_net, policy_net)
        epsilon = max(epsilon_end, epsilon * 0.985)
        returns.append(total)

    return {
        "returns": returns,
        "buffer_len": len(buffer),
        "buffer_capacity": buffer.capacity,
        "last_10_avg": sum(returns[-10:]) / 10,
        "epsilon": epsilon,
    }


if __name__ == "__main__":
    result = train()
    print("Enhanced DQN with circular replay buffer")
    print(f"  Buffer size / capacity:         {result['buffer_len']} / {result['buffer_capacity']}")
    print(f"  Last-10 episode average return: {result['last_10_avg']:.1f}")
    print(f"  Final epsilon:                  {result['epsilon']:.3f}")
    print("  Data structure: ring buffer + policy net + lagged target net")
