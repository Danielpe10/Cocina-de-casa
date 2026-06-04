import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)
_model = genai.GenerativeModel("gemini-1.5-flash")


def ask(prompt: str, system: str = "") -> str:
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    response = _model.generate_content(full_prompt)
    return response.text.strip()


SYSTEM_VOICE = (
    f"Eres el asistente de {config.RESTAURANT_NAME} en {config.RESTAURANT_CITY}. "
    "Eres cálido, eficiente y bilingüe (español e inglés). "
    "Hablas como colombiano amigable. Nunca das información falsa."
)
