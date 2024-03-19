import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton


def create_window():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("StableWealth_Advisor")
    window.setGeometry(200, 200, 800, 600)
    label = QLabel('<font size="30">Hello in StableWealth Advisor!!!', parent=window)
    label.move(200, 15)

    button1 = QPushButton('Markowitz', window)
    button1.move(10, 10)
    button1.clicked.connect(lambda: print("Markowitz"))
    button2 = QPushButton('Calculator', window)
    button2.move(10, 40)
    button2.clicked.connect(lambda: print("Calculator"))

    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    create_window()
