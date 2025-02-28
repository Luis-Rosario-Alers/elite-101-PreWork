import os

import dotenv
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

dotenv.load_dotenv("keys.env")
token = os.getenv("OPEN_API_KEY")
print(token)
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"


class ChatModel:
    """
    MODEL: Handles data operations and business logic
    Responsible for interacting with the AI model and managing conversation data
    """

    def __init__(self, api_token=token, model_name=model_name):
        self.token = api_token
        self.model_name = model_name
        self.conversation_history = []  # Store conversation for context

    async def get_response(self, prompt):
        """
        Get a response from the AI model
        Returns a dict containing the response text and validity status
        """
        # Create and call the AI model
        llm_model = RemoteModel(
            model=self.model_name,
            token=self.token,
            prompt=prompt,
            model_mode="chat",
        )
        response = await llm_model.response()

        # Store conversation for history/context
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append(
            {"role": "assistant", "content": response}
        )

        return {"text": response, "is_valid": llm_model.is_enabled}


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
        self.chat_output.append(f"\n**User**: {message}")

    def display_model_response(self, response):
        """Display model response in the chat output"""
        if response["is_valid"]:
            self.render_markdown(response["text"])
        else:
            self.chat_output.append("**Model**: Github token is invalid")

    def render_markdown(self, text):
        """Convert Markdown to HTML and display in chat output"""
        html_content = markdown.markdown(
            text,
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
    def __init__(self, model, view):
        self.view = view
        self.model = model
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
            ]
        )

    async def handle_send_message(self):
        """Handle the send message action"""
        # Get user input from view
        user_text = self.view.get_user_input()
        if not user_text:
            return

        # Update view with a user message
        self.view.display_user_message(user_text)
        self.view.clear_input()

        # Get response from the model
        response = await self.model.get_response(user_text)

        # Update view with model response
        self.view.display_model_response(response)


class ChatWidget(BaseWidget):
    def __init__(self, /):
        super().__init__()
        self.model = ChatModel()
        self.view = ChatView()
        self.controller = ChatController(self.model, self.view)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)

    def _setup_ui(self):
        pass

    def _connect_signals(self):
        pass
