from typing import List

class Individual:
    def __init__(self, params: List[float]):
        self.params: List[float] = params
        self.fitness: float = None

    def __repr__(self):
        f_val = f"{self.fitness:.4f}" if self.fitness is not None else "None"
        p_val = [f"{p:.2f}" for p in self.params]
        return f"Individual(params={p_val}, fitness={f_val})"