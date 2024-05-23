import pandas as pd
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout
from PySide6.QtCore import Qt, QFile, Signal

from Data.Companies import Companies
from GUI.Plots.StockPriceChart import StockPriceChart
from Configurators.CompanyConfigurator import CompanyConfigurator as config
from Utils import Utils

class CompanyDetails(QWidget):

    home_requested = Signal()

    def __init__(self, company_name, growth, percentage_growth):
        super().__init__()
        self.percentage_growth_label = None
        self.growth_label = None
        self.company_config = config()
        self.company_name = company_name
        self.growth_value = growth
        self.percentage_growth_value = percentage_growth
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.create_middle_part(self.company_name, self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        style_file = QFile(Utils.get_absolute_file_path("CompanyDetailsStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def create_middle_part(self, company_name, layout):
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_widget.setLayout(middle_layout)

        # Header section
        header = QLabel(company_name)
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header_company")
        header.setFixedHeight(self.height() * 0.1)

        header.setStyleSheet("font-size: 20px; font-weight: bold;")

        middle_layout.addWidget(header)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        middle_layout.addWidget(divider)

        # Grid layout for labels for growth
        upper_layout = QGridLayout()

        self.growth_label = QLabel("Growth:")
        self.growth_label.setObjectName("label")
        self.growth_label.setAlignment(Qt.AlignRight)
        self.growth_label.setStyleSheet("font-size: 14px;")
        upper_layout.addWidget(self.growth_label, 0, 0)

        self.growth_value = QLabel(f"{self.company_config.growth:.2f}")
        self.growth_value.setObjectName("label")
        self.growth_value.setAlignment(Qt.AlignLeft)
        self.growth_value.setStyleSheet("font-size: 14px;")
        upper_layout.addWidget(self.growth_value, 0, 1)

        self.percentage_growth_label = QLabel("Percentage Growth:")
        self.percentage_growth_label.setObjectName("label")
        self.percentage_growth_label.setAlignment(Qt.AlignRight)
        self.percentage_growth_label.setStyleSheet("font-size: 14px;")
        upper_layout.addWidget(self.percentage_growth_label, 0, 2)

        self.percentage_growth_value = QLabel(f"{self.company_config.percentage_growth:.2f}%")
        self.percentage_growth_value.setObjectName("label")
        self.percentage_growth_value.setAlignment(Qt.AlignLeft)
        self.percentage_growth_value.setStyleSheet("font-size: 14px;")
        upper_layout.addWidget(self.percentage_growth_value, 0, 3)

        middle_layout.addLayout(upper_layout)

        # Lower widget for Stock Price Chart
        self.stock_chart = StockPriceChart()
        lower_widget = QWidget()
        lower_layout = QVBoxLayout()
        lower_widget.setLayout(lower_layout)
        lower_layout.addWidget(self.stock_chart)

        # Load and plot the stock data
        df = pd.read_csv(Utils.get_absolute_file_path("stock_data_without_polish.csv"))

        company_df = df.iloc[:, [0]]
        company_ticker = None
        company_name_str = str(self.company_config.company_name)
        for key, value in Companies.get_companies_without_polish().items():
            if value == company_name_str:
                company_ticker = key
                break
        if company_ticker in df.columns:
            company_df.loc[:, company_ticker] = df.loc[:, company_ticker]

        self.stock_chart.plot(company_df)

        middle_layout.addWidget(lower_widget)

        layout.addWidget(middle_widget, 60)

    def update_growth_data(self, growth, percentage_growth):
        self.growth_label.setText(f"Growth: {growth}")
        self.percentage_growth_label.setText(f"Percentage Growth: {percentage_growth}%")

    def update_stock_chart(self, data):
        self.stock_chart.plot(data)

    def emit_home_requested(self):
        self.home_requested.emit()