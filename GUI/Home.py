from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget, QToolBar
from PySide6.QtCore import Qt, QFile
from GUI.SharesAssistant import SharesAssistant
from GUI.SharesAssistantResults import SharesAssistantResults
from GUI.Calculator import Calculator
from GUI.StockInformation import StockInformation
from GUI.CalculatorResults import CalculatorResults
from GUI.Settings import Settings
from GUI.Help import Help
from GUI.CompanyDetails import CompanyDetails
from Configurators.CompanyConfigurator import CompanyConfigurator as company_config
from Utils import Utils

class HomeWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.home_widget = None
        self.shares_assistant_results = None
        self.shares_assistant = None
        self.calculator = None
        self.calculator_results = None
        self.stock_information = None
        self.help = None
        self.shares_assistant_controller = None
        self.stock_controller = None
        self.settings = None
        self.company_details = None
        self.company_config = company_config()
        self.app = app
        self.stackedWidget = QStackedWidget()
        self._init_ui()
        self._setup_styles()

    def set_controller(self, controller):
        self.shares_assistant_controller = controller

    def setup_window_size(self):
        screen = self.app.primaryScreen().size()
        width = screen.width() * 1
        height = screen.height() * 0.91
        left = screen.width() * 0
        top = screen.height() * 0
        self.setGeometry(left, top, width, height)
        self.showMaximized()
        self.setWindowTitle("StableWealth Advisor")

    def init_others_widgets(self):

        self.shares_assistant = SharesAssistant()
        self.calculator = Calculator()
        self.calculator_results = CalculatorResults()
        self.stock_information = StockInformation()
        self.settings = Settings()
        self.help = Help()

        self.shares_assistant.home_requested.connect(self.show_home)
        self.shares_assistant.simulation_requested.connect(self.send_data_to_controller)
        self.calculator.home_requested.connect(self.show_home)
        self.stock_information.home_requested.connect(self.show_home)
        self.stock_information.stock_data_requested.connect(self.send_stock_data_to_stock_controller)
        self.stock_information.company_details_requested.connect(self.show_company_details)
        self.settings.home_requested.connect(self.show_home)
        self.help.home_requested.connect(self.show_home)

        self.stackedWidget.addWidget(self.shares_assistant)
        self.stackedWidget.addWidget(self.calculator)
        self.stackedWidget.addWidget(self.stock_information)
        self.stackedWidget.addWidget(self.settings)
        self.stackedWidget.addWidget(self.help)

    def _init_ui(self):
        """Initialize the main user interface of the window."""
        self.setup_window_size()

        layout = QVBoxLayout()
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        layout.addWidget(self.stackedWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.home_widget = QWidget()
        self.setup_home_widget()
        self.stackedWidget.addWidget(self.home_widget)
        self.init_others_widgets()
        self.setLayout(layout)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        home_action = QAction("Home", self)
        home_action.triggered.connect(self.show_home)
        shares_action = QAction("Shares Assistant", self)
        shares_action.triggered.connect(self.show_shares_assistant)
        calculator_action = QAction("Calculator", self)
        calculator_action.triggered.connect(self.show_calculator)
        stock_information_action = QAction("Stock Information", self)
        stock_information_action.triggered.connect(self.show_stock_information)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)


        toolbar.addAction(home_action)
        toolbar.addAction(shares_action)
        toolbar.addAction(calculator_action)
        toolbar.addAction(stock_information_action)
        toolbar.addAction(settings_action)
        toolbar.addAction(help_action)
        return toolbar

    def setup_home_widget(self):
        """Setup the layout and widgets of the home screen."""
        layout = QVBoxLayout()

        self.create_header(layout)
        self.create_middle_part(layout)
        self.create_footer(layout)

        self.home_widget.setLayout(layout)

    def _setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)


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

    def send_stock_data_to_stock_controller(self):
        self.stock_controller.create_data()

    def send_data_to_controller(self):
        self.shares_assistant_controller.run_simulation()

    def show_home(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.home_widget)

    def show_shares_assistant(self):
        """Switch the view to the shares assistant screen."""
        self.stackedWidget.setCurrentWidget(self.shares_assistant)

    def show_shares_assistant_results(self):
        self.shares_assistant_results = SharesAssistantResults()
        self.shares_assistant_results.home_requested.connect(self.show_home)
        self.stackedWidget.addWidget(self.shares_assistant_results)
        self.stackedWidget.setCurrentWidget(self.shares_assistant_results)

    def show_calculator(self):
        """Switch the view to the calculator screen."""
        self.stackedWidget.setCurrentWidget(self.calculator)

    def show_calculator_results(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.calculator_results)

    def show_stock_information(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.stock_information)

    def show_settings(self):
        """Switch the view to the shares assistant screen."""
        self.stackedWidget.setCurrentWidget(self.settings)

    def show_help(self):
        """Switch the view to the calculator screen."""
        self.stackedWidget.setCurrentWidget(self.help)

    def show_company_details(self):
        self.company_details = CompanyDetails(self.company_config.company_name, self.company_config.growth, self.company_config.percentage_growth)
        self.stackedWidget.addWidget(self.company_details)
        self.stackedWidget.setCurrentWidget(self.company_details)

if __name__ == "__main__":
    pass
