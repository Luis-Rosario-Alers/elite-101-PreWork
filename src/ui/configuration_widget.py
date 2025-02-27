from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QPushButton,
    QSlider,
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
        self.configuration_widget = loader.load(ui_file)
        ui_file.close()

        # Setup connections
        self.layout = QVBoxLayout(self)
        self.add_github_token_button = self.configuration_widget.findChild(
            QPushButton, "AddGitHubTokenButton"
        )
        self.add_github_token_button_label_indicator = (
            self.configuration_widget.findChild(
                QLabel, "AddGitHubTokenLabelIndicator"
            )
        )
        self.remote_model_chooser = self.configuration_widget.findChild(
            QComboBox, "RemoteModelChooser"
        )
        self.language_chooser = self.configuration_widget.findChild(
            QComboBox, "LanguageChooser"
        )
        self.theme_chooser = self.configuration_widget.findChild(
            QComboBox, "ThemeChooser"
        )
        self.back_testing_checkbox = self.configuration_widget.findChild(
            QPushButton, "BackTestingCheckBox"
        )
        self.max_trades_slider = self.configuration_widget.findChild(
            QSlider, "MaxTradesSlider"
        )
        self.risk_tolerance_chooser = self.configuration_widget.findChild(
            QComboBox, "RiskToleranceChooser"
        )
        self.history_days_slider = self.configuration_widget.findChild(
            QSlider, "HistoryDaysSlider"
        )
        self.add_github_token_button.clicked.connect(self.addusertoken)

        self.layout.addWidget(self.configuration_widget)

    def addusertoken(self):
        print("GitHub token added")
        self.add_github_token_button_label_indicator.setText("Token added ✅")
