from openai import OpenAI

BASE_URL = "http://127.0.0.1:53244/v1"
MODEL_NAME = "qwen3-1.7b-generic-cpu"

def main() -> None:
    client = OpenAI(
        base_url=BASE_URL,
        api_key="local",
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
               {
                    "role": "system",
                    "content": (
                        "Sen SkillForge AI isimli Türkçe bir kariyer asistanısın. "
                        "Yalnızca Türkçe cevap ver. "
                        "Kısa, doğal, somut ve tekrar etmeyen cümleler kullan."
                    ),
                },
               {
                    "role": "user",
                    "content": (
                        "/no_think "
                        "Backend geliştirici olmak isteyen bir üniversite öğrencisine "
                        "3 kısa ve somut öneri ver. "
                        "Yalnızca Türkçe cevap ver."
                    ),
                },
            ],
            temperature=0.7,
            max_tokens=250,
        )

        print("\nMODEL CEVABI")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)

    except Exception as error:
        print("\nModel çağrısı sırasında hata oluştu.")
        print(f"Hata türü: {type(error).__name__}")
        print(f"Hata mesajı: {error}")


if __name__ == "__main__":
    main()