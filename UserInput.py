from dataclasses import dataclass
from typing import Literal

@dataclass
class UserInput:
    range_begin: float
    range_end: float
    epochs: int
    param_num: int
    precision: int
    population_size: int

    alpha: float
    beta: float
    mutation_probability: float
    
    percent_elite_strategy: float
    percent_best_to_select: float

    cross_method: Literal['arithmetic', 'linear', 'blend_a', 'blend_a_b', 'average']
    mutation_method: Literal['uniform', 'gaussian']
    selection_method: Literal['best', 'roulette', 'tournament']
    optimization_method: Literal['min', 'max']
    
    func_name: str
    tournament_size: int | None = None