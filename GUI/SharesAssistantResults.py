import numpy as np
from PySide6.QtCharts import QPieSeries, QChart, QChartView, QPieSlice
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from Utils import Utils

class SharesAssistantResults(QWidget):
    home_requested = Signal()

    def __init__(self, ticker_symbols, optimal_weights, tab):
        super().__init__()
        self.ticker_symbols = ticker_symbols
        self.optimal_weights = optimal_weights
        self.tab = tab
        self.setWindowTitle("Shares Assistant Results")
        self.setup_shares_assistant_results_widget()
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

    def setup_shares_assistant_results_widget(self):
        """Set up the layout and widgets of the shares_assistant_results."""
        layout = QVBoxLayout()

        header = self.create_label("Shares Assistant Results", "header", Qt.AlignCenter)
        layout.addWidget(header, 5)

        self.setup_middle_widget(layout)

        footer = self.create_label("Footer", "footer", Qt.AlignCenter)
        layout.addWidget(footer, 5)

        self.setLayout(layout)

    def setup_middle_widget(self, layout):
        """Create and set up the middle widget with a home button and results layout."""
        # Create the main horizontal layout to hold results and the pie chart
        middle_layout = QHBoxLayout()

        # Create the layout for the results (left side)
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.create_label("Portfolio Analysis Results:", "results_header", Qt.AlignCenter))
        self.create_results_labels(results_layout)
        middle_layout.addLayout(results_layout, 50)  # Assign weight to the results layout

        # Create the chart (right side)
        chart_view = self.create_pie_chart()
        middle_layout.addWidget(chart_view, 50)  # Assign weight to the chart layout

        middle_widget = QWidget()
        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 90)

    def create_pie_chart(self):
        # Create Pie series
        series = QPieSeries()
        total = sum(self.optimal_weights)
        for ticker, weight in zip(self.ticker_symbols, self.optimal_weights):
            if weight > 0:
                slice = QPieSlice(f"{ticker}: {weight / total * 100:.2f}%", weight)
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

        # Display stock weights
        for st, weight in zip(self.ticker_symbols, self.optimal_weights):
            stock_label = self.create_label(f'Stock {st} has weight {np.round(weight * 100, 2)}%', None, Qt.AlignLeft)
            layout.addWidget(stock_label)

        # Display portfolio metrics
        for name, value in zip('Return Volatility SharpeRatio'.split(), self.tab):
            metrics_label = self.create_label(f'{name} is: {value:.2f}', None, Qt.AlignLeft)
            layout.addWidget(metrics_label)

    def emit_home_requested(self):
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()
