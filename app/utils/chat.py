import openai
from app.core.config import settings


def chat_with_gpt(query: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Update to use the correct GPT-4 model
            messages=[
                {"role": "user", "content": query}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        # Log the error appropriately and raise an informative error
        return f"Error: {str(e)}"