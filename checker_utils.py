from dataclasses import dataclass

@dataclass
class CheckerOutput:
    satisfied_states: set[int]
    num_iter: dict[str,int] # Number of iterations made on a variable
