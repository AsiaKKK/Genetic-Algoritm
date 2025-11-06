import random
from typing import List
from Individual import Individual
import numpy as np

class GeneticOperators:

    # --- SELEKCJA
    @staticmethod
    def selection_best(population: List[Individual], percent_best_to_select: float, optimization: str):
        reverse_order = True if optimization == 'max' else False
        sorted_population = sorted(population, key=lambda i: i.fitness, reverse=reverse_order)
        n = len(population)

        parents_population_size = int(n*percent_best_to_select)
        parents_population = sorted_population[:parents_population_size]
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

        return parents


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

        return tournament_winners

    
    # --- KRZYŻOWANIE
    @staticmethod
    def cross_one_point(parents, param_num, bits_per_param, offspring_missing_num):
        offspring = []
        num_bits = len(parents[0].chromosome)

        while len(offspring) < offspring_missing_num:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            cut_point = random.randint(1, num_bits - 1)

            child1_chr = parent1.chromosome[:cut_point] + parent2.chromosome[cut_point:]
            child2_chr = parent2.chromosome[:cut_point] + parent1.chromosome[cut_point:]
     
            offspring.append(Individual(param_num, bits_per_param, child1_chr))
            offspring.append(Individual(param_num, bits_per_param, child2_chr))

        # Odcinamy gdy mamy nieparzyście np 51 potomstwa, a potrzebujmy 50
        return offspring[:offspring_missing_num]
    

    @staticmethod
    def cross_two_point(parents, param_num, bits_per_param, offspring_missing_num):
        offspring = []
        num_bits = len(parents[0].chromosome)

        while len(offspring) < offspring_missing_num:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
  
            cut1 = random.randint(1, num_bits - 1)
            cut2 = random.randint(1, num_bits - 1)
            
            while cut1 == cut2:
                cut2 = random.randint(1, num_bits - 1)

            p1 = min(cut1, cut2)
            p2 = max(cut1, cut2)

            child1_chr = parent1.chromosome[:p1] + parent2.chromosome[p1:p2] + parent1.chromosome[p2:]
            child2_chr = parent2.chromosome[:p1] + parent1.chromosome[p1:p2] + parent2.chromosome[p2:]

            offspring.append(Individual(param_num, bits_per_param, child1_chr))
            offspring.append(Individual(param_num, bits_per_param, child2_chr))

        return offspring[:offspring_missing_num]


    @staticmethod
    def cross_homogenous(parents, prob, param_num, bits_per_param, offspring_missing_num):
        offspring = []
        num_bits = len(parents[0].chromosome)

        while len(offspring) < offspring_missing_num:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            child1_chr = []
            child2_chr = []

            for i in range(num_bits):
                alpha = random.random()

                if alpha < prob:
                    child1_chr.append(parent2.chromosome[i])
                    child2_chr.append(parent1.chromosome[i])

                else:
                    child1_chr.append(parent1.chromosome[i])
                    child2_chr.append(parent2.chromosome[i])

            offspring.append(Individual(param_num, bits_per_param, child1_chr))
            offspring.append(Individual(param_num, bits_per_param, child2_chr))

        return offspring[:offspring_missing_num]


    @staticmethod
    def cross_granular(parents, param_num, bits_per_param, offspring_missing_num):
        offspring = []
        num_bits = len(parents[0].chromosome)

        while len(offspring) < offspring_missing_num:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            child_chr = []

            for i in range(num_bits):
                alpha = random.random()

                if alpha <= 0.5:
                    child_chr.append(parent1.chromosome[i])
                
                else:
                    child_chr.append(parent2.chromosome[i])

            offspring.append(Individual(param_num, bits_per_param, child_chr))

        return offspring
    

    # --- MUTACJA
    @staticmethod
    def mutation_edge(offspring, prob):

        for o in offspring:
            alpha = random.random()

            if alpha <= prob:
                o.chromosome[-1] = 1 - o.chromosome[-1]

        return offspring


    @staticmethod
    def mutation_one_point(offspring, prob):
        num_bits = len(offspring[0].chromosome)

        for o in offspring:
            alpha = random.random()

            if alpha <= prob:
                p = random.randint(0, num_bits - 1)
            
                o.chromosome[p] = 1 - o.chromosome[p]

        return offspring


    @staticmethod
    def mutation_two_points(offspring, prob):
        num_bits = len(offspring[0].chromosome)

        for o in offspring:
            alpha = random.random()

            if alpha <= prob:
                p1 = random.randint(0, num_bits - 1)
                p2 = random.randint(0, num_bits - 1)
            
                while p1 == p2:
                    p2 = random.randint(0, num_bits - 1)
                
                o.chromosome[p1] = 1 - o.chromosome[p1]
                o.chromosome[p2] = 1 - o.chromosome[p2]

        return offspring