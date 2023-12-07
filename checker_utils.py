from dataclasses import dataclass
import time

@dataclass
class CheckerOutput:
    satisfied_states: set[int]
    num_iter: dict[str,int] # Number of iterations made on a variable
    running_time_millis: int

def get_time() -> int:
    return round(time.time() * 1000)
