import pandas as pd
from PySide6.QtCore import Qt, QFile, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QLabel, QPushButton, \
    QComboBox, QFrame, \
    QLineEdit, QTableWidget, QMessageBox, QScrollBar, QSizePolicy, QGridLayout

from Configurators.CalculatorConfigurator import CalculatorConfigurator as config
from Data.Bonds import Bonds
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
        self.inflation_rate = 12.4
        self.months_amount = 120
        self.NBP = ''
        self.bond_results = None
        self.results_table = None
        self.middle_layout = None
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
        self.middle_layout = QVBoxLayout()  # store middle layout reference
        self.middle_layout.setAlignment(Qt.AlignTop)

        title = QLabel("Treasury Bonds Calculator")
        title.setObjectName("section_title")
        title.setAlignment(Qt.AlignCenter)
        self.middle_layout.addWidget(title)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        self.middle_layout.addWidget(divider)

        bonds_type_label = QLabel("Select Bond Type")
        bonds_type_label.setObjectName("label")
        bonds_type_label.setAlignment(Qt.AlignLeft)
        self.middle_layout.addWidget(bonds_type_label)

        bonds_type_checkbox = QComboBox()
        bonds_type_checkbox.setObjectName("bonds_type_checkbox")
        bond_types = ["EDO", "OTS", "ROR", "DOR", "TOS", "COI", "ROS", "ROD"]
        bonds_type_checkbox.addItems(bond_types)
        self.middle_layout.addWidget(bonds_type_checkbox)

        belka_tax_label = QLabel("Belka Tax = 19%")
        belka_tax_label.setObjectName("label")
        belka_tax_label.setAlignment(Qt.AlignLeft)
        self.middle_layout.addWidget(belka_tax_label)

        grid_layout = QGridLayout()

        amount_label = QLabel("Investment Amount (in PLN)")
        amount_label.setObjectName("label")
        amount_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(amount_label, 0, 0)

        self.amount_input = QLineEdit(str(self.amount))
        self.amount_input.setObjectName("amount_input")
        grid_layout.addWidget(self.amount_input, 0, 1)

        months_amount_label = QLabel("Number of Months")
        months_amount_label.setObjectName("label")
        months_amount_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(months_amount_label, 0, 2)

        self.months_amount_input = QLineEdit(str(self.months_amount))
        self.months_amount_input.setObjectName("cycles_input")
        grid_layout.addWidget(self.months_amount_input, 0, 3)

        inflation_rate_label = QLabel("Inflation Rate (%):")
        inflation_rate_label.setObjectName("label")
        inflation_rate_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(inflation_rate_label, 1, 0)

        self.inflation_rate_input = QLineEdit(str(self.inflation_rate))
        self.inflation_rate_input.setObjectName("inflation_rate_input")
        grid_layout.addWidget(self.inflation_rate_input, 1, 1)

        NBP_label = QLabel("NBP Reference Rate:")
        NBP_label.setObjectName("label")
        NBP_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(NBP_label, 1, 2)

        self.NBP_input = QLineEdit(str(self.NBP))
        self.NBP_input.setObjectName("NBP_input")
        grid_layout.addWidget(self.NBP_input, 1, 3)

        self.middle_layout.addLayout(grid_layout)

        calculate_button = QPushButton("Calculate")
        calculate_button.setObjectName("calculate_button")
        calculate_button.clicked.connect(self.display_calculator_results)
        self.middle_layout.addWidget(calculate_button)

        self.results_table = QTableWidget()
        self.middle_layout.addWidget(self.results_table)

        middle_widget.setLayout(self.middle_layout)
        layout.addWidget(middle_widget, 80)

    def set_bond_type(self, bond_type):
        """Set the selected bond type."""
        self.bond_type = bond_type

    def display_calculator_results(self):
        """Placeholder method for displaying calculator results."""

        if self.findChild(QLineEdit, "NBP_input").text() != '' and \
                Bonds.get_bonds()[self.findChild(QComboBox, "bonds_type_checkbox").currentText()][6] is None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText(
                'This type of Bond does not use the NBP reference rate - please leave this field empty to calculate this bond')
            msg_box.exec()
            return

        if self.findChild(QLineEdit, "NBP_input").text() == '' and \
                Bonds.get_bonds()[self.findChild(QComboBox, "bonds_type_checkbox").currentText()][6] is not None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText(
                'This type of Bond uses the NBP reference rate - please input the desired (current) NBP reference rate to calculate this bond')
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

        csv_path = Utils.get_absolute_file_path("treasury_bond_results.csv")
        self.bond_results = pd.read_csv(csv_path)

        if self.results_table is not None:
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)

        # Remove the column with header 'Year Inflation'
        if 'Year Inflation' in self.bond_results.columns:
            self.bond_results = self.bond_results.drop(columns=['Year Inflation'])

        # Update the existing table
        self.results_table.setRowCount(len(self.bond_results))
        self.results_table.setColumnCount(len(self.bond_results.columns))
        self.results_table.setHorizontalHeaderLabels(self.bond_results.columns)
        self.results_table.setVerticalScrollBar(QScrollBar())

        # Hide the vertical headers
        self.results_table.verticalHeader().setVisible(False)

        zl_columns = [1, 3, 4, 5, 6, 7, 8, 10]
        percent_columns = [9]

        font = QFont()
        font.setPointSize(11)

        # Populate the table with CSV data and add suffixes
        for i in range(len(self.bond_results)):
            for j in range(len(self.bond_results.columns)):
                value = self.bond_results.iat[i, j]

                # Add 'zl' suffix
                if j in zl_columns:
                    value = f"{value} zł"
                # Add '%' suffix
                elif j in percent_columns:
                    value = f"{value}%"

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(font)
                self.results_table.setItem(i, j, item)

        # Resize columns to fit contents
        self.results_table.resizeColumnsToContents()
        self.results_table.horizontalHeader().setStretchLastSection(True)

        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SingleSelection)

        # Make table occupy full horizontal space
        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()
