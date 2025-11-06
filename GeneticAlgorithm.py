from typing import List
from Individual import Individual
from FitnessFunc import FitnessFunc
from GeneticOperators import GeneticOperators
import UserInput
import PlotsWindow
import math
import random

class GeneticAlgorithm:
    def __init__(self, user_input):
        self.user_input = user_input
        self.fitness_func = FitnessFunc.get_function(user_input.func_name)
        self.population: List[Individual] = []

        #self.best_fitness_history = []
        #self.avg_fitness_history = []


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
                self.best_fit = (
                    max(individual.fitness for individual in self.population)
                    if self.user_input.optimization_method == 'max'
                    else min(individual.fitness for individual in self.population)
                )
                self.phenotype = (
                    max(individual.phenotype for individual in self.population)
                    if self.user_input.optimization_method == 'max'
                    else min(individual.phenotype for individual in self.population)
                )
                print(f"    Current best fitness:   {self.best_fit}")

            except ValueError:
                print(f"    Current best fitness:   N/A")

            for individual in self.population:
                print(f"    {individual}")
        
        else:
            print(" No population yet!")


    def get_bits_per_param(self):
        num_space = (self.user_input.range_end - self.user_input.range_begin) * 10**self.user_input.precision + 1   
        # (b-a) * 10^pr <= 2^m -1
        bits_per_param = math.ceil(math.log2(num_space))    
        # ceil - mamy np 3.49, lepiej mieć 4 bity niż 3, wtedy zabraknie nam miejsca
        return int(bits_per_param)  # bo ceil zwraca float..
    

    def _init_population(self):
        """Wykonuje początkową inicjalizajcę populacji wg. parametrów z user_input."""
        self.population = []
        for _ in range(self.user_input.population_size):

            ind = Individual(
                self.user_input.param_num,
                self.get_bits_per_param(),
            )

            self._evaluate(ind)

            self.population.append(ind)


    def _evaluate(self, individual):
        value = self.fitness_func(individual.get_phenotype(
            self.user_input.range_begin, 
            self.user_input.range_end)
            )

        if self.user_input.optimization_method == 'min':
            fitness = value
        else:
            fitness = -value
        
        individual.fitness = round(fitness, self.user_input.precision)

    def _selection(self):
        parents = []
        
        if self.user_input.selection_method == 'Best Selection':
            parents = GeneticOperators.selection_best(self.population, self.user_input.percent_best_to_select, self.user_input.optimization_method)
        elif self.user_input.selection_method == "Tournament Selection":
            parents = GeneticOperators.selection_tournament(self.population, self.user_input.tournament_size, self.user_input.percent_best_to_select, self.user_input.optimization_method)
        elif self.user_input.selection_method == "Roulette Selection":
            parents = GeneticOperators.selection_roulette(self.population, self.user_input.optimization_method, self.user_input.percent_best_to_select)
        
        return parents
    

    def _crossover(self, parents, offspring_missing_num):
        bits_per_param = self.get_bits_per_param()

        if self.user_input.cross_method == 'One Point':
            offspring = GeneticOperators.cross_one_point(parents, self.user_input.param_num, bits_per_param, offspring_missing_num)

        elif self.user_input.cross_method == 'Two Point':
            offspring = GeneticOperators.cross_two_point(parents, self.user_input.param_num, bits_per_param, offspring_missing_num)

        elif self.user_input.cross_method == 'Homogenius':
            offspring = GeneticOperators.cross_homogenous(parents, self.user_input.cross_probability,self.user_input.param_num, bits_per_param, offspring_missing_num)

        elif self.user_input.cross_method == 'Granular':
            offspring = GeneticOperators.cross_granular(parents, self.user_input.param_num, bits_per_param, offspring_missing_num)

        return offspring

    
    def _mutation(self, offspring):
        if self.user_input.mutation_method == 'Edge':
            offspring = GeneticOperators.mutation_edge(offspring, self.user_input.mutation_probability)

        elif self.user_input.mutation_method == 'One Point':
            offspring = GeneticOperators.mutation_one_point(offspring, self.user_input.mutation_probability)

        elif self.user_input.mutation_method == 'Two Points':
            offspring = GeneticOperators.mutation_two_points(offspring, self.user_input.mutation_probability)

        return offspring

    
    def calculate(self):
        self._init_population()

        for epoch in range(self.user_input.epochs):
            print(f"--- Epoch {epoch + 1}/{self.user_input.epochs} ---")
            new_population =[]
            # selekcja elit - od razu do następnej iteracji
            elite_best_individuals = GeneticOperators.selection_best(self.population,self.user_input.percent_elite_strategy, self.user_input.optimization_method)
            offspring_missing_num = self.user_input.population_size - len(elite_best_individuals)
            new_population.extend(elite_best_individuals)
            # pula rodziców do krzyżowania:
            parents = self._selection()
                
            # print("PARENTS:")
            # for p in parents:
            #     print(p)
            # print(f"SIZE: {len(parents)}")

            offspring = self._crossover(parents, offspring_missing_num)
            mutated_offspring = self._mutation(offspring)

            #print("\nOFFSPRING AFTER MUTATION:")
            for o in mutated_offspring:
                self._evaluate(o)  # !!!
            #     print(o)
            # print(f"SIZE: {len(mutated_offspring)}")

            new_population.extend(mutated_offspring)
            self.population = new_population

            # print("\n\nNEW POPULATION:")
            # for i in new_population:
            #     print(i)
            # print(f"SIZE: {len(new_population)}")
            self.print_population()
