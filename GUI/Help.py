from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QFile, Signal

from Utils import Utils


class Help(QWidget):
    home_requested = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self._init_ui()

    def _init_ui(self):
        """Setup the layout and widgets of the home screen."""
        self.layout = QVBoxLayout()
        self.create_middle_part(self.layout)
        self.setLayout(self.layout)

    def setup_styles(self):
        """Read and apply the CSS stylesheet to the window."""
        style_file = QFile(Utils.get_absolute_file_path("HomeWindowStyle.qss"))
        style_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = str(style_file.readAll(), encoding='utf-8')
        self.setStyleSheet(style_sheet)

    def create_middle_part(self, layout):
        """Create and set up the central part of the home widget."""
        middle_widget = QWidget()
        middle_widget.setObjectName("middle_widget")
        middle_layout = QVBoxLayout()
        middle_widget.setLayout(middle_layout)

        layout.addWidget(middle_widget, 60)

    def emit_home_requested(self):
        """Emit a signal to indicate a request to go to the home window."""
        self.home_requested.emit()