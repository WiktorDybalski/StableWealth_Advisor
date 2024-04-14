from PySide6.QtCore import QFile, Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView
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

    def _init_ui(self):
        """Initialize the user interface components of the SharesAssistant."""
        self.layout = QVBoxLayout()
        self._setup_header()
        self._setup_content_area()
        self._setup_footer()
        self.setLayout(self.layout)

    def _load_styles(self):
        """Load CSS styles from the specified stylesheet file."""
        style_file = QFile(Utils.get_absolute_file_path("SharesAssistantStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("SharesAssistant StyleSheet Load Error.")

    def _setup_header(self):
        """Setup the header of the window."""
        header = QLabel("Shares Assistant", self)
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        self.layout.addWidget(header, 5)

    def _setup_content_area(self):
        """Setup the central content area of the widget."""
        content = QWidget(self)
        content_layout = QVBoxLayout()  # Changed from QHBoxLayout to QVBoxLayout
        content.setObjectName("middle_part")

        # Setup buttons in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)
        self._add_button(button_layout, "Home", self.emit_home_requested)
        self.toggle_list_button = self._add_button(button_layout, "Show Companies", self.toggle_company_list)
        self._add_button(button_layout, "Select Companies", self.select_companies)
        self._add_button(button_layout, "Start Simulation", self.send_data_to_home_window)
        content_layout.addLayout(button_layout)  # Add button layout to the content layout

        # Setup company list below the buttons
        self._setup_company_list(content_layout)  # This adds the company list to the vertical layout

        content.setLayout(content_layout)
        self.layout.addWidget(content, 90)

    def _setup_footer(self):
        """Setup the footer of the window."""
        footer = QLabel("Footer", self)
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(footer, 5)

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
        print("Selected companies:", self.selected_companies)

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()

    def send_data_to_home_window(self):
        """Emit a signal with selected companies to send data to the home window."""
        print("Sending to Home Window")
        self.companies_selected.emit(self.selected_companies)

