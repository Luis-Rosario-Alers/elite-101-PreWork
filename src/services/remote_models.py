from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential


class RemoteModel:
    def __init__(self, model: str, token: str, prompt: str, model_mode=""):
        self.model = model
        self.token = token
        self.endpoint = "https://models.inference.ai.azure.com"
        self.prompt = prompt
        self.model_mode = model_mode
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
            model=self.model,
        )

    async def response(self):
        try:
            response = await self.client.complete(
                messages=[
                    SystemMessage(self.model_mode),
                    UserMessage(self.prompt),
                ]
            )
        except Exception as e:
            print(f"Error: {e}")
            return None
        return response
