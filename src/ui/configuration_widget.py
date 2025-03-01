from PySide6.QtCore import QFile, QObject, Signal
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


class ConfigurationModel(QObject):
    token_changed = Signal(str)
    validity_changed = Signal(bool)
    remote_model_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.github_token = None
        self.github_username = None  # Store username when token is validated
        self.is_token_valid = False  # Track token validity state
        self.remote_model = ""
        self.language = None
        self.theme = None
        self.back_testing = False
        self.max_trades = 0
        self.risk_tolerance = None
        self.history_days = 0

    async def change_remote_model(self, updated_remote_model: str):
        self.remote_model = updated_remote_model
        self.remote_model_changed.emit(self.remote_model)

    async def verify_github_token(
        self, token: str, verification_service: callable
    ):
        """
        Verify GitHub token and update model state
        Returns verification result
        """
        try:
            result = await verification_service.verify_token(token)
            if result.is_valid:
                self.github_token = token
                self.github_username = result.username
                self.is_token_valid = True
            else:
                self.is_token_valid = False

            self.token_changed.emit(self.github_token)
            self.validity_changed.emit(self.is_token_valid)
            return result
        except Exception as e:
            print(f"Error verifying token: {e}")
            self.is_token_valid = False
            return None


class ConfigurationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.github_verification = GitHubTokenVerificationService()
        self._connect_signals()
        self.initialize_model_from_view()

    def _connect_signals(self):
        self.view.add_github_token_button.clicked.connect(
            self.view.add_github_token_input_dialog.show
        )

        self.view.connect_async_signals(
            [
                (
                    self.view.add_github_token_input_dialog,
                    "accepted",
                    self.verify_github_token,
                ),
                (
                    self.view.remote_model_chooser,
                    "currentTextChanged",
                    self.handle_remote_model_change,
                ),
            ]
        )

    def initialize_model_from_view(self):
        """Initialize model values from view's initial state"""
        if self.view.remote_model_chooser.count() > 0:
            initial_model = self.view.remote_model_chooser.itemText(0)
            self.model.remote_model = initial_model

    async def handle_remote_model_change(self, updated_model):
        await self.model.change_remote_model(updated_model)
        print(f"Remote model changed to: {updated_model}")

    async def verify_github_token(self):
        token = self.view.get_token_input()
        # Controller uses service to update model
        await self.model.verify_github_token(token, self.github_verification)
        # Controller updates view based on a result
        self.view.update_token_status(
            self.model.is_token_valid, self.model.github_username
        )


class ConfigurationView(BaseWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

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

    def get_token_input(self):
        return self.add_github_token_input_dialog.findChild(
            QLineEdit, "GitHubTokenLineEdit"
        ).text()

    def clear_token_input(self):
        self.add_github_token_input_dialog.findChild(
            QLineEdit, "GitHubTokenLineEdit"
        ).clear()

    def get_remote_model(self):
        return self.remote_model_chooser.currentText()

    def update_token_status(self, is_valid, username):
        """Update the UI to show GitHub token validation status"""
        if is_valid:
            self.add_github_token_button_label_indicator.setText(
                f"✅ Token added for {username}"
            )
        else:
            self.add_github_token_button_label_indicator.setText(
                "❌ Invalid token"
            )
        self.clear_token_input()

    def _connect_signals(self):
        pass


class ConfigurationWidget(BaseWidget):
    def __init__(self):
        super().__init__()
        self.view = ConfigurationView()
        self.model = ConfigurationModel()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.controller = ConfigurationController(self.model, self.view)

    def _setup_ui(self):
        pass

    def _connect_signals(self):
        pass
