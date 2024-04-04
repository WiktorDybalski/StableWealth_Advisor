import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGraphicsDropShadowEffect, QPlainTextEdit, QTextEdit)
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(QMargins(10, 10, 10, 10))
        self.centerWindow()

        # Top bar with title
        self.titleLabel = QLabel("StableWealth Advisor Dashboard")
        self.layout.addWidget(self.titleLabel)

        # Content area
        self.contentArea = QHBoxLayout()
        self.layout.addLayout(self.contentArea)

        # Left panel with buttons and info
        self.leftPanel = QVBoxLayout()
        self.contentArea.addLayout(self.leftPanel, 1)

        # Adding buttons with their callbacks and respective content
        self.addButton("Markowitz", "Your assistant in Portfolio Management!", "Portfolio Management Information...")
        self.addButton("Calculator", "Calculate your future wealth!", "Future Wealth Calculator...")

        # Right panel initially with Matplotlib chart
        self.chart = DynamicMplCanvas()
        self.contentWidget = self.chart
        self.contentArea.addWidget(self.contentWidget, 2)

        self.applyStyles()

    def addButton(self, text, tooltip, content):
        button = QPushButton(text)
        button.setToolTip(tooltip)
        button.clicked.connect(lambda: self.showContent(content))
        self.leftPanel.addWidget(button)

    def applyStyles(self):
        shadowEffect = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3, color=QColor(0, 0, 0, 150))
        self.titleLabel.setGraphicsEffect(shadowEffect)

    def centerWindow(self):
        screen = QApplication.primaryScreen().geometry()
        width = int(screen.width() * 0.7)
        height = int(screen.height() * 0.8)
        self.setGeometry((screen.width() - width) // 2, (screen.height() - height) // 2, width, height)

    def showContent(self, content):
        # Check if we're trying to display the same type of content (e.g., text again)
        if isinstance(self.contentWidget, QTextEdit) and not isinstance(content, FigureCanvas):
            self.contentWidget.setPlainText(content)
        else:
            # Remove the existing content widget and replace it with new content
            if self.contentWidget is not None:
                self.contentArea.removeWidget(self.contentWidget)
                self.contentWidget.deleteLater()
            if isinstance(content, str):
                self.contentWidget = QPlainTextEdit(content)
                self.contentWidget.setReadOnly(True)
            elif isinstance(content, FigureCanvas):
                self.contentWidget = content
            self.contentArea.addWidget(self.contentWidget, 2)


class DynamicMplCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(20, 10))
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.timer = self.new_timer(1000, [(self.update_figure, (), {})])
        self.timer.start()

    def update_figure(self):
        self.axes.clear()
        self.axes.plot([0, 1, 2, 3, 4], [0, 1, 0, 1, 0], 'r')
        self.draw()


def main():
    app = QApplication(sys.argv)
    mainWidget = DashboardWidget()
    mainWidget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
