from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget, QToolBar, QFrame
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
        self.toolbar = None
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
        width = screen.width() * 0.8
        height = screen.height() * 0.8
        left = screen.width() * 0.1
        top = screen.height() * 0.1
        self.setGeometry(left, top, width, height)

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
        self.create_toolbar()

        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbar_container")

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.toolbar)
        toolbar_layout.addStretch()
        toolbar_container.setLayout(toolbar_layout)

        layout.addWidget(toolbar_container)
        layout.addWidget(self.stackedWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.home_widget = QWidget()
        self.setup_home_widget()
        self.stackedWidget.addWidget(self.home_widget)
        self.init_others_widgets()
        self.setLayout(layout)

    def create_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setObjectName("mainToolbar")
        parent_width = self.width()
        self.toolbar.setFixedWidth(int(parent_width * 0.7))
        self.toolbar.setMovable(False)

        home_action = QAction("Home", self)
        home_action.triggered.connect(self.show_home)
        home_action.setCheckable(True)

        shares_action = QAction("Shares Assistant", self)
        shares_action.triggered.connect(self.show_shares_assistant)
        shares_action.setCheckable(True)

        calculator_action = QAction("Calculator", self)
        calculator_action.triggered.connect(self.show_calculator)
        calculator_action.setCheckable(True)

        stock_information_action = QAction("Stock Information", self)
        stock_information_action.triggered.connect(self.show_stock_information)
        stock_information_action.setCheckable(True)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        settings_action.setCheckable(True)

        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_action.setCheckable(True)

        self.toolbar.addAction(home_action)
        self.toolbar.addAction(shares_action)
        self.toolbar.addAction(calculator_action)
        self.toolbar.addAction(stock_information_action)
        self.toolbar.addAction(settings_action)
        self.toolbar.addAction(help_action)

        self.adjust_toolbar_buttons(self.toolbar)

    def adjust_toolbar_buttons(self, parrent):
        parent_width = parrent.width()
        button_width = int(parent_width * (1 / 6))
        for action in self.toolbar.actions():
            button = self.toolbar.widgetForAction(action)
            if button:
                button.setFixedWidth(button_width)

    def setup_home_widget(self):
        """Setup the layout and widgets of the home screen."""
        layout = QVBoxLayout()
        self.create_middle_part(layout)
        self.create_footer(layout)

        self.home_widget.setLayout(layout)

    def _setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def create_middle_part(self, layout):
        """Create and set up the main welcome screen layout."""
        # Title Section
        title_section = QWidget()
        title_section.setObjectName("title_section")
        title_layout = QVBoxLayout()
        title_section.setLayout(title_layout)

        # Add Title Label
        title_label = QLabel("Welcome to Safe Investment Assistant")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)

        # Add Subtitle Label
        subtitle_label = QLabel("Your Partner in Secure Investing")
        subtitle_label.setObjectName("subtitle_label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 16px; color: gray;")
        title_layout.addWidget(subtitle_label)

        layout.addWidget(title_section, alignment=Qt.AlignTop)

        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        # Button Section
        button_section = QWidget()
        button_section.setObjectName("button_section")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_section.setLayout(button_layout)

        # Shares Assistant Button
        shares_button = QPushButton("Shares Assistant")
        shares_button.setObjectName("shares_button")
        shares_button.setToolTip("Click to analyze your investment opportunities.")
        shares_button.setStyleSheet("font-size: 14px; padding: 10px;")
        shares_button.clicked.connect(self.show_shares_assistant)
        button_layout.addWidget(shares_button)

        # Treasury Bond Calculator Button
        calculator_button = QPushButton("Treasury Bond Calculator")
        calculator_button.setObjectName("calculator_button")
        calculator_button.setToolTip("Click to explore current market trends.")
        calculator_button.setStyleSheet("font-size: 14px; padding: 10px;")
        calculator_button.clicked.connect(self.show_calculator)
        button_layout.addWidget(calculator_button)

        layout.addWidget(button_section, alignment=Qt.AlignCenter)

        # Add Spacing for Alignment
        layout.addStretch()

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
        parent_width = self.width()
        footer.setFixedHeight(int(parent_width * 0.04))

        layout.addWidget(footer)


    def send_stock_data_to_stock_controller(self):
        self.stock_controller.create_data()

    def send_data_to_controller(self):
        self.shares_assistant_controller.run_simulation()

    def show_home(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.home_widget)
        self.highlight_action(self.sender())

    def show_shares_assistant(self):
        """Switch the view to the shares assistant screen."""
        self.stackedWidget.setCurrentWidget(self.shares_assistant)
        self.highlight_action(self.sender())

    def show_shares_assistant_results(self):
        self.shares_assistant_results = SharesAssistantResults()
        self.shares_assistant_results.home_requested.connect(self.show_home)
        self.stackedWidget.addWidget(self.shares_assistant_results)
        self.stackedWidget.setCurrentWidget(self.shares_assistant_results)

    def show_calculator(self):
        """Switch the view to the calculator screen."""
        self.stackedWidget.setCurrentWidget(self.calculator)
        self.highlight_action(self.sender())

    def show_calculator_results(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.calculator_results)

    def show_stock_information(self):
        """Return to the home screen view."""
        self.stackedWidget.setCurrentWidget(self.stock_information)
        self.highlight_action(self.sender())

    def show_settings(self):
        """Switch the view to the shares assistant screen."""
        self.stackedWidget.setCurrentWidget(self.settings)
        self.highlight_action(self.sender())

    def show_help(self):
        """Switch the view to the calculator screen."""
        self.stackedWidget.setCurrentWidget(self.help)
        self.highlight_action(self.sender())

    def show_company_details(self):
        self.company_details = CompanyDetails(self.company_config.company_name, self.company_config.growth, self.company_config.percentage_growth)
        self.stackedWidget.addWidget(self.company_details)
        self.stackedWidget.setCurrentWidget(self.company_details)

    def highlight_action(self, action):
        for toolbar_action in self.findChildren(QAction):
            toolbar_button = self.toolbar.widgetForAction(toolbar_action)
            if toolbar_button:
                toolbar_button.setChecked(toolbar_action == action)

if __name__ == "__main__":
    pass
