from PyQt5.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QComboBox, QFrame, \
    QLineEdit, QSlider, QCheckBox
from PySide6.QtCore import Qt, QFile, Signal

from Utils import Utils


class Calculator(QWidget):
    home_requested = Signal()
    table_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Treasury Bonds Calculator Configurator")
        self.bond_type = ""
        self.amount = 1000
        self.years = 10
        self.interest_rate = 3.5
        self.annual_inflation = True
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
        self.create_footer(self.layout)
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

        # Amount Entry
        amount_label = QLabel("Investment Amount (in PLN)")
        amount_label.setObjectName("label")
        amount_label.setAlignment(Qt.AlignLeft)
        middle_layout.addWidget(amount_label)

        self.amount_input = QLineEdit(str(self.amount))
        self.amount_input.setObjectName("amount_input")
        # self.amount_input.setValidator(QIntValidator(1, 1000000))
        middle_layout.addWidget(self.amount_input)

        # Years Slider
        years_label = QLabel("Investment Period (in Years)")
        years_label.setObjectName("label")
        years_label.setAlignment(Qt.AlignLeft)
        middle_layout.addWidget(years_label)

        self.years_slider = QSlider(Qt.Horizontal)
        self.years_slider.setObjectName("years_slider")
        self.years_slider.setMinimum(1)
        self.years_slider.setMaximum(30)
        self.years_slider.setValue(self.years)
        self.years_slider.setTickPosition(QSlider.TicksBelow)
        self.years_slider.setTickInterval(1)
        self.years_slider.valueChanged.connect(self.set_years)
        middle_layout.addWidget(self.years_slider)

        self.years_display = QLabel(f"{self.years} Years")
        self.years_display.setAlignment(Qt.AlignCenter)
        middle_layout.addWidget(self.years_display)

        # Interest Rate Entry
        interest_rate_label = QLabel("Interest Rate (%)")
        interest_rate_label.setObjectName("label")
        interest_rate_label.setAlignment(Qt.AlignLeft)
        middle_layout.addWidget(interest_rate_label)

        self.interest_rate_input = QLineEdit(str(self.interest_rate))
        self.interest_rate_input.setObjectName("interest_rate_input")
        # self.interest_rate_input.setValidator(QIntValidator(0, 100))
        middle_layout.addWidget(self.interest_rate_input)

        # Annual Inflation Checkbox
        self.annual_inflation_checkbox = QCheckBox("Include Annual Inflation")
        self.annual_inflation_checkbox.setChecked(self.annual_inflation)
        self.annual_inflation_checkbox.stateChanged.connect(self.toggle_inflation)
        middle_layout.addWidget(self.annual_inflation_checkbox)

        # Calculation Button
        calculate_button = QPushButton("Calculate")
        calculate_button.setObjectName("calculate_button")
        calculate_button.clicked.connect(self.display_calculator_results)
        middle_layout.addWidget(calculate_button)

        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 80)

    def create_footer(self, layout):
        """Create and configure the footer section."""
        footer = QLabel()
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)

        footer_layout = QHBoxLayout()
        footer.setLayout(footer_layout)

        label = QLabel("WealthStable Advisor - © 2024")
        label.setObjectName("tag_label")
        label.setAlignment(Qt.AlignCenter)

        additional_info = QLabel("Created by Wiktor Dybalski, Maksymilian Katolik")
        additional_info.setObjectName("additional_info_label")
        additional_info.setAlignment(Qt.AlignCenter)

        footer_layout.addWidget(label)
        footer_layout.addWidget(additional_info)
        layout.addWidget(footer, 8)

    def set_bond_type(self, bond_type):
        """Set the selected bond type."""
        self.bond_type = bond_type

    def set_years(self, value):
        """Set the investment period in years and update the label."""
        self.years = value
        self.years_display.setText(f"{value} Years")

    def toggle_inflation(self, state):
        """Toggle whether to include annual inflation."""
        self.annual_inflation = state == Qt.Checked

    def display_calculator_results(self):
        """Placeholder method for displaying calculator results."""
        print(f"Calculating for {self.bond_type}, Amount: {self.amount_input.text()}, Years: {self.years}, "
              f"Interest Rate: {self.interest_rate_input.text()}%, Annual Inflation: {self.annual_inflation}")

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()
