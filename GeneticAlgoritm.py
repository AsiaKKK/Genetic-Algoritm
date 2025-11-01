import math
import random

class GeneticAlgorithm:

    def fitness1(self, params, optimizationMethod):
        if optimizationMethod == 'min':
            result = sum(x ** 2 + 5 for x in params)
        else:
            result = -sum(x ** 2 + 5 for x in params)
        return result
        #testowa funkcja ZAMIENIC NA TO CO WYBIERZEMY

    def fitness2(self, params, optimizationMethod):
        return sum(x**2+5*x+math.log(x) for x in params)
        if optimizationMethod == 'min':
            result = sum(x**2+5*x+math.log(x) for x in params)
        else:
            result = -sum(x**2+5*x+math.log(x) for x in params)
        return result
        #testowa funkcja ZAMIENIC NA TO CO WYBIERZEMY

    def initIndividual(self, rangeBegin, rangeEnd, precision, paramNum):
        individual = []
        for i in range(paramNum):
            individual.append(round(random.uniform(rangeBegin,rangeEnd),precision))
        return individual

    def initPopulation(self, popSize, rangeBegin, rangeEnd, precision, paramNum, funcToCalc, optimizationMethod):
        population = []
        for i in range(popSize):
            ind = self.initIndividual(rangeBegin, rangeEnd, precision, paramNum)
            print(f" Osobnik nr {i+1} {ind}")
            if(funcToCalc == "Metoda 1"):
                result = self.fitness1(ind, optimizationMethod)
            else:
                result = self.fitness2(ind, optimizationMethod)
            population.append(round(result, precision))
        print(f"Populacja: {population}")
        return population

    # 1. zaimplemetowac metode selekcji

    # 2. zaimplementowac krzyzowanie

    # 3. zaimplementowac mutacje

    # 4. zaimplementowac inwersje



    def calculate(self, userInput):
        self.initPopulation(userInput.populationSize, userInput.rangeBegin, userInput.rangeEnd, userInput.precision, userInput.paramNum, userInput.funcToCalc, userInput.optimizationMethod)

        # 5. Dokonczyc kod zeby sie wszystko wyliczylo
