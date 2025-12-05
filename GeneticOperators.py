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

            alpha = random.random()

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
        offspring = []

        alpha = user_input.alpha

        rb = user_input.range_begin
        re = user_input.range_end
        pn = user_input.param_num
        pr = user_input.precision

        while len(offspring) < offspring_missing_num:
            p1 = random.choice(parents).phenotype
            p2 = random.choice(parents).phenotype

            new_ph = np.empty_like(p1)

            for i in range(pn):
                x = p1[i]
                y = p2[i]

                d = abs(x - y)

                min_val = min(x, y) - alpha * d
                max_val = max(x, y) + alpha * d

                new_ph_value = np.random.uniform(min_val, max_val)
                new_ph[i] = new_ph_value

            offspring.append(Individual(rb, re, pn, pr, phenotype=new_ph))
        
        return offspring


    @staticmethod
    def crossover_blend_a_b(parents: list[Individual], user_input, offspring_missing_num: int):
        offspring = []

        alpha = user_input.alpha
        beta = user_input.beta

        rb = user_input.range_begin
        re = user_input.range_end
        pn = user_input.param_num
        pr = user_input.precision

        while len(offspring) < offspring_missing_num:
            p1 = random.choice(parents).phenotype
            p2 = random.choice(parents).phenotype

            new_ph1 = np.empty_like(p1)
            new_ph2 = np.empty_like(p1)

            for i in range(pn):
                x = p1[i]
                y = p2[i]

                d = abs(x - y)

                min_val = min(x, y) - alpha * d
                max_val = max(x, y) + beta * d

                new_ph1[i] = np.random.uniform(min_val, max_val)
                new_ph2[i] = np.random.uniform(min_val, max_val)

            offspring.append(Individual(rb, re, pn, pr, phenotype=new_ph1))
            offspring.append(Individual(rb, re, pn, pr, phenotype=new_ph2))
        
        return offspring[:offspring_missing_num]



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
    def mutation_uniform(offspring: list[Individual], user_input):
        mutation_prob = user_input.mutation_probability
        for ind in offspring:
            if np.random.random() < mutation_prob:
                gene_idx = np.random.randint(0, ind.param_num)
                new_value = np.random.uniform(ind.range_begin, ind.range_end)
                ind.phenotype[gene_idx] = np.round(new_value, ind.precision)
        return offspring


    def mutation_gaussian(offspring: list[Individual], user_input):
        mutation_prob = user_input.mutation_probability
        for ind in offspring:
            if np.random.random() < mutation_prob:
                N = np.random.normal(size=ind.param_num)
                ind.phenotype = ind.phenotype + N
                ind.phenotype = np.clip(ind.phenotype, ind.range_begin, ind.range_end)
                ind.phenotype = np.round(ind.phenotype, ind.precision)
        return offspring
