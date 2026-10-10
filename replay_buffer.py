"""
Circular replay buffer.

This is the data-structure enhancement over the original append-only list.

Complexity
----------
push     O(1)  overwrite the oldest slot when full
sample   O(k)  uniform sample of k transitions without scanning the whole buffer
len      O(1)
space    O(capacity)  bounded RAM, unlike the original history list
"""

from collections import namedtuple
import random

Transition = namedtuple(
    "Transition", ["state", "action", "reward", "next_state", "done"]
)


class ReplayBuffer:
    """Fixed-capacity ring buffer for experience replay."""

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data = [None] * capacity
        self._index = 0
        self._size = 0

    def push(self, state, action, reward, next_state, done):
        self._data[self._index] = Transition(
            state, action, reward, next_state, done
        )
        self._index = (self._index + 1) % self.capacity
        if self._size < self.capacity:
            self._size += 1

    def sample(self, batch_size):
        if batch_size > self._size:
            raise ValueError("batch larger than buffer")
        return random.sample(self._data[: self._size], batch_size)

    def __len__(self):
        return self._size
