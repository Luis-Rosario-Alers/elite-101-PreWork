import os

import dotenv
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from openai import OpenAI
from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

dotenv.load_dotenv("keys.env")
token = os.getenv("OPEN_API_KEY")
print(token)
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"


class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.chat_output = QTextEdit(self)
        self.chat_output.setReadOnly(True)
        self.layout.addWidget(self.chat_output)

        self.input_line = QLineEdit(self)
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

    def send_message(self):
        user_text = self.input_line.text()
        if not user_text:
            return
        self.chat_output.append(f"\n**User**: {user_text}")
        self.input_line.clear()

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": user_text},
            ],
        )

        reply = response.choices[0].message.content.strip()
        self.display_markdown(reply)

    def display_markdown(self, text):
        html_content = markdown.markdown(
            text,
            extensions=[
                CodeHiliteExtension(linenums=False, css_class="highlight")
            ],
        )
        self.chat_output.setHtml(html_content)
