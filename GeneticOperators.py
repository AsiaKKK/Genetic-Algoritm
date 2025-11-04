import random
from typing import List
from Individual import Individual

class GeneticOperators:

    # --- SELEKCJA
    @staticmethod
    def selection_best(population: List[Individual], percent_best_to_select):
        pass


    @staticmethod
    def selection_roulette():
        pass


    @staticmethod
    def selection_tournament(population: List[Individual], tournament_size):
        pass

    
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