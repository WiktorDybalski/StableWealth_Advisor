import pandas as pd
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import QDateTime, Qt, QFile
from PySide6.QtGui import QPainter, QCursor
from PySide6.QtWidgets import QToolTip

from Utils import Utils


class StockPriceChart(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self._setup_styles()

    def _setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("StockPriceChartStyle.qss"))
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = str(style_file.readAll(), encoding='utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Unable to open stylesheet file.")

    def plot(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Provided data is not a pandas DataFrame")

        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)

        valid_df = df[pd.notna(df.iloc[:, 1])]

        if valid_df['Date'].isnull().any():
            raise ValueError("Date column contains invalid dates")

        # Clear previous series
        self.chart.removeAllSeries()

        # Create a new series
        series = QLineSeries()

        for index, row in df.iterrows():
            if pd.notna(row.iloc[1]):
                date = QDateTime(row['Date'])
                price = float(row.iloc[1])
                series.append(date.toMSecsSinceEpoch(), price)

        # Add series to chart
        self.chart.addSeries(series)

        # Create and set the X axis (Date)
        axisX = QDateTimeAxis()
        axisX.setFormat("dd MMM yyyy")
        axisX.setTitleText("Date")

        # Get date range and set custom ticks
        start_date = valid_df['Date'].min()
        end_date = valid_df['Date'].max()
        start_date_qt = QDateTime(start_date)
        end_date_qt = QDateTime(end_date)

        # Calculate total number of years and set tick interval
        total_years = end_date.year - start_date.year
        if total_years <= 10:
            period = 2
        elif total_years <= 20:
            period = 3
        else:
            period = 10

        tick_dates = [start_date]
        current_date = start_date + pd.DateOffset(years=period)
        while current_date <= end_date:
            tick_dates.append(current_date)
            current_date = current_date + pd.DateOffset(years=period)

        tick_values = [QDateTime(date).toMSecsSinceEpoch() for date in tick_dates]
        axisX.setTickCount(len(tick_values))
        axisX.setRange(start_date_qt, end_date_qt)

        self.chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        # Create and set the Y axis (Price)
        axisY = QValueAxis()
        axisY.setTitleText("Price [PLN]")
        axisY.setLabelFormat("%.2f")
        axisY.setTickCount(10)
        axisY.applyNiceNumbers()
        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart.setAnimationOptions(QChart.AllAnimations)

        axisX.setGridLineVisible(True)
        axisY.setGridLineVisible(True)

        self.chart.legend().setVisible(False)
        series.hovered.connect(self.show_tooltip)

    def show_tooltip(self, point, state):
        if state:
            # Ensure the point.x() is an integer to avoid overflow
            point_x = int(point.x())
            QToolTip.showText(QCursor.pos(),
                              f"Price: {point.y():.2f} PLN\nDate: {QDateTime.fromMSecsSinceEpoch(point_x).toString('dd MMM yyyy')}")
        else:
            QToolTip.hideText()
