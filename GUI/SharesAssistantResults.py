import numpy as np
from PySide6.QtCharts import QPieSeries, QChart, QChartView, QPieSlice
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QFile, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from Utils import Utils
from Data.Companies import Companies

class SharesAssistantResults(QWidget):
    home_requested = Signal()

    def __init__(self, companies_list, optimal_weights, tab):
        super().__init__()
        self.companies_list = companies_list
        self.optimal_weights = optimal_weights
        self.tab = tab
        self.setWindowTitle("Shares Assistant Results")
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
        self.layout = QVBoxLayout()

        self.create_header(self.layout)

        self.setup_middle_widget(self.layout)

        self.create_footer(self.layout)

        self.setLayout(self.layout)

    def create_header(self, layout):
        """Create and configure the header section."""
        header = QLabel("StableWealth Advisor")
        header.setAlignment(Qt.AlignCenter)
        header.setObjectName("header")
        layout.addWidget(header, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def setup_middle_widget(self, layout):
        """Create and set up the middle widget with a home button and results layout."""
        # Create the main horizontal layout to hold results and the pie chart
        middle_layout = QHBoxLayout()

        # Create the layout for the results (left side)
        self.create_buttons_label(middle_layout)
        results_layout = QVBoxLayout()
        results_layout.addWidget(self.create_label("Portfolio Analysis Results:", "results_header", Qt.AlignCenter))
        self.create_results_labels(results_layout)
        middle_layout.addLayout(results_layout, 50)  # Assign weight to the results layout

        # Create the chart (right side)
        chart_view = self.create_pie_chart()
        chart_view.setObjectName("chart_view")
        middle_layout.addWidget(chart_view, 50)  # Assign weight to the chart layout

        middle_widget = QWidget()
        middle_widget.setLayout(middle_layout)
        layout.addWidget(middle_widget, 60)

    def create_buttons_label(self, middle_layout):
        buttons_label = QLabel()
        buttons_layout = QHBoxLayout()  # Inicjalizacja QHBoxLayout
        buttons_label.setLayout(buttons_layout)

        # Tworzenie przycisków
        home_button = QPushButton("Home")
        additional_info_button = QPushButton("Get Additional Information")
        change_companies_button = QPushButton("Change Companies")

        # Podłączenie sygnałów do slotów
        home_button.clicked.connect(self.emit_home_requested)
        change_companies_button.clicked.connect(self.emit_shares_assistant_requested)
        additional_info_button.clicked.connect(self.show_advanced_data)

        # Dodawanie przycisków do layoutu
        buttons_layout.addWidget(home_button)
        buttons_layout.addWidget(additional_info_button)
        buttons_layout.addWidget(change_companies_button)

        # Dodanie całego layoutu przycisków do środkowego layoutu
        middle_layout.addLayout(buttons_layout)


    def create_pie_chart(self):
        # Create Pie series
        series = QPieSeries()
        total = sum(self.optimal_weights)
        for company, weight in zip(self.companies_list, self.optimal_weights):
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
        # Display stock weights
        for company, weight in zip(self.companies_list, self.optimal_weights):
            if weight > 0.01:
                stock_label = self.create_label(f'{company} has weight:  {np.round(weight * 100, 2)}%', None, Qt.AlignLeft)
                layout.addWidget(stock_label)
        names = ["Expected profit", "Expected investment risk"]
        profit_risk_ratio_name = "Profit to risk ratio"
        # Display portfolio metrics
        for name, value in zip(names, self.tab):
            metrics_label = self.create_label(f'{name} is: {value:.2f}%', None, Qt.AlignLeft)
            layout.addWidget(metrics_label)
        last_value_formatted = f'{float(self.tab[-1]):.2f}'
        metrics_label = self.create_label(f'{profit_risk_ratio_name} is: {last_value_formatted}', None, Qt.AlignLeft)
        layout.addWidget(metrics_label)

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
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()

    def emit_shares_assistant_requested(self):
        """Emit a signal when the home button is pressed."""
        self.home_requested.emit()

    def show_advanced_data(self):
        pass
