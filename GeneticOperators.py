import random
from Individual import Individual
from FitnessFunc import FitnessFunc
import numpy as np

class GeneticOperators:
    # --- SELEKCJA
    @staticmethod
    def selection_best(population: list[Individual], user_input, elite: bool = False):
        optimization = user_input.optimization_method
        if elite:
            percent_best = user_input.percent_elite_strategy
        else: 
            percent_best = user_input.percent_best_to_select


        reverse_order = True if optimization == 'max' else False
        sorted_population = sorted(population, key=lambda i: i.fitness, reverse=reverse_order)
        n = len(population)

        parents_population_size = int(n*percent_best)
        parents = sorted_population[:parents_population_size]
        return parents


    
    @staticmethod
    def selection_roulette(population: list[Individual], user_input):
        optimization = user_input.optimization_method
        percent_to_select = user_input.percent_best_to_select

        number_of_roulettes = int(len(population)*percent_to_select)

        if optimization == "max":
            fitness_sum = sum(ind.fitness for ind in population)
            probabilities = [
                abs((ind.fitness if ind.fitness != 0 else 0.001) / fitness_sum)
                for ind in population
            ]
        else:
            fitness_sum = sum((1 / ind.fitness) if ind.fitness != 0 else (1 / 0.001) for ind in population)
            probabilities = [
                abs(((1 / ind.fitness) if ind.fitness != 0 else (1 / 0.001)) / fitness_sum)
                for ind in population
            ]

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
    def selection_tournament(population: list[Individual], user_input):
        tournament_size = user_input.tournament_size
        tournament_number = user_input.percent_best_to_select
        optimization = user_input.optimization_method

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

            if optimization == 'max':
                winner = max(single_tournament, key=lambda ind: ind.fitness)
            else:
                winner = min(single_tournament, key=lambda ind: ind.fitness)

            tournament_winners.append(winner)

        return tournament_winners

    
    # --- KRZYŻOWANIE
    @staticmethod
    def crossover_arithmetic(parents: list[Individual], user_input, offspring_missing_num: int) -> list[Individual]:
        offspring = []

        rb = user_input.range_begin
        re = user_input.range_end
        pn = user_input.param_num
        pr = user_input.precision

        while len(offspring) < offspring_missing_num:
            x = random.choice(parents).phenotype
            y = random.choice(parents).phenotype

            alpha = random.rand()

            x_new = alpha * x + (1 - alpha) * y
            y_new = alpha * y + (1 - alpha) * x

            offspring.append(Individual(rb, re, pn, pr, phenotype=x_new))
            offspring.append(Individual(rb, re, pn, pr, phenotype=y_new))

        return offspring[:offspring_missing_num]


    @staticmethod
    def crossover_linear(parents: list[Individual], user_input, offspring_missing_num: int):
        def evaluate(phenotype: np.ndarray) -> float:
            fitness_func = FitnessFunc.get_function(user_input.func_name)
            value = fitness_func(phenotype)

            if user_input.optimization_method == 'min':
                fitness = value
            else:
                fitness = -value
        
            return round(fitness, user_input.precision)


        offspring = []

        rb = user_input.range_begin
        re = user_input.range_end
        pn = user_input.param_num
        pr = user_input.precision

        while len(offspring) < offspring_missing_num:
            x = random.choice(parents).phenotype
            y = random.choice(parents).phenotype

            Z = 0.5 * x + 0.5 * y
            V = 1.5 * x - 0.5 * y
            W = -0.5 * x + 1.5 * y

            candidates = [
                (Z, evaluate(Z)),
                (V, evaluate(V)),
                (W, evaluate(W))
            ]

            candidates.sort(key=lambda x: x[1])

            best = [candidates[0][0], candidates[1][0]]
            for b in best:
                offspring.append(Individual(rb, re, pn, pr, phenotype=b))

        return offspring[:offspring_missing_num]


    @staticmethod
    def crossover_blend_a(parents: list[Individual], user_input, offspring_missing_num: int):
        pass

    @staticmethod
    def crossover_blend_a_b(parents: list[Individual], user_input, offspring_missing_num: int):
        pass

    @staticmethod
    def crossover_average(parents: list[Individual], user_input, offspring_missing_num: int):
        offspring = []

        rb = user_input.range_begin
        re = user_input.range_end
        pn = user_input.param_num
        pr = user_input.precision

        while len(offspring) < offspring_missing_num:
            x = random.choice(parents).phenotype
            y = random.choice(parents).phenotype

            new = (x + y) / 2

            offspring.append(Individual(rb, re, pn, pr, phenotype=new))

        return offspring


    # --- MUTACJA
    def mutation_uniform(offspring: list[Individual], prob: float):
        pass

    def mutation_gaussian(offspring: list[Individual], prob: float):
        pass

    # @staticmethod
    # def cross_one_point(parents, param_num, bits_per_param, offspring_missing_num):
    #     offspring = []
    #     num_bits = len(parents[0].chromosome)

    #     while len(offspring) < offspring_missing_num:
    #         parent1 = random.choice(parents)
    #         parent2 = random.choice(parents)

    #         cut_point = random.randint(1, num_bits - 1)

    #         child1_chr = parent1.chromosome[:cut_point] + parent2.chromosome[cut_point:]
    #         child2_chr = parent2.chromosome[:cut_point] + parent1.chromosome[cut_point:]
     
    #         offspring.append(Individual(param_num, bits_per_param, child1_chr))
    #         offspring.append(Individual(param_num, bits_per_param, child2_chr))

    #     # Odcinamy gdy mamy nieparzyście np 51 potomstwa, a potrzebujmy 50
    #     return offspring[:offspring_missing_num]
    

    # @staticmethod
    # def cross_two_point(parents, param_num, bits_per_param, offspring_missing_num):
    #     offspring = []
    #     num_bits = len(parents[0].chromosome)

    #     while len(offspring) < offspring_missing_num:
    #         parent1 = random.choice(parents)
    #         parent2 = random.choice(parents)
  
    #         cut1 = random.randint(1, num_bits - 1)
    #         cut2 = random.randint(1, num_bits - 1)
            
    #         while cut1 == cut2:
    #             cut2 = random.randint(1, num_bits - 1)

    #         p1 = min(cut1, cut2)
    #         p2 = max(cut1, cut2)

    #         child1_chr = parent1.chromosome[:p1] + parent2.chromosome[p1:p2] + parent1.chromosome[p2:]
    #         child2_chr = parent2.chromosome[:p1] + parent1.chromosome[p1:p2] + parent2.chromosome[p2:]

    #         offspring.append(Individual(param_num, bits_per_param, child1_chr))
    #         offspring.append(Individual(param_num, bits_per_param, child2_chr))

    #     return offspring[:offspring_missing_num]


    # @staticmethod
    # def cross_homogenous(parents, prob, param_num, bits_per_param, offspring_missing_num):
    #     offspring = []
    #     num_bits = len(parents[0].chromosome)

    #     while len(offspring) < offspring_missing_num:
    #         parent1 = random.choice(parents)
    #         parent2 = random.choice(parents)

    #         child1_chr = []
    #         child2_chr = []

    #         for i in range(num_bits):
    #             alpha = random.random()

    #             if alpha < prob:
    #                 child1_chr.append(parent2.chromosome[i])
    #                 child2_chr.append(parent1.chromosome[i])

    #             else:
    #                 child1_chr.append(parent1.chromosome[i])
    #                 child2_chr.append(parent2.chromosome[i])

    #         offspring.append(Individual(param_num, bits_per_param, child1_chr))
    #         offspring.append(Individual(param_num, bits_per_param, child2_chr))

    #     return offspring[:offspring_missing_num]


    # @staticmethod
    # def cross_granular(parents, param_num, bits_per_param, offspring_missing_num):
    #     offspring = []
    #     num_bits = len(parents[0].chromosome)

    #     while len(offspring) < offspring_missing_num:
    #         parent1 = random.choice(parents)
    #         parent2 = random.choice(parents)

    #         child_chr = []

    #         for i in range(num_bits):
    #             alpha = random.random()

    #             if alpha <= 0.5:
    #                 child_chr.append(parent1.chromosome[i])
                
    #             else:
    #                 child_chr.append(parent2.chromosome[i])

    #         offspring.append(Individual(param_num, bits_per_param, child_chr))

    #     return offspring
    

    # # --- MUTACJA
    # @staticmethod
    # def mutation_edge(offspring, prob):

    #     for o in offspring:
    #         alpha = random.random()

    #         if alpha <= prob:
    #             o.chromosome[-1] = 1 - o.chromosome[-1]

    #     return offspring


    # @staticmethod
    # def mutation_one_point(offspring, prob):
    #     num_bits = len(offspring[0].chromosome)

    #     for o in offspring:
    #         alpha = random.random()

    #         if alpha <= prob:
    #             p = random.randint(0, num_bits - 1)
            
    #             o.chromosome[p] = 1 - o.chromosome[p]

    #     return offspring


    # @staticmethod
    # def mutation_two_points(offspring, prob):
    #     num_bits = len(offspring[0].chromosome)

    #     for o in offspring:
    #         alpha = random.random()

    #         if alpha <= prob:
    #             p1 = random.randint(0, num_bits - 1)
    #             p2 = random.randint(0, num_bits - 1)
            
    #             while p1 == p2:
    #                 p2 = random.randint(0, num_bits - 1)
                
    #             o.chromosome[p1] = 1 - o.chromosome[p1]
    #             o.chromosome[p2] = 1 - o.chromosome[p2]

    #     return offspring