from dataclasses import dataclass
from typing import Literal

# class UserInput:

#     def __init__(self, range_begin, range_end, epochs, param_num, precision, population_size, cross_method, cross_probability,
#                  inversion_probability, percent_elite_strategy, mutation_method, mutation_probability, selection_method, func_name,
#                  percent_best_to_select, optimization_method, tournament_size=None):
#         self.range_begin = range_begin
#         self.range_end = range_end
#         self.epochs = epochs
#         self.param_num = param_num
#         self.precision = precision
#         self.population_size = population_size
#         self.cross_method = cross_method
#         self.cross_probability = cross_probability
#         self.inversion_probability = inversion_probability
#         self.percent_elite_strategy = percent_elite_strategy
#         self.mutation_method = mutation_method
#         self.mutation_probability = mutation_probability
#         self.selection_method = selection_method
#         self.func_name = func_name
#         self.percent_best_to_select = percent_best_to_select
#         self.optimization_method = optimization_method
#         self.tournament_size = tournament_size


@dataclass
class UserInput:
    range_begin: float
    range_end: float
    epochs: int
    param_num: int
    precision: int
    population_size: int

    cross_probability: float
    inversion_probability: float
    mutation_probability: float
    
    percent_elite_strategy: float
    percent_best_to_select: float

    cross_method: Literal['arithmetic', 'linear', 'blend_a', 'blend_a_b', 'average']
    mutation_method: Literal['uniform', 'gaussian']
    selection_method: Literal['best', 'roulette', 'tournament']
    optimization_method: Literal['min', 'max']
    
    func_name: str
    tournament_size: int | None = None