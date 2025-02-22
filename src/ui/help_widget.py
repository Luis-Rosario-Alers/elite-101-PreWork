from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Help"))
        self.setLayout(self.layout)
