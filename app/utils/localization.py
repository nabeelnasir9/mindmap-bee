from googletrans import Translator

translator = Translator()

def translate_text(content: str, target_language: str) -> str:
    translated = translator.translate(content, dest=target_language)
    return translated.text
