from groq import Groq
from app.config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Calls Groq LLM and returns raw text response.
    """
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return completion.choices[0].message.content
