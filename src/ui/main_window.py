from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QSplashScreen,
    QStackedWidget,
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
        self.menu_bar = None
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(1000, 800))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.config_page = ConfigurationWidget()
        self.chat_page = ChatWidget(self.config_page.model)
        self.help_page = HelpWidget()
        self.feedback_page = FeedbackWidget()

        self.stacked_widget.addWidget(self.chat_page)
        self.stacked_widget.addWidget(self.config_page)
        self.stacked_widget.addWidget(self.help_page)
        self.stacked_widget.addWidget(self.feedback_page)

        self.setup_menu()

    def setup_menu(self):
        self.menu_bar = QMenuBar(self)

        chat_action = QAction("Chat", self)
        chat_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.chat_page)
        )

        config_action = QAction("Configuration", self)
        config_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.config_page)
        )

        help_action = QAction("Help", self)
        help_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.help_page)
        )

        feedback_action = QAction("Feedback", self)
        feedback_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.feedback_page)
        )

        self.menu_bar.addAction(chat_action)
        self.menu_bar.addAction(config_action)
        self.menu_bar.addAction(help_action)
        self.menu_bar.addAction(feedback_action)

        self.menu_bar.setStyleSheet(
            "QMenuBar { background-color: #000000; padding: 5px; }"
            "QMenu { color: white; margin: 3px; }"
        )
        self.setMenuBar(self.menu_bar)
