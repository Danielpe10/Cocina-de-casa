from openai import OpenAI
import config

_client = OpenAI(api_key=config.FIREWORKS_API_KEY, base_url=config.FIREWORKS_BASE_URL)


def ask(prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = _client.chat.completions.create(
        model=config.FIREWORKS_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


SYSTEM_VOICE = (
    f"Eres el asistente de {config.RESTAURANT_NAME} en {config.RESTAURANT_CITY}. "
    "Eres cálido, eficiente y bilingüe (español e inglés). "
    "Hablas como colombiano amigable. Nunca das información falsa."
)
