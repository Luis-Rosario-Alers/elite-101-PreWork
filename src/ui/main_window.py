from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QSplashScreen,
    QStackedWidget,
    QToolBar,
)

from src.ui.chat_widget import ChatWidget
from src.ui.configuration_widget import ConfigurationWidget
from src.ui.feedback_widget import FeedbackWidget
from src.ui.help_widget import HelpWidget


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(1000, 800))
        # Set all widgets to the main window
        self.stacked_widget = QStackedWidget(self)
        self.chat_page = ChatWidget()
        self.config_page = ConfigurationWidget()
        self.help_page = HelpWidget()
        self.feedback_page = FeedbackWidget()

        self.stacked_widget.addWidget(self.chat_page)  # Index 0
        self.stacked_widget.addWidget(self.config_page)  # Index 1
        self.stacked_widget.addWidget(self.help_page)  # Index 2
        self.stacked_widget.addWidget(self.feedback_page)  # Index 3
        self.setCentralWidget(self.stacked_widget)

        # Create QToolBar and add actions for each tab
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        # Custom style for consistent appearance
        toolbar.setStyleSheet(
            "QToolBar { background-color: #000000; padding: 5px; }"
            "QToolButton { color: white; margin: 3px; }"
        )

        chat_action = QAction("Chat", self)
        chat_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        toolbar.addAction(chat_action)

        config_action = QAction("Configuration", self)
        config_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )
        toolbar.addAction(config_action)

        help_action = QAction("Help", self)
        help_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(2)
        )
        toolbar.addAction(help_action)

        feedback_action = QAction("Feedback", self)
        feedback_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(3)
        )
        toolbar.addAction(feedback_action)

        self.addToolBar(toolbar)
