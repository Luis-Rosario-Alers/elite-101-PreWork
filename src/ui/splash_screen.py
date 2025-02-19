from PySide6.QtWidgets import QSplashScreen
import PySide6.QtGui

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(PySide6.QtGui.QPixmap("images/splash.png"))
        self.show()