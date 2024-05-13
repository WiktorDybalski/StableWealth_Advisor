from functools import partial

from PySide6.QtGui import QIcon, QPixmap, QBrush, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTableWidgetItem, QTableWidget, \
    QComboBox, QHeaderView, QSizePolicy, QFrame, QScrollBar, QToolButton
from PySide6.QtCore import Qt, QFile, Signal, QSize
from Configurators.StockInformationConfigurator import StockInformationConfigurator as si_config
from Utils import Utils
from Configurators.CompanyConfigurator import CompanyConfigurator as config

from Data.Companies import Companies


class StockInformation(QWidget):
    home_requested = Signal()
    stock_data_requested = Signal()
    company_details_requested = Signal()

    def __init__(self):
        super().__init__()
        self.config = config()
        self.si_config = si_config("day")
        self.scale_combo = None
        self.table_widget = None
        self.buttons_dict = {}
        self.last_date = self.si_config.last_update_time
        self._init_ui()
        self.setup_styles()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()
        self.create_middle_part(self.layout)
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

        last_update_text = QLabel("Date of last update:")
        last_update_value = QLabel(str(self.last_date))

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.update_table)
        refresh_button.setFixedHeight(50)
        refresh_button.setFixedWidth(150)

        controls_layout.addWidget(QLabel("Select a time period:"))
        controls_layout.addWidget(self.scale_combo)
        controls_layout.addWidget(last_update_text)
        controls_layout.addWidget(last_update_value)
        controls_layout.addStretch()
        controls_layout.addWidget(refresh_button)

        middle_layout.addLayout(controls_layout)

        # Create the table widget
        self.table_widget = QTableWidget(0, 7)
        self.table_widget.setHorizontalHeaderLabels(
            ["Nr", "Company Name", "Today's Value", "Growth", "Percentage growth", "Trend", "Show a period plot"])
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
        self.create_table()

    def create_table(self):
        """Populate the table based on the selected scale."""
        current_period = str(self.scale_combo.currentText())
        self.si_config.period = current_period

        if self.si_config.period == "Day":
            data = self.si_config.companies_day
        elif self.si_config.period == "Month":
            data = self.si_config.companies_month
        else:
            data = self.si_config.companies_year

        self.table_widget.setRowCount(len(data))
        self.buttons_dict = {}

        for i in range(len(data)):
            row = i
            company_name = Companies.get_companies_without_polish()[data[i][0]]
            value = data[i][1]
            growth = data[i][2]
            percentage_growth = data[i][3]

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

            # Company value
            company_value = QTableWidgetItem(f"{value:.2f}")
            company_value.setFlags(company_value.flags() & ~Qt.ItemIsEditable)
            company_value.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row, 2, company_value)

            # Growth
            growth_item = QTableWidgetItem(f"{growth:.2f}")
            growth_item.setFlags(growth_item.flags() & ~Qt.ItemIsEditable)
            growth_item.setTextAlignment(Qt.AlignCenter)

            if growth > 0:
                growth_item.setForeground(QBrush(QColor(0, 128, 0)))
            elif growth < 0:
                growth_item.setForeground(QBrush(QColor(255, 0, 0)))
            else:
                growth_item.setForeground(QBrush(QColor(0, 0, 0)))

            self.table_widget.setItem(row, 3, growth_item)

            # Percentage growth (duplicate of growth)
            percentage_growth_item = QTableWidgetItem(f"{percentage_growth:.2f}%")
            percentage_growth_item.setFlags(percentage_growth_item.flags() & ~Qt.ItemIsEditable)
            percentage_growth_item.setTextAlignment(Qt.AlignCenter)

            if percentage_growth > 0:
                percentage_growth_item.setForeground(QBrush(QColor(0, 128, 0)))
            elif growth < 0:
                percentage_growth_item.setForeground(QBrush(QColor(255, 0, 0)))
            else:
                percentage_growth_item.setForeground(QBrush(QColor(0, 0, 0)))

            self.table_widget.setItem(row, 4, percentage_growth_item)

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
            self.table_widget.setCellWidget(row, 5, trend_widget)

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
            self.table_widget.setCellWidget(row, 6, self.buttons_dict[company_name])

            self.table_widget.setRowHeight(row, 50)

            # Adjust the trend column width for larger icons
            self.table_widget.setColumnWidth(4, 40)

    def update_table(self):
        """Update the table based on the selected scale."""
        current_period = str(self.scale_combo.currentText())
        self.si_config.period = current_period
        if self.si_config.period == "Day":
            data = self.si_config.companies_day
        elif self.si_config.period == "Month":
            data = self.si_config.companies_month
        else:
            data = self.si_config.companies_year

        for row in range(len(data)):
            company_id = data[row][0]
            company_name = Companies.get_companies_without_polish()[company_id]
            value = data[row][1]
            growth = data[row][2]
            percentage_growth = data[row][3]

            # Update widgets
            self.table_widget.item(row, 0).setText(str(row + 1))
            self.table_widget.item(row, 1).setText(company_name)
            self.table_widget.item(row, 2).setText(f"{value:.2f}")
            self.table_widget.item(row, 3).setText(f"{growth:.2f}")
            self.table_widget.item(row, 4).setText(f"{percentage_growth:.2f}%")
            self.update_growth_color(self.table_widget.item(row, 3), growth)
            self.update_growth_color(self.table_widget.item(row, 4), growth)
            self.update_trend_icon(self.table_widget.cellWidget(row, 5), growth)
            plot_button = self.buttons_dict[company_name]
            plot_button.setProperty("company_name", company_name)
            plot_button.setProperty("growth", growth)
            plot_button.setProperty("percentage_growth", (growth / 100) * 100)

    def update_growth_color(self, item, growth):
        if growth > 0:
            item.setForeground(QBrush(QColor(0, 128, 0)))
        elif growth < 0:
            item.setForeground(QBrush(QColor(255, 0, 0)))
        else:
            item.setForeground(QBrush(QColor(0, 0, 0)))

    def update_trend_icon(self, widget, growth):
        icon_path = Utils.get_absolute_file_path("up_green.png" if growth > 0 else "down_red.png")
        widget.layout().itemAt(0).widget().setPixmap(
            QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

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
