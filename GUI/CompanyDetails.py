from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QFile, Signal

from GUI.Plots.StockPriceStart import StockPriceChart
from Utils import Utils

class CompanyDetails(QWidget):

    home_requested = Signal()

    def __init__(self, company_name, growth, percentage_growth):
        super().__init__()
        self.company_name = company_name
        self.growth = growth
        self.percentage_growth = percentage_growth
        self._init_ui()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()
        self.create_header(self.company_name, self.layout)
        self.create_middle_part(self.layout)
        self.create_footer(self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)


    def create_header(self, company_name, layout):
        """Create and configure the header section."""
        header = QLabel(company_name)
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

        # Upper widget for Growth and Percentage Growth
        upper_widget = QWidget()
        upper_layout = QHBoxLayout()
        upper_widget.setLayout(upper_layout)

        self.growth_label = QLabel("Growth: N/A")
        self.percentage_growth_label = QLabel("Percentage Growth: N/A")
        upper_layout.addWidget(self.growth_label)
        upper_layout.addWidget(self.percentage_growth_label)

        # Lower widget for Stock Price Chart
        self.stock_chart = StockPriceChart(width=8, height=6)
        lower_widget = QWidget()
        lower_layout = QVBoxLayout()
        lower_widget.setLayout(lower_layout)
        lower_layout.addWidget(self.stock_chart)

        # Add upper and lower widgets to the middle layout
        middle_layout.addWidget(upper_widget)
        middle_layout.addWidget(lower_widget)

        layout.addWidget(middle_widget, 60)

    def update_growth_data(self, growth, percentage_growth):
        """Update the growth and percentage growth labels."""
        self.growth_label.setText(f"Growth: {growth}")
        self.percentage_growth_label.setText(f"Percentage Growth: {percentage_growth}%")

    def update_stock_chart(self, data):
        """Update the stock chart with new data (list of tuples: [(Date, price), ...])."""
        self.stock_chart.plot(data)

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