from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, \
    QComboBox, QHeaderView, QSizePolicy, QFrame, QScrollBar, QToolButton
from PySide6.QtCore import Qt, QFile, Signal, QSize

from Utils import Utils


class StockInformation(QWidget):
    home_requested = Signal()

    def __init__(self):
        super().__init__()
        self.scale_combo = None
        self.table_widget = None
        self.setWindowTitle("Stock Information")
        self._init_ui()
        self.setup_styles()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()

        self.create_header(self.layout)
        self.create_middle_part(self.layout)
        self.create_footer(self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("StockInformationStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def create_header(self, layout):
        """Create and configure the header section."""
        header = QLabel("Stock information")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def create_middle_part(self, layout):
        """Create and set up the central part of the stock information widget."""
        middle_widget = QFrame()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_widget.setLayout(middle_layout)
        middle_layout.setAlignment(Qt.AlignCenter)
        middle_layout.setContentsMargins(15, 15, 15, 15)
        middle_layout.setSpacing(15)

        # Scale selection combo box and refresh button
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["Day", "Month", "Year"])
        self.scale_combo.setMinimumWidth(120)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.update_table)
        refresh_button.setFixedHeight(50)
        refresh_button.setFixedWidth(150)

        controls_layout.addWidget(QLabel("Select a time period:"))
        controls_layout.addWidget(self.scale_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(refresh_button)

        middle_layout.addLayout(controls_layout)

        # Create the table widget
        self.table_widget = QTableWidget(0, 6)
        self.table_widget.setHorizontalHeaderLabels(["Nr", "Company Name", "Growth", "Percentage growth", "Trend", "Show a period plot"])
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setShowGrid(False)
        self.table_widget.setVerticalScrollBar(QScrollBar())
        middle_layout.addWidget(self.table_widget)

        # Add the middle widget to the main layout
        layout.addWidget(middle_widget, 60)

        # Initialize the table with data
        self.update_table()

    def update_table(self):
        """Populate the table based on the selected scale."""
        data = self.get_growth_data(self.scale_combo.currentText())
        self.table_widget.setRowCount(len(data))

        for row, (company_name, growth) in enumerate(data):
            # Nr column
            nr_item = QTableWidgetItem(str(row + 1))
            nr_item.setFlags(nr_item.flags() & ~Qt.ItemIsEditable)
            nr_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 0, nr_item)

            # Company name
            company_item = QTableWidgetItem(company_name)
            company_item.setFlags(company_item.flags() & ~Qt.ItemIsEditable)
            company_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 1, company_item)

            # Growth
            growth_item = QTableWidgetItem(f"{growth:.2f}%")
            growth_item.setFlags(growth_item.flags() & ~Qt.ItemIsEditable)
            growth_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 2, growth_item)

            # Percentage growth (duplicate of growth)
            percentage_growth_item = QTableWidgetItem(f"{growth:.2f}%")
            percentage_growth_item.setFlags(percentage_growth_item.flags() & ~Qt.ItemIsEditable)
            percentage_growth_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 3, percentage_growth_item)

            # Trend icon
            trend_label = QLabel()
            trend_label.setFixedSize(50, 50)
            trend_label.setAlignment(Qt.AlignCenter)
            icon_path = Utils.get_absolute_file_path("up_green.png") if growth > 0 else Utils.get_absolute_file_path(
                "down_red.png")
            trend_label.setPixmap(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            trend_label.setStyleSheet("background-color: white; border: none;")
            trend_widget = QWidget()
            trend_widget.setStyleSheet("background-color: white; border: none;")
            trend_layout = QHBoxLayout(trend_widget)
            trend_layout.setAlignment(Qt.AlignCenter)
            trend_layout.setContentsMargins(0, 0, 0, 0)
            trend_layout.addWidget(trend_label)
            self.table_widget.setCellWidget(row, 4, trend_widget)

            # Show period plot button
            plot_button = QToolButton()
            plot_button.setText("Show more")
            plot_button.setIcon(QIcon(Utils.get_absolute_file_path("chart_icon.png")))
            plot_button.setIconSize(QSize(30, 30))
            plot_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            plot_button.setProperty("row", row)
            plot_button.clicked.connect(self.show_plot)
            self.table_widget.setCellWidget(row, 5, plot_button)

            self.table_widget.setRowHeight(row, 50)

        # Adjust the trend column width for larger icons
        self.table_widget.setColumnWidth(4, 70)


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

    def show_plot(self):
        pass

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()

