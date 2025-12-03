from Individual import Individual
from FitnessFunc import FitnessFunc
from GeneticOperators import GeneticOperators
import math
import random
import statistics
import sqlite3
import os


class GeneticAlgorithm:
    def __init__(self, user_input):
        self.user_input = user_input
        self.fitness_func = FitnessFunc.get_function(user_input.func_name)
        self.population: list[Individual] = []

        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.std_fitness_history = []

        self._selection_methods = {
            'best': GeneticOperators.selection_best,
            'roulette': GeneticOperators.selection_roulette,
            'tournament': GeneticOperators.selection_tournament
        }

        self._crossover_methods = {
            'arithmetic': GeneticOperators.crossover_arithmetic,
            'linear': GeneticOperators.crossover_linear, 
            'blend_a': GeneticOperators.crossover_blend_a, 
            'blend_a_b': GeneticOperators.crossover_blend_a_b, 
            'average': GeneticOperators.crossover_average
        }

        self._mutation_methods = {
            'uniform': GeneticOperators.mutation_uniform,
            'gaussian': GeneticOperators.mutation_gaussian
        }

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

    
    def print_population(self, epoch, connection):
        print("\n--- Current State ---")
        if self.population:
            print(f"    Population size:    {len(self.population)}")
            try:
                self.best_fit = (
                    max(individual.fitness for individual in self.population)
                    if self.user_input.optimization_method == 'max'
                    else min(individual.fitness for individual in self.population)
                )
                for ind in self.population:
                    if ind.fitness == self.best_fit:
                        phenotype = ind.phenotype
                        break

                self.insert_into_db(epoch, phenotype, self.best_fit, connection)
                cursor = connection.cursor()
                row = cursor.execute("SELECT * FROM best_fitness_history order by id desc")
                row = row.fetchone()
                if row:
                    phenotype = row[1]
                    best_fitness = row[2]
                else:
                    phenotype = 0
                    best_fitness = 0
                self.best_fitness_history.append(best_fitness)
                print(f"    Current best fitness | Phenotype: {phenotype} | Fitness: {best_fitness} | ")


            except ValueError:
                print(f"    Current best fitness:   N/A")
        
        else:
            print(" No population yet!")


    # def get_bits_per_param(self):
    #     num_space = (self.user_input.range_end - self.user_input.range_begin) * 10**self.user_input.precision + 1
    #     # (b-a) * 10^pr <= 2^m -1
    #     bits_per_param = math.ceil(math.log2(num_space))
    #     # ceil - mamy np 3.49, lepiej mieć 4 bity niż 3, wtedy zabraknie nam miejsca
    #     return int(bits_per_param)  # bo ceil zwraca float..
    

    def _init_population(self):
        """Wykonuje początkową inicjalizajcę populacji wg. parametrów z user_input."""
        self.population = []
        for _ in range(self.user_input.population_size):

            ind = Individual(
                self.user_input.range_begin,
                self.user_input.range_end,
                self.user_input.param_num,
                self.user_input.precision
            )

            self._evaluate(ind)

            self.population.append(ind)


    def _evaluate(self, individual):
        value = self.fitness_func(individual.phenotype)

        if self.user_input.optimization_method == 'min':
            fitness = value
        else:
            fitness = -value
        
        individual.fitness = round(fitness, self.user_input.precision)


    # def _selection(self):
    #     parents = []
        
    #     if self.user_input.selection_method == 'Best Selection':
    #         parents = GeneticOperators.selection_best(self.population, self.user_input.percent_best_to_select, self.user_input.optimization_method)
    #     elif self.user_input.selection_method == "Tournament Selection":
    #         parents = GeneticOperators.selection_tournament(self.population, self.user_input.tournament_size, self.user_input.percent_best_to_select, self.user_input.optimization_method)
    #     elif self.user_input.selection_method == "Roulette Selection":
    #         parents = GeneticOperators.selection_roulette(self.population, self.user_input.optimization_method, self.user_input.percent_best_to_select)
        
    #     return parents
    

    def _selection(self):
        method_name = self.user_input.selection_method
        selection_function = self._selection_methods[method_name]
        parents = selection_function(self.population, self.user_input)

        return parents
    

    def _crossover(self, parents, offspring_missing_num):
        method_name = self.user_input.cross_method
        crossover_function = self._crossover_methods[method_name]
        offspring = crossover_function(parents, self.user_input, offspring_missing_num)

        return offspring


    def _mutation(self, offspring):
        prob = self.user_input.mutation_probability
        method_name = self.user_input.mutation_method
        mutation_function = self._mutation_methods[method_name]

        offspring = mutation_function(offspring, prob)

    
    # def add_best_fit(self):
    #     best_fitness = min(individual.fitness for individual in self.population)
    #
    #     if self.user_input.optimization_method == 'max':
    #         self.best_fitness_history.append(-best_fitness)
    #     else:
    #         self.best_fitness_history.append(best_fitness)


    def add_avg_fit(self):
        if self.user_input.optimization_method == 'max':
            total = sum(-ind.fitness for ind in self.population)
        else:
            total = sum(ind.fitness for ind in self.population)
        
        avg_fit = total / len(self.population)
        self.avg_fitness_history.append(avg_fit)


    def add_std_fit(self):
        if self.user_input.optimization_method == 'max':
            actual_values = [-ind.fitness for ind in self.population]
        else:
            actual_values = [ind.fitness for ind in self.population]
        std_dev = statistics.stdev(actual_values)
        self.std_fitness_history.append(std_dev)


    def initialize_db(self):
        base_name = "data"
        num = 0

        while os.path.exists(f"./Data/{base_name}{num}.db"):
            num += 1

        file_name = f"./Data/{base_name}{num}.db"
        conn = sqlite3.connect(file_name)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS best_fitness_history (
            id INTEGER PRIMARY KEY,
            phenotype TEXT NOT NULL,
            best_fitness DECIMAL NOT NULL
        )
        """)

        return conn


    def insert_into_db(self, epoch, phenotype, fit, connection):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO best_fitness_history (id, phenotype, best_fitness) VALUES (?, ?, ?)", (epoch, str(phenotype), fit))
        connection.commit()


    def calculate(self):
        self._init_population()
        connection = self.initialize_db()

        for epoch in range(self.user_input.epochs):
            current_epoch = epoch + 1
            print("\n")
            print(f"--- Epoch {current_epoch}/{self.user_input.epochs} ---")
            new_population = []
            # selekcja elit - od razu do następnej iteracji
            elite_best_individuals = GeneticOperators.selection_best(self.population, self.user_input, elite=True)
            offspring_missing_num = self.user_input.population_size - len(elite_best_individuals)
            new_population.extend(elite_best_individuals)
            # pula rodziców do krzyżowania:
            parents = self._selection()

            offspring = self._crossover(parents, offspring_missing_num)
            mutated_offspring = self._mutation(offspring)

            for o in mutated_offspring:
                self._evaluate(o)  # !!!

            new_population.extend(mutated_offspring)
            
            self.population = new_population

            # self.add_best_fit()
            self.add_avg_fit()
            self.add_std_fit()

            self.print_population(current_epoch, connection)

        connection.close()
