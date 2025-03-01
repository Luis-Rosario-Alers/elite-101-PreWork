import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from src.services.models import RemoteModel
from src.ui.base_widget import BaseWidget


class ChatModel:
    """
    MODEL: Handles data operations and business logic
    Responsible for interacting with the AI model and managing conversation data
    """

    def __init__(self, config_model):
        self.config_model = config_model
        self.token = self.config_model.github_token
        self.model_name = self.config_model.remote_model
        self.conversation_history = []  # Store conversation for context

    async def update_token(self, updated_token=None):
        self.token = updated_token

    @staticmethod
    async def update_validity(updated_validity=None):
        if not updated_validity:
            return "Validity is None"
        return "Validity: {}".format(updated_validity)

    async def update_remote_model(self, updated_model):
        self.model_name = updated_model
        print(f"Chat model updated to: {updated_model}")

    async def get_response(self, prompt):
        """
        Get a response from the AI model

        Returns: LLM response: str
        """
        llm_model = RemoteModel(
            config_model=self.config_model,
            prompt=prompt,
        )

        response = await llm_model.response()
        return response


class ChatView(BaseWidget):
    def __init__(self):
        super().__init__()

    def _setup_ui(self):
        self.chat_output = QTextEdit(self)
        self.chat_output.setReadOnly(True)
        self.input_line = QLineEdit(self)
        self.send_button = QPushButton("Send", self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.chat_output)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.send_button)

    def _connect_signals(self):
        pass

    def display_user_message(self, message):
        """Display the user message in the chat output"""
        self.chat_output.append(f"\n**User**: {message}")

    def display_model_response(self, response):
        """
        Display model response in the chat output
        Convert Markdown to HTML and display in chat output
        """
        html_content = markdown.markdown(
            response,
            extensions=[
                CodeHiliteExtension(linenums=False, css_class="highlight")
            ],
        )
        self.chat_output.setHtml(html_content)

    def get_user_input(self):
        """Get text from the input line"""
        return self.input_line.text()

    def clear_input(self):
        """Clear the input line"""
        self.input_line.clear()


class ChatController:
    def __init__(self, model, view, config_model):
        self.view = view
        self.model = model
        self.config_model = config_model
        self._connect_signals()

    def _connect_signals(self):
        """Connect UI events to controller methods"""
        self.view.connect_async_signals(
            [
                (self.view.send_button, "clicked", self.handle_send_message),
                (
                    self.view.input_line,
                    "returnPressed",
                    self.handle_send_message,
                ),
                (
                    self.config_model,
                    "validity_changed",
                    self.handle_validity_changed,
                ),
                (
                    self.config_model,
                    "token_changed",
                    self.handle_token_changed,
                ),
                (
                    self.config_model,
                    "remote_model_changed",
                    self.handle_remote_model_changed,
                ),
            ]
        )

        # Change methods to accept signal parameters

    async def handle_remote_model_changed(self, model):
        await self.model.update_remote_model(model)
        # eventually, change the model displayed on the chat widget.

    async def handle_validity_changed(self, is_valid):
        await self.model.update_validity(is_valid)
        self.view.display_user_message(
            f"Token validity changed: {'Valid' if is_valid else 'Invalid'}"
        )

    async def handle_token_changed(self, token):
        await self.model.update_token(token)
        self.view.display_user_message("Token updated!")

    async def handle_send_message(self):
        """Handle the send message action"""
        user_input = self.view.get_user_input()
        self.view.display_user_message(user_input)
        self.view.clear_input()

        response = await self.model.get_response(user_input)
        self.view.display_model_response(response)

    async def handle_error(self, error_message):
        """Handle errors and display them in the chat output"""
        self.view.chat_output.append(f"\n**Error**: {error_message}")


class ChatWidget(BaseWidget):
    """
    CHAT WIDGET: Connects the view, model, and controller.
    Also contains Configuration Model for updating its state based on config
    """

    def __init__(self, /, config_model):
        super().__init__()
        self.config_model = config_model
        self.model = ChatModel(self.config_model)
        self.view = ChatView()
        self.controller = ChatController(
            self.model, self.view, self.config_model
        )

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)

    def _setup_ui(self):
        pass

    def _connect_signals(self):
        pass
