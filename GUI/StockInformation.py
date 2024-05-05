from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, \
    QComboBox
from PySide6.QtCore import Qt, QFile, Signal

from Utils import Utils


class StockInformation(QWidget):
    home_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Informations")
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
        header = QLabel("Stock informations")
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

        # Scale selection combo box and refresh button
        controls_layout = QHBoxLayout()
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["Day", "Month", "Year"])
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.update_table)

        controls_layout.addWidget(QLabel("Select Scale:"))
        controls_layout.addWidget(self.scale_combo)
        controls_layout.addWidget(refresh_button)
        middle_layout.addLayout(controls_layout)

        # Create the table widget
        self.table_widget = QTableWidget(10, 3)
        self.table_widget.setHorizontalHeaderLabels(["Company Name", "Growth", "Trend"])
        self.table_widget.horizontalHeader()
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        middle_layout.addWidget(self.table_widget)

        # Add the middle widget to the main layout
        layout.addWidget(middle_widget, 60)

        # Initialize the table with data
        self.update_table()

    def update_table(self):
        """Populate the table based on the selected scale."""
        data = self.get_growth_data(self.scale_combo.currentText())
        self.table_widget.setRowCount(len(data))

        column_widths = [200, 100, 100, 100]  # Adjust the first column (Nr) width to 80
        for col in range(4):
            self.table_widget.setColumnWidth(col, column_widths[col])

        for row, (company_name, growth) in enumerate(data):

            self.table_widget.setItem(row, 0, QTableWidgetItem(company_name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"{growth:.2f}%"))
            self.table_widget.setRowHeight(row, 60)
            icon_directory = r"C:\Users\wikto\Desktop\Everything\Studies\Term4\Python\Images"

            trend_icon = "up" if growth > 0 else "down"
            trend_color = "green" if growth > 0 else "red"
            icon_path = f"{icon_directory}\\{trend_icon}_{trend_color}.png"
            icon = QIcon(icon_path)

            trend_item = QTableWidgetItem()
            trend_item.setIcon(icon)
            trend_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 2, trend_item)
            self.table_widget.horizontalHeader().setStyleSheet(
                "QHeaderView::section {"
                "background-color: #2C3E50;"
                "color: white;"
                "font-weight: bold;"
                "font-size: 10pt;"
                "border: 1px solid #34495E;"
                "padding: 5px;"
                "}"
            )
            self.table_widget.setStyleSheet(
                "QTableWidget {"
                "font-size: 10pt;"
                "}"
                "QTableWidget::item {"
                "padding: 5px;"
                "}"
                "QTableWidget::item:selected {"
                "background-color: #1ABC9C;"
                "color: white;"
                "}"

            )
            self.table_widget.setAlternatingRowColors(True)
            self.table_widget.setAlternatingRowColors(True)
            self.table_widget.setAlternatingRowColors(True)


    def get_growth_data(self, scale):
        """Simulate fetching growth data based on the selected scale."""

        data = {
            "Day": [("Apple Inc.", 1.5), ("Microsoft Corporation", -0.3), ("Alphabet Inc.", 2.2), ("Apple Inc.", 1.5),
                    ("Microsoft Corporation", -0.3), ("Alphabet Inc.", 2.2), ("Apple Inc.", 1.5),
                    ("Microsoft Corporation", -0.3), ("Alphabet Inc.", 2.2)],
            "Month": [("Apple Inc.", -1.2), ("Microsoft Corporation", 3.4), ("Alphabet Inc.", 0.8),
                      ("Apple Inc.", -1.2), ("Microsoft Corporation", 3.4), ("Alphabet Inc.", 0.8),
                      ("Apple Inc.", -1.2), ("Microsoft Corporation", 3.4), ("Alphabet Inc.", 0.8)],
            "Year": [("Apple Inc.", 10.5), ("Microsoft Corporation", -2.1), ("Alphabet Inc.", 6.3),
                     ("Apple Inc.", 10.5), ("Microsoft Corporation", -2.1), ("Alphabet Inc.", 6.3),
                     ("Apple Inc.", 10.5), ("Microsoft Corporation", -2.1), ("Alphabet Inc.", 6.3)]
        }
        return data.get(scale, [])

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

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()
