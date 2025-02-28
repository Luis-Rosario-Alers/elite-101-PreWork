import asyncio
import sys

import dotenv
from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

dotenv.load_dotenv("keys.env")


def main():
    app = QApplication(sys.argv)
    loop = QtAsyncio.QAsyncioEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()


if __name__ == "__main__":
    QtAsyncio.run(main())
