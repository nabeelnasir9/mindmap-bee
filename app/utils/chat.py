import openai
from app.core.config import settings
openai.api_key = "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"  # Replace with your OpenAI API key


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
