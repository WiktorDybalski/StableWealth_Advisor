from PySide6.QtCore import Qt, QPoint, QFile, Qt, Signal, QPropertyAnimation, QRect
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView, \
    QMessageBox, QAbstractItemView, QLineEdit
from Data.Companies import Companies
from Utils import Utils
from Configurators.SharesAssistantConfigurator import SharesAssistantConfigurator as config


class SharesAssistant(QWidget):
    home_requested = Signal()
    simulation_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shares Assistant")
        self.config = config()
        self.selected_companies = []
        self._init_ui()
        self._load_styles()
        self.desired_return_min = None
        self.desired_return_max = None
        self.desired_risk_min = None
        self.desired_risk_max = None

    def _init_ui(self):
        """Initialize the user interface components of the SharesAssistant."""
        self.layout = QVBoxLayout()
        self._create_header(self.layout)
        self._create_content_area()
        self._create_footer(self.layout)
        self.setLayout(self.layout)

    def _load_styles(self):
        """Load CSS styles from the specified stylesheet file."""
        style_file = QFile(Utils.get_absolute_file_path("SharesAssistantStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("SharesAssistant StyleSheet Load Error.")

    def _create_header(self, layout):
        """Create and configure the header section."""
        header = QLabel("Shares Assistant")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)


    def _create_content_area(self):
        """Setup the central content area of the widget."""
        content = QWidget(self)
        content_layout = QVBoxLayout()
        content.setObjectName("middle_widget")

        # Input fields for desired return and risk
        self.return_input_min = QLineEdit(self)
        self.return_input_min.setPlaceholderText("Enter desired minimal return (0-100%)")
        self.return_input_max = QLineEdit(self)
        self.return_input_max.setPlaceholderText("Enter desired maximum return (0-100%)")
        self.risk_input_min = QLineEdit(self)
        self.risk_input_min.setPlaceholderText("Enter desired minimal risk (0-100%)")
        self.risk_input_max = QLineEdit(self)
        self.risk_input_max.setPlaceholderText("Enter desired maximum risk (0-100%)")

        self.return_input_min.textChanged.connect(self.on_return_input_changed)
        self.return_input_max.textChanged.connect(self.on_return_input_changed)
        self.risk_input_min.textChanged.connect(self.on_risk_input_changed)
        self.risk_input_max.textChanged.connect(self.on_risk_input_changed)

        input_layout = QHBoxLayout()
        input_layout.setObjectName("input_layout")
        input_layout.addWidget(QLabel("Desired minimum Return:"))
        input_layout.addWidget(self.return_input_min)
        input_layout.addWidget(QLabel("Desired maximum Return:"))
        input_layout.addWidget(self.return_input_max)

        input_layout.addWidget(QLabel("Desired minimum Risk:"))
        input_layout.addWidget(self.risk_input_min)
        input_layout.addWidget(QLabel("Desired maximum Risk:"))
        input_layout.addWidget(self.risk_input_max)
        content_layout.addLayout(input_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignTop)
        self._add_button(buttons_layout, "Home", self.emit_home_requested)
        self.toggle_list_button = self._add_button(buttons_layout, "Show Companies", self.toggle_company_list)
        self._add_button(buttons_layout, "Select Companies", self.select_companies)
        self._add_button(buttons_layout, "Start Simulation", self.send_data_to_home_window)
        content_layout.addLayout(buttons_layout)  # Add button layout to the content layout


        self._setup_company_list(content_layout)

        content.setLayout(content_layout)
        self.layout.addWidget(content, 60)


    def _create_footer(self, layout):
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

    def _add_button(self, layout, text, handler):
        """Helper method to create and add a button."""
        button = QPushButton(text, self)
        button.clicked.connect(handler)
        layout.addWidget(button)
        return button

    def _setup_company_list(self, layout):
        """Setup the company list widget."""
        self.company_list_widget = QListWidget(self)
        self.company_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.company_list_widget.setVisible(False)
        for ticker, name in Companies.get_companies_without_polish().items():
            self.company_list_widget.addItem(name)
        layout.addWidget(self.company_list_widget)

    def toggle_company_list(self):
        """Toggle the visibility of the company list and update button text."""
        is_visible = self.company_list_widget.isVisible()
        self.company_list_widget.setVisible(not is_visible)
        self.toggle_list_button.setText("Hide Companies" if is_visible else "Show Companies")

    def select_companies(self):
        """Store the selected companies and print them."""
        self.selected_companies = [item.text() for item in self.company_list_widget.selectedItems()]
        if len(self.selected_companies) > 10:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Invalid number of selected companies')
            msg_box.setText('You are allowed to select only 10 companies!')
            msg_box.setObjectName("msg_box")
            msg_box.exec()
            return
        print("Selected companies:", self.selected_companies)
        is_visible = self.company_list_widget.isVisible()
        self.company_list_widget.setVisible(not is_visible)

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()


    def is_valid_input(self, value):
        """Check if the input is a valid percentage (0-100)."""
        try:
            val = float(value)
            return 0 <= val <= 100
        except ValueError:
            return False if value else True  # Allow empty string which represents None

    def is_valid_max_min(self, min_value, max_value):
        """Validate that the minimum value is less than or equal to the maximum value."""
        try:
            min_val = float(min_value)
            max_val = float(max_value)
            return min_val <= max_val
        except ValueError:
            return False if min_value or max_value else True   # if both are empty (so if risks are not filled and returns are then allow None)

    def paired_inputs_filled(self, input_min, input_max):
        """Check that both inputs in a pair are filled or both are empty."""
        # Both fields are empty
        if not input_min and not input_max:
            return True
        # Both fields are filled
        if input_min and input_max:
            return True
        # One field is filled and the other is not
        return False

    def on_return_input_changed(self, text):
        """Disable the risk input if return input has text, else enable it."""
        if text:
            self.risk_input_min.setDisabled(True)
            self.risk_input_max.setDisabled(True)
        else:
            self.risk_input_min.setDisabled(False)
            self.risk_input_max.setDisabled(False)

    def on_risk_input_changed(self, text):
        """Disable the return input if risk input has text, else enable it."""
        if text:
            self.return_input_min.setDisabled(True)
            self.return_input_max.setDisabled(True)

        else:
            self.return_input_min.setDisabled(False)
            self.return_input_max.setDisabled(False)

    def send_data_to_home_window(self):

        """Validate inputs and start the portfolio simulation."""
        self.desired_return_min = self.return_input_min.text().strip()
        self.desired_return_max = self.return_input_max.text().strip()
        self.desired_risk_min = self.risk_input_min.text().strip()
        self.desired_risk_max = self.risk_input_max.text().strip()

        # Check that if one is filled, both are filled in each pair
        if not self.paired_inputs_filled(self.desired_return_min, self.desired_return_max):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Both maximum and minimum values of return should be entered (to set an exact value instead of a range enter the same value in both boxes)')
            msg_box.exec()
            return

        if not self.paired_inputs_filled(self.desired_risk_min, self.desired_risk_max):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Both maximum and minimum values of risk should be entered (to set an exact value instead of a range enter the same value in both boxes)')
            msg_box.exec()
            return

        # Check if inputs are valid
        if not self.is_valid_input(self.desired_return_min) or not self.is_valid_input(self.desired_return_max) or not self.is_valid_input(self.desired_risk_min) or not self.is_valid_input(self.desired_risk_max):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Please enter valid values for return and risk (0-100).')
            msg_box.exec()
            return

        # Check if min values are less than or equal to max values
        if not self.is_valid_max_min(self.desired_return_min, self.desired_return_max):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Maximum return must be greater than or equal to minimum return.')
            msg_box.exec()
            return

        if not self.is_valid_max_min(self.desired_risk_min, self.desired_risk_max):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Maximum risk must be greater than or equal to minimum risk.')
            msg_box.exec()
            return


        # Convert inputs to float or None if empty
        self.config.desired_return_min = float(self.desired_return_min) if self.desired_return_min else None
        self.config.desired_return_max = float(self.desired_return_max) if self.desired_return_max else None
        self.config.desired_risk_min = float(self.desired_risk_min) if self.desired_risk_min else None
        self.config.desired_risk_max = float(self.desired_risk_max) if self.desired_risk_max else None
        self.config.companies = self.selected_companies

        """Emit a signal with config to send data to the home window."""
        print("Sending config to Home Window")
        self.simulation_requested.emit()

