import random
import numpy as np
from dataclasses import dataclass, field

@dataclass
class Individual:
    range_begin: float
    range_end: float
    param_num: int
    precision: int

    phenotype: np.ndarray | None = None
    fitness: float = field(init=False, default=None)

    def __post_init__(self):
        if self.phenotype is None:
            self.phenotype = np.round(
                np.random.uniform(self.range_begin, self.range_end, self.param_num),
                self.precision
            )
        
        self.phenotype = np.clip(self.phenotype, self.range_begin, self.range_end)
        self.phenotype = np.round(self.phenotype, self.precision)


    def __repr__(self):
        f_val = f"{self.fitness}" if self.fitness is not None else "None"
        p_val = [f"{p}" for p in self.phenotype]
        return f"Individual(params={p_val},   fitness={f_val})"
