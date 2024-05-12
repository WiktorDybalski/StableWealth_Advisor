from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget, QToolBar, QFrame, \
    QApplication
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

    def set_sa_controller(self, controller):
        self.shares_assistant_controller = controller

    def set_si_controller(self, controller):
        self.stock_controller = controller

    def setup_window_size(self):
        screen = self.app.primaryScreen().size()
        width = screen.width() * 0.9
        height = screen.height() * 0.88
        left = screen.width() * 0.05
        top = screen.height() * 0.05
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
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

        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_action.setCheckable(True)

        close_action = QAction("Close App", self)
        close_action.triggered.connect(self.close)
        close_action.setCheckable(True)


        self.toolbar.addAction(home_action)
        self.toolbar.addAction(shares_action)
        self.toolbar.addAction(calculator_action)
        self.toolbar.addAction(stock_information_action)
        self.toolbar.addAction(help_action)
        self.toolbar.addAction(close_action)

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
        """Create and set up the central part of the stock information widget."""
        # Middle Widget Setup
        middle_widget = QFrame()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_widget.setLayout(middle_layout)
        middle_layout.setAlignment(Qt.AlignCenter)
        middle_layout.setContentsMargins(15, 15, 15, 15)
        middle_layout.setSpacing(15)
        middle_widget.setFixedHeight(self.height() * 0.8)
        middle_widget.setFixedWidth(self.width())

        # Title Section
        title_section = QWidget()
        title_section.setObjectName("title_section")
        title_layout = QVBoxLayout()
        title_section.setLayout(title_layout)
        middle_layout.addWidget(title_section)

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

        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        middle_layout.addWidget(divider)

        # Content Section
        content_section = QWidget()
        content_section.setObjectName("content_section")
        content_layout = QHBoxLayout()
        content_section.setLayout(content_layout)
        content_section.setFixedWidth(self.width() * 0.8)
        content_section.setFixedHeight(self.height() * 0.5)
        content_layout.setAlignment(Qt.AlignTop)

        # Left Section for Shares Assistant
        left_section = QWidget()
        left_section.setObjectName("left_section")
        left_layout = QVBoxLayout()
        left_section.setLayout(left_layout)
        left_section.setFixedHeight(content_section.height() * 0.6)

        left_title_label = QLabel("Shares Assistant")
        left_title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_layout.addWidget(left_title_label)

        left_desc_label = QLabel()
        left_desc_label.setTextFormat(Qt.RichText)
        left_desc_label.setText("""<p style='text-align: justify;'>
                Unlock your investment potential with our Shares Assistant, 
                a cutting-edge tool designed to navigate the complexities of 
                the stock market, offering tailored insights and real-time 
                analytics to help you make informed decisions and maximize 
                your financial growth.
            </p>""")
        left_desc_label.setWordWrap(True)
        left_desc_label.setStyleSheet("font-size: 14px; color: gray;")
        left_layout.addWidget(left_desc_label)

        shares_button = QPushButton("Go to Shares Assistant")
        shares_button.setStyleSheet("padding: 10px;")
        shares_button.clicked.connect(self.show_shares_assistant)
        left_layout.addWidget(shares_button)

        content_layout.addWidget(left_section)

        # Right Section for Treasury Bond Calculator
        right_section = QWidget()
        right_section.setObjectName("right_section")
        right_layout = QVBoxLayout()
        right_section.setLayout(right_layout)
        right_section.setFixedHeight(content_section.height() * 0.6)

        right_title_label = QLabel("Treasury Bond Calculator")
        right_title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        right_layout.addWidget(right_title_label)

        right_desc_label = QLabel()
        right_desc_label.setTextFormat(Qt.RichText)
        right_desc_label.setText("""<p style='text-align: justify;'>
                Explore the lucrative world of government securities with our Treasury Bond Calculator, 
                a sophisticated resource that simplifies bond market analysis, enabling you to understand yields, 
                calculate returns, and make strategic investment choices with confidence and precision.
            </p>""")
        right_desc_label.setWordWrap(True)
        right_desc_label.setStyleSheet("font-size: 14px; color: gray;")
        right_layout.addWidget(right_desc_label)

        calculator_button = QPushButton("Go to Bond Calculator")
        calculator_button.setStyleSheet("padding: 10px;")
        calculator_button.clicked.connect(self.show_calculator)
        right_layout.addWidget(calculator_button)

        content_layout.addWidget(right_section)

        # Adding Content Section to the Middle Layout
        middle_layout.addWidget(content_section)

        # Add the middle_widget to the main layout
        layout.addWidget(middle_widget, alignment=Qt.AlignCenter)

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

    def close(self):
        """Switch the view to the shares assistant screen."""
        QApplication.quit()

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
