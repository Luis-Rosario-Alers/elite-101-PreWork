from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class FeedbackWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Feedback"))
        self.setLayout(self.layout)
