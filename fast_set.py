from __future__ import annotations
import numpy as np

int_size_bits=64
max_val = np.uint64((1<<int_size_bits) - 1)

class FastSet:
    def __init__(self, num_states: int, full: bool):
        if full:
            self.set_full(num_states)
        else:
            self.set_empty(num_states)

    def set_full(self, num_states: int):
        num_ints = num_states//int_size_bits
        offset = num_states%int_size_bits
        if offset != 0:
            num_ints += 1
        self.state = np.full(num_ints, max_val)
        # The bits for the last integer should not all be set
        self.state[num_ints-1] = np.uint64((1<<offset) - 1)

    def set_empty(self, num_states: int):
        num_ints = num_states//int_size_bits
        if num_states%int_size_bits != 0:
            num_ints += 1
        self.state = np.zeros(num_ints, dtype=np.uint64)

    def add(self, idx: int):
        int_index = idx//int_size_bits
        offset = idx%int_size_bits
        self.state[int_index] |= np.uint64(1<<offset)

    def union(self, other: FastSet):
        "The result becomes this array"
        np.bitwise_or(self.state, other.state, out=self.state)

    def intersection(self, other: FastSet):
        "The result becomes this array"
        np.bitwise_and(self.state, other.state, out=self.state)

    def any_satisfying(self) -> bool:
        for i in self.state:
            if i != 0:
                return True

    def __str__(self):
        "Very slow. Should not be called except in tests"
        set_states = self.get_as_list()
        return "[" + ",".join(map(str, set_states)) + "]"

    def __eq__(self, other: FastSet) -> bool:
        return np.array_equal(self.state, other.state)

    def __contains__(self, idx: int) -> bool:
        int_index = idx//int_size_bits
        offset = idx%int_size_bits
        return self.state[int_index]&np.uint64(1<<offset) != np.uint64(0)

    def get_as_list(self):
        "Very slow. Should not be called in the hot path"
        set_states = []
        for i in range(0, len(self.state)):
            for j in range(int_size_bits):
                if self.state[i]&np.uint64(1<<j) != 0:
                    set_states.append((64*i) + j)
        return set_states
