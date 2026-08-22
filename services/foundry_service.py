from openai import OpenAI
import re


BASE_URL = "http://127.0.0.1:64789/v1"

MODEL_NAME = "Phi-4-mini-instruct-generic-cpu"


client = OpenAI(
    base_url=BASE_URL,
    api_key="local",
)


def clean_model_output(text: str) -> str:
    """
    Model cevabındaki kullanıcıya gösterilmemesi gereken
    reasoning etiketlerini ve gereksiz boşlukları temizler.
    """

    if not text:
        return ""

    # Olası <think>...</think> bloklarını kaldır
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    text = text.replace("<think>", "")
    text = text.replace("</think>", "")

    return text.strip()


def generate_answer(prompt: str) -> str:
    """
    Foundry Local üzerindeki Phi-4 Mini modelini kullanarak
    kullanıcıya gösterilecek nihai cevabı üretir.
    """

    if not prompt.strip():
        return "Geçerli bir soru veya içerik gönderilmedi."

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen SkillForge AI adlı Türkçe bir CV analiz "
                        "ve kariyer asistanısın. "
                        "Kullanıcının sorusuna doğrudan ve profesyonel cevap ver. "
                        "Yalnızca nihai cevabı yaz. "
                        "Düşünme sürecini, talimatları veya görev açıklamasını "
                        "kullanıcıya gösterme. "
                        "Gereksiz tekrar yapma. "
                        "Aynı ifadeyi art arda kullanma."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.2,
            max_tokens=500,
        )

        answer = response.choices[0].message.content

        answer = clean_model_output(answer)

        if not answer:
            return "Model geçerli bir cevap üretemedi."

        return answer

    except Exception as error:
        raise RuntimeError(
            f"Phi-4 Mini model çağrısı başarısız oldu: {error}"
        ) from error