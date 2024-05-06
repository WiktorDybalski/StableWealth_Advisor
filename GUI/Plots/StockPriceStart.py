from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StockPriceChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(StockPriceChart, self).__init__(fig)
        self.setParent(parent)

    def plot(self, data):
        """Plot the stock price data (list of tuples: [(Date, price), ...])"""
        dates, prices = zip(*data)
        self.axes.clear()
        self.axes.plot(dates, prices, marker='o')
        self.axes.set_xlabel("Date")
        self.axes.set_ylabel("Price")
        self.axes.set_title("Stock Prices")
        self.draw()

