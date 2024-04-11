from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QFile
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QFile, Signal
from Utils import Utils

class TreasuryBondCalculator(QWidget):
    homeRequested = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Treasury Bond Calculator")
        self.setupTreasuryBondsCalculatorWidget()

        style_file = QFile(Utils.get_absolute_file_path("CalculatorStyle.css"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Nie można załadować arkusza stylów.")

    def setupTreasuryBondsCalculatorWidget(self):
        layout = QVBoxLayout()

        header = QLabel("Header")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 2)

        middleWidget = QWidget()
        middleWidget.setObjectName("middleWidget")
        middleLayout = QHBoxLayout()
        homeButton = QPushButton("Home")
        middleLayout.addWidget(homeButton)
        homeButton.clicked.connect(self.emitHomeRequested)

        middleWidget.setLayout(middleLayout)

        layout.addWidget(middleWidget, 7)

        footer = QLabel("Footer")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer, 1)

        self.setLayout(layout)

    def emitHomeRequested(self):
        self.homeRequested.emit()