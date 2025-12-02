class UserInput:

    def __init__(self, range_begin, range_end, epochs, param_num, precision, population_size, cross_method, cross_probability,
                 inversion_probability, percent_elite_strategy, mutation_method, mutation_probability, selection_method, func_name,
                 percent_best_to_select, optimization_method, tournament_size=None):
        self.range_begin = range_begin
        self.range_end = range_end
        self.epochs = epochs
        self.param_num = param_num
        self.precision = precision
        self.population_size = population_size
        self.cross_method = cross_method
        self.cross_probability = cross_probability
        self.inversion_probability = inversion_probability
        self.percent_elite_strategy = percent_elite_strategy
        self.mutation_method = mutation_method
        self.mutation_probability = mutation_probability
        self.selection_method = selection_method
        self.func_name = func_name
        self.percent_best_to_select = percent_best_to_select
        self.optimization_method = optimization_method
        self.tournament_size = tournament_size