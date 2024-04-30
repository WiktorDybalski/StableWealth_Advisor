from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt, QFile
from GUI.SharesAssistant import SharesAssistant
from GUI.SharesAssistantResults import SharesAssistantResults
from GUI.Calculator import Calculator
from Utils import Utils


class HomeWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.home_widget = None
        self.shares_assistant_results = None
        self.shares_assistant = None
        self.calculator = None
        self.app = app
        self.stackedWidget = QStackedWidget()  # This widget holds the different screens of the application.
        self.init_ui()  # Initialize the user interface components.
        self.setup_styles()  # Setup the CSS styles for the window.
        self.controller = None  # Placeholder for a controller that will be set externally.

    def set_controller(self, controller):
        self.controller = controller

    def init_ui(self):
        """Initialize the main user interface of the window."""
        screen = self.app.primaryScreen().size()
        width = screen.width() * 0.9
        height = screen.height() * 0.8
        left = screen.width() * 0.05
        top = screen.height() * 0.1
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("StableWealth Advisor")

        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.home_widget = QWidget()
        self.setup_home_widget()

        self.stackedWidget.addWidget(self.home_widget)

        self.shares_assistant = SharesAssistant()
        self.shares_assistant.home_requested.connect(self.show_home)
        self.shares_assistant.companies_selected.connect(self.send_data_to_controller)
        self.stackedWidget.addWidget(self.shares_assistant)

        self.calculator = Calculator()
        self.calculator.home_requested.connect(self.show_home)
        self.stackedWidget.addWidget(self.calculator)


        self.setLayout(layout)

    def setup_home_widget(self):
        """Setup the layout and widgets of the home screen."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.create_header(layout)
        self.create_middle_part(layout)
        self.create_footer(layout)

        self.home_widget.setLayout(layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def show_shares_assistant(self):
        """Switch the view to the shares assistant screen."""
        self.stackedWidget.setCurrentWidget(self.shares_assistant)

    def show_calculator(self):
        """Switch the view to the calculator screen."""
        self.stackedWidget.setCurrentWidget(self.calculator)

    def show_home(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.home_widget)

    def create_header(self, layout):
        """Create and configure the header section."""
        header = QLabel("StableWealth Advisor")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def create_middle_part(self, layout):
        """Create and set up the central part of the home widget."""
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_widget.setLayout(middle_layout)

        self.create_upper_label(middle_layout)
        self.create_down_label(middle_layout)

        layout.addWidget(middle_widget, 70)

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

    def create_upper_label(self, parent_layout):
        upper_label = QLabel("Choose one of our products:")
        upper_label.setObjectName("upper_label")
        upper_label.setAlignment(Qt.AlignCenter)

        parent_layout.addWidget(upper_label, 30)

    def create_down_label(self, parent_layout):
        down_label = QLabel()
        down_label.setObjectName("down_label")
        down_label_layout = QHBoxLayout()
        down_label.setLayout(down_label_layout)

        shares_button = QPushButton("Shares assistant")
        shares_button.clicked.connect(self.show_shares_assistant)

        calculator_button = QPushButton("Treasury bond calculator")
        calculator_button.clicked.connect(self.show_calculator)

        shares_button.setToolTip("Click to perform investment analysis")
        calculator_button.setToolTip("Click to view current market trends")

        down_label_layout.addWidget(shares_button)
        down_label_layout.addWidget(calculator_button)

        parent_layout.addWidget(down_label, 70)

    def send_data_to_controller(self, companies):
        """Send selected company data to the controller for processing."""
        self.controller.run_simulation(companies)

    def show_shares_assistant_results(self, ticker_symbols, optimal_weights, tab):
        self.shares_assistant_results = SharesAssistantResults(ticker_symbols, optimal_weights, tab)
        self.shares_assistant_results.home_requested.connect(self.show_home)
        self.stackedWidget.addWidget(self.shares_assistant_results)
        self.stackedWidget.setCurrentWidget(self.shares_assistant_results)

if __name__ == "__main__":
    pass
