from PyQt6.QtWidgets import QMainWindow

from UI_MainWindow import Ui_MainWindow
from PlotsWindow import PlotWindow
from UserInput import UserInput
from GeneticAlgorithm import GeneticAlgorithm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plot_window = PlotWindow()

        self.ui.label_16.setVisible(False)
        self.ui.tournamentSizeTextEdit.setVisible(False)

        self.ui.selectionMethodComboBox.currentTextChanged.connect(self.on_selection_method_change)
        self.ui.calculateButton.clicked.connect(self.on_calculate_button_clicked)

    def on_selection_method_change(self):
        """Pokazuje lub ukrywa pole rozmiaru turnieju na podstawie combo boxa."""
        is_tournament = (self.ui.selectionMethodComboBox.currentText() == "Tournament Selection")
        is_roulette = (self.ui.selectionMethodComboBox.currentText() == "Roulette Selection")
        self.ui.tournamentSizeTextEdit.setVisible(is_tournament)
        self.ui.label_16.setVisible(is_tournament)
        if is_tournament:
            self.ui.label_15.setText("Tournament number")
            self.ui.bestToSelectTextEdit.setPlainText("5")
        elif is_roulette:
            self.ui.label_15.setText("% to select")
            self.ui.bestToSelectTextEdit.setPlainText("0.33")
        else:
            self.ui.label_15.setText("% best to select")
            self.ui.bestToSelectTextEdit.setPlainText("0.33")

    
    def _validate_field(self, widget, convert_to_type, error_msg, validation_rule=None):
        """Funkcja pomocnicza - waliduje pojedynzce pola."""
        try:
            value = convert_to_type(widget.toPlainText())
        except ValueError:
            raise ValueError(error_msg)

        if validation_rule and not validation_rule(value):
            raise ValueError(error_msg)
        
        return value
    

    def on_calculate_button_clicked(self):
        """Główna metoda. Próbuje pobrać dane - jeśli się uda, uruchamia algorytm."""
        try:
            user_input = self._try_get_user_input()
            self._run_algorithm(user_input)

        except ValueError as e:
            self.ui.warningLabel.setText(str(e))
        except Exception as e:
            print(e)

    
    def _try_get_user_input(self):
        """Zbiera i waliduje dane z formularza. """
        textEdits = (
            self.ui.precisionTextEdit,
            self.ui.rangeBeginningTextEdit,
            self.ui.rangeEndTextEdit,
            self.ui.epochsTextEdit,
            self.ui.paramNumbersTextEdit,
            self.ui.populationSizeTextEdit,
            self.ui.crossProbabilityTextEdit,
            self.ui.inversionProbabilityTextEdit,
            self.ui.eliteStrategyTextEdit,
            self.ui.mutationProbabilityTextEdit,
            self.ui.bestToSelectTextEdit,
        )
        if any(f.toPlainText().strip() == "" for f in textEdits):
            raise ValueError("Fill in all of the fields")
        
        selection_method = self.ui.selectionMethodComboBox.currentText() 
        if selection_method == "Tournament Selection" and self.ui.tournamentSizeTextEdit.toPlainText().strip() == "":
            raise ValueError("Fill in Tournament Size field")

        is_positive_int = lambda v: v > 0
        is_probability = lambda v: 0.0 < v < 1.0

        precision = self._validate_field(self.ui.precisionTextEdit, int, "Precision must be a integer number.")
        range_begin = self._validate_field(self.ui.rangeBeginningTextEdit, float, "Range begin must be a number.")
        range_end = self._validate_field(self.ui.rangeEndTextEdit, float, "Range end must be a number.")
    
        if range_end <= range_begin:
            raise ValueError("Range end must be greater than range begin")
        
        epochs = self._validate_field(self.ui.epochsTextEdit, int, "Epochs must be positive integer.", is_positive_int)
        param_num = self._validate_field(self.ui.paramNumbersTextEdit, int, "Number of params must be positive integer.", is_positive_int)
        population_size = self._validate_field(self.ui.populationSizeTextEdit, int, "Population size must be positive integer.", is_positive_int)

        cross_prob = self._validate_field(self.ui.crossProbabilityTextEdit, float, "Cross probability must be (0, 1).", is_probability)
        inversion_prob = self._validate_field(self.ui.inversionProbabilityTextEdit, float, "Inversion probability must be (0, 1).", is_probability)
        elite_strategy = self._validate_field(self.ui.eliteStrategyTextEdit, float, "Elite strategy must be (0, 1).", is_probability)
        mutation_prob = self._validate_field(self.ui.mutationProbabilityTextEdit, float, "Mutation probability must be (0, 1).", is_probability)

        tournament_size = None
        if selection_method == "Tournament Selection":
            tournament_size = self._validate_field(self.ui.tournamentSizeTextEdit, int, "Tournament size must be a positive integer.", is_positive_int)
            best_to_select = self._validate_field(self.ui.bestToSelectTextEdit, int, "Tournament size must be positive integer", is_positive_int)
            if tournament_size*best_to_select > population_size:
                raise ValueError("Tournament size multiplied by tournament number must be smaller than or equal to population size.")
        else:
            best_to_select = self._validate_field(self.ui.bestToSelectTextEdit, float, "Best to select must be (0, 1).",
                                                  is_probability)

        cross_method = self.ui.crossMethodComboBox.currentText()
        mutation_method = self.ui.mutationMethodComboBox.currentText()
        func_name = self.ui.calculateFunctionComboBox.currentText()
        optimization_method = "min" if self.ui.minimumRadioButton.isChecked() else "max"

        self.ui.warningLabel.setText("")
        print("All correct. Creating UserInput...")

        return UserInput(range_begin, range_end, epochs, 
                        param_num, precision, population_size,
                        cross_method, cross_prob, inversion_prob, 
                        elite_strategy, mutation_method, mutation_prob,
                        selection_method, func_name, best_to_select, 
                        optimization_method, tournament_size)
    

    def _run_algorithm(self, user_input: UserInput):
        print("Running the algorithm...")
        
        self.changePlotsComboBox()
        self.plot_window.show()
        
        genetic_algorithm = GeneticAlgorithm(user_input)
        print(genetic_algorithm)
        genetic_algorithm.calculate()


    def changePlotsComboBox(self):
        if self.ui.maximumRadioButton.isChecked():
            self.plot_window.ui.comboBox.setItemText(1, "Maximum Fitness Value Over Iterations")
        else:
            self.plot_window.ui.comboBox.setItemText(1, "Minimum Fitness Value Over Iterations")
