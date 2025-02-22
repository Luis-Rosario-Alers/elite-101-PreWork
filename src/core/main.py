import sys

import dotenv
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

dotenv.load_dotenv("keys.env")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
