class UserInput:

    def __init__(self, rangeBegin, rangeEnd, epochs, paramNum, precision, populationSize, crossMethod, crossProbability,
                 inversionProbability, percentEliteStrategy, mutationMethod, mutationProbability, selectionMethod, funcToCalc,
                 percentBestToSelect, tournamentSize, optimizationMethod):
        self.rangeBegin = rangeBegin
        self.rangeEnd = rangeEnd
        self.epochs = epochs
        self.paramNum = paramNum
        self.precision = precision
        self.populationSize = populationSize
        self.crossMethod = crossMethod
        self.crossProbability = crossProbability
        self.inversionProbability = inversionProbability
        self.percentEliteStrategy = percentEliteStrategy
        self.mutationMethod = mutationMethod
        self.mutationProbability = mutationProbability
        self.selectionMethod = selectionMethod
        self.funcToCalc = funcToCalc
        self.percentBestToSelect = percentBestToSelect
        self.tournamentSize = tournamentSize
        self.optimizationMethod = optimizationMethod

    def __init__(self, rangeBegin, rangeEnd, epochs, paramNum, precision, populationSize, crossMethod, crossProbability,
                 inversionProbability, percentEliteStrategy, mutationMethod, mutationProbability, selectionMethod, funcToCalc,
                 percentBestToSelect, optimizationMethod):
        self.rangeBegin = rangeBegin
        self.rangeEnd = rangeEnd
        self.epochs = epochs
        self.paramNum = paramNum
        self.precision = precision
        self.populationSize = populationSize
        self.crossMethod = crossMethod
        self.crossProbability = crossProbability
        self.inversionProbability = inversionProbability
        self.percentEliteStrategy = percentEliteStrategy
        self.mutationMethod = mutationMethod
        self.mutationProbability = mutationProbability
        self.selectionMethod = selectionMethod
        self.funcToCalc = funcToCalc
        self.percentBestToSelect = percentBestToSelect
        self.optimizationMethod = optimizationMethod


    def toString(self):
        print("Range Begin: " + str(self.rangeBegin) + "\n Range End: " + str(self.rangeEnd) + "\n Epochs: " +
              str(self.epochs) + "\n Number of paramethers: " + str(self.paramNum) + "\n Precision: " + str(self.precision) +
              "\n Population size: " + str(self.populationSize) + "\n Cross method: " + str(self.crossMethod) +
              "\n Cross probability: " + str(self.crossProbability) + "\n Range End: " + str(self.rangeEnd) + "\n Inversion probability: "
              + str(self.inversionProbability) + "\n Percent Elite Strategy: " + str(self.percentEliteStrategy) + "\n Mutation method: " +
              str(self.mutationMethod) + "\n Mutation Probability: " + str(self.mutationProbability) + "\n Selection method: " + str(self.selectionMethod) +
              "\n Function to calculate: " + str(self.funcToCalc) + "\n Percent of best to select: " + str(self.percentBestToSelect) +
              "\n Tournament Size: " + str(getattr(self, "tournamentSize", None)) + "\n Optimization method: " + str(self.optimizationMethod))

