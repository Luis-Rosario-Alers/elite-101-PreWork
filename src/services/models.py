from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from PySide6.QtCore import QObject, Signal


class RemoteModel(QObject):
    response_ready = Signal(str)
    response_error = Signal(str)

    def __init__(self, config_model, prompt):
        QObject.__init__(self)
        self.config_model = config_model
        self.model = self.config_model.remote_model
        self.token = self.config_model.github_token
        self.endpoint = "https://models.inference.ai.azure.com"
        self.prompt = prompt
        self.is_enabled = self.config_model.is_token_valid
        print(self.is_enabled)

    async def response(self):
        if not self.is_enabled:
            return "Model is not enabled, please check your settings..."
        async with ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
            model=self.model,
        ) as client:
            try:
                response = await client.complete(
                    messages=[
                        SystemMessage("You are a helpful assistant."),
                        UserMessage(self.prompt),
                    ]
                )
                response_text = response.choices[0].message.content
                return response_text
            except Exception as e:
                print(e)
                return None
