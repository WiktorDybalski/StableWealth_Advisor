from PySide6.QtCore import Qt, QFile, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from Utils import Utils

class Calculator(QWidget):
    home_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Treasury Bond Calculator")
        self.setup_calculator_widget()
        self.load_styles()

    def load_styles(self):
        """Load the QSS style sheet for the calculator widget."""
        style_file = QFile(Utils.get_absolute_file_path("CalculatorStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
            style_file.close()  # Always good practice to close the file after reading
        else:
            print("Calculator StyleSheet Load Error.")

    def setup_calculator_widget(self):
        """Set up the layout and widgets of the treasury bonds calculator."""
        layout = QVBoxLayout()

        header = self.create_label("Header", "header", Qt.AlignCenter)
        layout.addWidget(header, 2)

        middle_widget = self.setup_middle_widget()
        layout.addWidget(middle_widget, 7)

        footer = self.create_label("Footer", "footer", Qt.AlignCenter)
        layout.addWidget(footer, 1)

        self.setLayout(layout)

    def setup_middle_widget(self):
        """Create and set up the middle widget with a home button."""
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QHBoxLayout()

        home_button = QPushButton("Home")
        home_button.clicked.connect(self.emit_home_requested)
        middle_layout.addWidget(home_button)

        middle_widget.setLayout(middle_layout)
        return middle_widget

    def create_label(self, text, object_name, alignment):
        """Create a QLabel with specified properties."""
        label = QLabel(text)
        label.setAlignment(alignment)
        label.setObjectName(object_name)
        return label

    def emit_home_requested(self):
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()
