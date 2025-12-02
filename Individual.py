import random
from dataclasses import dataclass, field

@dataclass
class Individual:
    range_begin: float
    range_end: float
    param_num: int
    precision: int

    phenotype: list[float] | None = None
    fitness: float = field(init=False, default=None)

    def __post_init__(self):
        if self.phenotype is None:
            self.phenotype = [
                round(random.uniform(self.range_begin, self.range_end), self.precision)
                for _ in range(self.param_num)
            ]

    # def __init__(self, param_num, bits_per_param, chromosome: list[int] = None):
    #     self.param_num = param_num #liczba parametrow
    #     self.bits_per_param = bits_per_param #liczba genow dla jednogo parametru w reprezentacji binarnej
    #     self.num_bits = param_num * bits_per_param #liczba wszystkich genow
    #
    #     if chromosome:
    #         self.chromosome: list[int] = chromosome
    #     else:
    #         self.chromosome: list[int] = [
    #             random.randint(0, 1) for _ in range(self.num_bits)
    #         ]
    #
    #     self.phenotype: list[float] = None
    #     self.fitness: float = None


    # def __repr__(self):
    #     f_val = f"{self.fitness}" if self.fitness is not None else "None"
    #     p_val = [f"{p}" for p in self.phenotype]
    #     return f"Individual(params={p_val},   fitness={f_val})"
    #

    # def to_decimal(self, param: list[int]):
    #     suma = 0
    #     potega = 0
    #
    #     for bit in reversed(param):
    #         suma += bit * 2**potega
    #         potega+=1
    #
    #     return suma
    #
    #
    # def _decode_param(self, param: list[int], range_begin, range_end, precision):
    #     """Dekodujemy pojedynczy parametr (fragment binanrego chromosomu) na float."""
    #     # x = a + decimal(łańcuch_binarny) * (b-a)/(2^pr- 1)
    #     a, b = range_begin, range_end
    #     x = round(a + self.to_decimal(param) * (b - a) / (2**self.bits_per_param - 1), precision)#dodac zaokraglenie do precyzji
    #
    #     return x
    #

    # def get_phenotype(self, range_begin, range_end, precision):
    #     if self.phenotype is not None:
    #         return self.phenotype
    #
    #     a = self.chromosome
    #     n = self.bits_per_param
    #     params = [a[i:i + n] for i in range(0, len(a), n)]
    #
    #     phenotype = []
    #     for p in params:
    #         phenotype.append(self._decode_param(p, range_begin, range_end, precision))
    #     self.phenotype = phenotype
    #
    #     #print(phenotype)
    #
    #     return phenotype