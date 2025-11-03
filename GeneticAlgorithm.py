from typing import List
from Individual import Individual
from FitnessFunc import FitnessFunc
from GeneticOperators import GeneticOperators

class GeneticAlgorithm:
    def __init__(self, user_input):
        self.user_input = user_input
        self.fitness_func = FitnessFunc.get_function(user_input.func_name)
        self.population: List[Individual] = []

        self.best_fitness_history = []
        self.avg_fitness_history = []


    def __repr__(self):
        if not self.user_input:
            return f"--- Genetic Algorithm not initialized! ---"
        
        tournament_line = ""
        if self.user_input.tournament_size is not None:
            tournament_line = f"    Tournament size:    {self.user_input.tournament_size}\n"

        return f"""--- Genetic Algorithm Configuration ---
    Problem:            {self.user_input.optimization_method} {self.user_input.func_name}
    Range:              [{self.user_input.range_begin}, {self.user_input.range_end}]
    Epochs:             {self.user_input.epochs}
    Population:         {self.user_input.population_size}
    Num of parameters:  {self.user_input.param_num} per individual
    Precision:          {self.user_input.precision}
    Selection:          {self.user_input.selection_method}
{tournament_line}    Best to select:     {self.user_input.percent_best_to_select}
    Crossover:          {self.user_input.cross_method} (p = {self.user_input.cross_probability})
    Mutation:           {self.user_input.mutation_method} (p = {self.user_input.mutation_probability})
    Inversion prob:     {self.user_input.inversion_probability}
    Elite strategy:     {self.user_input.percent_elite_strategy}"""

    
    def print_population(self):
        print("\n--- Current State ---")
        if self.population:
            print(f"    Population size:    {len(self.population)}")
            try:
                best_fit = max(ind.fitness for ind in self.population)
                print(f"    Current best fitness:   {best_fit}")
            except ValueError:
                print(f"    Current best fitness:   N/A")

            for ind in self.population:
                print(f"    {ind}")
        
        else:
            print(" No population yet!")


    def _init_population(self):
        """Wykonuje początkową inicjalizajcę populacji wg. parametrów z user_input."""
        self.population = []
        for i in range(self.user_input.population_size):
            ind = Individual(
                self.user_input.range_begin,
                self.user_input.range_end,
                self.user_input.precision,
                self.user_input.param_num
            )

            self._evaluate(ind)

            self.population.append(ind)


    def _evaluate(self, individual):
        value = self.fitness_func(individual.params)

        if self.user_input.optimization_method == 'min':
            fitness = value
        
        else:
            fitness = -value
        
        individual.fitness = round(fitness, self.user_input.precision)


    def _selection(self):
        parents =[]

        if self.user_input.selection_method == "Tournament Selection":
            for _ in range(self.user_input.population_size):
                selected = GeneticOperators.selection_tournament(self.population, self.user_input.tournament_size)
                parents.append(selected)
            
        return parents

    
    def calculate(self):
        self._init_population()

        for epoch in range(self.user_input.epochs):
            print(f"--- Epoch {epoch + 1}/{self.user_input.epochs} ---")

            parents = self._selection()
            offspring = []
        
        # epochs
        # selection
        # crossover
        # mutation
    
