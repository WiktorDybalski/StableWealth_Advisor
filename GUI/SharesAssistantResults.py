import numpy as np
from PySide6.QtCharts import QPieSeries, QChart, QChartView, QPieSlice
from PySide6.QtGui import QPainter, QFont
from PySide6.QtCore import Qt, QFile, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QGridLayout
from Utils import Utils
from Configurators.SharesAssistantConfigurator import SharesAssistantConfigurator as config

class SharesAssistantResults(QWidget):
    home_requested = Signal()

    def __init__(self):
        super().__init__()
        self.config = config()
        self._init_ui()
        self.load_styles()

    def load_styles(self):
        """Load the QSS style sheet for the shares_assistant_results widget."""
        style_file = QFile(Utils.get_absolute_file_path("SharesAssistantResultsStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), 'utf-8')
            self.setStyleSheet(style_sheet)
            style_file.close()
        else:
            print("Shares Assistant Results StyleSheet Load Error.")

    def _init_ui(self):
        """Set up the layout and widgets of the shares_assistant_results."""
        main_layout = QVBoxLayout(self)

        # Add the section title
        section_title = QLabel("Investment Portfolio Results")
        section_title.setObjectName("section_title")
        section_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(section_title)

        # Add the divider line
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(divider)

        # Set up the middle widget with results and pie chart
        self.setup_middle_widget(main_layout)

        self.setLayout(main_layout)

    def setup_middle_widget(self, layout):
        """Create and set up the middle widget with a home button and results layout."""
        middle_layout = QHBoxLayout()

        # Create the layout for the results (left side)
        results_layout = QVBoxLayout()
        self.create_results_labels(results_layout)
        middle_layout.addLayout(results_layout, 50)

        # Create the chart (right side)
        chart_view = self.create_pie_chart()
        chart_view.setObjectName("chart_view")
        middle_layout.addWidget(chart_view, 50)

        middle_widget = QWidget()
        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 60)


    def create_pie_chart(self):
        # Create Pie series
        series = QPieSeries()
        total = sum(self.config.weights)
        for company, weight in zip(self.config.companies, self.config.weights):
            if weight > 0.01:
                slice = QPieSlice(f"{company}: {weight / total * 100:.2f}%", weight)
                slice.setLabelVisible(True)
                series.append(slice)

        # Create Chart and set its animation options
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Create ChartView and set it to be anti-aliased
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing, True)
        return chart_view

    def create_label(self, text, object_name, alignment):
        """Create a QLabel with specified properties."""
        label = QLabel(text)
        label.setAlignment(alignment)
        if object_name:
            label.setObjectName(object_name)
        return label


    def create_results_labels(self, layout):
        """Create and set up labels for displaying investment results."""

        stock_weights_title = QLabel("Stock Weights")
        stock_weights_title.setObjectName("section_subtitle")
        layout.addWidget(stock_weights_title)

        stock_weights_layout = QGridLayout()
        stock_weights_layout.setVerticalSpacing(8)
        stock_weights_layout.setHorizontalSpacing(20)

        row = 0
        for company, weight in zip(self.config.companies, self.config.weights):
            if weight > 0.01:
                stock_label = QLabel(f'{company}')
                weight_label = QLabel(f'{np.round(weight * 100, 2)}%')
                stock_label.setObjectName("stock_label")
                weight_label.setObjectName("weight_label")
                stock_weights_layout.addWidget(stock_label, row, 0)
                stock_weights_layout.addWidget(weight_label, row, 1)
                row += 1

        layout.addLayout(stock_weights_layout)

        # Portfolio Metrics Section
        portfolio_metrics_title = QLabel("Portfolio Metrics")
        portfolio_metrics_title.setObjectName("section_subtitle")
        layout.addWidget(portfolio_metrics_title)

        metrics_layout = QGridLayout()
        metrics_layout.setVerticalSpacing(8)
        metrics_layout.setHorizontalSpacing(20)

        names = ["Expected Profit", "Expected Investment Risk"]
        profit_risk_ratio_name = "Profit to Risk Ratio"
        for index, (name, value) in enumerate(zip(names, self.config.results[:-1])):
            name_label = QLabel(name)
            value_label = QLabel(f'{value:.2f}%')
            name_label.setObjectName("metrics_name_label")
            value_label.setObjectName("metrics_value_label")
            metrics_layout.addWidget(name_label, index, 0)
            metrics_layout.addWidget(value_label, index, 1)

        last_value_formatted = f'{float(self.config.results[-1]):.2f}'
        metrics_name_label = QLabel(profit_risk_ratio_name)
        metrics_value_label = QLabel(last_value_formatted)
        metrics_name_label.setObjectName("metrics_name_label")
        metrics_value_label.setObjectName("metrics_value_label")
        metrics_layout.addWidget(metrics_name_label, len(names), 0)
        metrics_layout.addWidget(metrics_value_label, len(names), 1)

        layout.addLayout(metrics_layout)

    def create_label_bold(self, text, parent_layout, alignment, bold=False):
        """Create a bold label with the specified text and alignment."""
        label = QLabel(text)
        label.setAlignment(alignment)
        label.setObjectName("portfolio_metrics_label")
        if bold:
            label.setStyleSheet("font-weight: bold;")
        if parent_layout:
            parent_layout.addWidget(label)
        return label

    def emit_home_requested(self):
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()

    def emit_shares_assistant_requested(self):
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()

    def show_advanced_data(self):
        pass
