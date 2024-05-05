from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea, QComboBox
from PySide6.QtCore import Qt, QFile, Signal

from Utils import Utils


class Calculator(QWidget):

    home_requested = Signal()
    table_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.bond_type = ""
        self._init_ui()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()
        self.create_header(self.layout)
        self.create_middle_part(self.layout)
        self.create_footer(self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)


    def create_header(self, layout):
        """Create and configure the header section."""
        header = QLabel("Calculator")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def create_middle_part(self, layout):
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QHBoxLayout()

        # Create the buttons widget and layout
        buttons = QWidget()
        buttons_layout = QVBoxLayout()
        buttons.setLayout(buttons_layout)
        buttons_layout.setAlignment(Qt.AlignTop)

        bonds_type_checkbox = QComboBox()
        bonds_type_checkbox.setObjectName("bonds_type_checkbox")
        company_names = [
            "OTS",
            "ROR",
            "DOR",
            "TOS",
            "COI",
            "EDO",
            "ROS",
            "ROD"
        ]
        bonds_type_checkbox.addItems(company_names)

        # Create a button for calculation
        button1 = QPushButton("Calculate")
        button1.setObjectName("calculate_button")
        button1.clicked.connect(self.display_calculator_results())

        # Add combo box and button to the layout
        buttons_layout.addWidget(bonds_type_checkbox)
        buttons_layout.addWidget(button1)
        middle_layout.addWidget(buttons)
        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 60)

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

    def display_calculator_results(bond_type):
        pass

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()