from PySide6.QtCore import Qt, QPoint, QFile, Qt, Signal, QPropertyAnimation, QRect
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView, \
    QMessageBox, QAbstractItemView, QLineEdit
from Data.Companies import Companies
from Utils import Utils


class SharesAssistant(QWidget):
    home_requested = Signal()
    companies_selected = Signal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shares Assistant")
        self.selected_companies = []
        self._init_ui()
        self._load_styles()
        self.desired_return = None
        self.desired_risk = None

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
        content.setObjectName("middle_part")

        # Input fields for desired return and risk
        self.return_input = QLineEdit(self)
        self.return_input.setPlaceholderText("Enter desired return (0-100%)")
        self.risk_input = QLineEdit(self)
        self.risk_input.setPlaceholderText("Enter desired risk (0-100%)")

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Desired Return:"))
        input_layout.addWidget(self.return_input)
        input_layout.addWidget(QLabel("Desired Risk:"))
        input_layout.addWidget(self.risk_input)
        content_layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)
        self._add_button(button_layout, "Home", self.emit_home_requested)
        self.toggle_list_button = self._add_button(button_layout, "Show Companies", self.toggle_company_list)
        self._add_button(button_layout, "Select Companies", self.select_companies)
        self._add_button(button_layout, "Start Simulation", self.send_data_to_home_window)
        content_layout.addLayout(button_layout)  # Add button layout to the content layout


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

    def send_data_to_home_window(self):

        """Validate inputs and start the portfolio simulation."""
        self.desired_return = self.return_input.text().strip()
        self.desired_risk = self.risk_input.text().strip()

        # Check if inputs are valid
        if not self.is_valid_input(self.desired_return) or not self.is_valid_input(self.desired_risk):
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Input Error')
            msg_box.setText('Please enter valid values for return and risk (0-100).')
            msg_box.exec()
            return

        # Convert inputs to float or None if empty
        self.desired_return = float(self.desired_return) if self.desired_return else None
        self.desired_return = float(self.desired_return) if self.desired_return else None


        """Emit a signal with selected companies to send data to the home window."""
        print("Sending to Home Window")
        self.companies_selected.emit(self.selected_companies)

