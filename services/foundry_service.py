from openai import OpenAI

BASE_URL = "http://127.0.0.1:61652/v1"
MODEL_NAME = "qwen3-1.7b-generic-cpu"


def get_client() -> OpenAI:
    return OpenAI(
        base_url=BASE_URL,
        api_key="local",
    )


def generate_answer(prompt: str) -> str:
    client = get_client()

    response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": (
                "Sen SkillForge AI isimli Türkçe bir kariyer asistanısın. "
                "Yalnızca Türkçe cevap ver. "
                "En fazla 3 madde yaz. "
                "Her madde en fazla 2 cümle olsun. "
                "Aynı ifadeyi tekrar etme."
            ),
        },
        {
            "role": "user",
            "content": f"/no_think {prompt}",
        },
    ],
    temperature=0.3,

    max_tokens=180,
)
    return response.choices[0].message.content