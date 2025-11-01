from UI_PlotsWindow import Ui_PlotsWindow
from PyQt6.QtWidgets import QMainWindow

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PlotsWindow()
        self.ui.setupUi(self)

