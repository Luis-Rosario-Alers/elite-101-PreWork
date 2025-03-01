import asyncio
import sys

import dotenv
import qasync
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

dotenv.load_dotenv("keys.env")


def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
