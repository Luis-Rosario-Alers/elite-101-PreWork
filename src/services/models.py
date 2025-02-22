"""
from openai import OpenAI



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
"""
