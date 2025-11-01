from PyQt6.QtWidgets import QMainWindow

from UI_MainWindow import Ui_MainWindow
from PlotsWindow import PlotWindow
from UserInput import UserInput
from GeneticAlgoritm import GeneticAlgorithm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plot_window = PlotWindow()
        self.ui.label_16.setVisible(False)
        self.ui.tournamentSizeTextEdit.setVisible(False)
        self.ui.selectionMethodComboBox.currentTextChanged.connect(lambda: self.onSelectionMethodChange())
        self.ui.calculateButton.clicked.connect(lambda: self.validateParams(self.ui, self.plot_window))

    def onSelectionMethodChange(self):
        if self.ui.selectionMethodComboBox.currentText() == "Tournament Selection":
            self.ui.tournamentSizeTextEdit.setVisible(True)
            self.ui.label_16.setVisible(True)
        else:
            self.ui.tournamentSizeTextEdit.setVisible(False)
            self.ui.label_16.setVisible(False)


    def validateParams(self, ui, plotWindow):
        textEdits = (
            ui.precisionTextEdit,
            ui.rangeBeginningTextEdit,
            ui.rangeEndTextEdit,
            ui.epochsTextEdit,
            ui.paramNumbersTextEdit,
            ui.populationSizeTextEdit,
            ui.crossProbabilityTextEdit,
            ui.inversionProbabilityTextEdit,
            ui.eliteStrategyTextEdit,
            ui.mutationProbabilityTextEdit,
            ui.bestToSelectTextEdit,
            ui.tournamentSizeTextEdit,
        )

        empty_fields = [f for f in textEdits if f.toPlainText().strip() == ""]

        if empty_fields:
            ui.warningLabel.setText("Fill in all of the fields")
        else:
            try:
                try:
                    precision = int(textEdits[0].toPlainText())
                except ValueError:
                    raise ValueError("Precision must be a integer number")

                try:
                    range_begin = float(textEdits[1].toPlainText())
                except ValueError:
                    raise ValueError("Range begin must be an integer/float")

                try:
                    range_end = float(textEdits[2].toPlainText())
                except ValueError:
                    raise ValueError("Range end must be an integer/float")
                if range_end <= range_begin:
                    raise ValueError("Range end must be greater than range begin")

                try:
                    epochs = int(textEdits[3].toPlainText())
                except ValueError:
                    raise ValueError("Epochs must be positive integer")
                if epochs <= 0:
                    raise ValueError("Epochs must be positive integer")

                try:
                    param_num = int(textEdits[4].toPlainText())
                except ValueError:
                    raise ValueError("Number of parameters must be positive integer")
                if param_num <= 0:
                    raise ValueError("Number of parameters must be positive integer")

                try:
                    population_size = int(textEdits[5].toPlainText())
                except ValueError:
                    raise ValueError("Population size must be positive integer")
                if population_size <= 0:
                    raise ValueError("Population size must be positive integer")

                try:
                    cross_prob = float(textEdits[6].toPlainText())
                except ValueError:
                    raise ValueError("Cross probability must be a decimal number between 0 and 1")
                if not (0.0 < cross_prob < 1.0):
                    raise ValueError("Cross probability must be a decimal number between 0 and 1")

                try:
                    inversion_prob = float(textEdits[7].toPlainText())
                except ValueError:
                    raise ValueError("Inversion probability must be a decimal number between 0 and 1")
                if not (0.0 < inversion_prob < 1.0):
                    raise ValueError("Inversion probability must be a decimal number between 0 and 1")

                try:
                    elite_strategy = float(textEdits[8].toPlainText())
                except ValueError:
                    raise ValueError("Elite strategy must be a decimal number between 0 and 1")
                if not (0.0 < elite_strategy < 1.0):
                    raise ValueError("Elite strategy must be a decimal number between 0 and 1")

                try:
                    mutation_prob = float(textEdits[9].toPlainText())
                except ValueError:
                    raise ValueError("Mutation probability must be a decimal number between 0 and 1")
                if not (0.0 < mutation_prob < 1.0):
                    raise ValueError("Mutation probability must be a decimal number between 0 and 1")

                try:
                    best_to_select = float(textEdits[10].toPlainText())
                except ValueError:
                    raise ValueError("Best to select must be a decimal number between 0 and 1")
                if not (0.0 < best_to_select < 1.0):
                    raise ValueError("Best to select must be a decimal number between 0 and 1")

                try:
                    tournament_size = int(textEdits[11].toPlainText())
                except ValueError:
                    raise ValueError("Tournament size must be an integer greater than 0")
                if tournament_size <= 0:
                    raise ValueError("Tournament size must be an integer greater than 0")

                ui.warningLabel.setText("")
                print("All correct")

                crossMethod = ui.crossMethodComboBox.currentText()
                mutationMethod = ui.mutationMethodComboBox.currentText()
                selectionMethod = ui.selectionMethodComboBox.currentText()
                calculationFunction = ui.calculateFunctionComboBox.currentText()
                optimizationMethod = "min" if ui.minimumRadioButton.isChecked() else "max"

                if(self.ui.selectionMethodComboBox == "Tournament Selection"):
                    userInput = UserInput(range_begin, range_end, epochs, param_num, precision, population_size,
                                          crossMethod, cross_prob,
                                          inversion_prob, elite_strategy, mutationMethod, mutation_prob,
                                          selectionMethod,
                                          calculationFunction,
                                          best_to_select, tournament_size, optimizationMethod)
                else:
                    userInput = UserInput(range_begin, range_end, epochs, param_num, precision, population_size,
                                          crossMethod, cross_prob,
                                          inversion_prob, elite_strategy, mutationMethod, mutation_prob,
                                          selectionMethod,
                                          calculationFunction,
                                          best_to_select, optimizationMethod)
                userInput.toString()
                self.changePlotsComboBox()
                plotWindow.show()
                geneticAlgorithm = GeneticAlgorithm()
                geneticAlgorithm.calculate(userInput)

            except ValueError as error:
                ui.warningLabel.setText(str(error))


    def changePlotsComboBox(self):
        if self.ui.maximumRadioButton.isChecked():
            self.plot_window.ui.comboBox.setItemText(1, "Maximum Fitness Value Over Iterations")
        else:
            self.plot_window.ui.comboBox.setItemText(1, "Minimum Fitness Value Over Iterations")


