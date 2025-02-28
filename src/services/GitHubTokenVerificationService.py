from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenVerificationResult:
    is_valid: bool = False
    username: Optional[str] = None
    error: Optional[str] = None


"""
class GitHubTokenVerificationService:
    @staticmethod
    async def verify_token(token: str) -> TokenVerificationResult:
        try:
            url = "https://api.github.com/user"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }
            response = requests.get(url, headers=headers)  # noqa

            if response.status_code == 200:
                data = response.json()
                return TokenVerificationResult(
                    is_valid=True, username=data.get("login")
                )
            return TokenVerificationResult(
                is_valid=False,
                error=f"Invalid token (Status: {response.status_code})",
            )

        except requests.RequestException as e:
            return TokenVerificationResult(is_valid=False, error=str(e))
"""
