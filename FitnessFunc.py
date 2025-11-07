import math
import numpy as np
class FitnessFunc:

    @staticmethod
    def get_function(func_name):
        if func_name == "Michalewicz":
            return FitnessFunc._michalewicz
        elif func_name == "HappyCat Function":
            return FitnessFunc._happy_cat_func
        elif func_name == "Shifted and Rotated HappyCat Function":
            return FitnessFunc._rotated_happy_cat_func
        else:
            raise ValueError(f"Nie rozpoznano funkcji celu : {func_name}")
    #
    # @staticmethod
    # def _fitness1(params: list[float]) -> float:
    #     return sum(x ** 2 + 5 for x in params)
    #
    # @staticmethod
    # def _fitness2(params: list[float]) -> float:
    #     try:
    #         return sum(x**2 + 5*x + math.log(x) for x in params)
    #     except ValueError:
    #         print(f"Error - próba obliczenia logarytmu z liczby niedodatniej w {params}")
    #         return None
    @staticmethod
    def _michalewicz(x: list[float], m: int = 10) -> float:
        x1 = np.array(x)
        ndim = len(x1)
        s = 0.0
        for i in range(ndim):
            s += math.sin(x1[i]) * pow(
                 math.sin((i + 1) * pow(x1[i], 2) / math.pi), 2 * m
            )
        return -s

    @staticmethod
    def _happy_cat_func(x: list[float], shift=0.0) -> float:
        z = np.array(x).ravel() + shift
        ndim = len(z)
        t1 = np.sum(z)
        t2 = np.sum(z ** 2)
        return np.abs(t2 - ndim) ** 0.25 + (0.5 * t2 + t1) / ndim + 0.5
    

    def _rotated_happy_cat_func(x: list[float]) -> float:
        from opfunu.cec_based import F132014
        ndim = len(x)
        func = F132014(ndim=ndim)
        return func.evaluate(x)
