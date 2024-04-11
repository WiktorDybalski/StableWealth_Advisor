from PySide6.QtCore import QFile, Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QAbstractItemView
from Data.Companies import Companies
from Utils import Utils


class SharesAssistant(QWidget):
    home_requested = Signal()
    companies_selected = Signal(list)

    def __init__(self):
        super().__init__()
        self.selected_companies = []
        self.toggle_list_button = None
        self.company_list_widget = None
        self.setWindowTitle("Shares Assistant")
        self.setup_shares_assistant_widget()
        self.load_styles()

    def load_styles(self):
        """Load CSS styles from the specified stylesheet file."""
        style_file = QFile(Utils.get_absolute_file_path("SharesAssistantStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("SharesAssistant StyleSheet Load Error.")

    def setup_shares_assistant_widget(self):
        """Setup the layout and widgets of the SharesAssistant window."""
        layout = QVBoxLayout()

        self.setup_header(layout)
        self.setup_content_area(layout)
        self.setup_footer(layout)
        self.setLayout(layout)

    def setup_header(self, layout):
        header = QLabel("Shares Assistant")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 5)

    def setup_content_area(self, layout):
        """Setup the central content area of the widget."""
        content = QWidget()
        content.setObjectName("middle_part")
        content_layout = QHBoxLayout()

        home_button = QPushButton("Home")
        home_button.clicked.connect(self.emit_home_requested)
        content_layout.addWidget(home_button)

        self.toggle_list_button = QPushButton("Show Companies")
        self.toggle_list_button.clicked.connect(self.toggle_company_list)
        content_layout.addWidget(self.toggle_list_button)

        self.company_list_widget = QListWidget()
        self.company_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.company_list_widget.setVisible(False)
        for ticker, name in Companies.companies.items():
            self.company_list_widget.addItem(name)
        content_layout.addWidget(self.company_list_widget)

        select_button = QPushButton("Select Companies")
        select_button.clicked.connect(self.select_companies)
        content_layout.addWidget(select_button)

        start_button = QPushButton("Start Simulation")
        start_button.clicked.connect(self.send_data_to_home_window)
        content_layout.addWidget(start_button)

        content.setLayout(content_layout)
        layout.addWidget(content, 90)

    def setup_footer(self, layout):
        """Setup the footer of the window."""
        footer = QLabel("Footer")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer, 5)

    def toggle_company_list(self):
        """Toggle the visibility of the company list and update button text."""
        is_visible = self.company_list_widget.isVisible()
        self.company_list_widget.setVisible(not is_visible)
        self.toggle_list_button.setText("Hide Companies" if not is_visible else "Show Companies")

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
