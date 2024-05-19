from PySide6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, \
    QComboBox, QFrame, \
    QLineEdit, QSlider, QCheckBox, QTableWidget, QMessageBox, QScrollBar
from PySide6.QtCore import Qt, QFile, Signal

from Configurators.CalculatorConfigurator import CalculatorConfigurator as config

from Data.Bonds import Bonds
import pandas as pd

from Utils import Utils


class Calculator(QWidget):
    home_requested = Signal()
    table_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Treasury Bonds Calculator Configurator")
        self.all_bonds = Bonds.get_bonds()
        self.config = config()
        self.bond_type = ""
        self.amount = 1000
        self.years = 10
        self.inflation_rate = 12.4
        self.months_amount = 12
        self.NBP = 5.25
        #self.annual_inflation = True
        self.bond_results = None
        self.results_table = None
        self.table_placeholder = None
        self._init_ui()
        self.load_styles()

    def load_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("CalculatorStyle.qss"))  # Update this path as required
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
            style_file.close()
        else:
            print("Calculator StyleSheet Load Error.")

    def _init_ui(self):
        """Setup the layout and widgets of the calculator home screen."""
        self.layout = QVBoxLayout()
        self.create_middle_part(self.layout)
        self.setLayout(self.layout)

    def create_middle_part(self, layout):
        """Create the main content of the calculator."""
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_layout.setAlignment(Qt.AlignTop)

        # Section Title
        title = QLabel("Treasury Bonds Calculator")
        title.setObjectName("section_title")
        title.setAlignment(Qt.AlignCenter)
        middle_layout.addWidget(title)

        # Divider Line
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        middle_layout.addWidget(divider)

        # Bond Type Selection
        bonds_type_label = QLabel("Select Bond Type")
        bonds_type_label.setObjectName("label")
        bonds_type_label.setAlignment(Qt.AlignLeft)
        middle_layout.addWidget(bonds_type_label)

        bonds_type_checkbox = QComboBox()
        bonds_type_checkbox.setObjectName("bonds_type_checkbox")
        bond_types = ["OTS", "ROR", "DOR", "TOS", "COI", "EDO", "ROS", "ROD"]
        bonds_type_checkbox.addItems(bond_types)
        # bonds_type_checkbox.currentIndexChanged[str].connect(self.set_bond_type)
        middle_layout.addWidget(bonds_type_checkbox)

        # Belka tax info
        belka_tax_label = QLabel("Belka Tax = 19%")
        belka_tax_label.setObjectName("label")
        belka_tax_label.setAlignment(Qt.AlignLeft)
        middle_layout.addWidget(belka_tax_label)

        # Amount and Cycles Entries in a Horizontal Layout
        amount_cycles_layout = QHBoxLayout()

        # Amount Entry
        amount_label = QLabel("Investment Amount (in PLN)")
        amount_label.setObjectName("label")
        amount_label.setAlignment(Qt.AlignLeft)
        amount_cycles_layout.addWidget(amount_label)

        self.amount_input = QLineEdit(str(self.amount))
        self.amount_input.setObjectName("amount_input")
        amount_cycles_layout.addWidget(self.amount_input)

        # Cycles Entry
        months_amount_label = QLabel("Number of Months")
        months_amount_label.setObjectName("label")
        months_amount_label.setAlignment(Qt.AlignLeft)
        amount_cycles_layout.addWidget(months_amount_label)

        self.months_amount_input = QLineEdit(str(self.months_amount))
        self.months_amount_input.setObjectName("cycles_input")
        amount_cycles_layout.addWidget(self.months_amount_input)

        # Add the horizontal layout to the main layout
        middle_layout.addLayout(amount_cycles_layout)


        # Inflation Rate and NBP Rate Entries in a Horizontal Layout
        inflation_nbp_layout = QHBoxLayout()

        # Inflation Rate Entry
        inflation_rate_label = QLabel("Inflation Rate (%):")
        inflation_rate_label.setObjectName("label")
        inflation_rate_label.setAlignment(Qt.AlignLeft)
        inflation_nbp_layout.addWidget(inflation_rate_label)

        self.inflation_rate_input = QLineEdit(str(self.inflation_rate))
        self.inflation_rate_input.setObjectName("inflation_rate_input")
        inflation_nbp_layout.addWidget(self.inflation_rate_input)

        # NBP Entry
        NBP_label = QLabel("NBP Reference Rate:")
        NBP_label.setObjectName("label")
        NBP_label.setAlignment(Qt.AlignLeft)
        inflation_nbp_layout.addWidget(NBP_label)

        self.NBP_input = QLineEdit(str(self.NBP))
        self.NBP_input.setObjectName("NBP_input")
        inflation_nbp_layout.addWidget(self.NBP_input)

        # Add the horizontal layout to the main layout
        middle_layout.addLayout(inflation_nbp_layout)


        # Calculation Button
        calculate_button = QPushButton("Calculate")
        calculate_button.setObjectName("calculate_button")
        calculate_button.clicked.connect(self.display_calculator_results)
        middle_layout.addWidget(calculate_button)

        # Placeholder for the results table
        self.table_placeholder = QWidget()
        middle_layout.addWidget(self.table_placeholder)


        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 80)

    def set_bond_type(self, bond_type):
        """Set the selected bond type."""
        self.bond_type = bond_type

    # def set_years(self, value):
    #     """Set the investment period in years and update the label."""
    #     self.years = value
    #     self.years_display.setText(f"{value} Years")

    # def toggle_inflation(self, state):
    #     """Toggle whether to include annual inflation."""
    #     self.annual_inflation = state == Qt.Checked

    def display_calculator_results(self):
        """Placeholder method for displaying calculator results."""
        #print(self.cycles)

        # print(self.findChild(QLineEdit, "NBP_input").text())
        # print(type(self.findChild(QLineEdit, "NBP_input").text()))
        # print(Bonds.get_bonds()[self.findChild(QComboBox, "bonds_type_checkbox").currentText()][6])

        if self.findChild(QLineEdit, "NBP_input").text() != '' and Bonds.get_bonds()[self.findChild(QComboBox, "bonds_type_checkbox").currentText()][6] is None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('This type of Bond doesn not use the NBP reference rate - please leave this field empty to calculate this bond')
            msg_box.exec()
            return

        # Retrieve the bond type
        self.bond_type = self.findChild(QComboBox, "bonds_type_checkbox").currentText()
        self.config.bond_type = self.bond_type

        # Retrieve the investment amount
        self.amount = int(self.findChild(QLineEdit, "amount_input").text())
        self.config.number_of_bonds = self.amount

        # Retrieve the number of cycles
        self.months_amount = int(self.findChild(QLineEdit, "cycles_input").text())
        self.config.period = self.months_amount

        # Retrieve the inflation rate
        self.inflation_rate = float(self.findChild(QLineEdit, "inflation_rate_input").text())
        self.config.curr_inflation = self.inflation_rate

        # Retrieve NPB value
        if self.findChild(QLineEdit, "NBP_input").text() == '':
            self.NBP = None
            self.config.NBP = self.NBP
        else:
            self.NBP = float(self.findChild(QLineEdit, "NBP_input").text())
            self.config.NBP = self.NBP

        self.table_requested.emit()


        # Print the retrieved values for debugging purposes
        #print(f"Bond Type: {self.bond_type}, Amount: {self.amount}, Cycles: {self.cycles}, Inflation Rate: {self.inflation_rate}")

        # self.bond_results = pd.read_csv(Utils.get_absolute_file_path("calc_results"))
        #
        # print(self.bond_results)

        # generting and showing the table

        csv_path = Utils.get_absolute_file_path("calc_results.csv")
        self.bond_results = pd.read_csv(csv_path)

        # Check if the table already exists
        if self.results_table is None:
            # Create a new QTableWidget if it doesn't exist
            self.results_table = QTableWidget()
            self.layout.replaceWidget(self.table_placeholder, self.results_table)
            self.layout.addWidget(self.results_table)

        # Update the existing table
        self.results_table.setRowCount(len(self.bond_results))
        self.results_table.setColumnCount(len(self.bond_results.columns))
        self.results_table.setHorizontalHeaderLabels(self.bond_results.columns)
        self.results_table.setVerticalScrollBar(QScrollBar())

        # Populate the table with CSV data
        for i in range(len(self.bond_results)):
            for j in range(len(self.bond_results.columns)):
                item = QTableWidgetItem(str(self.bond_results.iat[i, j]))
                self.results_table.setItem(i, j, item)

        # generting and showing the graph


        # print(f"Calculating for {self.bond_type}, Amount: {self.amount_input.text()}, Years: {self.years}, "
        #       f"Interest Rate: {self.interest_rate_input.text()}%, Annual Inflation: {self.annual_inflation}")

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()
