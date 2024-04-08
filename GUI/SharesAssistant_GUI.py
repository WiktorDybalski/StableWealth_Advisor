from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QAbstractItemView, QListWidget
from PySide6.QtCore import Qt, QFile
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QFile, Signal
from Model.companies import Companies
class SharesAssistant(QWidget):

    homeRequested = Signal()
    companiesSelected = Signal(list)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shares Assistant")
        self.setupSharesAssistantWidget()
        style_file = QFile("Styles/SharesAssistantStyle.css")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Nie można załadować arkusza stylów.")

    def setupSharesAssistantWidget(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Shares Assistant")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 5)

        # Content area
        content = QWidget()  # A QWidget that will hold the content layout
        content.setObjectName("middle_part")
        contentLayout = QHBoxLayout()  # The QVBoxLayout that will be set on the content QWidget

        # 'Home' button that emits the homeRequested signal
        homeButton = QPushButton("Home")
        homeButton.clicked.connect(self.emitHomeRequested)
        contentLayout.addWidget(homeButton)

        # Button to show/hide the QListWidget
        self.toggleListButton = QPushButton("Show Companies")
        self.toggleListButton.clicked.connect(self.toggleCompanyList)
        contentLayout.addWidget(self.toggleListButton)

        # QListWidget with multi-selection enabled
        self.companyListWidget = QListWidget()
        self.companyListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.companyListWidget.setVisible(False)
        for ticker, name in Companies.companies.items():
            self.companyListWidget.addItem(name)
        contentLayout.addWidget(self.companyListWidget)

        # 'Select' button that saves the selected companies
        selectButton = QPushButton("Select Companies")
        selectButton.clicked.connect(self.selectCompanies)
        contentLayout.addWidget(selectButton)

        startButton = QPushButton("Start Simulation")
        startButton.clicked.connect(self.start_simulation)
        contentLayout.addWidget(startButton)
        # Set the content layout to the content QWidget
        content.setLayout(contentLayout)

        # Add the content QWidget to the main layout
        layout.addWidget(content, 80)

        # Footer
        footer = QLabel("Footer")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer, 5)

        # Set the main layout to the window
        self.setLayout(layout)

    def toggleCompanyList(self):
        isVisible = self.companyListWidget.isVisible()
        self.companyListWidget.setVisible(not isVisible)
        self.toggleListButton.setText("Hide Companies" if not isVisible else "Show Companies")
    def selectCompanies(self):
        self.selectedCompanies = [item.text() for item in self.companyListWidget.selectedItems()]
        print("Selected companies", self.selectedCompanies)

    def emitHomeRequested(self):
        self.homeRequested.emit()

    def sendDataToHomeWindow(self):
        print("Sending to Home Window")
        self.companiesSelected.emit(self.selectedCompanies)


