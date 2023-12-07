from dataclasses import dataclass
import time

from fast_set import FastSet

@dataclass
class CheckerOutput:
    satisfied_states: FastSet
    num_iter: dict[str,int] # Number of iterations made on a variable
    running_time_millis: int

def get_time() -> int:
    return round(time.time() * 1000)
