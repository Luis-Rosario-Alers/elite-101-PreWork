from abc import ABC

from azure.ai.inference.aio import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from src.services.GitHubTokenVerificationService import TokenVerificationResult


class BaseModel(ABC):
    def __init__(self):
        self._is_enabled = False

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value: bool) -> None:
        self._is_enabled = value


class RemoteModel(BaseModel):
    def __init__(self, model: str, token: str, prompt: str, model_mode):
        super().__init__()
        self.model = model
        self.token = token
        self.endpoint = "https://models.inference.ai.azure.com"
        self.prompt = prompt
        self.model_mode = model_mode
        self.is_enabled = TokenVerificationResult.is_valid
        print(self.is_enabled)
        if self.is_enabled:
            self.client = ChatCompletionsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.token),
                model=self.model,
            )

    async def response(self):
        if self.is_enabled:
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
        else:
            return None
