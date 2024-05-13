import pandas as pd
from PySide6.QtCharts import QChart, QLineSeries, QChartView
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter


class StockPriceChart(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart = QChart()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

    def plot(self, df):
        print(df.columns)
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Provided data is not a pandas DataFrame")

        series = QLineSeries()
        for index, row in df.iterrows():
            if pd.notna(row.iloc[1]):
                date = QDateTime.fromString(str(row['Date'])[:10], 'yyyy-MM-dd')
                price = float(row.iloc[1])
                series.append(date.toMSecsSinceEpoch(), price)

        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Stock Price Over Time")
