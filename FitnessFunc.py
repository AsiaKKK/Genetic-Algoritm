import math

class FitnessFunc:

    @staticmethod
    def get_function(func_name):
        if func_name == "Metoda 1":
            return FitnessFunc._fitness1
        elif func_name == "Metoda 2":
            return FitnessFunc._fitness2
        else:
            raise ValueError(f"Nie rozpoznano funkcji celu : {func_name}")
        
    @staticmethod
    def _fitness1(params: list[float]) -> float:
        return sum(x ** 2 + 5 for x in params)
    
    @staticmethod
    def _fitness2(params: list[float]) -> float:
        try:
            return sum(x**2 + 5*x + math.log(x) for x in params)
        except ValueError:
            print(f"Error - próba obliczenia logarytmu z liczby niedodatniej w {params}")
            return None
    
    # To czy mamy problem maksymalizacji czy minimalizacji ma być obsługiwane przez GeneticAlgorithm, tu funkcje są sztywno zdefiniowane i tego nie ruszamy