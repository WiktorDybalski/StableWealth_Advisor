from functools import partial

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, \
    QComboBox, QHeaderView, QSizePolicy, QFrame, QScrollBar, QToolButton
from PySide6.QtCore import Qt, QFile, Signal, QSize
from Configurators.StockInformationConfigurator import StockInformationConfigurator as si_config
from Utils import Utils
from Configurators.CompanyConfigurator import CompanyConfigurator as config

from Data.Companies import Companies

from datetime import datetime, timedelta
import csv

class StockInformation(QWidget):
    home_requested = Signal()
    stock_data_requested = Signal()
    company_details_requested = Signal()
    def __init__(self):
        super().__init__()
        self.config = config()
        self.si_config = si_config("day")
        self.create_data()
        self.scale_combo = None
        self.table_widget = None
        self.buttons_dict = {}
        self._init_ui()
        self.setup_styles()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()
        self.create_middle_part(self.layout)
        self.create_footer(self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("StockInformationStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)


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
        self.table_widget.setHorizontalHeaderLabels(
            ["Nr", "Company Name", "Growth", "Percentage growth", "Trend", "Show a period plot"])
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
        #self.create_data()
        #data = self.si_config.companies_day
        data = self.get_data(self.scale_combo.currentText())
        self.table_widget.setRowCount(len(data))
        self.buttons_dict = {}

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
            plot_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            plot_button.setProperty("company_name", company_name)
            plot_button.setProperty("growth", growth)
            price = 100
            plot_button.setProperty("percentage_growth", (growth / price) * 100)

            if not company_name in self.buttons_dict:
                self.buttons_dict[company_name] = plot_button

            plot_button.clicked.connect(partial(self.show_company_button_details, plot_button))
            self.table_widget.setCellWidget(row, 5, self.buttons_dict[company_name])

            self.table_widget.setRowHeight(row, 50)

        # Adjust the trend column width for larger icons
        self.table_widget.setColumnWidth(4, 40)

    def get_data(self, scale):
        """Simulate fetching growth data based on the selected scale."""

        self.create_data()
        print(self.si_config.companies_day)
        data = {
            "Day": [("Apple Inc.", 1.5), ("Microsoft Corporation", -0.3), ("Alphabet Inc.", 2.2), ("Amazon.com Inc.", 1.5),
                    ("Berkshire Hathaway Inc.", -0.3), ("Tesla Inc.", 2.2), ("UnitedHealth Group Incorporated", 1.5),
                    ("Johnson & Johnson", -0.3), ("Visa Inc.", 2.2), ("NVIDIA Corporation", 2.2), ("Exxon Mobil Corporation", 2.2), ("Taiwan Semiconductor Manufacturing Company Limited", 2.2)],
            "Month": [("Apple Inc.", -1.2), ("Microsoft Corporation", 3.4), ("Alphabet Inc.", 0.8),
                      ("Amazon.com Inc.", -1.2), ("Berkshire Hathaway Inc.", 3.4), ("Tesla Inc.", 0.8),
                      ("UnitedHealth Group Incorporated", -1.2), ("Johnson & Johnson", 3.4), ("Visa Inc.", 0.8), ("NVIDIA Corporation", 0.8), ("Exxon Mobil Corporation", 0.8), ("Taiwan Semiconductor Manufacturing Company Limited", 0.8)],
            "Year": [("Apple Inc.", 10.5), ("Microsoft Corporation", -2.1), ("Alphabet Inc.", 6.3),
                     ("Amazon.com Inc.", 10.5), ("Berkshire Hathaway Inc.", -2.1), ("Tesla Inc.", 6.3),
                     ("UnitedHealth Group Incorporated", 10.5), ("Microsoft Corporation", -2.1), ("Visa Inc.", 6.3),
                     ("NVIDIA Corporation", 6.3), ("Exxon Mobil Corporation", 6.3), ("Taiwan Semiconductor Manufacturing Company Limited", 6.3)]
        }

        # """Fetch actual growth data based on the selected scale."""
        # # Read data from CSV file
        # with open('stock_data_without_polish.csv', newline='') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     stock_data = list(reader)
        #
        # # Get today's date and the second-to-last day
        # today = datetime.today().date()
        # second_last_day = today - timedelta(days=1)
        #
        # # Filter stock data for today and the second-to-last day
        # today_data = [data for data in stock_data if datetime.strptime(data['Date'], '%Y-%m-%d').date() == today]
        # second_last_day_data = [data for data in stock_data if
        #                         datetime.strptime(data['Date'], '%Y-%m-%d').date() == second_last_day]
        #
        # # Calculate growth percentage for each company based on the second-to-last day compared to today's price
        # growth_data = {}
        # for company in stock_data[0].keys():
        #     if company != 'Date':  # Exclude 'Date' column
        #         # Get today's and second-to-last day's prices
        #         today_price = float(today_data[0][company])
        #         second_last_day_price = float(second_last_day_data[0][company])
        #
        #         # Calculate growth percentage
        #         growth_percentage = ((today_price - second_last_day_price) / second_last_day_price) * 100
        #         data["Day"].append((company, growth_percentage))
        #         #growth_data[company] = growth_percentage
        #
        # # Sort companies by growth percentage
        # #sorted_growth_data = sorted(growth_data.items(), key=lambda x: x[1], reverse=True)
        #
        # # Add the growth data for today to the "Day" variant in the data dictionary
        # data["Day"] = growth_data

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

    def create_data(self):
        self.stock_data_requested.emit()

    def show_company_button_details(self, button):
        """Update the configuration and emit a signal to show company details."""
        company_name = button.property("company_name")
        growth = button.property("growth")
        percentage_growth = button.property("percentage_growth")
        self.config.company_name = company_name
        self.config.growth = growth
        self.config.percentage_growth = percentage_growth
        self.company_details_requested.emit()

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()
