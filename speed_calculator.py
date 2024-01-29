from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget,
                             QGridLayout, QLineEdit, QPushButton, QComboBox)
import sys
from datetime import datetime


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        # create widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()
        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()
        calculate_button = QPushButton("Calculate", self)
        calculate_button.clicked.connect(self.calculate_speed)
        self.output_label = QLabel("")
        combo = QComboBox()
        combo.addItems(['Metric (km)', 'Imperial (miles)'])

        # if combo.currentText() == 'Rice':
        #     "do something"
        # if combo.currentText() == 'Pasta':
        #     "do something else"

        # add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_speed(self):
        pass


app = QApplication(sys.argv)
speed_cal = SpeedCalculator()
speed_cal.show()
sys.exit(app.exec())
