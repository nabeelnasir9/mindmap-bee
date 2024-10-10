import openai
from app.core.config import settings
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print(os.getenv("OPENAI_API_KEY"))


def chat_with_gpt(query: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": query}], max_tokens=1000
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"
