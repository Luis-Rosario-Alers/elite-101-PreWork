from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from src.utils.file_handling import relative_directory


class ConfigurationWidget(QWidget):
    def __init__(self):
        super().__init__()
        # this needs to be here to load the ui file from a relative context
        ui_path = relative_directory("ui_files", "configuration_widget.ui")
        print(f"Loading UI from: {ui_path}")
        # Load the UI file
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Cannot open {ui_file}: {ui_file.errorString()}")
            exit(-1)

        # Load the UI
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()  # Close the file after loading

        # Set up the layout
        self.layout = QVBoxLayout(self)
        if self.ui:
            self.layout.addWidget(self.ui)
        else:
            print("Failed to load UI")
