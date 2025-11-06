import random
from typing import List
from Individual import Individual
import numpy as np

class GeneticOperators:

    # --- SELEKCJA
    @staticmethod
    def selection_best(population: List[Individual], percent_best_to_select: float, optimization: str):
        population.sort(key=lambda i: i.fitness, reverse=True) if optimization == 'max' else population.sort(key= lambda i: i.fitness, reverse=False)
        n = len(population)
        parents_population_size = int(n*percent_best_to_select)
        parents_population = population[:parents_population_size]
        print("Parents:", parents_population, "size:", len(parents_population))
        return parents_population


    @staticmethod
    def selection_roulette(population: List[Individual], optimization_method: str, percent_to_select: float):
        number_of_roulettes = int(len(population)*percent_to_select)

        if optimization_method == "max":
            fitness_sum = sum(ind.fitness for ind in population)
            probabilities = [abs(ind.fitness / fitness_sum) for ind in population]
        else:
            fitness_sum = sum(1 / ind.fitness for ind in population)
            probabilities = [abs((1 / ind.fitness) / fitness_sum) for ind in population]

        distributors = np.cumsum(probabilities)

        parents = []

        for _ in range(number_of_roulettes):
            random_prob = np.random.random()
            for i, cp in enumerate(distributors):
                if random_prob <= cp:
                    parents.append(population[i])
                    break

        print("Parents:", parents, "iosc:", len(parents))


    @staticmethod
    def selection_tournament(population: List['Individual'], tournament_size: int, tournament_number: int, optimization_method: str):

        population_size = len(population)
        tournament_winners = []

        for _ in range(tournament_number):
            single_tournament = []
            already_chosen = set()

            while len(single_tournament) < tournament_size:
                random_ind_num = np.random.randint(0, population_size)
                if random_ind_num not in already_chosen:
                    already_chosen.add(random_ind_num)
                    single_tournament.append(population[random_ind_num])

            if optimization_method == 'max':
                winner = max(single_tournament, key=lambda ind: ind.fitness)
            else:
                winner = min(single_tournament, key=lambda ind: ind.fitness)

            tournament_winners.append(winner)

        print("Tournament winners:", tournament_winners, "count:", len(tournament_winners))
        return tournament_winners







    
    # --- KRZYŻOWANIE
    @staticmethod
    def cross_one_point():
        pass


    @staticmethod
    def cross_two_poins():
        pass


    @staticmethod
    def cross_homogenous():
        pass


    @staticmethod
    def cross_granular():
        pass


    # --- MUTACJA
    @staticmethod
    def mutation_edge():
        pass


    @staticmethod
    def mutation_one_point():
        pass


    @staticmethod
    def mutation_two_points():
        pass