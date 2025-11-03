from typing import List
import random

class Individual:
    def __init__(self, range_begin, range_end, precision, param_num):
        self.params: List[float] = [
            round(random.uniform(range_begin,range_end),precision)
            for _ in range(param_num)
        ]
        self.fitness: float = None

    def __repr__(self):
        f_val = f"{self.fitness:.4f}" if self.fitness is not None else "None"

        # if len(self.params) > 5:
        #     p_val = f"[{self.params[0]:.2f}, {self.params[1]:.2f}, {self.params[2]:.2f}, ..., {self.params[-1]:.2f}]"
        # else:
        p_val = [f"{p:.2f}" for p in self.params]
        
        return f"Individual(params={p_val},   fitness={f_val})"
    