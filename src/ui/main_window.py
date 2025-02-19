import time
from PySide6.QtWidgets import QMainWindow
from src.ui.splash_screen import SplashScreen
from PySide6.QtWidgets import QApplication

class MainWindow(QMainWindow)::
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 800, 600)
        self.show_splash_screen()

    def show_splash_screen(self):
        app = QApplication.instance()
        self.splash_screen.show()
        app.processEvents()
        time.sleep(2)
        self.splash_screen.close()
        self.show()


    def __init__(self)




