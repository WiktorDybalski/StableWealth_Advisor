from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt, QFile
import sys
from GUI import SharesAssistant_GUI
from GUI import Calculator_GUI


class HomeWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.stackedWidget = QStackedWidget()
        self.initUI()
        self.setupStyles()
        self.controller = None
    def setController(self, controller):
        self.controller = controller

    def initUI(self):
        screen = self.app.primaryScreen().size()
        width = screen.width() * 0.8
        height = screen.height() * 0.8
        left = screen.width() * 0.1
        top = screen.height() * 0.1
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("StableWealth Advisor")


        layout = QVBoxLayout()

        layout.addWidget(self.stackedWidget)

        self.homeWidget = QWidget()
        self.setupHomeWidget()

        self.stackedWidget.addWidget(self.homeWidget)

        self.sharesAssistant = SharesAssistant_GUI.SharesAssistant()
        self.sharesAssistant.homeRequested.connect(self.showHome)
        self.stackedWidget.addWidget(self.sharesAssistant)

        self.calculator = Calculator_GUI.TreasuryBondCalculator()
        self.calculator.homeRequested.connect(self.showHome)
        self.stackedWidget.addWidget(self.calculator)
        self.setLayout(layout)

    def setupHomeWidget(self):
        layout = QVBoxLayout()

        self.create_header(layout)
        self.create_middle_part(layout)
        self.create_footer(layout)
        self.setLayout(layout)

        self.homeWidget.setLayout(layout)

    def setupStyles(self):
        style_file = QFile("Styles/HomeWindowStyle.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def showSharesAssistant(self):
        self.stackedWidget.setCurrentWidget(self.sharesAssistant)

    def showCalculator(self):
        self.stackedWidget.setCurrentWidget(self.calculator)

    def showHome(self):
        self.stackedWidget.setCurrentWidget(self.homeWidget)

    def create_header(self, layout):
        header = QLabel("StableWealth Advisor")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 2)

    def create_middle_part(self, layout):
        middleWidget = QWidget()
        middleWidget.setObjectName("middleWidget")
        middleLayout = QHBoxLayout()

        self.create_left_label(middleLayout)
        self.create_right_label(middleLayout)

        middleWidget.setLayout(middleLayout)
        layout.addWidget(middleWidget, 7)

    def create_footer(self, layout):
        footer = QLabel("Footer")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer, 1)

    def create_left_label(self, parent_layout):
        leftLabel = QLabel()
        leftLabel.setObjectName("leftLabel")
        leftLabelLayout = QVBoxLayout()
        leftLabelHeader = QLabel("Choose what you need")
        leftLabelContent = QLabel()
        sharesButton = QPushButton("Shares assistant")
        sharesButton.clicked.connect(self.showSharesAssistant)

        calculatorButton = QPushButton("Treasury bond calculator")
        calculatorButton.clicked.connect(self.showCalculator)

        leftLabelLayout.addWidget(leftLabelHeader, 2)
        leftLabelLayout.addWidget(leftLabelContent, 8)
        leftLabelContentLayout = QVBoxLayout()
        leftLabelContent.setLayout(leftLabelContentLayout)
        leftLabelContentLayout.addWidget(sharesButton)
        leftLabelContentLayout.addWidget(calculatorButton)
        leftLabelLayout.addWidget(leftLabelContent)

        leftLabel.setLayout(leftLabelLayout)
        parent_layout.addWidget(leftLabel, 4)

    def create_right_label(self, parent_layout):
        rightLabel = QLabel("Right Widget")
        rightLabel.setObjectName("rightLabel")

        parent_layout.addWidget(rightLabel, 6)

    def sendDataToController(self, companies):
        self.controller.runSimulation(companies)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = HomeWindow(app)
    view.show()
    sys.exit(app.exec())
    pass