from typing import List
import random
import math

class Individual:
    # def __init__(self, range_begin, range_end, precision, param_num):
    #     self.params: List[float] = [
    #         round(random.uniform(range_begin,range_end),precision)
    #         for _ in range(param_num)
    #     ]
    #     self.fitness: float = None


    def __init__(self, param_num, bits_per_param):
        self.param_num = param_num
        self.bits_per_param = bits_per_param
        self.num_bits = param_num * bits_per_param

        self.chromosome: List[int] = [
            random.randint(0, 1) for _ in range(self.num_bits)
        ]
        
        self.phenotype: List[float] = None
        self.fitness: float = None



    def __repr__(self):
        f_val = f"{self.fitness:.4f}" if self.fitness is not None else "None"

        # if len(self.params) > 5:
        #     p_val = f"[{self.params[0]:.2f}, {self.params[1]:.2f}, {self.params[2]:.2f}, ..., {self.params[-1]:.2f}]"
        # else:
        p_val = [f"{p:.2f}" for p in self.phenotype]
        #p_val = self.chromosome
        
        return f"Individual(params={p_val},   fitness={f_val})"
    

    def to_decimal(self, param: List[int]):
        suma = 0
        potega = 0

        for bit in reversed(param):
            suma += bit * 2**potega
            potega+=1
        
        return suma


    def _decode_param(self, param: List[int], range_begin, range_end):
        """Dekodujemy pojedynczy parametr (fragment binanrego chromosomu) na float."""
        # x = a + decimal(łańcuch_binarny) * (b-a)/(2^pr- 1)
        a, b = range_begin, range_end
        x = a + self.to_decimal(param) * (b - a) / (2**self.bits_per_param - 1)

        return x
    

    def get_phenotype(self, range_begin, range_end):
        if self.phenotype is not None:
            return self.phenotype
        
        a = self.chromosome
        n = self.bits_per_param
        params = [a[i:i + n] for i in range(0, len(a), n)]

        phenotype = []
        for p in params:
            phenotype.append(self._decode_param(p, range_begin, range_end))
        self.phenotype = phenotype

        print(phenotype)

        return phenotype
    

    def erase_previous_population(self):
        self.chromosome = []
        self.phenotype = []
        self.fitness = None
    