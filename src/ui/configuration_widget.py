from PySide6.QtCore import QFile, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from src.services.GitHubTokenVerificationService import (
    GitHubTokenVerificationService,
)
from src.ui.base_widget import BaseWidget
from src.utils.file_handling import relative_directory


class ConfigurationModel:
    def __init__(self):
        self.github_token = None
        self.remote_model = None
        self.language = None
        self.theme = None
        self.back_testing = False
        self.max_trades = 0
        self.risk_tolerance = None
        self.history_days = 0
        self.GitHubVerification = GitHubTokenVerificationService()


class ConfigurationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        self.view.add_github_token_button.clicked.connect(
            self.view.add_github_token
        )


class ConfigurationView(BaseWidget):
    def __init__(self):
        super().__init__()

    def _setup_ui(self):
        loader = QUiLoader()
        self.configuration_widget = loader.load(
            QFile(relative_directory("ui_files", "configuration_widget.ui")),
            self,
        )
        self.add_github_token_input_dialog = loader.load(
            QFile(relative_directory("ui_files", "github_token_input_box.ui")),
            self,
        )

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.configuration_widget)

        # Find Child Widgets
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

    def _connect_signals(self):
        pass


class ConfigurationWidget(BaseWidget):
    def __init__(self):
        super().__init__()
        self.view = ConfigurationView()
        self.model = ConfigurationModel()
        self.controller = ConfigurationController(self.view, self.model)

    def _setup_ui(self):
        pass

    def _connect_signals(self):
        pass

    @Slot(result=bool)
    async def add_github_token(self) -> bool:
        token = self.add_github_token_input_dialog.findChild(
            QLineEdit, "GitHubTokenLineEdit"
        ).text()

        result = await self.GitHubVerification.verify_token(token)
        if result.is_valid:
            self.add_github_token_button_label_indicator.setText(
                f"✅ Token added for {result.username}"
            )
            return True
        else:
            self.add_github_token_button_label_indicator.setText(
                f"❌ Error: {result.error}"
            )
            return False
