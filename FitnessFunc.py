import math
import numpy as np
class FitnessFunc:

    @staticmethod
    def get_function(func_name):
        if func_name == "Michalewicz":
            return FitnessFunc._michalewicz
        elif func_name == "Shifted and Rotated HappyCat Function":
            return FitnessFunc._rotated_happy_cat_func
        else:
            raise ValueError(f"Nie rozpoznano funkcji celu : {func_name}")

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
    def _rotated_happy_cat_func(x: list[float]) -> float:
        from opfunu.cec_based import F132014
        ndim = len(x)
        func = F132014(ndim=ndim)
        return func.evaluate(x)
